Feature: Game Room

    Scenario: Create a game room
        Given I create a game room for "Solitaire"
        Then I should see "Your Game Room for Solitaire has been created!"
    
    Scenario: Start a game
        Given I create a game room for "Solitaire"
        And I start game
        Then The browser's URL should contain "?player_id="

    @skip
    Scenario: Destroy a game room
        Given I create a game room for "Solitaire"
        And I start game
        When I click "End Game"
        Then I should be at "/"
    
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