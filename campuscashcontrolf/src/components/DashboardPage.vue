<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">CampusCashControl</a>

        <!-- Navbar Links -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item"><router-link class="nav-link" to="#">Departments</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="#">Upload</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="#">Reports</router-link></li>
        </ul>

        <!-- User Dropdown (Aligned Right) -->
        <div class="dropdown" ref="dropdown">
          <button class="btn btn-secondary dropdown-toggle" type="button" @click="toggleDropdown">
            <i class="fas fa-user"></i> <!-- User Icon -->
          </button>
          <ul v-show="dropdownVisible" class="dropdown-menu dropdown-menu-end">
            <li><button class="dropdown-item" @click="logout">Logout</button></li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Empty Body Content -->
    <div class="container mt-5">
      <h2>Welcome to the Dashboard</h2>
      <p>This is your dashboard content.</p>
    </div>

    <!-- Footer -->
    <footer class="text-center mt-5">
      <p>&copy; 2025 CampusCashControl</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "DashboardPage",
  data() {
    return {
      dropdownVisible: false, // Dropdown visibility state
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible; // Toggle dropdown state
    },
    logout() {
      localStorage.removeItem("authToken"); // Clear authentication details
      this.$router.push("/"); // Redirect to homepage
    },
  },
};
</script>

<style scoped>
.navbar {
  padding: 10px 20px;
}

.container {
  text-align: center;
}

footer {
  background-color: #f8f9fa;
  padding: 10px;
  position: absolute;
  bottom: 0;
  width: 100%;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-menu {
  display: block;
  position: absolute;
  top: 100%;
  right: 0;
  min-width: 150px;
  background: white;
  border-radius: 5px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.dropdown-menu li {
  list-style: none;
  padding: 8px;
}

.dropdown-menu li button {
  background: none;
  border: none;
  color: black;
  width: 100%;
  text-align: left;
  padding: 10px;
  cursor: pointer;
}

.dropdown-menu li button:hover {
  background: #f8f9fa;
}
</style>