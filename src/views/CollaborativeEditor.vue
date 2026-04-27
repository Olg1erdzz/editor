<template>
  <footer class="footer footer-center p-4 bg-base-300 text-base-content">
    <div class="chat chat-start">
      <div class="chat-bubble chat-bubble-primary">在线人数+{{ userLenth.length }}</div>
    </div>
    <div class="avatar-group">
      <div class="avatar placeholder slide-in-blurred-left" v-for="(item, index) in user" :key="index">
        <div :style="{ background: item ? item.color : '' }" class="text-neutral-content rounded-full w-24">
          <span>{{ item.name }}</span>
        </div>
      </div>
    </div>
    <button @click="toggleCollaboration" style="margin-left: 1200px;">{{ isCollaborating ? "关闭协同" : "开始协同" }}</button>
    <div v-if="shareCode" style="margin-left: 1200px;">分享码: {{ shareCode }}</div>
    <button @click="openModal" style="margin-left: 1200px;">加入协同</button>
    <div v-if="showModal" style="margin-left: 1200px;">
      <div>
        <span @click="closeModal" class="close">&times;</span><br>
        <input v-model="inputShareCode" type="text" placeholder="请输入分享码" /><br>
        <button @click="joinCollaboration">确定</button>
      </div>
    </div>
  </footer>
  <CassieEditor
    :user="user"
    footer-height="50"
    :body-width="w"
    :body-height="h"
    :content="pageContentHtml"
    :is-paging="false"
    @onCreate="onCreate"
    :collaboration-url="url"
    @onStatus="onStatus"
    @onAwarenessChange="onAwarenessChange"
    @onUpdate="onUpdate"
    :bodyWidth="750"
    :menu-list="menulist"
    :header-data="headerlist"
    :footer-data="footerlist"
  />
</template>

<script lang="ts">
import { getCurrentInstance, ref } from "vue";
import CassieEditor from "../components/CassieEditor.vue";
import { pageContentHtml, headerlist, footerlist } from "./content";
import { getRandomColor, getRandomName } from "@/denoutils";
import { UnitConversion } from "@/extension/page/core";
import * as Y from "yjs";
import { TiptapCollabProvider } from "@hocuspocus/provider";
import { useGetDerivedNamespace } from "element-plus";
import axios from "axios";

