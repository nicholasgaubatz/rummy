# Reference: https://www.youtube.com/watch?v=xJZksz2UpqE&list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV&index=206
# Guide for basic card stuff

# TODO: Add the following functionalities:
# Push to GitHub before adding Rummy-specific routines
# Bot to control opponent, greedy and random approach
# Possibly: undo button
# Possibly: chage global variables to be dependent on client's window size
# Possibly: add sleep to slow down dealing (aesthetics) (use after())
# Possibly: change Q, K, A run to lay down in that order (add duplicate ace card files of name '14_...'?)

# Quirks about my game:
# Player hands and river can have maximum size 14 (changeable)
# If you play off of a down set, you'll still get the points, but the card will appear in the played set
# Rummy rule is a little weird; able to call Rummy even if a player hasn't just played a card to the river (may fix later if there's time and energy)

from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
import random

root = Tk()
root.title('Nicholas\' Rummy')
root.geometry("1200x700")
root.configure(background='green')
root.attributes('-fullscreen', True)

# Global variables
deck = []
player_hands = [[],[]]
river = []
player_hands_highlighted = [[],[]]
played = [[], []]

player_scores = [0, 0]
auto_sort_hand = False

# Max sizes allowed by fullscreen for card size of 100x144
river_max_size = 14
player_hand_max_size = 14
player_played_max_size = 60
card_image_size_large = (80,115) # original 100x144
card_image_size_small = (80, 115) # just in case we want to customize

my_frame = Frame(root, bg='green')
my_frame.pack(pady=10)

# Create frames for cards
#score_frame = Text(my_frame, font=('Helvetica', 12), width=20, height=4, bd=0, background='green') #TODO: fix
#score_frame.insert(INSERT, f'Player 1 score: {player_scores[0]}\n\nPlayer 2 score: {player_scores[1]}')
#score_frame.grid(row=0, column=0, padx=20)
score_frame = Label(my_frame, text=f'Player 1 score: {player_scores[0]}\n\nPlayer 2 score: {player_scores[1]}', font='Helvetica 12 bold', background='green')
score_frame.place(x=40, y=50)

player2_frame = LabelFrame(my_frame, text='Opponent', font=('Helvetica', 12), bd=0, background='green')
player2_frame.grid(row=0, column=1, padx=20, ipadx=20)

player2_played_frame = LabelFrame(my_frame, text='Player 2\'s played cards', font=('Helvetica', 12), bd=0, background='green')
player2_played_frame.grid(row=1, column=1, padx=20, ipadx=20)

deck_frame = LabelFrame(my_frame, text='Deck', font=('Helvetica', 12), bd=0, background='green')
deck_frame.grid(row=2, column=0, padx=20, ipadx=20)

river_frame = LabelFrame(my_frame, text='River', font=('Helvetica', 12), bd=0, background='green')
river_frame.grid(row=2, column=1, ipadx=20)

player1_played_frame = LabelFrame(my_frame, text='Player 1\'s played cards', font=('Helvetica', 12), bd=0, background='green')
player1_played_frame.grid(row=3, column=1, padx=20, ipadx=20)

button_frame = Frame(my_frame, background='green')
button_frame.grid(row=3, column=0, padx=20)

player1_frame = LabelFrame(my_frame, text='You', font=('Helvetica', 12), bd=0, background='green')
player1_frame.grid(row=4, column=1, padx=20, ipadx=20)

