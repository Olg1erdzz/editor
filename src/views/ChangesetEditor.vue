<template>
  <div class="grid flex-grow card place-content-center bg-gray-200">
    <editor-content :editor="editor" class="my-2" />
    <div class="bottomcount">
      字数统计:
      {{ editor?.storage.characterCount.characters() }}
    </div>
  </div>
</template>

<script lang="ts">
import { CassieKit } from "@/extension/CassieKit";
import { useEditor, EditorContent } from "@tiptap/vue-3";
import { reactive } from "vue";
import { DiffExtension } from "@/extension/track/DiffExtension";
import { UnitConversion } from "@/extension/page/core";
import { BuildRender } from "@/default";
import { pageContent, headerlist, footerlist } from "./content";
import StarterKit from "@tiptap/starter-kit";
import Image from "@tiptap/extension-image";
import History from "@tiptap/extension-history";
import CharacterCount from "@tiptap/extension-character-count";

const unitConversion = new UnitConversion();
export default {
  components: {
    EditorContent
  },
  setup() {
    let w = unitConversion.mmConversionPx(210);
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

    //编辑器实例
    let editor = useEditor({
      content: pageContent, //初始化编辑器内容
      injectCSS: false,
      extensions: [
        CharacterCount.configure({
          limit: 10000
        }),
        Image.configure({
          inline: true // 设置为内联模式，使图片和文字可以在同一行
        }),
        CassieKit.configure({
          textAlign: { types: ["heading", "paragraph"] },
          mention: {
            HTMLAttributes: {
              class: "bg-gray-300"
            },
            clickSuggestion: BuildRender(menulist) //编辑器右键菜单
          },
          page: {
            bodyPadding: 10,
            bodyWidth: w,
            headerHeight: 100,
            footerHeight: 60,
            bodyHeight: h,
            headerData: headerlist,
            footerData: footerlist
          },
          focus: false
        }),
        DiffExtension
      ]
    });
    const menus = reactive([
      [
        {
          icon: "save",
          text: "保存",
          title: "保存页眉页脚",
          click() {
            console.log("");
          }
        }
      ]
    ]);
    return {
      editor,
      menus
    };
  }
};
</script>
<style scoped>
.ProseMirror-focused {
}
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
</style>
