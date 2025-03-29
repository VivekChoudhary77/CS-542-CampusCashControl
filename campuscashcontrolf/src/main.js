import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap"; // Ensure Bootstrap JS is included
import "@fortawesome/fontawesome-free/css/all.min.css"; // Import FontAwesome for icons

const app = createApp(App);
app.use(router);
app.mount("#app");
