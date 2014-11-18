Feature: Upload Game Definition

    @skip
    Scenario: Upload a game definition
        Given I visit site page "/upload_game/"
        When I upload a zipped file for Solitaire
        And I press "Submit"
        Then the browser's URL should contain "/successful_upload"
