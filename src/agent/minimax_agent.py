from agent.abstract_agent import Agent
from agent.scorer import BoardScorer
from chess.pieces import PieceColor
from chess.board import ChessBoard
from chess.movement import Move
import sys

class MinimaxAgent(Agent):
    def __init__(self, board: ChessBoard, team: PieceColor, scorer: BoardScorer):
        super().__init__(team)
        self._board = board
        self._scorer = scorer
        self.__MINIMAXDEPTH = 3
    
    def getMove(self) -> str:
        clonedBoard: ChessBoard = self._board.clone()
        return self.minimax(clonedBoard, self.__MINIMAXDEPTH, self._team)[0]
    
    def getPawnPromotion(self) -> str:
        # :)
        return "q"
    
    def minimax(self, board: ChessBoard, depth: int, currentTeam: PieceColor) -> tuple[str, int]:
        opponentColor: PieceColor = PieceColor.WHITE if currentTeam == PieceColor.BLACK else PieceColor.BLACK
        myMove: set[str] = board.getLegalMoves(currentTeam)
        if depth <= 0 or len(myMove) == 0 or len(board.getLegalMoves(opponentColor)) == 0:
            return ("", self._scorer.score(board, currentTeam))
        toRet: tuple[str, int]
        minVal: int = sys.maxsize
        for move in myMove:
            src: int = ChessBoard.chessNotationToIdx(move[:2])
            dst: int = ChessBoard.chessNotationToIdx(move[2:])
            curMove: Move = Move(src, dst, currentTeam)
            board.move(curMove)
            oppMax: int = self.minimax(board, depth - 1, opponentColor)[1]
            if oppMax < minVal:
                minVal = oppMax
                toRet = (move, oppMax)
            board.unMove(curMove)
        return toRet