# Draw the table
def redraw_table():
    global river_labels, auto_sort_hand
    
    # Redraw deck with frame displaying number of cards left
    if len(deck)>0:
        deck_label.config(image=deck_image)
    else:
        deck_label.config(image=green_image_large)
    deck_frame.config(text=f'\nCard Deck Demo - \n{len(deck)} cards remaining')

    if auto_sort_hand:
        auto_sort_button.config(text='Disable auto sort')
    if not auto_sort_hand:
        auto_sort_button.config(text=' Enable auto sort')

    # Redraw river
    if len(river)==0:
        for r in river_labels:
            r.config(image=green_image_large)
    elif len(river)<=river_max_size:
        for i in range(len(river)):
            river_labels[i].config(image=river[i][0])
        for i in range(river_max_size-1, len(river)-1, -1):
            river_labels[i].config(image=green_image_large)

    # Redraw Player 1's hand TODO: condense this and following
    if len(player_hands[0])==0:
        for r in player1_labels:
            r.config(image=green_image_large)
    elif len(player_hands[0])<=player_hand_max_size:
        for i in range(len(player_hands[0])):
            if i in player_hands_highlighted[0]:
                player1_labels[i].config(image=player_hands[0][i][0], background='yellow')
            else:
                player1_labels[i].config(image=player_hands[0][i][0], background='green')
        for i in range(player_hand_max_size-1, len(player_hands[0])-1, -1):
            player1_labels[i].config(image=green_image_large, background='green')

    # Redraw Player 2's hand
    if len(player_hands[1])==0:
        for r in player2_labels:
            r.config(image=green_image_large)
    elif len(player_hands[1])<=player_hand_max_size:
        for i in range(len(player_hands[1])):
            if i in player_hands_highlighted[1]:
                player2_labels[i].config(image=player_hands[1][i][0], background='yellow')
            else:
                player2_labels[i].config(image=player_hands[1][i][0], background='green')
        for i in range(player_hand_max_size-1, len(player_hands[1])-1, -1):
            player2_labels[i].config(image=green_image_large, background='green')

    # Redraw Player 1's played cards
    if len(played[0])==0:
        for r in player1_played_labels:
            r.config(image=green_image_small)
    elif len(played[0])<=player_played_max_size:
        current_spot = 0
        for i in range(len(played[0])):
            for j in range(len(played[0][i])):
                player1_played_labels[current_spot].config(image=played[0][i][j][0])
                current_spot += 1
            player1_played_labels[current_spot].config(image=green_image_small)
            current_spot += 1
        for i in range(player_played_max_size-1, current_spot-1, -1):
            player1_played_labels[i].config(image=green_image_small)
    elif len(played[0])>player_played_max_size: #TODO: make it so players' hands and played and river can't exceed max size
        for i in range(-1, -1*player_played_max_size-1, -1):
            for j in range(len(played[0][i])):
                player1_played_labels[i].config(image=played[0][i][j][0])

    # Redraw Player 2's played cards
    if len(played[1])==0:
        for r in player2_played_labels:
            r.config(image=green_image_small)
    elif len(played[1])<=player_played_max_size:
        current_spot = 0
        for i in range(len(played[1])):
            for j in range(len(played[1][i])):
                player2_played_labels[current_spot].config(image=played[1][i][j][0])
                current_spot += 1
            player2_played_labels[current_spot].config(image=green_image_small)
            current_spot += 1
        for i in range(player_played_max_size-1, current_spot-1, -1):
            player2_played_labels[i].config(image=green_image_small)
    elif len(played[1])>player_played_max_size:
        for i in range(-1, -1*player_played_max_size-1, -1):
            player2_played_labels[i].config(image=played[1][i][0][0])

    # Update scores
    score_frame.config(text=f'Player 1 score: {player_scores[0]}\n\nPlayer 2 score: {player_scores[1]}')

# Resize cards
def resize_card(card, size):
    our_card_img = Image.open(card)
    our_card_resized_image = our_card_img.resize(size)

    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resized_image)

    return our_card_image

# Create a new deck of cards and shuffle them
def shuffle_deck():
    redraw_table()

    global deck, player_hands, river, player_hands_highlighted, played

    deck = []
    player_hands = [[],[]]
    river = []
    player_hands_highlighted = [[],[]]
    played = [[], []]
    
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    values = range(1,10)
    # 1 = Ace, c11 = Jack, c12 = Queen, c13 = King

    for suit in suits:
        for value in values:
            deck.append(f'{value}_of_{suit}')

    # 10, Jack, Queen, and King come after numeric cards when sorted
    for suit in suits:
        for i in range(10,14):
            deck.append(f'c{i}_of_{suit}')

    random.shuffle(deck)

    for i in range(7):
        deal_card(0)
        deal_card(1)

    deck_to_river()

    redraw_table()
    
