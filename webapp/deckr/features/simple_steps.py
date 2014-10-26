from lettuce import *
from lettuce.django import django_url

from selenium import webdriver

@before.all
def create_browser():
    world.browser = webdriver.Firefox()
    
@after.all
def destroy_browser(results):
    world.browser.close()
    
@step(r'I access the url "(.*)"')
def go_to_url(step, url):
    world.browser.get(django_url(url))
    
@step(r'the page should contain "(.*)"')
def page_should_contain(step, text):
    assert text in world.browser.page_source