<template>
  <div class="auth-container">
    <h1 class="system-title">学工系统</h1>
    <div class="login-container">
      <h2>欢迎登录学工系统</h2>
      <div class="input-group">
        <label for="username">用户名:</label>
        <input type="text" v-model="loginUsername" id="username" placeholder="学号/工号" />
      </div>
      <div class="input-group">
        <label for="password">密码:</label>
        <input type="password" v-model="loginPassword" id="password" placeholder="密码" />
      </div>
      <div class="input-group role-selection">
        <label>选择角色:</label>
        <label><input type="radio" v-model="loginRole" value="student" /> 学生</label>
        <label><input type="radio" v-model="loginRole" value="teacher" /> 老师</label>
      </div>
      <button class="auth-button" @click="login">登录</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginRole: "student",
      loginUsername: "",
      loginPassword: ""
    };
  },
  methods: {
    login() {
      if (this.loginUsername && this.loginPassword) {
        localStorage.setItem("role", this.loginRole);
        localStorage.setItem("username", this.loginUsername);
        this.$router.push("/");
      } else {
        alert("请输入用户名和密码");
      }
    }
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
}

.system-title {
  font-size: 24px;
  color: #4caf50;
  margin-bottom: 20px;
}

.login-container {
  width: 400px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

h2 {
  margin-bottom: 20px;
  color: #4caf50;
  background-color: #e8f5e9;
  padding: 10px;
  border-radius: 5px;
  text-align: center;
}

.input-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

input[type="text"],
input[type="password"] {
  width: calc(100% - 20px);
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.role-selection label {
  display: inline-block;
  margin-right: 10px;
}

.auth-button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #4caf50;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.auth-button:hover {
  background-color: #45a049;
}
</style>
