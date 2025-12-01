import torch
import torchvision
import torch.nn as nn
from tqdm import tqdm
import multiprocessing
import torch.optim as optim
import torch.nn.functional as F
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import random
import numpy as np
import os

print("Torch version:", torch.__version__)

# Set random seed for reproducibility
SEED = 777
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

# Calculate mean and std from the training dataset instead of hardcoding
print("Calculating MNIST mean and std...")
# Download/Load data just for calculation
temp_train_data = torchvision.datasets.MNIST('.data/', train=True, download=True, transform=transforms.ToTensor())

# Stack all images to calculate statistics
# data is (N, H, W), we need to normalize to [0, 1] first as ToTensor does
data = temp_train_data.data.float() / 255.0

MNIST_MEAN = (data.mean().item(),)
MNIST_STD = (data.std().item(),)

print(f"Calculated Mean: {MNIST_MEAN}, Std: {MNIST_STD}")

train_transform = transforms.Compose([
    # Data Augmentation: Eliminamos ElasticTransform porque es muy lento en CPU
    # Volvemos a un RandomAffine robusto pero controlado
    transforms.RandomAffine(degrees=12, translate=(0.1, 0.1), scale=(0.9, 1.1), shear=8),
    transforms.ToTensor(),
    transforms.RandomErasing(p=0.1, scale=(0.02, 0.15)), # RandomErasing es más rápido y ayuda a regularizar
    transforms.Normalize(MNIST_MEAN, MNIST_STD)
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(MNIST_MEAN, MNIST_STD)
])

class MNIST_dataset(Dataset):
    
    def __init__(self, partition="train", transform=None):
        print("\nLoading MNIST ", partition, " Dataset...")
        self.partition = partition
        self.transform = transform
        
        if self.partition == "train":
            self.data = torchvision.datasets.MNIST('.data/', train=True, download=True)
        else:
            self.data = torchvision.datasets.MNIST('.data/', train=False, download=True)
        
        print("\tTotal Len.: ", len(self.data), "\n", 50*"-")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image = self.data[idx][0]
        image = self.transform(image)
        image = image.view(-1)

        label = self.data[idx][1]
        # Devolvemos el índice de la clase (Long) en lugar de One-Hot
        # Esto es necesario para usar label_smoothing en CrossEntropyLoss de forma eficiente
        label = torch.tensor(label, dtype=torch.long)

        return {"idx": idx, "img": image, "label": label}

class Net(nn.Module):
    def __init__(self, sizes=[[784, 1024], [1024, 1024], [1024, 1024], [1024, 512], [512, 10]], 
                 dropout_rate=0.3, criterion=None):
        super(Net, self).__init__()
        
        self.layers = nn.ModuleList()
        
        for i in range(len(sizes) - 1):
            dims = sizes[i]
            self.layers.append(nn.Linear(dims[0], dims[1]))
            self.layers.append(nn.BatchNorm1d(dims[1]))
            self.layers.append(nn.GELU()) # GELU suele funcionar mejor que ReLU en redes profundas
            self.layers.append(nn.Dropout(dropout_rate))
        
        dims = sizes[-1]
        self.classifier = nn.Linear(dims[0], dims[1])
        self.criterion = criterion
        
        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                # He initialization (Kaiming)
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def forward(self, x, y=None):
        for layer in self.layers:
            x = layer(x)
        x = self.classifier(x)
        
        if y is not None:
            loss = self.criterion(x, y)
            return loss, x
        return x

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

train_dataset = MNIST_dataset(partition="train", transform=train_transform)
test_dataset = MNIST_dataset(partition="test", transform=test_transform)

# Aumentamos el batch_size para acelerar el entrenamiento en GPU
batch_size = 512 

# Configuración segura de workers para Cluster/Compartido
# Intentamos leer de variables de entorno comunes en clusters (SLURM)
if 'SLURM_CPUS_PER_TASK' in os.environ:
    num_workers = int(os.environ['SLURM_CPUS_PER_TASK'])
else:
    # Si no estamos en un job de SLURM, limitamos a 4 para no saturar el nodo de login
    num_workers = min(4, multiprocessing.cpu_count())

print("Num workers configured:", num_workers)

# pin_memory=True acelera la transferencia Host-to-Device
train_dataloader = DataLoader(train_dataset, batch_size, shuffle=True, num_workers=num_workers, pin_memory=True)
test_dataloader = DataLoader(test_dataset, batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)

# Reducimos Label Smoothing a 0.05 para permitir mayor confianza en las predicciones
criterion = nn.CrossEntropyLoss(label_smoothing=0.05)

