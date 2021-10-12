#################################################################
# FILE : boggle.py
# WRITERS : Naveh Mevorach , navehmevorach , 318284569
#           Nitzan Abramovich, nitzanabr, 206588568
# EXERCISE : intro2cs2 ex12 2021
# DESCRIPTION: Boggle game
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: none
#################################################################

from tkinter import *
from tkinter import font as tk_font
import ex12_utils
from boggle_board_randomizer import randomize_board

# GLOBAL VARIABLES
COLORS = {
    'BLUE_COLOR': '#2ECDFF',
    'ORANGE_COLOR_BOLD': '#FA8400',
    'ORANGE_COLOR_REG': '#FCAE48',
    'WHITE_COLOR': '#FFFFFF',
    'RED_COLOR': '#F71D00',
}

FONT = {
    'GAME_FONT': 'Comic Sans MS',
    'FONT_WEIGHT': 'bold',
    'FONT_TITLE_SIZE': 50
}

LABELS = {
    'MAIN_TITLE': 'Boggle!',
    'TIME_LEFT': 'Time left:',
    'REPEAT_TEXT': 'Shake Cubes!',
    'PAUSE_TEXT': 'Pause Game',
    'RESUME_TEXT': 'Resume',
    'SCORE_LABEL': 'Score:',
    'WORD_FOUND_LABEL': 'Found:',
    'CURRENT_WORD_LABEL': 'Word:',
    'RESET_WORD': 'Reset Word',
    'INITiAIL_STR': '',
}
GLOBAL_NUM = {
    'MAX_PATH_LEN': 16,
    'INITiAIL_SCORE': 0,
    'INITiAIL_COUNTDOWN_AMOUNT': 180,
    'WARNING_TIME': 30,
}

GLOBAL_SETTINGS = {
    'FILE_PATH': 'boggle_dict.txt',
    'START_SCREEN_SIZE': "1000x600"
}


class Model:
    """
    The class is charge on all the Data of the game
    """

    def __init__(self, words):
        self._letters = []
        self._coordinates = []
        self._coor_dic = ex12_utils.dic_of_neighbors(self._coordinates)
        self._words = words
        self._path = []
        self._current_word = LABELS['INITiAIL_STR']
        self._words_found = set()
        self._score = GLOBAL_NUM['INITiAIL_SCORE']
        self._start_time = GLOBAL_NUM['INITiAIL_COUNTDOWN_AMOUNT']
        self._is_pause = False
        self._is_letters_hidden = True
        self._game_counter = 0
        self._is_shake_again = 1
        self._after_func = None

    # HELPERS
    @staticmethod
    def time_formatter(count):
        mins, secs = divmod(count, 60)
        mins_str = f'{mins}' if mins >= 10 else f'0{mins}'
        secs_str = f'{secs}' if secs >= 10 else f'0{secs}'
        return f'{mins_str}:{secs_str}'

    # GETTERS
    def get_current_word(self):
        """ Return current word (str)"""
        return self._current_word

    def get_letters(self):
        """ Return letters (list)"""
        return self._letters

    def get_words_found(self):
        """ Return words found (set)"""
        return self._words_found

    def get_words(self):
        """ Return words """
        return self._words

    def get_is_hidden(self):
        """ Return is_letters_hidden (boolean) """
        return self._is_letters_hidden

    def get_score(self):
        """ Return score (int) """
        return self._score

    def get_start_time_str(self):
        return self.time_formatter(self.get_start_time())

    def get_start_time(self):
        return self._start_time

    def get_path(self):
        """ Return path (list) """
        return self._path

    def get_is_paused(self):
        """ Return is game is paused (bool)"""
        return self._is_pause

    def get_game_counter(self):
        """ Return game counter (int) """
        return self._game_counter

    def get_is_shake_again(self):
        """ Return is shake again (int) """
        return self._is_shake_again

    # SETTERS

    def set_is_paused(self):
        self._is_pause = not self._is_pause

    def _set_letters(self, letters: list):
        """ Set letters """
        self._letters = letters

    def set_words_found(self, word: str):
        """ Set words found """
        self._words_found.add(word)

    def reset_words_found(self):
        self._words_found = set()

    def set_score(self, points: int):
        """ Set score """
        self._score += points

    def reset_score(self):
        """ Reset score """
        self._score = 0

    def set_hidden(self, b: bool):
        """ Set _is_letters_hidden """
        self._is_letters_hidden = b

    def set_path(self, coor: tuple):
        """ Set path """
        self._path.append(coor)

    def reset_path(self):
        """ Reset path """
        self._path = []

    def pop_last_coor_in_path(self):
        """ Pop last coor in path  """
        self._path.pop()

    def set_current_word(self, letter: str):
        """ Set current word """
        self._current_word += letter

    def reset_current_word(self):
        """ Reset current word """
        self._current_word = ''

    def pop_last_letter_in_current_word(self, amount_to_remove: int):
        """ Pop last letter in current word  """
        for i in range(1, amount_to_remove + 1):
            self._current_word = self.get_current_word()[:-1]

    def set_game_counter(self):
        self._game_counter += 1

    def set_is_shake_again(self):
        self._is_shake_again += 1


