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
        :currentFileIndex="mock.FileDatabase.currentFileIndex"
      />
      <Domain
        v-if="mock.NavigationDropDown.currentView.view === 'Domain'" 
      />
      <BoundaryConditions
        v-if="mock.NavigationDropDown.currentView.view === 'Boundary Conditions'" 
      />
      <SubSurface
        v-if="mock.NavigationDropDown.currentView.view === 'Subsurface Properties'" 
      />
      <Solver 
        v-if="mock.NavigationDropDown.currentView.view === 'Solver'" 
      />
      <ProjectGeneration
        v-if="mock.NavigationDropDown.currentView.view === 'Project Generation'" 
        :validation="mock.ProjectGeneration.validation"
        />
    </v-main>
  </v-app>
</template>

<script>
import SimulationType from './components/SimulationType';
import NavigationDropDown from './components/NavigationDropDown'
import OverlayDatabaseErrors from './components/OverlayDatabaseErrors'
import FileDatabase from './components/FileDatabase'
import Domain from './components/Domain'
import BoundaryConditions from './components/BoundaryConditions'
import SubSurface from './components/SubSurface'
import Solver from './components/Solver'
import ProjectGeneration from './components/ProjectGeneration'

import MockData from './MockData'

export default {
  name: 'App',

  components: {
    // Views
    FileDatabase,
    SimulationType,
    Domain,
    BoundaryConditions,
    SubSurface,
    Solver,
    ProjectGeneration,

    // Helpers
    NavigationDropDown,
    OverlayDatabaseErrors,
  },

  data: () => ({
    mock: MockData
  }),
};
</script>
<style>

html {
  overflow: auto;
}

</style>