# Pop card from deck and add to river
def deck_to_river():
    if len(river)>=river_max_size:
        messagebox.showerror('Python Error', f'River already full!')
        return None

    try:
        card = deck.pop()
    except:
        messagebox.showerror('Python Error', 'Can\'t add from empty deck!')
        return None
    
    card_image = resize_card(f'./cards/{card}.png', card_image_size_large)
    river.append([card_image, f'./cards/{card}.png']) # e.g., player_hand[0] = [[Image, '2_of_spades'], [Image, '13_of_hearts']]

    player_hands_highlighted = [[],[]]

    if auto_sort_hand:
        sort_both_hands()

    redraw_table()

# Deal a card to a player
def deal_card(player):
    if len(player_hands[player])>=player_hand_max_size:
        messagebox.showerror('Python Error', f'Player {player+1}\'s hand already full!')
        return None
    
    try:
        card = deck.pop()
    except:
        messagebox.showerror('Python Error', 'Can\'t deal from empty deck!')
        return None
    
    card_image = resize_card(f'./cards/{card}.png', card_image_size_large)
    player_hands[player].append([card_image, f'./cards/{card}.png']) # e.g., player_hand[0] = [[Image, '2_of_spades'], [Image, '13_of_hearts']]
    
    if auto_sort_hand:
        sort_both_hands()

    redraw_table()

# Button functionality that's not used currently
def print_deck():
    print(deck)

def add_card_to_river(i, player): # TODO: Elsewhere make one player's highlights reset the other's
    global player_hands_highlighted

    if i >= len(player_hands[player]):
        return None
    
    if len(river)>=river_max_size:
        messagebox.showerror('Python Error', f'River already full!')
        return None

    try:
        card = player_hands[player].pop(i)
    except:
        messagebox.showerror('Python Error', 'Can\'t add from empty hand!')
        return None

    river.append(card)
    player_hands_highlighted = [[],[]]

    if auto_sort_hand:
        sort_both_hands()

    redraw_table()

# Sorts hand: aces, numerics, then face cards
def sort_hand(player):
    if(len(player_hands[player])>0):
        player_hand_str_list = [i[1] for i in player_hands[player]]
        player_hand_str_list.sort()
        player_hands[player] = [[resize_card(s, card_image_size_large), s] for s in player_hand_str_list]
        player_hands_highlighted[player] = []

        redraw_table()

# Sorts both players' hands
def sort_both_hands():
    for i in range(2):
        sort_hand(i)

def river_to_hand(i, player):
    global player_hands_highlighted
    
    if (len(player_hands[player]) + len(river) - (i + 1)) >= player_hand_max_size:
        messagebox.showerror('Python Error', f'Player {player+1} trying to take too many cards!')
        return None
    
    if i<len(river):
        for j in range(i, len(river)):
            try:
                card = river.pop()
            except:
                messagebox.showerror('Python Error', 'Can\'t take from an empty river!')
                return None

            player_hands[player].append(card)

        player_hands_highlighted = [[],[]]
        
        if auto_sort_hand:
            sort_both_hands()

        redraw_table()

def toggle_highlight(i, p):
    if i<len(player_hands[p]):
        player_hands_highlighted[(p+1)%2] = []
        if i not in player_hands_highlighted[p]:
            player_hands_highlighted[p].append(i)
        else:
            player_hands_highlighted[p].remove(i)

    redraw_table()

def test_play(values, suits):
    # Test for triple or quadruple
    if len(set(values))==1 and len(values)>=3:
        return True
    
    # Test for run
    if len(set(suits))==1 and len(suits)>2:
        values.sort()
        if sum(values) == len(values)*(values[0]+values[-1])/2: # Fun math :)
            return True
        # Now change aces to have value 14 and test again
        values[:] = [x if x != 1 else 14 for x in values]
        values.sort()
        if sum(values) == int(len(values)*(values[0]+values[-1])/2): # Fun math again :)
            return True
        
    return False

