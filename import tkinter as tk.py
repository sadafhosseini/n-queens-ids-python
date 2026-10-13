import tkinter as tk
from tkinter import simpledialog, messagebox


def get_board_size():
    root = tk.Tk()
    root.withdraw()

    while True:
        value = simpledialog.askstring(
            "N-Queens",
            "تعداد وزیرها / اندازه صفحه شطرنج را وارد کنید:"
        )

        if value is None:
            root.destroy()
            return None

        try:
            n = int(value)

            if n > 0:
                root.destroy()
                return n

            messagebox.showerror(
                "خطا",
                "عدد باید بزرگ‌تر از صفر باشد."
            )

        except ValueError:
            messagebox.showerror(
                "خطا",
                "لطفاً یک عدد صحیح وارد کنید."
            )


def get_initial_positions(n):
    root = tk.Tk()
    root.withdraw()

    value = simpledialog.askinteger(
        "وزیرهای ثابت",
        f"چند وزیر از قبل روی صفحه قرار دارند؟\nعددی بین 0 تا {n} وارد کنید:",
        minvalue=0,
        maxvalue=n
    )

    if value is None:
        root.destroy()
        return None

    positions = []
    used_rows = set()

    for i in range(value):
        while True:
            position = simpledialog.askstring(
                "موقعیت وزیر",
                f"موقعیت وزیر {i + 1} را به شکل row,col وارد کنید:\n"
                f"مثال: 0,2"
            )

            if position is None:
                root.destroy()
                return None

            try:
                row, col = map(int, position.split(","))

                if not (0 <= row < n and 0 <= col < n):
                    messagebox.showerror(
                        "خطا",
                        f"row و col باید بین 0 و {n - 1} باشند."
                    )
                    continue

                if row in used_rows:
                    messagebox.showerror(
                        "خطا",
                        "در هر سطر فقط یک وزیر می‌تواند قرار بگیرد."
                    )
                    continue

                positions.append((row, col))
                used_rows.add(row)
                break

            except ValueError:
                messagebox.showerror(
                    "خطا",
                    "موقعیت را به صورت row,col وارد کنید.\nمثال: 1,3"
                )

    root.destroy()
    return positions


def is_safe(board, row, col):
    for r in range(len(board)):
        if r == row or board[r] == -1:
            continue

        c = board[r]

        # همان ستون
        if c == col:
            return False

        # قطر
        if abs(c - col) == abs(r - row):
            return False

    return True


def depth_limited_search(board, row, n, limit, fixed_rows):
    if row == n:
        return True

    if row >= limit:
        return False

    # اگر این سطر از قبل وزیر ثابت دارد
    if row in fixed_rows:
        col = board[row]

        if not is_safe(board, row, col):
            return False

        return depth_limited_search(
            board,
            row + 1,
            n,
            limit,
            fixed_rows
        )

    # امتحان ستون‌های مختلف
    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col

            if depth_limited_search(
                board,
                row + 1,
                n,
                limit,
                fixed_rows
            ):
                return True

            board[row] = -1

    return False


def ids(n, initial_positions):
    fixed_positions = dict(initial_positions)
    fixed_rows = set(fixed_positions.keys())

    # افزایش تدریجی عمق
    for depth in range(1, n + 1):

        board = [-1] * n

        for row, col in fixed_positions.items():
            board[row] = col

        if depth_limited_search(
            board,
            0,
            n,
            depth,
            fixed_rows
        ):
            if all(col != -1 for col in board):
                return board

    return None


def board_to_text(board):
    text = ""

    for row in range(len(board)):
        for col in range(len(board)):
            if board[row] == col:
                text += "Q  "
            else:
                text += ".  "

        text += "\n"

    return text


def main():
    board_size = get_board_size()

    if board_size is None:
        return

    initial_positions = get_initial_positions(board_size)

    if initial_positions is None:
        return

    solution = ids(board_size, initial_positions)

    root = tk.Tk()
    root.withdraw()

    if solution:
        result = board_to_text(solution)

        print("Solution found:")
        print(result)

        messagebox.showinfo(
            "Solution Found",
            result
        )

    else:
        messagebox.showwarning(
            "No Solution",
            "برای این حالت راه‌حلی پیدا نشد."
        )

    root.destroy()


if __name__ == "__main__":
    main()
