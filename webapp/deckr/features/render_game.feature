Feature: Render game

    @skip
    Scenario: Render new game
        Given I create a game room
        Then I should see the game