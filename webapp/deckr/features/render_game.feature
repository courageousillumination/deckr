Feature: Render game

    Scenario: Add div directly
        Given I visit site page "/test_game"
        Then javascript adds a div to "gamespace" with class "region row" and id "region0"
        Then the element with id "region0" does exist
        And the element with id "region0" is a child of the element with id "gamespace"

    Scenario: Add card directly
        Given I visit site page "/test_game"
        Then javascript adds a div to "gamespace" with class "region row" and id "region0"
        Then the element with id "region0" is a child of the element with id "gamespace"
        Then javascript adds a div to "region0" with class "vertical-span zone" and id "zone0"
        Then the element with id "zone0" is a child of the element with id "region0"
        Then javascript adds a card to "zone0" with attributes "{'id':'card0', 'class':'vertical-spread card', src:'static/deckr/cards/1.png'}"
        Then the element with id "card0" is a child of the element with id "zone0"

    Scenario: Reject duplicate card id
        Given I visit site page "/test_game"
        Then javascript adds a div to "gamespace" with class "region row" and id "region0"
        Then the element with id "region0" is a child of the element with id "gamespace"
        Then javascript adds a div to "region0" with class "vertical-span zone" and id "zone0"
        Then the element with id "zone0" is a child of the element with id "region0"
        Then javascript adds a card to "zone0" with attributes "{'id':'card0', 'class':'vertical-spread card', src:'static/deckr/cards/1.png'}"
        Then the element with id "card0" is a child of the element with id "zone0"
        Then javascript adds a div to "region0" with class "vertical-span zone" and id "zone1"
        Then the element with id "zone1" is a child of the element with id "region0"
        Then javascript adds a card to "zone1" with attributes "{'id':'card0', 'class':'vertical-spread card', src:'static/deckr/cards/1.png'}"
        Then the element with id "card0" is not a child of the element with id "zone1"

    Scenario Outline: Move card
        Given I visit site page "/test_game"
        Then javascript adds a div to "gamespace" with class "region row" and id "region0"
        Then the element with id "region0" is a child of the element with id "gamespace"
        Then javascript adds a div to "region0" with class "vertical-span zone" and id "zone0"
        Then the element with id "zone0" is a child of the element with id "region0"
        Then javascript adds a card to "zone0" with attributes "{'id':'card0', 'class':'vertical-spread card', src:'static/deckr/cards/1.png'}"
        Then the element with id "card0" is a child of the element with id "zone0"
        Then javascript adds a card to "zone0" with attributes "{'id':'card1', 'class':'vertical-spread card', src:'static/deckr/cards/2.png'}"
        Then the element with id "card1" is a child of the element with id "zone0"
        Then javascript adds a div to "region0" with class "vertical-span zone" and id "zone1"
        Then the element with id "zone1" is a child of the element with id "region0"
        And the element with id "zone0" is a child of the element with id "region0"
        Then javascript moves the card "<card>" to the zone "<tgt_zone>"
        Then the element with id "<card>" <tgt_result> a child of the element with id "<tgt_zone>"
        And the element with id "<card>" <src_result> a child of the element with id "<src_zone>"

    Examples:
        | card  | src_zone  | tgt_zone  | src_result    | tgt_result    |
        | card1 | zone0     | zone1     | is not        | is            |
        | card0 | zone0     | zone1     | is not        | is            |
        | card1 | zone1     | zone0     | is not        | is            |
        | card1 | zone0     | zone0     | is            | is            |
        | card1 | zone0     | zone2     | is            | is not        |

    Scenario: Remove element by id
        Given I visit site page "/test_game"
        Then javascript adds a div to "gamespace" with class "region row" and id "region0"
        Then the element with id "region0" does exist
        And the element with id "region0" is a child of the element with id "gamespace"
        Then javascript removes the element with id "region0"
        Then the element with id "region0" does not exist

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