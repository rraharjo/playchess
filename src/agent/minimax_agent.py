from agent.abstract_agent import Agent
from agent.scorer import BoardScorer, PruningScorer, SimpleScorer
from chess.pieces import PieceColor
from chess.board import ChessBoard
from chess.utils import chessNotationToIdx
from chess.movement import Move
import sys

class MinimaxAgent(Agent):
    def __init__(self, board: ChessBoard, team: PieceColor):
        super().__init__(team)
        self._board = board
        self._scorer = SimpleScorer()
        self.__MINIMAXDEPTH = 2
    
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
            src: int = chessNotationToIdx(move[:2])
            dst: int = chessNotationToIdx(move[2:])
            curMove: Move = Move(src, dst, currentTeam)
            board.move(curMove)
            oppMax: int = self.minimax(board, depth - 1, opponentColor)[1]
            if oppMax < minVal:
                minVal = oppMax
                toRet = (move, oppMax)
            board.unMove(curMove)
        return toRet

#WHITE -> maximizer
#BLACK -> minimizer
class PruningAgent(Agent):
    def __init__(self, board: ChessBoard, team: PieceColor):
        super().__init__(team)
        self._board = board
        self._scorer = PruningScorer()
        self.__MINIMAXDEPTH = 3
    
    def getMove(self) -> str:
        clonedBoard: ChessBoard = self._board.clone()
        return self.pruning(clonedBoard, self.__MINIMAXDEPTH, self._team, None, None)[0]
    
    def getPawnPromotion(self) -> str:
        # :)
        return "q"
    
    def pruning(self, board: ChessBoard, depth: int, currentTeam: PieceColor, alpha: int, beta: int) -> tuple[str, int]:
        opponentColor: PieceColor = PieceColor.WHITE if currentTeam == PieceColor.BLACK else PieceColor.BLACK
        myMove: set[str] = board.getLegalMoves(currentTeam)
        if depth <= 0 or len(myMove) == 0 or len(board.getLegalMoves(opponentColor)) == 0:
            return ("", self._scorer.score(board, currentTeam))
        toRet: tuple[str, int]
        curScore: int = None
        for move in myMove:
            src: int = chessNotationToIdx(move[:2])
            dst: int = chessNotationToIdx(move[2:])
            curMove: Move = Move(src, dst, currentTeam)
            board.move(curMove)
            childScore: int = self.pruning(board, depth - 1, opponentColor, alpha, beta)[1]
            board.unMove(curMove)
            if currentTeam == PieceColor.WHITE: #Maximizer
                if curScore == None:
                    curScore = childScore
                    toRet = (move, curScore)
                elif curScore < childScore:
                    curScore = childScore
                    toRet = (move, curScore)
                if alpha is None:
                    alpha = curScore
                else:
                    alpha = max(alpha, curScore)
                if beta is not None and beta <= alpha:
                    break

            else: #Minimizer
                if curScore == None:
                    curScore = childScore
                    toRet = (move, curScore)
                elif curScore > childScore:
                    curScore = childScore
                    toRet = (move, curScore)
                if beta is None:
                    beta = curScore
                else:
                    beta = min(beta, curScore)
                if alpha is not None and beta <= alpha:
                    break

        return toRet
