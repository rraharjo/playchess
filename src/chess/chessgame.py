from chess.board import ChessBoard
from chess.pieces import PieceColor
from agent.abstract_agent import Agent
from agent.player_agent import PlayerAgent

class Game():
    def __init__(self, player1: Agent, player2: Agent):
        self._board: ChessBoard = ChessBoard()
        self._player1: Agent = player1
        self._player2: Agent = player2
        if self._player1.getTeam() == self._player2.getTeam():
            raise ValueError("Can't play when both player are on the same team")
        self._currentPlayer: Agent = self._player1 if self._player1.getTeam() == PieceColor.WHITE else self._player2
    
    def __switchPlayer(self) -> None:
        if self._currentPlayer == self._player1:
            self._currentPlayer = self._player2
        else:
            self._currentPlayer = self._player1
            
    def play(self) -> None:
        while True:
            self._board.printBoard()
            # self._board.printAllMoves(self._currentPlayer.getTeam())
            print(str(self._currentPlayer.getTeam()) + "'s turn")
            while True:
                curMove = self._currentPlayer.getMove()
                src: int = self._board.chessNotationToIdx(curMove[:2])
                dst: int = self._board.chessNotationToIdx(curMove[2:])
                if self._board[src] is not None and self._board[src]._color == self._currentPlayer.getTeam() and dst in self._board[src].legal_moves():
                    self._board[src].move(dst)
                    break
                else:
                    print("Invalid Move")
            for pawn in self._board.enPassantStale:
                if pawn._color != self._currentPlayer.getTeam():
                    pawn.enPassable = False
                    self._board.enPassantStale.remove(pawn)
                    break
            for pawn in self._board.pawnPromotion:
                to:str = self._currentPlayer.getPawnPromotion()
                self._board[pawn._position] = pawn.promote(to)
            self._board.pawnPromotion.clear()
            self.__switchPlayer()


if __name__ == "__main__":
    player1: PlayerAgent = PlayerAgent(PieceColor.WHITE)
    player2: PlayerAgent = PlayerAgent(PieceColor.BLACK)
    game: Game = Game(player1, player2)
    game.play()