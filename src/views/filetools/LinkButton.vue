<!--  -->
<template>
  <!-- <Recorder ref="record"></Recorder> -->
  <Menu as="div" class="ai-links-menu">
    <div>
      <MenuButton class="ai-links-trigger btn-s btn-2">
        <svg-icon name="link-ai" class="mr-2"></svg-icon>
        Ai-Links
      </MenuButton>
    </div>

    <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
      <MenuItems class="ai-links-dropdown">
        <div class="ai-links-grid">
          <MenuItem v-slot="{ active }">
            <button type="button" :class="['ai-links-card', { 'is-active': active }]" @click="openModalAndSetAcceptedFileTypes('image/png,image/jpeg,image/jpg')">
              <svg-icon name="图片识别" class="ai-links-icon"></svg-icon>
              <span>图片识别</span>
            </button>
          </MenuItem>
          <MenuItem v-slot="{ active }">
            <button type="button" :class="['ai-links-card', { 'is-active': active }]" @click="openMindMapDiolog">
              <svg-icon name="m-思维导图" class="ai-links-icon"></svg-icon>
              <span>思维导图</span>
            </button>
          </MenuItem>
          <MenuItem v-slot="{ active }">
            <button type="button" :class="['ai-links-card', { 'is-active': active }]" @click="$emit('open-chartsdialog')">
              <svg-icon name="数据可视化1" class="ai-links-icon"></svg-icon>
              <span>生成图表</span>
            </button>
          </MenuItem>
          <MenuItem v-slot="{ active }">
            <button type="button" :class="['ai-links-card', { 'is-active': active }]" @click="openModalAndSetAcceptedFileTypes('.pdf')">
              <svg-icon name="pdf" class="ai-links-icon"></svg-icon>
              <span>PDF</span>
            </button>
          </MenuItem>
        </div>

        <div class="ai-links-footer">
          <MenuItem v-slot="{ active }">
            <button type="button" :class="['ai-links-action', { 'is-active': active }]" @click="setimage()">
              <svg-icon name="图片" class="ai-links-icon small"></svg-icon>
              <span>图片</span>
            </button>
          </MenuItem>
          <MenuItem v-slot="{ active }">
            <button type="button" :class="['ai-links-action', { 'is-active': active }]" @click="showRecorder()">
              <svg-icon name="录音" class="ai-links-icon small"></svg-icon>
              <span>录音</span>
            </button>
          </MenuItem>
          <MenuItem v-slot="{ active }">
            <button type="button" :class="['ai-links-action', { 'is-active': active }]" @click="openModalAndSetAcceptedFileTypes('audio/*,.mp3,.wav,.m4a,.ogg,.webm')">
              <svg-icon name="声音-音乐" class="ai-links-icon small"></svg-icon>
              <span>音频文件</span>
            </button>
          </MenuItem>
          <MenuItem v-slot="{ active }">
            <button type="button" :class="['ai-links-action', { 'is-active': active }]" @click="openModalAndSetAcceptedFileTypes('video/*')">
              <svg-icon name="视频" class="ai-links-icon small"></svg-icon>
              <span>视频文件</span>
            </button>
          </MenuItem>
        </div>
      </MenuItems>
    </transition>
  </Menu>
  <Teleport to="body">
  <transition name="modal-fade">
      <div v-show="isOpen"
        class="center-modal-overlay"
        aria-labelledby="modal-title" role="dialog" aria-modal="true"
        @click.self="closeModal"

      >
      <div class=" mx-auto w-full max-w-[550px] bg-white relative">
        <button @click="closeModal" class="absolute right-0 top-0 m-2">
          <svg-icon name="关闭 (1)"></svg-icon>
        </button>
          <form
          class="py-6 px-9 shadow-lg border-2 border-solid border-gray-200 rounded-lg"
          @submit.prevent="submitFiles"
          >

          <div class="mb-8">
          <input type="file" name="file" id="file" class="sr-only" multiple @change="handleFiles" :accept="acceptedFileTypes" />
          <label
          for="file"
          class="relative flex min-h-[200px] items-center justify-center rounded-md border border-dashed border-[#e0e0e0] p-12 text-center"
          >
          <div
            @dragover.prevent
            @drop="handleDrop"
          >
          <span class="mb-2 block text-xl font-semibold text-[#07074D]">
          拖拽文件到这里
          </span>
          <span class="mb-2 block text-base font-medium text-[#6B7280]">
          或者
          </span>
          <span
          class="inline-flex rounded border border-[#e0e0e0] py-2 px-7 text-base font-medium text-[#07074D]"
          >
          浏览
          </span>
          </div>
          </label>
          </div>

          <div v-for="file in files" :key="file.file.name" class="mb-5 rounded-md bg-[#F5F7FB] py-4 px-8">
              <div class="flex items-center justify-between">
                  <span class="truncate pr-3 text-base font-medium text-[#07074D]">
                  {{ file.file.name }}
                  </span>

                  <button type="button" class="text-[#07074D]" @click="deleteFile(file)">
                    <svg
                      width="10"
                      height="10"
                      viewBox="0 0 10 10"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        fill-rule="evenodd"
                        clip-rule="evenodd"
                        d="M0.279337 0.279338C0.651787 -0.0931121 1.25565 -0.0931121 1.6281 0.279338L9.72066 8.3719C10.0931 8.74435 10.0931 9.34821 9.72066 9.72066C9.34821 10.0931 8.74435 10.0931 8.3719 9.72066L0.279337 1.6281C-0.0931125 1.25565 -0.0931125 0.651788 0.279337 0.279338Z"
                        fill="currentColor"
                      />
                      <path
                        fill-rule="evenodd"
                        clip-rule="evenodd"
                        d="M0.279337 9.72066C-0.0931125 9.34821 -0.0931125 8.74435 0.279337 8.3719L8.3719 0.279338C8.74435 -0.0931127 9.34821 -0.0931123 9.72066 0.279338C10.0931 0.651787 10.0931 1.25565 9.72066 1.6281L1.6281 9.72066C1.25565 10.0931 0.651787 10.0931 0.279337 9.72066Z"
                        fill="currentColor"
                      />
                    </svg>
                  </button>
              </div>
              <div class="relative mt-5 h-[6px] w-full rounded-lg bg-[#dad9e6]">
                <div
                :style="{ width: `${file.progress}%` }"
                class="absolute left-0 right-0 h-full rounded-lg bg-[#6A64F1]"
                ></div>
                </div>
          </div>

          <div>
              <button
              class="hover:shadow-form w-full rounded-md bg-[#6A64F1] py-3 px-8 text-center text-base font-semibold text-white outline-none"
              :class="{'animate-pulse': isLoading}"
              >
              <span v-if="isLoading" class="flex justify-center items-center">
                <svg width="20" height="20" fill="currentColor" class="mr-2 animate-spin" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                  <path d="M526 1394q0 53-37.5 90.5t-90.5 37.5q-52 0-90-38t-38-90q0-53 37.5-90.5t90.5-37.5 90.5 37.5 37.5 90.5zm498 206q0 53-37.5 90.5t-90.5 37.5-90.5-37.5-37.5-90.5 37.5-90.5 90.5-37.5 90.5 37.5 37.5 90.5zm-704-704q0 53-37.5 90.5t-90.5 37.5-90.5-37.5-37.5-90.5 37.5-90.5 90.5-37.5 90.5 37.5 37.5 90.5zm1202 498q0 52-38 90t-90 38q-53 0-90.5-37.5t-37.5-90.5 37.5-90.5 90.5-37.5 90.5 37.5 37.5 90.5zm-964-996q0 66-47 113t-113 47-113-47-47-113 47-113 113-47 113 47 47 113zm1170 498q0 53-37.5 90.5t-90.5 37.5-90.5-37.5-37.5-90.5 37.5-90.5 90.5-37.5 90.5 37.5 37.5 90.5zm-640-704q0 80-56 136t-136 56-136-56-56-136 56-136 136-56 136 56 56 136zm530 206q0 93-66 158.5t-158 65.5q-93 0-158.5-65.5t-65.5-158.5q0-92 65.5-158t158.5-66q92 0 158 66t66 158z">
                  </path>
                </svg>
                loading
              </span>
              <span v-else>
                提交文件
              </span>
              </button>
          </div>
          </form>
      </div>
    </div>
  </transition>

  <!-- 思维导图模态框 -->
  <transition name="modal-fade">
    <div v-show="isMindMapDiologOpen"
      class="center-modal-overlay"
      aria-labelledby="modal-title" role="dialog" aria-modal="true"
      @click.self="closeMindMapDiolog"

    >
    <div class=" mx-auto w-full max-w-[550px] bg-white relative">
      <button @click="closeMindMapDiolog" class="absolute right-0 top-0 m-2">
        <svg-icon name="关闭 (1)"></svg-icon>
      </button>
        <div
        class="py-6 px-9 shadow-lg border-2 border-solid border-gray-200 rounded-lg"
        >

        <div class="mb-8">
        <input type="file" name="file" id="file" class="sr-only" multiple @change="handleFiles" :accept="acceptedFileTypes" />
        <label
        for="file"
        class="relative  min-h-[200px] items-center justify-center rounded-md p-12 text-center"
        >
        <!-- 输入描述框 -->
        <label for="Description" class="block text-base text-gray-500 dark:text-gray-300">描述</label>

        <textarea
        placeholder="例：生成一份有关计算机学习路线的思维导图"
        class="block  mt-2 w-full placeholder-gray-400/70 dark:placeholder-gray-500 rounded-lg border border-gray-200 bg-white px-4 h-32 py-2.5 text-gray-700 focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:focus:border-blue-300"
        v-model="description"
        ></textarea>

        <p v-if="isLoading" class="mt-3 text-xs text-gray-400 dark:text-gray-600">大模型正在为您加速生成中，请耐心等待~</p>
        </label>
        </div>

        <div>
            <button
            class="hover:shadow-form w-full rounded-md bg-[#6A64F1] py-3 px-8 text-center text-base font-semibold text-white outline-none"
            @click="generateMindMap"
            :class="{'animate-pulse': isLoading}"
            >
            <span v-if="isLoading" class="flex justify-center items-center">
              <svg width="20" height="20" fill="currentColor" class="mr-2 animate-spin" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                <path d="M526 1394q0 53-37.5 90.5t-90.5 37.5q-52 0-90-38t-38-90q0-53 37.5-90.5t90.5-37.5 90.5 37.5 37.5 90.5zm498 206q0 53-37.5 90.5t-90.5 37.5-90.5-37.5-37.5-90.5 37.5-90.5 90.5-37.5 90.5 37.5 37.5 90.5zm-704-704q0 53-37.5 90.5t-90.5 37.5-90.5-37.5-37.5-90.5 37.5-90.5 90.5-37.5 90.5 37.5 37.5 90.5zm1202 498q0 52-38 90t-90 38q-53 0-90.5-37.5t-37.5-90.5 37.5-90.5 90.5-37.5 90.5 37.5 37.5 90.5zm-964-996q0 66-47 113t-113 47-113-47-47-113 47-113 113-47 113 47 47 113zm1170 498q0 53-37.5 90.5t-90.5 37.5-90.5-37.5-37.5-90.5 37.5-90.5 90.5-37.5 90.5 37.5 37.5 90.5zm-640-704q0 80-56 136t-136 56-136-56-56-136 56-136 136-56 136 56 56 136zm530 206q0 93-66 158.5t-158 65.5q-93 0-158.5-65.5t-65.5-158.5q0-92 65.5-158t158.5-66q92 0 158 66t66 158z">
                </path>
              </svg>
              loading
            </span>
            <span v-else>
              生成思维导图
            </span>
            </button>
        </div>
        </div>
    </div>
  </div>
