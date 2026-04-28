<template>
  <div class="file-tools-shell">
    <v-style>
      body { box-shadow: none; }
      ::selection { background-color: rgba(var(--wx-brand-indigo), 0.2); color: rgb(var(--wx-ink)); }
      :root {
        --demo-font-color: rgb(var(--wx-ink));
        --demo-bars-bkg: rgba(255, 255, 255, 0.62);
        --demo-bars-shadow: none;
        --demo-bars-padding: 3px;
        --demo-bars-border-radius: 10px;
        --demo-text-bkg-color: white;
        --demo-text-box-shadow: none;
        --bar-font-color: rgb(var(--wx-ink-muted));
        --bar-font-family: Geist, "HarmonyOS Sans SC", "Microsoft YaHei", sans-serif;
        --bar-font-size: 13px;
        --bar-font-weight: 650;
        --bar-letter-spacing: 0px;
        --bar-padding: 2px;
        --bar-button-icon-size: 18px;
        --bar-button-padding: 6px 8px;
        --bar-button-radius: 8px;
        --bar-button-hover-bkg: rgba(var(--wx-workspace-surface), 0.96);
        --bar-button-active-color: rgb(var(--wx-brand-indigo));
        --bar-button-active-bkg: rgba(var(--wx-brand-indigo-soft), 0.82);
        --bar-button-open-color: rgb(var(--wx-ink));
        --bar-button-open-bkg: rgba(var(--wx-workspace-surface), 0.96);
        --bar-menu-bkg: rgba(255, 255, 255, 0.88);
        --bar-menu-border-radius: 10px;
        --bar-menu-item-hover-bkg: rgba(var(--wx-brand-indigo-soft), 0.68);
        --bar-menu-item-padding: 7px 12px 7px 32px;
        --bar-menu-item-icon-size: 16px;
        --bar-menu-item-icon-margin: 0 12px 0 -24px;
        --bar-menu-padding: 8px 0;
        --bar-menu-shadow: 0 18px 42px -30px rgba(15, 23, 42, 0.48), 0 0 0 1px rgba(15, 23, 42, 0.08);
        --bar-menu-separator-height: 1px;
        --bar-menu-separator-margin: 4px 0 4px 32px;
        --bar-menu-separator-color: rgba(var(--wx-workspace-border), 0.74);
        --bar-separator-color: rgba(var(--wx-workspace-border), 0.88);
        --bar-separator-width: 1px;
        --bar-sub-menu-border-radius: 10px;
      }
      .bars > .bar {
        border-bottom: none !important;
        margin-bottom: 0;
        border-radius: 10px;
        background: transparent;
      }
      .bars {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        gap: 6px;
      }
    </v-style>
    <div class="toolbar-layout">
      <div class="contextual-toolbar bars" aria-label="编辑工具栏">
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
      </div>

      <div class="mode-console" aria-label="工作模式">
        <div class="mode-segment">
          <button type="button" :class="{ active: activeMode === 1 }" @click="setMode(1)">
            <svg-icon name="编辑 (1)"></svg-icon>
            <span>编辑</span>
          </button>
          <button type="button" :class="{ active: activeMode === 3 }" @click="setMode(3)">
            <svg-icon name="问答"></svg-icon>
            <span>问答</span>
          </button>
        </div>
        <button type="button" class="video-toggle" :class="{ active: isVideoMode }" @click="toggleVideoMode">
          <span class="video-dot"></span>
          <span>视频</span>
        </button>
      </div>
    </div>

    <!-- 新建文档对话框 -->
    <el-dialog title="新建文档" v-model="dialogVisible" width="420px">
      <el-input v-model="newDocumentName" placeholder="请输入文档名称"></el-input>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createNewDocument">创建</el-button>
      </template>
    </el-dialog>
    <el-dialog title="上传模版" v-model="dialogVisible1" width="420px" >
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
import { Editor } from "@tiptap/vue-3";
import { useRouter } from "vue-router";
import axios from "axios";
import LinkButton from "./LinkButton.vue";
export default {
  name:"FileTools",
  components: { VueFileToolbarMenu, LinkButton },
  props: {
    document: {
      type: Object,
      default: null
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
      color: "#2b3775",
      font: "Geist",
      theme: "default",
      edit_mode: true,
      activeMode: 1,
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
    setMode(mode) {
      this.activeMode = mode;
      this.$emit('set-mode', mode);
    },
    toggleVideoMode() {
      this.isVideoMode = !this.isVideoMode;
      this.handleSwitchChange(this.isVideoMode);
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
    bars_content() {
      const fileGroup = [
        {
          text: "文件",
          menu: [
            {
              text: "新建",
              click: () => {
                this.dialogVisible = true;
              }
            },
            { is: "separator" },
            {
              text: "保存",
              click: () => {
                this.context = this.editor.getHTML();
                this.saveDocument();
              }
            },
            {
              text: "上传为模版",
              click: () => {
                this.context = this.editor.getHTML();
                this.dialogVisible1 = true;
              }
            },
            { is: "separator" },
            {
              text: "打印",
              click: () => {
                window.print();
              }
            },
            {
              text: "关闭",
              click: () => {
                this.router.push("/");
              }
            }
          ]
        },
        {
          icon: "undo",
          title: "撤销",
          click: () => {
            if (this.editor.can().undo()) this.editor.commands.undo();
          }
        },
        {
          icon: "redo",
          title: "重做",
          click: () => {
            if (this.editor.can().redo()) this.editor.commands.redo();
          }
        }
      ];

      const typographyGroup = [
        {
          text: "-",
          title: "缩小字号",
          click: () => {
            const textStyle = this.editor.getAttributes("textStyle");
            const currentSize = parseInt((textStyle.fontSize || "14px").replace("px", ""), 10);
            const newSize = Math.max(currentSize - 2, 8);
            this.editor.chain().focus().setFontSize(`${newSize}px`).run();
          }
        },
        {
          html: "<span>字号</span>",
          title: "字体大小",
          chevron: true,
          menu: [12, 14, 16, 18, 20, 24].map((size) => ({
            html: `<b>${size}px</b>`,
            title: `${size}px`,
            click: () => {
              this.editor.chain().focus().setFontSize(`${size}px`).run();
            }
          }))
        },
        {
          text: "+",
          title: "放大字号",
          click: () => {
            const textStyle = this.editor.getAttributes("textStyle");
            const currentSize = parseInt((textStyle.fontSize || "14px").replace("px", ""), 10);
            const newSize = Math.min(currentSize + 2, 72);
            this.editor.chain().focus().setFontSize(`${newSize}px`).run();
          }
        },
        {
          html: "<span>字体</span>",
          title: "字体",
          chevron: true,
          menu: [
            {
              html: "<b>Geist</b>",
              title: "Geist",
              click: () => {
                this.editor.chain().focus().setFontFamily("Geist").run();
              }
            },
            {
              html: "<b>黑体</b>",
              title: "黑体",
              click: () => {
                this.editor.chain().focus().setFontFamily("SimHei, Microsoft YaHei").run();
              }
            },
            {
              html: "<b>宋体</b>",
              title: "宋体",
              click: () => {
                this.editor.chain().focus().setFontFamily("SimSun, Songti SC, serif").run();
              }
            },
            {
              html: "<b>Monospace</b>",
              title: "Monospace",
              click: () => {
                this.editor.chain().focus().setFontFamily("Geist Mono, monospace").run();
              }
            },
            {
              html: "<b>默认字体</b>",
              title: "默认字体",
              click: () => {
                this.editor.chain().focus().unsetFontFamily().run();
              }
            }
          ]
        },
        {
          html: "<b>标题</b>",
          title: "标题",
          chevron: true,
          menu: [1, 2, 3, 4, 5, 6].map((level) => ({
            html: `<b>标题 H${level}</b>`,
            title: `标题 ${level}`,
            click: () => {
              this.editor.chain().focus().toggleHeading({ level }).run();
            }
          }))
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
        }
      ];

      const paragraphGroup = [
        {
          html: "<span>行距</span>",
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
        }
      ];

      const insertGroup = [
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
                      this.editor.chain().focus().deleteRow().run();
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
        }
      ];

      const documentGroup = [
        {
          icon: this.edit_mode ? "lock_open" : "lock",
          title: "切换只读",
          active: !this.edit_mode,
          click: () => {
            this.edit_mode = !this.edit_mode;
            this.editor.setEditable(this.edit_mode);
          }
        }
      ];

      return [fileGroup, typographyGroup, paragraphGroup, insertGroup, documentGroup];
    }
  }
};
</script>

<style scoped>
a {
  color: inherit;
}

.file-tools-shell {
  width: 100%;
  color: rgb(var(--wx-ink));
  font-family: var(--font-geist, "Geist"), "HarmonyOS Sans SC", "Microsoft YaHei", sans-serif;
}

.toolbar-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 14px;
  width: 100%;
  min-height: 50px;
}

