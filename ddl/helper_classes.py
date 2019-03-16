"""
A place for any and all useful helper classes that we might Create
but not intend to be part of the actual toolchainself.
"""

from ddl.asset import ComponentAsset
from ddl.renderer import Renderer


class ComponentFactory:
    """A class to help build componentss in-console.
    Needs to know an assetpack that it's using and co-ordinate information."""
    def __init__(self, assetpack, projection):
        self.assetpack = assetpack
        self.projection = projection
        self.clear_component()

    def change_assetpack(self, assetpack):
        """Checks a new assetpack can be used to build this component, then
         switches assetpack. Mostly used for A/B testing how components
         render"""
        for sub_asset in self.sub_assets:
            if sub_asset["type"] == "image":
                if sub_asset["image_id"] not in assetpack.images.keys():
                    raise Exception('Assetpack missing image %s',
                                    sub_asset["image_id"])
            if sub_asset["type"] == "component":
                if sub_asset["component_id"] not in\
                 assetpack.components.keys():
                    raise Exception('Assetpack missing component %s',
                                    sub_asset["component_id"])
        self.assetpack = assetpack

    def new_component(self, component_id, name='', tags=None, parts=None):
        """Initialises a new, empty component. All component parameters can
         be set using this method, so it's possible to 'copy' another component
        . Cannot be used twice if another component is under construction."""
        if self.current_component:
            raise Exception('''This factory is currently building another
 component. Please finalise that asset before starting a new one.''')
        self.current_component = True
        tags = [] if tags is None else tags
        parts = [] if parts is None else parts
        data = {
            "name": name,
            "id": component_id,
            "parts": parts,
            "tags": tags
        }
        self.component = ComponentAsset(data, self.assetpack.name)

    def add_image(self, image_id, x_coordinate, y_coordinate,
                  assetpack_name=None):
        """Adds a specific image asset to the component at grid co-ordinates
         x and y."""
        if assetpack_name is None:
            assetpack_name = self.assetpack.name
        image_key = assetpack_name+'.'+image_id
        if image_key not in self.assetpack.images.keys():
            raise Exception('This image ID doesnt exist in this assetpack.')
        image = self.assetpack.images[image_key]
        self.component.add_image(image, x_coordinate, y_coordinate)

    def add_component(self, component_id, x_coordinate, y_coordinate,
                      assetpack_name=None):
        """Adds a specific component to the component at grid co-ordinates
         x and y."""
        if assetpack_name is None:
            assetpack_name = self.assetpack.name
        component_key = assetpack_name+'.'+component_id
        if component_key not in self.assetpack.components.keys():
            raise Exception('This component ID isn\'t in this assetpack.')
        component = self.assetpack.components[component_key]
        self.component.add_component(component, x_coordinate, y_coordinate)

    def remove_last_part(self):
        """Removes the last part (and therefore all it's sub-parts)."""
        self.component.remove_last_part()

    def get_component(self):
        """Creates and returns the component without clearing the factory."""
        return self.component

    def print_component(self):
        """Prints the component in json without clearing the factory."""
        print(self.component.get_json())

    def clear_component(self):
        """Clears the factory to begin building a new component."""
        self.current_component = False
        self.component = None

    def pull_component(self):
        """Creates and returns the component and clears the factory"""
        image_list = self.get_component()
        self.clear_component()
        return image_list

    def output_component(self, destination='screen', filename=None):
        """Sets up a locator and a renderer and renders the current component.
         Can take many shortcuts as it knows it's own assetpack/grid.
         Defaults to screen output, but can throw to file if needed."""
        image_location_list = self.assetpack.\
            get_image_location_list(0, 0, self.component)
        image_list = self.assetpack.projection.\
            get_image_pixel_list(0, 0, image_location_list)
        Renderer(image_list).output(destination, filename)
