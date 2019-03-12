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


def make_add_taglist():
    """
    Makes a taglist and adds some components to it.
    Really overloading the tests here, but hey.
    """
    component1 = FakeComponent("component1", ['tag1', 'tag2'])
    component2 = FakeComponent("component2", ['tag2', 'tag3'])
    taglist = TagList()
    taglist.add_component(component1)
    taglist.add_component(component2)
    return (taglist)


def test_add_component_right_tags():
    """
    Checks that adding components modifies the tag_component tags correctly.
    """
    tag_components = make_add_taglist().tag_components
    if "tag1" and "tag2" and "tag3" not in tag_components.keys():
        raise AssertionError(tag_components.keys())


def test_add_component_right_components():
    """
    Checks that adding components modifies the tag_component components
    correctly.
    """
    tag_components = make_add_taglist().tag_components
    if "component1" and "component2" not in tag_components["tag2"]:
        raise AssertionError()


def test_add_component_right_sizes():
    """
    Checks that adding components gives the right size sets back afterwards.
    """
    tag_components = make_add_taglist().tag_components
    if not len(tag_components["tag1"]) == 1:
        raise AssertionError()
    if not len(tag_components["tag2"]) == 2:
        raise AssertionError()
    if not len(tag_components["tag3"]) == 1:
        raise AssertionError()


def make_append_taglist():
    """
    Makes tow taglists and sticks them together.
    Really overloading the tests here, but hey.
    """
    component1 = FakeComponent("component1", ['tag1', 'tag2'])
    component2 = FakeComponent("component2", ['tag2', 'tag3'])
    taglist1 = TagList()
    taglist1.add_component(component1)
    taglist2 = TagList()
    taglist2.add_component(component2)
    taglist1.append(taglist2)
    return(taglist1)


def test_append_component_right_tags():
    """
    Checks that appending taglists modifies the tag_component tags correctly.
    """
    tag_components = make_append_taglist().tag_components
    if "tag1" and "tag2" and "tag3" not in tag_components.keys():
        raise AssertionError(tag_components.keys())


def test_append_component_right_components():
    """
    Checks that appending taglists modifies the tag_component components
    correctly.
    """
    tag_components = make_append_taglist().tag_components
    if "component1" and "component2" not in tag_components["tag2"]:
        raise AssertionError()


def test_append_component_right_sizes():
    """
    Checks that appending components gives the right size sets back afterwards.
    """
    tag_components = make_append_taglist().tag_components
    if not len(tag_components["tag1"]) == 1:
        raise AssertionError()
    if not len(tag_components["tag2"]) == 2:
        raise AssertionError()
    if not len(tag_components["tag3"]) == 1:
        raise AssertionError()


def test_get_list_single_tags_1():
    """
    Checks that getting component lists given a set of tags works correctly.
    This only checks a single tag at a time.
    """
    taglist = make_add_taglist()
    tag2_components = taglist.get_components_that_match_tags(["tag2"])
    if not len(taglist.get_components_that_match_tags(["tag1"])) == 1:
        raise AssertionError()
    if "component1" not in taglist.get_components_that_match_tags(["tag1"]):
        raise AssertionError()


def test_get_list_single_tags_1():
    """
    Checks that getting component lists given a set of tags works correctly.
    This only checks a single tag at a time.
    """
    taglist = make_add_taglist()
    tag2_components = taglist.get_components_that_match_tags(["tag2"])
    if not len(tag2_components) == 2:
        raise AssertionError()
    if "component1" not in tag2_components:
        raise AssertionError()
    if "component2" not in tag2_components:
        raise AssertionError()


def test_get_list_double_tags():
    """
    Checks that getting component lists given a set of tags works correctly.
    This test checks multiple tags return just the one component.
    """
    taglist = make_add_taglist()
    double_tag_list = taglist.get_components_that_match_tags(["tag2", "tag3"])
    if not len(double_tag_list) == 1:
        raise AssertionError()
    if "component2" not in double_tag_list:
        raise AssertionError()


def test_get_list_missing_tag():
    """
    Checks that getting component lists given a set of tags works correctly.
    This checks that a tag that isn't in the artpack returns an empty list.
    """
    taglist = make_add_taglist()
    if not len(taglist.get_components_that_match_tags(["tag_umpt"])) == 0:
        raise AssertionError()


def test_get_list_single_tags():
    """
    Checks that getting component lists given a set of tags works correctly.
    This tests that asking for a combination of tags that doesnt exist
    returns an empty list.
    """
    taglist = make_add_taglist()
    if not len(taglist.get_components_that_match_tags(["tag1",
                                                       "tag2",
                                                       "tag3"])) == 0:
        raise AssertionError()
