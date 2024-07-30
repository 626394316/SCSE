<template>
  <div class="right-dom">
    <!-- 初始显示的div -->
    <div class="right-box">
      <div class="initial-modules">
        <div class="module" @mouseenter="moduleHover = true" @mouseleave="moduleHover = false">
          <h3>学习进度</h3>
          <div class="notification">
            <el-progress type="circle" :percentage=pre_num></el-progress>
          </div>
        </div>
        <!-- <div class="module" @mouseenter="moduleHover = true" @mouseleave="moduleHover = false">
          <h3>点击节点获得更多信息</h3>
          <i class="el-icon-s-opportunity lightbulb"></i>
        </div> -->
      </div>

      <!-- 点击后显示的4个div -->
      <div class="move-down" v-if="showDetails">
        <div class="detail-module">
          <div class="module-item" @click="toggleDrawer('text')">
            <h3>文本概念</h3>
          </div>
          <div class="module-item" @click="toggleDrawer('video')" v-if="showvideo">
            <h3>视频讲解</h3>
          </div>
          <div class="module-item" @click="toggleDrawer('question')" v-if="showtimu">
            <h3>测试题</h3>
          </div>
          <!--:destroyOnClose="true"解决视频不能暂停问题  -->
          <!-- v-bind:title绑定标签中属性动态改变 -->
          <el-drawer v-bind:title=(drawer_title) :visible.sync="drawer" :destroyOnClose="true" :with-header="true" :style="{ whiteSpace: 'pre-wrap'}">
            <div class="drawer-content">
              <!-- v-show改善渲染功能 -->
              <p class="description" v-show="currentContent === 'text'" >{{one_node_title}}</p>
              <!-- 不用uc浏览器 -->
              <div v-if="showvideo">
                <div v-if="currentContent === 'video'" controls>
                  <iframe :src=videoUrl  width="100%" height="1000"></iframe>
                </div>
                <!-- <div class="video-box" v-show="currentContent === 'video'" controls>
                  <video-player class="video-player vjs-custom-skin" ref="videoPlayer"
                    :options="playerOptions"></video-player>
                </div> -->
              </div>
              <div v-if="showtimu">
                <div class="test-question" v-show="currentContent === 'question'">
                  <el-alert v-if="isture" title="回答正确" type="success" center effect="dark">
                  </el-alert>
                  <p class="question">{{ subject[currentQuestionIndex].question }}</p>
                  <el-pagination @current-change="handlePageChange" small layout="prev, pager, next"
                    :total="subject.length * 10" style="margin-bottom: 20px;">
                  </el-pagination>
                  <el-input type="textarea" :rows="5" placeholder="请输入你的答案" v-model="userAnswer">
                  </el-input>
                  <el-button type="primary" @click="submitAnswer" plain class="question-button">提交答案</el-button>
                </div>
                <div v-if="showAnswer" class="test-answer">
                  <el-button type="primary" icon="el-icon-circle-close" circle plain
                    @click="showAnswer = !showAnswer"></el-button>
                  <p>正确答案：{{ subject[currentQuestionIndex].answer }}</p>
                </div>
              </div>
            </div>
          </el-drawer>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'RightDom',
  data() {
    return {
      // 控制是否显示详细信息
      showDetails: false,
      moduleHover: false,
      //进度条数据
      //统计未处理个数
      deal_num: 0,
      //全部数据量
      all_num: this.$store.state.data.length,
      pre_num: 0,
      //从数据仓库里面拿取右侧数据
      node_name: "",
      all_node: [],
      one_node_title: "",
      //抽屉设置  
      //抽屉是否显示
      drawer: false,
      //抽屉内容种类
      currentContent: '',
      //抽屉title
      drawer_title: "",
      //视频
      //是否展示视频
      showvideo: false,
      playerOptions: {
        sources: [],
        // 其他设置项
        fluid: true,// 当 fluid 设置为 true 时，Video.js 播放器将拥有流体大小，即它会根据容器的尺寸动态地调整自身的大小
        notSupportedMessage: "此视频暂无法播放，请稍后再试",//提示信息
        autoplay: false,//是否自动播放
        controls: true,//是否显示控制栏
        playbackRates: [0.5, 1.0, 1.5, 2.0], // 开启倍速，不开启倍速可以写个空数组

      },
      //测试题
      //是否展示测试题
      showtimu: false,
      subject: [],
      //当前题目索引
      currentQuestionIndex: 0,
      attempts: 0, // 用户尝试次数
      showAnswer: false, // 是否显示答案
      userAnswer: '', // 用户输入的答案
      isture: false,
      // 新增变量，标记是否所有测试题都答对了
      everycorrect: [],//单个题目是否答对了
      allCorrect: false,
      videoUrl:""
    };
  },
  //监听vuex中deal_num动态变化
