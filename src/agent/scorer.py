from abc import ABC, abstractmethod
from chess.board import ChessBoard
from chess.pieces import PieceColor, PieceType

class BoardScorer(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def score(self, board: ChessBoard, color: PieceColor) -> int:
        pass


class SimpleScorer(BoardScorer):
    scores: dict[PieceType, int] = {PieceType.KING: 0, 
                                    PieceType.PAWN: 1, 
                                    PieceType.KNIGHT: 3, 
                                    PieceType.BISHOP: 3, 
                                    PieceType.ROOK: 5, 
                                    PieceType.QUEEN: 9}
    def __init__(self):
        super().__init__()
    
    def score(self, board: ChessBoard, color: PieceColor) -> int:
        toRet: int = 0
        for piece in board._board:
            if piece is not None:
                score: int = SimpleScorer.scores[piece._type]
                if piece._color != color:
                    score = -score
                toRet += score
        return toRet