const unitConversion = new UnitConversion();
export default {
  components: { CassieEditor },
  data() {
    return {
      isCollaborating: false,
      showModal: false,
      inputShareCode: "",
      shareCode: "",
      userLenth: [],
      user: [],
      url: "ws://39.101.177.50:1234",
      w: unitConversion.mmConversionPx(210),
      h: unitConversion.mmConversionPx(297),
      menulist: [
        { classify: "radio", label: "单选", value: "radio" },
        { classify: "checkbox", label: "多选", value: "checkbox" },
        { classify: "date", label: "日期", value: "date" }
      ],
      ydocA: null ||new Y.Doc,
      providerA: null
      // ...
    };
  },
  methods: {
    toggleCollaboration() {
      this.isCollaborating = !this.isCollaborating;

      if (this.isCollaborating) {
        this.shareCode = Math.random().toString(36).substring(2, 15);
        const color = getRandomColor();
        const username = localStorage.getItem("userName");
        axios.post("http://127.0.0.1:5000/api/start-collaboration", { shareCode: this.shareCode, username: username, color: color });
        // 创建 TiptapCollabProvider 实例
        this.ydocA = new Y.Doc();
        this.providerA = new TiptapCollabProvider({
          appId: "JKV0ED9X",
          name: this.shareCode,
          document: this.ydocA
        });
      } else {
        axios.post("http://127.0.0.1:5000/api/close-collaboration", { shareCode: this.shareCode });
        if (this.providerA) {
          this.providerA.destroy();
          this.providerA = null;
          this.ydocA = null;
        }
        this.shareCode = "";
      }
    },
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    joinCollaboration() {
      if (this.providerA) {
        this.providerA.destroy();
        this.providerA = null;
        this.ydocA = null;
      }
      const username = localStorage.getItem("userName");
      const color = getRandomColor();
      axios.post("http://127.0.0.1:5000/api/join-collaboration", { shareCode: this.inputShareCode, username: username, color: color });
      this.shareCode = this.inputShareCode;
      this.showModal = false;
      this.ydocA = new Y.Doc();
      this.providerA = new TiptapCollabProvider({
        appId: "JKV0ED9X",
        name: this.shareCode,
        document: this.ydocA
      });
    },
    
    quitCollaboration() {
      if (this.providerA) {
        this.providerA.destroy();
        this.providerA = null;
        this.ydocA = null;
      }
      const username = localStorage.getItem("userName");
      const color = g
      axios.post("http://127.0.0.1:5000/api/join-collaboration", { shareCode: this.inputShareCode, username: username, color: color });
      this.shareCode = this.inputShareCode;
      this.showModal = false;
      this.ydocA = new Y.Doc();
      this.providerA = new TiptapCollabProvider({
        appId: "JKV0ED9X",
        name: this.shareCode,
        document: this.ydocA
      });
    },
    onUpdate(output, editor) {},
    onStatus(data, editor) {},
    onCreate(option) {
      console.log(option);
    },
    onAwarenessChange(data) {
      console.log(this.shareCode);
      axios
        .get("http://127.0.0.1:5000/api/get-users", {
          params: {
            shareCode: this.shareCode
          }
        })
        .then((response) => {
          console.log(typeof response);
          console.log(response);
          this.userLenth = response.user.flat();
          console.log(this.userLenth);
          this.user = this.userLenth.map((item) => {
            return { name: item.username, color: item.color };
          }, console.log(this.user));
          console.log(this.user);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }
};
</script>
<style scoped>
.slide-in-blurred-left {
	-webkit-animation: slide-in-blurred-left 0.6s cubic-bezier(0.230, 1.000, 0.320, 1.000) both;
	        animation: slide-in-blurred-left 0.6s cubic-bezier(0.230, 1.000, 0.320, 1.000) both;
}
@-webkit-keyframes slide-in-blurred-left {
  0% {
    -webkit-transform: translateX(-1000px) scaleX(2.5) scaleY(0.2);
            transform: translateX(-1000px) scaleX(2.5) scaleY(0.2);
    -webkit-transform-origin: 100% 50%;
            transform-origin: 100% 50%;
    -webkit-filter: blur(40px);
            filter: blur(40px);
    opacity: 0;
  }
  100% {
    -webkit-transform: translateX(0) scaleY(1) scaleX(1);
            transform: translateX(0) scaleY(1) scaleX(1);
    -webkit-transform-origin: 50% 50%;
            transform-origin: 50% 50%;
    -webkit-filter: blur(0);
            filter: blur(0);
    opacity: 1;
  }
}
@keyframes slide-in-blurred-left {
  0% {
    -webkit-transform: translateX(-1000px) scaleX(2.5) scaleY(0.2);
            transform: translateX(-1000px) scaleX(2.5) scaleY(0.2);
    -webkit-transform-origin: 100% 50%;
            transform-origin: 100% 50%;
    -webkit-filter: blur(40px);
            filter: blur(40px);
    opacity: 0;
  }
  100% {
    -webkit-transform: translateX(0) scaleY(1) scaleX(1);
            transform: translateX(0) scaleY(1) scaleX(1);
    -webkit-transform-origin: 50% 50%;
            transform-origin: 50% 50%;
    -webkit-filter: blur(0);
            filter: blur(0);
    opacity: 1;
  }
}
.close{
  margin-left: 150px;
  margin-bottom: 20px;
  cursor: pointer;
}
.close :hover{
  color: black;
}
</style>: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any: any
