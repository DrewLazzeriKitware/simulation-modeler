from trame.html import vuetify, Element, Div, Span

# TODO Unpythonic
# How does python parameterize an instance?
def domain(selected_file_model, grid_models):
    domainGridRow = vuetify.VRow(classes="ma-6 justify-space-between")
    domainGrid = [Element("H1", "Indicator"), domainGridRow]
    with domainGridRow:
        with Div():
            vuetify.VSelect(
                v_model=(selected_file_model, ""),
                placeholder="Select an indicator file",
                items=("Object.values(dbFiles)",),
                item_text="name",
                item_value="id",
            )
            with vuetify.VRow():
                with vuetify.VCol():
                    vuetify.VTextField(
                        v_model=(grid_models["LX"], 1.0), label="lx", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["DX"], 1.0), label="dx", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["NX"], 1.0), label="nx", readonly=True
                    )
                with vuetify.VCol():
                    vuetify.VTextField(
                        v_model=(grid_models["LY"], 1.0), label="ly", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["DY"], 1.0), label="dy", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["NY"], 1.0), label="ny", readonly=True
                    )
                with vuetify.VCol():
                    vuetify.VTextField(
                        v_model=(grid_models["LZ"], 1.0), label="lz", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["DZ"], 1.0), label="dz", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["NZ"], 1.0), label="nz", readonly=True
                    )

        with Div(classes="ma-6"):
            Span("Lorem Ipsum documentation for Indicator file")
            vuetify.VTextarea(
                v_if="indicatorFileDescription",
                value=("indicatorFileDescription", ""),
                readonly=True,
                style="font-family: monospace;",
            )

    element = Div(
        classes="d-flex flex-column fill-height", v_if="currentView=='Domain'"
    )
    with element:
        with vuetify.VToolbar(
            flat=True, classes="fill-width align-center grey lighten-2 flex-grow-0"
        ):
            vuetify.VToolbarTitle("Domain Parameters")
            vuetify.VSpacer()
            with vuetify.VBtnToggle(rounded=True, mandatory=True):
                with vuetify.VBtn(small=True):
                    vuetify.VIcon("mdi-format-align-left", small=True, classes="mr-1")
                    Span("Parameters")
                with vuetify.VBtn(small=True):
                    vuetify.VIcon("mdi-eye", small=True, classes="mr-1")
                    Span("Preview")
        Div(
            domainGrid,
            classes="fill-height fill-width flex-grow-1 ma-6",
        )
    return element
