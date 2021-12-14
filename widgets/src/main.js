import Vue from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify';

import SimputStandin from './components/SimputStandin';
Vue.config.productionTip = false;

Vue.component('SimputStandin', SimputStandin);

new Vue({ vuetify, render: (h) => h(App) }).$mount('#app');
