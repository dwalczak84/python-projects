# -*- coding: utf-8 -*-
"""
Created on Sat Apr 08 16:31:05 2017

@author: Dariusz
"""

class TicTacToe:
    # Tic-Tac-Toe 10-sizer game board initialization.
    def __init__(self):
        """Start a new game."""
        self._board = [ [' '] * 10 for j in range(10)]
        self._player = 'X'
        
    def mark(self, i, j):
        """Put an X or an O mark at position (i,j) for next player's turn."""
        if not (0 <= i <= 9 and 0 <= j <= 9):
            raise ValueError('Invalid board position')
        if self._board[i][j] != ' ':
            raise ValueError('Board position occupied')
        if self._player == 'X':
            self._board[i][j] = 'X'            
            self._player = 'O'
        else:
            self._board[i][j] = 'O'
            self._player = 'X'
            
    def _is_win(self, mark):
        # check board for possible winner        
        # need five consecutive marks to win the game.
        board = self._board
    
        # check for 5 consecutive Xs or Os:
        for row in board:
            for mark in ('X' * 5, 'O' * 5):
                if mark in ''.join(row): 
                    return True
        
        # check for 5 consecutive Xs Os in columns:
        for j in range(10):
            for mark in ('X' * 5, 'O' * 5):
                if mark in ''.join(map(lambda i: board[i][j], range(10))):
                    return True
    
        # possible diagonals:
        for mark in ('X' * 5, 'O' * 5):
            if mark in ''.join([board[i][j] for i, j in zip(range(5, 10), range(5))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(4, 10), range(6))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(3, 10), range(7))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(2, 10), range(8))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(1, 10), range(9))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(10), range(10))]) or \
                mark in ''.join([board[i][j] for i, j in zip(range(9), range(1, 10))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(8), range(2, 10))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(7), range(3, 10))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(6), range(4, 10))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(5), range(5, 10))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(5), range(4, -1, -1))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(6), range(5, -1, -1))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(7), range(6, -1, -1))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(8), range(7, -1, -1))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(9), range(8, -1, -1))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(10), range(9, -1, -1))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(1, 10), range(9, 0, -1))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(2, 10), range(9, 1, -1))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(3, 10), range(9, 2, -1))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(4, 10), range(9, 3, -1))]) or\
                mark in ''.join([board[i][j] for i, j in zip(range(5, 10), range(9, 4, -1))]):
                    return True
                       
        
    def winner(self):
        # Return mark of winning player, or None to indicate a tie
        for mark in 'XO':
            if self._is_win(mark):
                return mark
            return None
    
    def __str__(self):
        rows = [' | '.join(self._board[r]) for r in range(10)]
        return '\n-------------------------------------\n'.join(rows)
        

if __name__ == "__main__":
    game = TicTacToe()
    print 'Welcome to Tic Tac Toe game.'
    print 'Player X is starting a game..\n'
    while True:
        print 'Current board view:\n'
        print(game)
        print '\nSelect a place on the board where you want to place your mark.'
        print 'Enter two coordinates, separated by single space:\n'
        print '\n'
        i, j = map(int, raw_input().strip().split(' '))
        print '\n'
        try:
            game.mark(i, j)
        except Exception as e:
            print e
            continue
        if game.winner():
            print 'Game over.'
            print 'Player', game.winner(), 'won the game.\n'
            print (game)
            break