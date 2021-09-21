<template>
  <v-app>
    <v-app-bar app >
    <div class="text-h6"> Parflow Web </div>
    </v-app-bar>

    <v-main>
      <SimulationType :shortcuts="mock.SimulationType.shortcuts"/>
    </v-main>
  </v-app>
</template>

<script>
import SimulationType from './components/SimulationType';
import MockData from './MockData'

export default {
  name: 'App',

  components: {
    SimulationType,
  },

  data: () => ({
    mock: MockData
  }),
};
</script>
