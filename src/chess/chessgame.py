from chess.board import ChessBoard
from chess.pieces import PieceColor, PieceType, Pawn
from chess.movement import Move
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
            curMove: Move
            while True:
                moveIn = self._currentPlayer.getMove()
                src: int = self._board.chessNotationToIdx(moveIn[:2])
                dst: int = self._board.chessNotationToIdx(moveIn[2:])
                if self._board[src] is not None and self._board[src]._color == self._currentPlayer.getTeam() and dst in self._board[src].legal_moves():
                    curMove = Move(src, dst, self._currentPlayer.getTeam())
                    if self._board[src]._type == PieceType.PAWN and (56 <= dst < 64 or 0 <= dst < 8):
                        to:str = self._currentPlayer.getPawnPromotion()
                        definitelyPawn: Pawn = self._board[src]
                        curMove.promotion = definitelyPawn.promote(to)
                    self._board.move(curMove)
                    break
                else:
                    print("Invalid Move")
            self.__switchPlayer()


if __name__ == "__main__":
    player1: PlayerAgent = PlayerAgent(PieceColor.WHITE)
    player2: PlayerAgent = PlayerAgent(PieceColor.BLACK)
    game: Game = Game(player1, player2)
    game.play()