</transition>
  </Teleport>
</template>

<script>
import { Editor } from "@tiptap/vue-3";
import Recorder from "js-audio-recorder";
import axios from "axios";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
export default {
	
//import引入的组件需要注入到对象中才能使用
components: {
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  Recorder
},
props: {
  editor: {
      type: Editor,
      required: true
    },
    document: {
      type: Object,
      required: true
    },
    ifNoMindMap: Boolean,
}, // 接收 editor prop
data() {
//这里存放数据
return {
  isOpen: false,
  files: [],
  acceptedFileTypes: '',
  imageFileDataMap: [],
  videoFileDataMap: [],
  audioFileDataMap: [],
  pdfFileDataMap: [],
  isMindMapDiologOpen: false,
  isChartsDiologOpen: false,
  isLoading: false,
  description: '', // 新增一个数据属性来存储 textarea 中的内容
};
},

//监听属性 类似于data概念
computed: {},
//监控data中的数据变化
watch: {
  ifNoMindMap(newVal) {
    console.log(newVal);
    this.openMindMapDiolog();
    // if(newVal){
    //   this.openMindMapDiolog();
    //   console.log(this.ifNoMindMap);
    // };
  },
},
//方法集合
methods: {
   fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
      reader.readAsDataURL(file);
    });
  },
  openChartsDiolog() {
    this.isChartsDiologOpen = true;
  },
  closeChartsDiolog() {
    this.isChartsDiologOpen = false;
  },
  openMindMapDiolog() {
    this.isMindMapDiologOpen = true;
  },
  closeMindMapDiolog(){
    this.isMindMapDiologOpen = false;
  },
  // 上传思维导图描述
  async generateMindMap() {
    let response; // 将response的声明移动到这里
    this.isLoading = true;
    console.log('isLoading', this.isLoading);
    this.$emit('create-mindmap', this.isLoading, response);
    try {
        response = await axios.post('http://127.0.0.1:5000/api/mindmap', {
            user_input: this.description,
        });
        // 处理返回的数据...
        console.log(response);
    } catch (error) {
        console.error(error);
        // 添加错误处理逻辑
    } finally {
        this.isLoading = false;
        // this.closeMindMapDiolog(); // 如果是一个方法，确保调用它
        if (response) { // 检查response是否存在
            this.$emit('create-mindmap', this.isLoading, response);
        }
    }
  },
  showRecorder() {
    console.log("发送录音事件");
    this.$emit('record-button-clicked');
  },
  async setimage(){
      // 设置文件选择器的选项
      const pickerOpts = {
      types: [
          {
          description: "Images",
          accept: {
              "image/*": [".png", ".gif", ".jpeg", ".jpg"]
          }
          }
      ],
      excludeAcceptAllOption: true,
      multiple: false
      };
      // 打开文件选择器并获取用户选择的文件
      const [fileHandle] = await window.showOpenFilePicker(pickerOpts);
      // 读取文件内容
      const file = await fileHandle.getFile();
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
      // 使用 tiptap 的 setImage 方法来插入图片
          this.editor.commands.setImage({ src: reader.result });
      };
  },
  handleFiles(event) {
    const selectedFiles = event.target.files;
    for (let i = 0; i < selectedFiles.length; i++) {
      const file = selectedFiles[i];
      this.files.push({
        file: file,
        progress: 0 // Initial progress is 0
      });
    }
  },

  normalizeHwData(response) {
    return response && response.data && response.data.hwdata !== undefined ? response.data.hwdata : response;
  },

  resolveReturnedId(data) {
    if (Array.isArray(data)) {
      return data[0];
    }
    if (data && Array.isArray(data.Id)) {
      return data.Id[0];
    }
    return data && (data.id || data.Id);
  },

  // 上传图片/PDF/音频
  async uploadFile(file, index) {
    const base64 = await this.fileToBase64(file.file);
    console.log(file);
    const formData = new FormData();
    formData.append('file', file.file);
    const username = localStorage.getItem("userName") || "unknown_user";
    const file_name = this.document.title; // 从 props 获取当前文档名称
    const time = new Date();
    let endpoint = '';
    const isPdf = this.acceptedFileTypes === '.pdf' || file.file.type === 'application/pdf';
    const isAudio = file.file.type.startsWith('audio/') || this.acceptedFileTypes.startsWith('audio');
    if (isPdf) {
      console.log("上传pdf");
      endpoint = 'http://127.0.0.1:5000/api/pdf_upload';
      formData.append('username', username); // Replace with the actual username
      formData.append('file_name', file.file.name);
      formData.append('time', time);
    } else if (isAudio) {
      console.log("上传音频");
      endpoint = 'http://127.0.0.1:5000/api/audioIE';
      formData.append('username', username);
      formData.append('file_name', file_name);
      formData.append('filename', file.file.name);
      formData.append('time', time);
    } else {
      endpoint = 'http://127.0.0.1:5000/api/ocr';
      formData.append('username', username); // Replace with the actual username
      formData.append('file_name', file_name);
      formData.append('time', time);
    }
    try {
      const response = await axios.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          this.files[index].progress = (progressEvent.loaded / progressEvent.total) * 100;
        },
        timeout: 600000,
      });
      const responseData = this.normalizeHwData(response);
      if (responseData === 'false') {
        throw new Error(`文件 "${file.file.name}" 已存在`);
      }
      if (isPdf) {
        return { fileName: file.file.name, id: this.resolveReturnedId(responseData), data: responseData?.text || '', fileType: file.file.type, time: new Date() };
      }
      if (isAudio) {
        return { fileName: file.file.name, id: this.resolveReturnedId(responseData), data: responseData?.ie_result || '', fileType: file.file.type, time: new Date() };
      }

      console.log(responseData);
      return { fileName: file.file.name, base64: base64, data: responseData.text, Id: this.resolveReturnedId(responseData), fileType: file.file.type, time: new Date() };
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error(error.message);
      } else {
        console.error('Unknown error', error);
      }
      throw error;
    }
  },

  async submitFiles() {
    this.isLoading = true;
    const uploadedFileNames = new Set(); // Create a Set to store uploaded file names

    for (let i = 0; i < this.files.length; i++) {
      const fileName = this.files[i].file.name;

      // Check if the file name already exists
      if (uploadedFileNames.has(fileName)) {
        console.error(`File "${fileName}" has already been uploaded.`);
        continue; // Skip this file
      }
      uploadedFileNames.add(fileName);
      console.log("上传文件" + i);
      try {
        const fileData = await this.uploadFile(this.files[i], i);
        if (!fileData) {
          continue;
        }

        // Store the file name and its corresponding response data in the corresponding map based on the file type
        if (fileData.fileType.startsWith('image/')) {
          this.imageFileDataMap.push({
            id: fileData.Id,
            base64: fileData.base64,
            fileName: fileData.fileName,
            data: fileData.data,
            time: fileData.time,
            star: false,
          });
          console.log(this.imageFileDataMap);
        } else if (fileData.fileType.startsWith('video/')) {
          this.videoFileDataMap.push({
            id: fileData.id,
            fileName: fileData.fileName,
            data: fileData.data,
            time: fileData.time,
            star: false,
          });
          console.log(this.videoFileDataMap);
        } else if (fileData.fileType.startsWith('audio/')) {
          this.audioFileDataMap.push({
            id: fileData.id,
            fileName: fileData.fileName,
            data: fileData.data,
            time: fileData.time,
            star: false,
          });
          console.log(this.audioFileDataMap);
        } else if (fileData.fileType === 'application/pdf') {
          this.pdfFileDataMap.push({
            id: fileData.id,
            fileName: fileData.fileName,
            data: fileData.data,
            time: fileData.time,
            star: false,
          });
          console.log(this.pdfFileDataMap);
        }
      } catch (error) {
        alert(error.message); // 显示包含错误信息的警告
        break; // 停止循环
      }
    };

    this.$emit('update-data', {
      imageFileDataMap: this.imageFileDataMap,
      videoFileDataMap: this.videoFileDataMap,
      audioFileDataMap: this.audioFileDataMap,
      pdfFileDataMap: this.pdfFileDataMap,
    });
    this.isLoading = false;
    this.isOpen = false;
    this.files = [];
    this.$emit('open-success');
    // Now you have separate maps for each file type
  },

  deleteFile(file) {
    const index = this.files.indexOf(file);
    if (index !== -1) {
      this.files.splice(index, 1);
    }
  },

  handleDrop(event) {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files).map(file => ({
      file,
      progress: 0,
    }));
    this.files = this.files.concat(files);
  },
  closeModal() {
    this.isOpen = false;
    this.files = []; // Clear the files array
  },
  openModalAndSetAcceptedFileTypes(fileTypes) {
    this.acceptedFileTypes = fileTypes;
    this.isOpen = true;
  },
},
//生命周期 - 创建完成（可以访问当前this实例）
created() {

},
//生命周期 - 挂载完成（可以访问DOM元素）
mounted() {

},
beforeCreate() {}, //生命周期 - 创建之前
beforeMount() {}, //生命周期 - 挂载之前
beforeUpdate() {}, //生命周期 - 更新之前
updated() {}, //生命周期 - 更新之后
beforeDestroy() {}, //生命周期 - 销毁之前
destroyed() {}, //生命周期 - 销毁完成
activated() {}, //如果页面有keep-alive缓存功能，这个函数会触发
}
</script>
<style lang='scss' scoped>
.center-modal-overlay {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  inset: 0;
  z-index: 80;
  padding: 24px;
  overflow-y: auto;
  background: rgba(15, 23, 42, 0.12);
  backdrop-filter: blur(6px);
}

