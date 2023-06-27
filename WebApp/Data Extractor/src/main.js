import "./assets/main.css";

import { createApp } from "vue";
import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import Vuex from "vuex";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);
const store = new Vuex.Store({
    state: {
        csvString: "",
    },
    plugins: [
        createPersistedState({
            paths: ["csvString"],
            storage: window.sessionStorage,
        }),
    ],
    mutations: {
      setCsvString: (state, payload) => {
        state.csvString = payload;
      }
    }
});

app.use(router);
app.use(store);
app.mount("#app");
