<template>
  <div class="grid grid-rows-[300px_minmax(900,_1fr)_40px] grid-cols-3 gap-3 flex-grow card bg-base-300 rounded-box place-items-center">
    <div class="col-span-3">
      <FileTools :editor="editor" v-if="editor"></FileTools>
    </div>
    <!-- 大纲 -->
    <div class="col-span-1 justify-self-start self-start w-[78%]">
      <Outline></Outline>
    </div>
    <!-- 内容 -->
    <editor-content class="my-2 col-span-1 h-full" :editor="editor" />
    <!-- 右侧 -->
    <div class="col-span-1">
      <!-- left -->
    </div>
    <bubble-menu :editor="editor" :tippy-options="{ duration: 100 }" v-if="editor">
      <div class="flex items-center gap-1 bg-white rounded-xl py-1 px-1 shadow-lg">
        <Menu as="div" class="relative inline-block text-left">
          <div>
            <MenuButton class="inline-flex w-full justify-center gap-x-1.5 rounded-lg bg-white px-3 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              <svg class="h-4 w-4 fill-sky-500" viewBox="0 0 24 24">
                <path
                  fill-rule="evenodd"
                  d="M9 4.5a.75.75 0 01.721.544l.813 2.846a3.75 3.75 0 002.576 2.576l2.846.813a.75.75 0 010 1.442l-2.846.813a3.75 3.75 0 00-2.576 2.576l-.813 2.846a.75.75 0 01-1.442 0l-.813-2.846a3.75 3.75 0 00-2.576-2.576l-2.846-.813a.75.75 0 010-1.442l2.846-.813A3.75 3.75 0 007.466 7.89l.813-2.846A.75.75 0 019 4.5zM18 1.5a.75.75 0 01.728.568l.258 1.036c.236.94.97 1.674 1.91 1.91l1.036.258a.75.75 0 010 1.456l-1.036.258c-.94.236-1.674.97-1.91 1.91l-.258 1.036a.75.75 0 01-1.456 0l-.258-1.036a2.625 2.625 0 00-1.91-1.91l-1.036-.258a.75.75 0 010-1.456l1.036-.258a2.625 2.625 0 001.91-1.91l.258-1.036A.75.75 0 0118 1.5zM16.5 15a.75.75 0 01.712.513l.394 1.183c.15.447.5.799.948.948l1.183.395a.75.75 0 010 1.422l-1.183.395c-.447.15-.799.5-.948.948l-.395 1.183a.75.75 0 01-1.422 0l-.395-1.183a1.5 1.5 0 00-.948-.948l-1.183-.395a.75.75 0 010-1.422l1.183-.395c.447-.15.799-.5.948-.948l.395-1.183A.75.75 0 0116.5 15z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              AI Tools
              <ChevronDownIcon class="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
            </MenuButton>
          </div>

          <transition
            enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
          >
            <MenuItems class="px-2 py-1 absolute left-0 z-10 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
              <div class="py-1">
                <MenuItem v-slot="{ active }" class="rounded-md">
                  <button :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm w-full text-start']">文本摘要</button>
                </MenuItem>
                <MenuItem v-slot="{ active }" class="rounded-md">
                  <div class="relative group text-start font-medium rounded-lg text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20" id="dropdown-cta">
                    <div :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm w-full text-start']" class="rounded-md">文本修饰</div>
                    <ul class="px-2 py-2 text-center z-10 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none hidden absolute left-52 -top-1 border group-hover:block">
                      <button class="hover:bg-gray-100 hover:text-gray-900 text-gray-700 block px-4 py-2 text-sm w-full text-start rounded-md" @click="getSelectedText('简洁')" value="简洁">简洁</button>
                      <button class="hover:bg-gray-100 hover:text-gray-900 text-gray-700 block px-4 py-2 text-sm w-full text-start rounded-md" @click="getSelectedText('生动')" value="生动">生动</button>
                      <button class="hover:bg-gray-100 hover:text-gray-900 text-gray-700 block px-4 py-2 text-sm w-full text-start rounded-md" @click="getSelectedText('强烈')" value="强烈">强烈</button>
                      <button class="hover:bg-gray-100 hover:text-gray-900 text-gray-700 block px-4 py-2 text-sm w-full text-start rounded-md" @click="getSelectedText('委婉')" value="委婉">委婉</button>
                      <button type="button" @click="openModal('自定义风格')" class="hover:bg-gray-100 hover:text-gray-900 text-gray-700 block px-4 py-2 text-sm w-full text-start rounded-md">自定义风格</button>
                    </ul>
                  </div>
                </MenuItem>
                <MenuItem v-slot="{ active }" class="rounded-md">
                  <button :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm w-full text-start']" @click="openModal('文本续写')">文本续写</button>
                </MenuItem>
              </div>
              <div class="py-1">
                <MenuItem v-slot="{ active }" class="rounded-md">
                  <button :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm w-full text-start']">病句改写</button>
                </MenuItem>
                <MenuItem v-slot="{ active }" class="rounded-md">
                  <button :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm w-full text-start']">翻译</button>
                </MenuItem>
              </div>
            </MenuItems>
          </transition>
        </Menu>
        <TransitionRoot appear :show="isOpen" as="template">
          <Dialog as="div" @close="closeModal" class="relative z-10">
            <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0" enter-to="opacity-100" leave="duration-200 ease-in" leave-from="opacity-100" leave-to="opacity-0">
              <div class="fixed inset-0 bg-black/25" />
            </TransitionChild>

            <div class="fixed inset-0 overflow-y-auto">
              <div class="flex min-h-full items-center justify-center p-4 text-center">
                <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0 scale-95" enter-to="opacity-100 scale-100" leave="duration-200 ease-in" leave-from="opacity-100 scale-100" leave-to="opacity-0 scale-95">
                  <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                    <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 text-center">
                      {{ modalTitle }}
                    </DialogTitle>
                    <div class="relative w-full min-w-[200px] h-10 my-4">
                      <input
                        v-model="inputModel"
                        class="peer w-full h-full bg-transparent text-blue-gray-700 font-sans font-normal outline outline-0 focus:outline-0 disabled:bg-blue-gray-50 disabled:border-0 transition-all placeholder-shown:border placeholder-shown:border-blue-gray-200 placeholder-shown:border-t-blue-gray-200 border focus:border-2 border-t-transparent focus:border-t-transparent text-sm px-3 py-2.5 rounded-[7px] border-blue-gray-200 focus:border-blue-500"
                        placeholder=" "
                      /><label
                        class="flex w-full h-full select-none pointer-events-none absolute left-0 font-normal !overflow-visible truncate peer-placeholder-shown:text-blue-gray-500 leading-tight peer-focus:leading-tight peer-disabled:text-transparent peer-disabled:peer-placeholder-shown:text-blue-gray-500 transition-all -top-1.5 peer-placeholder-shown:text-sm text-[11px] peer-focus:text-[11px] before:content[' '] before:block before:box-border before:w-2.5 before:h-1.5 before:mt-[6.5px] before:mr-1 peer-placeholder-shown:before:border-transparent before:rounded-tl-md before:border-t peer-focus:before:border-t-2 before:border-l peer-focus:before:border-l-2 before:pointer-events-none before:transition-all peer-disabled:before:border-transparent after:content[' '] after:block after:flex-grow after:box-border after:w-2.5 after:h-1.5 after:mt-[6.5px] after:ml-1 peer-placeholder-shown:after:border-transparent after:rounded-tr-md after:border-t peer-focus:after:border-t-2 after:border-r peer-focus:after:border-r-2 after:pointer-events-none after:transition-all peer-disabled:after:border-transparent peer-placeholder-shown:leading-[3.75] text-blue-gray-400 peer-focus:text-blue-500 before:border-blue-gray-200 peer-focus:before:!border-blue-500 after:border-blue-gray-200 peer-focus:after:!border-blue-500"
                      >
                        {{ inputLable }}
                      </label>
                    </div>

                    <div class="mt-4">
                      <button
                        type="button"
                        class="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                        @click="
                          closeModal();
                          currentMethod === 'getSelectedText' ? getSelectedText(textInputStyle) : extend(length);
                        "
                      >
                        确定
                      </button>
                    </div>
                  </DialogPanel>
                </TransitionChild>
              </div>
            </div>
          </Dialog>
        </TransitionRoot>

        <button
          class="flex select-none items-center gap-2 rounded-lg py-1 px-2 text-center align-middle font-sans text-xs font-bold uppercase text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
          type="button"
          data-ripple-dark="true"
          @click="editor.chain().focus().toggleBold().run()"
          :class="{ 'is-active': editor.isActive('Bold') }"
        >
          <svg-icon name="bold" color="black"></svg-icon>
        </button>
        <button
          class="flex select-none items-center gap-2 rounded-lg py-1 px-2 text-center align-middle font-sans text-xs font-bold uppercase text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
          type="button"
          data-ripple-dark="true"
          @click="editor.chain().focus().toggleItalic().run()"
          :class="{ 'is-active': editor.isActive('italic') }"
        >
          <svg-icon name="italic" color="black"></svg-icon>
        </button>
        <button
          class="flex select-none items-center gap-2 rounded-lg py-1 px-2 text-center align-middle font-sans text-xs font-bold uppercase text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
          type="button"
          data-ripple-dark="true"
          @click="editor.chain().focus().toggleUnderline().run()"
          :class="{ 'is-active': editor.isActive('underline') }"
        >
          <svg-icon name="underline" color="black"></svg-icon>
        </button>
        <button
          class="flex select-none items-center gap-2 rounded-lg py-1 px-2 text-center align-middle font-sans text-xs font-bold uppercase text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
          type="button"
          data-ripple-dark="true"
          @click="editor.chain().focus().toggleStrike().run()"
          :class="{ 'is-active': editor.isActive('strike') }"
        >
          <svg-icon name="Strikethrough" color="black"></svg-icon>
        </button>
        <button
          class="flex select-none items-center gap-2 rounded-lg py-1 px-2 text-center align-middle font-sans text-xs font-bold uppercase text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
          type="button"
          data-ripple-dark="true"
          @click="editor.chain().focus().toggleCode().run()"
          :class="{ 'is-active': editor.isActive('underline') }"
        >
          <svg-icon name="code" color="black"></svg-icon>
        </button>
        <button
          class="flex select-none items-center gap-2 rounded-lg py-1 px-2 text-center align-middle font-sans text-xs font-bold uppercase text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
          type="button"
          data-ripple-dark="true"
          @click="editor.chain().focus().toggleCodeBlock().run()"
          :class="{ 'is-active': editor.isActive('underline') }"
        >
          <svg-icon name="codeblock" color="black"></svg-icon>
        </button>
      </div>

      <!-- stylesheet -->

      <!-- Ripple Effect from cdn -->
    </bubble-menu>
    <div class="bottomcount col-span-3">
      字数统计:
      {{ editor?.storage.characterCount.characters() }}
    </div>
  </div>
