from abc import ABC, abstractmethod
from chess.pieces import PieceColor

class Agent(ABC):
    def __init__(self, team: PieceColor):
        self.__team = team
    
    def getTeam(self) -> PieceColor:
        return self.__team
    
    @abstractmethod
    def getMove(self) -> str:
        pass
    
    @abstractmethod
    def getPawnPromotion(self) -> str:
        pass