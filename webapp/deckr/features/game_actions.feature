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
