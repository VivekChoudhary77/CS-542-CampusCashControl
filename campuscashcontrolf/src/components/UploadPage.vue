<template>
  <div class="upload">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/dashboard">
          <img src="@/assets/CCC Dashboard Logo.png" alt="CampusCashControl" class="navbar-logo" />
        </router-link>
  
        <!-- Navbar Links -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/departments">Departments</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/upload">Upload</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/reports">Reports</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/UserAccess">User Access</router-link>
          </li>
        </ul>
  
        <!-- User Logo (Circular, no arrow) -->
        <div class="user-logo" ref="userLogo" @click.stop="toggleDropdown">
          <i class="fas fa-user"></i>
          <div v-show="dropdownVisible" class="logout-menu">
            <button class="logout-btn" @click="logout">Logout</button>
          </div>
        </div>
      </div>
    </nav>
  
    <!-- Main Content Area -->
    <div class="content container">
      <h2 class="mb-4">Upload Financial Data</h2>
  
      <div class="w-100 max-w-2xl mx-auto p-4 bg-white rounded shadow">
        <div class="row mb-4">
          <!-- Department Dropdown -->
          <div class="col-md-4 mb-3">
            <label class="form-label">Department</label>
            <select class="form-select" v-model="metadata.department">
              <option value="" disabled>Select Department</option>
              <option v-for="dept in departments" :key="dept" :value="dept">
                {{ dept }}
              </option>
            </select>
          </div>
  
          <!-- Month and Year Dropdowns -->
          <div class="col-md-4 mb-3">
            <label class="form-label">Month</label>
            <select class="form-select" v-model="metadata.month">
              <option value="" disabled>Select Month</option>
              <option v-for="month in months" :key="month" :value="month">
                {{ month }}
              </option>
            </select>
          </div>
  
          <div class="col-md-4 mb-3">
            <label class="form-label">Financial Year</label>
            <select class="form-select" v-model="metadata.year">
              <option value="" disabled>Select Year</option>
              <option v-for="year in years" :key="year" :value="year">
                {{ year }}
              </option>
            </select>
          </div>
        </div>
  
        <!-- Template Download Link -->
        <div class="mb-4 p-3 bg-light rounded border">
          <div class="d-flex align-items-center">
            <i class="fas fa-file-excel text-success me-2"></i>
            <span>Need a template? </span>
            <a href="/financial_template.xlsx" download="financial_template.xlsx" class="ms-2 fw-medium text-primary">
              Download Excel Template
            </a>
            <span class="ms-2 small text-muted">(A preloaded template which helps you to fill data manually for upload purpose)</span>
          </div>
        </div>
  
        <!-- File Upload Area -->
        <div
          class="border border-2 border-dashed rounded p-4 text-center"
          :class="{ 'border-primary bg-light': isDragging, 'border-success bg-light': selectedFile }"
          @dragover.prevent="handleDragOver"
          @dragleave.prevent="handleDragLeave"
          @drop.prevent="handleDrop"
        >
          <template v-if="!selectedFile">
            <i class="fas fa-file-upload fs-1 text-secondary"></i>
            <p class="mt-2 small text-secondary">
              Drag and drop your Excel or CSV file here, or
            </p>
            <label class="mt-2 d-inline-block">
              <span class="btn btn-primary">Browse Files</span>
              <input
                type="file"
                class="d-none"
                @change="handleFileSelect"
                accept=".xlsx,.xls,.xlsm,.csv"
              />
            </label>
            <p class="mt-2 small text-muted">
              Only Excel (.xlsx, .xls, .xlsm) and CSV files are accepted. Max size: 10MB.
            </p>
          </template>
          <div v-else class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center">
              <i class="fas fa-file-excel text-success me-2"></i>
              <span class="fw-medium">{{ selectedFile.name }}</span>
              <span class="ms-2 small text-muted">
                ({{ formatFileSize(selectedFile.size) }})
              </span>
            </div>
            <button
              type="button"
              class="btn btn-sm btn-outline-danger"
              @click="handleCancelFile"
            >
              <i class="fas fa-times"></i>
              <span class="visually-hidden">Remove</span>
            </button>
          </div>
        </div>
  
        <!-- Error Message -->
        <div v-if="errorMessage" class="alert alert-danger mt-3 d-flex align-items-center">
          <i class="fas fa-exclamation-circle me-2"></i>
          <span>{{ errorMessage }}</span>
        </div>
  
        <!-- Success Message -->
        <div v-if="successMessage" class="alert alert-success mt-3 d-flex align-items-center">
          <i class="fas fa-check-circle me-2"></i>
          <span>{{ successMessage }}</span>
        </div>
  
        <!-- Action Buttons -->
        <div class="mt-4 d-flex justify-content-end gap-2">
          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="handleCancelFile"
            :disabled="!selectedFile"
          >
            Cancel
          </button>
          <button 
            type="button" 
            class="btn btn-primary"
            @click="handleUpload"
            :disabled="!isFormValid"
          >
            Upload File
          </button>
        </div>
      </div>
    </div>
  
    <!-- Footer -->
    <footer class="footer text-center">
      <p>&copy; 2025 CampusCashControl</p>
    </footer>
  </div>
