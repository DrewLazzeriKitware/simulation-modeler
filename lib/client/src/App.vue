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
      <OverlayDatabaseErrors 
        v-if="mock.NavigationDropDown.currentView.view === 'Simulation Type'" 
        :errors="mock.OverlayDatabaseErrors.errors"
        :workingDirectory="mock.OverlayDatabaseErrors.workingDirectory"
        :fileDB="mock.OverlayDatabaseErrors.fileDB"
      />
      <FileDatabase
        v-if="mock.NavigationDropDown.currentView.view === 'File Database'" 
        :files="mock.FileDatabase.files"
      />
    </v-main>
  </v-app>
</template>

<script>
import SimulationType from './components/SimulationType';
import NavigationDropDown from './components/NavigationDropDown'
import OverlayDatabaseErrors from './components/OverlayDatabaseErrors'
import FileDatabase from './components/FileDatabase'
import MockData from './MockData'

export default {
  name: 'App',

  components: {
    // Views
    FileDatabase,
    SimulationType,

    // Helpers
    NavigationDropDown,
    OverlayDatabaseErrors,
  },

  data: () => ({
    mock: MockData
  }),
};
</script>
