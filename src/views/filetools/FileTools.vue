<template>
  <div class="main">
    <v-style>
      body { box-shadow: none; }
      ::selection { background-color: rgb(186, 212, 253); }
      :root {
        --demo-font-color: #222;
        --demo-bars-bkg: rgb(255, 255, 255);
        --demo-bars-shadow: 0 1px 3px 1px rgba(60, 64, 67, 0.15);
        --demo-bars-padding: 5px;
        --demo-bars-border-radius: 1px;
        --demo-text-bkg-color: white;
        --demo-text-box-shadow: 0 1px 3px 1px rgba(60, 64, 67, 0.15);
        --bar-font-color: rgb(32, 33, 36);
        --bar-font-family: Roboto, RobotoDraft, Helvetica, Arial, sans-serif;
        --bar-font-size: 15px;
        --bar-font-weight: 500;
        --bar-letter-spacing: 0.2px;
        --bar-padding: 3px;
        --bar-button-icon-size: 20px;
        --bar-button-padding: 4px 6px;
        --bar-button-radius: 4px;
        --bar-button-hover-bkg: rgb(241, 243, 244);
        --bar-button-active-color: rgb(26, 115, 232);
        --bar-button-active-bkg: rgb(232, 240, 254);
        --bar-button-open-color: rgb(32, 33, 36);
        --bar-button-open-bkg: rgb(232, 240, 254);
        --bar-menu-bkg: white;
        --bar-menu-border-radius: 0 0 3px 3px;
        --bar-menu-item-chevron-margin: 0;
        --bar-menu-item-hover-bkg: rgb(241, 243, 244);
        --bar-menu-item-padding: 5px 8px 5px 35px;
        --bar-menu-item-icon-size: 15px;
        --bar-menu-item-icon-margin: 0 9px 0 -25px;
        --bar-menu-padding: 6px 1px;
        --bar-menu-shadow: 0 2px 6px 2px rgba(60, 64, 67, 0.15);
        --bar-menu-separator-height: 1px;
        --bar-menu-separator-margin: 5px 0 5px 34px;
        --bar-menu-separator-color: rgb(227, 229, 233);
        --bar-separator-color: rgb(218, 220, 224);
        --bar-separator-width: 1px;
        --bar-sub-menu-border-radius: 3px;
      }
      .bars > .bar:first-child {
        border-bottom: 1px solid rgb(218, 220, 224);
        margin-bottom: 3px;
      }
      .bars {
        display: flex;
        justify-content: center;
        align-items: center;
      }
    </v-style>
    <div class="bars">
      <vue-file-toolbar-menu
        v-for="(content, index) in bars_content"
        :key="'bar-' + index"
        :content="content"
        :editor="editor"
      />
      <LinkButton
      :editor="editor"
      :ifNoMindMap="ifNoMindMap"
      :document="document"
      @update-data="handleUpdateData"
      @record-button-clicked="showRecord"
      @create-mindmap="loadingMindMap"
      @open-chartsdialog="openChartsDialog"
      @open-success="openSuccess"
      ></LinkButton>

      <Menu as="div" class="ml-3 relative inline-block text-left absolute -right-">
        <div>
          <MenuButton class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
            Options
            <ChevronDownIcon class="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
          </MenuButton>
        </div>

        <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
          <MenuItems class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div class="py-1">
              <MenuItem v-slot="{ active }" @click="this.$emit('set-mode', 1)">


                  <div :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'px-4 py-2 text-sm items-center flex']">
                    <svg-icon name="编辑 (1)" class="mr-2"></svg-icon>
                    编辑模式
                  </div>
              </MenuItem>
              <!-- <MenuItem v-slot="{ active }" @click="this.$emit('set-editing', 2)">
                <div :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']">批注模式</div>
              </MenuItem> -->
              <MenuItem v-slot="{ active }" @click="this.$emit('set-mode', 3)">
                <div :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', ' px-4 py-2 text-sm items-center flex']">
                  <svg-icon name="问答" class="mr-2"></svg-icon>
                  知识库问答模式
                </div>
              </MenuItem>
            </div>
          </MenuItems>
        </transition>
      </Menu>
      <div class="absolute right-9" >
        <el-switch
        v-model="isVideoMode"
        active-color="#6A64F1"
        inactive-color="#ff4949"
        @change="handleSwitchChange(isVideoMode)"
        inline-prompt
        :active-icon="Check"
        :inactive-icon="Close"
      ></el-switch>
      </div>
    </div>
    <!-- 新建文档对话框 -->
    <el-dialog title="新建文档" v-model="dialogVisible" width="30%">
      <el-input v-model="newDocumentName" placeholder="请输入文档名称"></el-input>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createNewDocument">创建</el-button>
      </template>
    </el-dialog>
    <el-dialog title="上传模版" v-model="dialogVisible1" width="30%" >
      <el-input v-model="newStenciltName" placeholder="请输入模版名称"></el-input>
      <el-input v-model="newStencilLabel" placeholder="请输入模版标签"></el-input>
      <el-input v-model="newStencilDescription" placeholder="请输入模版简介"></el-input>
      <template #footer>
        <el-button @click="dialogVisible1 = false">取消</el-button>
        <el-button type="primary" @click="upload_stencil">上传</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import VueFileToolbarMenu from "vue-file-toolbar-menu";
