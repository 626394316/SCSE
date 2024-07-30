// 导入 vue
import Vue from 'vue'
// 导入 vuex
import Vuex from 'vuex'
// vuex也是vue的插件, 需要use一下, 进行插件的安装初始化
Vue.use(Vuex)

// 创建仓库 store
const store = new Vuex.Store({
    actions:{
        set_num({commit},num){
            commit("setnum",num)
        },
        set_everycorrect({commit},cho_name){
            commit("seteverycorrect",cho_name)
        }

    },
    mutations:{
        setnum(state,num){
            state.deal_num=num
        },
        seteverycorrect(state,cho_name){
            state.everycorrect.push(cho_name)
        }

    },
    getters:{
        gettitle:state=>{
            return state.topic
        },
        geteverycorrect:state=>{
            return state.everycorrect
        }
    },
    state:{
        data:[
            // 定义所有节点的信息
            // Level 0: 基础知识节点
            { name: '课程要求', level: 0 },
            { name: '学习要点', level: 0 },
            { name: '模式识别预备知识', level: 0 },
            { name: '模式识别相关学科',  level: 0 },
            { name: '模式识别相关教材', level: 0 },
            // Level 1: 进阶知识节点
            { name: '模式识别的基本概念', level: 1 },
            { name: '什么是模式',  level: 1 },
            { name: '什么是识别',  level: 1 },
            { name: '什么是样本',  level: 1 },
            { name: '什么是特征',  level: 1 },
            { name: '什么是类别',  level: 1 },
            { name: '什么是特征提取',  level: 1 },
            { name: '什么是特征选择',  level: 1 },
            { name: '什么是特征向量表示法',  level: 1 },
            { name: '什么是分类决策',  level: 1 },
            { name: '什么是训练',  level: 1 },
            // Level 2: 高级应用节点
            { name:"如何学习大模型", level: 2 },
            { name:"如何学习RAG", level: 2 },
            { name:"如何微调大模型", level: 2 },
        ],

        title:[
            {name:"基础知识",level:0},
            {name:"进阶知识",level:1},
            {name:"高级应用",level:2},

        ],
        //题目翻译
        topic:[
            {
                name:"课程要求",
                content:`
                本课程的考核要求为：\n
                平时成绩（考勤、作业、实验报告） 30%;\n
                期末考试 70%;
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"学习要点",
                content:`
                重点掌握模式识别的基本概念，基本方法和算法原理。

                注重理论与实践紧密结合，注意如何将所学知识运用到实际应用之中

                为研究新的模式识别的理论和方法打下基础

                不要被繁琐的数学推导吓倒

                基本要求：完成课程学习，通过考试，获得学分。

                提高：能够将所学知识和内容用于课题研究，解决实际问题。

                飞跃：通过模式识别的学习，改进思维方式，为将来的工作打好基础，终身受益。
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"模式识别预备知识",
                content:`
                线性代数：向量、矩阵的基本运算、逆、行列式、特征值、特征向量等；

                概率论与数理统计：概率（先验、条件）、概率密度、随机变量和分布、数学期望、全概率和贝叶斯公式、正态分布、参数估计、假设检验

                高等数学、最优化方法、信息论、程序设计基础
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"模式识别相关学科",
                content:`
                机器学习、人工智能、图像处理、计算机视觉
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"模式识别相关教材",
                content:`
                《模式分类》(第2版)，R.O.Duda等著，李宏东等译，机械工业出版社，2003年

                《模式识别》(第3版)，张学工等著，清华大学出版社，2010年

                《模式识别》（第4版），Sergios Theodoridis著，李晶皎译，电子工业出版社，2016年
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"模式识别的基本概念",
                content:`
                模式识别是指对表征事物或现象的各种形式的(数值的、文字的和逻辑关系的)信息进行处理和分析，以对事物或现象进行描述、辨认、分类和解释的过程，是信息科学和人工智能的重要组成部分。
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"什么是模式",
                content:`
                广义地说，存在于时间和空间中可观察的物体，如果我们可以区别它们是否相同或是否相似，都可以称之为模式。

                模式所指的不是事物本身，而是从事物获得的信息，因此，模式往往表现为具有时间和空间分布的信息。

                模式的直观特性：可观察性、可区分性、相似性
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"什么是识别",
                content:`
                把具体的样本归类到某一个模式，可以叫做模式的识别（或分类）。识别是时时刻刻都在发生的；识别（Recognition)是再认知的过程；

                识别行为：识别具体事物和抽象事物
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"什么是样本",
                content:`
                样本是研究对象的个体，样本集
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"什么是特征",
                content:`
                特征是表征样本的观测，是指用于描述模式性质(特性)的一种定量概念。例如苹果的大小、颜色、味道
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"什么是类别",
                content:`
                类别是具有某些公共特性(模式)样本的集合
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"什么是特征提取",
                content:`
                特征提取是指采用映射（或变换）实现由模式测量空间向特征空间的转变或者将特征空间的维数从高维变成低维。
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"什么是特征选择",
                content:`
                特征选择是指从一组中挑选最有效的特征以降低维数。
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"什么是特征向量表示法",
                content:`
                印刷体数字图像往往用一个N×M的数组表示。如果N＝5，M＝7，则一个数字就用5×7共35个网格是黑是白来表示。

                如令是黑为“1”，是白为“0”，那么一个数字就可用35维的二进制向量表示。这就是典型的特征向量表示法。
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"什么是分类决策",
                content:`
                分类决策是指对待分类样本进行决策的过程
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"什么是训练",
                content:`
                训练是依据特征空间的分布，决定分类器的具体参数。一般说来采用什么样式的决策分界由设计者决定，如可用直线、折线或曲

                线作为类别的分界线。分界线的类型可由设计者直接确定，也可通过训练过程产生，但是这些分界线的具体参数则利用训练样本经训练过程确定。
                `,
                subject:[],
                videoUrl:""
            },
            {
                name:"如何学习大模型",
                content:`
                大模型已经成为了发展通用人工智能的重要途径，从从前的一个任务一个专用模型逐渐向能够同时解决多模态任务的通用大模型演变。
                为此，书生蒲语大模型进行了开发并开源。
                与此同时，书生实战营为广大想要学习大模型的用户提供了学习资料，可以大大的帮助用户快速入门。
                `,
                subject:[{
                    question:"如何学习大模型",
                    answer:"参加书生浦语大模型实战营"
                }],
                videoUrl:"https://www.bilibili.com/video/BV1Vx421X72D"
            },
            {
                name:"如何学习RAG",
                content:`
                RAG（Retrieval Augmented Generation）技术，通过检索与用户输入相关的信息片段，并结合外部知识库来生成更准确、更丰富的回答。解决 LLMs 在处理知识密集型任务时可能遇到的挑战, 如幻觉、知识过时和缺乏透明、可追溯的推理过程等。提供更准确的回答、降低推理成本、实现外部记忆。
                `,
                subject:[{
                    question:"如何学习RAG",
                    answer:"参加书生浦语大模型实战营"
                }],
                videoUrl:"https://www.bilibili.com/video/BV1QA4m1F7t4"
            },
            {
                name:"如何微调大模型",
                content:`
                大模型常见的微调范式包含增量预训练微调和指令跟随微调，
                在日常的使用中，需要根据不同的大模型配置不同的指令模板才能够进行大模型的微调。
                而XTuner已经配置好了转换的脚本文件，大家只需要撰写数据集模板，就可以通过XTuner实现自动转换格式从而进行微调训练。
                `,
                subject:[{
                    question:"如何微调大模型",
                    answer:"参加书生浦语大模型实战营"
                }],
                videoUrl:"https://www.bilibili.com/video/BV15m421j78d"
            },
        ],
        deal_num:0,
        //做题标签
        everycorrect:[
            {name:"课程要求",isture:true},
            { name: '学习要点',isture:true },
            { name: '模式识别预备知识', isture:true},
            { name: '模式识别相关学科',  isture:true },
            { name: '模式识别相关教材', isture:true },
            { name: '模式识别的基本概念', isture:true },
            { name: '什么是模式',  isture:true },
            { name: '什么是识别',  isture:true },
            { name: '什么是样本',  isture:true },
            { name: '什么是特征',  isture:true },
            { name: '什么是类别',  isture:true },
            { name: '什么是特征提取',  isture:true },
            { name: '什么是特征选择',  isture:true },
            { name: '什么是特征向量表示法',  isture:true },
            { name: '什么是分类决策',  isture:true },
            { name: '什么是训练',  isture:true },
        ],
    }
})

// 导出仓库
export default store
