# FAQ

### Q: How do I get [package name]?

Make sure you have pip. To get pip, navigate [here](https://pip.pypa.io/en/latest/installing.html). Right-click the link to get-pip.py and save the target. In your shell, navigate to the folder where you downloaded the file and run

```
  python get-pip.py
```

Now you're ready to install other packages. To install one, simply run

```
  pip install [package-name]
```

You may need to use `sudo` to complete the install.
 
### Q: `pip install [name]` isn't working.

**A:** Try running `sudo pip install [name]` instead. You might have to enter your password.

### Q: I successfully installed everything, but later quit the shell. Which exact commands do I need to use to get the server running again?

**A:** Type the following into your shell:

```
  cd location_of_deckr_folder/deckr
  source venv/bin/activate
  cd webapp
```

From here you can run `make run`, `make test`, and so on.

### Q: I'm trying to move a card, but it's not working!

**A:** You cannot drag the cards. To move a card, make sure you first click the card, then click where you would like to go. Also be sure that you are making a legal action.

### Q: I'm trying to start the game, but nothing happens when I press "start".

**A:** To play Hearts or Dominion, there must be at least one other player in the game.

### Q: I forgot to copy the invite link. Can I get it back?

**A:** Yes! To figure out your invite link, simply look at the URL at the top of your game room. It should look something like

`(root_address)/game_room/(game_id_number)/?player_id=your_player_id`

An example is deckr.mooo.com/game_room/160/?player_id=3

 What you want is the game_id_number. The invite link that corresponds to your game_id_number is

`(root_address)/game_room_staging_area/(game_id_number)`

An example is deckr.mooo.com/game_room_staging_area/160

Simply replace (root_adress) with the address of the instance you are using (either deckr.mooo.com or localhost:8000) and replace (game_id_number) with the id number from your game room's URL. This is your invite link.

Alternatively, you could just use the "back" button, but if you've already begun the game and want to invite spectators, this is probably not a good idea.

### Q: I'm playing Dominion, but I'm not sure how to resolve the action on (some action card).

A: Certain cards require that all of the players discard or reveal something or that you choose cards to discard. To resolve these actions, you need to use the "Send Info" button at the top of the page. Select the cards you want to perform the action on, then press "Send Info" to tell the game that these are the cards you want to use. In the case where all players need to perform an action, no one will be able to proceed until every player has selected cards and pressed "Send Info".

### Q: Where is the chat?

**A:** At the top right of the game room screen, there is a picture of two chat bubbles. Clicking this will open the chat.

### Q: Where is the action feed?

**A:** Follow the directions above to open the chat. The action feed is displayed above the box where messages appear.

### Q: How can I see who else is playing?

**A:** Next to the chat icon is some text that reads "Players", followed by the number of players. Clicking this will allow you to see the nicknames of the other players.

### Q: The website layout looks a little bit off...

**A:** You might want to switch to Chrome. If you can't see any scrollbars in Hearts or Dominion, you may need to try zooming out.

## Known Issues

* Developers can't upload a set of card images with their game definitions
* No protection against malicious developers
* Hearts UI has not been beutified
* The UI for Hearts or Dominion looks weird when the window size is too small.