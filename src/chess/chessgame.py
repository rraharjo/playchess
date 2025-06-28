from chess.board import ChessBoard
from chess.pieces import PieceColor, PieceType, ChessPiece, Pawn
from chess.movement import Move, MoveType
from agent.abstract_agent import Agent
from agent.player_agent import PlayerAgent
from collections import deque

class Game():
    def __init__(self, board: ChessBoard, player1: Agent, player2: Agent):
        self._board: ChessBoard = board
        self._player1: Agent = player1
        self._player2: Agent = player2
        if self._player1.getTeam() == self._player2.getTeam():
            raise ValueError("Can't play when both player are on the same team")
        self._currentPlayer: Agent = self._player1 if self._player1.getTeam() == PieceColor.WHITE else self._player2
        self._moveHistory: deque = deque()
    
    def __switchPlayer(self) -> None:
        if self._currentPlayer == self._player1:
            self._currentPlayer = self._player2
        else:
            self._currentPlayer = self._player1
        
    def play(self) -> None:
        while True:
            availableMoves: set[str] = self._board.getLegalMoves(self._currentPlayer.getTeam())
            self._board.printBoard()
            if len(availableMoves) == 0:
                opponent: Agent = self._player1 if self._currentPlayer == self._player2 else self._player2
                if self._board.isCheck(self._currentPlayer.getTeam()):
                    print(opponent.getTeam(), "wins")
                else:
                    print("Draw")
                break
            print(str(self._currentPlayer.getTeam()) + "'s turn")
            
            while True:
                moveIn: str = self._currentPlayer.getMove()
                if moveIn in availableMoves:
                    src: int = self._board.chessNotationToIdx(moveIn[:2])
                    dst: int = self._board.chessNotationToIdx(moveIn[2:])
                    curMove = Move(src, dst, self._currentPlayer.getTeam())
                    self._board.move(curMove)
                    if curMove.moveType == MoveType.PROMOTION:
                        to:str = self._currentPlayer.getPawnPromotion()
                        definitelyPawn: Pawn = curMove.piece
                        curMove.promotion = definitelyPawn.promote(to)
                        self._board.promote(curMove)
                    self._moveHistory.append(curMove)
                    print(curMove.moveType)
                    break
                else:
                    print("Invalid Move")
            self.__switchPlayer()


if __name__ == "__main__":
    player1: PlayerAgent = PlayerAgent(PieceColor.WHITE)
    player2: PlayerAgent = PlayerAgent(PieceColor.BLACK)
    game: Game = Game(player1, player2)
    game.play()