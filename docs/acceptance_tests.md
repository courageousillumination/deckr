##Acceptance Tests

######Test 1
* **Input**: Click "Create new game room".
* **Output**: Transition to game creation screen.

######Test 2
* **Input**: Select nothing from the drop-down, then click "Create game room".
* **Output**: A message stating that this field is required.

######Test 3
* **Input**: Select "Solitaire" from drop-down. Click "Create game room".
* **Output**: Transition to "Set Nickname" screen.

######Test 4
* **Input**: Enter nothing into the text field. Click "change name".
* **Output**: Message appears stating that this field is required.

######Test 5
* **Input**: Enter a nickname into the text field.
* **Output**: Transition to the game room.

######Test 6
* **Input**: Click start.
* **Output**: The game field is populated with cards in solitaire layout.

######Test 7
* **Input**: Click the deck.
* **Output**: A card is flipped over next to the deck.

######Test 8
* **Input**: Click on a face-up card in the field of play.
* **Output**: Yellow border appears around card.

######Test 9
* **Input**: Click on another face-up card in the field of play.
* **Output**: If move is legal, the card selected first moves to be in front of the card selected second. If move is illegal, nothing happens.

######Test 10
* **Input**: Click an ace, then click the victory zone.
* **Output**: Selected ace moves to the victory zone.

######Test 11
* **Input**: Flip over cards in the deck until the deck is empty. Click empty deck space.
* **Output**: Flipped cards return to the deck.

######Test 12
* **Input**: Click a card that is flipped over.
* **Output**: Nothing happens.

######Test 13
* **Input**: Make moves until the game is won.
* **Output**: Game concludes with a message notifying the user of victory.

######Test 14
* **Input**: Click "End Game".
* **Output**: Transition to main page.

######Test 15
* **Input**: Click "Leave Game".
* **Output**: Transition to main page.

#####Test Sequence 1 (Hearts Set-Up)
######Test 16
* **Input**: Navigate to the main page, select “Create a Game Room”, and select “Hearts”. In another tab, copy the staging room link. Enter a username into the textbox on each tab (these must be different names; alternatively, find a friend to open the site on their own machine), and in each tab click “Choose Nickname”.
* **Output**: You will be taken to a page with the Hearts game board.

######Test 17
* **Input**: Select “start game”.
* **Output**: In each tab, your hand will be populated with playing cards. The event feed (click the chat icon to view this) will display the nickname of the player who began the game.

######Test 18
* **Input**: Click on the Two of Clubs in the hand of whichever player happens to hold it.
* **Output**: The Two of Clubs will be moved from the player’s hand to the game board. The action feed will display the player’s nickname and state that you have played the Two of Clubs.

######Test 19
* **Input**: Click on another card of the suit clubs in the hand of the player who did not play the first card.
* **Output**: The card you click will move to the game board. The action feed will display the player’s nickname and state that you have played this card.

######Test 20
* **Input**:  In the tab for whoever played the higher card (this will necessarily be the second player), click on one of the cards on the game board.
* **Output**: All cards on the game board will move to that player’s discard pile.  The action feed will display the player’s nickname and state that you have won these cards.


#####Test Sequence 2 (Hearts Extras)
######Test 21
* **Input**: Start a game of hearts as above, with as many players as you’d like. Have one of these players win the game.
* **Output**: The game will announce that this player has won.
Test Sequence 3 (Dominion Set-Up)

######Test 22
* **Input**: Navigate to the main page, select “Create a Game Room”, and select “Dominion”. In another tab, copy the staging room link. Enter a username into the textbox on each tab (these must be different names; alternatively, find a friend to open the site on their own machine), and in each tab click “Choose Nickname”.
* **Output**: You will be taken to a page with the Dominion game board.

######Test 23
* **Input**: Select “start game”.
* **Output**: The gameboard in each tab (or on each machine) will be populated with cards, as will your hand and deck. The action feed (click the chat icon to view this) will display the nickname of the player who began the game, the nickname of the player who goes first, and the current phase of the player’s turn (“action phase”).

######Test 24
* **Input**: Select “next phase”.
* **Output**: The action feed will display the game’s new phase (“buy phase”).

######Test 25
* **Input**: Click on each treasure card in your hand. These are the gold cards with coins displayed on them.
* **Output**: The treasure cards clicked will move to the play zone, the area directly above your hand.

######Test 26
* **Input**: Click “next phase”.
* **Output**: The action feed will display that it is now the other player’s turn and will note the current phase of their turn (“action phase”).

#####Test Sequence 4 (Dominion Extras)
######Test 27
* **Input**: While in a game of Dominion, gain enough treasure to buy an Action card, buy the card, and play it when you next have a chance (this is when the Action card is in your hand and you are in Action Phase).
* **Output**: The Action card will appear in your play zone. The action feed will state what card you have played.

######Test 28
* **Input**: If the card necessitates discarding/trashing a card or choosing other players’ cards to take/discard/trash, select the cards you want and press “Send Info”. If other players must choose cards, the game will wait for them to do so.
* **Output**: The actions performed by you and other players will be logged in the action feed.

######Test 29
* **Input**: If the action card you played grants you more actions, you may choose to play another action card now.
* **Output**: The effect of whatever action card you play will take place as outlined in the previous steps.

######Test 30
* **Input**: If your action card gives you more coins, switch to buy phase, and attempt to buy something that requires these extra coins.
* **Output**: You will buy the card.

######Test 31
* **Input**: Win a game of Dominion.
* **Output**: The game will announce that you have won.

#####Test Sequence 5 (Chat)
######Test 32
* **Input**: While in a game, press the chat icon near the upper right hand corner.
* **Output**: A sidebar with chat input and output boxes will appear on the right side of the screen.

######Test 33
* **Input**: Type a message in the chat input box, press “Send Message.”
* **Output**: Your message appears in the chat output box, with your username prepended. The same appears in all other users’ chat boxes, if they are displayed.
Test Sequence 6 (Solitaire)

######Test 34
* **Input**: Navigate to the main page, select “Create a Game Room”, and select “Solitaire.”Enter a username into the textbox.
* **Output**: You are redirected to the game room.

######Test 35
* **Input**: Press “Start.”
* **Output**: The start button disappears, and a standard game of klondike solitaire is dealt.

######Test 36
* **Input**: Select a card in the main play area.
* **Output**: The card is highlighted in yellow.

######Test 37
* **Input**: After selecting a card in the main play area, click on a card of the opposite color and one value point higher that is completely visible in the main area, not occluded (e.g. if you selected a red seven, click on a black eight, or if you selected a red ten, click on a black jack).
* **Output**: The initially selected card moves on top of the clicked card, and no longer has its highlighting.

######Test 38
* **Input**: Click on the deck (in the upper left corner of the table).
* **Output**: A new card appears on the flipped deck. If that was the only card in the deck, then the deck is now empty.

#####Test Sequence 7 (Upload a game)
######Test 39
* **Input**: Create a .zip archive containing the files described on the “Upload new game” page. Each of the files should follow the examples of the existing games.
* **Output**: A new entry with the same name will appear on the “Create game room” dropdown menu. This game should play as expected.

#####Test Sequence 8 (Spectator)
######Test 40
* **Input**: Create a game room for any game, and click “Join as Spectator”. You can choose to add real players to the game by copying the link at the bottom of the staging area to another tab, inputting a nickname, and pressing “Choose Nickname”.
* **Output**: You will be taken to the game room, but you will not be able to perform any actions. Your nickname will be displayed as “Spectator”. Any actions made by the players in the room will be displayed to you in the same way it is displayed to them, but you will not see anyone’s hand.