.contextual-toolbar {
  min-width: 0;
  overflow-x: auto;
  border: 1px solid rgba(var(--wx-workspace-border), 0.72);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 14px 36px -30px rgba(15, 23, 42, 0.58);
  padding: 5px;
  backdrop-filter: blur(18px);
}

.bars {
  background-color: var(--demo-bars-bkg, white);
  border-radius: var(--demo-bars-border-radius, 5px);
  box-shadow: var(--demo-bars-shadow, none);
  padding: var(--demo-bars-padding, 8px);
  transition: background 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
}

::v-deep(.bars) * {
  letter-spacing: 0;
  transition: background 140ms ease, color 140ms ease, box-shadow 140ms ease;
}

::v-deep(.bar) {
  border-right: 1px solid rgba(var(--wx-workspace-border), 0.72);
  padding-right: 6px;
}

::v-deep(.bar:last-child) {
  border-right: 0;
  padding-right: 0;
}

::v-deep(.bar-button),
::v-deep(.bar select) {
  min-height: 32px;
}

::v-deep(.bar-menu) {
  border: 1px solid rgba(var(--wx-workspace-border), 0.7);
  backdrop-filter: blur(16px);
}

.mode-console {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  flex: 0 0 auto;
}

.mode-segment {
  display: inline-flex;
  align-items: center;
  min-height: 40px;
  padding: 4px;
  border: 1px solid rgba(var(--wx-workspace-border), 0.76);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.74);
  box-shadow: 0 14px 36px -32px rgba(15, 23, 42, 0.62);
  backdrop-filter: blur(18px);
}

