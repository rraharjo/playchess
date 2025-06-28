from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from chess.board import ChessBoard

class PieceType(Enum):
    PAWN = 0
    ROOK = 1
    KNIGHT = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5
    
    def __str__(self) -> str:
        return self.name
    
class PieceColor(Enum):
    WHITE = 0
    BLACK = 1
    
    def __str__(self) -> str:
        return self.name
    
class MoveType(Enum):
    REGULAR = 0
    ENPASSANT = 1
    PROMOTION = 2
    CASTLESHORT = 3
    CASTLELONG = 4
    PAWNFIRSTMOVE = 5
    ROOKFIRSTMOVE = 6
    KINGFIRSTMOVE = 7
    
class ChessPiece(ABC):
    def __init__(self, board: ChessBoard, type: PieceType, color: PieceColor, position: int):
        self._board: ChessBoard = board
        self._type: PieceType = type
        self._color: PieceColor = color
        self._position: int = position
        self._numOfMove: int = 0
    
    def move(self, dest: int) -> MoveType:
        self._numOfMove += 1
        self._position = dest
        return MoveType.REGULAR
    
    def unMove(self, src: int) -> None:
        self._numOfMove -= 1
        self._position = src
    
    def _canMove(self, dest: int) -> bool:
        if dest >= 64:
            return False
        if dest < 0:
            return False
        if self._board[dest] is None or (isinstance(self._board[dest], ChessPiece) and self._board[dest]._color != self._color):
            return True
        return False
    
    def __str__(self) -> str:
        return f"{self._color.__str__()} {self._type.__str__()}"
    
    @abstractmethod
    def legal_moves(self) -> list[int]:
        pass
    
    @abstractmethod
    def letter(self) -> str:
        pass

class Pawn(ChessPiece): 
    def __init__(self, board: ChessBoard, color: PieceColor, position: int): 
        super().__init__(board, PieceType.PAWN, color, position)
        self.enPassable: bool = False
        self.enPassableAt: int = -1
    
    def move(self, dest: int) -> ChessPiece:
        self._numOfMove += 1
        toRet: MoveType = MoveType.REGULAR
        if self._numOfMove == 1:
            toRet = MoveType.PAWNFIRSTMOVE
        multiplier: int
        if self._color == PieceColor.BLACK:
            multiplier = -8
        else:
            multiplier = 8
        
        # move two steps
        if dest == self._position + (2 * multiplier):
            self.enPassable = True
        
        # capture en passant
        if abs(dest - self._position) == 8 + 1:
            maybePawn: Pawn = self._board[dest - multiplier]
            if isinstance(maybePawn, Pawn) and maybePawn._color != self._color and maybePawn.enPassable:
                toRet = MoveType.ENPASSANT
                # self._board.enPassantStale.clear()
        
        # promotion
        if self._color == PieceColor.BLACK and 0 <= dest <= 7:
            toRet = MoveType.PROMOTION

        if self._color == PieceColor.WHITE and 56 <= dest <= 63:
            toRet = MoveType.PROMOTION
        
        self._position = dest
        return toRet
        
    def unMove(self, src: int) -> None: 
        super().unMove(src)
        if self._numOfMove == 1 and 24 <= src < 40:
            self.enPassable = True
    
    def legal_moves(self) -> list[int]:
        toRet: list[int] = []
        multiplier: int
        if self._color == PieceColor.BLACK:
            multiplier = -8
        else:
            multiplier = 8
        
        # First move - two steps ahead
        if self._numOfMove == 0 and self._board[self._position + multiplier] == None and self._board[self._position + (2 * multiplier)] == None:
            toRet.append(self._position + (2 * multiplier))
        
        # Regular move - one step ahead
        if self._board[self._position + multiplier] == None:
            toRet.append(self._position + multiplier)
        
        # capture right
        if self._position % 8 != 8 - 1 and 0 <= self._position + multiplier + 1 < 8 ** 2 and self._board[self._position + multiplier + 1] is not None and self._board[self._position + multiplier + 1]._color != self._color:
            toRet.append(self._position + multiplier + 1)
        
        # capture left
        if self._position % 8 != 0 and 0 <= self._position + multiplier - 1 < 8 ** 2 and self._board[self._position + multiplier - 1] is not None and self._board[self._position + multiplier - 1]._color != self._color:
            toRet.append(self._position + multiplier - 1)
        
        # en passant right
        if self._position % 8 != 8 - 1 and isinstance(self._board[self._position + 1], Pawn):
            rightPiece: Pawn = self._board[self._position + 1]
            if rightPiece.enPassable and rightPiece._color != self._color:
                toRet.append(self._position + multiplier + 1)
        
        # en passant left
        if self._position % 8 != 0 and isinstance(self._board[self._position - 1], Pawn):
            leftPiece: Pawn = self._board[self._position - 1]
            if leftPiece.enPassable and leftPiece._color != self._color:
                toRet.append(self._position + multiplier - 1)
        return toRet
        
    def letter(self):
        if self._color == PieceColor.BLACK:
            return "p"
        else:
            return "P"
        
    def promote(self, to: str) -> ChessPiece:
        if to.lower() == 'r':
            return Rook(self._board, self._color, self._position)
        elif to.lower() == 'k': 
            return Knight(self._board, self._color, self._position)
        elif to.lower() == 'b': 
            return Bishop(self._board, self._color, self._position)
        elif to.lower() == 'q': 
            return Queen(self._board, self._color, self._position)
        else:
            raise ValueError("Can't evolve to " + to)

