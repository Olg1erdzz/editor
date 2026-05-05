<template>
  <!-- component -->
  <div class="w-full max-w-sm flex flex-col mx-auto text-center">
    <div v-data="{ selected: true }" class="w-full rounded bg-white h-auto m-auto shadow flex flex-col p-2 rounded-xl">
      <div class="relative w-full rounded-md border h-10 p-1 bg-gray-200">
        <div class="relative w-full h-full flex items-center">
          <div @click="selected=!selected; $emit('toggle-display', selected); isMindMapVisible = false" class="w-full flex justify-center text-gray-400 cursor-pointer">
            <button>多模态数据中心</button>
          </div>
          <div @click="selected=!selected; $emit('toggle-display', selected); isMindMapVisible = true" class="w-full flex justify-center text-gray-400 cursor-pointer">
            <button>思维导图</button>
          </div>
        </div>
        <span :class="{ 'left-1/2 -ml-1 text-orange-500 font-semibold':!selected, 'left-1 text-indigo-600 font-semibold':selected }"
          v-text="selected ? '多模态数据中心' : '思维导图'"
          class="bg-white shadow text-sm flex items-center justify-center w-1/2 rounded h-[1.88rem] transition-all duration-150 ease-linear top-[4px] absolute"></span>
      </div>
      
    </div>

  </div>
  <!-- 壳子 -->
  <div class="h-[76vh] bg-white rounded-xl shadow-xl mt-3 opacity-80 overflow-y-auto whitespace-normal overflow-auto scrollbar-hide" :class="{ 'w-3/12 h-[777px] float-left': isFullscreen }">
  <!-- 卡片组 -->
   
  <transition name="slide-fade">
    <div v-if="!isMindMapVisible" class="w-full ">
      <VueDraggable
        ref="el"
        v-model="list"
        ghostClass="ghost"
        class="flex flex-col gap-2 p-2 w-full h-300px m-auto rounded transition-all duration-500"
        @update="onUpdate"
        handle=".handle"
      >
      <TransitionGroup
        type="transition"
        name="fade"
        class="sort-target"
      >
      <!-- 识别录音记录 -->
      <li
      v-for="(item, index) in transcriptions" :key="index"
      class="p-1 mb-3 items-center justify-center w-full rounded-xl group sm:flex space-x-6  bg-opacity-50 shadow-xl hover:rounded-2xl bg-gradient-to-r from-violet-200 to-pink-200"
      >
      <div class="inline-flex items-center">
        <label
          class="relative flex cursor-pointer items-center rounded-full"
          for="checkbox-1"
          data-ripple-dark="true"
        >
          <input
            type="checkbox"
            class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-md border border-blue-gray-200 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-pink-500 checked:bg-pink-500 checked:before:bg-pink-500 hover:before:opacity-10"
            id="checkbox-1"
             :value="item" @change="selectId(item, 'audio')"
          />
          <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-white opacity-0 transition-opacity peer-checked:opacity-100">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-3.5 w-3.5"
              viewBox="0 0 20 20"
              fill="currentColor"
              stroke="currentColor"
              stroke-width="1"
            >
              <path
                fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
        </label>
      </div>
      <!-- <svg-icon name="draggable" class="handle"></svg-icon> -->
        <div class="sm:w-8/12 pl-0 p-5 relative">
                  <button
                  class="hover:bg-blue-200 hover:rounded-full absolute -right-6"
                  @click="deleteItem(index)"
                  >
                      <svg-icon name="关闭"></svg-icon>
                  </button>
          <div class="space-y-2">
            <div class="space-y-4">
                    {{ item.name }}
            </div>
            <div
            class="space-y-4 bg-gray-50 bg-opacity-80 rounded-lg shadow-inner px-3 py-1 ease-in-out duration-100 transition-all"
            @click="toggleDisplay(index)"
            draggable="true" @dragstart="dragStart($event, item.transcription)" @dragend="dragEnd"
            >
              <div v-if="item.showExtracted">
                <div v-for="(info, i) in item.extractedData" :key="i">
                  <div v-if="i >= 0">
                    {{ info }}: {{ item.answers[i]}}
                  </div>
                </div>
              </div>
              <div v-else title=item.transcription
              >
              {{ item.transcription.length > 30 ? item.transcription.slice(0, 30) + '...' : item.transcription }}
              </div>
            </div>
            <div class="flex items-center space-x-4 justify-between">
            <div class="text-grey-500 flex flex-row space-x-1  my-4 h-9">
              <svg stroke="currentColor" fill="none" stroke-width="0" viewBox="0 0 24 24" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <p class="text-xs">{{ item.currentTime }}</p>
            </div>
            <div class="flex flex-row space-x-1 relative">
              <div
              class="bg-red-200 shadow-lg shadow- hover:shadow-red-300 hover:scale-95 text-white cursor-pointer px-3 py-1 text-center justify-center items-center rounded-xl flex space-x-2 flex-row absolute right-20"
              @click="insertText(item.transcription)"
              >
              <span class="text-nowrap">插入</span>
              </div>
              <div
              class="bg-emerald-200 shadow-lg shadow- hover:shadow-emerald-300 hover:scale-95 text-white cursor-pointer px-3 text-center justify-center items-center py-1 rounded-xl flex space-x-2 flex-row absolute right-0"
              @click="openModal(item.transcription, item.name, 'audio')"
              >
              <span class="text-nowrap">提取</span>
              </div>
            </div>
            </div>
          </div>
        </div>
      </li>
      
      <!-- 音频文件上传记录 -->
      <li
      v-for="(item, index) in fileDataMap.audioFileDataMap" :key="'uploaded-audio-' + index"
      class="p-1 mb-3 items-center justify-center w-full rounded-xl group sm:flex space-x-6  bg-opacity-50 shadow-xl hover:rounded-2xl bg-gradient-to-r from-violet-200 to-pink-200"
      >
      <div class="inline-flex items-center">
        <label
          class="relative flex cursor-pointer items-center rounded-full"
          data-ripple-dark="true"
        >
          <input
            type="checkbox"
            class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-md border border-blue-gray-200 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-pink-500 checked:bg-pink-500 checked:before:bg-pink-500 hover:before:opacity-10"
            :value="item" @change="selectId(item, 'audio')"
          />
          <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-white opacity-0 transition-opacity peer-checked:opacity-100">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-3.5 w-3.5"
              viewBox="0 0 20 20"
              fill="currentColor"
              stroke="currentColor"
              stroke-width="1"
            >
              <path
                fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
        </label>
      </div>
        <div class="sm:w-8/12 pl-0 p-5 relative">
          <button
          class="hover:bg-blue-200 hover:rounded-full absolute -right-6"
          @click="fileDataMap.audioFileDataMap.splice(index, 1)"
          >
              <svg-icon name="关闭"></svg-icon>
          </button>
          <div class="space-y-2">
            <div class="space-y-4">
                    {{ item.fileName }}
            </div>
            <div
            class="space-y-4 bg-gray-50 bg-opacity-80 rounded-lg shadow-inner px-3 py-1"
            :title="item.data"
            draggable="true" @dragstart="dragStart($event, item.data)" @dragend="dragEnd"
            >
              {{ item.data && item.data.length > 30 ? item.data.slice(0, 30) + '...' : item.data }}
            </div>
            <div class="flex items-center space-x-4 justify-between">
            <div class="text-grey-500 flex flex-row space-x-1  my-4 h-9">
              <svg stroke="currentColor" fill="none" stroke-width="0" viewBox="0 0 24 24" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <p class="text-xs">{{ item.time }}</p>
            </div>
            <div class="flex flex-row space-x-1 relative">
              <div
              class="bg-red-200 shadow-lg shadow- hover:shadow-red-300 hover:scale-95 text-white cursor-pointer px-3 py-1 text-center justify-center items-center rounded-xl flex space-x-2 flex-row absolute right-20"
              @click="insertText(item.data)"
              >
              <span class="text-nowrap">插入</span>
              </div>
              <div
              class="bg-emerald-200 shadow-lg shadow- hover:shadow-emerald-300 hover:scale-95 text-white cursor-pointer px-3 text-center justify-center items-center py-1 rounded-xl flex space-x-2 flex-row absolute right-0"
              @click="openModal(item.data, item.fileName, 'audio')"
              >
              <span class="text-nowrap">提取</span>
              </div>
            </div>
            </div>
          </div>
        </div>
      </li>

      <!-- 数据库录音记录 -->
      <li
      v-for="(item, index) in audioData" :key="index"
      class="p-1 mb-3 items-center justify-center w-full rounded-xl group sm:flex space-x-6  bg-opacity-50 shadow-xl hover:rounded-2xl bg-gradient-to-r from-violet-200 to-pink-200"
      >
      <div class="inline-flex items-center">
        <label
          class="relative flex cursor-pointer items-center rounded-full"
          for="checkbox-1"
          data-ripple-dark="true"
        >
          <input
            type="checkbox"
            class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-md border border-blue-gray-200 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-pink-500 checked:bg-pink-500 checked:before:bg-pink-500 hover:before:opacity-10"
            id="checkbox-1"

             :value="item" @change="selectId(item, 'audio')"
          />
          <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-white opacity-0 transition-opacity peer-checked:opacity-100">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-3.5 w-3.5"
              viewBox="0 0 20 20"
              fill="currentColor"
              stroke="currentColor"
              stroke-width="1"
            >
              <path
                fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
        </label>
      </div>
      <!-- <svg-icon name="draggable" class="handle"></svg-icon> -->
        <div class="sm:w-8/12 pl-0 p-5 relative">
                  <button
                  class="hover:bg-blue-200 hover:rounded-full absolute -right-6"
                  @click="deleteItemDataBase(index, 'audio', item)"
                  >
                      <svg-icon name="关闭"></svg-icon>
                  </button>
          <div class="space-y-2">
            <div class="space-y-4">
                    {{ item.name }}
            </div>
            <div
            class="space-y-4 bg-gray-50 bg-opacity-80 rounded-lg shadow-inner px-3 py-1"
            @click="toggleDisplay(index)"
            draggable="true" @dragstart="dragStart($event, item.text)" @dragend="dragEnd"
            >
              <div v-if="item.showExtracted">
                <div v-for="(info, i) in item.extractedData" :key="i">
                  <div v-if="i > 0">
                    {{ info }}: {{ item.answers[i-1] }}
                  </div>
                </div>
              </div>
              <div v-else title=item.transcription
              >
              {{ item.text.length > 30 ? item.text.slice(0, 30) + '...' : item.text }}
              </div>
            </div>
            <div class="flex items-center space-x-4 justify-between">
            <div class="text-grey-500 flex flex-row space-x-1  my-4 h-9">
              <svg stroke="currentColor" fill="none" stroke-width="0" viewBox="0 0 24 24" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <p class="text-xs">{{ item.time }}</p>
            </div>
            <div class="flex flex-row space-x-1 relative">
              <div
              class="bg-red-200 shadow-lg shadow- hover:shadow-red-300 hover:scale-95 text-white cursor-pointer px-3 py-1 text-center justify-center items-center rounded-xl flex space-x-2 flex-row absolute right-20"
              @click="insertText(item.text)"
              >
              <span class="text-nowrap">插入</span>
              </div>
              <div
              class="bg-emerald-200 shadow-lg shadow- hover:shadow-emerald-300 hover:scale-95 text-white cursor-pointer px-3 text-center justify-center items-center py-1 rounded-xl flex space-x-2 flex-row absolute right-0"
              @click="openModal(item.text, item.name, 'audio')"
              >
              <span class="text-nowrap">提取</span>
              </div>
            </div>
            </div>
          </div>
        </div>
      </li>

      <!-- 图片识别记录 -->
      <li
      v-for="(item, index) in fileDataMap.imageFileDataMap" :key="index"
      class="p-1 mb-3 items-center justify-center w-full rounded-xl group sm:flex space-x-6  bg-opacity-50 shadow-xl hover:rounded-2xl bg-gradient-to-tr from-sky-200 to-indigo-400"
      draggable="true" @dragstart="dragStart($event, item.data || item.fileName)" @dragend="dragEnd"
      >
      <div class="inline-flex items-center">
        <label
          class="relative flex cursor-pointer items-center rounded-full"
          for="checkbox-1"
          data-ripple-dark="true"
        >
          <input
            type="checkbox"
            class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-md border border-blue-gray-200 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-pink-500 checked:bg-pink-500 checked:before:bg-pink-500 hover:before:opacity-10"
            id="checkbox-1"

             :value="item" @change="selectId(item, 'image')"
          />
          <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-white opacity-0 transition-opacity peer-checked:opacity-100">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-3.5 w-3.5"
              viewBox="0 0 20 20"
              fill="currentColor"
              stroke="currentColor"
              stroke-width="1"
            >
              <path
                fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
        </label>
      </div>
      <img  class="mx-auto block w-4/12 h-40 rounded-lg"  alt="art cover" loading="lazy" :src='item.base64' />
      <div class="sm:w-8/12 pl-0 p-5 relative">
        <button
          class="hover:bg-blue-200 hover:rounded-full absolute right-0"
          @click="deleteImage(index)"
        >
          <svg-icon name="关闭"></svg-icon>
        </button>
        <div class="space-y-2">
          <div class="space-y-4">
            {{ item.fileName }} <!-- Display the file name -->
          </div>
          <div
           class="space-y-4 bg-gray-300 bg-opacity-80 rounded-lg shadow-inner px-3 py-1"
           :title="item.data"
            draggable="true" @dragstart="dragStart($event, item.transcription)" @dragend="dragEnd"
           >
            {{ item.data.length > 30 ? item.data.slice(0, 30) + '...' : item.data }}
          </div>
          <div class="flex items-center space-x-4 justify-between">
            <div class="text-grey-500 flex flex-row space-x-1  my-4 h-9">
              <svg stroke="currentColor" fill="none" stroke-width="0" viewBox="0 0 24 24" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <p class="text-xs">{{ item.time }} <!-- Display the extraction time --></p>
            </div>
            <div class="flex flex-row space-x-1 relative">
              <div
                class="bg-red-200 shadow-lg shadow- hover:shadow-red-300 hover:scale-95 text-white cursor-pointer px-3 py-1 text-center justify-center items-center rounded-xl flex space-x-2 flex-row absolute right-20"
                @click="insertText(item.data)"
              >
                <span class="text-nowrap">插入</span>
              </div>
              <div
                class="bg-emerald-200 shadow-lg shadow- hover:shadow-emerald-300 hover:scale-95 text-white cursor-pointer px-3 text-center justify-center items-center py-1 rounded-xl flex space-x-2 flex-row absolute right-0"
                @click="openModal(item.data)"
              >
                <span class="text-nowrap">提取</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      </li>
      
      <!-- 数据库图片记录 -->
      <li
      v-for="(item, index) in pictureData" :key="index"
      class="p-1 mb-3 items-center justify-center w-full rounded-xl group sm:flex space-x-6  bg-opacity-50 shadow-xl hover:rounded-2xl bg-gradient-to-tr from-sky-200 to-indigo-400"
      draggable="true" @dragstart="dragStart($event, item.text)" @dragend="dragEnd"
      >
      <div class="inline-flex items-center">
        <label
          class="relative flex cursor-pointer items-center rounded-full"
          for="checkbox-1"
          data-ripple-dark="true"
        >
          <input
            type="checkbox"
            class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-md border border-blue-gray-200 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-pink-500 checked:bg-pink-500 checked:before:bg-pink-500 hover:before:opacity-10"
            id="checkbox-1"

             :value="item" @change="selectId(item, 'image')"
          />
          <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-white opacity-0 transition-opacity peer-checked:opacity-100">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-3.5 w-3.5"
              viewBox="0 0 20 20"
              fill="currentColor"
              stroke="currentColor"
              stroke-width="1"
            >
              <path
                fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
        </label>
      </div>
      <img  class="mx-auto block w-4/12 h-40 rounded-lg"  alt="art cover" loading="lazy" :src="'data:image/png;base64,'+item.file" />
      <div class="sm:w-8/12 pl-0 p-5 relative">
        <button
          class="hover:bg-blue-200 hover:rounded-full absolute right-0"
          @click="deleteItemDataBase(index, 'image', item)"
        >
          <svg-icon name="关闭"></svg-icon>
        </button>
        <div class="space-y-2">
          <div class="space-y-4">
            {{ item.name }} <!-- Display the file name -->
          </div>
          <div
           class="space-y-4 bg-gray-300 bg-opacity-80 rounded-lg shadow-inner px-3 py-1"
           :title="item.text"
            draggable="true" @dragstart="dragStart($event, item.text)" @dragend="dragEnd"
           >
            {{ item.text.length > 30 ? item.text.slice(0, 30) + '...' : item.text }}
          </div>
          <div class="flex items-center space-x-4 justify-between">
            <div class="text-grey-500 flex flex-row space-x-1  my-4 h-9">
              <svg stroke="currentColor" fill="none" stroke-width="0" viewBox="0 0 24 24" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <p class="text-xs">{{ item.time }} <!-- Display the extraction time --></p>
            </div>
            <div class="flex flex-row space-x-1 relative">
              <div
                class="bg-red-200 shadow-lg shadow- hover:shadow-red-300 hover:scale-95 text-white cursor-pointer px-3 py-1 text-center justify-center items-center rounded-xl flex space-x-2 flex-row absolute right-20"
                @click="insertText(item.text)"
              >
                <span class="text-nowrap">插入</span>
              </div>
              <div
                class="bg-emerald-200 shadow-lg shadow- hover:shadow-emerald-300 hover:scale-95 text-white cursor-pointer px-3 text-center justify-center items-center py-1 rounded-xl flex space-x-2 flex-row absolute right-0"
                @click="openModal(item.text)"
              >
                <span class="text-nowrap">提取</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      </li>

      <!-- pdf上传记录 -->
      <li
      v-for="(item, index) in fileDataMap.pdfFileDataMap" :key="index"
      class="p-1 mb-3 items-center justify-center w-full rounded-xl group sm:flex space-x-6  bg-opacity-50 shadow-xl hover:rounded-2xl bg-gradient-to-tr from-red-200 to-red-400"
      draggable="true" @dragstart="dragStart($event, item.data)" @dragend="dragEnd"
      >
      <div class="inline-flex items-center">
        <label
          class="relative flex cursor-pointer items-center rounded-full"
          for="checkbox-1"
          data-ripple-dark="true"
        >
          <input
            type="checkbox"
            class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-md border border-blue-gray-200 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-pink-500 checked:bg-pink-500 checked:before:bg-pink-500 hover:before:opacity-10"
            id="checkbox-1"

             :value="item" @change="selectId(item, 'pdf')"
          />
          <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-white opacity-0 transition-opacity peer-checked:opacity-100">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-3.5 w-3.5"
              viewBox="0 0 20 20"
              fill="currentColor"
              stroke="currentColor"
              stroke-width="1"
            >
              <path
                fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
        </label>
      </div>
      <img  class="mx-auto block w-4/12 h-40 rounded-lg"  alt="art cover" loading="lazy" src='../../assets/images/pdf.png' />
      <div class="sm:w-8/12 pl-0 p-5 relative">
        <button
          class="hover:bg-blue-200 hover:rounded-full absolute right-0"
          @click="deletePdf(index)"
        >
          <svg-icon name="关闭"></svg-icon>
        </button>
        <div class="space-y-2">
          <div class="space-y-4">
            {{ item.fileName }} <!-- Display the file name -->
          </div>
          <div
           class="space-y-4 bg-gray-300 bg-opacity-80 rounded-lg shadow-inner px-3 py-1"
            :title="item.data"
            draggable="true" @dragstart="dragStart($event, item.data || item.fileName)" @dragend="dragEnd"
           >
            {{ item.data ? (item.data.length > 30 ? item.data.slice(0, 30) + '...' : item.data) : '电子文档编号：' + item.id }}
          </div>
          <div class="flex items-center space-x-4 justify-between">
            <div class="text-grey-500 flex flex-row space-x-1  my-4 h-9">
              <svg stroke="currentColor" fill="none" stroke-width="0" viewBox="0 0 24 24" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <p class="text-xs">{{ item.time }} <!-- Display the extraction time --></p>
            </div>
            <div class="flex flex-row space-x-1 relative">
              <div
                class="bg-red-200 shadow-lg shadow- hover:shadow-red-300 hover:scale-95 text-white cursor-pointer px-3 py-1 text-center justify-center items-center rounded-xl flex space-x-2 flex-row absolute right-20"
                @click="insertText(item.data || item.fileName)"
              >
                <span class="text-nowrap">插入</span>
              </div>
              <div
                class="bg-emerald-200 shadow-lg shadow- hover:shadow-emerald-300 hover:scale-95 text-white cursor-pointer px-3 text-center justify-center items-center py-1 rounded-xl flex space-x-2 flex-row absolute right-0"
                @click="openModal(item.data, item.fileName, 'pdf')"
              >
                <span class="text-nowrap">提取</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      </li>

      <!-- 数据库pdf记录 -->
      <li
      v-for="(item, index) in pdfData" :key="index"
      class="p-1 mb-3 items-center justify-center w-full rounded-xl group sm:flex space-x-6  bg-opacity-50 shadow-xl hover:rounded-2xl bg-gradient-to-tr from-red-200 to-red-400"
      draggable="true" @dragstart="dragStart($event, item.text || item.name)" @dragend="dragEnd"
      >
        <div class="inline-flex items-center">
        <label
          class="relative flex cursor-pointer items-center rounded-full"
          for="checkbox-1"
          data-ripple-dark="true"
        >
          <input
            type="checkbox"
            class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-md border border-blue-gray-200 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-pink-500 checked:bg-pink-500 checked:before:bg-pink-500 hover:before:opacity-10"
            id="checkbox-1"

             :value="item" @change="selectId(item, 'pdf')"
          />
          <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-white opacity-0 transition-opacity peer-checked:opacity-100">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-3.5 w-3.5"
              viewBox="0 0 20 20"
              fill="currentColor"
              stroke="currentColor"
              stroke-width="1"
            >
              <path
                fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
        </label>
      </div>
      <img  class="mx-auto block w-4/12 h-40 rounded-lg"  alt="art cover" loading="lazy" src='../../assets/images/pdf.png' />
      <div class="sm:w-8/12 pl-0 p-5 relative">
        <button
          class="hover:bg-blue-200 hover:rounded-full absolute right-0"
          @click="deleteItemDataBase(index, 'pdf', item)"
        >
          <svg-icon name="关闭"></svg-icon>
        </button>
        <div class="space-y-2">
          <div class="space-y-4">
            {{ item.name }} <!-- Display the file name -->
          </div>
          <div
           class="space-y-4 bg-gray-300 bg-opacity-80 rounded-lg shadow-inner px-3 py-1"
            :title="item.text"
            draggable="true" @dragstart="dragStart($event, item.text || item.name)" @dragend="dragEnd"
           >
           {{ item.text ? (item.text.length > 30 ? item.text.slice(0, 30) + '...' : item.text) : '电子文档编号：' + item.id }}
          </div>
          <div class="flex items-center space-x-4 justify-between">
            <div class="text-grey-500 flex flex-row space-x-1  my-4 h-9">
              <svg stroke="currentColor" fill="none" stroke-width="0" viewBox="0 0 24 24" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <p class="text-xs">{{ item.time }} <!-- Display the extraction time --></p>
            </div>
            <div class="flex flex-row space-x-1 relative">
              <div
                class="bg-red-200 shadow-lg shadow- hover:shadow-red-300 hover:scale-95 text-white cursor-pointer px-3 py-1 text-center justify-center items-center rounded-xl flex space-x-2 flex-row absolute right-20"
                @click="insertText(item.text || item.name)"
              >
                <span class="text-nowrap">插入</span>
              </div>
              <div
                class="bg-emerald-200 shadow-lg shadow- hover:shadow-emerald-300 hover:scale-95 text-white cursor-pointer px-3 text-center justify-center items-center py-1 rounded-xl flex space-x-2 flex-row absolute right-0"
                @click="openModal(item.text, item.name, 'pdf')"
              >
                <span class="text-nowrap">提取</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      </li>
    </TransitionGroup>
      </VueDraggable>
    </div>
  </transition>

