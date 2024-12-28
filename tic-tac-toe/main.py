import tkinter as tk

def set_tile(row, column):
    global curr_player, game_over

    if game_over:
        return

    if board[row][column]['text'] != '':
        return

    board[row][column]['text'] = curr_player
    if curr_player == playerO:
        curr_player = playerX
    else:
        curr_player = playerO

    label['text'] = f"{curr_player}'s turn"

    check_winner()


def check_winner():
    global turns, game_over
    turns += 1

    # Check rows and columns
    for i in range(3):
        if (board[i][0]['text'] == board[i][1]['text'] == board[i][2]['text'] and
                board[i][0]['text'] != ''):
            label.config(text=board[i][0]['text'] + ' is the winner!', foreground=color_yellow)
            for j in range(3):
                board[i][j].config(foreground=color_yellow, background=color_light_grey)
            game_over = True
            return

        if (board[0][i]['text'] == board[1][i]['text'] == board[2][i]['text'] and
                board[0][i]['text'] != ''):
            label.config(text=board[0][i]['text'] + ' is the winner!', foreground=color_yellow)
            for j in range(3):
                board[j][i].config(foreground=color_yellow, background=color_light_grey)
            game_over = True
            return

    # Check diagonals
    if board[0][0]['text'] == board[1][1]['text'] == board[2][2]['text'] and board[0][0]['text'] != '':
        label.config(text=board[0][0]['text'] + ' is the winner!', foreground=color_yellow)
        for i in range(3):
            board[i][i].config(foreground=color_yellow, background=color_light_grey)
        game_over = True
        return

    if board[0][2]['text'] == board[1][1]['text'] == board[2][0]['text'] and board[0][2]['text'] != '':
        label.config(text=board[0][2]['text'] + ' is the winner!', foreground=color_yellow)
        board[0][2].config(foreground=color_yellow, background=color_light_grey)
        board[1][1].config(foreground=color_yellow, background=color_light_grey)
        board[2][0].config(foreground=color_yellow, background=color_light_grey)
        game_over = True
        return

    # Check for a tie
    if turns == 9:
        game_over = True
        label.config(text='Tie', foreground=color_yellow, background=color_light_grey)


def new_game():
    global turns, game_over, curr_player

    turns = 0
    game_over = False
    curr_player = playerO if curr_player == playerX else playerX


    label.config(text=f"{curr_player}'s turn", foreground='white')

    for row in range(3):
        for column in range(3):
            board[row][column].config(text='', foreground=color_blue, background=color_grey)


# Game setup
playerX = 'X'
playerO = 'O'
curr_player = playerX

board = [[0, 0, 0] for _ in range(3)]  # Using placeholders for Buttons

color_blue = '#4584b6'
color_yellow = '#ffde57'
color_grey = '#343434'
color_light_grey = '#646464'

turns = 0
game_over = False

# Window setup
window = tk.Tk()
window.title('Tic-Tac-Toe')
window.resizable(False, False)

frame = tk.Frame(window)
label = tk.Label(frame, text=f"{curr_player}'s turn", font=('Consolas', 20), background=color_grey,
                 foreground='white')
label.grid(column=0, row=0, columnspan=3, sticky='we')

for row in range(3):
    for column in range(3):
        board[row][column] = tk.Button(frame, text='', font=('Consolas', 50, 'bold'), background=color_grey,
                                       foreground=color_blue, width=4, height=1,
                                       command=lambda r=row, c=column: set_tile(r, c))
        board[row][column].grid(row=row + 1, column=column)
restart_button = tk.Button(frame, text='Restart', font=('Consolas', 20), background=color_grey, foreground='white',
                           command=new_game)
restart_button.grid(row=4, column=0, columnspan=3, sticky='we')

frame.pack()

# Set initial size and center window
window.update_idletasks()  # Update window to get its dimensions
window_width = 474
window_height = 508
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')

window.mainloop()
