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