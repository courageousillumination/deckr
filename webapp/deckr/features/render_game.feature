Feature: Render game

    Scenario: Render Solitaire
        Given I create a game room for "Solitaire"
        And I enter game with nickname "Tester"
        And I start the game
        Then "52" cards should be rendered