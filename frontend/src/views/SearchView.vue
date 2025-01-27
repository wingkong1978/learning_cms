<template>
  <div class="page-container">
    <!-- 顶部搜索栏 -->
    <div class="search-header">
      <div class="search-bar">
        <select class="protocol-select">
          <option value="https">https</option>
          <option value="http">http</option>
        </select>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="输入关键词..."
          @input="handleSearch"
          @keyup.enter="search"
          class="search-input"
          ref="searchInput"
        />
        <button class="search-button" @click="search">
          <i class="fas fa-search"></i>
        </button>
        <button class="settings-button">
          <i class="fas fa-cog"></i>
        </button>
      </div>
    </div>

    <div class="main-content">
      <!-- 左侧导航 -->
      <div class="sidebar">
        <div class="nav-group">
          <h3>Overview</h3>
          <ul>
            <li class="active">Organic Keywords</li>
            <li>Backlink Profile</li>
            <li>Referring Domains</li>
          </ul>
        </div>
      </div>

      <!-- 主要内容区域 -->
      <div class="content">
        <div class="content-header">
          <h2>Organic Keywords <span class="help-icon">?</span></h2>
        </div>

        <!-- 过滤器 -->
        <div class="filters">
          <div class="filter-tag">
            Position: Min-1 <span class="close">×</span>
          </div>
          <div class="filter-tag">
            Volume: Min-50 <span class="close">×</span>
          </div>
          <div class="filter-dropdown">
            KD <i class="fas fa-chevron-down"></i>
          </div>
          <div class="filter-dropdown">
            CPC <i class="fas fa-chevron-down"></i>
          </div>
          <div class="filter-dropdown">
            Traffic <i class="fas fa-chevron-down"></i>
          </div>
        </div>

        <!-- 结果表格 -->
        <div class="results-table">
          <table>
            <thead>
              <tr>
                <th>Keyword</th>
                <th>Volume</th>
                <th>KD</th>
                <th>CPC</th>
                <th>Traffic</th>
                <th>Position</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="result in results" :key="result.id">
                <td>{{ result.keyword }}</td>
                <td>{{ result.volume }}</td>
                <td>{{ result.kd }}</td>
                <td>{{ result.cpc }}</td>
                <td>{{ result.traffic }}</td>
                <td class="position">{{ result.position }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'

export default {
  name: 'SearchView',
  setup() {
    const searchQuery = ref('')
    const results = ref([
      {
        id: 1,
        keyword: 'how to lose weight steadily',
        volume: '40',
        kd: '62',
        cpc: '-',
        traffic: '16',
        position: '1'
      },
      {
        id: 2,
        keyword: 'help to lose weight',
        volume: '40',
        kd: '79',
        cpc: '1.50',
        traffic: '13',
        position: '1'
      },
      {
        id: 3,
        keyword: 'ways to reduce weight',
        volume: '30',
        kd: '76',
        cpc: '-',
        traffic: '13',
        position: '1'
      }
    ])

    // 使用原生防抖函数
    let searchTimeout = null
    const handleSearch = () => {
      if (searchTimeout) {
        clearTimeout(searchTimeout)
      }
      searchTimeout = setTimeout(async () => {
        try {
          // 这里添加实际的搜索逻辑
          console.log('Searching for:', searchQuery.value)
        } catch (error) {
          console.error('Search failed:', error)
        }
      }, 300)
    }

    const search = () => {
      // 立即搜索的逻辑
      console.log('Immediate search for:', searchQuery.value)
    }

    onMounted(() => {
      const searchInput = document.querySelector('.search-input')
      if (searchInput) {
        searchInput.focus()
      }
    })

    return {
      searchQuery,
      results,
      handleSearch,
      search
    }
  }
}
</script>

<style scoped>
.page-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.search-header {
  background-color: #2c4b8c;
  padding: 10px 20px;
}

.search-bar {
  display: flex;
  gap: 10px;
  max-width: 1200px;
  margin: 0 auto;
}

.protocol-select {
  width: 100px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-button,
.settings-button {
  padding: 8px 16px;
  background: #f97316;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.main-content {
  display: flex;
  flex: 1;
  background: #f8f9fa;
}

.sidebar {
  width: 250px;
  background: white;
  padding: 20px;
  border-right: 1px solid #ddd;
}

.nav-group h3 {
  color: #666;
  margin-bottom: 10px;
}

.nav-group ul {
  list-style: none;
  padding: 0;
}

.nav-group li {
  padding: 8px 0;
  cursor: pointer;
}

.nav-group li.active {
  color: #2c4b8c;
  font-weight: bold;
}

.content {
  flex: 1;
  padding: 20px;
}

.content-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.help-icon {
  margin-left: 8px;
  color: #666;
  cursor: pointer;
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-tag {
  background: #fff;
  padding: 6px 12px;
  border-radius: 4px;
  border: 1px solid #ddd;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-tag .close {
  cursor: pointer;
  color: #666;
}

.filter-dropdown {
  padding: 6px 12px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.results-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background: #f8f9fa;
  font-weight: 500;
}

.position {
  color: #2c4b8c;
  font-weight: bold;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #ddd;
  }
}
</style> 