</template>
  
<script>
import axios from 'axios';
export default {
  name: "UploadPage",
  data() {
    return {
      dropdownVisible: false,
      selectedFile: null,
      isDragging: false,
      errorMessage: '',
      successMessage: '', // New: success message after upload
      metadata: {
        department: '',
        month: '',
        year: '',
      },
      // Options for dropdowns
      departments: [
        "Computer Science",
        "Global School",
        "Business School",
        "AI & Data Science",
        "Sports and Recreational Center",
        "Sales"
      ],
      months: ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"],
      years: ["2023", "2024", "2025", "2026", "2027"]
    }
  },
  computed: {
    isFormValid() {
      return this.selectedFile &&
             this.metadata.department &&
             this.metadata.month &&
             this.metadata.year;
    }
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("authenticated");
      this.$router.replace({ name: "home" });
    },
    handleClickOutside(event) {
      if (this.$refs.userLogo && !this.$refs.userLogo.contains(event.target)) {
        this.dropdownVisible = false;
      }
    },
    // Validate file size and type
    validateFile(file) {
      const maxSize = 10 * 1024 * 1024; // 10 MB
      if (file.size > maxSize) {
        this.errorMessage = "File size exceeds 10MB. Please select a smaller file.";
        return false;
      }
  
      const acceptedTypes = [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv',
        'application/csv',
      ];
      const acceptedExtensions = ['.xlsx', '.xls', '.xlsm', '.csv'];
  
      // Check the MIME type first, if available
      if (!acceptedTypes.includes(file.type)) {
        const fileName = file.name.toLowerCase();
        const hasValidExtension = acceptedExtensions.some(ext => fileName.endsWith(ext));
        if (!hasValidExtension) {
          this.errorMessage = "Please upload Excel or CSV files only (.xlsx, .xls, .xlsm, .csv)";
          return false;
        }
      }
      return true;
    },
    handleFileSelect(event) {
      const files = event.target.files;
      if (files && files.length > 0) {
        const file = files[0];
        if (this.validateFile(file)) {
          this.selectedFile = file;
          this.errorMessage = '';
        } else {
          event.target.value = '';
        }
      }
    },
    handleDragOver() {
      this.isDragging = true;
    },
    handleDragLeave() {
      this.isDragging = false;
    },
    handleDrop(event) {
      this.isDragging = false;
      const files = event.dataTransfer.files;
      if (files && files.length > 0) {
        const file = files[0];
        if (this.validateFile(file)) {
          this.selectedFile = file;
          this.errorMessage = '';
        }
      }
    },
    handleCancelFile() {
      this.selectedFile = null;
      this.errorMessage = '';
      this.successMessage = '';
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    handleUpload() {
      if (!this.selectedFile) {
        this.errorMessage = "Please select a file to upload";
        return;
      }
      if (!this.metadata.department || !this.metadata.month || !this.metadata.year) {
        this.errorMessage = "Please select all dropdown options";
        return;
      }
      const formData = new FormData();
      formData.append("file", this.selectedFile);
      formData.append("department", this.metadata.department);
      formData.append("month", this.metadata.month);
      formData.append("year", this.metadata.year);
      axios
        .post("http://localhost:8000/api/upload/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((response) => {
          this.successMessage = response.data.message || "Your data is uploaded successfully.";
          // Optionally clear error message if any.
          this.errorMessage = '';
          // Wait 3 seconds before clearing file and success message.
          setTimeout(() => {
            this.handleCancelFile(); // This will now clear the file and also success message.
          }, 3000);
        })
        .catch((error) => {
          console.error("Upload error:", error.response.data);
          this.errorMessage = error.response.data.error || "Upload failed.";
        });
    },
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  }
};
</script>
  
<style scoped>
.upload {
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
  background-color: white;
  border: 2px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
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
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
  background-color: #f8f9fa;
}
.footer {
  background-color: #f8f9fa;
  padding: 10px;
  border-top: 1px solid #e7e7e7;
}
.border-dashed {
  border-style: dashed !important;
}
</style>
