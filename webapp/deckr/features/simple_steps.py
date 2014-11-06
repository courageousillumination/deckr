from lettuce import *
from lettuce.django import django_url

from selenium import webdriver

import lettuce_webdriver.webdriver
import lettuce_webdriver.django

# Delete me.
import time


@before.all
def create_browser():
    world.browser = webdriver.Firefox()


@after.all
def destroy_browser(results):
    world.browser.close()


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
    world.browser.execute_script('addDiv("{0}", {{"id":"{1}", "class":"{2}"}})'
        .format(parentid, elementid, classname))

@step(u'the element with id "([^"]*)" exists')
def element_exists(step, elementid):
    if not world.browser.find_element_by_id(elementid):
        raise Exception('Element "{}" not found.'.format(elementid))

@step(u'the element with id "([^"]*)" is a child of the element with id "([^"]*)"')
def is_child_of(step, childid, parentid):
    world.browser.find_element_by_xpath('//*[@id="{0}"]/*[@id="{1}"]'.format(parentid, childid))
    
# The "attributes" is the lesser of two evils. Takes a dict with
# keys: id, class, src, among other optionals.
@step(u'javascript adds a card to "([^"]*)" with attributes "([^"]*)"')
def js_add_card(step, zoneid, card):
    world.browser.execute_script('addCard({0},"{1}")'.format(card, zoneid))

@step(u'javascript moves the card "([^"]*)" to the zone "([^"]*)"')
def js_move_card(step, cardid, zoneid):
    world.browser.execute_script('moveCard("{0}","{1}")'.format(cardid, zoneid))


@step(u'Just testing "([^"]*)"')
def just_testing(step, other):
    world.browser.execute_script('console.log("{}")'.format(other))