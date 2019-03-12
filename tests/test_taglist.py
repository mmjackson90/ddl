"""Tests TagList"""

from ddl.taglist import TagList


class FakeComponent:
    """A fake component"""
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

    def get_full_id(self):
        """Fake ID function that simply returns this instance's name"""
        return (self.name)


def test_add_component_to_tag():
    """Checks adding a component name to a tag functions as expected"""
    taglist = TagList()
    taglist.add_component_to_tag("test", "component1")
    taglist.add_component_to_tag("test", "component2")
    taglist.add_component_to_tag("test2", "component3")
    if not len(taglist.tag_components["test"]) == 2:
        raise AssertionError()
    if not len(taglist.tag_components["test2"]) == 1:
        raise AssertionError()
    # The hell is this syntax?
    if "component1" and "component2" not in taglist.tag_components["test"]:
        raise AssertionError()


def combined_component_check(tag_components):
    """
    Runs checks on component lists that are meant to include combinations of
    component and tag. This is a measure to have tidy code.
    """
    if "tag1" and "tag2" and "tag3" not in tag_components.keys():
        raise AssertionError(tag_components.keys())
    if "component1" and "component2" not in tag_components["tag2"]:
        raise AssertionError()
    if not len(tag_components["tag1"]) == 1:
        raise AssertionError()
    if not len(tag_components["tag2"]) == 2:
        raise AssertionError()
    if not len(tag_components["tag3"]) == 1:
        raise AssertionError()


def test_add_component():
    """
    Checks that adding components modifies the tag_component list correctly.
    """
    component1 = FakeComponent("component1", ['tag1', 'tag2'])
    component2 = FakeComponent("component2", ['tag2', 'tag3'])
    taglist = TagList()
    taglist.add_component(component1)
    taglist.add_component(component2)
    combined_component_check(taglist.tag_components)


def test_append_taglist():
    """
    Checks that appending taglists works correctly and is commutative.
    """
    component1 = FakeComponent("component1", ['tag1', 'tag2'])
    component2 = FakeComponent("component2", ['tag2', 'tag3'])
    taglist1 = TagList()
    taglist1.add_component(component1)
    taglist2 = TagList()
    taglist2.add_component(component2)
    taglist1.append(taglist2)
    taglist2.append(taglist1)
    combined_component_check(taglist1.tag_components)
    combined_component_check(taglist2.tag_components)


def test_get_component_list():
    """
    Checks that getting component lists given a set of tags works correctly.
    """
    component1 = FakeComponent("component1", ['tag1', 'tag2'])
    component2 = FakeComponent("component2", ['tag2', 'tag3'])
    taglist = TagList()
    taglist.add_component(component1)
    taglist.add_component(component2)
    if not len(taglist.get_components_that_match_tags(["tag1"])) == 1:
        raise AssertionError()
    if "component1" not in taglist.get_components_that_match_tags(["tag1"]):
        raise AssertionError()
    if not len(taglist.get_components_that_match_tags(["tag2"])) == 2:
        raise AssertionError()

    double_tag_list = taglist.get_components_that_match_tags(["tag2", "tag3"])
    if not len(double_tag_list) == 1:
        raise AssertionError()
    if "component2" not in double_tag_list:
        raise AssertionError()

    if not len(taglist.get_components_that_match_tags(["tag_umpt"])) == 0:
        raise AssertionError()
    if not len(taglist.get_components_that_match_tags(["tag1",
                                                       "tag2",
                                                       "tag3"])) == 0:
        raise AssertionError()