<!-- 思维导图 -->
<div v-show="(showCreateMindMapButton&&!isMindMapLoading&&isMindMapVisible&&!isFullscreen)" class="absolute left-[40%] top-[50%] z-50" >
  <button 
  class="group relative h-8 w-24 overflow-hidden rounded-2xl bg-orange-500 opacity-100 text-base font-bold text-white"
  @click="emitOpenMindMapModal"
  >
    点击生成
    <div class="absolute inset-0 h-full w-full scale-0 rounded-2xl transition-all duration-300 group-hover:scale-100 group-hover:bg-white/30"></div>
  </button>
</div>
<transition name="slide-fade">
  <!-- 壳子 -->
  <div v-show="isMindMapVisible" class="flex w-full h-full justify-center items-center z-50 transition-all duration-500" :class="{ 'w-3/12': isFullscreen }">
    <div class="absolute " v-show="isMindMapLoading">
      <div class="h-24 w-24 rounded-full border-t-8 border-b-8 border-gray-300"></div>
      <div class="absolute top-0 left-0 h-24 w-24 rounded-full border-t-8 border-b-8 border-blue-500 animate-spin">
      </div>
    </div>
    <div id="jsmind_container" class="w-full h-full" v-show="!isMindMapLoading"></div>
    <!-- <div id="jsmind_container" class="w-full h-[730px]" key="mind"></div> -->
  </div>
