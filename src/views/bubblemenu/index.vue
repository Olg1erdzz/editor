<template>
  <BubbleMenu :editor="editor" pluginKey="textMenu" :shouldShow="states.shouldShow" :tippyOptions="{ popperOptions: { placement: 'top-start' } }" updateDelay="100">
    <ToolbarWrapper>
      <AIDropdown
        :onCompleteSentence="commands.onCompleteSentence"
        :onEmojify="commands.onEmojify"
        :onFixSpelling="commands.onFixSpelling"
        :onMakeLonger="commands.onMakeLonger"
        :onMakeShorter="commands.onMakeShorter"
        :onSimplify="commands.onSimplify"
        :onTldr="commands.onTldr"
        :onTone="commands.onTone"
        :onTranslate="commands.onTranslate"
      />
      <ToolbarDivider />
      <ContentTypePicker :options="blockOptions" />
      <FontFamilyPicker :onChange="commands.onSetFont" :value="states.currentFont || ''" />
      <FontSizePicker :onChange="commands.onSetFontSize" :value="states.currentSize || ''" />
      <ToolbarDivider />
      <Button tooltip="Bold" tooltipShortcut="['Mod', 'B']" @click="commands.onBold" :active="states.isBold">
        <Icon name="Bold" />
      </Button>
      <!-- ...其他按钮 -->
      <PopoverRoot>
        <PopoverTrigger asChild>
          <Button :active="!!states.currentHighlight" tooltip="Highlight text">
            <Icon name="Highlighter" />
          </Button>
        </PopoverTrigger>
        <PopoverContent side="top" sideOffset="8" asChild>
          <Surface class="p-1">
            <ColorPicker :color="states.currentHighlight" @onChange="commands.onChangeHighlight" @onClear="commands.onClearHighlight" />
          </Surface>
        </PopoverContent>
      </PopoverRoot>
      <!-- ...其他Popover组件 -->
    </ToolbarWrapper>
  </BubbleMenu>
</template>

<script setup>
import { ref, computed } from "vue";
import { useTextmenuCommands } from "./hooks/useTextmenuCommands";
import { useTextmenuStates } from "./hooks/useTextmenuStates";
import { useTextmenuContentTypes } from "./hooks/useTextmenuContentTypes";
import { BubbleMenu, EditorContent, Editor } from "@tiptap/vue-3";
import { ToolbarWrapper, ToolbarDivider, Button, Icon, PopoverRoot, PopoverTrigger, PopoverContent, Surface, AIDropdown, ContentTypePicker, FontFamilyPicker, FontSizePicker, ColorPicker } from "@/components/ui";

const editor = ref(null);

const commands = useTextmenuCommands(editor);
const states = useTextmenuStates(editor);
const blockOptions = useTextmenuContentTypes(editor);
</script>
