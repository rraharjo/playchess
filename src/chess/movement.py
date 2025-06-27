from __future__ import annotations
from chess.pieces import ChessPiece, PieceColor, MoveType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from chess.board import ChessBoard
class Move():
    def __init__(self, src: int, dst: int, color: PieceColor):
        self.color: PieceColor = color
        self.src: int = src
        self.dst: int = dst
        self.piece: ChessPiece = None
        self.captured: ChessPiece = None
        self.promotion: ChessPiece = None
        self.moveType: MoveType = None
    
    def __str__(self) -> str:
        toRet: str = f"{"Piece"<10}: {self.piece.__str__()}\n"
        toRet += f"{"From"<10}: {ChessBoard.idxToChessNotation(self.src)}\n"
        toRet += f"{"To"<10}: {ChessBoard.idxToChessNotation(self.dst)}\n"
        toRet += f"{"Captured"<10}: {self.captured.__str__() if self.captured is not None else "None"}"
        toRet += f"{"Promotion"<10}: {self.promotion.__str__() if self.promotion is not None else "None"}"
        return toRet
    