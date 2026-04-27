<template>
  <div style="height: 100%">
    <el-container style="height: 100%">
      <el-aside>
        <side-component></side-component>
      </el-aside>
      <el-container>
        <el-header>
          <div style="width: 100%; height: 80%; display: flex; align-items: center; justify-content: space-between">
            <el-avatar src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Flmg.jj20.com%2Fup%2Fallimg%2Ftx04%2F071020195590.jpg&refer=http%3A%2F%2Flmg.jj20.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1652889988&t=10eaf8745df2f8c8c2b2ba1575591471"></el-avatar>
            <el-button type="warning"><router-link :to="{ path: '/' }">返回首页</router-link></el-button>
          </div>
        </el-header>
        <el-main>
          <router-view></router-view>
        </el-main>
        <el-footer>Footer</el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import SideComponent from "./SideComponent.vue";
export default {
  name: "ManagerPage",
  components: {
    SideComponent
  }
};
</script>

<style scoped>
.el-header {
  background-color: #333333;
  color: #333;
  text-align: center;
  line-height: 60px;
  display: flex;
  align-items: center;
}

.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
  display: flex;
  align-items: center;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  /*text-align: center;*/
  line-height: 200px;
}

.el-main {
  /*background-color: #E9EEF3;*/
  color: #333;
  text-align: center;
  /*line-height: 160px;*/
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
</style>
