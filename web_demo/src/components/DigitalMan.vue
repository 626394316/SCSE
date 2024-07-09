<template>
  <div id="three_model">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { EventBus } from "./main.vue";
export default {
  data() {
    return {
      user_input: null,
      fbxmodel: null,
      mixer: null,
    };
  },

  mounted() {
    this.init();

  },
  methods: {
    init() {

      // 创建场景
      const scene = new THREE.Scene();
      // 设置白色背景
      scene.background = new THREE.Color(0xF9FAFB);
      // 创建相机
      const three_id = document.getElementById("three_model");
      const camera = new THREE.PerspectiveCamera(
        // 视场角，相机能够看到的场景的角度范围
        75,
        // 视口的宽高比
        // window.innerWidth / window.innerHeight,
        (three_id.clientWidth * 1.02) / three_id.clientHeight,
        // 相机能够看到的最近距离。物体距离相机小于这个值将不被渲染。
        0.1,
        // 相机能够看到的最远距离。物体距离相机大于这个值将不被渲染。
        1000
      ); // 设置相机位置
      camera.position.set(-1, 20, 45);
      // camera.position.z = 20;

      // 创建渲染
      const renderer = new THREE.WebGLRenderer({ canvas: this.$refs.canvas });

      renderer.setSize(three_id.clientWidth, three_id.clientHeight);

      // 添加环境光 第四种光源
      const light = new THREE.HemisphereLight(0xffffff, "#333333", 2.4);
      light.position.set(0, 200, 100);
      scene.add(light);
      const shadowLight = new THREE.DirectionalLight(0xffffff);
      shadowLight.position.set(0, 20, 10);
      scene.add(shadowLight);

      // //gui
      // const gui = new GUI();
      // gui.add(light.position, "x", -1000, 1000).name("X");
      // gui.add(light.position, "y", -1000, 1000).name("y");
      // gui.add(light.position, "z", -1000, 1000).name("z");

      // 加载FBX模型
      var mixer = null; //混合器变量

      var glbmodel;
      const loader = new GLTFLoader();
      loader.load("/human.glb", (glb) => {
        glbmodel = glb;
        glbmodel.scene.scale.set(25, 25, 25);
        glbmodel.scene.position.set(0, 0, 0);
        scene.add(glbmodel.scene);
        Orgin_Animation(glbmodel);
      });

      //加载初始动画
      function Orgin_Animation(model) {
        mixer = new THREE.AnimationMixer(model.scene);
        //拿取input,用来处理输入的时候
        var inputElements = document.getElementsByTagName("input");
        var user_input = inputElements[0];

        // 获取流式输出的信息
        const IdleAction = mixer.clipAction(model.animations[1]);
        const TalkAction = mixer.clipAction(model.animations[2]);
        const LookAction = mixer.clipAction(model.animations[0]);
        // console.log(IdleAction)
        //初始动画
        IdleAction.play();
        user_input.addEventListener("click", function () {
          //动作切换
          fadeAction(IdleAction, LookAction);
        });
        user_input.addEventListener("blur", function () {
          //动作切换
          fadeAction(LookAction, IdleAction);
        });
        //问答动作切换
        accept_message(IdleAction, TalkAction);
      }

      // 实现动作平滑
      function fadeAction(curAction, newAction, outspeed = 0.5, inspeed = 0.3) {
        // 淡出当前动画
        curAction && curAction.fadeOut && curAction.fadeOut(outspeed);
        // 重置并淡入新的动画
        //动画需要重置
        newAction.reset();
        //设置权重
        newAction.setEffectiveWeight(1);
        //再进行播放
        newAction.play();
        newAction.fadeIn(inspeed);
      }
      //实现讲解动画的播放时计数器的变化
      function accept_message(curAction, newAction) {
        // 在组件创建时监听事件
        EventBus.$on("timerValue", (timerValue) => {
          // 在这里处理接收到的计时器的值
          // console.log(timerValue);
          if (timerValue == 0) {
            fadeAction(curAction, newAction, 0.4);
          } else if (timerValue == 2) {
            fadeAction(newAction, curAction);
          }
        });
      }
      //实现自适应窗口
      // onresize 事件会在窗口被调整大小时发生
      window.onresize = function () {
        // 更新摄像头
        camera.aspect = three_id.clientWidth / three_id.clientHeight;
        //   更新摄像机的投影矩阵
        camera.updateProjectionMatrix();
        //   更新渲染器
        renderer.setSize(three_id.clientWidth, three_id.clientHeight);
        //   设置渲染器的像素比
        renderer.setPixelRatio(three_id.devicePixelRatio);
      };

      // 创建动画循环
      var clock = new THREE.Clock();
      const render = () => {
        renderer.render(scene, camera);
        requestAnimationFrame(render);

        if (mixer !== null) {
          console.log();
          mixer.update(clock.getDelta());
        }
      };
      // 调用render开始动画循环
      render();
    },
  },
};
</script>

<style>
/* 添加一些样式，确保Canvas占满屏幕 */
#three_model {
  height: 80vh;
  position: absolute;
  bottom: 0;
}

</style>
