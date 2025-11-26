from datasets import load_dataset

try:
    dataset = load_dataset("xmj2002/Chinese_modern_classical", streaming=True)
    print("Dataset structure:")
    print(dataset)
    print("\nFirst example from train:")
    # Take the first item from the iterable dataset
    print(next(iter(dataset["train"])))
except Exception as e:
    print(f"Error loading dataset: {e}")