</transition>
  </div>
  <!-- 数据可视化 -->
  <div v-show="isFullscreen" class="w-8/12 bg-gray-200 opacity-65 h-5/6 absolute left-[450px] top-[69px] rounded-xl border-[1px] border-solid border-gray-300 shadow-xl">
    <aside class="z-20 flex flex-col float-left rounded-l-xl items-center w-16 h-full py-8 overflow-y-auto bg-white border-r rtl:border-l rtl:border-r-0 dark:bg-gray-900 dark:border-gray-700">
      <nav class="flex flex-col flex-1 space-y-6">
          <div >
              <img class="w-auto h-6 " src="../../../assets/logo2.png" alt="">
          </div>
  
          <div href="#" class="p-1.5 text-gray-700 focus:outline-nones transition-colors duration-200 rounded-lg dark:text-gray-200 dark:hover:bg-gray-800 hover:bg-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
              </svg>
          </div>
  
          <div class="p-1.5 text-gray-700 focus:outline-nones transition-colors duration-200 rounded-lg dark:text-gray-200 dark:hover:bg-gray-800 hover:bg-gray-100">
              <button @click="toggleMenu">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
              </svg>
              </button>
              <div 
              v-show="isMenuVisible" 
              class="absolute left-16 top-32 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50"
              >
                <div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
                  <button class="block text-left w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">柱状图</button>
                  <button class="block text-left w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">折线图</button>
                  <button class="block text-left w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">饼图</button>
                </div>
              </div>
          </div>
          
          <a  class="p-1.5 text-gray-700 focus:outline-nones transition-colors duration-200 rounded-lg dark:text-gray-200 dark:hover:bg-gray-800 hover:bg-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M11.35 3.836c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m8.9-4.414c.376.023.75.05 1.124.08 1.131.094 1.976 1.057 1.976 2.192V16.5A2.25 2.25 0 0118 18.75h-2.25m-7.5-10.5H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V18.75m-7.5-10.5h6.375c.621 0 1.125.504 1.125 1.125v9.375m-8.25-3l1.5 1.5 3-3.75" />
              </svg>
          </a>
  
          <a class="p-1.5 text-gray-700 focus:outline-nones transition-colors duration-200 rounded-lg dark:text-gray-200 dark:hover:bg-gray-800 hover:bg-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v1.5M3 21v-6m0 0l2.77-.693a9 9 0 016.208.682l.108.054a9 9 0 006.086.71l3.114-.732a48.524 48.524 0 01-.005-10.499l-3.11.732a9 9 0 01-6.085-.711l-.108-.054a9 9 0 00-6.208-.682L3 4.5M3 15V4.5" />
              </svg>
          </a>
  
          <a class="p-1.5 text-gray-700 focus:outline-nones transition-colors duration-200 rounded-lg dark:text-gray-200 dark:hover:bg-gray-800 hover:bg-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
              </svg>
          </a>
      </nav>
    </aside>
    <div class="relative pl-20 z-10 h-full">
      <LineChart v-if="chartType === 'line'" :chartData="chartData"/>
      <PieChart v-else-if="chartType === 'pie'" :chart-data="chartData" />
      <BarChart v-else-if="chartType === 'bar'" :chart-data="chartData"/>
    </div>
  </div>






  <transition name="modal-fade">
  <div v-show="isOpen"
        class="fixed inset-0 z-10 overflow-y-auto"
        aria-labelledby="modal-title" role="dialog" aria-modal="true"
  >
        <div class="flex items-end justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <span class="hidden sm:inline-block sm:h-screen sm:align-middle" aria-hidden="true">&#8203;</span>

                <div class="relative inline-block px-4 pt-5 pb-4 overflow-hidden text-left align-bottom transition-all transform bg-white rounded-lg shadow-xl dark:bg-gray-900 sm:my-8 sm:w-full sm:max-w-sm sm:p-6 sm:align-middle">
                    <h3 class="text-lg font-medium leading-6 text-gray-800 capitalize dark:text-white" id="modal-title">
                        提取信息
                    </h3>
                    <p class="mt-2 text-sminvite text-gray-500 dark:text-gray-400">
                        您可以在这里自定义加入需要提取的信息
                    </p>

                    <form class="mt-4" action="#">
                        <label for="emails-list" class="text-sm text-gray-700 dark:text-gray-200">
                            Informations
                        </label>

                        <div v-for="(input, index) in inputs" :key="index" class="relative items-center">
                          <label class="block mt-3" for="email">
                            <input name="Input" v-model.lazy="input.value" @blur="input.touched = true" required placeholder="信息：" class="block w-full px-4 py-3 text-sm text-gray-700 bg-white border border-gray-200 rounded-md focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:focus:border-blue-300" />
                          </label>
                          <p v-if="!input.value && input.touched" class="text-red-500 text-xs ml-4">输入不能为空</p>
                          <button type="button" class="absolute right-0 top-3 text-red-500 align-middle mr-2 hover:bg-blue-200 rounded-full px-1 py-1" @click="removeInput(index)">
                            <svg-icon name="减"></svg-icon>
                          </button>
                        </div>

                        <button
                        type="button"
                        class="mt-2 flex items-center rounded py-1.5 px-2 text-sm text-blue-600 transition-colors duration-300 hover:text-blue-400 focus:outline-none dark:text-blue-400 dark:hover:text-blue-500"
                        @click="addInput"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                            </svg>

                            <span class="mx-2">添加</span>
                        </button>


                        <div class="mt-4 sm:flex sm:items-center sm:-mx-2">
                            <button type="button" @click="isOpen = false" class="w-full px-4 py-2 text-sm font-medium tracking-wide text-gray-700 capitalize transition-colors duration-300 transform border border-gray-200 rounded-md sm:w-1/2 sm:mx-2 dark:text-gray-200 dark:border-gray-700 dark:hover:bg-gray-800 hover:bg-gray-100 focus:outline-none focus:ring focus:ring-gray-300 focus:ring-opacity-40">
                                取消
                            </button>
                            <button type="button" @click="submitData" :class="{'animate-pulse': isLoading}" class="w-full px-4 py-2 mt-3 text-sm font-medium tracking-wide text-white capitalize transition-colors duration-300 transform bg-blue-600 rounded-md sm:mt-0 sm:w-1/2 sm:mx-2 hover:bg-blue-500 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40">
                            <span v-if="isLoading" class="flex items-center justify-center">
                              <div style="border-top-color:transparent" class="w-4 h-4 border-4 border-blue-200 rounded-full animate-spin"></div>
                              <p class="ml-2">loading...</p>
                            </span>
                            <span v-else>
                              提取
                            </span>
                            </button>
                        </div>
                    </form>
                </div>
        </div>
    </div>
  </transition>
  <Transition name="modal-fade">
    <div v-show="isOpenChartsDialog"
        class="charts-center-modal"
        aria-labelledby="modal-title" role="dialog" aria-modal="true"
    >
    <div class="flex items-end justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <span class="hidden sm:inline-block sm:h-screen sm:align-middle" aria-hidden="true">&#8203;</span>

          <div class=" relative inline-block px-1 pt-5 pb-4 overflow-hidden text-center align-bottom transition-all transform bg-white rounded-lg shadow-xl dark:bg-gray-900 sm:my-8 sm:w-full sm:max-w-sm sm:p-6 sm:align-middle">
            <div class="space-y-3" v-if="!isCreating">
              <button 
              class="btn overflow-hidden relative w-64 bg-blue-500 text-white py-4 px-4 rounded-xl font-bold uppercase -- before:block before:absolute before:h-full before:w-full before:bg-red-300 before:left-0 before:top-0 before:-translate-y-full hover:before:translate-y-0 before:transition-transform"
              @click="createCharts('bar')"
              >
                <span class="relative">柱状图</span>
              </button>
              <button 
              class="btn overflow-hidden relative w-64 bg-blue-500 text-white py-4 px-4 rounded-xl font-bold uppercase -- before:block before:absolute before:h-full before:w-1/2 before:rounded-full before:bg-orange-400 before:top-0 before:left-1/4 before:transition-transform before:opacity-0 before:hover:opacity-100 hover:text-orange-200 hover:before:animate-ping transition-all duration-300"
              @click="createCharts('line')"
              >
                <span class="relative">折线图</span>
              </button>
              <button 
              class="btn-default overflow-hidden relative w-64 bg-stone-50 text-gray-900 py-4 px-4 rounded-xl font-bold uppercase transition-all duration-100 -- hover:shadow-md border border-stone-100 hover:bg-gradient-to-t hover:from-stone-100 before:to-stone-50 hover:-translate-y-[3px]"
              @click="createCharts('pie')"
              >
                <span class="relative">饼图</span>
              </button>
            </div>
            <div class="flex justify-center items-center" v-else>
              <div class="rounded-full h-20 w-20 bg-violet-600 animate-ping"></div>
            </div>
          </div>
  </div>
    </div>
  </Transition>
  


  </template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { type UseDraggableReturn, VueDraggable } from 'vue-draggable-plus';
