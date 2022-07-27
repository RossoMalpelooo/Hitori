from boardgame import BoardGame
from boardgamegui import BoardGameGui
from boardgamegui import gui_play

def main():
    game = BoardGame("hitori-6x6-16075.txt")
    gui_play(game)

main()