# Returns true if highlighted cards are a valid triple, quadruple, or run
def is_valid_play(player):
    global played, player_hands_highlighted
    
    highlighted = [player_hands[player][i][1] for i in player_hands_highlighted[player]] # Get list of strings of highlighted cards

    if len(highlighted)==0:
        messagebox.showerror('Python Error', 'None in hand')
        return False

    highlighted.sort()
    highlighted = [s.split('_') for s in highlighted]
    values = [int(s[0].replace('./cards/', '').replace('c', '').replace('.png', '')) for s in highlighted]
    suits = [s[2] for s in highlighted]

    if test_play(values, suits):
        return True
    
    for s in range(len(played)):
        if len(played[s])>0:
            for t in range(len(played[s])):
                temp_strings = [s[1] for s in played[s][t]]
                temp_suits = suits
                temp_suits = suits + [s.split('_')[2] for s in temp_strings] # For some reason when I try += it uses the old value of temp_suits, which messes stuff up
                temp_values = values
                temp_values = values + [int(s.split('_')[0].replace('./cards/', '').replace('c', '').replace('.png', '')) for s in temp_strings] # A mess, I know...

                if test_play(temp_values, temp_suits): # We're gonna try to do the stuff here instead of below. If it works, move stuff from below to this function above
                    # Pretty much same here as below
                    player_hands_highlighted[player].sort()
                    for i in player_hands_highlighted[player][::-1]:
                        card = player_hands[player].pop(i)
                        card = [resize_card(card[1], card_image_size_small), card[1]]
                        played[s][t].append(card)
                        player_scores[player] += card_score(card)
                    
                    player_hands_highlighted = [[],[]]
                    organize_played()

                    redraw_table()
                    
                    return False

    # Else
    return False

def hand_to_played(player): # TODO: make things more organized
    global player_hands_highlighted

    player_hands_highlighted[player].sort()

    # Test whether highlighted cards form a valid play
    if is_valid_play(player):
        to_play = []
        for i in player_hands_highlighted[player][::-1]: # reverse order of list to make sure we pop from back to front and don't go out of range
            card = player_hands[player].pop(i)
            card = [resize_card(card[1], card_image_size_small), card[1]]
            to_play.append(card)
            player_scores[player] += card_score(card)
        
        played[player].append(to_play)
        player_hands_highlighted = [[],[]]

        organize_played()

        if auto_sort_hand:
            sort_both_hands()

        redraw_table()

    player_hands_highlighted = [[],[]]
    redraw_table()
    #else:
    #    messagebox.showerror('Python Error', f'Must be a set or a run! {player_hands_highlighted}')

def organize_played():
    global played

    # See following reference for sorting along different axes: https://docs.python.org/3/howto/sorting.html
    for side in played:
        for st in side:
            st.sort(key= lambda x: x[1])

# Note: can call Rummy even when a player hasn't just played cards. Not exactly the rules, but fix later if there's time
def rummy(player):
    card = river.pop(-1)
    card_info = card[1].split('_')
    suit = [card_info[2]]
    value = [int(card[1].split('_')[0].replace('./cards/', '').replace('c', '').replace('.png', ''))]
    
    # Copied from is_valid_play(player)
    for s in range(len(played)):
        if len(played[s])>0:
            for t in range(len(played[s])):
                temp_strings = [s[1] for s in played[s][t]]
                temp_suits = suit
                temp_suits = suit + [s.split('_')[2] for s in temp_strings] # For some reason when I try += it uses the old value of temp_suits, which messes stuff up
                temp_values = value
                temp_values = value + [int(s.split('_')[0].replace('./cards/', '').replace('c', '').replace('.png', '')) for s in temp_strings] # A mess, I know...

                if test_play(temp_values, temp_suits): # We're gonna try to do the stuff here instead of below. If it works, move stuff from below to this function above
                    # Pretty much same here as below
                    card = [resize_card(card[1], card_image_size_small), card[1]]
                    played[s][t].append(card)
                    player_scores[player] += card_score(card)
                    
                    player_hands_highlighted = [[],[]]
                    organize_played()

                    redraw_table()

                    return True

    messagebox.showerror('Python Error', 'Not a valid Rummy!')
    river.add(card)
    
    return False

def card_score(card):
    value = int(card[1].split('_')[0].replace('./cards/', '').replace('c', '').replace('.png', ''))
    if value==1:
        return 15
    if value>=2 and value<=9:
        return 5
    if value>=10 and value<=13:
        return 10
    
def toggle_auto_sort():
    global auto_sort_hand
    
    auto_sort_hand = not auto_sort_hand
    redraw_table()

def close_window():
    root.destroy()

# Put cards in frames
deck_label = Label(deck_frame, text='', bd=5, background='green')
deck_label.bind('<Button-1>', func= lambda x: deal_card(0))
deck_label.bind('<Button-3>', func= lambda x: deal_card(1))
deck_label.pack(pady=20)

