"""Adds a class to store and retrieve names of components, given their tags"""


class TagList:
    """
    A class that stores and retrieves names of components given their
    tag lists. Basically a fancy lookup class for faster/easier tag handling.
    """
    def __init__(self):
        self.tag_components = {}

    def add_component_to_tag(self, tag, component_id):
        """Adds a component ID to the list of components matching a tag"""
        self.tag_components.setdefault(tag, set()).add(component_id)

    def add_component(self, component):
        """
        Adds a component's ID to the tag_component list for all the
        component's tags.
        """
        component_id = component.get_full_id()
        for tag in component.tags:
            self.add_component_to_tag(tag, component_id)

    def append(self, taglist):
        """Sticks two taglists together"""
        tag_components = taglist.tag_components
        for tag, components in tag_components.items():
            self.tag_components.setdefault(tag,
                                           set()).update(components)

    def get_components_that_match_tags(self, tags):
        """
        For an array of tags, goes through and finds the ID of all components
        that match all tags. Returns an empty set if one of the tags is missing
        or if no component matches all tags.
        """
        for tag in tags:
            if tag not in self.tag_components.keys():
                return(set())

        good_components = self.tag_components[tags.pop(0)]
        for tag in tags:
            components = self.tag_components[tag]
            good_components = good_components.intersection(components)
        return(good_components)
