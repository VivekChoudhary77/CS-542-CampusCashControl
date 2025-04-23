<template>
  <div class="report d-flex flex-column min-vh-100">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/dashboard">
          <img src="@/assets/CCC Dashboard Logo.png" alt="CampusCashControl" class="navbar-logo" />
        </router-link>
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item"><router-link class="nav-link" to="/departments">Departments</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/upload">Upload</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/reports">Reports</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/UserAccess">User Access</router-link></li>
        </ul>
        <div class="user-logo" ref="userLogo" @click.stop="toggleDropdown">
          <i class="fas fa-user"></i>
          <div v-show="dropdownVisible" class="logout-menu">
            <button class="logout-btn" @click="logout">Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <div class="content container flex-grow-1 mt-4">
      <h2 class="mt-4 mb-4">Financial Reports</h2>

      <!-- Filter Controls -->
      <div class="row mb-4">
        <div class="col-md-4 mb-3">
          <label for="department" class="form-label">Department</label>
          <select id="department" class="form-select" v-model="filters.department">
            <option value="all_departments">All Departments</option>
            <option v-for="dept in departments" :key="dept" :value="dept">
              {{ dept }}
            </option>
          </select>
        </div>
        <div class="col-md-4 mb-3">
          <label for="month" class="form-label">Month</label>
          <select id="month" class="form-select" v-model="filters.month">
            <option value="all_months">All Months</option>
            <option v-for="name in months" :key="name" :value="name">
              {{ name }}
            </option>
          </select>
        </div>
        <div class="col-md-4 mb-3">
          <label for="year" class="form-label">Financial Year</label>
          <select id="year" class="form-select" v-model="filters.year">
            <option value="all_years">All Years</option>
            <option v-for="yr in years" :key="yr" :value="yr">
              {{ yr }}
            </option>
          </select>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="row mb-4">
        <div class="col-12 d-flex gap-2 justify-content-center">
          <button class="btn btn-dark" @click="displayReport">
            <i class="fas fa-search me-2"></i> Display Report
          </button>
          <button class="btn btn-outline-dark" @click="downloadReport" :disabled="!displayedData.length">
            <i class="fas fa-download me-2"></i> Download Report
          </button>
        </div>
      </div>

      <!-- Search & Info -->
      <div class="row mb-3" v-if="displayedData.length">
        <div class="col-md-6 text-start">
          <div class="input-group">
            <span class="input-group-text"><i class="fas fa-search"></i></span>
            <input type="text" class="form-control" placeholder="Search reports…" v-model="searchQuery" />
          </div>
        </div>
        <div class="col-md-6 text-end">
          <span class="badge bg-info">{{ filteredReportData.length }} records found</span>
        </div>
      </div>

      <!-- Report Table -->
      <div class="table-responsive">
        <div v-if="!hasSearched" class="alert alert-info mt-4">
          <i class="fas fa-info-circle me-2"></i>
          Please select your filter criteria and click "Display Report" to view financial data.
        </div>
        
        <table v-if="hasSearched && displayedData.length" class="table table-striped table-hover">
          <thead class="table-light">
            <tr>
              <th @click="sortBy('department')" class="sortable">
                Department <i :class="getSortIcon('department')"></i>
              </th>
              <th @click="sortBy('item')" class="sortable">
                Item <i :class="getSortIcon('item')"></i>
              </th>
              <th @click="sortBy('revenue')" class="sortable">
                Revenue <i :class="getSortIcon('revenue')"></i>
              </th>
              <th @click="sortBy('month')" class="sortable">
                Month <i :class="getSortIcon('month')"></i>
              </th>
              <th @click="sortBy('year')" class="sortable">
                Financial Year <i :class="getSortIcon('year')"></i>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in paginatedReportData" :key="idx">
              <td>{{ row.department }}</td>
              <td>{{ row.item }}</td>
              <td>${{ row.revenue.toLocaleString() }}</td>
              <td>{{ row.month }}</td>
              <td>{{ row.year }}</td>
            </tr>
          </tbody>
        </table>

        <div v-if="hasSearched && !displayedData.length" class="alert alert-warning mt-4">
          <i class="fas fa-exclamation-circle me-2"></i>
          No records found for the selected criteria.
        </div>
      </div>

      <!-- Pagination -->
      <nav v-if="displayedData.length && totalPages > 1" class="mt-4">
        <ul class="pagination justify-content-center">
          <!-- Previous -->
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <a class="page-link" href="#" @click.prevent="currentPage > 1 && currentPage--">
              ‹ Previous
            </a>
          </li>

          <!-- Page numbers -->
          <li v-for="p in paginationRange" :key="p" class="page-item" :class="{ active: currentPage === p }">
            <a class="page-link" href="#" @click.prevent="currentPage = p">
              {{ p }}
            </a>
          </li>

          <!-- Next -->
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <a class="page-link" href="#" @click.prevent="currentPage < totalPages && currentPage++">
              Next ›
            </a>
          </li>
        </ul>
      </nav>

    </div>

    <!-- Footer -->
    <footer class="footer text-center">
      <p>&copy; 2025 CampusCashControl</p>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

