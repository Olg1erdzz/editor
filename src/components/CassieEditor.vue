<template>
  <div class="editor-workspace">
    <div
      v-if="editor"
      class="toolbar-dock"
      v-motion
      :initial="{ opacity: 0, y: -8 }"
      :enter="{ opacity: 1, y: 0 }"
    >
      <FileTools :editor="editor" :document="document"></FileTools>
    </div>

    <section class="editor-stage" aria-label="文档编辑区">
      <aside class="workspace-rail" aria-label="编辑状态">
        <div class="rail-block">
          <span class="rail-label">Mode</span>
          <strong>{{ editable ? "Edit" : "Read" }}</strong>
        </div>
        <div class="rail-block">
          <span class="rail-label">Sync</span>
          <strong>{{ providerStatusLabel }}</strong>
        </div>
        <div v-if="collaborationUsers.length" class="presence-cluster" aria-label="在线协作者">
          <span
            v-for="(collaborator, index) in collaborationUsers.slice(0, 4)"
            :key="`${collaborator.name || 'user'}-${index}`"
            class="presence-avatar"
            :title="collaborator.name"
            :style="{ '--presence-color': collaborator.color || '#2b3775' }"
          >
            {{ getUserInitial(collaborator) }}
          </span>
          <span v-if="collaborationUsers.length > 4" class="presence-more">+{{ collaborationUsers.length - 4 }}</span>
        </div>
      </aside>

      <div class="paper-stack">
        <editor-content :editor="editor" class="editor-surface" />
      </div>
    </section>

    <div class="floating-count">
      <span>字数</span>
      <strong>{{ editor?.storage.characterCount.characters() || 0 }}</strong>
    </div>
  </div>
</template>

<script lang="ts">
//import applyDevTools from "prosemirror-dev-tools";
import { EditorContent, Editor } from "@tiptap/vue-3";
import { computed, defineComponent, onBeforeUnmount, onMounted, PropType, ref, shallowRef, unref, watchEffect } from "vue";
import { BuildRender, ContextMenuOptions } from "@/default";
import { CassieKit } from "@/extension";
import * as Y from "yjs";
import Collaboration from "@tiptap/extension-collaboration";
import CollaborationCursor from "@tiptap/extension-collaboration-cursor";
import { HocuspocusProvider } from "@hocuspocus/provider";
import { Extensions } from "@tiptap/core";
import FileTools from "@/views/filetools/FileTools.vue";
import ImageResize from "tiptap-extension-resize-image";
import History from "@tiptap/extension-history";
import CharacterCount from '@tiptap/extension-character-count';
export default defineComponent({
  name: "cassie-editor",
  components: {
    FileTools,
    EditorContent
  },
  props: {
    content: {
      type: [Object, String]
    },
    menuList: {
      type: Array as PropType<ContextMenuOptions[]>
    },
    footerHeight: {
      type: Number,
      default: 100
    },
    headerHeight: {
      type: Number,
      default: 100
    },
    bodyHeight: {
      type: Number,
      default: 400
    },
    bodyWidth: {
      type: Number,
      default: 1200
    },
    bodyPadding: {
      type: Number,
      default: 10
    },
    isPaging: {
      type: Boolean,
      default: true
    },
    headerData: {
      type: Array,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: []
    },
    footerData: {
      type: Array,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: []
    },
    output: {
      type: String,
      default: "html"
    },
    class: {
      type: String,
      default: ""
    },
    spellcheck: {
      type: Boolean,
      default: false
    },
    editable: {
      type: Boolean,
      default: true
    },
    document: {
      type: Object,
      default: null
    },
    collaborationUrl: {
      type: String,
      default: undefined
    },
    user: {
      type: Object,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: { name: "John Doe", color: "#ffcc00" }
    }
  },
  setup(props, { emit }) {
    const ydoc = new Y.Doc();
    const editor = shallowRef<Editor>();
    const provider = shallowRef<HocuspocusProvider>();
    const collaborationUsers = ref<any[]>([]);
    const providerStatus = ref("local");
    const syncCollaborationUsers = () => {
      collaborationUsers.value = editor.value?.storage.collaborationCursor?.users || [];
    };
    const providerStatusLabel = computed(() => {
      if (!props.collaborationUrl) return "Local";
      if (providerStatus.value === "connected") return "Online";
      if (providerStatus.value === "connecting") return "Syncing";
      return "Offline";
    });
    const getUserInitial = (user: any) => {
      const name = user?.name || "U";
      return name.slice(0, 1).toUpperCase();
    };
    onMounted(() => {
      //协作编辑 ws url
      let extensions: Extensions = [
        CassieKit.configure({
          textAlign: { types: ["heading", "paragraph"] },
          mention: {
            clickSuggestion: BuildRender(props.menuList) //编辑器右键菜单
          },
          page: { ...props },
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
          focus: false, //选中样式
          history: false //历史记录回退 协作模式禁止开启
        }),
        ImageResize,
        History,
        CharacterCount.configure({
            limit: 10000
        }),
      ];
      if (props.collaborationUrl) {
        provider.value = new HocuspocusProvider({
          url: props.collaborationUrl,
          name: "1", //TODO 这里需要修改 这里是文档唯一id 用于区分不同的文档
          document: ydoc,
          onStatus: (data) => {
            providerStatus.value = data.status;
            emit("onStatus", data, editor.value);
          },
          onConnect: () => {},
          onClose: (data) => {
            console.log(data);
          },
          onAwarenessChange: (data) => {
            //协作用户状态的变化
            syncCollaborationUsers();
            emit("onAwarenessChange", data);
          },
          onSynced: (data) => {
            syncCollaborationUsers();
            //TODO 如果当前协作文档 只有一个人 证明是第一个打开文档的 需要添加文档
            //TODO  这里的实现是错误的 应该在服务端实现打开文档的时候就添加文档 为了演示暂时这样处理减少网络请求
            if (editor.value && editor.value.storage.collaborationCursor.users.length == 1) {
              if (props.content) {
                editor.value.commands.setContent(props.content);
              }
            }
          }
        });
        extensions.push(
          Collaboration.configure({
            document: ydoc
          })
        );
        extensions.push(
          CollaborationCursor.configure({
            provider: provider.value,
            //这里应该使用当前你的登录用户
            user: props.user
          })
        );
      }
      //如果是协作模式 设置 content需要滞后 否则会重复添加
      editor.value = new Editor({
        editable: props.editable,
        content: props.collaborationUrl ? null : props.content,
        onCreate: (options) => {
          emit("onCreate", options);
        },
        onTransaction: (options) => {
          emit("onTransaction", options);
        },
        onFocus: (options) => {
          emit("onFocus", options);
        },
        onBlur: (options) => {
          emit("onBlur", options);
        },
        onDestroy: (options) => {
          emit("onDestroy", options);
        },
        onUpdate({ editor }) {
          let output;
          if (props.output === "html") {
            output = editor.getHTML();
          } else {
            output = editor.getJSON();
          }
          emit("update:content", output);
          emit("onUpdate", output, editor);
        },
        onSelectionUpdate({ editor }) {
          emit("onSelectionUpdate", editor);
        },
        editorProps: {
          attributes: {
            class: props.class
          }
        },
        injectCSS: false,
        extensions
      });
      setTimeout(() => {
        editor.value?.view.dispatch(editor.value?.state.tr.setMeta("splitPage", true));
        syncCollaborationUsers();
      }, 1000);
      //TODO 开发模式打开 applyDevTools(editor.value.view);
    });

    onBeforeUnmount(() => {
      editor.value?.destroy();
      provider.value?.destroy();
    });

    watchEffect(() => {
      unref(editor)?.setOptions({
        editorProps: {
          attributes: {
            spellcheck: String(props.spellcheck)
          }
        }
      });
    });
    return { collaborationUsers, editor, getUserInitial, providerStatusLabel };
  }
});
</script>
<style scoped>
.editor-workspace {
  position: relative;
  display: flex;
  flex: 1 1 auto;
  flex-direction: column;
  align-items: center;
  width: 100%;
  min-height: calc(100vh - 4rem);
  padding: 18px 28px 72px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.22), rgba(255, 255, 255, 0)),
    rgb(var(--wx-workspace-bg));
  color: rgb(var(--wx-ink));
  font-family: var(--font-geist, "Geist"), "HarmonyOS Sans SC", "Microsoft YaHei", sans-serif;
}

