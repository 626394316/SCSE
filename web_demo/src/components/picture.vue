<template>
  <div class="pic">
    <LeftDom @select-node="getchosenode"></LeftDom>
    <!-- ECharts 图表容器 -->
    <div ref="chart" class="chat-container" ></div>
    <RightDom :sendNode="click_node" :sendmoreNode="is_hide" ></RightDom>
  </div>
</template>

<script>
import * as echarts from 'echarts'; // 引入 ECharts 库
import LeftDom from"./leftdom.vue"
import RightDom from "./rightdom.vue"
export default {
  name: 'App',
  components:{
    LeftDom,
    RightDom
  },
  data() {
    return {
      highlightedNode: "课程要求", // 当前高亮的节点，初始为根节点
      highlightedNodes:["课程要求"],
      allNodes:this.$store.state.data,
      allLinks: [],
      click_node:" ",
      //是否隐藏
      is_hide:true,
      
    };
  },
  mounted() {
    // 组件挂载后初始化图表
  this.initChart();
  },
  created(){
  this.initAllLinks()
  },
  methods: {
    initAllLinks(){
      this.allLinks = this.allNodes.reduce((links, currentNode, index, array) => {
      if (index < array.length - 1) {
        links.push({ source: currentNode.name, target: array[index + 1].name });
      }
      return links;
    }, [])
    },
    initChart() {
      // 初始化 ECharts 实例
      this.chart = echarts.init(this.$refs.chart);
      // 更新图表数据
      this.updateChart();
      // 为图表添加点击事件监听
      this.chart.on('click', this.handleChartClick);
    },
    getNodesAndLinks() {
      // 获取节点和链接的样式和数据
      const highlightedNodes = this.getHighlightedNodes(); // 获取当前需要高亮的节点
      const nodes = this.allNodes.map(node => ({
        ...node,
        itemStyle: {
          // 设置节点的样式
          color: this.getNodeColor(node.level), // 根据节点的级别设置颜色
          opacity: highlightedNodes.includes(node.name) ? 1 : 0.2 // 高亮节点不透明度为1，其余为0.2
        },
        symbolSize: 100, // 节点的大小
        label: {
          show: true // 显示节点标签
        }
      }));
      // console.log(nodes)
      const links = this.allLinks.map(link => ({
        ...link,
        lineStyle: {
          // 设置链接的样式
          opacity: highlightedNodes.includes(link.source) || highlightedNodes.includes(link.target) ? 0.5 : 0.1 // 高亮的链接不透明度为0.5，其余为0.1
        }
      }));

      return { nodes, links };
    },
  
    //点击左侧菜单节点
    getchosenode(params){
      console.log(params)
      this.handleChartClick(params)
    },
    getHighlightedNodes() {
      // 获取当前需要高亮的节点（包括路径上的节点）
      if (!this.highlightedNode) return []; // 如果没有高亮节点，返回空数组

      const highlightedNodes = new Set(); // 使用 Set 存储高亮的节点
      const nodesToCheck = [this.highlightedNode]; // 从当前高亮节点开始检查
      
      while (nodesToCheck.length) {
        const currentNode = nodesToCheck.pop(); // 取出当前节点
        highlightedNodes.add(currentNode); // 将当前节点标记为高亮

        // 查找并添加当前节点的前置节点
        this.allLinks
          .filter(link => link.target === currentNode)
          .forEach(link => {
            if (!highlightedNodes.has(link.source)) {
              nodesToCheck.push(link.source); // 将前置节点添加到待检查列表中
            }
          });
      }
      //向rightdom传递消息获得代处理节点个数
      //获取全部节点
      const existingNodes = this.allNodes.map(node => node.name); 
      //查询为点亮节点
      const uniqueHighlightedNodes = existingNodes.map(nodeName => highlightedNodes.has(nodeName));
      //统计未点亮个数
      const countFalse = uniqueHighlightedNodes.filter(isHighlighted => isHighlighted === false).length;
      //传递
      this.$store.commit("setnum",countFalse)

      return Array.from(highlightedNodes); // 将 Set 转换为数组
    },
    updateChart() {
      // 更新 ECharts 图表
      const { nodes, links } = this.getNodesAndLinks(); // 获取节点和链接的数据

      this.chart.setOption({
        title: {
          text: '模式识别闯关地图', // 图表标题
          left: 'center' // 标题位置
        },
        series: [
          {
            type: 'graph', // 图表类型为图
            layout: 'force', // 使用力导向布局
            symbolSize: 60, // 节点大小
            roam: true, // 是否允许缩放和拖拽
            label: {
              show: true, // 显示标签
              position: 'inside', // 标签位置
              fontSize: 15 // 标签字体大小
            },
            edgeSymbol: ['circle', 'arrow'], // 链接的箭头形状
            edgeSymbolSize: [4, 10], // 链接的箭头大小
            force: {
              repulsion: 1000, // 节点间的排斥力
              edgeLength: [100, 200] // 链接的长度范围
            },
            draggable: true, // 节点是否可拖拽
            data: nodes, // 节点数据
            links: links, // 链接数据
            lineStyle: {
              color: 'source', // 链接的颜色来源
              curveness: 0.3 // 链接的弯曲度
            }
          }
        ]
      });
    },
    getNodeColor(level) {
      // 根据节点的级别返回颜色
      const colors = ['#ff7f50', '#87cdfa', '#da70d6', '#32cd32'];
      return colors[level] || '#cccccc'; // 如果级别超出范围，返回灰色
    },
    handleChartClick(params) {
      console.log(params)
  if (params.dataType === 'node') {
    const clickedNode = params.data.name;
   
    //传递点击该节点消息
    this.click_node=clickedNode
    const allNodes = this.allNodes.map(node => node.name);
    const links = this.allLinks;
    if (this.highlightedNodes.includes(clickedNode)) {
        return false
      }
    // 检查前置节点是否全部点亮
    const checkPredecessors = (node) => {
      const predecessors = links
        .filter(link => link.target === node)
        .map(link => link.source);

      const allPredecessorsLit = predecessors.every(predecessor => allNodes.includes(predecessor) && this.getHighlightedNodes().includes(predecessor));
      if (!allPredecessorsLit) {
        alert('需要先学习好前面的知识哦');
        this.is_hide=!this.is_hide
        return false;
      }
      return true;
    };
  
    // 递归检查前置节点
    let currentNode = clickedNode;
    let canHighlight = true;

    while (canHighlight && currentNode) {
 
      canHighlight = checkPredecessors(currentNode);
      // 如果当前节点不是根节点，继续检查其前置节点
      if (canHighlight) {
        const parentLink = links.find(link => link.target === currentNode);
        currentNode = parentLink ? parentLink.source : null;
      }
   
    }
     //拿取数据仓库的题库数据
     const get_everycorrect=this.$store.getters.geteverycorrect
    //拿取该节点前一个节点的name值
    //取索引
    let index = this.allNodes.findIndex(function(item) {
    return item.name === clickedNode;
    });
    //取值
    const prenode_name=this.allNodes[index]

    if(get_everycorrect.find(node=>node.name==prenode_name.name)===undefined){
      alert("请将该节的测试题完成") 
        return false
        //如果还是弹出这个问题则在数据库everycorrect中加入该节点题目完成即可
    }
    if (canHighlight) {
      this.highlightedNode = clickedNode;
      if (!this.highlightedNodes.includes(clickedNode)) {
        this.highlightedNodes.push(clickedNode);
        this.updateChart();
      }
    }
  }
}
  }
};
</script>

<style>
.pic {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex; /* 使用Flexbox布局 */
  width: 100%; /* 容器宽度设置为100% */
  height: 100vh; /* 容器高度占满视口高度 */
  
}
.chat-container {
  flex: 4;
  margin-top:30px;
}
</style>