import {  Menu, MenuButton, MenuItem, MenuItems, TransitionRoot, TransitionChild, Dialog, DialogPanel, DialogTitle } from "@headlessui/vue";
import mindmap from 'vue3-mindmap';
import 'vue3-mindmap/dist/style.css';
import axios from 'axios';
import { ConstructionOutlined } from '@vicons/material';
import { selectDictLabel } from '@/utils/basis';
import { FullScreen } from '@icon-park/vue-next';
import BarChart from './bar.vue';
import LineChart from './line.vue';
import PieChart from './pie.vue'
interface Transcription {
  transcription: string; // The transcription text
  showExtracted: boolean; // A flag to show if the extracted data is shown
  extractedData: string[]; // The extracted data from the transcription
  answers: string[]; // The answers from the backend after processing the extracted data
  name: string; // The name of the transcription
  currentTime: string; // The current time of the transcription
  // Other possible properties...
}

interface FileDataMap {
  imageFileDataMap: any[];
  audioFileDataMap: any[];
  videoFileDataMap: any[];
  pdfFileDataMap: any[];
}
export default defineComponent({
  components: {
    VueDraggable,
    mindmap,
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
    BarChart,
    LineChart,
    PieChart
  },
  props: {
    editor: {
      type: Object as () => any,
      required: true,
    },
    transcriptions: {
      type: Array as () => Transcription[],
      required: true,
    },
    fileDataMap: {
      type: Object as () => FileDataMap,
      required: true,
    },
    document: {
      type: Object,
      required: true
    },
    isMindMapLoading: Boolean,
    isOpenChartsDialog: Boolean,
    mindMap: String,
    selectedTextCC: String,
    isFullscreen: Boolean
  },
  data() {
    return {
      inputs: [] as Array<{ value: string; touched: boolean }>,
      // other data properties...
      mindmapdata: "",
      isMindMapMode: false,
      selected: false,
      jm: null,
      mind:{},
      isMindMapVisible: true,
      ifNoMindMap: true,
      showCreateMindMapButton: true,
      audioData: [],
      pictureData: [],
      pdfData: [],
      selectedIdList: [],
      isMenuVisible: false,
      chartType: '',
      
    };
  },
  methods: {

    toggleMenu() {
      this.isMenuVisible = !this.isMenuVisible;
    },
    base64ImgtoFile(dataurl, filename = 'file') {
      let arr = dataurl.split(',')
      let mime = arr[0].match(/:(.*?);/)[1]
      let suffix = mime.split('/')[1]
      let bstr = atob(arr[1])
      let n = bstr.length
      let u8arr = new Uint8Array(n)
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n)
      }
      return new File([u8arr], `${filename}.${suffix}`, {
        type: mime
      })
    },

    async  postData(formData: FormData) {
        // 使用 axios 发送 POST 请求
        const response = await axios.post('/update_kstar', formData, {
          headers: {
          'Content-Type': 'multipart/form-data',
        },
        });

        // 返回响应的数据
        return response.data;
      },

    async selectId(item, type: string) {
      const index = this.selectedIdList.indexOf(item.id);
      if (index !== -1) {
        // id已经存在于selectedIdList中，删除它
        this.selectedIdList.splice(index, 1);
        console.log('取消');
      } else {
        // id不存在于selectedIdList中，添加它
        this.selectedIdList.push(item.id);

        // 创建一个 FormData 对象并添加 id 和 type
        const formData = new FormData();
        formData.append('id', item.id);
        formData.append('type', type);

        // 发送 POST 请求
        try {
          const result = await this.postData(formData);
          console.log(result);
        } catch (error) {
          console.error('Error:', error);
        }
      }
      console.log(this.selectedIdList);
    },

    async deleteItemDataBase(index, type, item) {
      const username = localStorage.getItem("userName") || "unknown_user";
      const file_name = this.document.title;
      let url = '';
      const formData = new FormData();
      switch (type) {
        case 'audio':
          url = '/audio_delete';
          formData.append('username', username);
          formData.append('file_name', file_name);
          formData.append('name', item.name);
          break;
        case 'image':
          url = '/ocr_delete';
          formData.append('username', username);
          formData.append('file_name', file_name);
          formData.append('name', item.name);
          break;
        case 'pdf':
          url = '/pdf_delete';
          formData.append('username', username);
          formData.append('file_name', item.name);
          break;
        default:
          console.error('Unknown type: ', type);
          return;
      }

      try {
        await axios.post(url, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        switch (type) {
          case 'audio':
            this.audioData.splice(index, 1);
            break;
          case 'image':
            this.pictureData.splice(index, 1);
            break;
          case 'pdf':
            this.pdfData.splice(index, 1);
            break;
        }
      } catch (error) {
        console.error('Delete failed:', error);
      }
    },

    emitOpenMindMapModal() {
      this.$emit('open-mindmap-modal', this.ifNoMindMap);
      this.ifNoMindMap = !this.ifNoMindMap;
    },
    toggleDisplay(selected: boolean) {
      this.selected = !this.selected;
      this.isMindMapMode = selected;
    },
        // 定义mindjs
    loadJsMind() {
      var options = {
          container:'jsmind_container',
          editable:true,
          theme:'orange',
          view: {
            hmargin:100,        // 思维导图距容器外框的最小水平距离
            vmargin:50,         // 思维导图距容器外框的最小垂直距离
            draggable: true,   // 当容器不能完全容纳思维导图时，是否允许拖动画布代替鼠标滚动
            hide_scrollbars_when_draggable: true, // 当设置 draggable = true 时，是否隐藏滚动条
          }
      };

      this.jm = new jsMind(options);
      // 让 jm 显示这个 mind 即可
      console.log(typeof this.mind);
      console.log(this.mind);
      this.jm.show(this.mind);
      this.jm.shoot();
    },
    // ...
    
  },
  watch: {
    mindMap(newVal) {
      if(newVal){
      this.mind = JSON.parse(newVal);
      console.log(typeof this.mind);
      console.log("newMind", this.mind);
      var options = {
          container:'jsmind_container',
          editable:true,
          theme:'orange',
          view: {
            draggable: true,   // 当容器不能完全容纳思维导图时，是否允许拖动画布代替鼠标滚动
            hide_scrollbars_when_draggable: true, // 当设置 draggable = true 时，是否隐藏滚动条
          }
      };
      if (this.jm) {
        this.ifNoMindMap = false;
        this.jm.show(this.mind);
        this.showCreateMindMapButton = false;
      }
      }

    }
  },
  async mounted() {
    let script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://unpkg.com/jsmind@0.8.5/es6/jsmind.js';
    document.body.appendChild(script);

    let script2 = document.createElement('script');
    script2.type = 'text/javascript';
    script2.src = 'https://unpkg.com/jsmind@0.8.5/es6/jsmind.draggable-node.js';
    document.body.appendChild(script2);

    let script3 = document.createElement('script');
    script3.type = 'text/javascript';
    script3.src = 'https://unpkg.com/dom-to-image@2.6.0/dist/dom-to-image.min.js';
    document.body.appendChild(script3);

    let script4 = document.createElement('script');
    script4.type = 'text/javascript';
    script4.src = 'https://unpkg.com/jsmind@0.8.5/es6/jsmind.screenshot.js';
    script.onload = this.loadJsMind; // 当 jsMind 库加载完成后，调用 loadJsMind 方法
    document.body.appendChild(script4);

    // 获取数据库中的卡片
    const username = localStorage.getItem("userName") || "unknown_user"; // 替换为实际的用户名
    const file_name = this.document.title; // 替换为实际的文件名
    console.log('username', username, "file_name", file_name);
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('file_name', file_name);
    try {
      const response = await axios.get("/get_datas", {
        params: params,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      const responseData = response && response.data && response.data.hwdata !== undefined ? response.data.hwdata : response;
      const payload = responseData || { audio: [], picture: [], pdf: [] };
      console.log(payload);

      (payload.audio || []).forEach(item => {
        this.audioData.push(item);
      });

      (payload.picture || []).forEach(item => {
        this.pictureData.push(item);
      });

      (payload.pdf || []).forEach(item => {
        this.pdfData.push(item);
      });

    } catch (error) {
      console.error("API request failed: ", error);
    }
  },
  setup(props, { emit }) {
    const chartOptions = {
      xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          data: [150, 230, 224, 218, 135, 147, 260],
          type: 'line'
        }
      ]
    };
    const isCreating = ref(false);
    const isOpen = ref(false);
    const isLoading = ref(false);
    const inputs = ref([{}]);
    const selectedTranscription = ref<{ transcription: string; fileName?: string; fileType?: string } | null>(null);
    const data = [{
      "name":"如何学习D3",
      "children": [
        {
          "name":"预备知识",
          "children": [
            { "name":"HTML & CSS" },
            { "name":"JavaScript" },
          ]
        },
        {
          "name":"安装",
          "collapse": true,
          "children": [ { "name": "折叠节点" } ]
        },
        { "name":"进阶", "left": true },
      ]
    }]
    const chartType = ref('');
    const chartData = ref(null);

    // 创建图表
    async function createCharts(type: string) {
      isCreating.value = true;
      console.log(props.selectedTextCC);
      // 创建一个 FormData 对象并添加 user_input 和 type
      const formData = new FormData();
      formData.append('user_input', props.selectedTextCC);
      formData.append('type', type);

      // 发送 POST 请求
      try {
        const response = await axios.post('/visual_data', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log(response);

        chartData.value = JSON.parse(response);
        console.log(chartData.value); // 假设服务器返回的数据在 response.data 中
        chartType.value = type;

        } catch (error) {
          console.error('Error:', error);
        } finally {
          isCreating.value = false;
          emit('close-chartsdialog'); // 向父组件发送事件
          emit('open-success');
        }
      };
    const onUpdate = () => {
      console.log('update');
    };

    const deleteItem = (index: number) => {
      props.transcriptions.splice(index, 1);
    };

    const deleteImage = (index: number) => {
      props.fileDataMap.imageFileDataMap.splice(index, 1);
    };

    const deletePdf = async (index: number) => {
    const pdfData = props.fileDataMap.pdfFileDataMap[index];
    const username = localStorage.getItem("userName") || "unknown_user";
    const file_name = pdfData.fileName;

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/pdf_delete', {
        username: username,
        file_name: file_name
      });
      console.log(response);
        props.fileDataMap.pdfFileDataMap.splice(index, 1);

    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error(error.message);
      } else {
        console.error('Unknown error', error);
      }
    }
  };

    const insertText = (text: string) => {
      if (props.editor) {
        props.editor.chain().focus().insertContent(text).run();
      }
    };

    const addInput = () => {
      inputs.value.push({});
    };

    const removeInput = (index: number) => {
      inputs.value.splice(index, 1);
    };

    const openModal = (transcription: string, fileName?: string, fileType?: string) => {
      selectedTranscription.value = { transcription, fileName, fileType };
      console.log(selectedTranscription.value);
      isOpen.value = true;
    };

    const toggleDisplay = (index: number) => {
      props.transcriptions[index].showExtracted = !props.transcriptions[index].showExtracted;
    };

    // 传递要提取的信息
    const submitData = async () => {
      isLoading.value = true;
      // Check if all input boxes are not empty
      for (let input of inputs.value) {
        if (!(input as Input).value) {
          alert('All input boxes cannot be empty!');
          return;
        }
      }

      const inputData = inputs.value.map((input: Input) => input.value);
      // Add the selectedTranscription to the inputData
      inputData.unshift(selectedTranscription.value.transcription);

      try {
        let response;
        if (selectedTranscription.value.fileType === 'pdf') {
          const username = localStorage.getItem("userName") || "unknown_user";
          const file_name = selectedTranscription.value.fileName;
          response = await axios.post('http://127.0.0.1:5000/api/pdf_modifyIE',
            {
              username: username,
              file_name: file_name,
              extracted_info: inputData
            },
            {
              headers: {
                'Content-Type': 'application/json',
              },
            }
          );
        } else {
          response = await axios.post('http://127.0.0.1:5000/api/modifyIE',
            inputData,
            {
              headers: {
                'Content-Type': 'application/json',
              },
            }
          );
        }
        console.log(inputData);
        console.log(response);
        const processedText = response; // Assuming this is the returned field from the backend
        console.log(selectedTranscription.value.transcription);
        // Store the extracted data
        props.transcriptions.forEach((item, index) => {
          if (item.transcription === selectedTranscription.value.transcription) {
            inputData.splice(0,1);
            console.log(inputData);
            props.transcriptions[index].extractedData = inputData;
            
            props.transcriptions[index].answers = processedText;
          }
        });
      } catch (error) {
        if (error instanceof Error) {
          console.error(error.message);

        } else {
          console.error('Unknown error', error);
        }
      } finally {
          isLoading.value = false;
          isOpen.value = false;
          emit('open-success');
        }
    };


    // 拖拽文字
    const dragStart = (event: DragEvent, transcription: string) => {
      event.dataTransfer?.setData('text/plain', transcription);
    };

    const dragEnd = () => {
      // handle drag end event
    };

    const drop = (event: DragEvent) => {

      const text = event.dataTransfer?.getData('text/plain');
      console.log(text);

      if (props.editor) {
        props.editor.chain().focus().insertContent(text).run();
      }
    };

    return {
      isOpen,
      isLoading,
      inputs,
      selectedTranscription,
      onUpdate,
      deleteItem,
      deleteImage,
      deletePdf,
      insertText,
      addInput,
      removeInput,
      openModal,
      toggleDisplay,
      submitData,
      dragStart,
      dragEnd,
      drop,
      data,
      chartOptions,
      createCharts,
      isCreating,
      chartType,
      chartData,
    };
  },
});
  </script>
<style scoped>
.charts-center-modal {
  position: fixed;
  inset: 0;
  z-index: 80;
  overflow-y: auto;
  background: rgba(15, 23, 42, 0.12);
  backdrop-filter: blur(6px);
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
.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}
.fade-move,
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scaleY(0.01) translate(30px, 0);
}

.fade-leave-active {
  position: absolute;
}
.move-right {
  transform: translateX(100%);
  transition: transform 0.3s ease-in-out;
}

.move-left {
  transform: translateX(-100%);
  transition: transform 0.3s ease-in-out;
}
.slide-fade-enter-active {
  transition: all 0.3s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter, .slide-fade-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

</style>
