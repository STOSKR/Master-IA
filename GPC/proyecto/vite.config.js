// vite.config.js
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
    // Es posible que no necesites 'plugins', pero si los usas, déjalos.
    // plugins: [react()], 

    // Esto es lo importante para tu profesor:
    build: {
        sourcemap: true, // Habilita los mapas de código fuente
    }
})