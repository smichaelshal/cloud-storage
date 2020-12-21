import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const state = {
  namePage: "/",
  token: "",
  username: "",
  dataMsg: "",
  typeMsg: "",
  idMsg: 0,

  host: "http://localhost:8000/",
  trees: null,
  pathNow: "/",
  pathHome: "/Users/michael/Desktop/Home",
  listSelected: {},
  listSelectedLength: 0,
  listSelectedDirectories: {},
  listSelectedLengthDirectories: 0,
  isRightClick: false,
};

const mutations = {
  setToken(state, token) {
    state.token = token;
  },
  setListSelectedLength(state, listSelectedLength) {
    state.listSelectedLength = listSelectedLength;
  },
  setIsRightClick(state, isRightClick) {
    state.isRightClick = isRightClick;
  },
  setDataMsg(state, dataMsg) {
    state.dataMsg = dataMsg;
  },
  setIdMsg(state, idMsg) {
    state.idMsg = idMsg;
  },
  setTypeMsg(state, typeMsg) {
    state.typeMsg = typeMsg;
  },
  setPathHome(state, pathHome) {
    state.token = pathHome;
  },

  setPathNow(state, pathNow) {
    state.pathNow = pathNow;
  },
  setTrees(state, trees) {
    state.trees = trees;
  },
  setNamePage(state, namePage) {
    state.namePage = namePage;
  },

  setUsername(state, username) {
    state.username = username;
  },
};

const actions = {};

const modules = {};

const getters = {
  getToken() {
    return state.token;
  },
  getListSelectedLength() {
    return state.listSelectedLength;
  },
  getListSelectedLengthDirectories() {
    return state.listSelectedLengthDirectories;
  },
  getIsRightClick() {
    return state.isRightClick;
  },
  getListSelected() {
    return state.listSelected;
  },
  getListSelectedDirectories() {
    return state.listSelectedDirectories;
  },
  getTypeMsg() {
    return state.typeMsg;
  },
  getIdMsg() {
    return state.idMsg;
  },
  getDataMsg() {
    return state.dataMsg;
  },
  getPathHome() {
    return state.pathHome;
  },
  getPathNow() {
    return state.pathNow;
  },
  getNamePage() {
    return state.namePage;
  },
  getUsername() {
    return state.username;
  },
  getHost() {
    return state.host;
  },
  getTrees() {
    return state.trees;
  },
};

export default new Vuex.Store({
  state,
  mutations,
  actions,
  modules,
  getters,
});
