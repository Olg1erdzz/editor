import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import BaseEditor from "../views/BaseEditor.vue";
import PageEditor from "../views/PageEditor.vue";
import PageEditorDeflate from "../views/PageEditorDeflate.vue";
import PageEditorDeflate1 from "../views/PageEditorDeflate.vue";
import SignEditor from "../views/SignEditor.vue";
import DocxEditor from "../views/DocxEditor.vue";
import CommentEditor from "../views/CommentEditor.vue";
import ChangesetEditor from "../views/ChangesetEditor.vue";
import CollaborativeEditor from "../views/CollaborativeEditor.vue";
import PrintEditor from "../views/PrintEditor.vue";
import DiffEditor from "../views/DiffEditor.vue";
import IndexEditor from "../views/indexEditor.vue";
import Layout from "@/views/Layout/index.vue";
import PublicPage from "@/views/PublicPage/index.vue";
import OcrIndexComponent from "@/views/OcrIndexComponent.vue";
import NewDocumentPage from "@/views/NewDocumentPage.vue";
import ManagerPage from "../views/ManagerPage/index.vue";
import VideoManagerPage from "../views/ManagerPage/VideoManagerPage.vue";
import Ocr from "../views/ManagerPage/ocr.vue";
import Ocrhistory from "../views/ManagerPage/history.vue";
import VideoClassify from "../views/OcrIndexComponent.vue";
export const isRememberMe: boolean = localStorage.getItem("isRemembered") == "1";
const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "index",
    component: IndexEditor,
    meta: { showNavbar: true } // 在 Index 页面显示导航栏
  },
  {
    path: "/login",
    name: "login",
    meta: { title: "登录" },
    component: () => import("@/views/login/index.vue")
  },
  {
    path: "/register",
    name: "register",
    meta: { title: "注册" },
    component: () => import("@/views/register/index.vue")
  },
  {
    path: "/forgetPassword",
    name: "forgetPassword",
    meta: { title: "忘记密码" },
    component: () => import("@/views/forgetPassword/index.vue")
  },
  {
    path: "/page2",
    name: "base",
    component: BaseEditor,
    meta: { showNavbar: true }
  },
  {
    path: "/page",
    name: "page",
    component: PageEditor,
    meta: { showNavbar: true }
  },
  {
    path: "/documents/:id",
    name: "DocumentEditor",
    component: PageEditorDeflate,
    props: (route) => {
      const documentQuery = route.query.document;
      let document = {};
      if (typeof documentQuery === "string") {
        try {
          document = JSON.parse(documentQuery);
        } catch (e) {
          console.error("Invalid document query:", documentQuery);
        }
      }
      return { document };
    },
    meta: { showNavbar: true }
  },
  {
    path: "/document/:id",
    name: "Documents",
    component: PageEditorDeflate1,
    props: (route) => {
      const documentQuery = route.query.document;
      let document = {};
      if (typeof documentQuery === "string") {
        try {
          document = JSON.parse(documentQuery);
        } catch (e) {
          console.error("Invalid document query:", documentQuery);
        }
      }
      return { document };
    },
    meta: { showNavbar: true }
  },
  {
    path: "/collaborativeeditor",
    name: "collaborativeeditor",
    component: CollaborativeEditor,
    meta: { showNavbar: true }
  },
  {
    path: "/commenteditor",
    name: "commenteditor",
    component: CommentEditor,
    meta: { showNavbar: true }
  },
  {
    path: "/changeseteditor",
    name: "changeseteditor",
    component: ChangesetEditor,
    meta: { showNavbar: true }
  },
  {
    path: "/print",
    name: "print",
    component: PrintEditor,
    meta: { showNavbar: true }
  },
  {
    path: "/diff",
    name: "diff",
    component: DiffEditor,
    meta: { showNavbar: true }
  },
  {
    path: "/sign",
    name: "sign",
    component: SignEditor,
    meta: { showNavbar: true }
  },
  {
    path: "/docx",
    name: "docx",
    component: DocxEditor,
    meta: { showNavbar: true }
  },
  {
    path: "/about",
    name: "about",
    component: () => import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
    meta: { showNavbar: true }
  },
  {
    path: "/ocrIndexComponent",
    name: "OcrIndexComponent",
    component: OcrIndexComponent,
    meta: { showNavbar: true }
  },
  {
    path: "/new-document-page",
    name: "NewDocumentPage",
    component: NewDocumentPage,
    meta: { showNavbar: true }
  },
  {
    path: "/videoClassify",
    name: "VideoClassify",
    component: VideoClassify
  },
  {
    path: "/layout",
    name: "Layout",
    component: Layout,
    meta: { showNavbar: true },
    redirect: "/publicPage",
    children: [
      {
        path: "/publicPage",
        name: "PublicPage",
        component: PublicPage
      }
    ]
  },
  {
    path: "/managerPage",
    name: "ManagerPage",
    component: ManagerPage,
    redirect: "/videoManagerPage",
    children: [
      {
        path: "/videoManagerPage",
        name: "VideoManagerPage",
        component: VideoManagerPage
      },
      {
        path: "/ocr",
        name: "Ocr",
        component: Ocr
      },
      {
        path: "/ocrhistory",
        name: "Ocrhistory",
        component: Ocrhistory
      }
    ]
  },
  {
    path: "/register",
    name: "register",
    meta: { title: "注册" },
    component: () => import("@/views/register/index.vue")
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
