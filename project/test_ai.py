
# def build_board(width=10,height=10):
#     return [["{}{}".format(chr(j+65),i+1) for i in range(width)] for j in range(height)]

def build_image(width=10,height=10):
    return [[0]*width for i in range(height)]


def spaces(board, size, condition, new_board):
    board_len = len(board)
    board_zone = range(len(board))
    for y in board_zone:
        for x in board_zone:
            if x + (size-1) < board_len:
                if all(condition(board[y][inc]) for inc in range(x,x+size)):
                    for increment in range(size):
                        new_board[y][x+increment]+=1
            if y + (size-1) < board_len:
                if all(condition(board[inc][x]) for inc in range(y,y+size)):
                    for increment in range(size):
                        new_board[y+increment][x]+=1
    return new_board
def run_test():
    ships = [5,4,3,3,2]
    current_image = build_image()
    print(current_image)
    for boat in ships:
        spaces(current_image, boat, lambda item: True, current_image)
    return current_image

# Pass Coordinate to set to Zero And Updates Image of Board
def update_test(image, x, y):
    ships = [5,4,3,3,2]
    # current_image = build_image()
    # print(current_image)
    image[y][x] = 0
    update = build_image()
    for boat in ships:
        spaces(image, boat, lambda item: item != 0, update)
    return update

def make_tabel(image):
    size = len(image)
    temp = ""
    for idx in range(size):
        temp += "\n{}".format(idx)
        temp += ("|{}"*size).format(*image[idx])+"|"
    print(temp)

