<template>
  <div class="forgetPassword-box">
    <div class="title-bar">
      <span>忘记密码</span>
    </div>
    <div class="input-area">
      <div>
        <el-form ref="loginFormRef" :model="loginForm" status-icon :rules="rules" label-width="60px" class="loginForm" size="large" label-position="top">
          <el-form-item label="账号" prop="acc">
            <el-input v-model="loginForm.acc" placeholder="请输入手机号" clearable type="text" autocomplete="off" :prefix-icon="User" />
          </el-form-item>
          <el-form-item label="密码" prop="psw">
            <el-input v-model="loginForm.psw" placeholder="请输入密码" show-password clearable type="password" autocomplete="off" :prefix-icon="Lock" />
          </el-form-item>
          <el-form-item label="确认密码" prop="rePsw">
            <el-input v-model="loginForm.rePsw" placeholder="请确认密码" show-password clearable type="password" autocomplete="off" :prefix-icon="Lock" />
          </el-form-item>
          <el-form-item label="验证码" prop="code">
            <el-input v-model="loginForm.code" placeholder="请输入验证码" clearable type="text" maxlength="6" autocomplete="off" style="width: 50%" />
            <el-button :disabled="codeDisabled" :loading="codeLoading" @click="getVerifyCode" style="width: 45%; margin-left: 5%">{{ codeText }}</el-button>
          </el-form-item>
          <el-form-item>
            <el-button class="submit" :loading="loading" type="primary" @click="submitForm">重置</el-button>
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
import { confirmAccount, resetPassword, sendSms } from "@/api/user";
import { Lock, User } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";

const router = useRouter();

const loginFormRef = ref<FormInstance>();
const codeLoading = ref<boolean>(false);
const codeText = ref<string>("获取验证码");
const codeDisabled = ref<boolean>(true);

const count = ref<number>(10);

const daojishi = () => {
  codeDisabled.value = true;
  let timer = setInterval(() => {
    if (count.value > 1) {
      count.value--;
      codeText.value = `${count.value} 秒后获取`;
    } else {
      clearInterval(timer);
      count.value = 10;
      codeText.value = "获取验证码";
      codeDisabled.value = false;
    }
  }, 1000);
};

const getVerifyCode = async () => {
  daojishi();
  codeLoading.value = true;
  try {
    const d = await sendSms({ countryCode: "86", phone: loginForm.acc, oemId: "haiwell" });
    codeLoading.value = false;
    ElMessage.success(`验证码已发送，请注意查收`);
    console.log("🚀 ~ file: index.vue:133 ~ getVerifyCode ~ d:", d);
  } catch (err: any) {
    console.log("🚀 ~ file: index.vue:135 ~ getVerifyCode ~ err:", err);
    setTimeout(() => {
      codeLoading.value = false;
      ElMessage.error(`出现错误，${err.hwmsg}`);
    }, 300);
  }
};

const validateAcc = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error("请输入手机号"));
  }
  const regPhone = /^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-79])|(?:5[0-35-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[1589]))\d{8}$/;
  setTimeout(async () => {
    if (!regPhone.test(value)) {
      callback(new Error("手机号格式有误"));
      codeDisabled.value = true;
    } else {
      try {
        const d = await confirmAccount({ countryCode: "86", account: `${value}` });
        console.log("confirmAccount===success", d);
        callback();
        codeDisabled.value = false;
      } catch (err: any) {
        console.log("confirmAccount===error", err);
        if (err.hwcode == 404) {
          callback(new Error("该手机号未注册过"));
        } else {
          callback(new Error("出现其他错误"));
        }
        codeDisabled.value = true;
      }
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

const validateRePass = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("请再次输入密码"));
  }
  setTimeout(() => {
    if (value.length < 6 || value.length > 20) {
      callback(new Error("密码长度在6-20之间"));
    } else if (value !== loginForm.psw) {
      callback(new Error("输入的密码不一致，请重新输入"));
    } else {
      callback();
    }
  }, 200);
};

const validateCode = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("请输入验证码"));
  }
  setTimeout(() => {
    if (value.length !== 4) {
      callback(new Error("验证码长度为4位"));
    } else {
      callback();
    }
  }, 200);
};

const loginForm = reactive({
  acc: "",
  psw: "",
  rePsw: "",
  code: ""
});

const loading = ref<boolean>(false);

const rules = reactive<FormRules>({
  acc: [{ validator: validateAcc, trigger: "change" }],
  psw: [{ validator: validatePass, trigger: "change" }],
  rePsw: [{ validator: validateRePass, trigger: "change" }],
  code: [{ validator: validateCode, trigger: "change" }]
});

const submitForm = async () => {
  if (!loginFormRef.value) return;
  loading.value = true;
  loginFormRef.value.validate((valid: boolean) => {
    if (valid) {
      resetPasswordAction();
    } else {
      ElMessage({
        message: "校验错误",
        type: "error"
      });
      loading.value = false;
    }
  });
};

const resetPasswordAction = async () => {
  try {
    const d: any = await resetPassword({
      account: loginForm.acc,
      password: loginForm.psw,
      countryCode: "86",
      oemId: "haiwell",
      code: loginForm.code
    });
    console.log(d);
    ElMessage.success(`重置成功！`);
    setTimeout(() => {
      router.push("/login");
    }, 500);
  } catch (err: any) {
    console.log(err);
    switch (err.hwcode) {
      case 406:
        ElMessage.error("验证码错误");
        break;
      default:
        ElMessage.error(err.hwmsg);
        break;
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style lang="less" scoped>
.forgetPassword-box {
  .loginForm {
    & .submit {
      width: 100%;
      margin-top: 20px;
    }
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
    justify-content: end;
  }
}
</style>
