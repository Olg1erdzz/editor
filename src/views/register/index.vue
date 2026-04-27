<template>
  <div class="register-box">
    <div class="title-bar">
      <span>欢迎注册</span>
    </div>
    <div class="input-area">
      <div>
        <el-form ref="registerFormRef" :model="registerForm" status-icon :rules="rules" label-width="60px" class="registerForm" size="large" label-position="top">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="registerForm.username" placeholder="请输入用户名" clearable type="text" autocomplete="off" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="registerForm.email" placeholder="请输入邮箱" clearable type="text" autocomplete="off" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="registerForm.password" placeholder="请输入密码" show-password clearable type="password" autocomplete="off" />
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input v-model="registerForm.confirmPassword" placeholder="请确认密码" show-password clearable type="password" autocomplete="off" />
          </el-form-item>
          <el-form-item label="角色" prop="role">
            <el-select v-model="registerForm.role" placeholder="请选择角色">
              <el-option label="用户" value="user"></el-option>
              <el-option label="老师" value="teacher"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button class="submit" :loading="loading" type="primary" @click="submitForm">注册</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="footer">
      <el-link :underline="false" @click="$router.push('/login')">已有账号？去登录</el-link>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import { ElMessage, FormInstance, FormRules } from "element-plus";
import { useRouter } from "vue-router";
import { register } from "@/api/user";

const router = useRouter();

const registerFormRef = ref<FormInstance>();

const validateUsername = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error("请输入用户名"));
  }
  setTimeout(() => {
    callback();
  }, 200);
};

const validateEmail = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error("请输入邮箱"));
  }
  const regEmail = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
  setTimeout(() => {
    if (!regEmail.test(value)) {
      callback(new Error("邮箱格式有误"));
    } else {
      callback();
    }
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

const validateConfirmPass = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("请再次输入密码"));
  }
  setTimeout(() => {
    if (value !== registerForm.password) {
      callback(new Error("两次输入的密码不一致"));
    } else {
      callback();
    }
  }, 200);
};

const validateRole = (rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error("请选择角色"));
  } else {
    callback();
  }
};

const registerForm = reactive({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
  role: ""
});

const loading = ref<boolean>(false);

const rules = reactive<FormRules>({
  username: [{ validator: validateUsername, trigger: "change" }],
  email: [{ validator: validateEmail, trigger: "change" }],
  password: [{ validator: validatePass, trigger: "change" }],
  confirmPassword: [{ validator: validateConfirmPass, trigger: "change" }],
  role: [{ validator: validateRole, trigger: "change" }]
});

const submitForm = async () => {
  if (!registerFormRef.value) return;
  loading.value = true;
  registerFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const response = await register({
          username: registerForm.username,
          email: registerForm.email,
          password: registerForm.password,
          role: registerForm.role
        });
        const { token, user } = response.data; // 从 response.data 获取 token 和 user
        localStorage.setItem("token", token);
        localStorage.setItem("userName", user.name);
        localStorage.setItem("role", user.role);
        setTimeout(() => {
          router.push("/login");
          ElMessage.success("注册成功");
        }, 300);
      } catch (err: any) {
        console.log(err);
        ElMessage.error(err.message || "注册失败，请重试");
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

<style scoped>
.register-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.registerForm {
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
</style>
