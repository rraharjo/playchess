
def idxToChessNotation(idx: int) -> str:
    if idx < 0 or idx >= 64:
        raise ValueError("Invalid Position")
    row: int = idx // 8
    col: int = idx % 8
    colLetter: str = chr(ord('a') + col)
    return f"{colLetter}{row + 1}"
def chessNotationToIdx(notation: str) -> int:
    if (len(notation) != 2 or notation[0] < 'a' or notation[0] > 'h' or notation[1] < '1' or notation[1] > '8'):
        raise ValueError("Invalid Position")
    col: int = ord(notation[0]) - ord('a')
    row: int = int(notation[1]) - 1
    return row * 8 + col