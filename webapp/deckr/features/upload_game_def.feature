Feature: Upload Game Definition

    Scenario: Upload a game definition
        Given I visit site page "/upload_game/"
        When I upload "solitaire.zip"
        And I press "Submit"
        Then the browser's URL should contain "/successful_upload"
