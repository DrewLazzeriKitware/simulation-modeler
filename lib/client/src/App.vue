<template>
  <v-app>
    <v-app-bar app >
    <div class="text-h6"> Parflow Web </div>
    <v-spacer />
    <NavigationDropDown 
      :currentView="mock.NavigationDropDown.currentView" 
      :views="mock.NavigationDropDown.views"/>
    <v-spacer />
    </v-app-bar>

    <v-main>
      <SimulationType 
        v-if="mock.NavigationDropDown.currentView.view === 'Simulation Type'" 
        :shortcuts="mock.SimulationType.shortcuts" 
      />
      <FileDatabaseErrors 
        v-if="mock.NavigationDropDown.currentView.view === 'Simulation Type'" 
        :errors="mock.FileDatabaseErrors.errors"
        :workingDirectory="mock.FileDatabaseErrors.workingDirectory"
        :fileDB="mock.FileDatabaseErrors.fileDB"
      />
    </v-main>
  </v-app>
</template>

<script>
import SimulationType from './components/SimulationType';
import NavigationDropDown from './components/NavigationDropDown'
import FileDatabaseErrors from './components/FileDatabaseErrors'
import MockData from './MockData'

export default {
  name: 'App',

  components: {
    SimulationType,
    NavigationDropDown,
    FileDatabaseErrors 
  },

  data: () => ({
    mock: MockData
  }),
};
</script>
