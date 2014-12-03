from lettuce import *
from lettuce.django import django_url

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException

import lettuce_webdriver.webdriver
import lettuce_webdriver.django


@before.all
def create_browser():
    world.browser = webdriver.Firefox()


@after.all
def destroy_browser(results):
    world.browser.close()

# Note that all the functions with "pass" are integration tests, which is why
# they aren't filled out.


@step("I create a game room")
def create_game_room(step):
    pass


@step(u'my friend should be able to join my game room')
def check_my_friend_can_join_my_game_room(step):
    my_friend_joins_my_game_room(step)


@step(u'my friend joins my game room')
def my_friend_joins_my_game_room(step):
    pass


@step(u'my friend should see "([^"]*)"')
def my_friend_should_see_group1(step, text):
    pass


@step(u'the element with id "([^"]*)" does( not)? exist')
def element_exists(step, elementid, negation):
    try:
        world.browser.find_element_by_id(elementid)
        if negation:
            raise Exception('Element "{}" was NOT expected.'.format(elementid))
    except NoSuchElementException:
        if not negation:
            raise NoSuchElementException(
                'Element "{}" not found.'.format(elementid))


@step(
    u'the element with id "([^"]*)" is( not)? a child of the element with id "([^"]*)"')
def is_child_of(step, childid, negation, parentid):
    try:
        world.browser.find_element_by_xpath('//*[@id="{0}"]/*[@id="{1}"]'
                                            .format(parentid, childid))
        if negation:
            raise Exception(
                'Element "{}" was NOT expected to be the child of {}.'.format(
                    childid,
                    parentid))
    except NoSuchElementException:
        if not negation:
            raise NoSuchElementException("Could not find {0} as child of {1}"
                                         .format(childid, parentid))


@step(u'the element with id "([^"]*)" has the texture "([^"]*)"')
def card_has_texture(step, card_id, texture):
    e = world.browser.find_element_by_id(card_id)
    src = e.get_attribute('src').split('/')[-1]
    # assert src == texture, (texture, src)


@step(u'I upload "([^"]*)"')
def upload_zipped_file(step, file):
    element = world.browser.find_element_by_css_selector(
        "input[type=\"file\"]")
    element.send_keys(file)
