import tkinter as tk
from tkinter import messagebox
import json
import os
import hashlib

USERS_FILE = "users.json"

# Начальные позиции фигур (белые: Король(K), Пешка(P), Конь(N); чёрные: Король(k), Слон(b))
INITIAL_POSITIONS = {
    "K": (7, 4),  # Белый король
    "P": (6, 4),  # Белая пешка
    "N": (7, 1),  # Белый конь
    "k": (0, 4),  # Чёрный король
    "b": (0, 5),  # Чёрный слон
}

# Соответствие символов фигур юникодным шахматным фигурам:
PIECE_SYMBOLS = {
    "K": "\u2654",  # Белый король (&#9812;)
    "P": "\u2659",  # Белая пешка (&#9817;)
    "N": "\u2658",  # Белый конь (&#9816;)
    "k": "\u265A",  # Чёрный король (&#9818;)
    "b": "\u265D",  # Чёрный слон (&#9821;)
}


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


class AuthWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Авторизация")

        # Центрируем окно авторизации размером 300x200
        center_window(self.master, 300, 200)

        tk.Label(self.master, text="Логин:").pack(pady=5)
        self.login_entry = tk.Entry(self.master)
        self.login_entry.pack(pady=5)

        tk.Label(self.master, text="Пароль:").pack(pady=5)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.master, text="Войти", command=self.login).pack(pady=5)
        tk.Button(self.master, text="Регистрация", command=self.register).pack(pady=5)

        self.load_users()

    def load_users(self):
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'w') as f:
                json.dump({}, f)
        with open(USERS_FILE, 'r') as f:
            self.users = json.load(f)

    def save_users(self):
        with open(USERS_FILE, 'w') as f:
            json.dump(self.users, f)

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def login(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        if login in self.users and self.users[login] == self.hash_password(password):
            messagebox.showinfo("Успех", "Вы успешно авторизовались!")
            self.open_game_window(login)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

    def register(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        if not login or not password:
            messagebox.showerror("Ошибка", "Логин и пароль не могут быть пустыми!")
            return
        if login in self.users:
            messagebox.showerror("Ошибка", "Пользователь уже существует!")
            return
        self.users[login] = self.hash_password(password)
        self.save_users()
        messagebox.showinfo("Успех", "Регистрация прошла успешно! Теперь авторизуйтесь с использованием новых данных.")

    def open_game_window(self, username):
        self.master.destroy()
        root = tk.Tk()
        GameWindow(root, username)
        root.mainloop()


class GameWindow:
    def __init__(self, master, username):
        self.master = master
        self.master.title(f"Эндшпиль: Король, пешка, конь против Король, слон | Игрок: {username}")

        # Центрируем окно игры. Например, пусть будет 600x700 для поля и панелей.
        center_window(self.master, 600, 700)

        self.board_size = 8
        self.cell_size = 64
        self.selected_piece = None
        self.pieces_positions = INITIAL_POSITIONS.copy()

        self.current_turn = 'white'

        self.turn_label = tk.Label(self.master, text="Ход белых")
        self.turn_label.pack(pady=5)

        self.check_label = tk.Label(self.master, text="", fg="red")
        self.check_label.pack(pady=5)

        self.canvas = tk.Canvas(self.master, width=self.board_size * self.cell_size,
                                height=self.board_size * self.cell_size)
        self.canvas.pack()

        self.highlight_id = None

        self.draw_board()
        self.draw_pieces()
        self.update_check_status()

        self.canvas.bind("<Button-1>", self.on_click)

    # Далее код без изменений...
    def draw_board(self):
        self.canvas.delete("cell")
        colors = ["#EEEED2", "#769656"]
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(col * self.cell_size, row * self.cell_size,
                                             (col + 1) * self.cell_size, (row + 1) * self.cell_size,
                                             fill=color, outline=color, tags="cell")

    def draw_pieces(self):
        self.canvas.delete("piece")
        for piece, pos in self.pieces_positions.items():
            row, col = pos
            x = col * self.cell_size + self.cell_size / 2
            y = row * self.cell_size + self.cell_size / 2
            symbol = PIECE_SYMBOLS[piece]
            self.canvas.create_text(x, y, text=symbol, font=("Arial", 32, "bold"), tags="piece")
        self.highlight_selected_piece()

    def highlight_selected_piece(self):
        if self.highlight_id:
            self.canvas.delete(self.highlight_id)
            self.highlight_id = None

        if self.selected_piece:
            pos = self.pieces_positions[self.selected_piece]
            row, col = pos
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.highlight_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=3, tags="highlight")

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        clicked_piece = None
        for p, pos in self.pieces_positions.items():
            if pos == (row, col):
                clicked_piece = p
                break

        if self.selected_piece:
            piece = self.selected_piece
            from_pos = self.pieces_positions[piece]
            to_pos = (row, col)

            if self.can_move(piece, from_pos, to_pos):
                victim = self.get_enemy_at_pos(piece, to_pos)
                if victim and victim.lower() == 'k':
                    messagebox.showerror("Недопустимый ход", "Нельзя брать короля.")
                    self.selected_piece = None
                    self.draw_pieces()
                    return

                saved_positions = self.pieces_positions.copy()
                if victim:
                    del self.pieces_positions[victim]
                self.pieces_positions[piece] = to_pos

                if self.is_king_in_check('white' if piece.isupper() else 'black'):
                    self.pieces_positions = saved_positions
                    messagebox.showerror("Недопустимый ход", "Нельзя оставлять своего короля под шахом.")
                    self.selected_piece = None
                    self.draw_pieces()
                    return

                self.selected_piece = None
                self.draw_pieces()
                self.switch_turn()

                opponent_color = 'black' if self.current_turn == 'white' else 'white'
                if self.is_king_in_check(opponent_color) and not self.has_legal_moves(opponent_color):
                    messagebox.showinfo("Мат", f"{'Белые' if self.current_turn == 'black' else 'Чёрные'} поставили мат!")
                    self.canvas.unbind("<Button-1>")
                else:
                    if self.is_stalemate(opponent_color):
                        messagebox.showinfo("Пат", "Ничья (пат)!")
                        self.canvas.unbind("<Button-1>")

            else:
                messagebox.showerror("Недопустимый ход", "Этот ход не соответствует правилам.")
                self.selected_piece = None
                self.draw_pieces()
        else:
            if clicked_piece and self.can_select(clicked_piece):
                self.selected_piece = clicked_piece
            else:
                self.selected_piece = None
            self.draw_pieces()

    def can_select(self, piece):
        if self.current_turn == 'white' and piece.isupper():
            return True
        if self.current_turn == 'black' and piece.islower():
            return True
        return False

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        self.turn_label.config(text="Ход белых" if self.current_turn == 'white' else "Ход чёрных")
        self.update_check_status()

    def update_check_status(self):
        if self.is_king_in_check(self.current_turn):
            self.check_label.config(text="Шах!")
        else:
            self.check_label.config(text="")

    def can_move(self, piece, from_pos, to_pos):
        if from_pos == to_pos:
            return False
        if self.is_occupied_by_same_color(piece, to_pos):
            return False

        if piece.upper() == "P":
            return self.is_legal_pawn_move(piece, from_pos, to_pos)
        elif piece.upper() == "N":
            return self.is_legal_knight_move(piece, from_pos, to_pos)
        elif piece.upper() == "K":
            return self.is_legal_king_move(piece, from_pos, to_pos)
        elif piece.upper() == "B":
            return self.is_legal_bishop_move(piece, from_pos, to_pos)
        else:
            return False

    def is_occupied_by_same_color(self, piece, to_pos):
        is_white = piece.isupper()
        for p, pos in self.pieces_positions.items():
            if pos == to_pos:
                if p.isupper() and is_white:
                    return True
                if p.islower() and not is_white:
                    return True
        return False

    def get_enemy_at_pos(self, piece, pos):
        is_white = piece.isupper()
        for p, po in self.pieces_positions.items():
            if po == pos:
                if (p.isupper() and not is_white) or (p.islower() and is_white):
                    return p
        return None

    def is_free(self, pos):
        return all(po != pos for po in self.pieces_positions.values())

    def is_pawn_on_starting_position(self, piece, from_pos):
        if piece == 'P' and from_pos == (6, 4):
            return True
        return False

    def is_legal_pawn_move(self, piece, from_pos, to_pos):
        (fr, fc) = from_pos
        (tr, tc) = to_pos
        direction = -1 if piece.isupper() else 1
        if fc == tc and tr == fr + direction and self.is_free(to_pos):
            return True
        if piece == 'P' and self.is_pawn_on_starting_position(piece, from_pos):
            if fc == tc and tr == fr + 2 * direction and self.is_free((fr + direction, fc)) and self.is_free(to_pos):
                return True
        if abs(tc - fc) == 1 and tr == fr + direction and self.get_enemy_at_pos(piece, to_pos):
            victim = self.get_enemy_at_pos(piece, to_pos)
            if victim and victim.lower() == 'k':
                return False
            return True
        return False

    def is_legal_knight_move(self, piece, from_pos, to_pos):
        (fr, fc) = from_pos
        (tr, tc) = to_pos
        dr = abs(tr - fr)
        dc = abs(tc - fc)
        return (dr, dc) in [(2, 1), (1, 2)]

    def is_legal_king_move(self, piece, from_pos, to_pos):
        (fr, fc) = from_pos
        (tr, tc) = to_pos
        if abs(fr - tr) <= 1 and abs(fc - tc) <= 1:
            saved_positions = self.pieces_positions.copy()

            victim = self.get_enemy_at_pos(piece, to_pos)
            if victim and victim.lower() == 'k':
                return False

            if victim:
                del self.pieces_positions[victim]

            self.pieces_positions[piece] = to_pos
            color = 'white' if piece.isupper() else 'black'
            in_check = self.is_king_in_check(color)

            self.pieces_positions = saved_positions
            return not in_check
        return False

    def is_legal_bishop_move(self, piece, from_pos, to_pos):
        (fr, fc) = from_pos
        (tr, tc) = to_pos
        if abs(fr - tr) == abs(fc - tc):
            return self.is_path_clear_diagonal(from_pos, to_pos)
        return False

    def is_path_clear_diagonal(self, from_pos, to_pos):
        (fr, fc) = from_pos
        (tr, tc) = to_pos
        dr = 1 if tr > fr else -1
        dc = 1 if tc > fc else -1
        r = fr + dr
        c = fc + dc
        while (r, c) != (tr, tc):
            if not self.is_free((r, c)):
                return False
            r += dr
            c += dc
        return True

    def is_king_in_check(self, color):
        king_piece = 'K' if color == 'white' else 'k'
        king_pos = self.pieces_positions[king_piece]
        enemy_color = 'black' if color == 'white' else 'white'
        return self.is_square_attacked(king_pos, enemy_color)

    def is_square_attacked(self, pos, by_color):
        for p, ppos in self.pieces_positions.items():
            if by_color == 'white' and p.isupper():
                if p.upper() == 'P':
                    (r, c) = ppos
                    if (r - 1, c - 1) == pos or (r - 1, c + 1) == pos:
                        return True
                else:
                    if self.can_move(p, ppos, pos) and not self.is_own_king(p, pos):
                        return True

            elif by_color == 'black' and p.islower():
                if p.upper() == 'P':
                    (r, c) = ppos
                    if (r + 1, c - 1) == pos or (r + 1, c + 1) == pos:
                        return True
                else:
                    if self.can_move(p, ppos, pos) and not self.is_own_king(p, pos):
                        return True
        return False

    def is_own_king(self, piece, pos):
        for pc, ppos in self.pieces_positions.items():
            if ppos == pos:
                if piece.isupper() and pc == 'K':
                    return True
                if piece.islower() and pc == 'k':
                    return True
        return False

    def has_legal_moves(self, color):
        for piece, pos in self.pieces_positions.items():
            if color == 'white' and piece.isupper():
                moves = self.generate_moves_for_piece(piece, pos)
                for m in moves:
                    if self.try_move(piece, pos, m):
                        return True
            elif color == 'black' and piece.islower():
                moves = self.generate_moves_for_piece(piece, pos)
                for m in moves:
                    if self.try_move(piece, pos, m):
                        return True
        return False

    def try_move(self, piece, from_pos, to_pos):
        if not self.can_move(piece, from_pos, to_pos):
            return False
        saved_positions = self.pieces_positions.copy()
        victim = self.get_enemy_at_pos(piece, to_pos)
        if victim and victim.lower() == 'k':
            return False
        if victim:
            del self.pieces_positions[victim]
        self.pieces_positions[piece] = to_pos
        color = 'white' if piece.isupper() else 'black'
        in_check = self.is_king_in_check(color)
        self.pieces_positions = saved_positions
        return not in_check

    def generate_moves_for_piece(self, piece, pos):
        moves = []
        (r, c) = pos
        if piece.upper() == 'P':
            direction = -1 if piece.isupper() else 1
            f1 = (r + direction, c)
            if 0 <= f1[0] < 8 and 0 <= f1[1] < 8:
                moves.append(f1)
            if piece == 'P' and self.is_pawn_on_starting_position(piece, pos):
                f2 = (r + 2 * direction, c)
                if 0 <= f2[0] < 8 and 0 <= f2[1] < 8:
                    moves.append(f2)
            for dc in [-1, 1]:
                diag_pos = (r + direction, c + dc)
                if 0 <= diag_pos[0] < 8 and 0 <= diag_pos[1] < 8:
                    moves.append(diag_pos)
        elif piece.upper() == 'N':
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for (dr, dc) in knight_moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    moves.append((nr, nc))
        elif piece.upper() == 'K':
            king_moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for (dr, dc) in king_moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    moves.append((nr, nc))
        elif piece.upper() == 'B':
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for (dr, dc) in directions:
                nr, nc = r + dr, c + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    moves.append((nr, nc))
                    if not self.is_free((nr, nc)):
                        break
                    nr += dr
                    nc += dc
        return moves

    def is_stalemate(self, color):
        if self.is_king_in_check(color):
            return False
        if self.has_legal_moves(color):
            return False
        pieces_of_color = [p for p in self.pieces_positions if (p.isupper() if color == 'white' else p.islower())]
        if len(pieces_of_color) == 1 and (
                (color == 'white' and pieces_of_color[0] == 'K') or (color == 'black' and pieces_of_color[0] == 'k')):
            return True
        return False


def main():
    root = tk.Tk()
    AuthWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