river_labels = []
for i in range(river_max_size):
    river_labels.append(Label(river_frame, text='', bd=5, background='green'))
    river_labels[i].pack(pady=10, side=LEFT)

player1_labels = []
for i in range(player_hand_max_size):
    player1_labels.append(Label(player1_frame, text='', bd=5, background='green'))
    player1_labels[i].pack(side=LEFT)

player2_labels = []
for i in range(player_hand_max_size):
    player2_labels.append(Label(player2_frame, text='', bd=5, background='green'))
    player2_labels[i].pack(side=LEFT)

player1_played_labels = []
for i in range(player_played_max_size):
    player1_played_labels.append(Label(player1_played_frame, width=15, text='', background='green', anchor='w'))
    player1_played_labels[i].pack(pady=10, side=LEFT)

player2_played_labels = []
for i in range(player_played_max_size):
    player2_played_labels.append(Label(player2_played_frame, width=15, text='', background='green', anchor='w'))
    player2_played_labels[i].pack(pady=10, side=LEFT)

# For some reason this doesn't work in a for loop. I saw something about lambda expressions being "lazy", but I'm not sure.
# Put inside a function so we can collapse and ignore. Remember to adjust amount of values based on max sizes
def bind_commands_to_cards():
    # Left click river card to move it and following cards to player 1
    river_labels[0].bind('<Button-1>', func= lambda x: river_to_hand(0, 0))
    river_labels[1].bind('<Button-1>', func= lambda x: river_to_hand(1, 0))
    river_labels[2].bind('<Button-1>', func= lambda x: river_to_hand(2, 0))
    river_labels[3].bind('<Button-1>', func= lambda x: river_to_hand(3, 0))
    river_labels[4].bind('<Button-1>', func= lambda x: river_to_hand(4, 0))
    river_labels[5].bind('<Button-1>', func= lambda x: river_to_hand(5, 0))
    river_labels[6].bind('<Button-1>', func= lambda x: river_to_hand(6, 0))
    river_labels[7].bind('<Button-1>', func= lambda x: river_to_hand(7, 0))
    river_labels[8].bind('<Button-1>', func= lambda x: river_to_hand(8, 0))
    river_labels[9].bind('<Button-1>', func= lambda x: river_to_hand(9, 0))
    river_labels[10].bind('<Button-1>', func= lambda x: river_to_hand(10, 0))
    river_labels[11].bind('<Button-1>', func= lambda x: river_to_hand(11, 0))
    river_labels[12].bind('<Button-1>', func= lambda x: river_to_hand(12, 0))
    river_labels[13].bind('<Button-1>', func= lambda x: river_to_hand(13, 0))

    # Right click river card to move it and following cards to player 2
    river_labels[0].bind('<Button-3>', func= lambda x: river_to_hand(0, 1))
    river_labels[1].bind('<Button-3>', func= lambda x: river_to_hand(1, 1))
    river_labels[2].bind('<Button-3>', func= lambda x: river_to_hand(2, 1))
    river_labels[3].bind('<Button-3>', func= lambda x: river_to_hand(3, 1))
    river_labels[4].bind('<Button-3>', func= lambda x: river_to_hand(4, 1))
    river_labels[5].bind('<Button-3>', func= lambda x: river_to_hand(5, 1))
    river_labels[6].bind('<Button-3>', func= lambda x: river_to_hand(6, 1))
    river_labels[7].bind('<Button-3>', func= lambda x: river_to_hand(7, 1))
    river_labels[8].bind('<Button-3>', func= lambda x: river_to_hand(8, 1))
    river_labels[9].bind('<Button-3>', func= lambda x: river_to_hand(9, 1))
    river_labels[10].bind('<Button-3>', func= lambda x: river_to_hand(10, 1))
    river_labels[11].bind('<Button-3>', func= lambda x: river_to_hand(11, 1))
    river_labels[12].bind('<Button-3>', func= lambda x: river_to_hand(12, 1))
    river_labels[13].bind('<Button-3>', func= lambda x: river_to_hand(13, 1))

    # Left click player 1 card to highlight
    player1_labels[0].bind('<Button-1>', func= lambda x: toggle_highlight(0, 0))
    player1_labels[1].bind('<Button-1>', func= lambda x: toggle_highlight(1, 0))
    player1_labels[2].bind('<Button-1>', func= lambda x: toggle_highlight(2, 0))
    player1_labels[3].bind('<Button-1>', func= lambda x: toggle_highlight(3, 0))
    player1_labels[4].bind('<Button-1>', func= lambda x: toggle_highlight(4, 0))
    player1_labels[5].bind('<Button-1>', func= lambda x: toggle_highlight(5, 0))
    player1_labels[6].bind('<Button-1>', func= lambda x: toggle_highlight(6, 0))
    player1_labels[7].bind('<Button-1>', func= lambda x: toggle_highlight(7, 0))
    player1_labels[8].bind('<Button-1>', func= lambda x: toggle_highlight(8, 0))
    player1_labels[9].bind('<Button-1>', func= lambda x: toggle_highlight(9, 0))
    player1_labels[10].bind('<Button-1>', func= lambda x: toggle_highlight(10, 0))
    player1_labels[11].bind('<Button-1>', func= lambda x: toggle_highlight(11, 0))
    player1_labels[12].bind('<Button-1>', func= lambda x: toggle_highlight(12, 0))
    player1_labels[13].bind('<Button-1>', func= lambda x: toggle_highlight(13, 0))

    # Left click player 2 card to highlight
    player2_labels[0].bind('<Button-1>', func= lambda x: toggle_highlight(0, 1))
    player2_labels[1].bind('<Button-1>', func= lambda x: toggle_highlight(1, 1))
    player2_labels[2].bind('<Button-1>', func= lambda x: toggle_highlight(2, 1))
    player2_labels[3].bind('<Button-1>', func= lambda x: toggle_highlight(3, 1))
    player2_labels[4].bind('<Button-1>', func= lambda x: toggle_highlight(4, 1))
    player2_labels[5].bind('<Button-1>', func= lambda x: toggle_highlight(5, 1))
    player2_labels[6].bind('<Button-1>', func= lambda x: toggle_highlight(6, 1))
    player2_labels[7].bind('<Button-1>', func= lambda x: toggle_highlight(7, 1))
    player2_labels[8].bind('<Button-1>', func= lambda x: toggle_highlight(8, 1))
    player2_labels[9].bind('<Button-1>', func= lambda x: toggle_highlight(9, 1))
    player2_labels[10].bind('<Button-1>', func= lambda x: toggle_highlight(10, 1))
    player2_labels[11].bind('<Button-1>', func= lambda x: toggle_highlight(11, 1))
    player2_labels[12].bind('<Button-1>', func= lambda x: toggle_highlight(12, 1))
    player2_labels[13].bind('<Button-1>', func= lambda x: toggle_highlight(13, 1))

    # Right click player 1 card to move to river
    player1_labels[0].bind('<Button-3>', func= lambda x: add_card_to_river(0, 0))
    player1_labels[1].bind('<Button-3>', func= lambda x: add_card_to_river(1, 0))
    player1_labels[2].bind('<Button-3>', func= lambda x: add_card_to_river(2, 0))
    player1_labels[3].bind('<Button-3>', func= lambda x: add_card_to_river(3, 0))
    player1_labels[4].bind('<Button-3>', func= lambda x: add_card_to_river(4, 0))
    player1_labels[5].bind('<Button-3>', func= lambda x: add_card_to_river(5, 0))
    player1_labels[6].bind('<Button-3>', func= lambda x: add_card_to_river(6, 0))
    player1_labels[7].bind('<Button-3>', func= lambda x: add_card_to_river(7, 0))
    player1_labels[8].bind('<Button-3>', func= lambda x: add_card_to_river(8, 0))
    player1_labels[9].bind('<Button-3>', func= lambda x: add_card_to_river(9, 0))
    player1_labels[10].bind('<Button-3>', func= lambda x: add_card_to_river(10, 0))
    player1_labels[11].bind('<Button-3>', func= lambda x: add_card_to_river(11, 0))
    player1_labels[12].bind('<Button-3>', func= lambda x: add_card_to_river(12, 0))
    player1_labels[13].bind('<Button-3>', func= lambda x: add_card_to_river(13, 0))

    # Right click player 2 card to move to river
    player2_labels[0].bind('<Button-3>', func= lambda x: add_card_to_river(0, 1))
    player2_labels[1].bind('<Button-3>', func= lambda x: add_card_to_river(1, 1))
    player2_labels[2].bind('<Button-3>', func= lambda x: add_card_to_river(2, 1))
    player2_labels[3].bind('<Button-3>', func= lambda x: add_card_to_river(3, 1))
    player2_labels[4].bind('<Button-3>', func= lambda x: add_card_to_river(4, 1))
    player2_labels[5].bind('<Button-3>', func= lambda x: add_card_to_river(5, 1))
    player2_labels[6].bind('<Button-3>', func= lambda x: add_card_to_river(6, 1))
    player2_labels[7].bind('<Button-3>', func= lambda x: add_card_to_river(7, 1))
    player2_labels[8].bind('<Button-3>', func= lambda x: add_card_to_river(8, 1))
    player2_labels[9].bind('<Button-3>', func= lambda x: add_card_to_river(9, 1))
    player2_labels[10].bind('<Button-3>', func= lambda x: add_card_to_river(10, 1))
    player2_labels[11].bind('<Button-3>', func= lambda x: add_card_to_river(11, 1))
    player2_labels[12].bind('<Button-3>', func= lambda x: add_card_to_river(12, 1))
    player2_labels[13].bind('<Button-3>', func= lambda x: add_card_to_river(13, 1))