export default {
  name: "ReportPage",
  data() {
    return {
      dropdownVisible: false,
      hasSearched: false,
      displayedData: [],
      filters: {
        department: 'all_departments',
        month: 'all_months',
        year: 'all_years'
      },
      searchQuery: '',
      // no default sort
      currentSort: null,
      currentSortDir: 'asc',
      currentPage: 1,
      itemsPerPage: 10,
      departments: [],
      months: [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
      ],
      years: Array.from({ length: 2027 - 2023 + 1 }, (_, i) => 2023 + i)
    };
  },
  computed: {
    filteredReportData() {
      let res = this.displayedData.slice();

      // client‐side search
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        res = res.filter(r =>
          r.department.toLowerCase().includes(q) ||
          r.item.toLowerCase().includes(q) ||
          String(r.revenue).includes(q) ||
          r.month.toLowerCase().includes(q) ||
          String(r.year).includes(q)
        );
      }

      // only sort if user clicked
      if (!this.currentSort) return res;

      const dir = this.currentSortDir === 'asc' ? 1 : -1;
      return res.slice().sort((a, b) => {
        if (this.currentSort === 'month') {
          const iA = this.months.indexOf(a.month);
          const iB = this.months.indexOf(b.month);
          return (iA - iB) * dir;
        }
        if (this.currentSort === 'revenue') return (a.revenue - b.revenue) * dir;
        if (this.currentSort === 'year') return (a.year - b.year) * dir;
        // string fields:
        return a[this.currentSort].localeCompare(b[this.currentSort]) * dir;
      });
    },
    totalPages() {
      return Math.ceil(this.filteredReportData.length / this.itemsPerPage);
    },
    paginatedReportData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredReportData.slice(start, start + this.itemsPerPage);
    },
    paginationRange() {
      const range = [];
      const maxVisible = 5;
      let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
      let end = Math.min(this.totalPages, start + maxVisible - 1);
      if (end - start + 1 < maxVisible) start = Math.max(1, end - maxVisible + 1);
      for (let i = start; i <= end; i++) range.push(i);
      return range;
    }
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    logout() {
      localStorage.clear();
      this.$router.replace({ name: "home" });
    },
    handleClickOutside(e) {
      if (this.$refs.userLogo && !this.$refs.userLogo.contains(e.target)) {
        this.dropdownVisible = false;
      }
    },
    displayReport() {
      this.hasSearched = true;
      axios.get("http://localhost:8000/api/reports/", { params: this.filters })
        .then(({ data }) => {
          this.displayedData = data;
          this.currentPage = 1;
        })
        .catch(err => {
          console.error(err);
          alert("Error fetching report data");
        });
    },
    downloadReport() {
      const rows = this.filteredReportData.map(r => ({
        Department: r.department,
        Item: r.item,
        Revenue: r.revenue,
        Month: r.month,
        Year: r.year
      }));
      const ws = XLSX.utils.json_to_sheet(rows);
      ws['!cols'] = [
        { wch: 25 }, { wch: 30 }, { wch: 15 }, { wch: 12 }, { wch: 10 }
      ];
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Report');
      const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
      saveAs(new Blob([wbout], { type: 'application/octet-stream' }), 'financial_report.xlsx');
    },
    sortBy(col) {
      if (this.currentSort === col) {
        this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
      } else {
        this.currentSort = col;
        this.currentSortDir = 'asc';
      }
    },
    getSortIcon(col) {
      if (this.currentSort === col) {
        return this.currentSortDir === 'asc'
          ? 'fas fa-sort-up'
          : 'fas fa-sort-down';
      }
      // always show the up/down sort icon
      return 'fas fa-sort';
    }
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);

    // 1) load departments
    axios.get("http://localhost:8000/api/departments/active/")
      .then(({ data }) => this.departments = data.map(d => d.name))
      .catch(err => console.error("Could not load departments:", err));
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
  watch: {
    searchQuery() {
      this.currentPage = 1;
    }
  }
};
</script>

<style scoped>
.report {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar-logo {
  height: 40px;
  object-fit: contain;
}

.content {
  flex: 1;
  margin-top: 20px;
}

.navbar {
  padding: 10px 20px;
}

.container {
  text-align: center;
}

.user-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
}

.user-logo i {
  font-size: 18px;
  color: #333;
}

.logout-menu {
  position: absolute;
  top: 45px;
  right: 0;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.logout-btn {
  background: none;
  border: none;
  padding: 10px 15px;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.logout-btn:hover {
  background: #f8f9fa;
}

.footer {
  background: #f8f9fa;
  padding: 10px;
  border-top: 1px solid #e7e7e7;
  margin-top: 2rem;
}

.table {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border-radius: 5px;
}

.table thead th {
  background: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
}

.sortable {
  cursor: pointer;
}

.sortable:hover {
  background: #e9ecef;
}

input.form-control,
.form-select {
  border-radius: 4px;
  border: 1px solid #ced4da;
  padding: .375rem .75rem;
}

.badge {
  font-weight: 500;
  padding: .5em .75em;
}

.pagination .page-link {
  color: #0d1a38;
  border: 1px solid #dee2e6;
}

.pagination .page-item.active .page-link {
  background: #0d1a38;
  border-color: #0d1a38;
  color: #fff;
}

@media (max-width:768px) {
  .btn {
    width: 100%;
    margin-bottom: .5rem;
  }

  .col-12.d-flex {
    flex-direction: column;
  }
}
</style>