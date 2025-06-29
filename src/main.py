from chess.pieces import PieceColor
from chess.chessgame import Game
from chess.board import ChessBoard
from agent.abstract_agent import Agent
from agent.player_agent import PlayerAgent
from agent.minimax_agent import MinimaxAgent, PruningAgent
from agent.scorer import SimpleScorer
if __name__ == "__main__":
    board: ChessBoard = ChessBoard()
    player1: Agent = PruningAgent(board, PieceColor.WHITE)
    #player1: Agent = PlayerAgent(PieceColor.WHITE)
    player2: Agent = PruningAgent(board, PieceColor.BLACK)
    #player2: Agent = PlayerAgent(PieceColor.BLACK)
    game: Game = Game(board, player1, player2)
    game.play()