class Rook(ChessPiece):
    def __init__(self, board: ChessBoard, color: PieceColor, position: int):
        super().__init__(board, PieceType.ROOK, color, position)

    def legal_moves(self):
        toRet: list[int] = []
        row, col = divmod(self._position, 8)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                dest = r * 8 + c
                if self._canMove(dest):
                    toRet.append(dest)
                else:
                    break

        return toRet

    def move(self, dest):
        self._numOfMove += 1
        toRet: MoveType = MoveType.REGULAR
        if self._numOfMove == 1:
            toRet = MoveType.ROOKFIRSTMOVE
        self._position = dest
        return toRet
        
    def letter(self):
        if self._color == PieceColor.BLACK:
            return "r"
        else:
            return "R"


class Knight(ChessPiece):
    def __init__(self, board: ChessBoard, color: PieceColor, position: int):
        super().__init__(board, PieceType.KNIGHT, color, position)

    def legal_moves(self):
        toRet: list[int] = []
        row, col = divmod(self._position, 8)
        deltas = [
            (-2, -1), (-2, +1),
            (-1, -2), (-1, +2),
            (+1, -2), (+1, +2),
            (+2, -1), (+2, +1),
        ]

        for dr, dc in deltas:
            new_row = row + dr
            new_col = col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                new_idx = new_row * 8 + new_col
                if self._canMove(new_idx):
                    toRet.append(new_idx)

        return toRet
    def letter(self):
        if self._color == PieceColor.BLACK:
            return "k"
        else:
            return "K"


class Bishop(ChessPiece):
    def __init__(self, board: ChessBoard, color: PieceColor, position: int):
        super().__init__(board, PieceType.BISHOP, color, position)

    def legal_moves(self):
        toRet: list[int] = []
        row, col = divmod(self._position, 8)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] 

        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                dest = r * 8 + c
                if self._canMove(dest):
                    toRet.append(dest)
                else:
                    break

        return toRet
    def letter(self):
        if self._color == PieceColor.BLACK:
            return "b"
        else:
            return "B"


class Queen(ChessPiece):
    def __init__(self, board: ChessBoard, color: PieceColor, position: int):
        super().__init__(board, PieceType.QUEEN, color, position)

    def legal_moves(self):
        toRet: list[int] = []
        row, col = divmod(self._position, 8)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                dest = r * 8 + c
                if self._canMove(dest):
                    toRet.append(dest)
                else:
                    break

        return toRet
    def letter(self):
        if self._color == PieceColor.BLACK:
            return "q"
        else:
            return "Q"


class King(ChessPiece):
    def __init__(self, board: ChessBoard, color: PieceColor, position: int):
        super().__init__(board, PieceType.KING, color, position)

    def canCastle(self, short: bool) -> bool:
        if self._numOfMove != 0:
            return False
        multiplier: int = 1 if short else -1
        if self._board[self._position + 1 * multiplier] is not None or self._board[self._position + 2 * multiplier] is not None:
            return False
        if not short and self._board[self._position + 3 * multiplier] is not None:
            return False
        maybeRook: Rook = self._board[self._position + 3 * multiplier] if short else self._board[self._position + 4 * multiplier]
        if not isinstance(maybeRook, Rook) or maybeRook._numOfMove != 0 or maybeRook._color != self._color:
            return False
        opponentColor: PieceColor = PieceColor.BLACK if self._color == PieceColor.WHITE else PieceColor.WHITE
        opponentMoves: set[int] = self._board.getPiecesMoves(opponentColor, [PieceType.PAWN,
                                                                             PieceType.ROOK,
                                                                             PieceType.KNIGHT,
                                                                             PieceType.BISHOP,
                                                                             PieceType.QUEEN])
        if self._position in opponentMoves or self._position + 1 * multiplier in opponentMoves or self._position + 2 * multiplier in opponentMoves:
            return False
        return True

    def legal_moves(self):
        toRet: list[int] = []
        row, col = divmod(self._position, 8)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            r, c = row, col
            r += dy
            c += dx
            if not (0 <= r < 8 and 0 <= c < 8):
                continue
            dest: int = self._position + 8 * dy + dx
            if self._canMove(dest):
                toRet.append(dest)
        if self.canCastle(True):
            toRet.append(self._position + 2)
        if self.canCastle(False):
            toRet.append(self._position - 2)
        return toRet

    def move(self, dest):
        self._numOfMove += 1
        toRet: MoveType = MoveType.REGULAR
        if self._numOfMove == 1:
            toRet = MoveType.KINGFIRSTMOVE
        if dest == self._position + 2:
            toRet = MoveType.CASTLESHORT
        if dest == self._position - 2:
            toRet = MoveType.CASTLELONG
        self._position = dest
        return toRet

        
    def letter(self):
        if self._color == PieceColor.BLACK:
            return "k"
        else:
            return "K"
