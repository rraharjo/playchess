from typing import Optional
from chess.pieces import *

BOARD_W = 8
class ChessBoard:
    def __init__(self):
        self.enPassantStale: list[Pawn] = []
        self.pawnPromotion:list[Pawn] = []
        self.__board: list[Optional[ChessPiece]] = [None] * (BOARD_W * BOARD_W)

        # White back rank (row 0)
        self.__board[0] = Rook(self, PieceColor.WHITE, 0)
        self.__board[1] = Knight(self, PieceColor.WHITE, 1)
        self.__board[2] = Bishop(self, PieceColor.WHITE, 2)
        self.__board[3] = Queen(self, PieceColor.WHITE, 3)
        self.__board[4] = King(self, PieceColor.WHITE, 4)
        self.__board[5] = Bishop(self, PieceColor.WHITE, 5)
        self.__board[6] = Knight(self, PieceColor.WHITE, 6)
        self.__board[7] = Rook(self, PieceColor.WHITE, 7)

        # White pawns (row 1)
        for i in range(8):
            self.__board[8 + i] = Pawn(self, PieceColor.WHITE, 8 + i)

        # Black pawns (row 6)
        for i in range(8):
            self.__board[48 + i] = Pawn(self, PieceColor.BLACK, 48 + i)

        # Black back rank (row 7)
        self.__board[56] = Rook(self, PieceColor.BLACK, 56)
        self.__board[57] = Knight(self, PieceColor.BLACK, 57)
        self.__board[58] = Bishop(self, PieceColor.BLACK, 58)
        self.__board[59] = Queen(self, PieceColor.BLACK, 59)
        self.__board[60] = King(self, PieceColor.BLACK, 60)
        self.__board[61] = Bishop(self, PieceColor.BLACK, 61)
        self.__board[62] = Knight(self, PieceColor.BLACK, 62)
        self.__board[63] = Rook(self, PieceColor.BLACK, 63)
    
    def idxToChessNotation(self, idx: int) -> str:
        if idx < 0 or idx >= 64:
            raise ValueError("Invalid Position")
        row: int = idx // 8
        col: int = idx % 8
        colLetter: str = chr(ord('a') + col)
        return f"{colLetter}{row + 1}"
        
    def chessNotationToIdx(self, notation: str) -> int:
        if (len(notation) != 2 or notation[0] < 'a' or notation[0] > 'h' or notation[1] < '1' or notation[1] > '8'):
            raise ValueError("Invalid Position")
        col: int = ord(notation[0]) - ord('a')
        row: int = int(notation[1]) - 1
        return row * 8 + col
    
    def get_legal_moves(self, color: PieceColor) -> list[int]:
        toRet: list[int] = []
        for i in range(64):
            if self.__board[i] is not None and self.__board[i]._color == color:
                toRet.extend(self.__board[i].legal_moves())
        return toRet
    
    def printAllMoves(self, color: PieceColor) -> None:
        for i in range(64):
            if self.__board[i] is not None and self.__board[i]._color == color:
                print(self.__board[i]._type)
                for move in self.__board[i].legal_moves():
                    print(self.idxToChessNotation(move))
                print("")

    def printBoard(self) -> None:
        print("       BLACK     ")
        for row in range(BOARD_W - 1, -1, -1):
            line = []
            for col in range(BOARD_W):
                index = row * BOARD_W + col
                piece = self[index]
                line.append(piece.letter() if piece else '.')
            print(f"{row + 1} {' '.join(line)}")
        print("  a b c d e f g h")
        print("       WHITE     ")
    
    def print_arr(self) -> None:
        for i in range(len(self.__board)):
            if isinstance(self.__board[i], ChessPiece):
                print(self.__board[i].letter())
            else:
                print(".")
        
    def __getitem__(self, idx: int) -> Optional[ChessPiece]:
        if idx < 0 or idx >= BOARD_W ** 2:
            raise ValueError("Invalid position")
        return self.__board[idx]
    
    def __setitem__(self, idx: int, value: Optional[ChessPiece]) -> None:
        if idx < 0 or idx >= BOARD_W ** 2:
            raise ValueError("Invalid position")
        self.__board[idx] = value

if __name__ == "__main__":
    myBoard = ChessBoard()
    myBoard.printBoard()
    # myBoard.print_arr()