bind_commands_to_cards()

# Create buttons
reshuffle_button = Button(button_frame, text='Shuffle deck', command=shuffle_deck)
reshuffle_button.grid(row=0, column=0, pady=5)

#player1_deal_button = Button(button_frame, text='Deal to Player 1', command= lambda: deal_card(0))
#player1_deal_button.pack(padx=20, pady=20, side=LEFT)

#player2_deal_button = Button(button_frame, text='Deal to Player 2', command= lambda: deal_card(1))
#player2_deal_button.pack(padx=20, pady=20, side=LEFT)

#print_deck_button = Button(button_frame, text='Print deck', command=print_deck)
#print_deck_button.pack(padx=20, pady=20, side=LEFT)

#add_river_0_button = Button(button_frame, text='Player 1 to River', command= lambda: add_card_to_river(0))
#add_river_0_button.pack(padx=20, pady=20, side=LEFT)

#add_river_1_button = Button(button_frame, text='Player 2 to River', command= lambda: add_card_to_river(1))
#add_river_1_button.pack(padx=20, pady=20, side=LEFT)

add_sort_hand_button = Button(button_frame, text='Sort player\'s hand', command= lambda: sort_hand(0))
add_sort_hand_button.bind('<Button-3>', func= lambda x: sort_hand(1))
add_sort_hand_button.grid(row=1, column=0, pady=5)

