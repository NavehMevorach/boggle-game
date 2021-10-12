#################################################################
# FILE : ex12_utils.py
# WRITERS : Naveh Mevorach , navehmevorach , 318284569
#           Nitzan Abramovich, nitzanabr, 206588568
# EXERCISE : intro2cs2 ex12 2021
# DESCRIPTION: Backtracking functions
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: none
#################################################################

WORDS_MODIFIER = 'WORDS'


def get_coordinates(board):
    """
    Get a board and return its coordinates
    :param board: list
    :return: list of coordinates
    """
    coordinates = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            coordinates.append((i, j))
    return coordinates


def dic_of_start_with(words):
    """ Create a dictionary with all start with of the  words
    for instance abcdef, hijklmn:
                    3: abc, hij
                    4: abcd, hijk
                    5: abcde ...
    :return: dictionary
    """
    reduced_words = dict()
    for i in range(3, 16):
        reduced_words[i] = {word[:i] for word in words}
    return reduced_words


def find_neighbors(current_coor: tuple, coordinates: list):
    """
    Find all the neighbors of a specific coordinate
    :param current_coor: tuple
    :param coordinates: list of tuples
    :return: list of coordinates (tuples)
    """
    neighbors = []
    for coordinate in coordinates:
        if coordinate == current_coor:
            continue
        if -1 <= (coordinate[0] - current_coor[0]) <= 1 and \
                -1 <= (coordinate[1] - current_coor[1]) <= 1:
            neighbors.append(coordinate)

    return neighbors


def dic_of_neighbors(coordinates):
    """
    Creates a dictionary which store all the neighbors of each coordinate
    :param coordinates: list of tuples
    :return: dictionary -> coor: [neighbors]
    """
    neighbors_data = dict()
    for coordinate in coordinates:
        neighbors_data[coordinate] = find_neighbors(coordinate, coordinates)
    return neighbors_data


def is_valid_path_helper(board, i, item, path):
    """
    Check if a path i a valid path
    :return: True upon success, None otherwise
    """
    if not isinstance(item, tuple):
        return
    if len(item) != 2:
        return
    if not isinstance(item[0], int) or not isinstance(item[1], int):
        return
    if not (0 <= item[0] < len(board)) or not (0 <= item[1] < len(board)):
        return
    # Check if valid path by checking neighbors
    neighbors = find_neighbors(item, get_coordinates(board))
    if i < len(path) - 1 and path[i + 1] not in neighbors:
        return
    return True


def is_valid_path(board, path: list, words):
    """
    Check if a given path is a valid path
    :param board: Board Object
    :param path: list of tuples
    :param words: set
    :return: string upon success and None otherwise
    """
    word = ''
    used_path = set()
    # Check the path
    for i, item in enumerate(path):
        keep_going = is_valid_path_helper(board, i, item, path)
        if not keep_going:
            return
        # Check if the coordinate already appeared
        if item in used_path:
            return
        used_path.add(item)
        x, y = item
        word += (board[x][y])
    # Check if word in words
    if word not in words:
        return
    return word


def find_length_n_second_helper(word, words, path, all_path):
    """
    Check if a given work is in the Words and if it is its adds
    the path to all_path list
    """
    if word in words:
        all_path.append(path)


def find_length_n_helper(board, all_path, n, board_coor, words, reduced_words,
                         initial_coor, path, composed_word,
                         modifier=None):
    """
    An helper function which go through all the neighbors of a given coordinate
    And using Backtracking to find all possible path from that coordinate
    The recursion has a stop condition which is depend on the modifier
    :param board: Board object
    :param all_path: empty list to store all the paths
    :param n: int which represent length of the path
    :param board_coor: list with all the board coordinates
    :param words: set with all the words in the game
    :param reduced_words: dictionary with all the reduced words
    :param initial_coor: tuple the first coordinate in the path
    :param path: list of tuples which represent the path to the final word
    :param composed_word: str - the word that been composed
    :param modifier: modifier

    """
    # Check the Modifier
    if modifier == WORDS_MODIFIER:
        # Base condition
        if len(composed_word) == n:
            find_length_n_second_helper(composed_word, words, path, all_path)
            return
    # Base condition
    elif len(path) == n:
        find_length_n_second_helper(composed_word, words, path, all_path)
        return
    for coor in find_neighbors(initial_coor, board_coor):
        word_len = len(composed_word)
        # Check if the word is even exists in the Dictionary
        if word_len > 2 and composed_word not in reduced_words[word_len]:
            continue
        # Check if the coordinate was already
        if coor in path:
            continue
        x, y = coor
        word_to_add = board[x][y]
        find_length_n_helper(board, all_path, n, board_coor, words,
                             reduced_words, coor, path + [coor],
                             composed_word + word_to_add,
                             modifier)


