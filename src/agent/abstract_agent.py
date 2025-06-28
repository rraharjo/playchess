from abc import ABC, abstractmethod
from chess.pieces import PieceColor
from chess.board import ChessBoard

class Agent(ABC):
    def __init__(self, team: PieceColor):
        self._team: PieceColor = team
    
    def getTeam(self) -> PieceColor:
        return self._team
    
    @abstractmethod
    def getMove(self) -> str:
        pass
    
    @abstractmethod
    def getPawnPromotion(self) -> str:
        pass