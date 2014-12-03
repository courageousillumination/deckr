Feature: Game Room

    Scenario: Create a game room
        Given I visit site page "/new_game_room/"
        When I select "Solitaire" from "game_id"
        And I click "Create game room"
        Then I should see "Your Game Room for Solitaire has been created!"
    
    Scenario: Destroy a game room
        Give I create a game room for "Solitaire"
        When I press "Destroy Room"
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