.toolbar-dock {
  position: sticky;
  top: 4.7rem;
  z-index: 45;
  width: min(1280px, 100%);
  margin: 0 auto 22px;
}

.editor-stage {
  display: grid;
  grid-template-columns: 92px minmax(0, 1fr);
  width: min(1280px, 100%);
  align-items: start;
  gap: 22px;
}

.workspace-rail {
  position: sticky;
  top: 9rem;
  display: flex;
  flex-direction: column;
  gap: 14px;
  color: rgb(var(--wx-ink-subtle));
}

.rail-block {
  display: grid;
  gap: 3px;
  padding-left: 10px;
  border-left: 2px solid rgba(var(--wx-workspace-border), 0.9);
}

.rail-label {
  font-size: 10px;
  font-weight: 720;
  letter-spacing: 0;
  text-transform: uppercase;
}

.rail-block strong {
  color: rgb(var(--wx-ink));
  font-size: 12px;
  font-weight: 720;
}

.presence-cluster {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding-left: 3px;
}

.presence-avatar,
.presence-more {
  display: grid;
  width: 28px;
  height: 28px;
  place-items: center;
  border: 2px solid rgba(255, 255, 255, 0.92);
  border-radius: 999px;
  background: var(--presence-color);
  color: #ffffff;
  box-shadow: 0 12px 22px -18px rgba(15, 23, 42, 0.75);
  font-size: 11px;
  font-weight: 760;
}

.presence-more {
  background: rgb(var(--wx-ink));
}

.paper-stack {
  width: 100%;
  min-width: 0;
}

.editor-surface {
  width: 100%;
  min-height: 960px;
}

.floating-count {
  position: fixed;
  right: 24px;
  bottom: 20px;
  z-index: 40;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid rgba(var(--wx-workspace-border), 0.78);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.78);
  box-shadow: 0 16px 32px -28px rgba(15, 23, 42, 0.65);
  color: rgb(var(--wx-ink-subtle));
  font-size: 12px;
  font-weight: 650;
  backdrop-filter: blur(14px);
}

.floating-count strong {
  color: rgb(var(--wx-ink));
  font-weight: 760;
}

@media (max-width: 900px) {
  .editor-workspace {
    padding: 14px 14px 64px;
  }

  .editor-stage {
    grid-template-columns: 1fr;
  }

  .workspace-rail {
    position: static;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }

  .rail-block {
    padding-left: 0;
    border-left: 0;
  }
}
</style>
