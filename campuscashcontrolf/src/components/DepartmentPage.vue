<template>
  <el-row justify="center" :class="['department-page-wrap', { 'is-dark': isDarkMode }]">
    <el-col :xs="24" :md="22" :lg="20">
      <el-skeleton :loading="showSkeleton" animated :rows="8">
        <template #template>
          <el-card shadow="never" class="department-card">
            <el-skeleton-item variant="h1" style="width: 40%; height: 28px;" />
            <el-skeleton-item variant="rect" style="width: 100%; height: 56px; margin-top: 16px;" />
            <el-skeleton-item variant="rect" style="width: 100%; height: 350px; margin-top: 16px;" />
          </el-card>
        </template>

        <template #default>
          <el-card shadow="hover" class="department-card" v-loading="pageLoading">
            <template #header>
              <div class="card-header-row">
                <h2>Department Management</h2>
              </div>
            </template>

            <el-form inline class="editor-form" @submit.prevent>
              <el-form-item label="Department Name">
                <el-input
                  v-model="form.name"
                  placeholder="Enter department name"
                  clearable
                  @keyup.enter="submitForm"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" :loading="submitLoading" @click="submitForm">
                  {{ isEditing ? 'Update' : 'Create' }}
                </el-button>
                <el-button v-if="isEditing" @click="cancelEdit">Cancel</el-button>
              </el-form-item>
            </el-form>

            <el-table :data="departments" stripe border class="department-table" v-loading="tableLoading">
              <el-table-column prop="id" label="ID" width="90" />
              <el-table-column prop="name" label="Name" min-width="280" />
              <el-table-column label="Status" width="140" align="center">
                <template #default="scope">
                  <el-tag :type="scope.row.is_active ? 'success' : 'danger'" effect="light">
                    {{ scope.row.is_active ? 'Active' : 'Inactive' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="Actions" width="260" align="center">
                <template #default="scope">
                  <el-space>
                    <el-button size="small" @click="editDepartment(scope.row)">
                      <el-icon><Edit /></el-icon>
                      Edit
                    </el-button>
                    <el-button
                      v-if="scope.row.is_active"
                      size="small"
                      type="warning"
                      @click="toggleStatus(scope.row)"
                    >
                      <el-icon><CloseBold /></el-icon>
                      Deactivate
                    </el-button>
                    <el-button
                      v-else
                      size="small"
                      type="success"
                      @click="toggleStatus(scope.row)"
                    >
                      <el-icon><Check /></el-icon>
                      Activate
                    </el-button>
                  </el-space>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </template>
      </el-skeleton>
    </el-col>
  </el-row>
</template>

<script>
import axios from "axios";
import { ElMessageBox, ElNotification } from "element-plus";
import { Edit, CloseBold, Check } from "@element-plus/icons-vue";
import { themeState } from "@/state/themeState";
import { apiUrl } from "@/config/api";

export default {
  name: "DepartmentPage",
  components: {
    Edit,
    CloseBold,
    Check,
  },
  data() {
    return {
      departments: [],
      showSkeleton: true,
      pageLoading: false,
      tableLoading: false,
      submitLoading: false,
      form: {
        id: null,
        name: "",
      },
      isEditing: false,
    };
  },
  computed: {
    isDarkMode() {
      return themeState.isDarkMode;
    },
  },
  methods: {
    fetchDepartments() {
      this.tableLoading = true;
      if (!this.departments.length) {
        ElNotification({
          title: "Loading",
          message: "Fetching departments...",
          type: "info",
        });
      }
      axios
        .get(apiUrl("/departments/"))
        .then((res) => {
          this.departments = res.data;
        })
        .catch((err) => {
          console.error("Failed to fetch departments:", err);
          ElNotification({
            title: "Fetch failed",
            message: "Could not load departments. Check the server.",
            type: "error",
          });
        })
        .finally(() => {
          this.tableLoading = false;
        });
    },
    submitForm() {
      if (!this.form.name.trim()) {
        ElNotification({
          title: "Validation",
          message: "Department name cannot be empty.",
          type: "warning",
        });
        return;
      }

      this.submitLoading = true;
      const operation = this.isEditing ? "UPDATE" : "CREATE";

      axios
        .post(apiUrl("/manage-department/"), {
          operation,
          id: this.form.id,
          name: this.form.name,
        })
        .then(() => {
          ElNotification({
            title: "Success",
            message: this.isEditing ? "Department updated." : "Department created.",
            type: "success",
          });
          this.fetchDepartments();
          this.resetForm();
        })
        .catch((err) => {
          console.error("Submit failed:", err);
          ElNotification({
            title: "Submit failed",
            message: "Failed to submit department details.",
            type: "error",
          });
        })
        .finally(() => {
          this.submitLoading = false;
        });
    },
    editDepartment(dept) {
      this.form = { id: dept.id, name: dept.name };
      this.isEditing = true;
    },
    cancelEdit() {
      this.resetForm();
    },
    resetForm() {
      this.form = { id: null, name: "" };
      this.isEditing = false;
    },
    async toggleStatus(dept) {
      const operation = dept.is_active ? "DEACTIVATE" : "ACTIVATE";

      if (operation === "DEACTIVATE") {
        try {
          await ElMessageBox.confirm(
            `Deactivate ${dept.name}?`,
            "Confirm Action",
            {
              confirmButtonText: "Deactivate",
              cancelButtonText: "Cancel",
              type: "warning",
            }
          );
        } catch {
          return;
        }
      }

      this.tableLoading = true;
      axios
        .post(apiUrl("/manage-department/"), {
          operation,
          id: dept.id,
          name: dept.name,
        })
        .then(() => {
          ElNotification({
            title: "Status updated",
            message: `Department ${dept.is_active ? "deactivated" : "activated"}.`,
            type: "info",
          });
          this.fetchDepartments();
        })
        .catch((err) => {
          console.error("Toggle status failed:", err);
          ElNotification({
            title: "Status update failed",
            message: "Failed to change status.",
            type: "error",
          });
        })
        .finally(() => {
          this.tableLoading = false;
        });
    },
  },
  mounted() {
    this.pageLoading = true;
    this.fetchDepartments();
    setTimeout(() => {
      this.showSkeleton = false;
      this.pageLoading = false;
    }, 360);
  },
};
</script>

<style scoped>
.department-page-wrap.is-dark :deep(.el-card) {
  background: linear-gradient(160deg, rgba(11, 15, 24, 0.68), rgba(11, 15, 24, 0.82));
  border-color: rgba(166, 188, 216, 0.24);
}

.department-page-wrap.is-dark :deep(.el-form-item__label) {
  color: #d4e0f1;
}

.department-page-wrap.is-dark :deep(.el-input__wrapper) {
  background: rgba(10, 14, 22, 0.74);
  box-shadow: 0 0 0 1px rgba(166, 188, 216, 0.3) inset;
}

.department-page-wrap.is-dark :deep(.el-input__inner) {
  color: #e7eefc;
}

.department-page-wrap.is-dark :deep(.el-table) {
  --el-table-bg-color: rgba(9, 13, 20, 0.78);
  --el-table-tr-bg-color: rgba(9, 13, 20, 0.78);
  --el-table-expanded-cell-bg-color: rgba(9, 13, 20, 0.78);
  --el-table-header-bg-color: rgba(14, 20, 30, 0.88);
  --el-table-border-color: rgba(166, 188, 216, 0.22);
  --el-table-text-color: #dce7f7;
  --el-table-header-text-color: #eef4ff;
  --el-fill-color-lighter: rgba(255, 255, 255, 0.02);
}

.department-card {
  border-radius: 14px;
}

.card-header-row h2 {
  margin: 0;
  font-size: 1.35rem;
  color: #11334f;
}

.department-page-wrap.is-dark .card-header-row h2 {
  color: #e7eefc;
}

.editor-form {
  margin-bottom: 20px;
}

.department-table {
  width: 100%;
}

.department-table :deep(.el-table) {
  --el-table-row-hover-bg-color: transparent;
}

.department-table :deep(.el-table__body tr:hover > td.el-table__cell),
.department-table :deep(.el-table__body tr.hover-row > td.el-table__cell) {
  background-color: inherit !important;
}
</style>
