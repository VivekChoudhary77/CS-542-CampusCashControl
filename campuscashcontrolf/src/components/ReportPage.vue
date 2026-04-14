<template>
  <el-row justify="center" :class="['report-page-wrap', { 'is-dark': isDarkMode }]">
    <el-col :xs="24" :md="22" :lg="20">
      <el-skeleton :loading="showSkeleton" animated :rows="8">
        <template #template>
          <el-card shadow="never" class="report-card">
            <el-skeleton-item variant="h1" style="width: 38%; height: 28px;" />
            <el-skeleton-item variant="rect" style="width: 100%; height: 60px; margin-top: 16px;" />
            <el-skeleton-item variant="rect" style="width: 100%; height: 360px; margin-top: 16px;" />
          </el-card>
        </template>

        <template #default>
          <el-card shadow="hover" class="report-card" v-loading="pageLoading">
            <template #header>
              <h2>Financial Reports</h2>
            </template>

            <el-row :gutter="14" class="filters">
              <el-col :xs="24" :md="8">
                <el-form-item label="Department">
                  <el-select v-model="filters.department" class="full-width">
                    <el-option label="All Departments" value="all_departments" />
                    <el-option v-for="dept in departments" :key="dept" :label="dept" :value="dept" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :md="8">
                <el-form-item label="Month">
                  <el-select v-model="filters.month" class="full-width">
                    <el-option label="All Months" value="all_months" />
                    <el-option v-for="month in months" :key="month" :label="month" :value="month" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :md="8">
                <el-form-item label="Financial Year">
                  <el-select v-model="filters.year" class="full-width">
                    <el-option label="All Years" value="all_years" />
                    <el-option v-for="yr in years" :key="yr" :label="String(yr)" :value="yr" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <div class="actions">
              <el-button type="primary" :loading="tableLoading" @click="displayReport">
                <el-icon><Search /></el-icon>
                Display Report
              </el-button>
              <el-button @click="downloadReport" :disabled="!displayedData.length">
                <el-icon><Download /></el-icon>
                Download Report
              </el-button>
            </div>

            <div v-if="displayedData.length" class="toolbar">
              <el-input v-model="searchQuery" placeholder="Search reports" clearable class="search-input" />
              <el-tag type="info">{{ filteredReportData.length }} records found</el-tag>
            </div>

            <el-alert
              v-if="!hasSearched"
              type="info"
              :closable="false"
              show-icon
              title="Please select filter criteria and click Display Report to view financial data."
            />

            <div v-if="hasSearched" v-loading="tableLoading" class="report-table-wrap">
              <el-table
                v-if="displayedData.length"
                :data="paginatedReportData"
                stripe
                border
                @sort-change="handleSortChange"
                class="report-table"
              >
                <el-table-column prop="department" label="Department" sortable="custom" min-width="170" />
                <el-table-column prop="item" label="Item" sortable="custom" min-width="210" />
                <el-table-column prop="revenue" label="Revenue" sortable="custom" min-width="140">
                  <template #default="scope">${{ Number(scope.row.revenue).toLocaleString() }}</template>
                </el-table-column>
                <el-table-column prop="month" label="Month" sortable="custom" min-width="130" />
                <el-table-column prop="year" label="Financial Year" sortable="custom" min-width="130" />
              </el-table>

              <el-alert
                v-if="!tableLoading && !displayedData.length"
                type="warning"
                :closable="false"
                show-icon
                title="No records found for the selected criteria."
                class="empty-alert"
              />
            </div>

            <div v-if="displayedData.length && totalPages > 1" class="pagination-wrap">
              <el-pagination
                background
                layout="prev, pager, next"
                :total="filteredReportData.length"
                :current-page="currentPage"
                :page-size="itemsPerPage"
                @current-change="currentPage = $event"
              />
            </div>
          </el-card>
        </template>
      </el-skeleton>
    </el-col>
  </el-row>
</template>

<script>
import axios from "axios";
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";
import { ElNotification } from "element-plus";
import { Search, Download } from "@element-plus/icons-vue";
import { themeState } from "@/state/themeState";
import { apiUrl } from "@/config/api";

