<template>
  <div class="fixed inset-x-0 bottom-8 z-50 flex justify-center pointer-events-none">
    <div 
      class="bg-white/90 backdrop-blur-xl border border-[var(--border-subtle)] shadow-2xl rounded-2xl p-1.5 flex items-center gap-1 pointer-events-auto"
      v-motion
      :initial="{ y: 100, opacity: 0 }"
      :enter="{ y: 0, opacity: 1 }"
    >
      <!-- History Group -->
      <div class="flex items-center gap-0.5 border-r border-[var(--border-subtle)] pr-1.5 mr-1">
        <ToolbarButton @click="editor.chain().focus().undo().run()" :disabled="!editor.can().undo()">
          <ArrowUturnLeftIcon class="w-4 h-4" />
        </ToolbarButton>
        <ToolbarButton @click="editor.chain().focus().redo().run()" :disabled="!editor.can().redo()">
          <ArrowUturnRightIcon class="w-4 h-4" />
        </ToolbarButton>
      </div>

      <!-- Formatting Group -->
      <div class="flex items-center gap-0.5">
        <ToolbarButton 
          @click="editor.chain().focus().toggleBold().run()" 
          :active="editor.isActive('bold')"
        >
          <BoldIcon class="w-4 h-4" />
        </ToolbarButton>
        <ToolbarButton 
          @click="editor.chain().focus().toggleItalic().run()" 
          :active="editor.isActive('italic')"
        >
          <ItalicIcon class="w-4 h-4" />
        </ToolbarButton>
        <ToolbarButton 
          @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" 
          :active="editor.isActive('heading', { level: 1 })"
        >
          <H1Icon class="w-4 h-4" />
        </ToolbarButton>
      </div>

      <!-- Alignment Group -->
      <div class="flex items-center gap-0.5 border-l border-[var(--border-subtle)] pl-1.5 ml-1">
        <ToolbarButton @click="editor.chain().focus().setTextAlign('left').run()" :active="editor.isActive({ textAlign: 'left' })">
          <Bars3BottomLeftIcon class="w-4 h-4" />
        </ToolbarButton>
        <ToolbarButton @click="editor.chain().focus().setTextAlign('center').run()" :active="editor.isActive({ textAlign: 'center' })">
          <Bars3Icon class="w-4 h-4" />
        </ToolbarButton>
      </div>

      <!-- Action Group -->
      <div class="flex items-center gap-0.5 border-l border-[var(--border-subtle)] pl-1.5 ml-1">
        <button 
          @click="$emit('save')"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded-xl text-xs font-bold transition-all shadow-lg shadow-blue-500/20 active:scale-95"
        >
          保存
        </button>
      </div>
    </div>
  </div>

  <!-- Side Quick Actions -->
  <div class="fixed right-6 top-1/2 -translate-y-1/2 z-40 flex flex-col gap-3">
    <div class="bg-white/80 backdrop-blur-lg border border-[var(--border-subtle)] shadow-xl rounded-2xl p-1.5 flex flex-col gap-1">
      <SideAction @click="$emit('toggle-ai')" tooltip="AI 助手">
        <SparklesIcon class="w-5 h-5 text-purple-600" />
      </SideAction>
      <SideAction @click="$emit('toggle-video')" tooltip="视频模式">
        <VideoCameraIcon class="w-5 h-5 text-gray-600" />
      </SideAction>
    </div>
  </div>
</template>

<script setup>
import { 
  ArrowUturnLeftIcon, 
  ArrowUturnRightIcon,
  Bars3BottomLeftIcon,
  Bars3Icon,
  VideoCameraIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline';

// Mocked icons since some specific ones might not be in standard heroicons
const BoldIcon = () => h('span', { class: 'font-bold' }, 'B');
const ItalicIcon = () => h('span', { class: 'italic' }, 'I');
const H1Icon = () => h('span', { class: 'font-black' }, 'H1');

import { h } from 'vue';

defineProps({
  editor: {
    type: Object,
    required: true
  }
});

const ToolbarButton = ({ active, disabled }, { slots, emit }) => {
  return h('button', {
    onClick: () => !disabled && emit('click'),
    class: [
      'w-8 h-8 flex items-center justify-center rounded-xl transition-all',
      active ? 'bg-blue-50 text-blue-600 shadow-inner' : 'hover:bg-gray-100 text-gray-600',
      disabled ? 'opacity-30 cursor-not-allowed' : 'cursor-pointer'
    ]
  }, slots.default());
};

const SideAction = ({ tooltip }, { slots, emit }) => {
  return h('button', {
    onClick: () => emit('click'),
    class: 'w-10 h-10 flex items-center justify-center rounded-xl hover:bg-white hover:shadow-md transition-all group relative'
  }, [
    slots.default(),
    h('span', {
      class: 'absolute right-full mr-3 px-2 py-1 bg-gray-900 text-white text-[10px] rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none'
    }, tooltip)
  ]);
};
</script>