computed:{
  active_dealnum: {
      get() {
        return this.$store.state.deal_num;
      },
      set(val) {
        console.log(val)
      },
    },
},
  //接收点击事件
  props: ["sendNode", "sendmoreNode"],
  watch: {
    //当prop的值发生变化则改变showDetail
    sendNode(news) {
      this.showDetails = true
      this.node_name = news
      this.all_node = this.$store.getters.gettitle
     
      this.updateOneNodeTitle();
    },
    sendmoreNode(news) {
      this.showDetails = false
      console.log(news)
    },
    //监听allCorrect给picture发送消息
    allCorrect(newVal) {
      if (newVal === true) {
        // 当 allCorrect 为 true 时，执行发送逻辑
        this.sendMessageToParent();
      }
    },
    active_dealnum(newVal){
      this.deal_num=newVal
      console.log(newVal)
      this.calculatePercentage()
    }
  },
  mounted() {
    //延迟使用
    setTimeout(() => {
      this.deal_num = this.$store.state.deal_num
      console.log(this.deal_num)
      this.calculatePercentage()
    }, 100);

  },
  methods: {
    //测试题逻辑
    //题的切换
    handlePageChange(newIndex) {
      this.currentQuestionIndex = newIndex - 1;
      this.isture = false
    },
    submitAnswer() {
      if (this.userAnswer == "" & this.attempts == 0) {
        this.$message({
          message: '请输入答案',
          type: 'warning'
        });
        return
      }
      this.attempts++; // 增加尝试次数
      if (this.userAnswer === this.subject[this.currentQuestionIndex].answer) {
        this.isture = true
        this.showAnswer = false; // 隐藏答案
        this.attempts = 0; // 重置尝试次数
        //标记地点
        this.everycorrect[this.currentQuestionIndex] = true

        this.userAnswer = ""
        //判断是否全答对
        if (this.checkAllCorrect()) {
          this.$message({
            message: '恭喜你，所有问题都回答正确！',
            type: 'success'
          });
          //将每个清空
          this.everycorrect = []
          this.allCorrect = true
          this.isture = false
          return;
        }

      } else if (this.attempts >= 3) {
        this.userAnswer = ""
        this.showAnswer = true; // 显示答案
        this.attempts = 0
      }
      else {
        this.userAnswer = ""
        this.$message.error(`答案错误,您还有${3 - this.attempts}次答题机会`)
      }

    },
    // 判断everycorrect数组中的所有元素是否都为true
    checkAllCorrect() {
      // console.log(this.everycorrect.every(item => item === true))
      return this.everycorrect.every(item => item === true);
    },
    //当测试题全部回答完毕后存入数据仓库
    sendMessageToParent() {
      this.$store.dispatch("set_everycorrect", { name: this.node_name, isture: this.allCorrect })
      this.allCorrect=false


    },

    //上部分逻辑
    calculatePercentage() {
      this.pre_num = parseFloat((100-(this.deal_num / this.all_num * 100)).toFixed(2)); // 保留两位小数
    },

    //抽屉方法
    toggleDrawer(type) {
      this.drawer = true;
      this.currentContent = type;
      if (type == "text") {
        this.drawer_title = "文本概念"
      }
      else if (type == "video") {
        this.drawer_title = "视频讲解"
      } else {
        this.drawer_title = "测试题"
      }
    },
    //拿取章节对应的文本概念，视频讲解，测试题
    updateOneNodeTitle() {
      //拿取文本内容
      const matchedNode = this.all_node.find(node => node.name === this.node_name);
      console.log(matchedNode)
      //
      if (matchedNode) {
        this.one_node_title = matchedNode.content;
        this.everycorrect=matchedNode.subject.map(() => false)
        console.log(this.everycorrect)
        //拿取视频内容
        //有关于是否展示题目的判断
        //如果还有视频出现则是因为没有该节点数据
        if (matchedNode.name == "如何学习大模型" || matchedNode.name == "如何学习RAG" || matchedNode.name == "如何微调大模型") {
          this.showvideo = true
          this.videoUrl = matchedNode.videoUrl

        } else {
          this.showvideo = false
        }
        //拿取测试题
        if (matchedNode.subject.length != 0) {
          this.showtimu = true
          this.subject = matchedNode.subject
        } else {
          this.showtimu = false
        }
      }

    }
  }
};
</script>

<style scoped>
.right-dom {
  height: 100%;
  /* 这将依赖于父容器的高度 */
  top: 0;
  left: 0;
  background-color: white;
  border: 2px solid #c8e0f7;
  border-top: none;
  flex: 0 0 20%;
  /* 其他样式 */
}

