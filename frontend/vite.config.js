import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  // This ensures Vite doesn't get confused by the file path
  server: {
    fs: {
      allow: ['..']
    }
  }
})