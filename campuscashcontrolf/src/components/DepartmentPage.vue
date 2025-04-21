<template>
  <div class="department d-flex flex-column min-vh-100">
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
 
        <!-- User Logo -->
        <div class="user-logo position-relative" ref="userLogo" @click.stop="toggleDropdown">
          <i class="fas fa-user"></i>
          <div v-show="dropdownVisible" class="logout-menu bg-white border shadow-sm position-absolute end-0">
            <button class="logout-btn" @click="logout">Logout</button>
          </div>
        </div>
      </div>
    </nav>
 
    <!-- Main Content Area -->
    <div class="content container flex-grow-1 mt-4">
      <!-- Department Management -->
      <div class="p-4 bg-white rounded shadow-sm">
        <h2 class="h4 mb-4">Departments Management</h2>
 
        <!-- Add/Edit Form -->
        <div class="mb-4">
          <h3 class="h5 mb-3">{{ isEditing ? 'Edit Department' : 'Add Department' }}</h3>
          <div class="row g-2 align-items-center">
            <div class="col-md-6">
              <input v-model="form.name" type="text" placeholder="Department Name" class="form-control" />
            </div>
            <div class="col-auto">
              <button @click="submitForm" class="btn btn-primary">
                {{ isEditing ? 'Update' : 'Create' }}
              </button>
            </div>
            <div class="col-auto" v-if="isEditing">
              <button @click="cancelEdit" class="btn btn-secondary">Cancel</button>
            </div>
          </div>
        </div>
 
        <!-- Department Table -->
        <div class="table-responsive">
          <table class="table table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Status</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="dept in departments" :key="dept.id">
                <td>{{ dept.id }}</td>
                <td>{{ dept.name }}</td>
                <td>
                  <span :class="dept.is_active ? 'text-success' : 'text-danger'">
                    {{ dept.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="text-center">
                  <button @click="editDepartment(dept)" class="btn btn-sm btn-warning me-2">Edit</button>
                  <button
                    @click="toggleStatus(dept)"
                    class="btn btn-sm"
                    :class="dept.is_active ? 'btn-danger' : 'btn-success'"
                  >
                    {{ dept.is_active ? 'Deactivate' : 'Activate' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
 
    <!-- Footer -->
    <footer class="footer bg-light text-center py-2 mt-auto">
      <p class="mb-0">&copy; 2025 CampusCashControl</p>
    </footer>
  </div>
</template>
 
<script>
import axios from 'axios';
 
const API_BASE_URL = 'http://localhost:8000/api';
 
export default {
  name: 'DepartmentPage',
  data() {
    return {
      dropdownVisible: false,
      departments: [],
      form: {
        id: null,
        name: '',
      },
      isEditing: false,
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('authenticated');
      this.$router.replace({ name: 'home' });
    },
    handleClickOutside(event) {
      if (this.$refs.userLogo && !this.$refs.userLogo.contains(event.target)) {
        this.dropdownVisible = false;
      }
    },
    fetchDepartments() {
      axios.get(`${API_BASE_URL}/departments/`)
        .then(res => {
          this.departments = res.data;
        })
        .catch(err => {
          console.error('Failed to fetch departments:', err);
          alert('Could not load departments. Check the server is running.');
        });
    },
    submitForm() {
      // Prevent empty department name
      if (!this.form.name.trim()) {
        alert('Department name cannot be empty.');
        return;
      }
      const operation = this.isEditing ? 'UPDATE' : 'CREATE';
      axios.post(`${API_BASE_URL}/manage-department/`, {
        operation,
        id: this.form.id,
        name: this.form.name,
      }).then(() => {
        this.fetchDepartments();
        this.resetForm();
      }).catch(err => {
        console.error('Submit failed:', err);
        alert('Failed to submit form.');
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
      this.form = { id: null, name: '' };
      this.isEditing = false;
    },
    toggleStatus(dept) {
      const operation = dept.is_active ? 'DEACTIVATE' : 'ACTIVATE';
      axios.post(`${API_BASE_URL}/manage-department/`, {
        operation,
        id: dept.id,
        name: dept.name,
      }).then(() => {
        this.fetchDepartments();
      }).catch(err => {
        console.error('Toggle status failed:', err);
        alert('Failed to change status.');
      });
    },
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
    this.fetchDepartments();
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
  },
};
</script>
 
<style scoped>
.department {
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
.footer {
  background-color: #f8f9fa;
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
}
.logout-menu {
  top: 45px;
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
</style>