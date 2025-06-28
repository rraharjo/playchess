from typing import Optional
from chess.pieces import *
from chess.movement import Move

BOARD_W = 8
class ChessBoard:
    def __init__(self):
        self.curNumOfMove: int = 0
        self.whitePieces: list[ChessPiece] = []
        self.blackPieces: list[ChessPiece] = []
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

        # # Black pawns (row 6)
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
        
        for i in range(0, 16):
            if self.__board[i] is not None:
                self.whitePieces.append(self.__board[i])
        for i in range(48, 64):
            if self.__board[i] is not None:
                self.blackPieces.append(self.__board[i])
    
    def move(self, move: Move) -> None:
        self.curNumOfMove += 1
        move.piece = self.__board[move.src]
        moveType: MoveType = move.piece.move(move.dst)
        move.moveType = moveType
        opponentPieces: list[ChessPiece] = self.blackPieces if move.color == PieceColor.WHITE else self.whitePieces
        
        # print(moveType)
        if moveType == MoveType.REGULAR or moveType == MoveType.ROOKFIRSTMOVE or moveType == MoveType.KINGFIRSTMOVE:
            move.captured = self.__board[move.dst]
        elif moveType == MoveType.PAWNFIRSTMOVE:
            move.captured = self.__board[move.dst]
            definitelyPawn: Pawn = move.piece
            if definitelyPawn.enPassable:
                definitelyPawn.enPassableAt = self.curNumOfMove + 1
        elif moveType == MoveType.PROMOTION:
            move.captured = self.__board[move.dst]
            self.__board[move.dst] = move.promotion
            self.__board[move.src] = None
            if move.captured is not None:
                opponentPieces.remove(move.captured)
            return
        elif moveType == MoveType.ENPASSANT:
            if move.piece._color == PieceColor.WHITE:
                move.captured = self.__board[move.dst - 8]
                self.__board[move.dst - 8] = None
            else:
                move.captured = self.__board[move.dst + 8]
                self.__board[move.dst + 8] = None
        elif moveType == MoveType.CASTLESHORT:
            self.__board[move.src + 3].move(move.src + 1)
            self.__board[move.src + 1] = self.__board[move.src + 3]
            self.__board[move.src + 3] = None
        elif moveType == MoveType.CASTLELONG:
            self.__board[move.src - 4].move(move.src - 1)
            self.__board[move.src - 1] = self.__board[move.src - 4]
            self.__board[move.src - 4] = None
        
        if move.captured is not None:
            opponentPieces.remove(move.captured)

        self.__board[move.dst] = self.__board[move.src]
        self.__board[move.src] = None
        
        for piece in opponentPieces:
            if piece._type == PieceType.PAWN:
                pawn: Pawn = piece
                pawn.enPassable = False
    
    def unMove(self, move: Move) -> None:
        if self.curNumOfMove == 0:
            raise ValueError("No movements have been made")
        opponentPieces: list[ChessPiece] = self.blackPieces if move.color == PieceColor.WHITE else self.whitePieces
        playerPieces: list[ChessPiece] = self.blackPieces if move.color == PieceColor.BLACK else self.whitePieces
        self.__board[move.dst].unMove(move.src)
        if move.moveType == MoveType.CASTLESHORT:
            definitelyRook: Rook = self.__board[move.dst - 1]
            definitelyRook.unMove(definitelyRook._position + 2)
            self.__board[definitelyRook._position] = definitelyRook
            self.__board[move.dst - 1] = None
        elif move.moveType == MoveType.CASTLELONG:
            definitelyRook: Rook = self.__board[move.dst + 1]
            definitelyRook.unMove(definitelyRook._position - 3)
            self.__board[definitelyRook._position] = definitelyRook
            self.__board[move.dst + 1] = None     
            
        self.__board[move.src] = self.__board[move.dst]
        self.__board[move.dst] = None
        if move.captured is not None:
            self.__board[move.captured._position] = move.captured
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
            if isinstance(self.__board[i], King) and self.__board[i]._color == color:
                kingPos = i
                break
        if kingPos in oppMoves:
            return True
        return False
    
    @staticmethod
    def idxToChessNotation(idx: int) -> str:
        if idx < 0 or idx >= 64:
            raise ValueError("Invalid Position")
        row: int = idx // 8
        col: int = idx % 8
        colLetter: str = chr(ord('a') + col)
        return f"{colLetter}{row + 1}"
        
    @staticmethod
    def chessNotationToIdx(notation: str) -> int:
        if (len(notation) != 2 or notation[0] < 'a' or notation[0] > 'h' or notation[1] < '1' or notation[1] > '8'):
            raise ValueError("Invalid Position")
        col: int = ord(notation[0]) - ord('a')
        row: int = int(notation[1]) - 1
        return row * 8 + col
    
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
                    toRet.add(f"{self.idxToChessNotation(src)}{self.idxToChessNotation(dst)}")
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
            if self.__board[i] is not None and self.__board[i]._color == color and self.__board[i]._type in pieceType:
                toRet.extend(self.__board[i].legal_moves())
        return set(toRet)
    
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