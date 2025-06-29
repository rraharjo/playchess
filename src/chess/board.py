from typing import Optional
from copy import deepcopy
from chess.pieces import *
from chess.movement import Move
from chess.utils import idxToChessNotation

BOARD_W = 8
class ChessBoard:
    def __init__(self):
        self.curNumOfMove: int = 0
        self.whitePieces: list[ChessPiece] = []
        self.blackPieces: list[ChessPiece] = []
        self._board: list[Optional[ChessPiece]] = [None] * (BOARD_W * BOARD_W)

        # White back rank (row 0)
        self._board[0] = Rook(self, PieceColor.WHITE, 0)
        self._board[1] = Knight(self, PieceColor.WHITE, 1)
        self._board[2] = Bishop(self, PieceColor.WHITE, 2)
        self._board[3] = Queen(self, PieceColor.WHITE, 3)
        self._board[4] = King(self, PieceColor.WHITE, 4)
        self._board[5] = Bishop(self, PieceColor.WHITE, 5)
        self._board[6] = Knight(self, PieceColor.WHITE, 6)
        self._board[7] = Rook(self, PieceColor.WHITE, 7)

        # White pawns (row 1)
        for i in range(8):
            self._board[8 + i] = Pawn(self, PieceColor.WHITE, 8 + i)

        # # Black pawns (row 6)
        for i in range(8):
            self._board[48 + i] = Pawn(self, PieceColor.BLACK, 48 + i)

        # Black back rank (row 7)
        self._board[56] = Rook(self, PieceColor.BLACK, 56)
        self._board[57] = Knight(self, PieceColor.BLACK, 57)
        self._board[58] = Bishop(self, PieceColor.BLACK, 58)
        self._board[59] = Queen(self, PieceColor.BLACK, 59)
        self._board[60] = King(self, PieceColor.BLACK, 60)
        self._board[61] = Bishop(self, PieceColor.BLACK, 61)
        self._board[62] = Knight(self, PieceColor.BLACK, 62)
        self._board[63] = Rook(self, PieceColor.BLACK, 63)
        
        for i in range(0, 16):
            if self._board[i] is not None:
                self.whitePieces.append(self._board[i])
        for i in range(48, 64):
            if self._board[i] is not None:
                self.blackPieces.append(self._board[i])
    
    def move(self, move: Move) -> None:
        self.curNumOfMove += 1
        move.piece = self._board[move.src]
        moveType: MoveType = move.piece.move(move.dst)
        move.moveType = moveType
        opponentPieces: list[ChessPiece] = self.blackPieces if move.color == PieceColor.WHITE else self.whitePieces
        
        if moveType == MoveType.REGULAR or moveType == MoveType.ROOKFIRSTMOVE or moveType == MoveType.KINGFIRSTMOVE or moveType == MoveType.PROMOTION:
            move.captured = self._board[move.dst]
        elif moveType == MoveType.PAWNFIRSTMOVE:
            move.captured = self._board[move.dst]
            definitelyPawn: Pawn = move.piece
            if definitelyPawn.enPassable:
                definitelyPawn.enPassableAt = self.curNumOfMove + 1
        elif moveType == MoveType.ENPASSANT:
            if move.piece._color == PieceColor.WHITE:
                move.captured = self._board[move.dst - 8]
                self._board[move.dst - 8] = None
            else:
                move.captured = self._board[move.dst + 8]
                self._board[move.dst + 8] = None
        elif moveType == MoveType.CASTLESHORT:
            self._board[move.src + 3].move(move.src + 1)
            self._board[move.src + 1] = self._board[move.src + 3]
            self._board[move.src + 3] = None
        elif moveType == MoveType.CASTLELONG:
            self._board[move.src - 4].move(move.src - 1)
            self._board[move.src - 1] = self._board[move.src - 4]
            self._board[move.src - 4] = None
        
        if move.captured is not None:
            opponentPieces.remove(move.captured)

        self._board[move.dst] = self._board[move.src]
        self._board[move.src] = None
        
        for piece in opponentPieces:
            if piece._type == PieceType.PAWN:
                pawn: Pawn = piece
                pawn.enPassable = False
            
    def promote(self, move: Move) -> None:
        curTeam: list[ChessPiece] = self.whitePieces if move.color == PieceColor.WHITE else self.blackPieces
        curTeam.append(move.promotion)
        curTeam.remove(move.piece)
        self._board[move.piece._position] = move.promotion
    
    def unMove(self, move: Move) -> None:
        if self.curNumOfMove == 0:
            raise ValueError("No movements have been made")
        opponentPieces: list[ChessPiece] = self.blackPieces if move.color == PieceColor.WHITE else self.whitePieces
        playerPieces: list[ChessPiece] = self.blackPieces if move.color == PieceColor.BLACK else self.whitePieces
        if move.moveType == MoveType.PROMOTION:
            self._board[move.dst] = move.piece
            if move.promotion is not None:
                playerPieces.append(move.piece)
                playerPieces.remove(move.promotion)
        self._board[move.dst].unMove(move.src)
        if move.moveType == MoveType.CASTLESHORT:
            definitelyRook: Rook = self._board[move.dst - 1]
            definitelyRook.unMove(definitelyRook._position + 2)
            self._board[definitelyRook._position] = definitelyRook
            self._board[move.dst - 1] = None
        elif move.moveType == MoveType.CASTLELONG:
            definitelyRook: Rook = self._board[move.dst + 1]
            definitelyRook.unMove(definitelyRook._position - 3)
            self._board[definitelyRook._position] = definitelyRook
            self._board[move.dst + 1] = None
            
        self._board[move.src] = self._board[move.dst]
        self._board[move.dst] = None
        if move.captured is not None:
            self._board[move.captured._position] = move.captured
            if move.captured._color == PieceColor.WHITE:
                self.whitePieces.append(move.captured)
            else:
                self.blackPieces.append(move.captured)
                
        for piece in opponentPieces:
            if piece._type == PieceType.PAWN:
                definitelyPawn: Pawn = piece
                if definitelyPawn.enPassableAt == self.curNumOfMove:
                    definitelyPawn.enPassable = True
                
        for piece in playerPieces:
            if piece._type == PieceType.PAWN:
                definitelyPawn: Pawn = piece
                if definitelyPawn.enPassable == self.curNumOfMove:
                    definitelyPawn.enPassableAt = -1
        self.curNumOfMove -= 1
        
        
    
    # check if the color is in check
    def isCheck(self, color: PieceColor) -> bool:
        opponentColor: PieceColor = PieceColor.BLACK if color == PieceColor.WHITE else PieceColor.WHITE
        oppMoves: set[int] = self.getPiecesMoves(opponentColor)
        kingPos: int
        for i in range(64):
            if isinstance(self._board[i], King) and self._board[i]._color == color:
                kingPos = i
                break
        if kingPos in oppMoves:
            return True
        return False
    
    def getLegalMoves(self, color: PieceColor) -> set[str]:
        toRet: set[str] = set()
        currentPieces: list[ChessPiece] = self.whitePieces if color == PieceColor.WHITE else self.blackPieces
        for piece in currentPieces:
            src: int = piece._position
            pieceMoves: list[int] = piece.legal_moves()
            for dst in pieceMoves:
                curMove = Move(src, dst, piece._color)
                self.move(curMove)
                if not self.isCheck(piece._color):
                    toRet.add(f"{idxToChessNotation(src)}{idxToChessNotation(dst)}")
                self.unMove(curMove)
        return toRet
    
    def getPiecesMoves(self, color: PieceColor, pieceType: list[PieceType] = [PieceType.PAWN,
                                                                             PieceType.ROOK,
                                                                             PieceType.KNIGHT,
                                                                             PieceType.BISHOP,
                                                                             PieceType.QUEEN,
                                                                             PieceType.KING]) -> set[int]:
        toRet: list[int] = []
        for i in range(64):
            if self._board[i] is not None and self._board[i]._color == color and self._board[i]._type in pieceType:
                toRet.extend(self._board[i].legal_moves())
        return set(toRet)
    
    def printAllMoves(self, color: PieceColor) -> None:
        for i in range(64):
            if self._board[i] is not None and self._board[i]._color == color:
                print(self._board[i]._type)
                for move in self._board[i].legal_moves():
                    print(idxToChessNotation(move))
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
        for i in range(len(self._board)):
            if isinstance(self._board[i], ChessPiece):
                print(self._board[i].letter())
            else:
                print(".")
        
    def __getitem__(self, idx: int) -> Optional[ChessPiece]:
        if idx < 0 or idx >= BOARD_W ** 2:
            raise ValueError("Invalid position")
        return self._board[idx]
    
    def __setitem__(self, idx: int, value: Optional[ChessPiece]) -> None:
        if idx < 0 or idx >= BOARD_W ** 2:
            raise ValueError("Invalid position")
        self._board[idx] = value
        
    def clone(self) -> "ChessBoard":
        toRet: ChessBoard = ChessBoard.__new__(ChessBoard)
        toRet.whitePieces = []
        toRet.blackPieces = []
        toRet.curNumOfMove = self.curNumOfMove
        toRet._board = deepcopy(self._board)
        for piece in toRet._board:
            if piece is not None:
                piece._board = toRet
                if piece._color == PieceColor.WHITE:
                    toRet.whitePieces.append(piece)
                else:
                    toRet.blackPieces.append(piece)
        return toRet
        

if __name__ == "__main__":
    myBoard = ChessBoard()
    myBoard.printBoard()
    # myBoard.print_arr()