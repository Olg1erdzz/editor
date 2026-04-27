<template>
  <div class="bg-gray-100 flex justify-center items-center h-screen">
    <div class="w-1/2 h-screen hidden lg:block">
  <img src="/assets/logo.png"  class="bounce-in-top" style="width: 400px; height: 230px; margin-top: 150px;margin-left: 150px">
  <p class="tracking-in-expand" style="font-size: 30px;width: 300px; height: 100px;margin-left: 250px">
    文星编辑器<br>
    WENXING EDITER
  </p>
</div>
    <div class="lg:p-36 md:p-52 sm:20 p-8 w-full lg:w-1/2">
      <h1 class="text-3xl font-semibold mb-5" style="margin-bottom: 50px">欢迎登录</h1>
      <div>
        <el-form ref="loginFormRef" :model="loginForm" status-icon :rules="rules" label-width="60px" class="loginForm" size="large" label-position="top">
          <el-form-item label="用户名" prop="username" class="block text-gray-600">
            <el-input v-model="loginForm.username" placeholder="请输入用户名" clearable type="text"  autocomplete="off" />
          </el-form-item>
          <el-form-item label="密码" prop="password" class="block text-gray-600">
            <el-input v-model="loginForm.password" placeholder="请输入密码" show-password clearable type="password"  autocomplete="off" :prefix-icon="Lock" />
          </el-form-item>
          <el-form-item>
            <el-button class="bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-md py-2 px-4 w-full" :loading="loading" type="primary" @click="submitForm" style="margin-top: 20px">登录</el-button>
            <el-link :underline="false" @click="$router.push('/register')" class="hover:underline">没有账号？去注册</el-link>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import { ElMessage, FormInstance, FormRules } from "element-plus";
import { useRouter } from "vue-router";
import { login } from "@/api/user";
import { Lock } from "@element-plus/icons-vue";

const router = useRouter();

const loginFormRef = ref<FormInstance>();

const validateUsername = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error("请输入用户名"));
  }
  setTimeout(() => {
    callback();
  }, 200);
};

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("请输入密码"));
  }
  setTimeout(() => {
    if (value.length < 6 || value.length > 20) {
      callback(new Error("密码长度在6-20之间"));
    } else {
      callback();
    }
  }, 200);
};

const loginForm = reactive({
  username: "",
  password: ""
});

const loading = ref<boolean>(false);

const rules = reactive<FormRules>({
  username: [{ validator: validateUsername, trigger: "change" }],
  password: [{ validator: validatePass, trigger: "change" }]
});

const submitForm = async () => {
  if (!loginFormRef.value) return;
  loading.value = true;
  loginFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const response = await login({
          username: loginForm.username,
          password: loginForm.password
        });
        const { token, user } = response.data; // 修改为从 response.data 获取 token 和 user
        localStorage.setItem("token", token);
        localStorage.setItem("userName", user.name);
        localStorage.setItem("role", user.role);
        localStorage.setItem("avatar",user.avatar)
        setTimeout(() => {
          router.push({ name: 'index' });
        }, 50);
        setTimeout(()=>{
          location.reload();
        },100)
      } catch (err: any) {
        console.log(err);
        ElMessage.error(err.message || "登录失败，请重试");
      } finally {
        loading.value = false;
      }
    } else {
      ElMessage.error("请检查输入的内容");
      loading.value = false;
    }
  });
};
</script>

<style lang='scss' scoped>
.login-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.loginForm {
  width: 400px;
}

.title-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
& span {
    font-size: 24px;
    color: #777;
    font-weight: bold;
  }
}

.footer {
  display: flex;
  justify-content: space-between;
}
.bounce-in-top {
	-webkit-animation: bounce-in-top 2s both;
	        animation: bounce-in-top 2s both;
}
.tracking-in-expand {
	-webkit-animation: tracking-in-expand 2s ;
	        animation: tracking-in-expand 2s ;
}
@-webkit-keyframes bounce-in-top {
  0% {
    -webkit-transform: translateY(-500px);
            transform: translateY(-500px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
    opacity: 0;
  }
  38% {
    -webkit-transform: translateY(0);
            transform: translateY(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
    opacity: 1;
  }
  55% {
    -webkit-transform: translateY(-65px);
            transform: translateY(-65px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  72% {
    -webkit-transform: translateY(0);
            transform: translateY(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
  81% {
    -webkit-transform: translateY(-28px);
            transform: translateY(-28px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  90% {
    -webkit-transform: translateY(0);
            transform: translateY(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
  95% {
    -webkit-transform: translateY(-8px);
            transform: translateY(-8px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  100% {
    -webkit-transform: translateY(0);
            transform: translateY(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
}
@keyframes bounce-in-top {
  0% {
    -webkit-transform: translateY(-500px);
            transform: translateY(-500px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
    opacity: 0;
  }
  38% {
    -webkit-transform: translateY(0);
            transform: translateY(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
    opacity: 1;
  }
  55% {
    -webkit-transform: translateY(-65px);
            transform: translateY(-65px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  72% {
    -webkit-transform: translateY(0);
            transform: translateY(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
  81% {
    -webkit-transform: translateY(-28px);
            transform: translateY(-28px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  90% {
    -webkit-transform: translateY(0);
            transform: translateY(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
  95% {
    -webkit-transform: translateY(-8px);
            transform: translateY(-8px);
    -webkit-animation-timing-function: ease-in;
            animation-timing-function: ease-in;
  }
  100% {
    -webkit-transform: translateY(0);
            transform: translateY(0);
    -webkit-animation-timing-function: ease-out;
            animation-timing-function: ease-out;
  }
}
@-webkit-keyframes tracking-in-expand {
  0% {
    letter-spacing: -0.5em;
    opacity: 0;
  }
  40% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
}
@keyframes tracking-in-expand {
  0% {
    letter-spacing: -0.5em;
    opacity: 0;
  }
  40% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
}
</style>
