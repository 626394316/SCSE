<template>
  <div class="left-dom">
    <div class="left-box">
      <el-input
      class="left-input"
      placeholder="输入关键字进行过滤"
      v-model="filterText">
      </el-input>

      <el-tree
      class="filter-tree"
      :data="data"
      :props="defaultProps"
      default-expand-all
      :filter-node-method="filterNode"
       @node-click="handleNodeClick"
       :current-node-key="selectedNodelable"
      ref="tree">
      </el-tree>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeftDom',
  watch: {
      filterText(val) {
        this.$refs.tree.filter(val);
      }
    },
    methods: {
      filterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      get_data(all_data){
        // 根据 level 将 title 和 data 结合
        let new_data=[]
        const process_data=[]
        all_data.title.forEach(titleItem=>{
          const unit_data=[]
          unit_data.push(titleItem)
          const matchedDate=all_data.data.filter(dataItem=>dataItem.level === titleItem.level)
          unit_data.push(matchedDate)
          process_data.push(unit_data)
        })
        new_data=process_data.map(row=>{
          return{
            label:row[0].name,
            children: row[1].map(item => ({ // 对该行的每个元素创建子元素
              label: item.name}))
          }
        })
        return new_data
      },
      handleNodeClick(nodeData) {
      // console.log(nodeData)
      // 这里nodeData就是当前点击的节点的数据
      this.selectedNodelable = nodeData.label; // 假设每个节点都有一个唯一的ID
      // this.fetchData(nodeData.id);
      let params = {
        data : {
          name:this.selectedNodelable
        },
        dataType:"node"
      }
      this.$emit("select-node",params)
    },
    },
    data() {
      return {
        filterText: '',
        data: this.get_data(this.$store.state),
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        selectedNodelable: null,
      };
    }
}


</script>

<style scoped>
.left-dom {
  height: 100%; /* 这将依赖于父容器的高度 */ 
  top: 0;
  left: 0;
  flex: 0 0 13%;
  border: 2px solid #c8e0f7;
  border-top: none;
  background-color: #f5f5f5;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  /* 其他样式 */
}
.left-box{
  height: 100%;
  width: 95%;
  margin-left: 2%;
  border: 2px solid #c8e0f7;
  border-top: none;
  border-left:none;
  background-color: white; /* 更亮的背景色 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* 添加阴影效果 */
}
.left-input{
  width: 95%;
  margin-top: 15%;
  margin-bottom: 10%;
  
}
.filter-tree {
  width: 85%;
  margin-left: 2%;
  overflow-y: auto; /* 允许滚动 */
  margin-top: 10px;
  padding: 10px;
  border-radius: 4px; /* 圆角边框 */
  border: 1px solid #dcdfe6; /* 更细的边框 */
  

}

</style>