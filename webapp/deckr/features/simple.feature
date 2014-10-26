Feature: The webapp is awesome

    Scenario: Saying Hello World
        Given I access the url "/"
        Then the page should contain "Hello World"