import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// Import Bootstrap CSS
import "bootstrap/dist/css/bootstrap.min.css";

const app = createApp(App);

// Use Vue Router
app.use(router);

// Mount the application
app.mount("#app");

