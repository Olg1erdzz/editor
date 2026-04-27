<template>
  <div>
    <video class="video-js filmVideo vjs-big-play-centered vjs-show-big-play-button-on-pause" id="myVideo">
      <source :src="baseUrl + videoUrl" controls="controls" type="video/mp4" />
    </video>
  </div>
</template>

<script>
export default {
  name: "VideoCheck",
  props: {
    videoUrl: ""
  },
  data() {
    return {
      baseUrl: ""
    };
  },
  created() {
    this.baseUrl = this.$store.state.baseUrl.remoteUrl;
    console.log("视频地址：", this.baseUrl + this.videoUrl);
  },
  mounted() {
    this.initVideo();
  },
  methods: {
    initVideo() {
      //初始化视频方法
      let myPlayer = this.$video(myVideo, {
        //是否显示控制栏
        controls: true,
        //是否自动播放,muted:静音播放
        autoplay: false,
        //是否静音播放
        muted: false,
        //是否流体自适应容器宽高
        // fluid:true,
        //设置视频播放器的显示宽度（以像素为单位）
        width: "800px",
        //设置视频播放器的显示高度（以像素为单位）
        height: "400px"
      });
    }
  }
};
</script>

<style scoped></style>
