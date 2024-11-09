import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // preview: {
  //   proxy: {
  //     '/styles': 'https://api.mapbox.com'
  //   }
  // },
  server: {
    cors: false,
    proxy: {
      '/styles': 'https://api.mapbox.com'
    }
  },
  assetsInclude: ['**/*.JPG'],
})
