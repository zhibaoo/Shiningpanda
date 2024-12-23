def evaluate_board(board, stone):
    """強化された評価関数"""
    stable_discs = 0
    mobility = 0
    corner_positions = [(0, 0), (0, len(board) - 1), (len(board[0]) - 1, 0), (len(board[0]) - 1, len(board) - 1)]
    bad_positions = [(1, 0), (0, 1), (1, 1), (len(board[0]) - 2, 0), (len(board[0]) - 1, 1),
                     (len(board[0]) - 2, 1), (0, len(board) - 2), (1, len(board) - 1), (1, len(board) - 2),
                     (len(board[0]) - 2, len(board) - 1), (len(board[0]) - 1, len(board) - 2)]

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                if (x, y) in corner_positions:
                    stable_discs += 500
                elif (x, y) in bad_positions:
                    stable_discs -= 150
                else:
                    stable_discs += 1

    # モビリティ（合法手数）
    my_moves = len(get_legal_moves(board, stone))
    opponent_moves = len(get_legal_moves(board, 3 - stone))
    mobility = (my_moves - opponent_moves) * 30

    # 石数の優位性を考慮（終盤強化）
    total_stones = sum(row.count(BLACK) + row.count(WHITE) for row in board)
    stone_count_bonus = sum(row.count(stone) for row in board) if total_stones > 50 else 0

    return stable_discs + mobility + stone_count_bonus * 10

class PandaAI:
    def face(self):
        return "💕"

    def place(self, board, stone):
        depth = self.determine_depth(board)
        _, best_move = self.alpha_beta(board, stone, depth, -math.inf, math.inf, True)
        return best_move

    def determine_depth(self, board):
        """局面に応じた探索深度を動的に設定"""
        total_stones = sum(row.count(BLACK) + row.count(WHITE) for row in board)
        if total_stones < 20:
            return 5
        elif total_stones < 50:
            return 10
        else:
            return 16

    def alpha_beta(self, board, stone, depth, alpha, beta, maximizing):
        legal_moves = get_legal_moves(board, stone)
        if depth == 0 or not legal_moves:
            return evaluate_board(board, stone), None

        best_move = None

        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                x, y = move
                simulated_board = [row[:] for row in board]
                simulate_place(simulated_board, stone, x, y)
                eval, _ = self.alpha_beta(simulated_board, 3 - stone, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in legal_moves:
                x, y = move
                simulated_board = [row[:] for row in board]
                simulate_place(simulated_board, stone, x, y)
                eval, _ = self.alpha_beta(simulated_board, 3 - stone, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

play_othello(PandaAI())
