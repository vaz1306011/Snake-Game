import random
import tkinter as tk

FPS = 200
C = 17  # 寬
R = 15  # 高
block_size = 30
width = C*block_size
height = R*block_size

color_dic = {
    'h': "#4475EB",
    'b': "#4475EB",
    'a': "#E6471D",
}


def control(event):  # 鍵盤控制
    global direction
    x, y = snake_head
    x += direction[0]
    y += direction[1]
    if (direction == [1, 0] or direction == [-1, 0]) and event.keysym == 'Up':
        control_temp.append([0, -1])
        direction = [0, -1]
    elif (direction == [1, 0] or direction == [-1, 0]) and event.keysym == 'Down':
        control_temp.append([0, 1])
        direction = [0, 1]
    elif (direction == [0, -1] or direction == [0, 1]) and event.keysym == 'Left':
        control_temp.append([-1, 0])
        direction = [-1, 0]
    elif (direction == [0, -1] or direction == [0, 1]) and event.keysym == 'Right':
        control_temp.append([1, 0])
        direction = [1, 0]
    else:
        return


def create_apple():  # 隨機產生蘋果
    while True:
        x = random.randint(0, C-1)
        y = random.randint(0, R-1)
        if board[y][x] == '':
            board[y][x] = 'a'
            break


def draw_block(canvas, c, r, color=None):  # 繪製方格
    if color is None:
        color = "#A2D049" if (c+r) % 2 else "#A9D750"
    x1 = c*block_size
    y1 = r*block_size
    x2 = c*block_size+block_size
    y2 = r*block_size+block_size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)


def draw_eyes(canvas, c, r):  # 繪製方格
    if direction == [0, -1] or direction == [0, 1]:
        x1 = c*block_size+5
        y1 = r*block_size+10
        x2 = c*block_size+block_size-20
        y2 = r*block_size+block_size-10
        canvas.create_rectangle(
            x1, y1, x2, y2, fill="black", outline=color_dic['h'])
        canvas.create_rectangle(x1+15, y1, x2+15, y2,
                                fill="black", outline=color_dic['h'])
    else:
        x1 = c*block_size+10
        y1 = r*block_size+5
        x2 = c*block_size+block_size-10
        y2 = r*block_size+block_size-20
        canvas.create_rectangle(
            x1, y1, x2, y2, fill="black", outline=color_dic['h'])
        canvas.create_rectangle(x1, y1+15, x2, y2+15,
                                fill="black", outline=color_dic['h'])


def draw_board(canvas):  # 繪製畫板
    canvas.delete(tk.ALL)
    for i in range(R):
        for j in range(C):
            kind = board[i][j]
            if kind:
                draw_block(canvas, j, i, color_dic[kind])
                if kind == 'h':
                    draw_eyes(canvas, j, i)
            else:
                draw_block(canvas, j, i)


def game_init():  # 遊戲初始化
    global snake_win
    snake_win.title("貪食蛇")
    snake_win.resizable(0, 0)
    snake_win.geometry('+700+200')
    snake_win.config(bg="#568A35")
    snake_win.focus_force()

    global score_canvas
    score_canvas = tk.Canvas(snake_win, height=80, bg="#4a752c", bd=-2)
    score_canvas.pack(fill='x')

    global canvas
    canvas = tk.Canvas(snake_win, width=width, height=height, bd=-2)
    canvas.pack(padx=20, pady=20)

    global board
    board = [['' for i in range(C)] for j in range(R)]

    global snake_head
    snake_head = [3, 7]

    global snake_body
    snake_body = [[1, 7], [2, 7]]

    global score
    score = score_canvas.create_text(90, 40, text=0, font=(
        'Hobo std', 20), fill='white', justify='left')
    draw_block(score_canvas, 1, 0.8, color_dic['a'])

    create_apple()
    draw_board(canvas)

    global direction
    direction = [1, 0]

    global control_temp
    control_temp = []

    global loop
    loop = True

    snake_win.protocol('WM_DELETE_WINDOW', game_quit)
    canvas.bind_all("<Key-Left>", control)
    canvas.bind_all("<Key-Right>", control)
    canvas.bind_all("<Key-Up>", control)
    canvas.bind_all("<Key-Down>", control)


def game_loop():  # 遊戲迴圈
    global snake_win, loop
    if control_temp:
        move(control_temp[0])
        del control_temp[0]
    else:
        move(direction)
    if loop:
        loop = snake_win.after(FPS, game_loop)


def game_quit():
    global loop
    snake_win.after_cancel(loop)
    loop = None
    snake_win.quit()
    snake_win.destroy()


def move(way):
    global snake_head, snake_body, board
    x, y = snake_head
    x += way[0]  # 頭位移
    y += way[1]
    if x < 0 or x >= C or y < 0 or y >= R or board[y][x] == 'b':
        import tkinter.messagebox
        tkinter.messagebox.showinfo('遊戲結束', f'分數:{len(snake_body)-2}')
        game_quit()
        return
    snake_body.append(snake_head[:])  # 把頭加到身體裡面
    snake_head = [x, y]
    if board[y][x] != 'a':  # 如果頭走到的位置不是蘋果
        board[y][x] = 'h'  # 把頭放進畫板裡
        board[snake_body[0][1]][snake_body[0][0]] = ''  # 清空身體最後一格
        del snake_body[0]
    else:
        board[y][x] = 'h'
        create_apple()
        score_canvas.itemconfig(score, text=len(snake_body)-2)

    for xy in snake_body:
        x, y = xy
        board[y][x] = 'b'
    draw_board(canvas)
    if len(snake_body) == C*R:
        import tkinter.messagebox
        tkinter.messagebox.showinfo('遊戲結束', '遊戲通關')
        game_quit()
        return


def main():  # 主程式
    global snake_win
    snake_win = tk.Tk()
    game_init()
    game_loop()
    snake_win.mainloop()


if __name__ == "__main__":
    main()
