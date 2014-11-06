Feature: Game Room

    @skip
    Scenario: Create a game room
        Given I visit site page "/create_game/"
        When I select "Test Game" from "Games"
        And I press "Submit"
        Then the browser's URL should contain "room/"
    
    @skip
    Scenario: Destroy a game room
        Give I create a game room for "Test Game"
        When I press "Destroy Room"
        And I confirm
        Then I should be at site page "/"
    
    @skip    
    Scenario: Multiple players in a room
        Given I create a game room for "Test Game"
        Then My friend should be able to visit my room
        
    @skip
    Scenario: Make valid game action
        Given I create a game room for "Test Game"
        When I make a valid move
        Then I should see "Made action" within 2 seconds
        
    @skip
    Scenario: Make invalid game action
        Given I create a game room for "Test Game"
        When I make an invalid move
        Then I should see "Error" within 2 seconds