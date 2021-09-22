<template>
  <v-app>
    <v-app-bar app >
    <div class="text-h6"> Parflow Web </div>
    <v-spacer />
    <NavigationDropDown />
    <v-spacer />
    </v-app-bar>

    <v-main>
      <SimulationType :shortcuts="mock.SimulationType.shortcuts"/>
    </v-main>
  </v-app>
</template>

<script>
import SimulationType from './components/SimulationType';
import NavigationDropDown from './components/NavigationDropDown'
import MockData from './MockData'

export default {
  name: 'App',

  components: {
    SimulationType,
    NavigationDropDown 
  },

  data: () => ({
    mock: MockData
  }),
};
</script>