class Controller(Model):
    """
    The Controller Class Mediator between the View and the Model
    and its the core of the Boggle App.
    The Class inherit the Model class in order to manipulate all the Data
    """

    def __init__(self, words):
        super().__init__(words)
        self._root = Tk()
        self._view = View(self._root, self)

    def start(self):
        """ Activate the View object which will display all the
        tkinter components
        """
        self._view.start_game()

    def start_game(self, _):
        """ Start one iteration of the game """
        # If game paused the user cant shake board
        if self.get_is_paused():
            return
        # Count games
        self.set_game_counter()
        # Reset Model
        letters = self._randomizer()
        self._set_letters(letters)
        self._set_coordinates(self._letters)
        self.reset_score()
        self.reset_current_word()
        self.reset_path()
        self.reset_words_found()
        self.countdown(self.get_start_time())

        # Reset View
        self._view.reset_word_list()
        self._view.set_current_word('')
        self._view.add_buttons(self._letters)
        self._view.add_pause_btn()
        self._view.add_reset_btn()
        self._view.set_score(self._score)

    def restart(self):
        """
        Restart the game after the countdown reached 0
        """
        self._view.remove_buttons()
        self._view.reset_word_list()
        self._view.remove_pause_btn()
        self._view.remove_reset_btn()
        self.start()

    def pause(self, _):
        """ Pause the game """
        self._view.hide_letters()
        self._view.set_pause_btn_text()
        self.set_is_paused()

    def user_action_manager(self, _, coor: tuple, let: str):
        """
        Check what button the user clicked on and activate the proper
         methods.
        :param _: event
        :param coor: tuple
        :param let: string
        :return: None
        """
        if self._path:
            # Check if Double clicked
            if self.check_if_double_click(coor, let):
                # Change back Button color
                return
            # Check if valid path
            if self.check_if_valid_path(coor):
                return
        # Update Path
        self.set_path(coor)
        # Update current word
        self.set_current_word(let)
        self._view.set_current_word(self._current_word)
        # check if in words and not in found words
        self.check_if_word_was_found()
        # If Path is 16 reset it and the word
        self.check_if_path_exceeded()

    def score_manager(self, path: list):
        """
        Calculate the score and update the View
        :param path: list of coordinates
        """
        path_len = len(path)
        points_to_add = path_len ** 2
        self.set_score(points_to_add)
        new_score = self.get_score()
        self._view.set_score(new_score)

    def countdown(self, count):
        """
        Count down and update the View
        If the count is 0 or the user asked for a new game the count will stop
        :param count: int
        :return:
        """
        if self.check_if_shake_again_in_middle():
            self._view.change_timer_color(COLORS['WHITE_COLOR'])
            self._view.set_time(self.time_formatter(self.get_start_time()))
            self._root.after_cancel(self._after_func)
            self._after_func = self._root.after(1000, self.countdown, count - 1)
        elif self.get_is_paused():
            self._after_func = self._root.after(1000, self.countdown, count)
        elif count > 0:
            if count <= GLOBAL_NUM['WARNING_TIME']:
                self._view.change_timer_color(COLORS['RED_COLOR'])
            self._view.set_time(self.time_formatter(count))
            self._after_func = self._root.after(1000, self.countdown, count - 1)
        else:
            self._view.change_timer_color(COLORS['WHITE_COLOR'])
            self._view.set_time(self.time_formatter(self.get_start_time()))
            self.restart()

    # HELPERS

    def check_if_shake_again_in_middle(self):
        if self.get_is_shake_again() != self.get_game_counter():
            self.set_is_shake_again()
            return True
        return False

    def check_if_double_click(self, coor: tuple, let: str):
        """
        Check if the user double click the same button
        which in that case it will pop the coordinate of the button from the
        path and will pop the button letter from the current word
        """
        if coor == self.get_path()[-1]:
            self.pop_last_coor_in_path()
            self.pop_last_letter_in_current_word(len(let))
            self._view.set_current_word(self.get_current_word())
            return True
        return False

    def check_if_valid_path(self, coor: tuple):
        """
        Check if the button was clicked is a valid button to click on
        """
        neighbors = ex12_utils.find_neighbors(self._path[-1],
                                              self._coordinates)
        if coor not in neighbors or coor in self.get_path():
            return True
        return False

    def check_if_word_was_found(self):
        """ Check if the word that was composed by the user so far
        is in the words and not in the founded words
        if its a valid word the method will reset the data for the next turn and
        update the score
        """
        current_word = self.get_current_word()
        words_list = self.get_words()
        words_found = self.get_words_found()
        path = self.get_path()
        if current_word not in words_found and current_word in words_list:
            self.set_words_found(current_word)
            # add word to word list in board
            self._view.update_word_list(current_word)
            # reset data for a new turn
            self.new_turn()
            # update score
            self.score_manager(path)

    def check_if_path_exceeded(self):
        """ Check if the path is 16 and if it is
        activate the new_turn method
        """
        if len(self.get_path()) >= GLOBAL_NUM['MAX_PATH_LEN']:
            self.new_turn()

    def new_turn(self):
        """Reset the Board and the Data for the
        next attempt of finding a word
        """
        self.reset_current_word()
        self.reset_path()
        self._view.set_current_word('')

    @staticmethod
    def _randomizer():
        """
        Randomize letters using a helper function
        :return: matrix (list of lists)
        """
        return randomize_board()

    # GETTERS
    def get_root(self):
        """ Return the root of the tkinter """
        return self._root

    # SETTERS
    def _set_coordinates(self, board):
        """ Set the coordinates of the board """
        for i in range(len(board)):
            for j in range(len(board[i])):
                self._coordinates.append((i, j))