import DemoCustomButton from "./DemoCustomButton.vue";
import DemoCustomMenuItem from "./DemoCustomMenuItem.vue";
import { Editor } from "@tiptap/vue-3";
import { undo } from "y-prosemirror";
import { useRouter } from "vue-router";
import axios from "axios";
import LinkButton from "./LinkButton.vue";
import { Check, Close } from '@element-plus/icons-vue'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'
export default {
  name:"FileTools",
  components: { VueFileToolbarMenu, LinkButton, Check, Close, Menu, MenuButton, MenuItem, MenuItems, ChevronDownIcon},
  props: {
    document: {
      type: Object,
      required: true
    },
    editor: {
      type: Editor,
      required: true
    },
    ifNoMindMap: Boolean,
  },
  setup() {
    const router = useRouter();
    return {
      router
    };
  },
  data() {
    return {
      color: "rgb(74, 238, 164)",
      font: "Avenir",
      theme: "default",
      edit_mode: true,
      check1: false,
      check2: false,
      check3: true,
      dialogVisible: false,
      dialogVisible1: false,
      newDocumentName: "",
      newStenciltName:"",
      newStencilLabel:"",
      newStencilDescription:"",
      context: "",
      docName: "",
      isVideoMode: false, // 新增的数据属性，用于控制是否显示视频播放器
    };
  },
  methods: {
    openSuccess() {
      this.$emit('open-success');
    },
    changeLineSpacing() {
      const selectElement = document.getElementById('lineSpacingSelect');
      const lineSpacingValue = selectElement.value;
      this.editor.chain().focus().setLineHeight(lineSpacingValue).run();
    },
    handleSwitchChange(value) {
      console.log("切换");
      this.$emit('video-mode-change', value);
    },
    showRecord() {
      console.log("接收录音事件");
      this.$emit('record-button-clicked');
    },
    // 发送数据
    handleUpdateData(data) {
      this.$emit('update-data', data);
    },
    // 加载思维导图
    loadingMindMap(isLoading, mindmap) {
      this.$emit('create-mindmap', isLoading, mindmap);
    },
    openChartsDialog() {
      this.$emit('open-chartsdialog');
    },
    // 新建
    async createNewDocument() {
      if (this.newDocumentName.trim() === "") {
        this.$message.error("文档名称不能为空！");
        return;
      }
      const username = localStorage.getItem("userName") || "unknown_user";
      // 获取所有文档名称进行比较
      try {
        const existingDocumentsResponse = await axios.get("http://127.0.0.1:5000/api/check_documents", {
          params: {
            username: username,
            file_name: this.newDocumentName
          },
          headers: {
            "Content-Type": "application/json"
          }
        });

        console.log(existingDocumentsResponse);
        // 检查文档名称是否重复
        if (existingDocumentsResponse === "true") {
          this.$message.error("文档名称已存在，请选择其他名称！");
          return;
        }
      } catch (error) {
        console.error("Error fetching existing documents:", error);
        this.$message.error("无法获取现有文档信息，请稍后重试！");
        return;
      }
      const newDocument = {
        id: Date.now().toString(),
        title: this.newDocumentName,
        path: `/documents/${Date.now()}`,
        isOpen: true,
        username: username
      };
      this.dialogVisible = false;
      this.newDocumentName = "";
      this.$emit("add-document", newDocument);
      this.$router.push({
        path: newDocument.path,
        query: {
          document: JSON.stringify(newDocument)
        }
      });
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/upload",
          {
            username: username,
            file_name: newDocument.title,
            file_type: "doc"
          },
          {
            headers: {
              "Content-Type": "application/json"
            }
          }
        );
        console.log(response);
      } catch (error) {
        console.error("Error saving document:", error);
      }
    },
    // 保存
    async saveDocument() {
      const username = localStorage.getItem("userName") || "unknown_user";
      if (!this.document || !this.document.title) {
        this.$message.error("无法获取文档名称！");
        return;
      }
      const fileName = this.document.title; // 从 props 获取当前文档名称
      console.log(fileName);
      console.log("保存");
      const html = this.editor.getHTML();
      console.log(html);
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/save",
          {
            username,
            file_name: fileName,
            text: html
          },
          {
            headers: {
              "Content-Type": "application/json"
            }
          }
        );
        console.log(response);
      } catch (error) {
        console.error("Error saving document:", error);
      }
    },
    async upload_stencil() {
      const username = localStorage.getItem("userName") || "unknown_user";
      if (!this.document || !this.document.title) {
        this.$message.error("无法获取文档名称！");
        return;
      }
      const fileName = this.document.title; // 从 props 获取当前文档名称
      // console.log(fileName);
      console.log("模版");
      const html = this.editor.getHTML();
      console.log(html);
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/upload_stencil",
          {
            username,
            file_name: fileName,
            name: this.newStenciltName,
            label: this.newStencilLabel,
            description: this.newStencilDescription
          },
          {
            headers: {
              "Content-Type": "application/json"
            }
          }
        );
        this.dialogVisible1 = false;
        console.log(response);
      } catch (error) {
        console.error("Error upload stencil:", error);
      }
    }
  },
  computed: {
    // Read the API documentation about the available menu content options
    bars_content() {
      return [
        [
          {
            text: "文件",
            menu: [
              {
                text: "新建",
                click: () => {
                  this.dialogVisible = true; // 打开新建文档对话框
                }
              },
              { is: "separator" },
              {
                text: "保存",
                click: () => {
                  console.log(this.editor.getHTML());
                  this.context = this.editor.getHTML();
                  this.saveDocument(); // 调用保存文档的功能
                }
              },
              { is: "separator" },
              {
                text: "上传为模版",
                click: () => {
                  console.log(this.editor.getHTML());
                  this.context = this.editor.getHTML();
                  this.dialogVisible1 = true;
                  // this.upload_stencil(); // 调用上传文档功能
                }
              },
              { is: "separator" },
              {
                text: "打印",
                click: () => {
                  console.log("New Print!");
                }
              },
              { is: "separator" },
              {
                text: "关闭",
                click: () => {
                  this.router.push("/"); // 跳转到主页面
                  console.log("Close and navigate to home page");
                }
              }
            ]
          },
          {
            icon: "undo",
            click: () => {
              // 执行撤回操作
              if (this.editor.can().undo()) {
                this.editor.commands.undo();
                console.log("Undo last action!");
              }
            }
          },
          {
            icon: "redo",
            click: () => {
              // 执行重做操作
              if (this.editor.can().redo()) {
                this.editor.commands.redo();
                console.log("Redo last action!");
              }
            },
          },
        {
          text: "-",
          click: () => {
            const textStyle = this.editor.getAttributes('textStyle');
            if (textStyle && textStyle.fontSize) {
              const currentSize = parseInt(textStyle.fontSize.replace('px', ''));
              const newSize = currentSize - 2;
              if (newSize > 0) { // 防止字体大小变成负数
                this.editor.chain().focus().setFontSize(`${newSize}pt`).run();
              }
            }
          }
        },
        {
          html: "<div>字体大小</div>",
          title: "字体大小",
          chevron: true,
          menu: [
            {
              html: "<b>12px</b>",
              title: "12px",
              click: () => {
                this.editor.chain().focus().setFontSize('12px').run();
              }
            },
            {
              html: "<b>14px</b>",
              title: "14px",
              click: () => {
                this.editor.chain().focus().setFontSize('14px').run();
              }
            },
            {
              html: "<b>16px</b>",
              title: "16px",
              click: () => {
                this.editor.chain().focus().setFontSize('16px').run();
              }
            },
            {
              html: "<b>18px</b>",
              title: "18px",
              click: () => {
                this.editor.chain().focus().setFontSize('18px').run();
              }
            },
            {
              html: "<b>20px</b>",
              title: "20px",
              click: () => {
                this.editor.chain().focus().setFontSize('20px').run();
              }
            }
          ]
        },
        {
          text: "+",
          click: () => {
            const textStyle = this.editor.getAttributes('textStyle');
            if (textStyle && textStyle.fontSize) {
              const currentSize = parseInt(textStyle.fontSize.replace('px', ''));
              const newSize = currentSize + 2;
              this.editor.chain().focus().setFontSize(`${newSize}pt`).run();
            }
          }
        },
        {
          html: "<span>字体</span>",
          title: "字体",
          chevron: true,
          menu: [
            {
              html: "<b>Inter</b>",
              title: "Inter",
              click: () => {
                this.editor.chain().focus().setFontFamily('Inter').run();
              }
            },
            {
              html: "<b>Comic Sans</b>",
              title: "Comic Sans",
              click: () => {
                this.editor.chain().focus().setFontFamily('Comic Sans MS, Comic Sans').run();
              }
            },
            {
              html: "<b>Serif</b>",
              title: "Serif",
              click: () => {
                this.editor.chain().focus().setFontFamily('serif').run();
              }
            },
            {
              html: "<b>Monospace</b>",
              title: "Monospace",
              click: () => {
                this.editor.chain().focus().setFontFamily('monospace').run();
              }
            },
            {
              html: "<b>Cursive</b>",
              title: "Cursive",
              click: () => {
                this.editor.chain().focus().setFontFamily('cursive').run();
              }
            },
            {
              html: "<b>Unset font family</b>",
              title: "Unset font family",
              click: () => {
                this.editor.chain().focus().unsetFontFamily().run();
              }
            }
          ]
        },
        {
            html: "<span>行间距</span>",
            title: "行间距",
            chevron: true,
            menu: [
              {
                html: "<b>行间距 1</b>",
                title: "行间距 1",
                click: () => {
                  this.editor.chain().focus().setLineHeight("1").run();
                }
              },
              {
                html: "<b>行间距 1.5</b>",
                title: "行间距 1.5",
                click: () => {
                  this.editor.chain().focus().setLineHeight("1.5").run();
                }
              },
              {
                html: "<b>行间距 2</b>",
                title: "行间距 2",
                click: () => {
                  this.editor.chain().focus().setLineHeight("2").run();
                }
              }
              // 添加更多样式...
            ]
          },
          { is: "separator" },

          {
            icon: "format_align_left",
            title: "左对齐",
            click: () => {
              this.editor.chain().focus().setTextAlign("left").run();
            }
          },
          {
            icon: "format_align_center",
            title: "居中",
            click: () => {
              this.editor.chain().focus().setTextAlign("center").run();
            }
          },
          {
            icon: "format_align_right",
            title: "右对齐",
            click: () => {
              this.editor.chain().focus().setTextAlign("right").run();
            }
          },
          {
            icon: "format_align_justify",
            title: "两端对齐",
            click: () => {
              this.editor.chain().focus().setTextAlign("justify").run();
            }
          },
          { is: "separator" },
          {
            icon: "table_view",
            title: "表格",
            menu: [
              {
                text: "表格",
                menu: [
                  {
                    text: "固定表格",
                    click: () => {
                      this.editor.chain().focus().fixTables().run();
                    }
                  },
                  {
                    text: "插入表格",
                    click: () => {
                      this.editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: false }).run();
                    }
                  },
                  {
                    text: "删除表",
                    click: () => {
                      this.editor.chain().focus().deleteTable().run();
                    }
                  }
                ]
              },
              {
                text: "表头",
                menu: [
                  {
                    text: "自适应表头",
                    click: () => {
                      this.editor.chain().focus().toggleHeaderRow().run();
                    }
                  },
                  {
                    text: "设置成表头样式",
                    click: () => {
                      this.editor.chain().focus().toggleHeaderCell().run();
                    }
                  }
                ]
              },
              {
                text: "列操作",
                menu: [
                  {
                    text: "添加列(之前)",
                    click: () => {
                      this.editor.chain().focus().addColumnBefore().run();
                    }
                  },
                  {
                    text: "添加列(之后)",
                    click: () => {
                      this.editor.chain().focus().addColumnAfter().run();
                    }
                  },
                  {
                    text: "删除列",
                    click: () => {
                      this.editor.chain().focus().deleteColumn().run();
                    }
                  },
                  {
                    text: "设置第一列",
                    click: () => {
                      this.editor.chain().focus().toggleHeaderColumn().run();
                    }
                  }
                ]
              },
              {
                text: "行操作",
                menu: [
                  {
                    text: "添加行(之前)",
                    click: () => {
                      this.editor.chain().focus().addRowBefore().run();
                    }
                  },
                  {
                    text: " 添加行(之后)",
                    click: () => {
                      this.editor.chain().focus().addRowAfter().run();
                    }
                  },
                  {
                    text: "删除行",
                    click: () => {
                      this.editor.chain().focus().deleteRow.run();
                    }
                  }
                ]
              },
              {
                text: "单元格操作",
                menu: [
                  {
                    text: "合并单元格",
                    click: () => {
                      this.editor.chain().focus().mergeCells().run();
                    }
                  },
                  {
                    text: " 分割单元格",
                    click: () => {
                      this.editor.chain().focus().splitCell().run();
                    }
                  },
                  {
                    text: "合并或分割",
                    click: () => {
                      this.editor.chain().focus().mergeOrSplit().run();
                    }
                  },
                  {
                    text: "下一个单元格",
                    click: () => {
                      this.editor.chain().focus().goToNextCell().run();
                    }
                  },
                  {
                    text: "上一个单元格",
                    click: () => {
                      this.editor.chain().focus().goToPreviousCell().run();
                    }
                  }
                ]
              }
            ]
          },
          {
            icon: "format_list_numbered",
            title: "编号列表",
            click: () => {
              this.editor.chain().focus().toggleOrderedList().run();
            }
          },
          {
            icon: "format_list_bulleted",
            title: "符号列表",
            click: () => {
              this.editor.chain().focus().toggleBulletList().run();
            }
          },
          { is: "separator" },
          {
            icon: "format_bold",
            title: "加粗",
            click: () => {
              this.editor.chain().focus().toggleBold().run();
            }
          },
          {
            icon: "format_italic",
            title: "斜体",
            click: () => {
              this.editor.chain().focus().toggleItalic().run();
            }
          },
          {
            icon: "format_underline",
            title: "下划线",
            click: () => {
              this.editor.chain().focus().toggleUnderline().run();
            }
          },
          {
            icon: "format_strikethrough",
            title: "中划线",
            click: () => {
              this.editor.chain().focus().toggleStrike().run();
            }
          },
          {
            is: "button-color",
            type: "compact",
            menu_class: "align-center",
            stay_open: false,
            color: this.color,
            update_color: (new_color) => {
              this.editor.chain().focus().setColor(new_color.hex).run();
            }
          },
          {
            is: "button-color",
            type: "compact",
            menu_class: "align-center",
            stay_open: false,
            color: this.color,
            update_color: (new_color) => {
              this.editor.chain().focus().toggleHighlight({ color: new_color.hex }).run();
            }
          },
          { is: "separator" },
          { is: DemoCustomButton, text: "自定义按钮", click: () => alert("Your custom action!") },
          { is: "separator" },
          {
            html: "<b>标题</b>",
            title: "标题",
            chevron: true,
            menu: [
              {
                html: "<b>标题 H1</b>",
                title: "标题 1",
                click: () => {
                  this.editor.chain().focus().toggleHeading({ level: 1 }).run();
                }
              },
              {
                html: "<b>标题 H2</b>",
                title: "标题 2",
                click: () => {
                  this.editor.chain().focus().toggleHeading({ level: 2 }).run();
                }
              },
              {
                html: "<b>标题 H3</b>",
                title: "标题 H3",
                click: () => {
                  this.editor.chain().focus().toggleHeading({ level: 3 }).run();
                }
              },
              {
                html: "<b>标题 H4</b>",
                title: "标题 H4",
                click: () => {
                  this.editor.chain().focus().toggleHeading({ level: 4 }).run();
                }
              },
              {
                html: "<b>标题 H5</b>",
                title: "标题 H5",
                click: () => {
                  this.editor.chain().focus().toggleHeading({ level: 5 }).run();
                }
              },
              {
                html: "<b>标题 H6</b>",
                title: "标题 H6",
                click: () => {
                  this.editor.chain().focus().toggleHeading({ level: 6 }).run();
                }
              }
            ]
          },
          // {is: LinkButton},
          {
            icon: this.edit_mode ? "lock_open" : "lock",
            title: "切换模式",
            active: !this.edit_mode,
            click: () => {
              this.edit_mode = !this.edit_mode;
              this.editor.setEditable(this.edit_mode);
            }
          }
        ]
      ];
    }
  }
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,700;1,400;1,500;1,700&display=swap");
:root {
  --demo-font-color: rgb(74, 238, 164);
}
::selection {
  background-color: rgba(74, 238, 164, 0.2);
}
</style>

<style scoped>
a {
  color: inherit;
}
svg.github {
  fill: var(--demo-font-color);
  margin-right: 5px;
}

.main {
  width: 100%;
  height: 100%;
}
.bars {
  background-color: var(--demo-bars-bkg, white);
  border-radius: var(--demo-bars-border-radius, 5px);
  box-shadow: var(--demo-bars-shadow, 0 0 20px black);
  padding: var(--demo-bars-padding, 8px);
  transition: 0.5s;
}
::v-deep(.bars) * {
  transition: font-size 0.1s linear, padding 0.1s linear, margin 0.1s linear;
}
.line-height-1 {
  line-height: 1;
}
.line-height-1-5 {
  line-height: 1.5;
}
.line-height-2 {
  line-height: 2;
}
</style>
