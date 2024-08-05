<template>
  <div class="main">
    <el-row>
      <el-col :xs="6" :sm="6" :lg="4">
        <div class="history">
          <div class="new_qa" id="new_qa">
            <div class="qa_button" @click="addQA">
              <img src="@/imgs/加号.svg" />
              <span>新对话</span>
            </div>
          </div>

          <div class="doubao" tabindex="0">
            <img src="@/imgs/机器人头像.svg" alt="小H" />
            小H
          </div>
          <div class="history_box">
            <div
              v-for="(item, index) in chat_history"
              :key="index"
              @click="click_history(item)"
            >
              <div class="history_chat" tabindex="0" @click="togglespan(isVisible=true)">
                <span class="history_chat_message" :title="item.message">{{
                  item.message
                }}</span>
                <el-popover placement="top-start" width="200" trigger="click">
                  <span class="history_chat_time">{{ item.talk_time }}</span
                  ><br />
                  <div class="rename_box" @click="renameSummarize(item)">
                    <img src="@/imgs/重写.svg" />
                    <span>重命名</span>
                  </div>
                  <div class="delete_box" @click="deleteHistory(item)">
                    <img src="@/imgs/删除.svg" />
                    <span>删除</span>
                  </div>
                  <img src="@/imgs/省略号.svg" slot="reference" />
                </el-popover>
              </div>
            </div>
          </div>

          <div class="find_agent" tabindex="0" @click="selectAgent">
            <img src="@/imgs/智能体.svg" alt="智能体" class="zhuangshi" />
            <span class="agent">智能体</span>
            <img :src="moreIcon" class="show_more_agent" />
          </div>

          <div v-if="showAgents">
            <div
              v-for="(item, index) in agent"
              :key="index"
              class="agent_title"
              tabindex="0"
              @click="agentChat(item),togglespan(isVisible=false)"
            >
              <img :src="item.icon" />
              <span>{{ item.title }}</span>
            </div>
          </div>

          <div class="login">
            <el-button
              type="primary"
              class="login_button"
              @click="toLogin"
              v-if="!isLogin"
              >登录</el-button
            >
            <div v-if="isLogin" class="user_info">
              <div class="user_avatar">
                <img src="@/imgs/用户头像.png" alt="" />
                <span>admin</span>
              </div>
              <div class="log_out">
                <img src="@/imgs/退出.svg" alt="退出" @click="toLogout" />
              </div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="1" :sm="1" :lg="3" class="white"></el-col>
      <el-col :xs="16" :sm="16" :lg="12" class="chat_container">
        <div
          class="chat_box"
          ref="chatMessages"
          v-loading="videoLoading"
          element-loading-text="正在进行语音生成..."
          element-loading-spinner="el-icon-loading"
        >
          <div v-for="(item, index) in messages" :key="index">
            <br />
            <div class="userChat" v-show="item.question">
              <img src="@/imgs/用户头像.png" class="chatImg_user" />
              <span>{{ item.question }}</span>
            </div>
            <br />
            <div class="botChat">
              <img src="@/imgs/机器人.png" class="chatImg_bot" />
              <Loadding
                class="loadding"
                v-if="loadding && index == messages.length - 1"
              />
              <div v-if="isImage(item.answer).includes('llm_img')">
                <span v-if="isImage(item.answer).includes('other')"
                  >抱歉,暂时无法为您生成该图片</span
                >
                <img
                  :src="require('../assets' + isImage(item.answer))"
                  v-if="!isImage(item.answer).includes('other')"
                  class="answer_image"
                />
              </div>
              <vue-markdown
              v-show="!isImage(item.answer).includes('llm_img')"
              class="bot_response"
              :source="item.answer"
              v-if="isVisible" />
              <span v-show="!isImage(item.answer).includes('llm_img')" class="bot_response" v-html=(item.answer) v-if="!isVisible"></span>
              <div v-show="!loadding" class="chat_icon">
                <img
                  src="@/imgs/删除.png"
                  @click="delChatHistory(item)"
                  v-if="talk_id != 'exam' && talk_id != 'v'"
                />
                <img
                  src="@/imgs/文本转语音.svg"
                  @click="toTTS(item)"
                  v-if="!isImage(item.answer).includes('llm_img')"
                />
              </div>
            </div>
            <audio controls class="tts" :src="item.audio" v-if="item.audio">
              Your browser does not support the audio element.
            </audio>
            <div class="source">
              <div
                v-show="item.source[0]"
                v-for="(source, index) in item.source"
                :key="index"
              >
                出处 [{{ index + 1 }}]:<a
                  target="_blank"
                  @click="toSource(source)"
                  >{{ source.title }}</a
                >
              </div>
            </div>
          </div>
        </div>
        <div class="user-input">
          <el-button @click="toSpeech" class="speech_btn">
            {{ isRecording ? "录音中..." : "开始录音" }}</el-button
          >
          <input
            type="text"
            v-model="newMessage"
            class="message-input"
            placeholder="Type your message..."
            @keyup.enter="sendMessage"
          />
          <img
            src="@/imgs/发送1.svg"
            alt="发送"
            v-if="!newMessage || !this.$route.params.talk_id"
            style="position: absolute; width: 30px; height: 30px; right: 25px"
          />
          <img
            src="@/imgs/发送2.svg"
            alt="发送"
            v-if="newMessage && this.$route.params.talk_id"
            @click="sendMessage"
            style="position: absolute; width: 30px; height: 30px; right: 25px"
          />
        </div>
      </el-col>
      <el-col :xs="1" :sm="1" :lg="5" class="human">
        <DigitalMan />
      </el-col>
    </el-row>
    <el-dialog
      title="登录后开始畅聊!"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="账号">
          <el-input v-model="form.username" placeholder="请输入账号"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            placeholder="请输入密码"
            show-password
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="toLogin">登 录</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import DigitalMan from "./DigitalMan.vue";
import Loadding from "./loadding.vue";
import Vue from "vue";
import VueMarkdown from "vue-markdown";
import Recorder from "js-audio-recorder";


