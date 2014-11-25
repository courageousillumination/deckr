Feature: Performing game actions

    @skip
    Scenario: Legal action
        Given I create a game room
        When I move "card1" to "zone1"
        Then "card1" should be in "zone1"

    @skip
    Scenario: Illegal action
        Given I create a game room
        When I move "card1" to "zone2"
        Then I should see "Error"

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