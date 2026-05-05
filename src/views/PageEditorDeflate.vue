<template>
  <div class="page-editor-workspace">
    <!-- 工具栏 -->
    <div class="editor-toolbar-shell">
      <FileTools
      :editor="editor"
      :document="document"
      :isMindMapLoading="isMindMapLoading"
      :mindmap="mindMap"
      :ifNoMindMap="ifNoMindMap"
      v-if="editor"
      @add-document="addDocument"
      @update-data="handleUpdateData"
      @record-button-clicked="showRecord"
      @video-mode-change="showVideo"
      @create-mindmap="loadingMindMap"
      @set-mode="handleSetMode"
      @open-chartsdialog="openChartsDialog"
      @open-success="openSuccess"
      ></FileTools>
    </div>
    <div class="record-strip">
      <Record 
      @toggle-drawer="toggleDrawer" 
      @transcription-uploaded="handleTranscriptionUploaded" 
      :document="document"
      v-if="isShowRecord"></Record>
    </div>

    <!-- 视频播放 -->
    <div
      class="video-panel"
      v-show="isShowVideo"
    >
    <video-player
		class="video-player vjs-custom-skin"
    ref="videoPlayer"
    :src="videoUrl"
    :playsinline="true"
    :options="playerOptions"
    ></video-player>
    <div class="video-url-row">
      <input v-model="videoUrl" type="text" placeholder="Enter new video URL" class="video-url-input" />
      <button 
      @click="updateVideoUrl(videoUrl)"
      class="video-upload-button"
      >
        <span class="relative z-10" v-if="!isLoading" >上传视频</span>
        <div v-else class='flex  space-x-2 justify-center items-center bg-white h-full w-full dark:invert'>
          <span class='sr-only'>Loading...</span>
           <div class='h-4 w-4 bg-black rounded-full animate-bounce [animation-delay:-0.3s]'></div>
         <div class='h-4 w-4 bg-black rounded-full animate-bounce [animation-delay:-0.15s]'></div>
         <div class='h-4 w-4 bg-black rounded-full animate-bounce'></div>
       </div>
      </button>
    </div>
    </div>
    <!-- 大纲 -->
    <div
    class="outline-panel"
    :class="{ 'outline-open': !isOutLineOpen }"
    v-show="!isShowVideo"
    >
      <button class="panel-toggle outline-toggle collapsed" @click="isOutLineOpen = !isOutLineOpen" v-if="!isOutLineOpen">
        <svg-icon name="汉堡包-展开" class="ml-2 absolute right-0 top-0"></svg-icon>
      </button>
      <button class="panel-toggle outline-toggle" @click="isOutLineOpen = !isOutLineOpen" v-if="isOutLineOpen">
        <svg-icon name="汉堡包-收缩" class="ml-2 absolute left-0 top-0"></svg-icon>
      </button>
      <Outline></Outline>
    </div>
    <!-- 内容 -->
    <editor-content 
    :class="{ 'mt-24': isDrawerOpen && isShowRecord, 'vieomode': isShowVideo , 'RAGMode': isRAG}" 
    class="editor-canvas" 
    :editor="editor" />
    <!-- 右侧 -->
    <div 
    v-show="isEditing" 
    class="inspector-panel" 
    :class="{ fullscreen: isFullscreen, 'drawer-open': isDrawerOpen2, 'top-[126px]': !isShowRecord, 'RAGMode': isRAG}">
      <button v-show="!isRAG" @click="isFullscreen = !isFullscreen" v-if="!isDrawerOpen2" class="panel-toggle inspector-toggle fullscreen-toggle">
        <svg-icon name="全屏" class="ml-2"></svg-icon>
      </button>
      <button v-show="!isRAG" @click="isDrawerOpen2 = !isDrawerOpen2" v-if="!isFullscreen" class="panel-toggle inspector-toggle drawer-toggle">
        <svg-icon name="抽屉2" class="ml-2"></svg-icon>
      </button>
      <CardGroup
      :isFullscreen="isFullscreen"
      :editor="editor"
      :transcriptions="transcriptions"
      :fileDataMap="fileDataMap"
      :isMindMapLoading="isMindMapLoading"
      :mindMap="mindMap"
      :document="document"
      :isOpenChartsDialog="isOpenChartsDialog"
      :selectedTextCC="selectedTextCC"
      @open-mindmap-modal="openMindMapModal"
      @close-chartsdialog="closeChartsDialog"
      @open-success="openSuccess"
      ></CardGroup>
    </div>
    <!-- 批注 -->
    <div v-show="!isEditing" class="comment-panel">
      <OuterCommentVue :active-comments-instance="activeCommentsInstance" :all-comments="allComments" :format-date="formatDate" :focus-content="focusContent" :is-comment-mode-on="isCommentModeOn" @set-comment="setComment" />
    </div>
    <!-- 对话机器人 -->
    <chatBot
      class="rag-panel"
      v-show="isRAG"
      :editor="editor"
      :document="document"
      :selected-text="selectedTextCC"
    ></chatBot>
    <!-- 编辑气泡菜单 -->
    <bubble-menu :editor="editor" :tippy-options="{ duration: 100 }" v-if="editor&&isEditing" link>
      <div class="format-bubble">
        <Menu as="div" class="relative inline-block text-left">
          <div>
            <MenuButton class="inline-flex w-full justify-center items-center gap-x-1.5 rounded-lg bg-white px-3 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              <div class="h-4 w-[90px] justify-center items-center flex flex-row gap-2" v-if="isLoading">
                <div class="w-2 h-2 rounded-full bg-sky-500 animate-bounce"></div>
                <div class="w-2 h-2 rounded-full bg-sky-500 animate-bounce [animation-delay:-.3s]"></div>
                <div class="w-2 h-2 rounded-full bg-sky-500 animate-bounce [animation-delay:-.4s]"></div>
              </div>
              <div class="inline-flex w-full justify-center items-center " v-else>
                <svg class="h-4 w-4 fill-sky-500 mr-1" viewBox="0 0 24 24">
                  <path
                    fill-rule="evenodd"
                    d="M9 4.5a.75.75 0 01.721.544l.813 2.846a3.75 3.75 0 002.576 2.576l2.846.813a.75.75 0 010 1.442l-2.846.813a3.75 3.75 0 00-2.576 2.576l-.813 2.846a.75.75 0 01-1.442 0l-.813-2.846a3.75 3.75 0 00-2.576-2.576l-2.846-.813a.75.75 0 010-1.442l2.846-.813A3.75 3.75 0 007.466 7.89l.813-2.846A.75.75 0 019 4.5zM18 1.5a.75.75 0 01.728.568l.258 1.036c.236.94.97 1.674 1.91 1.91l1.036.258a.75.75 0 010 1.456l-1.036.258c-.94.236-1.674.97-1.91 1.91l-.258 1.036a.75.75 0 01-1.456 0l-.258-1.036a2.625 2.625 0 00-1.91-1.91l-1.036-.258a.75.75 0 010-1.456l1.036-.258a2.625 2.625 0 001.91-1.91l.258-1.036A.75.75 0 0118 1.5zM16.5 15a.75.75 0 01.712.513l.394 1.183c.15.447.5.799.948.948l1.183.395a.75.75 0 010 1.422l-1.183.395c-.447.15-.799.5-.948.948l-.395 1.183a.75.75 0 01-1.422 0l-.395-1.183a1.5 1.5 0 00-.948-.948l-1.183-.395a.75.75 0 010-1.422l1.183-.395c.447-.15.799-.5.948-.948l.395-1.183A.75.75 0 0116.5 15z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                AI Tools
                <ChevronDownIcon class="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
              </div>
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
                  <button :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm w-full text-start']" @click="abstracts()">文本摘要</button>
                </MenuItem>
                <MenuItem v-slot="{ active }" class="rounded-md">
                  <div class="relative group text-start font-medium rounded-lg text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20" id="dropdown-cta">
                    <div :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm w-full text-start']" class="rounded-md" @click.stop>文本修饰</div>
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
                  <button :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm w-full text-start']" @click="modify()">病句改写</button>
                </MenuItem>
                <MenuItem v-slot="{ active }" class="rounded-md">
                  <div class="relative group text-start font-medium rounded-lg text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20" id="dropdown-cta">
                    <div :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm w-full text-start']" class="rounded-md" @click.stop>翻译</div>
                    <ul class="px-2 py-2 text-center z-10 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none hidden absolute left-52 -top-1 border group-hover:block">
                      <button class="hover:bg-gray-100 hover:text-gray-900 text-gray-700 px-4 py-2 text-sm w-full text-start rounded-md inline-flex items-center" @click="translate('中文')" value="中文">
                        <svg-icon name="简体中文" class="mr-2"></svg-icon>
                        中文
                      </button>
                      <button class="hover:bg-gray-100 hover:text-gray-900 text-gray-700 px-4 py-2 text-sm w-full text-start rounded-md inline-flex items-center" @click="translate('英文')" value="英文">
                        <svg-icon name="flag-uk" class="mr-2"></svg-icon>
                        英文
                      </button>
                      <button class="hover:bg-gray-100 hover:text-gray-900 text-gray-700 px-4 py-2 text-sm w-full text-start rounded-md inline-flex items-center" @click="translate('德语')" value="德语">
                        <svg-icon name="Germany" class="mr-2"></svg-icon>
                        德语
                      </button>
                      <button class="hover:bg-gray-100 hover:text-gray-900 text-gray-700 px-4 py-2 text-sm w-full text-start rounded-md inline-flex items-center" @click="translate('俄语')" value="俄语">
                        <svg-icon name="俄罗斯" class="mr-2"></svg-icon>
                        俄语
                      </button>
                      <div class="w-full inline-flex justify-between items-center py-1">
                        <input
                          type="text"
                          v-model="inputText"
                          class="w-20 px-4 py-2 h-7 ml-3 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                          placeholder="语言"
                          @click.stop
                        />
                        <button type="button" @click="translate(inputText)" class="hover:bg-gray-100 hover:text-gray-900 text-gray-700 block mx-2 px-2 py-2 text-sm w-full text-start rounded-md">输入语言</button>
                      </div>
                    </ul>
                  </div>
                </MenuItem>
              </div>
              <div class="py-1">
                <MenuItem v-slot="{ active }" class="rounded-md">
                  <button :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm w-full text-start']" @click="autosort()">自动排版</button>
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
          <svg-icon name="斜体" color="black"></svg-icon>
        </button>

        <!-- 下划 -->
        <button
          class="flex select-none items-center gap-2 rounded-lg py-1 px-2 text-center align-middle font-sans text-xs font-bold uppercase text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
          type="button"
          data-ripple-dark="true"
          @click="editor.chain().focus().toggleUnderline().run()"
          :class="{ 'hover:bg-gray-900/10': editor.isActive('underline') }"
        >
          <svg-icon name="下划线" color="black"></svg-icon>
        </button>

        <button
          class="flex select-none items-center gap-2 rounded-lg py-1 px-2 text-center align-middle font-sans text-xs font-bold uppercase text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
          type="button"
          data-ripple-dark="true"
          @click="editor.chain().focus().toggleStrike().run()"
          :class="{ 'is-active': editor.isActive('strike') }"
        >
          <svg-icon name="中划线" color="black"></svg-icon>
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
          <svg-icon name="代码 (1)" color="black"></svg-icon>
        </button>
      </div>

      <!-- stylesheet -->

      <!-- Ripple Effect from cdn -->
    </bubble-menu>
    <!-- 批注气泡菜单 -->
    <BubbleMenu v-if="editor&&!isEditing" :tippy-options="{ duration: 100, placement: 'bottom' }" :editor="editor" :should-show="({ editor }) => isCommentModeOn && !editor.state.selection.empty && !activeCommentsInstance.uuid" class="comment-bubble">
      <div class="comment-bubble-inner">
        <h2 class="card-title">评论</h2>
        <div class="card-body" style="padding: 15px">
          <textarea class="textarea textarea-bordered" v-model="commentText" cols="30" rows="4" placeholder="添加新的批注" @keypress.enter.stop.prevent="() => setComment()" />
        </div>

        <div class="card-actions">
          <button class="btn btn-outline btn-xs" @click="() => setComment()">添加</button>
          <button class="btn btn-outline btn-xs" @click="() => (commentText = '')">清空</button>
        </div>
      </div>
    </BubbleMenu>
    <!-- 字数统计 -->
    <div class="bottomcount" >

      字数统计:
      {{ editor?.storage.characterCount.characters() }}
    </div>
  </div>

  <!-- success -->
  <transition name="modal-fade">
    <div  v-show="isSuccess"
      class="fixed inset-0 z-10 top-64 overflow-y-auto"
      aria-labelledby="modal-title" role="dialog" aria-modal="true"
      @click.self="closeSuccess"
    >
  <div class="flex items-center justify-center">
    <div class="rounded-lg bg-gray-50 px-16 py-14">
      <div class="flex justify-center">
        <div class="rounded-full bg-green-200 p-6">
          <div class="flex h-16 w-16 items-center justify-center rounded-full bg-green-500 p-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-8 w-8 text-white">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
            </svg>
          </div>
        </div>
      </div>
      <h3 class="my-4 text-center text-3xl font-semibold text-gray-700">Congratuation!!!</h3>
      <p class="w-[230px] text-center font-normal text-gray-600">您的请求已经完成</p>
      <button @click="isSuccess = false" class="mx-auto mt-10 block rounded-xl border-4 border-transparent bg-orange-400 px-6 py-3 text-center text-base font-medium text-orange-100 outline-8 hover:outline hover:duration-300"> OK</button>
    </div>
  </div>
