<!--  -->
<template>
  <div class="flex">
    <input type="checkbox" id="drawer-toggle" class="relative sr-only peer">

      <div class="flex items-center border-2 border-solid border-gray-100 px-3 z-20 w-full transition-all duration-500 transform translate-x-3/4 bg-white shadow-sm peer-checked:-translate-x-0">
        <label
        for="drawer-toggle"
        class="mr-4 inline-block transition-all duration-1000 rounded-lg"
        :class="{ 'rotate-180': isRotated }"
        @click="toggleRotation"
        >
            <div class="w-4 h-1 mb-1 -rotate-45 bg-gray-300 rounded-lg"></div>
            <div class="w-4 h-1  rotate-45 bg-gray-300 rounded-lg"></div>
        </label>

          <button
          @click="changePlaybackRate()"
          >
            {{ playbackRate }}x
          </button>
          <button
          class="hover:bg-gray-200 rounded-full h-4 w-4 mx-1"
          @click="togglePlayPause"
          >
            <svg-icon :name="isPlaying ? '暂停 (1)' : '播放 (1)'"></svg-icon>
          </button>
          <button
          class="hover:bg-gray-200 rounded-full h-4 w-4 mx-1"
          @click="toggleRecordPause"
          >
            <svg-icon :name="isRecording ? '暂停' : '录音 (1)'"></svg-icon>
          </button>
          <div class="BaseRecorder-wave h-10 w-full flex">
            <canvas ref="record"></canvas>
            <canvas ref="play"></canvas>
          </div>
          <Menu as="div" class=" inline-block text-left right-0 fixed">
            <div>
              <MenuButton class="inline-flex w-full justify-center items-center gap-x-1.5 rounded-lg bg-white px-3 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                <svg-icon name="menu"></svg-icon>
              </MenuButton>
            </div>
            <transition
            enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
            @leave="isEditing = false"
            >
            <MenuItems class="px-2 py-1 absolute right-0 top-6 z-10 mt-2 w-96 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
              <MenuItem
              class="w-full flex py-2"
              >
                <div class="w-full grid grid-cols-2 ">
                  <span class="text-base px-1">录制的音频</span>
                  <div class="flex items-center justify-center">
                    <button @click.stop="toggleEdit" class="mx-1">
                      编辑
                    </button>
                    <button v-if="selectedRecordings.length === 1" @click.stop="renameSelectedRecording"  class="mx-1">
                      <svg-icon name="编辑"></svg-icon>
                    </button>
                    <button v-if="selectedRecordings.length >= 1" @click.stop="deleteSelectedRecordings"  class="mx-1">
                      <svg-icon name="icon_delete"></svg-icon>
                    </button>
                  </div>
                </div>
              </MenuItem>
              <MenuItem
              v-for="(recording, index) in recordings"
              :key="index"
              class="w-full hover:bg-gray-200 rounded-md grid grid-cols-2 items-center"
              @mouseover="recording.isHovered = true"
              @mouseleave="recording.isHovered = false"
              @click.stop="playRecording(index)"
              >
              <div class="w-full items-center py-2 rounded-sm">
                <div class="flex items-center">
                  <div class="inline-flex items-center">
                    <label
                    class="relative flex cursor-pointer items-center rounded-full mr-2"
                    for="checkbox-6"
                    data-ripple-dark="true"
                    >
                    <input
                      type="checkbox"
                      class="before:content[''] peer relative h-4 w-4 cursor-pointer appearance-none rounded-full border border-orange-800 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-6 before:w-6 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-orange-700 before:opacity-0 before:transition-opacity checked:border-orange-500 checked:bg-orange-600 checked:before:bg-orange-600 hover:before:opacity-10"
                      id="checkbox-6"
                      v-model="selectedRecordings"
                      :value="index" v-show="isEditing"
                      @click.stop
                    />
                    <div
                      class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-white opacity-0 transition-opacity peer-checked:opacity-100"
                      :value="index" v-show="isEditing"
                      @click.stop
                    >
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
                  <label class="text-orange-500">{{ recording.name }}</label>
                </div>
                <button
                  class=" h-8 w-29 rounded-full px-2 py-1 hover:text-blue-400 hover:bg-blue-100 hover:shadow-md hover:shadow-blue-400/50"
                  :class="{ 'bg-gray-200': recording.isHovered  }"
                  @click.stop="uploadRecording(index)"
                >
                  <span v-if="recording.isLoading" class="flex items-center justify-center">
                    <div style="border-top-color:transparent" class="w-4 h-4 border-4 border-blue-200 rounded-full animate-spin"></div>
                    <p class="ml-2">loading...</p>
                  </span>
                  <span v-else class="inline-flex items-center">
                    <svg-icon name="语音转文本-copy" class="mr-2"></svg-icon>
                    语音转文字
                  </span>
                </button>
              </div>
            </MenuItem>
            </MenuItems>
          </transition>
        </Menu>
      </div>
  </div>