class View:
    """ Charge on the Graphic aspect of the game """

    def __init__(self, root, controller):
        self._controller = controller
        self._root = root
        self._myFont = tk_font.Font(family=FONT['GAME_FONT'], size=20,
                                    weight=FONT['FONT_WEIGHT'])
        self._myFont_s = tk_font.Font(family=FONT['GAME_FONT'], size=14,
                                      weight=FONT['FONT_WEIGHT'])

        # Main Frames
        self._top_frame = Frame(self._root, bg=COLORS['BLUE_COLOR'], width=450,
                                height=120, pady=3)
        self._bottom_frame = Frame(self._root, bg=COLORS['ORANGE_COLOR_BOLD'],
                                   width=50,
                                   height=40, padx=3, pady=10)

        # TOP FRAME ELEMENTS
        self._top_label = Label(self._top_frame, text=LABELS['MAIN_TITLE'],
                                fg=COLORS['WHITE_COLOR'],
                                bg=COLORS['BLUE_COLOR'],
                                font=(
                                    FONT['GAME_FONT'], FONT['FONT_TITLE_SIZE'],
                                    FONT['FONT_WEIGHT']))
        # Bottom frame frames
        self._bottom_left = Frame(self._bottom_frame,
                                  bg=COLORS['ORANGE_COLOR_BOLD'],
                                  width=100, height=190, padx=10, pady=3)
        self._bottom_mid = Frame(self._bottom_frame,
                                 bg=COLORS['ORANGE_COLOR_REG'],
                                 width=250, height=190, padx=3, pady=3)
        self._bottom_right = Frame(self._bottom_frame,
                                   bg=COLORS['ORANGE_COLOR_BOLD'],
                                   width=100, height=190, padx=10, pady=3)

        # LEFT BOTTOM FRAME COMPONENTS
        self._score_label = Label(self._bottom_left,
                                  bg=COLORS['ORANGE_COLOR_BOLD'],
                                  fg=COLORS['WHITE_COLOR'], font=self._myFont,
                                  text=LABELS['SCORE_LABEL'])
        self._score = Label(self._bottom_left, bg=COLORS['ORANGE_COLOR_BOLD'],
                            fg=COLORS['WHITE_COLOR'], font=self._myFont,
                            text=self._controller.get_score())

        self._current_word = Label(self._bottom_frame,
                                   bg=COLORS['ORANGE_COLOR_BOLD'],
                                   fg=COLORS['BLUE_COLOR'], font=self._myFont,
                                   text=self._controller.get_current_word())
        self._current_word_label = Label(self._bottom_frame,
                                         bg=COLORS['ORANGE_COLOR_BOLD'],
                                         fg=COLORS['WHITE_COLOR'],
                                         font=self._myFont,
                                         text=LABELS['CURRENT_WORD_LABEL'])

        self._words_found_label = Label(self._bottom_left,
                                        bg=COLORS['ORANGE_COLOR_BOLD'],
                                        fg=COLORS['WHITE_COLOR'],
                                        font=self._myFont,
                                        text=LABELS['WORD_FOUND_LABEL'])
        self._word_found_frame = Frame(self._bottom_left,
                                       bg=COLORS['WHITE_COLOR'],
                                       width=100)

        # RIGHT BOTTOM FRAME COMPONENTS
        self._time_label = Label(self._bottom_right,
                                 bg=COLORS['ORANGE_COLOR_BOLD'],
                                 fg=COLORS['WHITE_COLOR'], font=self._myFont,
                                 text=LABELS['TIME_LEFT'])
        self._time = Label(self._bottom_right, bg=COLORS['ORANGE_COLOR_BOLD'],
                           fg=COLORS['WHITE_COLOR'], font=self._myFont,
                           text=self._controller.get_start_time_str())

        self._repeat_btn = Button(self._bottom_right, fg=COLORS['WHITE_COLOR'],
                                  bg=COLORS['BLUE_COLOR'],
                                  highlightbackground=COLORS['BLUE_COLOR'],
                                  font=self._myFont_s,
                                  text=LABELS['REPEAT_TEXT'],
                                  padx=20, pady=20)
        self._pause_game = Button(self._bottom_right, text=LABELS['PAUSE_TEXT'],
                                  highlightbackground=COLORS['BLUE_COLOR'],
                                  bg=COLORS['BLUE_COLOR'],
                                  fg=COLORS['WHITE_COLOR'], font=self._myFont_s,
                                  padx=20,
                                  pady=20)
        self._reset_word = Button(self._bottom_right, text=LABELS['RESET_WORD'],
                                  highlightbackground=COLORS['BLUE_COLOR'],
                                  bg=COLORS['BLUE_COLOR'],
                                  fg=COLORS['WHITE_COLOR'], font=self._myFont_s,
                                  padx=20,
                                  pady=20)

    def start_game(self):
        """
        Create all the tkinter components
        """
        self._root.title("Boggle!")
        self._root.configure(background=COLORS['ORANGE_COLOR_BOLD'])
        self._root.geometry(GLOBAL_SETTINGS['START_SCREEN_SIZE'])

        # UNPACK MAIN FRAMES
        self._top_frame.grid(row=0, sticky="ew")
        self._bottom_frame.grid(row=1, sticky="nsew")

        # UNPACK TOP FRAME
        self._top_label.place(relx=0, relwidth=1)

        # UNPACK BOTTOM FRAMES
        self._bottom_left.place(relwidth=0.2, relheight=1, relx=0)
        self._bottom_mid.place(relwidth=0.6, relheight=1, relx=0.2)
        self._bottom_right.place(relwidth=0.2, relheight=1, relx=0.8)

        # UNPACK RIGHT BOTTOM COMPONENTS
        self._time_label.place(rely=0, relx=0, relwidth=1)
        self._time.place(rely=0.1, relx=0, relwidth=1)
        self._repeat_btn.place(rely=0.3, relx=0, relwidth=1)
        self._repeat_btn.bind("<Button-1>", self._controller.start_game)

        # UNPACK LEFT BOTTOM COMPONENTS
        self._score_label.place(rely=0, relx=0, relwidth=1)
        self._score.place(rely=0.1, relx=0, relwidth=1)
        self._current_word_label.place(rely=0.2, relx=0, relwidth=0.2)
        self._current_word.place(rely=0.3, relx=0, relwidth=0.2)
        self._words_found_label.place(rely=0.4, relx=0, relwidth=1)
        self._word_found_frame.place(rely=0.5, relx=0, relwidth=1, relheight=1)

        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_columnconfigure(0, weight=1)

        mainloop()

    # SETTERS

    def set_time(self, time):
        """ Set the time """
        self._time.config(text=time)

    def change_timer_color(self, color):
        """ Set the time color """
        self._time.config(fg=color)

    def set_current_word(self, word):
        """ Set the current word text """
        self._current_word.config(text=word)

    def set_score(self, score: int):
        """ Set the score text """
        self._score.config(text=score)

    def set_pause_btn_text(self):
        """ Set the pause button text """
        text = LABELS['PAUSE_TEXT'] if self._controller.get_is_hidden() else \
            LABELS['RESUME_TEXT']
        self._pause_game.config(text=text)

    def reset_pause_btn_text(self):
        self._pause_game.config(text=LABELS['PAUSE_TEXT'])

    def hide_letters(self):
        """
        The method hide all the letters or revealed the letter
        depends on the set_hidden variable
        """
        if self._controller.get_is_hidden():
            self._controller.set_hidden(False)
            for child in self._bottom_mid.winfo_children():
                child.place_forget()
        else:
            self._controller.set_hidden(True)
            self.add_buttons(self._controller.get_letters())

    def add_pause_btn(self):
        """ The method adds a pause btn to the game """
        self._pause_game.place(rely=0.5, relx=0, relwidth=1)
        self._pause_game.bind("<Button-1>", self._controller.pause)

    def remove_pause_btn(self):
        """ The method removes the pause btn from the game """
        self._pause_game.place_forget()

    def add_reset_btn(self):
        """ The method adds a reset btn to the game """
        self._reset_word.place(rely=0.7, relx=0, relwidth=1)
        self._reset_word.bind("<Button-1>",
                              lambda e: self._controller.new_turn())

    def remove_reset_btn(self):
        """ The method removes the pause btn from the game """
        self._reset_word.place_forget()

    def add_buttons(self, letters: list):
        """
        The method creates all the button components and place them
        :param letters: list with all the letters
        """
        for i, row in enumerate(letters):
            for j, let in enumerate(row):
                btn = Button(self._bottom_mid, text=let, font=self._myFont,
                             bg=COLORS['WHITE_COLOR'],
                             activebackground=COLORS['BLUE_COLOR'],
                             fg=COLORS['BLUE_COLOR'], padx=30, pady=30)
                btn.place(relx=i * 0.2 + 0.1, rely=j * 0.2 + 0.1, relwidth=0.2,
                          relheight=0.2)
                btn.bind("<Button-1>",
                         lambda e, i=i, j=j,
                                l=let: self._controller.user_action_manager(e,
                                                                            (i,
                                                                             j),
                                                                            l))

    def remove_buttons(self):
        """ The method remove all the buttons from the game """
        for btn in self._bottom_mid.winfo_children():
            btn.destroy()

    def update_word_list(self, word: str):
        """ The method add a new Label to the word list
        and place it
        """
        word = Label(self._word_found_frame, text=word,
                     fg=COLORS['ORANGE_COLOR_BOLD'],
                     bg=COLORS['WHITE_COLOR'])
        word.pack()

    def reset_word_list(self):
        """ The method remove all the words from the word lis """
        for word in self._word_found_frame.winfo_children():
            word.destroy()


def load_words(file_path):
    """ Load the words from a given file """
    with open(r'{}'.format(file_path), 'r') as file:
        return {line.strip('\n') for line in file}


if __name__ == "__main__":
    words = load_words(GLOBAL_SETTINGS['FILE_PATH'])
    boggle = Controller(words)
    boggle.start()