export default {
  name: "ReportPage",
  components: {
    Search,
    Download,
  },
  data() {
    return {
      showSkeleton: true,
      pageLoading: false,
      tableLoading: false,
      hasSearched: false,
      displayedData: [],
      filters: {
        department: "all_departments",
        month: "all_months",
        year: "all_years",
      },
      searchQuery: "",
      currentSort: null,
      currentSortDir: "asc",
      currentPage: 1,
      itemsPerPage: 10,
      departments: [],
      months: [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
      ],
      years: Array.from({ length: 2027 - 2023 + 1 }, (_, i) => 2023 + i),
    };
  },
  computed: {
    isDarkMode() {
      return themeState.isDarkMode;
    },
    filteredReportData() {
      let res = this.displayedData.slice();

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        res = res.filter((r) =>
          r.department.toLowerCase().includes(q) ||
          r.item.toLowerCase().includes(q) ||
          String(r.revenue).includes(q) ||
          r.month.toLowerCase().includes(q) ||
          String(r.year).includes(q)
        );
      }

      if (!this.currentSort) return res;

      const dir = this.currentSortDir === "asc" ? 1 : -1;
      return res.slice().sort((a, b) => {
        if (this.currentSort === "month") {
          const iA = this.months.indexOf(a.month);
          const iB = this.months.indexOf(b.month);
          return (iA - iB) * dir;
        }
        if (this.currentSort === "revenue") return (a.revenue - b.revenue) * dir;
        if (this.currentSort === "year") return (a.year - b.year) * dir;
        return String(a[this.currentSort]).localeCompare(String(b[this.currentSort])) * dir;
      });
    },
    totalPages() {
      return Math.ceil(this.filteredReportData.length / this.itemsPerPage);
    },
    paginatedReportData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredReportData.slice(start, start + this.itemsPerPage);
    },
  },
  methods: {
    displayReport() {
      this.hasSearched = true;
      this.tableLoading = true;
      ElNotification({
        title: "Loading",
        message: "Fetching report data...",
        type: "info",
      });
      axios
        .get(apiUrl("/reports/"), { params: this.filters })
        .then(({ data }) => {
          this.displayedData = data;
          this.currentPage = 1;
        })
        .catch((err) => {
          console.error(err);
          ElNotification({
            title: "Fetch failed",
            message: "Error fetching report data.",
            type: "error",
          });
        })
        .finally(() => {
          this.tableLoading = false;
        });
    },
    downloadReport() {
      const rows = this.filteredReportData.map((r) => ({
        Department: r.department,
        Item: r.item,
        Revenue: r.revenue,
        Month: r.month,
        Year: r.year,
      }));

      const ws = XLSX.utils.json_to_sheet(rows);
      ws["!cols"] = [{ wch: 25 }, { wch: 30 }, { wch: 15 }, { wch: 12 }, { wch: 10 }];
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Report");
      const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
      saveAs(new Blob([wbout], { type: "application/octet-stream" }), "financial_report.xlsx");
      ElNotification({
        title: "Download ready",
        message: "Report downloaded.",
        type: "primary",
      });
    },
    handleSortChange({ prop, order }) {
      if (!order) {
        this.currentSort = null;
        return;
      }
      this.currentSort = prop;
      this.currentSortDir = order === "ascending" ? "asc" : "desc";
    },
  },
  mounted() {
    this.pageLoading = true;
    axios
      .get(apiUrl("/departments/active/"))
      .then(({ data }) => {
        this.departments = data.map((d) => d.name);
      })
      .catch((err) => {
        console.error("Could not load departments:", err);
      })
      .finally(() => {
        this.pageLoading = false;
      });

    setTimeout(() => {
      this.showSkeleton = false;
    }, 360);
  },
  watch: {
    searchQuery() {
      this.currentPage = 1;
    },
  },
};
</script>

<style scoped>
.report-page-wrap.is-dark :deep(.el-card) {
  background: linear-gradient(160deg, rgba(11, 15, 24, 0.68), rgba(11, 15, 24, 0.82));
  border-color: rgba(166, 188, 216, 0.24);
}

.report-page-wrap.is-dark :deep(.el-form-item__label) {
  color: #d4e0f1;
}

.report-page-wrap.is-dark :deep(.el-input__wrapper),
.report-page-wrap.is-dark :deep(.el-select__wrapper) {
  background: rgba(10, 14, 22, 0.74);
  box-shadow: 0 0 0 1px rgba(166, 188, 216, 0.3) inset;
}

.report-page-wrap.is-dark :deep(.el-input__inner),
.report-page-wrap.is-dark :deep(.el-select__placeholder),
.report-page-wrap.is-dark :deep(.el-select__selected-item) {
  color: #e7eefc;
}

.report-page-wrap.is-dark :deep(.el-table) {
  --el-table-bg-color: rgba(9, 13, 20, 0.78);
  --el-table-tr-bg-color: rgba(9, 13, 20, 0.78);
  --el-table-expanded-cell-bg-color: rgba(9, 13, 20, 0.78);
  --el-table-header-bg-color: rgba(14, 20, 30, 0.88);
  --el-table-border-color: rgba(166, 188, 216, 0.22);
  --el-table-text-color: #dce7f7;
  --el-table-header-text-color: #eef4ff;
  --el-fill-color-lighter: rgba(255, 255, 255, 0.02);
}

.report-card {
  border-radius: 14px;
}

.report-card h2 {
  margin: 0;
  font-size: 1.35rem;
  color: #11334f;
}

.report-page-wrap.is-dark .report-card h2 {
  color: #e7eefc;
}

.full-width {
  width: 100%;
}

.actions {
  margin-bottom: 14px;
  display: flex;
  gap: 10px;
}

.actions :deep(.el-button) {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.toolbar {
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.search-input {
  max-width: 380px;
}

.report-table,
.empty-alert {
  margin-top: 12px;
}

.report-table-wrap {
  min-height: 220px;
}

.pagination-wrap {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .actions,
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    max-width: 100%;
  }
}
</style>
