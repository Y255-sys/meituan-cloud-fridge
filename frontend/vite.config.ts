import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      app: path.resolve(__dirname, "./src/app"),
      components: path.resolve(__dirname, "./src/components"),
      features: path.resolve(__dirname, "./src/features"),
      hooks: path.resolve(__dirname, "./src/hooks"),
      lib: path.resolve(__dirname, "./src/lib"),
      pages: path.resolve(__dirname, "./src/pages"),
      services: path.resolve(__dirname, "./src/services"),
      styles: path.resolve(__dirname, "./src/styles"),
      types: path.resolve(__dirname, "./src/types"),
    },
  },
  server: {
    host: "127.0.0.1",
    port: 5173,
  },
});