</template>

<script lang="ts">
import applyDevTools from "prosemirror-dev-tools";
import { pageContent, headerlist, footerlist, pageContentHtml, resumeTemplate } from "./content";
import { UnitConversion } from "@/extension/page/core";
import { BubbleMenu, EditorContent, Editor } from "@tiptap/vue-3";
import { onBeforeUnmount, onMounted, PropType, reactive, ref, shallowRef, unref, watchEffect, h, type Component } from "vue";
import { BuildRender, ContextMenuOptions } from "@/default";
import { CassieKit } from "@/extension";
import { storeToRefs } from "pinia";
import { useEditorStore } from "@/store";

import FileTools from "./filetools/FileTools.vue";
// 图片编辑
import ImageResize from "tiptap-extension-resize-image";
// 回退
import History from "@tiptap/extension-history";
// 文字样式
import TextStyle from "@tiptap/extension-text-style";
// 字数统计
import CharacterCount from "@tiptap/extension-character-count";

import Outline from "./outline/index.vue";

import { useTextmenuCommands } from "./bubblemenu/hooks/useTextmenuCommands";

import { UndoRound, MoreHorizOutlined } from "@vicons/material";
import { post } from "@/request/api";
import axios from "axios";
import { Menu, MenuButton, MenuItem, MenuItems, TransitionRoot, TransitionChild, Dialog, DialogPanel, DialogTitle } from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
const unitConversion = new UnitConversion();
export default {
  components: {
    EditorContent,
    FileTools,
    BubbleMenu,
    Outline,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    ChevronDownIcon
  },
  data() {
    return {
      isOpen: false,
      modalTitle: "",
      currentMethod: "",
      inputLable: "",
      length: "",
      textInputStyle: "" // 绑定输入框的数据
    };
  },
  computed: {
    inputModel: {
      get() {
        // 根据 currentMethod 返回相应的数据属性
        return this.currentMethod === "getSelectedText" ? this.textInputStyle : this.length;
      },
      set(value: string) {
        // 根据 currentMethod 设置相应的数据属性
        if (this.currentMethod === "getSelectedText") {
          this.textInputStyle = value;
        } else {
          this.length = value;
        }
      }
    }
  },
  methods: {
    closeModal() {
      this.isOpen = false;
    },
    openModal(type: string) {
      this.isOpen = true;
      // 根据按钮类型设置模态框标题
      if (type === "自定义风格") {
        this.modalTitle = "请输入您需要的文本风格";
        this.inputLable = "输入风格";
        this.currentMethod = "getSelectedText";
      } else if (type === "文本续写") {
        this.modalTitle = "请输入需要续写的字数";
        this.inputLable = "输入字数";
        this.currentMethod = "extend";
      }
    }
  },
  setup() {
    let bodyWidth = unitConversion.mmConversionPx(210);
    let h = unitConversion.mmConversionPx(297);
    const menulist = [
      { classify: "radio", label: "单选", value: "radio" },
      {
        classify: "checkbox",
        label: "多选",
        value: "checkbox"
      },
      {
        classify: "date",
        label: "日期",
        value: "date"
      }
    ];
    const onUpdate = (output: any, editor: any) => {};
    const onCreate = (option: any) => {
      console.log(option);
    };
    const editor = shallowRef<Editor>();

    // 获取当前光标选中文本并发送给后端替换
    const getSelectedText = async (style: string) => {
      if (editor.value) {
        const { from, to, empty } = editor.value.state.selection;
        if (!empty) {
          const selectedText = editor.value.state.doc.textBetween(from, to, " ");
          console.log(selectedText);
          console.log("自定义文本风格");
          try {
            const response = await axios.post(
              "http://127.0.0.1:5000/api/polish",
              {
                text: selectedText,
                style: style
              },
              {
                headers: {
                  "Content-Type": "application/json"
                }
              }
            );
            console.log(response);
            const processedText = response; // 假设这是后端返回的字段
            if (editor.value) {
              editor.value.commands.insertContent(processedText);
              // editor.value.commands.setContent(processedText);
            }
          } catch (error) {
            if (error instanceof Error) {
              console.error(error.message);
            } else {
              console.error("未知错误", error);
            }
          }
        }
      }
    };

    // 续写
    const extend = async (length: string) => {
      if (editor.value) {
        const { from, to, empty } = editor.value.state.selection;
        if (!empty) {
          const selectedText = editor.value.state.doc.textBetween(from, to, " ");
          console.log(selectedText);
          console.log("自定义续写字数");
          try {
            const response = await axios.post(
              "http://127.0.0.1:5000/api/extend",
              {
                text: selectedText,
                length: length
              },
              {
                headers: {
                  "Content-Type": "application/json"
                }
              }
            );
            console.log(response);
            const processedText = response; // 假设这是后端返回的字段
            if (editor.value) {
              editor.value.commands.insertContent(processedText);
              // editor.value.commands.setContent(processedText);
            }
          } catch (error) {
            if (error instanceof Error) {
              console.error(error.message);
            } else {
              console.error("未知错误", error);
            }
          }
        }
      }
    };

    onMounted(() => {
      let rippleScript = document.createElement("script");
      rippleScript.setAttribute("src", "https://unpkg.com/@material-tailwind/html@latest/scripts/ripple.js");
      document.head.appendChild(rippleScript);
      //如果是协作模式 设置 content需要滞后 否则会重复添加
      editor.value = new Editor({
        onUpdate({ editor }) {
          loadHeadings();
          // editorStore.setEditorInstance(editor.value)
          //console.log(editor.getHTML());
        },
        onCreate({ editor }) {
          loadHeadings();
          // editorStore.setEditorInstance(editor.value)
        },
        editable: true,
        content: resumeTemplate,
        editorProps: {
          attributes: {
            class: ""
          }
        },
        injectCSS: false,
        extensions: [
          CharacterCount.configure({
            limit: 10000
          }),
          TextStyle,
          ImageResize,
          History,
          CassieKit.configure({
            textAlign: { types: ["heading", "paragraph"] },
            mention: {
              clickSuggestion: BuildRender(menulist) //编辑器右键菜单
            },
            highlight: {
              multicolor: true
            },
            table: {
              HTMLAttributes: {
                class: "border-collapse border border-slate-400"
              }
            },
            tableCell: {
              HTMLAttributes: {
                class: "border border-slate-300"
              }
            },
            tableHeader: {
              HTMLAttributes: {
                class: "border border-slate-300"
              }
            },
            page: {
              bodyPadding: 10,
              bodyWidth: bodyWidth,
              headerHeight: 100,
              footerHeight: 60,
              bodyHeight: h - 100,
              headerData: headerlist,
              footerData: footerlist,
              isPaging: true
            },
            focus: false, //选中样式
            history: false //历史记录回退 协作模式禁止开启
          })
        ]
      });
      setTimeout(() => {
        editor.value?.view.dispatch(editor.value?.state.tr.setMeta("splitPage", true));
      }, 1000);

      const editorStore = useEditorStore();
      const loadHeadings = () => {
        const headings = [] as any[];
        if (!editor.value) return;
        const transaction = editor.value.state.tr;
        if (!transaction) return;

        editor.value?.state.doc.descendants((node, pos) => {
          if (node.type.name === "heading") {
            console.log(pos, node);
            const start = pos;
            const end = pos + node.content.size;
            // const end = pos + node
            const id = `heading-${headings.length + 1}`;
            if (node.attrs.id !== id) {
              transaction?.setNodeMarkup(pos, undefined, {
                ...node.attrs,
                id
              });
            }

            headings.push({
              level: node.attrs.level,
              text: node.textContent,
              start,
              end,
              id
            });
          }
        });

        transaction?.setMeta("addToHistory", false);
        transaction?.setMeta("preventUpdate", true);

        editor.value?.view.dispatch(transaction);
        editorStore.setHeadings(headings);
      };
    });

    onBeforeUnmount(() => {
      editor.value?.destroy();
    });
    return { pageContent, menulist, headerlist, footerlist, onUpdate, onCreate, editor, bodyWidth, getSelectedText, extend };
  }
};
</script>
<style scoped>
.bottomcount {
  border-top: 1px dashed #9ca19f65;
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 100%;
  justify-items: center;
  align-items: center;
}

/* Bubble menu */
.bubble-menu {
  background-color: var(--white);
  border: 1px solid var(--gray-1);
  border-radius: 0.7rem;
  box-shadow: var(--shadow);
  display: flex;
  padding: 0.2rem;

  button {
    background-color: unset;

    &:hover {
      background-color: var(--gray-3);
    }

    &.is-active {
      background-color: var(--purple);

      &:hover {
        background-color: var(--purple-contrast);
      }
    }
  }
}

.lefttools {
  background-color: rgb(183, 194, 155);
  height: 100%;
  width: 78%;
  align-self: start;
  justify-self: start;
  column-span: 1;
}
.righttools {
  background-color: rgb(183, 194, 155);
  height: 100%;
  width: 100%;
}
.dropdownmenu li {
  background: #000;
}
.dropdownmenu li :hover {
  background: #de0000;
}
</style>