.ai-links-menu {
  position: relative;
  z-index: 130;
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
}

.ai-links-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  z-index: 140;
  width: 360px;
  padding: 14px;
  border: 1px solid rgba(148, 163, 184, 0.24);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 24px 60px -34px rgba(15, 23, 42, 0.42);
  backdrop-filter: blur(18px);
}

.ai-links-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.ai-links-card,
.ai-links-action {
  display: inline-flex;
  width: 100%;
  align-items: center;
  gap: 10px;
  border: 1px solid rgba(203, 213, 225, 0.9);
  background: rgba(255, 255, 255, 0.95);
  color: #334155;
  transition: border-color 0.16s ease, background 0.16s ease, box-shadow 0.16s ease, transform 0.16s ease;
}

.ai-links-card {
  min-height: 72px;
  padding: 0 16px;
  border-radius: 16px;
  font-size: 15px;
  font-weight: 600;
  justify-content: flex-start;
}

.ai-links-action {
  min-height: 48px;
  padding: 0 14px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  justify-content: flex-start;
}

.ai-links-card:hover,
.ai-links-action:hover,
.ai-links-card.is-active,
.ai-links-action.is-active {
  border-color: rgba(99, 102, 241, 0.38);
  background: rgba(248, 250, 255, 0.98);
  box-shadow: 0 18px 30px -28px rgba(79, 70, 229, 0.5);
  transform: translateY(-1px);
}

