import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    component: () => import("../views/AboutView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/Login/LoginPage.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("../views/SignUp/SignUpPage.vue"),
  },
  {
    path: "/transactions",
    name: "transactions",
    component: () => import("../views/Transactions/TransactionPage.vue"),
  },
  {
    path: "/budget",
    name: "budget",
    component: () => import("../views/Budget/BudgetPage.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
