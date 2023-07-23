# Nicholas' Rummy

Welcome to my Rummy implementation! This is a project of mine that will one day be capable of running a Rummy game that two players can play online.

Rummy is a game for two or more players in which the goal is to score the most points in various rounds. Players take turns drawing and playing cards, and they score by playing sets (3 or 4 of a kind) or runs (straight/sequence of 3 or more cards of the same suit, with aces possibly either preceding twos or succeeding kings).

## Playing

To start playing on Windows, simply click the "<> Code" button above and either clone the repository or download the ZIP file. Then, once you've navigated to the "rummy" folder, open the Command Prompt and run "python card-demo.py". This should open up a fullscreen window with the card game! You can play around with it, and whenever you're finished, click the "Exit game" button or press Alt+F4.

## Controls

- In general, left click means player 1 (bottom of screen) and right click means player 2 (top of screen).
- On startup, the program shuffles the deck, deals 7 cards to each player (alternating, of course, for those of you worried about bad luck!), and places a card faceup in the river in the middle.
### Buttons
- The "Shuffle deck" button clears the table and repeats the above.
- The "Sort player's hand" sorts the specified player's hand (left or right click for player 1 or 2, respectively) in ascending order (aces treated as ones).
- The "Check play" button checks the specified player's highlighted cards and plays them if they form a valid play by themselves or with another play currently on the table.
- The "Rummy!" button causes the specified player to attempt to play the top card of the river.
- The "Enable/Disable auto sort" button toggles the setting to automatically sort the players' hands upon any action.
- The "Exit game" button closes the window and terminates the program.
### Clicking
- Left or right click the deck on the left to deal the top card to a player (the deck is always facedown).
- Left click a card in either player's hand to add it to the highlighted cards. Performing actions besides highlighting multiple cards in a single hand will clear the highlights.
- Right click a card in either player's hand to add it to the river.
- Left or right click a card in the river to add it and all following cards to the specified player's hand, assuming it will not bring their hand size above the maximum.

## Quirks in Nicholas' Rummy

There are some quirks about my game, either due to limitations or stylistic choice:
- Player hands and river can have maximum size 14 (changeable in the code).
- If you play off of a down set, you'll still get the points, but the card will appear in the played set (easier to implement).
- Able to call Rummy even if a player hasn't just played a card to the river (may fix in a later version, okay for now).

Questions? Feel free to contact me!