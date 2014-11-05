Feature: Render game

    @skip
    Scenario: Render new game
        Given I create a game room
        Then I should see the game

    @skip
    Scenario: Render textures
        Given I create a game room
        Then "card1" should have texture "card1.jpg"

    @skip
    Scenario: Win
        Given I create a game room
        When I move "card1" to "win_zone"
        Then I should see "You won"

    @skip
    Scenario: Lose
        Given I create a game room
        When I move "card1" to "lose_zone"
        Then I should see "You lose"