</template>

<script>
import Recorder from 'js-audio-recorder';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue';
import axios from "axios";

export default {
name: 'record',
components: {
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
},
props: {
    document: {
      type: Object,
      required: true
    },
  },
data() {
  return {
    recorder: null,
    // 波浪图-录音
    drawRecordId: null,
    // 波浪图-播放
    drawPlayId: null,
    // 切换播放速度
    playbackRate: 1.0,
    playbackRates: [0.5, 0.75, 1.0, 1.25, 1.5, 2.0],
    currentRateIndex: 2, // 对应1.0x
    // 播放暂停
    isPlaying: false,
    isRecording: false,
    recordings: [],
    recordingCount: 0,
    isEditing: false,
    selectedRecordings: [],
    isHovered: false,
    isLoading: false,
    isRotated: false,
  }
},
computed: {
  isDisabled() {
      return this.isHovered;
    },
},
mounted() {
  this.init();
  this.fetchRecordings();

},
methods: {
  // 初始化
  init() {
    this.recorder = new Recorder({
      // 采样位数，支持 8 或 16，默认是16
      sampleBits: 16,
      // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值
      sampleRate: 16000,
      // 声道，支持 1 或 2， 默认是1
      numChannels: 1,
      // 是否边录边转换，默认是false
      compiling: false
    })
  },
  toggleRotation() {
    this.$emit('toggle-drawer');
    console.log("toggle");
    this.isRotated = !this.isRotated;
  },
  toggleEdit() {
      this.isEditing = !this.isEditing;
  },
  deleteSelectedRecordings() {
    this.selectedRecordings.sort().reverse().forEach(index => this.recordings.splice(index, 1));
    this.selectedRecordings = [];
  },
  renameSelectedRecording() {
    const index = this.selectedRecordings[0];
    const newName = prompt('请输入新的录音名称：', this.recordings[index].name);
    if (newName) {
      this.recordings[index].name = newName;
    }
  },
  changePlaybackRate() {
    this.currentRateIndex = (this.currentRateIndex + 1) % this.playbackRates.length;
    this.playbackRate = this.playbackRates[this.currentRateIndex];
    this.recorder.playbackRate = this.playbackRate;
  },
  // 开始录音
  startRecorder() {
    this.recorder.start().then(
      () => {
        this.drawRecord()
      },
      error => {
        // 出错了
        console.log(`${error.name} : ${error.message}`)
      }
    )
  },
  // 继续录音
  resumeRecorder() {
    this.recorder.resume()
  },
  toggleRecordPause() {
    if (this.isRecording) {
      this.stopRecorder();
    } else {
      this.startRecorder();
    }
    this.isRecording = !this.isRecording;
  },
  //切换播放暂停
  togglePlayPause() {
    if (this.isPlaying) {
      this.stopPlayRecorder();
    } else {
      this.playRecorder();
    }
    this.isPlaying = !this.isPlaying;
  },

  // 暂停录音
  pauseRecorder() {
    this.recorder.pause()
    this.drawRecordId && cancelAnimationFrame(this.drawRecordId)
    this.drawRecordId = null
  },
  // 结束录音
  async stopRecorder() {
  this.recorder.stop();
  this.drawRecordId && cancelAnimationFrame(this.drawRecordId);
  this.drawRecordId = null;

    // 保存录音
    const blob = await this.recorder.getWAVBlob();
    const url = URL.createObjectURL(blob);
    this.recordingCount += 1; // Increment the count
    const recordingName = `录音 ${this.recordingCount.toString().padStart(3, '0')}`; // Generate the name
    this.recordings.push({ name: recordingName, url }); // Use the generated name
  },
  // 录音播放
  playRecorder() {
    this.recorder.play()
    this.drawPlay() // 绘制波浪图
  },
  // 暂停录音播放
  pausePlayRecorder() {
    this.recorder.pausePlay()
  },
  // 恢复录音播放
  resumePlayRecorder() {
    this.recorder.resumePlay()
    this.drawPlay() // 绘制波浪图
  },
  // 停止录音播放
  stopPlayRecorder() {
    this.recorder.stopPlay()
  },
  // 销毁录音
  destroyRecorder() {
    this.recorder.destroy().then(function() {
      this.drawRecordId && cancelAnimationFrame(this.drawRecordId)
      this.drawRecordId = null

      this.drawPlayId && cancelAnimationFrame(this.drawPlayId)
      this.drawPlayId = null

      this.recorder = null
    })
  },

  /**
   *  下载录音文件
   * */
  // 下载pcm
  downPCM() {
    // 这里传参进去的时文件名
    this.recorder.downloadPCM('新文件')
  },
  // 下载wav
  downWAV() {
    // 这里传参进去的时文件名
    this.recorder.downloadWAV('新文件')
  },

  /**
   * 绘制波浪图-录音
   * */
  drawRecord() {
    this.drawRecordId = requestAnimationFrame(this.drawRecord)
    this.drawWave({
      canvas: this.$refs.record,
      dataArray: this.recorder.getRecordAnalyseData(),
      bgcolor: 'rgb(255, 128, 200)',
      lineWidth: 1,
      lineColor: 'rgb(0, 128, 255)'
    })
  },
  /**
   * 绘制波浪图-播放
   * */
  drawPlay() {
    this.drawPlayId = requestAnimationFrame(this.drawPlay)
    this.drawWave({
      canvas: this.$refs.play,
      dataArray: this.recorder.getPlayAnalyseData()
    })
  },
  drawWave({
    canvas,
    dataArray,
    bgcolor = 'rgb(200, 200, 200)',
    lineWidth = 2,
    lineColor = 'rgb(0, 0, 0)'
  }) {
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    const bufferLength = dataArray.length
    // 一个点占多少位置，共有bufferLength个点要绘制
    const sliceWidth = canvas.width / bufferLength
    // 绘制点的x轴位置
    let x = 0

    // 填充背景色
    ctx.fillStyle = bgcolor
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    // 设定波形绘制颜色
    ctx.lineWidth = lineWidth
    ctx.strokeStyle = lineColor

    ctx.beginPath()

    for (let i = 0; i < bufferLength; i++) {
      const v = dataArray[i] / 128
      const y = (v * canvas.height) / 2

      if (i === 0) {
        // 第一个点
        ctx.moveTo(x, y)
      } else {
        // 剩余的点
        ctx.lineTo(x, y)
      }
      // 依次平移，绘制所有点
      x += sliceWidth
    }

    // 最后一个点
    ctx.lineTo(canvas.width, canvas.height / 2)
    ctx.stroke()
  },

  async fetchRecordings() {
    // 假设你有一个获取录音的方法，返回一个包含录音对象的数组
    const recordings = await getRecordings();
    this.recordings = recordings.map(recording => ({ ...recording, isLoading: false, isHovered: false }));
  },
  /**
   * 上传录音文件
   */
   async uploadRecording(index) {
    this.recordings[index].isLoading = true;
    this.uploadStatus = '上传中...';
    console.log("上传录音" + index);

    try {
      const recording = this.recordings[index];
      const response = await fetch(recording.url);
      const blob = await response.blob();


      console.log('Blob size:', blob.size);
      // 判断 Blob 是否获取成功
      if (blob.size === 0) {
        throw new Error('获取 Blob 失败，文件大小为 0');
      } else {
        console.log('成功获取blob对象');
      };
      const username = localStorage.getItem("userName") || "unknown_user";
      const file_name = this.document.title;
      const formData = new FormData();
      const name = recording.name; // 获取录音名字
      formData.append('file', blob, 'recording.wav'); // 假设你要上传的文件名为 recording.wav
      formData.append('username', username); // Replace 'your_username' with the actual username
      formData.append('file_name', file_name); // Replace 'recording.wav' with the actual file name
      formData.append('time', new Date());
      formData.append('filename', name);
      const uploadResponse = await axios.post('http://127.0.0.1:5000/api/audioIE', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log(uploadResponse);
        const id = uploadResponse.Id[0];
        const transcription = uploadResponse.ie_result; // 假设后端返回的文字信息在 transcription 字段
        const currentTime = new Date().toLocaleString(); // 获取当前时间

            // 发送事件
        this.$emit('transcription-uploaded', { id, transcription, currentTime, name });

        console.log("上传成功");
        console.log(uploadResponse);
        // this.transcription = uploadResponse.transcription; // 假设后端返回的文字信息在 transcription 字段
      } catch (error) {
        console.log("上传失败");
        console.error(error);
        // 这里可以添加用户友好的错误处理
      } finally {
        this.recordings[index].isLoading = false;
      }
    },


  saveRecording() {
    const blob = this.recorder.getWAVBlob();
    const url = URL.createObjectURL(blob);
    this.recordings.push({ name: 'New Recording', url });
  },
  renameRecording(index, newName) {
    this.recordings[index].name = newName;
  },
  playRecording(index) {
      const recording = this.recordings[index];
      const audio = new Audio(recording.url);
      audio.play();
    },
}
}
</script>
<style lang='scss' scoped>
//@import url(); 引入公共css类
.rotate-180 {
  transform: rotate(180deg);
}
</style>