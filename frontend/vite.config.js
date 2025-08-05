import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {  // Toutes les requêtes vers /api seront redirigées
        target: 'http://localhost:8000',  // URL de votre serveur Django
        changeOrigin: true,
        secure: false,
        rewrite: path => path.replace(/^\/api/, '') // Optionnel : supprime /api dans la requête Django
      },
    },
  },
});
