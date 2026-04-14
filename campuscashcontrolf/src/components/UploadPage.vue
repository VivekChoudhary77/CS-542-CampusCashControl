<template>
  <el-row justify="center" :class="['upload-page-wrap', { 'is-dark': isDarkMode }]">
    <el-col :xs="24" :md="22" :lg="20">
      <el-skeleton :loading="showSkeleton" animated :rows="8">
        <template #template>
          <el-card shadow="never" class="upload-card">
            <el-skeleton-item variant="h1" style="width: 40%; height: 28px;" />
            <el-skeleton-item variant="rect" style="width: 100%; height: 52px; margin-top: 16px;" />
            <el-skeleton-item variant="rect" style="width: 100%; height: 210px; margin-top: 16px;" />
          </el-card>
        </template>

        <template #default>
          <el-card shadow="hover" class="upload-card" v-loading="pageLoading">
            <template #header>
              <div class="card-header-row">
                <h2>Upload Financial Data</h2>
                <a href="/financial_template.xlsx" download="financial_template.xlsx">
                  <el-icon><Download /></el-icon>
                  Download Excel Template
                </a>
              </div>
            </template>

            <el-row :gutter="14" class="filter-row">
              <el-col :xs="24" :md="8">
                <el-form-item label="Department">
                  <el-select v-model="metadata.department" placeholder="Select Department" class="full-width">
                    <el-option v-for="dept in departments" :key="dept" :value="dept" :label="dept" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :md="8">
                <el-form-item label="Month">
                  <el-select v-model="metadata.month" placeholder="Select Month" class="full-width">
                    <el-option v-for="month in months" :key="month" :value="month" :label="month" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :md="8">
                <el-form-item label="Financial Year">
                  <el-select v-model="metadata.year" placeholder="Select Year" class="full-width">
                    <el-option v-for="yr in years" :key="yr" :value="yr" :label="String(yr)" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-upload
              ref="uploadRef"
              drag
              :auto-upload="false"
              :show-file-list="false"
              :limit="1"
              :before-upload="beforeUpload"
              :on-change="handleFileChange"
              :on-exceed="handleExceed"
              accept=".xlsx,.xls,.xlsm,.csv"
              class="upload-zone"
            >
              <div class="upload-copy">
                <p class="title">
                  <el-icon><UploadFilled /></el-icon>
                  Drop Excel/CSV file here or click to browse
                </p>
                <p class="hint">Supported: .xlsx, .xls, .xlsm, .csv. Max 10MB.</p>
              </div>
            </el-upload>

            <el-alert
              v-if="selectedFile"
              :title="`Selected: ${selectedFile.name} (${formatFileSize(selectedFile.size)})`"
              type="info"
              show-icon
              :closable="false"
              class="status-alert"
            />

            <el-alert
              v-if="errorMessage"
              :title="errorMessage"
              type="error"
              show-icon
              :closable="false"
              class="status-alert"
            />

            <el-alert
              v-if="successMessage"
              :title="successMessage"
              type="success"
              show-icon
              :closable="false"
              class="status-alert"
            />

            <div class="actions-row">
              <el-button @click="handleCancelFile" :disabled="!selectedFile">Cancel</el-button>
              <el-button type="primary" :loading="uploadLoading" @click="handleUpload" :disabled="!isFormValid">Upload File</el-button>
            </div>
          </el-card>
        </template>
      </el-skeleton>
    </el-col>
  </el-row>
</template>

<script>
import axios from "axios";
import { ElNotification } from "element-plus";
import { Download, UploadFilled } from "@element-plus/icons-vue";
import { themeState } from "@/state/themeState";

