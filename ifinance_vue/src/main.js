import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { setupAxiosHandler } from "./api/axiosHandler";

const app = createApp(App).use(store).use(router);
app.mount("#app");
setupAxiosHandler();
export { app };