num_classes = 10
# Arquitectura mas ancha para mayor capacidad (Over-parameterization)
net = Net(
    sizes=[
        [784, 1500], 
        [1500, 1500], 
        [1500, 1000], 
        [1000, 500], 
        [500, num_classes]
    ], 
    dropout_rate=0.2, 
    criterion=criterion
)

print(net)
print("Params: ", count_parameters(net))

# Ajustamos LR inicial a 0.2 debido al aumento del batch_size (Linear Scaling Rule aproximada)
optimizer = optim.SGD(net.parameters(), lr=0.2, momentum=0.9, weight_decay=1e-4)

# Cambiamos a ReduceLROnPlateau para bajar el LR automáticamente cuando la accuracy se estanque
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.2, patience=3, min_lr=1e-6)

net = net.to(device)
epochs = 60

print("\n---- Start Training ----")
best_accuracy = -1
best_epoch = 0

# Inicializamos GradScaler para Mixed Precision Training (AMP)
# Updated to use torch.amp.GradScaler as torch.cuda.amp.GradScaler is deprecated
scaler = torch.amp.GradScaler('cuda')

for epoch in range(epochs):
    
    # TRAIN NETWORK
    train_loss, train_correct = 0, 0
    net.train()
    
    for batch in train_dataloader:
        images = batch["img"].to(device)
        labels = batch["label"].to(device)
        ids = batch["idx"].to('cpu').numpy()
        
        optimizer.zero_grad()
        
        # Usamos autocast para Mixed Precision
        # Updated to use torch.amp.autocast as torch.cuda.amp.autocast is deprecated
        with torch.amp.autocast('cuda'):
            loss, outputs = net(images, labels)
        
        # Escalamos la pérdida y hacemos backward
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        
        # labels ya son índices, no hace falta argmax
        # labels = torch.argmax(labels, dim=1) 
        pred = torch.argmax(outputs, dim=1)
        train_correct += pred.eq(labels).sum().item()
        train_loss += loss.item()

    # scheduler.step() # Movido al final para ReduceLROnPlateau
    # Corregimos la normalizacion del loss (promedio por batch en lugar de por sample total)
    train_loss /= len(train_dataloader) 
    train_accuracy = 100. * train_correct / len(train_dataloader.dataset)
    
    # TEST NETWORK
    test_loss, test_correct = 0, 0
    net.eval()
    
    with torch.no_grad():
        for batch in test_dataloader:
            images = batch["img"].to(device)
            labels = batch["label"].to(device)
            ids = batch["idx"].to('cpu').numpy()
            
            outputs = net(images)
            test_loss += criterion(outputs, labels).item()
            
            # labels ya son índices
            # labels = torch.argmax(labels, dim=1)
            pred = torch.argmax(outputs, dim=1)
            test_correct += pred.eq(labels).sum().item()
    
    test_loss /= len(test_dataloader)
    test_accuracy = 100. * test_correct / len(test_dataloader.dataset)
    
    # Actualizamos el scheduler basándonos en la accuracy de test
    scheduler.step(test_accuracy)
    
    print("[Epoch {:2d}] Train: {:.2f}% | Test: {:.2f}% | Loss: {:.4f} | LR: {:.5f}".format(
        epoch + 1, train_accuracy, test_accuracy, test_loss, optimizer.param_groups[0]['lr']
    ))
    
    if test_accuracy > best_accuracy:
        best_accuracy = test_accuracy
        best_epoch = epoch
        torch.save(net.state_dict(), "best_model_high_acc.pt")

print("\nBEST TEST ACCURACY: ", best_accuracy, " in epoch ", best_epoch)

net.load_state_dict(torch.load("best_model_high_acc.pt"))

test_loss, test_correct = 0, 0
net.eval()

with torch.no_grad():
    with tqdm(iter(test_dataloader), desc="Test " + str(epoch), unit="batch") as tepoch:
        for batch in tepoch:
            images = batch["img"].to(device)
            labels = batch["label"].to(device)
            ids = batch["idx"].to('cpu').numpy()
            
            outputs = net(images)
            test_loss += criterion(outputs, labels).item()
            
            # labels ya son índices
            # labels = torch.argmax(labels, dim=1)
            pred = torch.argmax(outputs, dim=1)
            test_correct += pred.eq(labels).sum().item()

test_loss /= len(test_dataloader)
test_accuracy = 100. * test_correct / len(test_dataloader.dataset)
print(f"Final best acc: {test_accuracy:.2f}")
