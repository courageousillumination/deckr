from lettuce import *
from lettuce.django import django_url

from selenium import webdriver

import lettuce_webdriver.webdriver
import lettuce_webdriver.django


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