def find_length_n_paths(n, board, words):
    """
    Find all the words in the game that their path equal
    to n
    The func go through all the coordinates in the board
    and use a helper function to calculate all the words from each coordinate
    """
    all_path = []
    board_coor = get_coordinates(board)
    reduced_words = dic_of_start_with(words)
    for coordinate in board_coor:
        x, y = coordinate
        first_letter = board[x][y]
        find_length_n_helper(board, all_path, n, board_coor, words,
                             reduced_words, coordinate, [coordinate],
                             first_letter)
    return all_path


def find_length_n_words(n, board, words):
    """
    Find all the words in the game that their letters equal
    to n
    The func go through all the coordinates in the board
    and use a helper function to calculate all the words from each coordinate
    """
    all_path = []
    board_coor = get_coordinates(board)
    reduced_words = dic_of_start_with(words)
    for coordinate in board_coor:
        x, y = coordinate
        first_letter = board[x][y]
        find_length_n_helper(board, all_path, n, board_coor, words,
                             reduced_words, coordinate, [coordinate],
                             first_letter, WORDS_MODIFIER)
    return all_path


def max_score_second_helper(word_dict, all_paths):
    """
   An helper function that gets a dictionary of all the words found on the board
    and the
   highest scores path to them and returns a list of the paths
    :param word_dict: a dictionary with all the words found on the board and the
     highest score paths to them
   :param all_paths: an empty list that will contain all the paths from the
   dictionary
    """
    for value in word_dict.values():
        all_paths.append(value)
    return all_paths


def max_score_helper(board, board_coor, words, path, initial_coor,
                     composed_word, reduced_words, dict_words):
    """
        An helper function which go through all the neighbors of a given
        coordinate And using recursion to find the highest score path to all
        found words from the word list on the board
        :param board: list of list representing a board
        :param board_coor: list with all the board coordinates
        :param words: set with all the words in the game
        :param path: list of tuples which represent the path to the final word
        :param initial_coor: tuple the first coordinate in the path
        :param composed_word: str - the word that been composed
        :param reduced_words: dictionary with all the reduced words
        :param dict_words: a dictionary with all the words found on the board
        and the highest score paths to them

    """
    # basic condition
    if composed_word in words:
        if composed_word not in dict_words:
            dict_words[composed_word] = path
        elif len(dict_words[composed_word]) < len(path):
            dict_words[composed_word] = path
    for coor in find_neighbors(initial_coor, board_coor):
        word_len = len(composed_word)
        # Check if the word is even exists in the Dictionary
        if word_len > 2 and composed_word not in reduced_words[word_len]:
            continue
        # Check if the coordinate was already
        if coor in path:
            continue
        x, y = coor
        word_to_add = board[x][y]
        max_score_helper(board, board_coor, words, path + [coor], coor,
                         composed_word + word_to_add,
                         reduced_words, dict_words)


def max_score_paths(board, words):
    """
    The func calc what are the best path combination which will result
    the best score that a user can get from the current board.
    """
    dict_words = {}
    board_coor = get_coordinates(board)
    reduced_words = dic_of_start_with(words)
    all_paths = []
    for coordinate in board_coor:
        x, y = coordinate
        first_letter = board[x][y]
        max_score_helper(board, board_coor, words, [coordinate], coordinate,
                         first_letter, reduced_words, dict_words)
    max_score_second_helper(dict_words, all_paths)
    return all_paths
