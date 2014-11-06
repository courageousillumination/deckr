Feature: Render game

    Scenario: I am sane
        Given I visit site page "/"
        Then I should not see "Cthulu knows."
        And Just testing "Somethingelse"

    Scenario: Add div directly
        Given I visit site page "/"
        Then javascript adds a div to "gamespace" with class "region row" and id "region0"
        Then the element with id "region0" exists
        And the element with id "region0" is a child of the element with id "gamespace"

    Scenario: Add card directly
        Given I visit site page "/"
        Then javascript adds a div to "gamespace" with class "region row" and id "region0"
        Then the element with id "region0" is a child of the element with id "gamespace"
        Then javascript adds a div to "region0" with class "vertical-span zone" and id "zone0"
        Then the element with id "zone0" is a child of the element with id "region0"
        Then javascript adds a card to "zone0" with attributes "{'id':'card0', 'class':'vertical-spread card', src:'static/deckr/cards/1.png'}"
        Then the element with id "card0" is a child of the element with id "zone0"

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