.mode-segment button,
.video-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  min-height: 32px;
  border-radius: 8px;
  color: rgb(var(--wx-ink-muted));
  cursor: pointer;
  font-size: 13px;
  font-weight: 700;
  transition: background 160ms ease, color 160ms ease, box-shadow 160ms ease;
}

.mode-segment button {
  padding: 0 10px;
}

.mode-segment svg {
  width: 16px;
  height: 16px;
}

.mode-segment button.active {
  background: rgb(var(--wx-brand-indigo));
  color: #ffffff;
  box-shadow: 0 12px 22px -18px rgba(43, 55, 117, 0.9);
}

.mode-segment button:not(.active):hover,
.video-toggle:hover {
  background: rgba(var(--wx-workspace-surface), 0.96);
  color: rgb(var(--wx-ink));
}

.video-toggle {
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid rgba(var(--wx-workspace-border), 0.76);
  background: rgba(255, 255, 255, 0.66);
  box-shadow: 0 14px 36px -32px rgba(15, 23, 42, 0.62);
  backdrop-filter: blur(18px);
}

.video-toggle.active {
  border-color: rgba(var(--wx-brand-emerald), 0.36);
  background: rgba(var(--wx-brand-emerald-soft), 0.86);
  color: rgb(var(--wx-brand-emerald));
}

.video-dot {
  width: 7px;
  height: 7px;
  border-radius: 999px;
  background: rgb(var(--wx-ink-faint));
}

.video-toggle.active .video-dot {
  background: rgb(var(--wx-brand-emerald));
  box-shadow: 0 0 0 4px rgba(var(--wx-brand-emerald), 0.12);
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

@media (max-width: 980px) {
  .toolbar-layout {
    grid-template-columns: 1fr;
  }

  .mode-console {
    justify-content: space-between;
    width: 100%;
  }
}
</style>
