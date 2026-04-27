import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";
import wasm from "vite-plugin-wasm";
import topLevelAwait from "vite-plugin-top-level-await";
import { createSvg } from "./src/icons/index";
// import legacy from "@vitejs/plugin-legacy";

export default defineConfig({
  appType: "spa",
  resolve: {
    alias: [
      {
        find: "@",
        replacement: path.resolve(__dirname, "src")
      }
    ]
  },
  plugins: [
    vue(),
    wasm(),
    topLevelAwait(),
    createSvg("./src/icons/svg/"),
    // legacy({
    //   targets: ["defaults", "not IE 11"]
    // })
  ],
  build: {
    minify: "terser",
    brotliSize: false,
    sourcemap: false,
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000", // 确保这里的Flask服务器地址和端口正确
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, "")
      }
    }
  },
  define: {
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false
  }
});
