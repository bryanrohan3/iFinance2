import axios from "axios";
import VueAxios from "vue-axios";
import store from "../store";
import { app } from "../main";

function setupAxiosHandler() {
  app.use(VueAxios, axios);
  app.axios.defaults.xsrfCookieName = "csrftoken";
  app.axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  app.axios.interceptors.request.use(function (config) {
    if (store.state.authToken) {
      config.headers.Authorization = "Token " + store.state.authToken;
    }
    console.log(store.state.authToken);
    return config;
  });
}

function axiosInstance() {
  return app.axios;
}
export { axiosInstance, setupAxiosHandler };
