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


@step(u'I should see the game')
def i_should_see_the_game(step):
    pass


@step(u'"([^"]*)" should have texture "([^"]*)"')
def card_should_have_texture(step, card, texture):
    pass


@step(u'I move "([^"]*)" to "([^"]*)"')
def i_move_card_to_zone(step, card, zone):
    pass


@step(u'"([^"]*)" should be in "([^"]*)"')
def check_card_in_zone(step, card, zone):
    pass

# Should be in separate file?
@step(u'javascript adds a div to "([^"]*)" with class "([^"]*)" and id "([^"]*)"')
def js_add_div(step, parentid, classname, elementid):
    world.browser.execute_script('addDiv("{0}", {{"id":"{1}", "class":"{2}"}});'
        .format(parentid, elementid, classname))

@step(u'the element with id "([^"]*)" does( not)? exist')
def element_exists(step, elementid, negation):
    try:
        world.browser.find_element_by_id(elementid)
        if negation:
            raise Exception('Element "{}" was NOT expected.'.format(elementid));
    except NoSuchElementException:
        if not negation:
            raise NoSuchElementException('Element "{}" not found.'.format(elementid))

@step(u'the element with id "([^"]*)" is( not)? a child of the element with id "([^"]*)"')
def is_child_of(step, childid, negation, parentid):
    try:
        world.browser.find_element_by_xpath('//*[@id="{0}"]/*[@id="{1}"]'
            .format(parentid, childid))
        if negation:
            raise Exception('Element "{}" was NOT expected to be the child of {}.'.format(childid, parentid));
    except NoSuchElementException:
        if not negation:
            raise NoSuchElementException("Could not find {0} as child of {1}"
                .format(childid, parentid))
    
# The "attributes" is the lesser of two evils. Takes a dict with
# keys: id, class, src, among other optionals.
@step(u'javascript adds a card to "([^"]*)" with attributes "([^"]*)"')
def js_add_card(step, zoneid, card):
    world.browser.execute_script('addCard({0},"{1}");'.format(card, zoneid))

@step(u'javascript (does not move|moves) the card "([^"]*)" to the zone "([^"]*)"')
def js_move_card(step, condition, cardid, zoneid):
    try:
        world.browser.execute_script('moveCard("{0}","{1}");'.format(cardid, zoneid))
    except WebDriverException:
        if condition != "does not move":
            raise 


@step(u'javascript removes the element with id "([^"]*)"')
def js_remove_element_by_id(step, elementid):
    world.browser.execute_script('removeElementById("{0}");'.format(elementid))