Feature: Game Room

    Scenario: Create a game room
        Given I create a game room for "Solitaire"
        Then I should see "Your Game Room for Solitaire has been created!"
    
    Scenario: Start a game
        Given I create a game room for "Solitaire"
        And I enter game with nickname "Tester"
        Then The browser's URL should contain "?player_id="

    # Probably want to test that the game room no longer exists
    Scenario: Destroy a game room
        Given I create a game room for "Solitaire"
        And I enter game with nickname "Tester"
        When I click "End Game"
        Then I should see "Welcome to Deckr"
    
    # Probably want to test that the game room still exists
    Scenario: Leave game room
        Given I create a game room for "Solitaire"
        And I enter game with nickname "Tester"
        When I click "End Game"
        Then I should see "Welcome to Deckr"

    Scenario: Multiple players in a room
        Given I create a game room for "Hearts"
        And I enter game with nickname "Tester1"
        And my friend joins my game with nickname "Tester2"
        Then the number of players in my game room should be "2"
        
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