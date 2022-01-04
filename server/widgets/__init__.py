from trame.internal.app import get_app_instance
import widgets.components as components

from widgets.widgets.domain import domain
from widgets.widgets.project_generation import project_generation

# Client initialization for Vue components
get_app_instance().enable_module(components)

# Re-expose Vue components
FileDatabase = components.FileDatabase
NavigationDropDown = components.NavigationDropDown

# Re-expose Trame widgets
Domain = domain
ProjectGeneration = project_generation
