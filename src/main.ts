import { createApp, h } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import VCalendar from "v-calendar";
import "./index.css";
import axios from "./api/axios"; // 导入配置好的 axios 实例
import CustomHline from "./design/components/custom-hline/index.vue";
import CustomVline from "./design/components/custom-vline/index.vue";
import CustomText from "./design/components/custom-text/index.vue";
import Customimage from "./design/components/custom-image/index.vue";
import Customlogo from "./design/components/custom-logo/index.vue";
import CustomSelect from "./design/components/custom-select/index.vue";
import PageCount from "./design/components/page-count/index.vue";
import "v-calendar/dist/style.css";
import svgIcon from "./icons/index.vue";
import { createPinia } from "pinia";
import 'vue-fullpage.js/dist/style.css';
import VueFullpage from 'vue-fullpage.js';
// import "./assets/text/text.css";
import VideoPlayer from 'vue-video-player'
import 'video.js/dist/video-js.css';
import { MotionPlugin } from '@vueuse/motion';
import 'vue-video-player/src/custom-theme.css';
import "vue-simple-uploader/dist/style.css";
import uploader from "vue-simple-uploader";
const pinia = createPinia();

const app = createApp(App);
// app.config.unwrapInjectedRef = true;
app.use(VCalendar, {});
app.use(ElementPlus);
app.component(CustomHline.name, CustomHline);
app.component(CustomVline.name, CustomVline);

app.component(CustomText.name, CustomText);
app.component(Customimage.name, Customimage);
app.component(Customlogo.name, Customlogo);
app.component(CustomSelect.name, CustomSelect);
app.component(PageCount.name, PageCount);

app.use(uploader); // 加入这一行来使用 vue-simple-uploader 插件
app.component("v-style", {
  render() {
    return h("style", {}, this.$slots.default());
  }
});

for (const [name, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(name, component);
};
app.config.globalProperties.$axios = axios; // 将 axios 实例挂载到 Vue 全局属性
app.use(store).use(pinia).use(MotionPlugin).use(VideoPlayer).use(VueFullpage).component("svg-icon", svgIcon).use(router).mount("#app");
