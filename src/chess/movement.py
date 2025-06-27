from chess.pieces import ChessPiece, PieceColor
class Move():
    def __init__(self, src: int, dst: int, color: PieceColor):
        self.color: PieceColor = color
        self.src: int = src
        self.dst: int = dst
        self.piece: ChessPiece = None
        self.captured: ChessPiece = None
        self.promotion: ChessPiece = None
    
    