#take_river_0_button = Button(button_frame, text='River to Player 1', command= lambda: take_card_from_river(0))
#take_river_0_button.pack(padx=20, pady=20, side=LEFT)

#take_river_1_button = Button(button_frame, text='River to Player 2', command= lambda: take_card_from_river(1))
#take_river_1_button.pack(padx=20, pady=20, side=LEFT)

check_play_button = Button(button_frame, text='Check play', command= lambda: hand_to_played(0))
check_play_button.bind('<Button-3>', func= lambda x: hand_to_played(1))
check_play_button.grid(row=2, column=0, pady=5)

rummy_button = Button(button_frame, text='Rummy!', command= lambda: rummy(0))
rummy_button.bind('<Button-3>', func= lambda x: rummy(1))
rummy_button.grid(row=0, column=1, pady=5)

auto_sort_button = Button(button_frame, text='Auto sort button', command= toggle_auto_sort)
auto_sort_button.grid(row=1, column=1, padx=5, pady=5)

exit_button = Button(button_frame, text='Exit game', command=close_window)
exit_button.grid(row=2, column=1, pady=5)

#score_label = Label(button_frame, text=f'Player 1 score: {player_scores[0]}\nPlayer 2 score: {player_scores[1]}')
#score_label.pack(pady=10)


# Define deck image and shuffle deck on start
deck_image = resize_card('./cards/card_back.png', card_image_size_large)
green_image_large = resize_card('./cards/green.png', card_image_size_large)
green_image_small = resize_card('./cards/green.png', card_image_size_small)

shuffle_deck()

root.mainloop()