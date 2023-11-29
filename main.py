import chess
import chess.engine

class ChessGame:
    def __init__(self, human_starts=True):
        self.board = chess.Board()
        self.moves_history = []
        self.human_starts = human_starts

    def make_move(self, move):
        if move in self.board.legal_moves:
            self.moves_history.append(self.board.copy())
            self.board.push(move)
            return True
        else:
            return False

    def undo_move(self):
        if len(self.moves_history) > 0:
            self.board = self.moves_history.pop()
            return True
        else:
            return False

    def get_best_move(self):
        with chess.engine.SimpleEngine.popen_uci("./stockfish-windows-x86-64.exe") as engine:
            result = engine.play(self.board, chess.engine.Limit(time=2.0))
            return result.move

def print_board(board):
    print("\n  a  b  c  d  e  f  g  h")
    print("+-------------------------")
    for rank in range(8, 0, -1):
        row = f"{rank}|"
        for file in range(1, 9):
            square = chess.square(file - 1, rank - 1)
            piece = board.piece_at(square)

            if piece is not None:
                row += f" {piece.symbol()} "
            else:
                row += " . "
        print(row)

def main():
    human_starts = input("Quem começa jogando? (Você - 'v' / Adversário - 'a'): ").lower() == 'v'
    game = ChessGame(human_starts)

    while not game.board.is_game_over():
        print_board(game.board)

        if (game.board.turn == chess.WHITE and game.human_starts) or (game.board.turn == chess.BLACK and not game.human_starts):
            move_uci = input("Digite a sua jogada (notação UCI): ")

            if move_uci.lower() == 'undo':
                if game.undo_move():
                    print_board(game.board)
                else:
                    print("Não há jogadas para desfazer.")
            else:
                move = chess.Move.from_uci(move_uci)

                if game.make_move(move):
                    print_board(game.board)
                else:
                    print("Movimento inválido. Tente novamente.")
        else:
            move_uci = game.get_best_move().uci()
            print(f"Melhor jogada para as Pretas: {move_uci}")
            move = chess.Move.from_uci(move_uci)
            game.make_move(move)

    print("Fim do jogo. Resultado:", game.board.result())

if __name__ == "__main__":
    main()
