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
  isUser: null,
  // host: "http://django-cloud-storage.herokuapp.com/",
  // host_ws: "ws://django-cloud-storage.herokuapp.com/",
  host: "http://localhost:8000/",
  host_ws: "ws://localhost:8000/",
  trees: null,
  pathNow: "/",
  pathHome: "/Users/michael/Desktop/Home",
  listSelected: {},
  listSelectedLength: 0,
  listSelectedDirectories: {},
  listSelectedLengthDirectories: 0,
  isRightClick: false,
  wsData: "",
  idUser: null,
  dataToSendWs: null,
  isChangeDataToSendWs: false,
  returnListDirFiles: false,
  // sizeFilesNow: 0,
};

const mutations = {
  setToken(state, token) {
    state.token = token;
  },
  setIsChangeDataToSendWs(state, isChangeDataToSendWs) {
    state.isChangeDataToSendWs = isChangeDataToSendWs;
  },
  setDataToSendWs(state, dataToSendWs) {
    state.dataToSendWs = dataToSendWs;
  },
  setWsData(state, wsData) {
    state.wsData = wsData;
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
  setIdUser(state, idUser) {
    state.idUser = idUser;
  },
  setReturnListDirFiles(state, returnListDirFiles) {
    state.returnListDirFiles = returnListDirFiles;
  },
};

const actions = {};

const modules = {};

const getters = {
  getToken() {
    return state.token;
  },
  getReturnListDirFiles() {
    return state.returnListDirFiles;
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
  getWsData() {
    return state.wsData;
  },
  getHost_ws() {
    return state.host_ws;
  },
  getIdUser() {
    return state.idUser;
  },
  getDataToSendWs() {
    return state.dataToSendWs;
  },
  getIsChangeDataToSendWs() {
    return state.isChangeDataToSendWs;
  },
};

export default new Vuex.Store({
  state,
  mutations,
  actions,
  modules,
  getters,
});
