import { createStore } from "vuex";
import user from "./user";
import baseUrl from "./baseUrl";
import blog from "./blog";
import { h, ref, type Component } from "vue";
import { defineStore } from "pinia";

export default createStore({
  state: {
    token: "",
    userInfo: JSON.parse(sessionStorage.getItem("userInfo") || "{}")
  },
  getters: {
    getUser: (state) => {
      return state.userInfo;
    }
  },
  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token;
      localStorage.setItem("token", token);
    },
    SET_USERINFO: (state, userInfo) => {
      state.userInfo = userInfo;
      sessionStorage.setItem("userInfo", JSON.stringify(userInfo));
    },
    REMOVE_INFO: (state) => {
      state.token = "";
      state.userInfo = {};
      localStorage.setItem("token", "");
      sessionStorage.setItem("userInfo", "{}");
    }
  },
  actions: {},
  modules: {
    user,
    baseUrl,
    blog
  }
});

export const mainStore = defineStore("main", {
  state: () => {
    return {
      helloPinia: "你好 Pinia!"
    };
  },
  getters: {},
  actions: {}
});

export const useEditorStore = defineStore("editor", () => {
  const headings = ref();
  const activeHeading = ref();
  const editorInstance = ref();
  const setHeadings = (data: string[]) => {
    headings.value = data;
  };
  const setActiveHeading = (data: string[]) => {
    activeHeading.value = data;
  };
  const setEditorInstance = (data: string[]) => {
    console.log(editorInstance.value);

    editorInstance.value = data;
  };
  return {
    headings,
    setHeadings,
    activeHeading,
    setActiveHeading,
    editorInstance,
    setEditorInstance
  };
});