.ai-links-footer {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed rgba(203, 213, 225, 0.9);
}

.ai-links-icon {
  flex: 0 0 auto;
  color: #4f46e5;
}

.ai-links-icon.small {
  color: #475569;
}

.ai-links-trigger {
  display: inline-flex;
  min-height: 36px;
  min-width: 118px;
  align-items: center;
  justify-content: center;
  padding: 0 14px;
  border-radius: 999px;
  white-space: nowrap;
  flex: 0 0 auto !important;
  width: auto;
  position: relative;
  z-index: 1;
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
.btn-s {
  flex: 0 0 auto;
  text-align: center;
  text-transform: uppercase;
  transition: 0.5s;
  background-size: 200% auto;
  color: white;
 /* text-shadow: 0px 0px 10px rgba(0,0,0,0.2);*/
  box-shadow: 0 0 20px #eee;
 }
 .btn-s:hover {
  background-position: right center; /* change the direction of the change here */
}
 .btn-2 {
  background-image: linear-gradient(to right, #fbc2eb 0%, #a6c1ee 51%, #fbc2eb 100%);
 }

@media (max-width: 768px) {
  .ai-links-dropdown {
    right: auto;
    left: 50%;
    width: min(360px, calc(100vw - 24px));
    transform: translateX(-50%);
  }
}
</style>
