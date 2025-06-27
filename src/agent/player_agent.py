from agent.abstract_agent import Agent
from chess.pieces import PieceColor

class PlayerAgent(Agent):
    def __init__(self, team: PieceColor):
        super().__init__(team)
    
    def getMove(self) -> str:
        while True:
            userInput = input("Enter movement: ")
            if userInput == "u":
                return userInput
            if len(userInput) != 4:
                print("Invalid input")
            elif not ("a" <= userInput[0] <= "h"):
                print("Invalid input")
            elif not ("1" <= userInput[1] <= "8"):
                print("Invalid input")
            elif not ("a" <= userInput[2] <= "h"):
                print("Invalid input")
            elif not ("1" <= userInput[3] <= "8"):
                print("Invalid input")
            else:
                return userInput
    
    def getPawnPromotion(self) -> str:
        while True:
            userInput = input("Enter promotion (r/k/b/q): ")
            if len(userInput) != 1:
                print("Invalid input")
            elif userInput != "r" and userInput != "k" and userInput != "b" and userInput != "q":
                print("Invalid input")
            else:
                return userInput