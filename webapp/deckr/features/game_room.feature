Feature: Game room

    @skip
    Scenario: Create new game room link exists
        Given I visit site page "/"
        Then I should see "Create new game room"
        
    @skip
    Scenario: Create new game room
        Given I visit site page "/new_game_room"
        When I select "Solitaire" from "Games"
        And I click "Create new game room"
        Then the browser's URL should contain "game_room"
        And the browser's URL should not contain "new_"

    @skip
    Scenario: Multiplayer
        Given I create a game room
        Then my friend should be able to join my game room

    @skip
    Scenario: Destroy game room
        Given I create a game room
        When I click "Destroy game room"
        Then I should be at "http://127.0.0.1:8000/"

    @skip
    Scenario: Multiplayer game room destruction notification
        Given I create a game room
        And my friend joins my game room
        When I click "Destroy game room"
        Then my friend should see "Game room has been destroyed by host"