import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
const API_URL = 'http://127.0.0.1:8000'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server:{
    proxy: {
       "^/tenders": {
         "target": API_URL,
         "ws": true,
         "changeOrigin": true
       },
       "^/admin": {
         "target": API_URL,
         "ws": true,
         "changeOrigin": true
       },
       "^/media": {
         "target": API_URL,
         "ws": true,
         "changeOrigin": true
       },
       "^/send_tender_info": {
        "target": API_URL,
        "ws": true,
        "changeOrigin": true
      },
      "^/tenders_suppliers/{tender_id}": {
        "target": API_URL,
        "ws": true,
        "changeOrigin": true
      },
      "^/supplier_form": {
        "target": API_URL,
        "ws": true,
        "changeOrigin": true
      },
      "^/login": {
        "target": API_URL,
        "ws": true,
        "changeOrigin": true
      },
      "^/registration": {
        "target": API_URL,
        "ws": true,
        "changeOrigin": true
      },
         }
     }
})