export default {
  name: "UploadPage",
  components: {
    Download,
    UploadFilled,
  },
  data() {
    return {
      showSkeleton: true,
      pageLoading: false,
      uploadLoading: false,
      selectedFile: null,
      errorMessage: "",
      successMessage: "",
      metadata: {
        department: "",
        month: "",
        year: "",
      },
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
    isFormValid() {
      return (
        this.selectedFile &&
        this.metadata.department &&
        this.metadata.month &&
        this.metadata.year
      );
    },
  },
  methods: {
    validateFile(file) {
      const maxSize = 10 * 1024 * 1024;
      if (file.size > maxSize) {
        this.errorMessage = "File size exceeds 10MB. Please select a smaller file.";
        return false;
      }

      const acceptedTypes = [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/csv",
        "application/csv",
      ];
      const acceptedExtensions = [".xlsx", ".xls", ".xlsm", ".csv"];

      if (!acceptedTypes.includes(file.type)) {
        const fileName = file.name.toLowerCase();
        const hasValidExtension = acceptedExtensions.some((ext) => fileName.endsWith(ext));
        if (!hasValidExtension) {
          this.errorMessage = "Please upload Excel or CSV files only.";
          return false;
        }
      }

      this.errorMessage = "";
      return true;
    },
    beforeUpload(file) {
      return this.validateFile(file);
    },
    handleFileChange(file) {
      if (!file.raw) {
        return;
      }
      if (this.validateFile(file.raw)) {
        this.selectedFile = file.raw;
        this.successMessage = "";
      }
    },
    handleExceed() {
      ElNotification({
        title: "File limit",
        message: "Only one file can be selected at a time.",
        type: "warning",
      });
    },
    handleCancelFile() {
      this.selectedFile = null;
      this.errorMessage = "";
      this.successMessage = "";
      if (this.$refs.uploadRef) {
        this.$refs.uploadRef.clearFiles();
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
    },
    handleUpload() {
      if (!this.metadata.department) {
        this.errorMessage = "Department has not been selected.";
        return;
      }
      if (!this.metadata.month) {
        this.errorMessage = "Month has not been selected.";
        return;
      }
      if (!this.metadata.year) {
        this.errorMessage = "Financial Year has not been selected.";
        return;
      }
      if (!this.selectedFile) {
        this.errorMessage = "Please select a file to upload.";
        return;
      }

      this.uploadLoading = true;
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
          this.successMessage = response.data.message || "Your data was uploaded successfully.";
          this.errorMessage = "";
          ElNotification({
            title: "Upload success",
            message: "Upload completed.",
            type: "success",
          });
          setTimeout(() => {
            this.handleCancelFile();
          }, 3000);
        })
        .catch((error) => {
          console.error("Upload error:", error.response?.data || error);
          this.errorMessage = error.response?.data?.error || "Upload failed.";
          ElNotification({
            title: "Upload failed",
            message: this.errorMessage,
            type: "error",
          });
        })
        .finally(() => {
          this.uploadLoading = false;
        });
    },
  },
  mounted() {
    this.pageLoading = true;
    ElNotification({
      title: "Loading",
      message: "Fetching active departments...",
      type: "info",
    });
    axios
      .get("http://localhost:8000/api/departments/active/")
      .then((res) => {
        this.departments = res.data.map((d) => d.name);
      })
      .catch((err) => {
        console.error("Could not load departments:", err);
        ElNotification({
          title: "Fetch failed",
          message: "Could not load active departments.",
          type: "error",
        });
      })
      .finally(() => {
        this.pageLoading = false;
      });

    setTimeout(() => {
      this.showSkeleton = false;
    }, 360);
  },
};
</script>

<style scoped>
.upload-page-wrap.is-dark :deep(.el-card) {
  background: linear-gradient(160deg, rgba(11, 15, 24, 0.68), rgba(11, 15, 24, 0.82));
  border-color: rgba(166, 188, 216, 0.24);
}

.upload-page-wrap.is-dark :deep(.el-form-item__label) {
  color: #d4e0f1;
}

.upload-page-wrap.is-dark :deep(.el-input__wrapper),
.upload-page-wrap.is-dark :deep(.el-select__wrapper),
.upload-page-wrap.is-dark :deep(.el-upload-dragger) {
  background: rgba(10, 14, 22, 0.74);
  box-shadow: 0 0 0 1px rgba(166, 188, 216, 0.3) inset;
}

.upload-page-wrap.is-dark :deep(.el-input__inner),
.upload-page-wrap.is-dark :deep(.el-select__placeholder),
.upload-page-wrap.is-dark :deep(.el-select__selected-item) {
  color: #e7eefc;
}

.upload-card {
  border-radius: 14px;
}

.card-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-header-row h2 {
  margin: 0;
  color: #11334f;
  font-size: 1.35rem;
}

.upload-page-wrap.is-dark .card-header-row h2 {
  color: #e7eefc;
}

.card-header-row a {
  color: #245f8f;
  text-decoration: none;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.filter-row {
  margin-bottom: 6px;
}

.full-width {
  width: 100%;
}

.upload-zone {
  margin-top: 10px;
}

.upload-copy .title {
  margin: 0;
  font-weight: 700;
  color: #274a66;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.upload-page-wrap.is-dark .upload-copy .title {
  color: #e7eefc;
}

.upload-copy .hint {
  margin: 6px 0 0;
  color: #627789;
}

.upload-page-wrap.is-dark .upload-copy .hint {
  color: #b7c5d8;
}

.status-alert {
  margin-top: 14px;
}

.actions-row {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .card-header-row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