</div>
</transition>
</template>

<script lang="ts">
import applyDevTools from "prosemirror-dev-tools";
import { pageContent, headerlist, footerlist, pageContentHtml, resumeTemplate } from "./content";
import { UnitConversion } from "@/extension/page/core";
import { BubbleMenu, EditorContent, Editor } from "@tiptap/vue-3";
import { onBeforeUnmount, onMounted, PropType, reactive, ref, shallowRef, unref, watchEffect, h, type Component, defineComponent } from "vue";
import { BuildRender, ContextMenuOptions } from "@/default";
import { CassieKit, Comment} from "@/extension";
import { storeToRefs } from "pinia";
import { useEditorStore } from "@/store";
import LinkButton from "./filetools/LinkButton.vue";
import FileTools from "./filetools/FileTools.vue";
// 图片编辑
import Image from '@tiptap/extension-image';
import ImageResize from "tiptap-extension-resize-image";
// 回退
import History from "@tiptap/extension-history";
// 文字样式
import TextStyle from "@tiptap/extension-text-style";
import FontFamily from "@tiptap/extension-font-family";
import FontSize from "tiptap-extension-font-size";
import { Color } from "@tiptap/extension-color";
// 字数统计
import CharacterCount from "@tiptap/extension-character-count";
// 大纲
import Outline from "./outline/index.vue";
import Record from "./record/index.vue";
import chatBot from "./home.vue";
import CardGroup from "./cardgroup/index.vue";
import axios from "axios";
import { Menu, MenuButton, MenuItem, MenuItems, TransitionRoot, TransitionChild, Dialog, DialogPanel, DialogTitle } from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import { Document } from "@/types/types"; // 这里导入Document类型

