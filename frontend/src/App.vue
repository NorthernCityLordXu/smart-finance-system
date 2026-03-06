<template>
  <div class="dashboard-container">
    <div class="header">
      <div class="logo">✨ Smart Finance AI Dashboard</div>
      <div class="user-profile">
        <el-avatar size="small" style="background-color: #409EFF;">User</el-avatar>
        <span style="margin-left: 10px; font-weight: 500;">智能财务管家</span>
      </div>
    </div>

    <div class="main-content">
      <el-card shadow="hover" class="box-card add-record-card">
        <template #header>
          <div class="card-header">
            <span>🚀 快速记账与智能分类</span>
          </div>
        </template>
        <el-form :inline="true" :model="newRecord" class="demo-form-inline">
          <el-form-item label="账单描述">
            <el-input v-model="newRecord.description" placeholder="例如：打车回家" clearable style="width: 250px;"></el-input>
          </el-form-item>
          <el-form-item label="消费金额 (¥)">
            <el-input-number v-model="newRecord.amount" :min="0" :precision="2" :step="10" style="width: 150px;"></el-input-number>
          </el-form-item>
          <el-form-item label="初步分类">
            <el-select v-model="newRecord.category" placeholder="选择分类" style="width: 150px;">
              <el-option label="🍣 Food (餐饮)" value="Food"></el-option>
              <el-option label="🚕 Transport (交通)" value="Transport"></el-option>
              <el-option label="🛍️ Shopping (购物)" value="Shopping"></el-option>
              <el-option label="🎬 Entertainment (娱乐)" value="Entertainment"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitRecord" :loading="isSubmitting" color="#409EFF" round>
              智能入库
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-row :gutter="20" class="chart-row">
        <el-col :span="12">
          <el-card shadow="hover" class="chart-card">
            <div ref="pieChartRef" style="width: 100%; height: 350px;"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover" class="chart-card">
            <div ref="lineChartRef" style="width: 100%; height: 350px;"></div>
          </el-card>
        </el-col>
      </el-row>

      <el-card shadow="hover" class="table-card">
        <template #header>
          <div class="card-header">
            <span>📜 实时账单流水</span>
          </div>
        </template>
        
        <el-table :data="transactions" stripe style="width: 100%" height="400" v-loading="loading">
          <el-table-column prop="description" label="账单描述" width="280">
            <template #default="scope">
              <span style="font-weight: bold; color: #303133;">{{ scope.row.description }}</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="category" label="AI 分类标签" width="180">
            <template #default="scope">
              <el-tag :type="getTagType(scope.row.category)" effect="light" round size="large">
                {{ scope.row.category }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="amount" label="金额" width="180">
            <template #default="scope">
              <span style="color: #F56C6C; font-weight: bold; font-size: 16px;">
                ¥ {{ Number(scope.row.amount).toFixed(2) }}
              </span>
            </template>
          </el-table-column>
          
          <el-table-column prop="transactionDate" label="记录时间">
            <template #default="scope">
              <span style="color: #909399;">
                {{ scope.row.transactionDate ? scope.row.transactionDate.replace('T', ' ') : '未知时间' }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, nextTick } from 'vue';
import axios from 'axios';
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';

// 响应式状态
const transactions = ref([]);
const newRecord = ref({ description: '', amount: undefined, category: 'Food' });
const isSubmitting = ref(false);
const loading = ref(true);

// 图表 DOM 引用 (Vue 3 规范做法)
const pieChartRef = ref(null);
const lineChartRef = ref(null);
let myChart = null;
let lineChart = null;

// 获取标签颜色的方法
const getTagType = (category) => {
  const map = { 'Food': 'warning', 'Transport': 'info', 'Shopping': 'success', 'Entertainment': 'danger' };
  return map[category] || 'primary';
};

// 获取后端数据
const fetchData = async () => {
  loading.value = true;
  try {
    const response = await axios.get('http://localhost:8080/api/all');
    // 让最新添加的账单排在最前面
    transactions.value = response.data.reverse(); 
    
    await nextTick(); // 确保 DOM 更新后再渲染图表
    renderChart();      
    renderLineChart();  
  } catch (e) {
    ElMessage.error("后端服务未响应，请检查 Docker 容器状态");
  } finally {
    loading.value = false;
  }
};

// 渲染饼图
const renderChart = () => {
  const stats = {};
  transactions.value.forEach(t => {
    stats[t.category] = (stats[t.category] || 0) + t.amount;
  });

  const chartData = Object.keys(stats).map(name => ({
    name: name,
    value: stats[name].toFixed(2)
  }));

  if (!myChart) myChart = echarts.init(pieChartRef.value);

  myChart.setOption({
    title: { text: '分类支出占比', left: 'center', top: '20' },
    tooltip: { trigger: 'item', formatter: '{b}: ¥{c} ({d}%)' },
    legend: { bottom: '10' },
    series: [{
      name: '支出分类',
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '55%'],
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      data: chartData,
    }]
  });
};

