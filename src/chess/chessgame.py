from chess.board import ChessBoard
from chess.pieces import PieceColor, PieceType, ChessPiece, Pawn
from chess.movement import Move
from agent.abstract_agent import Agent
from agent.player_agent import PlayerAgent
from collections import deque

class Game():
    def __init__(self, player1: Agent, player2: Agent):
        self._board: ChessBoard = ChessBoard()
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
        
    def __getLegalMoves(self, player: Agent) -> set[str]:
        toRet: set[str] = set()
        currentPieces: list[ChessPiece] = self._board.whitePieces if player.getTeam() == PieceColor.WHITE else self._board.blackPieces
        for piece in currentPieces:
            src: int = piece._position
            pieceMoves: list[int] = piece.legal_moves()
            for dst in pieceMoves:
                curMove = Move(src, dst, piece._color)
                self._board.move(curMove)
                if not self._board.isCheck(piece._color):
                    toRet.add(f"{self._board.idxToChessNotation(src)}{self._board.idxToChessNotation(dst)}")
                self._board.unMove(curMove)
        return toRet
            
    def play(self) -> None:
        while True:
            availableMoves: set[str] = self.__getLegalMoves(self._currentPlayer)
            if len(availableMoves) == 0:
                opponent: Agent = self._player1 if self._currentPlayer == self._player2 else self._player2
                if self._board.isCheck(self._currentPlayer.getTeam()):
                    print(opponent.getTeam(), "wins")
                else:
                    print("Draw")
                break
            self._board.printBoard()
            print(str(self._currentPlayer.getTeam()) + "'s turn")
            
            while True:
                moveIn: str = self._currentPlayer.getMove()
                if moveIn in availableMoves:
                    src: int = self._board.chessNotationToIdx(moveIn[:2])
                    dst: int = self._board.chessNotationToIdx(moveIn[2:])
                    curMove = Move(src, dst, self._currentPlayer.getTeam())
                    if self._board[src]._type == PieceType.PAWN and (56 <= dst < 64 or 0 <= dst < 8):
                        to:str = self._currentPlayer.getPawnPromotion()
                        definitelyPawn: Pawn = self._board[src]
                        curMove.promotion = definitelyPawn.promote(to)
                    self._board.move(curMove)
                    self._moveHistory.append(curMove)
                    break
                else:
                    print("Invalid Move")
            self.__switchPlayer()


if __name__ == "__main__":
    player1: PlayerAgent = PlayerAgent(PieceColor.WHITE)
    player2: PlayerAgent = PlayerAgent(PieceColor.BLACK)
    game: Game = Game(player1, player2)
    game.play()