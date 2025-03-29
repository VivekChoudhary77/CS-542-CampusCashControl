<template>
  <div class="dashboard">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">CampusCashControl</a>

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
        </ul>
        <!-- User Logo (Circular, no arrow) -->
        <div class="user-logo" @click="toggleDropdown">
          <i class="fas fa-user"></i>
          <!-- Logout button dropdown -->
          <div v-show="dropdownVisible" class="logout-menu">
            <button class="logout-btn" @click="logout">Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <div class="content container">
      <h2>Welcome to the Dashboard</h2>
      <p>This is your dashboard content.</p>
    </div>

    <!-- Footer -->
    <footer class="footer text-center">
      <p>&copy; 2025 CampusCashControl</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "DashboardPage",
  data() {
    return {
      dropdownVisible: false,
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    logout() {
      localStorage.removeItem("authToken");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
/* Root container to ensure full height and flex layout */
.dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Main content takes remaining space */
.content {
  flex: 1;
  margin-top: 20px; /* optional spacing */
}

/* Navbar adjustments */
.navbar {
  padding: 10px 20px;
}

/* Container text centering for content */
.container {
  text-align: center;
}

/* User Logo Styling */
.user-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%; /* Makes it circular */
  background-color: white;
  border: 2px solid #ccc; /* Optional border */
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

/* Logout menu styling */
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
  background-color: #f8f9fa;
}

/* Footer styling: Remove top margin and ensure it stays at bottom */
.footer {
  background-color: #f8f9fa;
  padding: 10px;
  border-top: 1px solid #e7e7e7;
}
</style>