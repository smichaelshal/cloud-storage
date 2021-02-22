import Vue from "vue";
import VueRouter from "vue-router";

import Home from "@/views/Home.vue";

// import NotFound from "@/views/NotFound.vue";

import Register from "@/views/Register.vue";

import Login from "@/views/Login.vue";

import ForgotPassword from "@/views/ForgotPassword.vue";

// import ResetPasswordNew from "@/views/ResetPasswordNew.vue";

import ChangePassword from "@/views/ChangePassword.vue";

Vue.use(VueRouter);
const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/forgot-password",
    name: "ForgotPassword",
    component: ForgotPassword,
  },
  {
    path: "/change-password",
    name: "ChangePassword",
    component: ChangePassword,
  },

  // {
  //   path: "/reset-password-new",
  //   name: "ResetPasswordNew",
  //   component: ResetPasswordNew
  // },

  // {
  //   path: "*",
  //   name: "NotFound",
  //   component: NotFound
  // }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