// 渲染折线图
const renderLineChart = () => {
  const dailyStats = {};
  transactions.value.forEach(t => {
    const date = t.transactionDate ? t.transactionDate.substring(0, 10) : '未知';
    dailyStats[date] = (dailyStats[date] || 0) + t.amount;
  });

  const sortedDates = Object.keys(dailyStats).sort();
  const seriesData = sortedDates.map(date => dailyStats[date].toFixed(2));

  if (!lineChart) lineChart = echarts.init(lineChartRef.value);

  lineChart.setOption({
    title: { text: '每日支出趋势', left: 'center', top: '20' },
    tooltip: { trigger: 'axis' },
    xAxis: { 
      type: 'category', 
      data: sortedDates,
      axisLine: { lineStyle: { color: '#E4E7ED' } },
      axisLabel: { color: '#909399' }
    },
    yAxis: { 
      type: 'value',
      splitLine: { lineStyle: { type: 'dashed', color: '#E4E7ED' } }
    },
    grid: { left: '5%', right: '5%', bottom: '15%', containLabel: true },
    series: [{
      name: '每日支出',
      data: seriesData,
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      itemStyle: { color: '#409EFF' },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(64,158,255,0.3)' },
          { offset: 1, color: 'rgba(64,158,255,0.05)' }
        ])
      }
    }]
  });
};

// 提交新记录
const submitRecord = async () => {
  if (!newRecord.value.description || !newRecord.value.amount || !newRecord.value.category) {
    return ElMessage.warning("请填写完整的账单描述和金额！");
  }

  isSubmitting.value = true;
  try {
    const perfectDateString = new Date().toISOString().substring(0, 19);

    await axios.post('http://localhost:8080/api/add', {
      description: newRecord.value.description,
      amount: newRecord.value.amount,
      category: newRecord.value.category,
      transactionDate: perfectDateString
    });
    
    ElMessage.success("🎉 账单记录成功，AI 已完成分类入库！");
    newRecord.value = { description: '', amount: undefined, category: 'Food' };
    await fetchData(); 
  } catch (error) {
    ElMessage.error("提交失败，请检查网络连接");
  } finally {
    isSubmitting.value = false;
  }
};

// 监听窗口缩放，让图表自适应大小
const resizeCharts = () => {
  myChart?.resize();
  lineChart?.resize();
};

onMounted(() => {
  fetchData();
  window.addEventListener('resize', resizeCharts);
});

onUnmounted(() => {
  window.removeEventListener('resize', resizeCharts);
});
</script>

<style scoped>
/* 整个大屏背景 */
.dashboard-container {
  min-height: 100vh;
  background-color: #F0F2F5;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

/* 顶部黑色科技感导航栏 */
.header {
  height: 60px;
  background-color: #1F2D3D;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  color: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.logo {
  font-size: 20px;
  font-weight: bold;
  letter-spacing: 1px;
}

.user-profile {
  display: flex;
  align-items: center;
}

/* 页面主体区域 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px;
}

.card-header {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}

.add-record-card {
  margin-bottom: 25px;
  border-radius: 8px;
}

.chart-row {
  margin-bottom: 25px;
}

.chart-card {
  border-radius: 8px;
}

.table-card {
  border-radius: 8px;
}

/* 覆盖 Element Plus 默认的一些边距，让表单更好看 */
.demo-form-inline .el-form-item {
  margin-bottom: 0;
  margin-right: 20px;
}
</style>