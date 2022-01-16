Skip to content
Why GitHub? 
Team
Enterprise
Explore 
Marketplace
Pricing 
Search
Sign in
Sign up
cheukyin699
/
py-scrabble
Public
Code
Issues
Pull requests
Actions
Projects
1
Wiki
Security
Insights
py-scrabble/board.py /

Cheuk Yin Ng [move] Fixed validation bug
…
Latest commit 3908dea on 15 Jan 2017
 History
 0 contributors
388 lines (342 sloc)  13 KB
   
import pygame
import colors
import tile
import resman
import word_helpers as wh

class ScrabbleBoard:
    '''
    A snug little scrabble board class that stores information about
    the bonus system, the tiles currently on the board, and if a move
    is valid or not.
    '''
    def __init__(self, pos, rman):
        '''
        Initializes positions, tiles, and bonuses. Tiles have tile items,
        whereas bonuses have surfaces as items.
        '''
        self.pos = pos
        self.tiles = [[None for _ in range(15)] for __ in range(15)]
        self.rman = rman
        self.size = (15 * resman.Tile_Size[0],
                     15 * resman.Tile_Size[1])
        self.rect = pygame.Rect(self.pos, self.size)
        self.clean = True

        # Initialize the bonus system
        self.init_bonus("res/board_data.txt")

    def __contains__(self, pos):
        '''
        Returns true if point is inside Scrabble board, and false if otherwise.
        Uses pygame Rect.collidepoint method to compact code.
        '''
        return self.rect.collidepoint(pos)

    def _find_connected_words(self, m, ms):
        '''
        Finds all the words that are connected either horizontally or vertically
        to the single letter in move m (in a moveset, of course).
            (pos0, word, pos1)
        Where:
            pos0 - Starting point of the word
            word - The word itself
            pos1 - Ending point of the word
        Returns a list (max size 2) of words in the above format.
        '''
        x, y, l = m
        # Horizontal word
        hw_0, hw_w, hw_1 = (x, y), "", (x, y)
        # Go left
        for i in range(x, -1, -1):
            # First, try to get a tile
            item = None
            if self.tiles[i][y] is None:
                try:
                    item = ms.get_item(i, y)
                    hw_0 = (i, y)       # In edge cases
                except ValueError:
                    # If there are no more tiles left, get out
                    hw_0 = (i + 1, y)
                    break
            else:
                ms.is_chain = True
                item = (i, y, self.tiles[i][y])
                hw_0 = (i, y)           # In edge cases

            # Add letter to front of word
            hw_w = item[2] + hw_w

        # Go right
        for i in range(x + 1, 15):
            # First, try to get a tile
            item = None
            if self.tiles[i][y] is None:
                try:
                    item = ms.get_item(i, y)
                    hw_1 = (i, y)
                except ValueError:
                    hw_1 = (i - 1, y)
                    break
            else:
                ms.is_chain = True
                item = (i, y, self.tiles[i][y])
                hw_1 = (i, y)

            hw_w += item[2]

        # Vertical word
        vw_0, vw_w, vw_1 = None, "", None
        # Go up
        for j in range(y, -1, -1):
            # First, try to get a tile
            item = None
            if self.tiles[x][j] is None:
                try:
                    item = ms.get_item(x, j)
                    vw_0 = (x, j)
                except ValueError:
                    # If there are no more tiles left, get out
                    vw_0 = (x, j + 1)
                    break
            else:
                ms.is_chain = True
                item = (x, j, self.tiles[x][j])
                vw_0 = (x, j)

            # Add letter to front of word
            vw_w = item[2] + vw_w

        # Go right
        for j in range(y + 1, 15):
            # First, try to get a tile
            item = None
            if self.tiles[x][j] is None:
                try:
                    item = ms.get_item(x, j)
                    vw_1 = (x, j)
                except ValueError:
                    vw_1 = (x, j - 1)
                    break
            else:
                ms.is_chain = True
                item = (x, j, self.tiles[x][j])
                vw_1 = (x, j)

            vw_w += item[2]

        # Filter out all the single-letters, as they don't do anything (not
        # connected to anything, and is just there by itself).
        ret = []
        if len(hw_w) > 1:
            ret.append((hw_0, hw_w, hw_1))

        if len(vw_w) > 1:
            ret.append((vw_0, vw_w, vw_1))

        return ret

    def find_connected_words(self, ms):
        '''
        Finds all the words that are connected either horizontally or vertically
        to any of the letters in the moveset. To ensure that duplicates are
        eliminated, the list of words are returned as such:
            (pos0, word, pos1)
        Where:
            pos0 - Starting point of the word
            word - The word
            pos1 - Ending point of the word
        '''
        words = []
        for m in ms.m:
            words.extend(self._find_connected_words(m, ms))

        return list(set(words))

    def validate_moveset(self, ms, wd):
        '''
        Returns true if the moveset on the board contains valid scrabble words.
        Returns false otherwise.
        '''
        # TODO consider caching
        words = map(lambda item: item[1], self.find_connected_words(ms))
        return all(map(wd.isValid, words))

    def execute(self, ms):
        assert(ms.t == 'M')

        for x, y, l in ms.m:
            if self.tiles[x][y] is None:
                self.tiles[x][y] = l
            else:
                raise Exception('cannot place move - there is something here!')

    def get_word_score(self, ms, word):
        '''
        Returns the score of a particular word on the board, given all the
        bonuses gotten from moveset ms. Doesn't validate the moveset, though.
        '''
        word_bonus = 1
        score = 0
        if word[0][1] == word[2][1]:
            # Horizontal word (y is same)
            for x in range(word[0][0], word[2][0] + 1):
                # Tries to obtain the letter in moveset and check that there is
                # also a bonus tile of significant nature
                try:
                    i, j, l = ms.get_item(x, word[0][1])
                    # This tile is going to be placed on the board, so check if
                    # it exists in the bonus
                    letter_bonus = 1
                    if self.bonus[x][word[0][1]] in ['MD', 'DW']:
                        # Double word
                        word_bonus *= 2
                    elif self.bonus[x][word[0][1]] == 'DL':
                        # Double letter
                        letter_bonus = 2
                    elif self.bonus[x][word[0][1]] == 'TW':
                        # Triple word
                        word_bonus *= 3
                    elif self.bonus[x][word[0][1]] == 'TL':
                        # Triple letter
                        letter_bonus *= 3

                    score += wh.letterScore(word[1][x - word[0][0]]) * letter_bonus
                except:
                    # This tile is already on the board, so just count the score
                    score += wh.letterScore(word[1][x - word[0][0]])
        elif word[0][0] == word[2][0]:
            # Vertical word (x is same)
            for y in range(word[0][1], word[2][1] + 1):
                try:
                    i, j, l = ms.get_item(word[0][1], y)
                    # This tile is going to be placed on the board, so check if
                    # it exists in the bonus
                    letter_bonus = 1
                    if self.bonus[word[0][0]][y] in ['MD', 'DW']:
                        # Double word
                        word_bonus *= 2
                    elif self.bonus[word[0][0]][y] == 'DL':
                        # Double letter
                        letter_bonus = 2
                    elif self.bonus[word[0][0]][y] == 'TW':
                        # Triple word
                        word_bonus *= 3
                    elif self.bonus[word[0][0]][y] == 'TL':
                        # Triple letter
                        letter_bonus *= 3

                    score += wh.letterScore(word[1][y - word[0][1]]) * letter_bonus
                except:
                    # This tile is already on the board, so just count the score
                    score += wh.letterScore(word[1][y - word[0][1]])
        else:
            raise Exception('invalid word: neither horizontal nor vertical')

        if len(ms.m) == 7:
            return score * word_bonus + wh.BINGO_BONUS
        else:
            return score * word_bonus

    def get_score(self, ms):
        '''
        Returns the score of a particular moveset ms on the board, considering
        all the different bonuses it gets. Doesn't validate the moveset, though.
        '''
        words = self.find_connected_words(ms)
        return sum(map(lambda w: self.get_word_score(ms, w), words))

    def validate(self, ms, wd):
        '''
        Returns true if the moveset on the board is valid, and false if
        otherwise.
        '''
        if ms.t == "M":
            # It is a move
            # Moves are only valid if:
            #  - there exists at least 1 placed tile
            #  - placed tiles are in a line
            #  - placed tiles are adjacent to tiles (unless first move)
            #  - words that placed tiles make are valid with dictionary
            #  - if it is the first move, a tile must be on the center square
            return len(ms.m) > 0 and\
                   ms.validate(self.tiles) and\
                   self.validate_moveset(ms, wd)
        elif ms.t == "E":
            # It is an exchange
            # Exchanges are only valid if there are tiles placed on the board
            return len(ms.m) > 0
        elif ms.t == "P":
            # It is a pass
            # Passes are always valid
            return True
        else:
            # Throw an error for nothing that we've ever seen before
            raise Exception("error: invalid move type %s" % ms.t)

    def get_tile_pos(self, pos):
        '''
        Returns the 2D indices for position pos. Since the board is of constant
        size, it is assumed that position pos is already inside board. It will
        always return a position, and won't error.
        '''
        # Normalize position
        pos[0] -= self.pos[0]
        pos[1] -= self.pos[1]

        # Calculate integer division
        return (pos[0] // resman.Tile_Size[0],
                pos[1] // resman.Tile_Size[1])

    def get_tile(self, pos):
        '''
        Returns the character on the tile. If it is empty, returns None.
        '''
        ind = self.get_tile_pos(pos)
        return self.tiles[ind[0]][ind[1]]

    def remove_tile(self, pos):
        '''
        Replaces the character at position pos on the board with None value.
        If it is empty (None), it doesn't do a thing.
        '''
        ind = self.get_tile_pos(pos)
        self.tiles[ind[0]][ind[1]] = None

    def init_bonus(self, fn):
        '''
        Initializes bonuses using the file.
        '''
        self.bonus = [[]]
        f = open(fn, 'r')
        for line in f.readlines():
            for sym in line.rstrip().split():
                self.bonus[-1].append(sym)
            self.bonus.append([])

        f.close()

    def place(self, pos, letter):
        '''
        Converts letter to be placed into tile.Tile type.
        '''
        x, y = pos
        if self.tiles[x][y] is not None:
            raise Exception("error: tile exists")

        self.tiles[x][y] = tile.Tile(letter)

    def take_back(self, pos):
        '''
        Removes letter and returns it.
        '''
        x, y = pos
        t = self.tiles[x][y]

        if t is None:
            raise Exception("error: tile doesn't exist")

        self.tiles[x][y] = None
        return t

    def handle(self, evt):
        '''
        Handles all events, like dragging of tiles and typing.
        '''
        pass

    def draw(self, scrn, ms):
        '''
        Draws the scrabble board along with all the tiles.
        If tile is none, draw bonus
        if not, draw tiles (draw tile first, then bonus)
        If there is an active moveset, draws it as well
        '''
        for x in range(len(self.tiles)):
            # Draw the tiles (bonus or bust)
            for y in range(len(self.tiles[x])):
                if self.tiles[x][y] is None:
                    # Draw the bonus if there is no tile
                    scrn.blit(self.rman.tiles[self.bonus[x][y]], (x * 50, y * 50))
                else:
                    # Draw the tile otherwise
                    scrn.blit(self.rman.tiles[self.tiles[x][y]], (x * 50, y * 50))

        for x, y, l in ms.m:
            scrn.blit(self.rman.tiles[l], (x * 50, y * 50))

        # Draw the lines between the tiles
        for i in range(15):
            pygame.draw.aaline(scrn,
                               colors.BLACK,
                               (0, i * 50),
                               (800, i * 50))
            pygame.draw.aaline(scrn,
                               colors.BLACK,
                               (i * 50, 0),
                               (i * 50, 800))

    def update(self, delta):
        '''
        Updates the scrabble board.
        '''
        pass