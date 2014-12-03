# Playing a Game

## Creating a Game Room

To initiate a game, navigate to the home page (this can be found [here](http://deckr.mooo.com) for the live instance, or at localhost:8000 for your own instance). Select "Create New Game Room". From the dropdown, select the game you want to play, and click "Create Game Room". You will be taken to a screen where you can set a nickname for yourself. (If you would like to invite other players or spectators, copy the link at the bottom of the screen now.) Enter a name and click "Choose Nickname". You will be taken to the game room you created.

## Beginning the Game

If you have selected a multiplayer game such as Hearts or Dominion, you will need to wait for other players to join before you may begin the game. To invite other players, simply send them the link you copied in the staging area. If you have lost this link, see the [FAQ](#faq). Once enough players have joined, anyone in the room may press "Start Game" to begin the game.

## Joining a Game as a Player

Assuming the game has not started yet, navigate to the invite link provided to you by the player who created the game room. Enter a nickname here and press "Choose Nickname". Make sure that you pick a nickname that no other player in the game room has already chosen. Also, make sure there is room for you to join in the game.

## Joining a Game as a Spectator

You may join as a spectator whether or not a game has begun. To do so, navigate to the invite link provided by the person who created the game room. Without entering a nickname, press "Join as Spectator". You will be taken to the game room, but you will be unable to participate in the game. You may, however, participate in the chat.

## Games

Once you have selected "Start Game", cards will be dealt to all the players. What happens next depends on the game.

### Solitaire

To move a card, first click the card, then click where you would like to place the card. To move a stack of cards, click the highest card in the stack. For example, if you have a stack of cards 4♦-3♠︎-2♥︎, you should select the 4♦.

To flip over a card from the deck at the top left, click the deck. If all of the cards in the deck have been flipped, click the empty space where the deck was to restore it.

### Hearts

Rules [here](http://www.bicyclecards.com/card-games/rule/hearts).

To play a card, click the card you would like to play, then click the large board in the center of the game. The game's action feed will notify you when it is your turn. It will also notify you when special actions need to be made.

To take the cards in the center when you win a trick, simply click the board in the center or any of the cards there. All cards will be awarded to you.

### Dominion

Rules [here](http://riograndegames.com/getFile.php?id=348).
Card information [here](http://dominionstrategy.com/card-lists/dominion-card-list/).

When you start the game, a player will be selected to go first. The acion feed with indicate this, and the game will notify the player.

To end your current phase and move to the next phase, press the button at the top of the screen that reads either "Buy Phase" or "End Turn". 

Certain action cards require more information. This may be information from the player who has played the card (for instance, choosing a card to trash), from the other players (for instance, requiring them to discard or reveal cards), or from both. To resolve these cards, select the cards you would like to perform the action on, then press "Send Info" to tell the game that you have chosen. The game will wait until everyone has sent info, if necessary. The action feed with notify players when further action is required.

Some action cards will require input from other players (such as revealing a Moat when playing an attack). At the moment, the UI doesn't notify the attacking player that a moat has been revealed, despite the server knowing this. The easiest way to verify that your moat has worked is to open the chat and ask other players, or to try to move on with other actions or switching to your buy phase.

## Chatting

To chat with other players, select the chat icon at the top right of the game room screen. Enter whatever you'd like to say into the bottom-most box, then press "Send Message".