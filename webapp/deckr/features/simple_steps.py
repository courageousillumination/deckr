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

@step(u'I create a game room for "([^"]*)"')
def create_game_room(step, game):
    step.given('I visit site page "/new_game_room/"')
    step.given('I select "{0}" from "game_id"'.format(game))
    step.given('I click "Create game room"')
    world.game_room_id = world.browser.current_url.split('/')[-2]

@world.absorb
@step(u'I enter game with nickname "([^"]*)"')
def enter_game(step, nickname):
    step.given('I fill in "nickname" with "{0}"'.format(nickname))
    step.given('I click "Choose nickname"')

@step(u'I start the game')
def start_game(step):
    step.given('I click "Start"')


@step(u'my friend joins my game with nickname "([^"]*)"')
def my_friend_joins_my_game(step, nickname):
    step.given('I visit site page "/game_room_staging_area/{0}"'.format(
        world.game_room_id))
    enter_game(step, "Tester2")


@step(u'number of players in my game room should be "([^"]*)"')
def confirm_connected_players(step, n):
    player_names = world.browser.find_element_by_id("player-names")
    n_players = len(player_names.find_elements_by_tag_name("li"))
    assert n_players == int(n)

@step(u'Then "([^"]*)" cards should be rendered')
def n_cards_should_be_rendered(step, n):
    n_cards = len(world.browser.find_elements_by_class_name('card'))
    assert n_cards == int(n)


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