.right-box {
  height: 100%;
  width: 95%;
  margin-left: 1%;
  border: 2px solid #c8e0f7;
  border-top: none;
  border-right: none;
}

.module,
.detail-module {
  margin-bottom: 20px;
  padding: 10px;
}

.initial-modules {
  display: flex;
}

.module {
  flex: 1;
  margin: 10px;
  padding: 20px;
  border-radius: 30px;
  /* 椭圆边框 */
  background-color: white;
  border: 2px solid #c8e0f7;
  /* 浅蓝色边框 */
  transition: box-shadow 0.3s, transform 0.3s;
  /* 平滑过渡效果 */
  text-align: center;
}

.module:hover,
.module[module-hover="true"] {
  border-color: #3c53bb;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 鼠标悬停时的阴影效果 */
  transform: translateY(-5px);
  /* 鼠标悬停时的按下效果 */
}



button {
  margin-top: 10px;
  padding: 5px 15px;
  border: none;
  background-color: #c8e0f7;
  /* 按钮颜色与边框颜色一致 */
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #a7c9e6;
  /* 鼠标悬停时按钮颜色变深 */
}

/* 小灯泡 */
.lightbulb {
  font-size: 30px;
  /* 根据需要调整大小 */
  color: #ffef00;
  /* 调整为更柔和的黄色 */
  background: linear-gradient(#fff, #ddd);
  /* 添加渐变背景模拟灯泡的玻璃 */
  border-radius: 50%;
  /* 圆形效果 */
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  /* 轻微的投影 */
  padding: 10px;
  /* 增加内边距以适应背景和阴影 */
  margin: 10px;
  /* 外边距以避免与其他元素重叠 */
  cursor: pointer;
  /* 鼠标悬浮时显示指针手势 */
  transition: transform 0.2s ease;
  /* 平滑过渡效果 */
}

.lightbulb:hover {
  transform: scale(1.1);
  /* 鼠标悬浮时放大 */
}

/* 3个div的形式 */
.move-down {
  height: 80%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* 水平居中 */
  margin-top: 20px;
  /* 与上一个元素的间隔 */
}

.detail-module {
  display: flex;
  height: 100%;
  width: 95%;
  flex-direction: column;
  gap: 50px;
  /* 设置子元素之间的间隔 */
}

.module-item {
  padding-top: 20%;
  height: 20%;
  width: 100%;
  border-radius: 30px;
  /* 椭圆边框 */
  border: 2px solid #c8e0f7;
  /* 浅蓝色边框 */
  transition: border 0.3s ease, transform 0.2s ease;
  /* 平滑过渡效果 */
  text-align: center;
  /* 文字居中 */
  cursor: pointer;
  /* 鼠标指针样式 */
}

.module-item:hover {
  border-color: #3c53bb;
  /* 鼠标悬停时显示边框 */
  transform: translateY(-2px);
  /* 轻微上移，制造按下效果 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 添加阴影效果 */
}

/* 抽屉样式 */
.drawer-content {
  padding: 20px;
  font-family: 'Arial', sans-serif;
  color: #333;
}


.drawer-content p.description {
  font-size: 16px;
  line-height: 1.6;
  color: #666;
}

.el-drawer__header {
  background-color: #f5f5f5;
  padding: 10px 20px;
  border-bottom: 1px solid #eee;
 
}

.el-drawer__body {
  padding: 0;
}

/* 测试题样式 */
.drawer-content {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  text-align: left;
}

.question {
  margin-bottom: 20px;
}

.question-button {
  margin-right: 30px;
  height: 50px;
}

.test-question {
  height: 400px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px;
  margin-bottom: 10px;


}

.test-answer {
  position: relative;
  height: 400px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px;
  margin-bottom: 10px;
}

.test-answer .el-button {
  position: absolute;
  top: 2%;
  /* 距离顶部0，即容器的顶部 */
  right: 2%;
  /* 距离右边0，即容器的右边 */
  /* 其他样式保持不变 */
}

.question-title,
.answer-title {
  margin-bottom: 50px;
  color: #333;
}

.question-text,
.answer-text {
  margin-bottom: 15px;
  color: #666;
}

.answer-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) inset;
}

.button-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.submit-button,
.answer-button {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button {
  background-image: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
  color: white;
}

.submit-button:hover {
  background-color: #0056b3;
}

.answer-button {
  background-image: linear-gradient(to right, #f4e2b2 0%, #d6a4a4 100%);
  color: #333;
}

.answer-button:hover {
  background-color: #5a6268;
}
</style>