// CommentEditor
import OuterCommentVue from "./OuterComment.vue";
import { Editor as E } from "@tiptap/core";
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import { v4 as uuidv4 } from "uuid";
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import format from "date-fns/format";
import { DiffExtension } from "@/extension/track";
import { modifyAwarenessUpdate } from "y-protocols/awareness";
import { Loading } from "@icon-park/vue-next";
import baseUrl from "@/store/baseUrl";
import { vi } from "date-fns/locale";

const unitConversion = new UnitConversion();
export default defineComponent({
  props: {
    document: {
      type: Object as PropType<Document>,
      required: true
    }
  },
  components: {
    LinkButton,
    EditorContent,
    FileTools,
    Record,
    CardGroup,
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
    ChevronDownIcon,
    OuterCommentVue,
    chatBot
  },
  data() {
    return {
      videoUrl: '',
      isEditing: true,
      isMindMapLoading: false,
      mindMap: "",
      isOpen: false,
      modalTitle: "",
      currentMethod: "",
      inputLable: "",
      length: "",
      textInputStyle: "", // 绑定输入框的数据
      isDrawerOpen: false,
      transcriptions: [] as Array<{ Id: number; transcription: string; currentTime: string; name: string }>,
      inputText: "",
      fileDataMap: {},
      options: {
        //是否显示两侧的箭头
        controlArrows: true,
        //是否可以使用键盘方向键导航（上下键翻页），默认为true
        keyboardScrolling: true,
        //设置每个section顶部的padding，当我们要设置一个固定在顶部的菜单、导航、元素等时使用
        paddingTop: "-100px",
        //是否包含滚动条，设为true，则浏览器自带的滚动条会出现，页面还是按页滚动，但是浏览器滚动条默认行为也有效
        scrollBar: false,
        //是否使用插件滚动方式，设为false后，会出现浏览器自带的滚动条，将不会按页滚动
        autoScrolling: false,
        //是否显示两侧的箭头
        licenseKey: "OPEN-SOURCE-GPLV3-LICENSE",
        //是否显示导航，默认为false
        navigation: true,
        //为每个section设置背景色
        sectionsColor: ["#41b883"]
      },
      playerOptions: {
        playbackRates: [0.5, 1.0, 1.5, 2.0, 4.0, 8.0], //可选择的播放速度
        autoplay: false, //如果true,浏览器准备好时开始回放。
        muted: false, // 默认情况下将会消除任何音频。
        loop: false, // 视频一结束就重新开始。
        preload: "auto", // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: "zh-CN",
        aspectRatio: "16:9", // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        sources: [
          {
            type: "",
            src: "https://prod-streaming-video-msn-com.akamaized.net/a8c412fa-f696-4ff2-9c76-e8ed9cdffe0f/604a87fc-e7bc-463e-8d56-cde7e661d690.mp4" //url地址
          }
        ],
        //poster: "../assets/img/home_top.jpg", //你的封面地址
        // width: document.documentElement.clientWidth,
        notSupportedMessage: "此视频暂无法播放，请稍后再试", //允许覆盖Video.js无法播放媒体源时显示的默认信息。
        controlBar: {
          timeDivider: true, //当前时间和持续时间的分隔符
          durationDisplay: true, //显示持续时间
          remainingTimeDisplay: false, //是否显示剩余时间功能
          fullscreenToggle: true //全屏按钮
        }
      },

      isFullscreen: false,
      isDrawerOpen2: false,
      isOutLineOpen: true,
      isShowRecord: false,
      isShowVideo: false,
      ifNoMindMap:false,
      isRAG: false,
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


    handleSetMode(mode: number){
      console.log(mode);
      switch(mode) {
        case 1:
          // 执行当 mode 为 1 时的操作
          this.isRAG = false;
          this.isEditing = true;
          this.isOutLineOpen = true;
          break;
        case 2:
          this.isEditing = false;
          break;
        case 3:
          // 执行当 mode 为 3 时的操作
          this.isRAG = true;
          this.isOutLineOpen = false;
          break;
        default:
          // 执行当 mode 不是 1、2 或 3 时的操作
          break;
      }
    },
    openMindMapModal(value: boolean){
      this.ifNoMindMap = value;
    },
    loadingMindMap(value: boolean, mindmap: string){
      this.isMindMapLoading = value;
      this.mindMap = mindmap;
    },
    showVideo(value: boolean) {
      console.log('value', value);
      this.isShowVideo = !this.isShowVideo;
      if(value){
        this.isOutLineOpen = false;
        this.isDrawerOpen2 = true;
      } else {
        this.isOutLineOpen = true;
        this.isDrawerOpen2 = false;
      }
    },
    showRecord() {
      console.log("显示录音条");
      this.isShowRecord = !this.isShowRecord;
      this.isDrawerOpen = false;
      console.log(this.isShowRecord);
    },
    handleTranscriptionUploaded(response) {
      this.transcriptions.push(response);
    },

    toggleDrawer() {
      this.isDrawerOpen = !this.isDrawerOpen;
    },
    handleUpdateData(data) {
      this.fileDataMap = data;
    },
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
    },
    addDocument(document: Document) {
      this.$emit("add-document", document);
    }
  },
  setup(props) {
    //CommentEditor
    let w = unitConversion.mmConversionPx(210);
    let h = unitConversion.mmConversionPx(297);
    const dateTimeFormat = "yyyy.MM.dd HH:mm";

    const formatDate = (d: any) => (d ? format(new Date(d), dateTimeFormat) : null);
    const currentUserName = ref("黄医生");

    const commentText = ref("");
    const isSuccess = ref(false);

    const showCommentMenu = ref(false);

    const isLoading = ref(false);

    const isCommentModeOn = ref(false);

    const isTextSelected = ref(false);
    const isOpenChartsDialog = ref(false);
    const selectedTextCC = ref("");
    const showAddCommentSection = ref(true);

    interface CommentInstance {
      uuid?: string;
      comments?: any[];
    }

    const activeCommentsInstance = ref<CommentInstance>({});

    const allComments = ref<any[]>([]);

    const findCommentsAndStoreValues = (editor: E) => {
      const tempComments: any[] = [];

      editor.state.doc.descendants((node, pos) => {
        const { marks } = node;

        marks.forEach((mark) => {
          if (mark.type.name === "comment") {
            const markComments = mark.attrs.comment;

            const jsonComments = markComments ? JSON.parse(markComments) : null;

            if (jsonComments !== null) {
              tempComments.push({
                node,
                jsonComments,
                from: pos,
                to: pos + (node.text?.length || 0),
                text: node.text
              });
            }
          }
        });
      });

      allComments.value = tempComments;
    };

    const { log } = console;

    const setCurrentComment = (editor: E) => {
      const newVal = editor.isActive("comment");

      if (newVal) {
        setTimeout(() => (showCommentMenu.value = newVal), 50);

        showAddCommentSection.value = !editor.state.selection.empty;

        const parsedComment = JSON.parse(editor.getAttributes("comment").comment);

        parsedComment.comment = typeof parsedComment.comments === "string" ? JSON.parse(parsedComment.comments) : parsedComment.comments;

        activeCommentsInstance.value = parsedComment;
      } else {
        activeCommentsInstance.value = {};
      }
    };

    const getIsCommentModeOn = () => isCommentModeOn.value;
    // const editor = shallowRef<Editor>();
    const setComment = (val?: string) => {
      const localVal = val || commentText.value;

      if (!localVal.trim().length) return;

      const activeCommentInstance: CommentInstance = JSON.parse(JSON.stringify(activeCommentsInstance.value));
      const commentsArray = typeof activeCommentInstance.comments === "string" ? JSON.parse(activeCommentInstance.comments) : activeCommentInstance.comments;

      if (commentsArray) {
        commentsArray.push({
          userName: currentUserName.value,
          time: Date.now(),
          content: localVal
        });

        const commentWithUuid = JSON.stringify({
          uuid: activeCommentsInstance.value.uuid || uuidv4(),
          comments: commentsArray
        });
        editor.value?.chain().setComment(commentWithUuid).run();
      } else {
        const commentWithUuid = JSON.stringify({
          uuid: uuidv4(),
          comments: [
            {
              userName: currentUserName.value,
              time: Date.now(),
              content: localVal
            }
          ]
        });
        editor.value?.chain().setComment(commentWithUuid).run();
      }

      setTimeout(() => (commentText.value = ""), 50);
    };

    const toggleCommentMode = () => {
      isCommentModeOn.value = !isCommentModeOn.value;
      if (isCommentModeOn.value) editor.value?.setEditable(false);
      else editor.value?.setEditable(true);
    };

    const focusContent = ({ from, to }: { from: number; to: number }) => {
      editor.value?.chain().setTextSelection({ from, to }).run();
    };
    onBeforeUnmount(() => {
      editor.value?.destroy();
    });
    onMounted(() => {
      toggleCommentMode();
      //编辑器实例
      editor.value = new Editor({
        onUpdate({ editor }) {
          findCommentsAndStoreValues(editor);
          setCurrentComment(editor);
        },
        onSelectionUpdate({ editor }) {
          setCurrentComment(editor);
          isTextSelected.value = !!editor.state.selection.content().size;
        },

        onCreate({ editor }) {
          findCommentsAndStoreValues(editor);
        },
        editorProps: {
          attributes: {
            class: "divide-y divide-black-600"
          }
        },
        content: pageContentHtml, //初始化编辑器内容
        injectCSS: false,
        extensions: [
          CharacterCount.configure({
            limit: 10000
          }),
          CassieKit.configure({
            textAlign: { types: ["heading", "paragraph"] },
            mention: {
              HTMLAttributes: {
                class: "bg-gray-300"
              }
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
          DiffExtension,
          Comment.configure({ isCommentModeOn: getIsCommentModeOn })
        ]
      });
    });
    let bodyWidth = unitConversion.mmConversionPx(210);
    // let h = unitConversion.mmConversionPx(297);
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
   
    // 解析url
    const updateVideoUrl = async (videoUrl: string) => {
      isLoading.value = true;
      console.log(videoUrl);

      // Inserting the summary text before sending the request
      if (editor.value) {
        const summaryText = '<p style="font-size:30px; font-weight:bold;">摘要:</p><p style="font-size:20px; font-weight:normal;"><br/>';
        editor.value.commands.insertContent(summaryText);
      }

      try {
        const response = await axios.post('/video_upload', {
            url: videoUrl
        });
        console.log("解析url");
        console.log(response);
        if (editor.value) {
            // Convert the response to a string and split it into an array of characters
            const responseChars = response.toString().split('');
            let i = 0;
            // Use setInterval to insert the characters one by one
            const intervalId = setInterval(() => {
              if (i < responseChars.length) {
                editor.value.commands.insertContent(responseChars[i]);
                i++;
              } else {
                // Once all characters have been inserted, clear the interval
                clearInterval(intervalId);
              }
            }, 100); // Adjust the interval as needed
          };
      } catch (error) {
        console.error(error);
      } finally {
        isLoading.value = false;
      }
    };
    // 打开图表
    const openChartsDialog = () => {
      if (editor.value) {
        const { from, to, empty } = editor.value.state.selection;
        if (!empty) {
          const selectedText = editor.value.state.doc.textBetween(from, to, " ");
          selectedTextCC.value = selectedText;
          isOpenChartsDialog.value = !isOpenChartsDialog.value;
        }
      }
      console.log('打开图表模态框')
    };

    const openSuccess = () => {
      isSuccess.value = true;
    };
    const closeSuccess = () => {
      isSuccess.value = false;
    };
    const closeChartsDialog = () => {
      isOpenChartsDialog.value = false;
    };
    // 获取当前光标选中文本并发送给后端替换
    const getSelectedText = async (style: string) => {
      if (editor.value) {
        isLoading.value = true;
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
          } finally {
            isLoading.value = false;
          }
        }
      }
    };

    // 续写
    const extend = async (length: string) => {
      if (editor.value) {
        isLoading.value = true;
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
          } finally {
            isLoading.value = false;
          }
        }
      }
    };

    // 摘要
    const abstracts = async () => {
      isLoading.value = true;
      if (editor.value) {
        const { from, to, empty } = editor.value.state.selection;
        if (!empty) {
          const selectedText = editor.value.state.doc.textBetween(from, to, " ");
          console.log(selectedText);
          console.log("摘要");
          try {
            const response = await axios.post(
              "http://127.0.0.1:5000/api/abstracts",
              {
                text: selectedText
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
          } finally {
            isLoading.value = false;
          }
        }
      }
    };

    // 病句改写
    const modify = async () => {
      if (editor.value) {
        isLoading.value = true;
        const { from, to, empty } = editor.value.state.selection;
        if (!empty) {
          const selectedText = editor.value.state.doc.textBetween(from, to, " ");
          console.log(selectedText);
          console.log("病句改写");
          try {
            const response = await axios.post(
              "http://127.0.0.1:5000/api/modify",
              {
                text: selectedText
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
          } finally {
            isLoading.value = false;
          }
        }
      }
    };

    // 翻译
    const translate = async (target_language: string) => {
      if (editor.value) {
        isLoading.value = true;
        const { from, to, empty } = editor.value.state.selection;
        if (!empty) {
          const selectedText = editor.value.state.doc.textBetween(from, to, " ");
          console.log(selectedText);
          console.log("翻译");
          try {
            const response = await axios.post(
              "http://127.0.0.1:5000/api/translate",
              {
                text: selectedText,
                target_language: target_language
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
          } finally {
            isLoading.value = false;
          }
        }
      }
    };
    // 排版

    const autosort = async () => {
      if (editor.value) {
        isLoading.value = true;
        // 获取编辑器中的HTML内容
        const html = editor.value.getHTML();
        console.log(html);
        try {
          const response = await axios.post(
            "http://127.0.0.1:5000/api/sort",
            {
              text: html
            },
            {
              headers: {
                "Content-Type": "application/json"
              }
            }
          );
          console.log(response);
          if (editor.value) {
            // editor.value.commands.insertContent(processedText);
            processArrayAndInsertIntoEditor(editor.value, response);
          }
        } catch (error) {
          if (error instanceof Error) {
            console.error(error.message);
          } else {
            console.error("未知错误", error);
          }
        } finally {
          isLoading.value = false;
        }
      }
    };
    // 自动排版算法
    const processArrayAndInsertIntoEditor = (editor: Editor, array: [string, string][]) => {
  array.forEach(([text, format]) => {
    // Start a chain of commands
    let chain = editor.chain().focus();
    console.log(text);
    // Insert the text
    chain.insertContent(text);

    // Apply formatting based on the format type
    switch (format) {
      case 'Title':
        chain
          .setParagraph() // Reset to default paragraph
          .toggleHeading({ level: 1 }) // Set as heading 1
          .setTextAlign("center") // Center align
          .toggleBold(); // Make bold
        break;
      case 'Heading 1':
        chain
          .setParagraph() // Reset to default paragraph
          .toggleHeading({ level: 1 }); // Set as heading 1
        break;
      case 'Heading 2':
        chain
          .setParagraph() // Reset to default paragraph
          .toggleHeading({ level: 2 }); // Set as heading 2
        break;
      case 'Heading 3':
        chain
          .setParagraph() // Reset to default paragraph
          .toggleHeading({ level: 3 }) // Set as heading 3
          .setTextAlign("left"); // Left align
        break;
      case 'Quote':
        chain
          .setParagraph() // Reset to default paragraph
          .setFontFamily('cursive') // Set font family to cursive
          .toggleOrderedList() // Set as ordered list
          .setTextAlign("left"); // Left align
        break;
      case 'Tables':
        chain
          .setParagraph() // Reset to default paragraph
          .toggleOrderedList() // Set as ordered list
          .setTextAlign("left"); // Left align
        break;
      case 'Caption':
        chain
          .setParagraph() // Reset to default paragraph
          .setTextAlign("center"); // Center align
        break;
      case 'Body':
        chain
          .setParagraph(); // Reset to default paragraph
        break;
      default:
        console.warn(`Unknown format type: ${format}`);
    }

    // Run the chain of commands
    chain.run();

    // Move the cursor to the end of the document
    const endOfDocPos = editor.state.doc.content.size;
    editor.commands.setTextSelection({ from: endOfDocPos, to: endOfDocPos });
  });
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
          Image.configure({
            inline: true,
          }),
          ImageResize.configure({
            inline: true,
          }),
          CharacterCount.configure({
            limit: 10000
          }),
          FontFamily.configure({
            types: ["textStyle"]
          }),
          FontSize,
          Color,
          TextStyle,
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
      // 如果有传递的document内容，加载到编辑器
      if (props.document) {
        editor.value.commands.setContent(props.document.content);
      }
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
    return { 
      pageContent, 
      menulist, 
      headerlist, 
      footerlist, 
      onUpdate, 
      onCreate, 
      editor, 
      bodyWidth, 
      getSelectedText, 
      extend, 
      modify,
      autosort, 
      abstracts, 
      translate,
      focusContent,
      toggleCommentMode,
      setComment,
      getIsCommentModeOn,
      setCurrentComment,
      findCommentsAndStoreValues,
      commentText,
      isLoading,
      isCommentModeOn,
      activeCommentsInstance,
      allComments,
      formatDate,
      openChartsDialog,
      closeChartsDialog,
      openSuccess,
      isSuccess,
      isOpenChartsDialog,
      selectedTextCC,
      closeSuccess,
      updateVideoUrl
    };
  }
});
</script>

<style scoped>
.page-editor-workspace {
  position: relative;
  min-height: calc(100vh - 4rem);
  background:
    linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
  color: #1f2937;
}

.editor-toolbar-shell {
  position: fixed;
  top: 4rem;
  left: 0;
  right: 0;
  z-index: 50;
  overflow: visible;
  min-height: 58px;
  border-bottom: 1px solid #d8dee8;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
}

.editor-toolbar-shell :deep(.el-button),
.editor-toolbar-shell :deep(button) {
  border-radius: 6px;
}

.record-strip {
  position: fixed;
  top: 122px;
  left: 0;
  right: 0;
  z-index: 40;
  border-bottom: 1px solid #d8dee8;
  background: #ffffff;
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
}

.editor-canvas {
  display: block;
  min-height: calc(100vh - 4rem);
  padding: 104px 360px 58px 304px;
  transition: transform 0.25s ease, padding 0.25s ease;
}

.editor-canvas :deep(.ProseMirror) {
  min-height: 100%;
  outline: none;
}

.editor-canvas :deep(.Page) {
  margin: 18px auto;
  border: 1px solid #e2e8f0;
  box-shadow: 0 16px 38px rgba(15, 23, 42, 0.12);
}

.outline-panel,
.inspector-panel,
.comment-panel,
.rag-panel {
  position: fixed;
  z-index: 20;
  border: 1px solid #d8dee8;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 14px 34px rgba(15, 23, 42, 0.08);
}

.outline-panel {
  top: 146px;
  left: 18px;
  width: 272px;
  max-height: calc(100vh - 178px);
  overflow: auto;
  padding: 12px;
  transition: transform 0.25s ease;
}

.inspector-panel,
.comment-panel {
  top: 136px;
  right: 16px;
  width: 330px;
  max-height: calc(100vh - 168px);
  overflow: auto;
  padding: 12px;
  transition: transform 0.25s ease, width 0.25s ease, height 0.25s ease;
}

.rag-panel {
  top: 82px;
  right: 24px;
  width: 360px;
  max-height: calc(100vh - 104px);
  overflow: auto;
  padding: 12px;
  transition: transform 0.25s ease;
}

.panel-toggle {
  position: absolute;
  display: grid;
  width: 30px;
  height: 30px;
  place-items: center;
  border: 1px solid #d8dee8;
  border-radius: 6px;
  background: #ffffff;
  color: #475569;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
}

.panel-toggle:hover {
  border-color: #94a3b8;
  background: #f8fafc;
  color: #0f172a;
}

.outline-toggle {
  top: 10px;
  right: 10px;
}

.outline-toggle.collapsed {
  right: -42px;
}

.inspector-toggle {
  left: -36px;
}

.fullscreen-toggle {
  top: 10px;
}

.drawer-toggle {
  top: 48px;
}

.video-panel {
  position: fixed;
  top: 132px;
  left: 20px;
  z-index: 25;
  width: min(796px, calc(100vw - 390px));
  min-height: 490px;
  padding: 12px;
  border: 1px solid #d8dee8;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 16px 38px rgba(15, 23, 42, 0.12);
}

.video-url-row {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.video-url-input {
  min-width: 0;
  flex: 1;
  height: 40px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: #ffffff;
  color: #1f2937;
  padding: 0 12px;
  outline: none;
}

.video-url-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.video-upload-button {
  display: inline-flex;
  width: 120px;
  height: 40px;
  align-items: center;
  justify-content: center;
  border: 1px solid #2563eb;
  border-radius: 6px;
  background: #2563eb;
  color: #ffffff;
  font-weight: 600;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.video-upload-button:hover {
  border-color: #1d4ed8;
  background: #1d4ed8;
}

.format-bubble {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px;
  border: 1px solid #d8dee8;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 14px 34px rgba(15, 23, 42, 0.14);
}

.format-bubble button {
  min-width: 30px;
  min-height: 30px;
  border-radius: 6px;
}

.format-bubble .is-active {
  background: #ecfdf5;
  color: #0f766e;
}

.comment-bubble {
  border: 0;
  border-radius: 8px;
  background: transparent;
  box-shadow: none;
}

.comment-bubble-inner {
  width: 280px;
  padding: 12px;
  border: 1px solid #d8dee8;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 14px 34px rgba(15, 23, 42, 0.14);
  text-align: left;
}

.comment-bubble-inner :deep(.card-title) {
  margin: 0 0 8px;
  color: #1f2937;
  font-size: 15px;
}

.bottomcount {
  position: fixed;
  right: 18px;
  bottom: 14px;
  z-index: 30;
  display: inline-flex;
  min-height: 32px;
  align-items: center;
  padding: 0 12px;
  border: 1px solid #d8dee8;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.94);
  color: #64748b;
  font-size: 13px;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
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
.fullscreen {
  position: fixed;
  top: 4rem;
  right: 0;
  width: 420px;
  height: calc(100vh - 4rem);
  z-index: 9999;
  background: #ffffff;
  border-radius: 0;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.drawer-open {
  transform: translateX(380px);
  transition: transform 0.25s ease-in-out;
}
.outline-open {
  transform: translateX(-330px);
  transition: transform 0.25s ease-in-out;
}
.vieomode {
  transform: translateX(420px);
  transition: transform 0.25s ease-in-out;
}
.RAGMode {
  transform: translateX(-420px);
  transition: transform 0.25s ease-in-out;
}
.ProseMirror-focused {
}
.comment {
  background: rgba(250, 250, 0, 0.25);
  border-bottom: 2px rgb(255, 183, 0) solid;
  user-select: all;
  padding: 0 2px 0 2px;
  border-radius: 4px;
}
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease-out, opacity 0.2s ease-in;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-to, .modal-fade-leave-from {
  opacity: 1;
}

@media (max-width: 1200px) {
  .editor-canvas {
    padding-right: 24px;
  }

  .inspector-panel,
  .comment-panel,
  .rag-panel {
    transform: translateX(380px);
  }
}

@media (max-width: 860px) {
  .editor-canvas {
    padding: 104px 14px 58px;
  }

  .outline-panel {
    transform: translateX(-330px);
  }

  .video-panel {
    left: 12px;
    width: calc(100vw - 24px);
  }
}
</style>