export const EventBus = new Vue();

export default {
  name: "Main",
  components: {
    DigitalMan,
    Loadding,
    VueMarkdown,
  },
  created() {
    this.recorder = new Recorder();
  },
  data() {
    return {
      chat_history: [],
      agent: [
        {
          icon: require("@/imgs/心理.svg"),
          title: "小V",
          talk_id: "v",
        },
        {
          icon: require("@/imgs/考试.svg"),
          title: "模式识别课程小助手",
          talk_id: "exam",
        },
      ],
      showAgents: false,
      messages: [],
      newMessage: "",
      timer: 0,
      isLogin: false,
      dialogVisible: false,
      form: {
        username: "",
        password: "",
      },
      moreIcon: require("@/imgs/展开.png"),
      loadding: false,
      isFinishChat: false,
      videoLoading: false,
      isRecording: false,
      talk_id:"",
      //控制是否使用markdown
      isVisible:true
    };
  },
  mounted() {
    if (
      localStorage.getItem("username") == "admin" &&
      localStorage.getItem("password") == "123456"
    ) {
      this.isLogin = true;
      this.get_history();
    }
  },
  methods: {
    togglespan(isVisible){
      if(isVisible){
        this.isVisible=true
      }
      else{
        this.isVisible=false
      }
    },
    async typeset(){
      //1.去除空格
      //特殊符号相邻要加{}^\infty   ^{z-1}这个就不是了 更新版本就好了
      //{{}}这样的情况怎么办 fastapi处理
      // window.MathJax.typesetPromise()
        if(window.MathJax){
          window.MathJax.startup.promise.then(()=>{
            window.MathJax.typesetPromise([document.getElementsByClassName("bot_response")])

          })
        }
    },
    async toSpeech() {
      if (!this.isRecording) {
        this.recorder = new Recorder();
        Recorder.getPermission().then(
          () => {
            console.log("开始录音");
            this.recorder.start(); // 开始录音
            this.isRecording = true;
          },
          (error) => {
            this.$message({
              message: "请先允许该网页使用麦克风",
              type: "info",
            });
            console.log(`${error.name} : ${error.message}`);
          }
        );
      } else {
        const formData = new FormData();
        const blob = this.recorder.getWAVBlob(); // 获取wav格式音频数据
        // 此处获取到blob对象后需要设置fileName满足当前项目上传需求，其它项目可直接传把blob作为file塞入formData
        const newbolb = new Blob([blob], { type: "audio/wav" });
        const fileOfBlob = new File([newbolb], "demo" + ".wav");
        formData.append("file", fileOfBlob);
        const url = "llmapi/whisper";

        await axios.post(url, formData).then((res) => {
          this.newMessage = res.data;
          console.log("停止录音");
          this.recorder.stop();
          this.isRecording = false;
        });
      }
    },
    isImage(answer) {
      let isImg = answer.split(".")[1] == "jpg";
      if (isImg) {
        answer = answer.split("assets")[1].replace("\\", "/");
        return answer;
      } else {
        return answer;
      }
    },
    toSource(source) {
      // console.log(source)
      window.open("http://localhost:8080/" + source.link);
    },
    toTTS(item) {
      this.videoLoading = true;
      const tts_url = "llmapi/tts";
      axios
        .post(
          tts_url,
          {
            content: item.answer,
          },
          { responseType: "blob" }
        )
        .then((res) => {
          item.audio = window.URL.createObjectURL(res.data);
          this.videoLoading = false;
          console.log(item);
        });
    },
    async agentChat(item) {
      if (this.$route.params.talk_id == item.talk_id) {
        return;
      }

      this.$router.push({
        path: `/chat/${item.talk_id}`,
      });

      this.messages = [];
      this.talk_id = item.talk_id
      if(item.talk_id === "exam"){
        this.messages=[{
        question: "",
        answer: "将地址改为 http://localhost:8080/kg 可进入模式识别学习闯关地图",
      }];
      }
    },
    async sendMessage() {
      if (!this.$route.params.talk_id){
        this.$message({
              type: 'error',
              message: `请先创建对话框`
            });
        return;
      }
      if (this.isLogin == false) {
        this.toLogin();
        return;
      }
      this.loadding = true;
      this.messages.push({
        question: this.newMessage,
        answer: "",
        source: [],
        audio: "",
      });
      this.newMessage = "";
      this.$nextTick(() => {
        let chatMessages = this.$refs.chatMessages;
        chatMessages.scrollTop = chatMessages.scrollHeight;
      });
      let url = "";
      if (this.$route.params.talk_id == "exam") {
        url = "llmapi/send_exam_question";
      } else if (this.$route.params.talk_id == "v") {
        url = "llmapi/send_emo_question";
      } else {
        url = "llmapi/send_question";
      }

      this.timer = 0;
      EventBus.$emit("timerValue", this.timer);
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          // 发送的信息
          content: this.messages[this.messages.length - 1].question,
        }),
      });

      const reader = res.body.getReader();
      const textDecoder = new TextDecoder();
      let result = true;

      this.loadding = false;
      while (result) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }
        // 接收到的信息
        let str = textDecoder.decode(value);
        if (/llm_img/.test(str)) {
          str = str.replace('"', "").replace('"', "");
        }
        console.log(str);
        this.messages[this.messages.length - 1].answer += str;
        //出现多次渲染的情况 使用v-html来进行处理
        this.typeset()

        this.$nextTick(() => {
        let chatMessages = this.$refs.chatMessages;
        chatMessages.scrollTop = chatMessages.scrollHeight;
      });
      }

      console.log(this.messages[this.messages.length - 1].answer)
      this.timer = 2;
      EventBus.$emit("timerValue", this.timer);

      var new_qa = document.getElementById("new_qa");
      // console.log(new_qa)
      this.qaDisabled(new_qa, !this.messages[0]);

      if (
        this.$route.params.talk_id != "exam" &&
        this.$route.params.talk_id != "v" &&
        this.$route.params.talk_id != "math"
      ) {
        if (this.messages.length === 1) {
          const summarize_url = "llmapi/summarize";
          const data = {
            question: this.messages[this.messages.length - 1].question,
            answer: this.messages[this.messages.length - 1].answer,
          };
          // 将问答存入数据库
          axios.post(summarize_url, data).then((res) => {
            const message = res.data;
            const currentTime = new Date().toLocaleTimeString(); // 获取当前时间
            const currentyear = new Date().toLocaleDateString();
            const currentalltime = currentyear + " " + currentTime;
            const add_history_url = "history/add_history";
            const history_data = {
              talk_id: this.$route.params.talk_id,
              talk_time: currentalltime,
              question: this.messages[this.messages.length - 1].question,
              answer: this.messages[this.messages.length - 1].answer,
              message: message,
            };
            // console.log(history_data)
            axios.post(add_history_url, history_data).then((res) => {
              this.messages[this.messages.length - 1].id = res.data.id
              this.chat_history[0].message = message;
            });
          });
        } else {
          const currentTime = new Date().toLocaleTimeString(); // 获取当前时间
          const currentyear = new Date().toLocaleDateString();
          const currentalltime = currentyear + " " + currentTime;
          const add_history_url = "history/add_history";
          const history_data = {
            talk_id: this.$route.params.talk_id,
            talk_time: currentalltime,
            question: this.messages[this.messages.length - 1].question,
            answer: this.messages[this.messages.length - 1].answer,
            message: "",
          };
          axios.post(add_history_url, history_data).then((res) => {
            this.messages[this.messages.length - 1].id = res.data.id
            this.$nextTick(() => {
              let chatMessages = this.$refs.chatMessages;
              chatMessages.scrollTop = chatMessages.scrollHeight;
            });
          });
        }

        // 得到答案的来源
        const source_url = "llmapi/get_source";
        axios
          .post(source_url)
          .then((res) => {
            // console.log(res.data);
            let source = res.data.map((item) => {
              if (item.link.includes("/public/static/")) {
                return {
                  link: item.link.split("public/")[1].replace(".md",".pdf"),
                  title: item.title.replace(".md",".pdf")
                };
              } else {
                return item;
              }
            });
            this.messages[this.messages.length - 1].source = source;
            // console.log(this.messages[this.messages.length - 1].source);
          })
          .catch((error) => {
            console.log(error);
          });

        this.$nextTick(() => {
          let chatMessages = this.$refs.chatMessages;
          chatMessages.scrollTop = chatMessages.scrollHeight;
        });
      }
    },
    // 删除整个聊天记录
    deleteHistory(data) {
      const del_chat_url = `history/delete_history/${data.talk_id}`;
      axios.delete(del_chat_url).then((_) => {
        this.$message({
          message: "删除成功",
          type: "success",
        });
        window.location.reload();
      });
    },
    // 摘要重命名
    renameSummarize(item) {
      console.log(item);
      this.$prompt("修改名称", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^.{0,10}$/,
        inputErrorMessage: "最大长度为10",
      }).then(({ value }) => {
        console.log(value);
        const rename_url = "history/rename_chat";
        axios
          .post(rename_url, {
            id: item.id,
            message: value,
          })
          .then((_) => {
            this.$message({
              type: "success",
              message: `修改名称为 ${value} 成功`,
            });
            window.location.reload();
          });
      });
    },
    chatCopy(answer) {
      navigator.clipboard
        .writeText(answer)
        .then(() => {
          this.$message({
            message: "复制成功",
            type: "success",
          });
        })
        .catch((err) => {
          console.error("复制失败: ", err);
        });
    },
    // 对话界面中点击删除按钮触发的删除单个对话聊天
    delChatHistory(data) {
      const del_chat_url = `history/delete_chat/${data.id}`;
      axios.delete(del_chat_url).then((_) => {
        this.$message({
          message: "删除成功",
          type: "success",
        });
      });
      this.messages = this.messages.filter((item) => item.id != data.id);

      // this.get_history();
    },
    get_history() {
      const history_url = "http://127.0.0.1:7090/get_history";
      axios.get(history_url).then((res) => {
        // console.log(res.data);
        // 用于存储新数组的变量
        const history_list = [];
        // 用于跟踪已经添加到新数组中的talk_id的哈希表
        const addedTalkIds = {};

        // 遍历原始数组
        res.data.forEach((item) => {
          // 检查当前元素的talk_id是否已经存在于哈希表中
          if (!addedTalkIds[item.talk_id]) {
            // 如果不存在，将其添加到新数组中
            history_list.push(item);
            // 并将talk_id添加到哈希表中
            addedTalkIds[item.talk_id] = true;
          }
        });

        // console.log(history_list);
        // 得到所有的聊天记录
        this.chat_history = history_list;

        // 进入最后一个聊天记录面板
        const talk_id = this.chat_history[0].talk_id;
        if (this.$route.params.talk_id == talk_id) {
          this.messages = res.data.filter(
            (item) => item.talk_id == this.$route.params.talk_id
          );
          console.log(this.messages);
          return;
        } else {
          this.$router.push({
            path: `/chat/${talk_id}`,
          });
          this.messages = res.data.filter(
            (item) => item.talk_id == this.$route.params.talk_id
          );
          console.log(this.messages);
        }
      });
    },
    addQA() {
      this.messages = [];
      const currentTime = new Date().toLocaleTimeString(); // 获取当前时间
      const currentyear = new Date().toLocaleDateString();
      const currentalltime = currentyear + " " + currentTime;
      // console.log(this.chat_history[0])
      if (!this.chat_history[0]) {
        this.chat_history.unshift({
          message: "未命名对话",
          talk_time: currentalltime,
          question: "",
          answer: "",
          talk_id: 1,
          id: 1,
        });
      } else {
        this.chat_history.unshift({
          message: "未命名对话",
          talk_time: currentalltime,
          question: "",
          answer: "",
          talk_id: this.chat_history[0].talk_id + 1,
          id: this.chat_history[0].id + 1,
        });
      }
      console.log(this.chat_history);
      var new_qa = document.getElementById("new_qa");
      // console.log(new_qa)
      this.qaDisabled(new_qa, !this.messages[0]);
      // console.log(this.chat_history)
      this.$router.push({
        path: `/chat/${this.chat_history[0].talk_id}`,
      });
    },
    // 用于判断新增对话是否禁用
    qaDisabled(divElement, shouldDisable) {
      if (shouldDisable) {
        divElement.classList.add("disabled");
      } else {
        divElement.classList.remove("disabled");
      }
    },
    selectAgent() {
      this.showAgents = !this.showAgents;
      if (this.showAgents == false) {
        this.moreIcon = require("@/imgs/展开.png");
      } else {
        this.moreIcon = require("@/imgs/展开2.png");
      }
    },

    handleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },
    toLogin() {
      if (this.dialogVisible == true) {
        if (this.form.username == "admin" && this.form.password == "123456") {
          this.$message({
            message: "登录成功!",
            type: "success",
          });
          this.isLogin = true;
          this.dialogVisible = false;
          localStorage.setItem("username", this.form.username);
          localStorage.setItem("password", this.form.password);
          this.get_history();
          return;
        } else {
          this.$message({
            message: "登录失败,请输入正确的账号和密码",
            type: "error",
          });
        }
      }
      if (this.dialogVisible == false) {
        this.dialogVisible = true;
      }
    },
    toLogout() {
      localStorage.removeItem("username", this.form.username);
      localStorage.removeItem("password", this.form.password);
      this.$router.push({
        path: `/chat`,
      });
      window.location.reload();
    },
    click_history(item) {
      if (this.$route.params.talk_id == item.talk_id) {
        return;
      } else {
        this.$router.push({
          path: `/chat/${item.talk_id}`,
        });
        this.talk_id = item.talk_id
        axios.get("http://127.0.0.1:7090/get_history").then((res) => {
          this.messages = res.data.filter(
            (item) => item.talk_id == this.$route.params.talk_id
          );
        });
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.white {
  height: 30px;
}

.main {
  background-color: rgb(249, 250, 251);
}
.history {
  position: relative;
  min-height: 100vh; /* 确保容器至少为视口的高度 */
  border-right: 0.5px solid rgba(0, 0, 0, 0.08);
  overflow: hidden;
  background-color: #f3f4f6;
}
.new_qa {
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 0 22px;
}
.qa_button {
  border-radius: 10px;
  width: 100%;
  height: 44px;
  display: flex;
  align-items: center;
  background-color: rgb(229, 235, 247);
  border: 0.5px solid rgba(0, 102, 255, 0.15);
  color: #0057ff;
  cursor: pointer;
  border-radius: 12px;
}
.qa_button span {
  font-size: 16px;
  font-weight: 800;
}
.qa_button img {
  height: 20px;
  width: 20px;
  margin-left: 20px;
  margin-right: 10px;
}
.doubao {
  display: flex;
  align-items: center;
  font-weight: 600;
  font-size: 18px;
  padding-top: 10px;
  padding-bottom: 10px;
  height: 44px;
  line-height: 44px;
  border-radius: 10px;
  margin-right: 10px;
  margin-left: 10px;
  cursor: pointer;
}
.doubao img {
  height: 25px;
  width: 25px;
  /* border-radius: 50%; */
  margin-left: 16px;
  padding-right: 8px;
  object-fit: fill;
}
.doubao:hover {
  background-color: rgb(233, 234, 236);
}
.doubao:focus {
  font-weight: 600;
  color: #05f;
}

.activate {
  background-color: rgb(240, 246, 255);
}
.find_agent {
  display: flex;
  align-items: center; /* 垂直居中 */
  font-weight: 600;
  font-size: 18px;
  padding-top: 10px;
  padding-bottom: 10px;
  height: 44px;
  border-radius: 10px;
  margin-right: 10px;
  margin-left: 10px;
  cursor: pointer;
}
.zhuangshi {
  height: 25px;
  width: 25px;
  margin-left: 16px;
}
.agent {
  margin-left: 8px;
}
.find_agent:hover {
  background-color: rgb(233, 234, 236);
}
.find_agent:focus {
  color: #05f;
  font-weight: 600;
}
.show_more_agent {
  width: 20px;
  height: 20px;
  position: absolute;
  right: 20px;
}

.login {
  position: absolute;
  bottom: 20px;
  width: 90%;
  margin-left: 14px;
  margin-bottom: 10px;
}
.login_button {
  width: 100%;
  border-radius: 10px;
}

.agent_title {
  display: flex;
  align-items: center;
  height: 40px;
  line-height: 40px;
  margin-left: 16px;
  margin-right: 10px;
  border-radius: 20px;
  cursor: pointer;
  color: rgba(0, 0, 0, 0.5);
  font-size: 18px;
}
.agent_title img {
  height: 25px;
  width: 25px;
  margin-left: 10px;
  margin-right: 10px;
}
.agent {
  width: 100px;
}
.agent_title:hover {
  background-color: rgb(233, 234, 236);
}
.agent_title:focus {
  color: #05f;
}
.chat_container {
  background-color: rgb(249, 250, 251);
}
.chat_box {
  width: 1000px;
  height: 90vh;
  margin: 0px auto;
  overflow-y: scroll;
  scrollbar-width: none;
  margin-top: 10px;
  font-size: 18px;
}
.user-input {
  padding: 10px;
  display: flex;
  align-items: center;
  position: relative;
}
.user-input img {
  height: 50px;
  width: 50px;
  cursor: pointer;
}
.message-input {
  flex-grow: 1;
  padding: 20px 35px;
  border-radius: 20px;
}
.userChat {
  display: flex;
  width: 100%;
}
.userChat span {
  background-color: rgb(210, 249, 209);
  height: 100%;
  line-height: 30px;
  border-radius: 0.375rem;
  padding: 6px;
  font-size: 18px;
}
.botChat {
  display: flex;
  width: 1000px;
  /* margin-left: 10px; */
}

.botChat span {
  background-color: rgb(244, 246, 248);
  height: 100%;
  line-height: 1.5;
  border-radius: 0.375rem;
  /* padding: 6px; */
  /* width: 80%; */
}
.chatImg_user {
  width: 30px;
  height: 30px;
  padding-right: 10px;
}
.chatImg_bot {
  margin-top: 10px;
  width: 30px;
  height: 30px;
  padding-right: 10px;
}
.user_info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 10px;
}
.user_avatar {
  display: flex;
  align-items: center;
}
.user_more {
  height: 60px;
  line-height: 60px;
  padding-bottom: 16px;
  margin-right: 10px;
  color: gray;
  font-size: 24px;
}
.user_more:hover {
  color: black;
}
.user_info img {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  margin-left: 10px;
}
.user_info span {
  margin-left: 10px;
  /* margin-bottom:20px; */
}
.source {
  margin-left: 10px;
  margin-top: 6px;
}
.source a {
  color: #0000ff;
  cursor: pointer;
}
.history_box {
  height: 300px;
  overflow: auto;
}
.history_chat {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 30px;
  margin: 0 22px;
  padding: 5px;
  cursor: pointer;
  border-radius: 20px;
}
.history_chat_message {
  width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.history_chat:hover {
  background-color: rgb(233, 234, 236);
}
.history_chat:focus {
  background-color: rgb(255, 255, 255);
  border: 2px solid rgb(59, 130, 246);
  border-radius: 0.5rem;
}
.history_chat img {
  height: 20px;
  width: 20px;
  cursor: pointer;
}
.log_out {
  cursor: pointer;
}
.log_out img {
  height: 30px;
  width: 30px;
}
.rename_box {
  display: flex;
  align-items: center;
  padding: 10px;
  cursor: pointer;
  border-radius: 10px;
}
.rename_box img {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}
.rename_box:hover {
  background-color: rgb(233, 234, 236);
}
.delete_box {
  display: flex;
  align-items: center;
  padding: 10px;
  cursor: pointer;
  border-radius: 10px;
}
.delete_box img {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}
.delete_box:hover {
  background-color: rgb(233, 234, 236);
}
.disabled {
  pointer-events: none; /* 禁用鼠标事件 */
  opacity: 0.5; /* 降低透明度 */
  cursor: not-allowed; /* 更改鼠标指针样式 */
}
.chat_icon img {
  width: 20px;
  height: 20px; 
  margin-top: 10px;
  padding-left: 10px;
  cursor: pointer; 
}
.tts {
  margin-top: 10px;
}
.answer_image {
  margin-top: 10px;
  width: 400px;
  height: 200px;
}
.speech_btn {
  height: 60px;
  border-radius: 20px;
  margin-right: 10px;
}
.bot_response {
  background-color: #ffffff;
  width:760px;
  padding-top:16px;
  padding-bottom: 16px;
  padding-left: 30px;
  padding-right: 20px;
  height: 100% !important;
  line-height: 1.5;
  display: inline;
}
::v-deep .v-note-wrapper {
    min-height: 30px !important;
}

::v-deep .auto-textarea-input{
  margin-top: 14px !important;
  /* height: 100% !important; */
}


</style>
