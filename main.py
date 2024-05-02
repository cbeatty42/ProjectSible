from Gui import *

def main():
    colors = NIGHT_MODE_COLORS
    win = pygame.display.set_mode((0, 0),pygame.RESIZABLE)
    pygame.display.set_caption("Project Sible")
    difficulty = 3
    board = Grid(win,9, 9, 540, 540, True, difficulty)
    key = None
    run = True

    night_mode = True
    offset = board.get_time()
    start = time.time()

    while run:

        board.set_time(round(offset + time.time() - start))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_BACKSPACE:
                    if board.selected:
                        row,column=board.selected
                        board.reset_cube(row, column)
                        key = 0
                if event.key == pygame.K_DELETE:
                    if board.selected:
                        row,column=board.selected
                        board.reset_cube(row,column)
                        key = 0
                if event.key == pygame.K_RETURN: #if Enter is pressed
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        board.place(board.cubes[i][j].temp)
                        key = None

                    '''   
                    if board.is_finished():
                            print("Game over")
                            run = False
                            display_game_over(win, colors)
                            time.sleep(3) # Pause for 3 seconds before closing the window
                    '''
                #use n key to set night mode
                if event.key == pygame.K_n:
                    night_mode = toggle_night_mode(win, board, night_mode)
                    if night_mode:
                        colors = NIGHT_MODE_COLORS
                    else:
                        colors = DAY_MODE_COLORS
                    redraw_window(win, board, colors)
                #use r key to reset board and time.
                if event.key == pygame.K_r and (event.mod & pygame.KMOD_CTRL):
                    board.reset()
                    key = None
                    start = time.time()
                #various keys are used to set the difficulty
                if event.key == pygame.K_h and (event.mod & pygame.KMOD_CTRL):
                    difficulty = 2 #Hard difficulty
                    offset = 0
                    start = time.time()
                    board.set_time(0)
                    board = Grid(win,9, 9, 540, 540, False, difficulty, board.get_bestTime())
                    key = None
                if event.key == pygame.K_m and (event.mod & pygame.KMOD_CTRL):
                    difficulty = 3 #Medium difficulty
                    offset = 0
                    start = time.time()
                    board.set_time(0)
                    board = Grid(win,9, 9, 540, 540, False, difficulty, board.get_bestTime())
                    key = None
                if event.key == pygame.K_e and (event.mod & pygame.KMOD_CTRL):
                    difficulty = 4 #Easy
                    offset = 0
                    start = time.time()
                    board.set_time(0)
                    board = Grid(win,9, 9, 540, 540, False, difficulty, board.get_bestTime())
                    key = None
                if event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                    difficulty = 5 #Very Easy
                    offset = 0
                    start = time.time()
                    board.set_time(0)
                    board = Grid(win,9, 9, 540, 540, False, difficulty, board.get_bestTime())
                    key = None
                if event.key == pygame.K_c and (event.mod & pygame.KMOD_CTRL):
                    #C+CTRL verifies you have a correct board
                    isTheBoardSolved = board.is_solved()
                    isTheBoardFilled = board.is_finished()
                    if isTheBoardSolved:
                        if board.get_time() < board.get_bestTime() or board.get_bestTime() == -1:
                            board.set_bestTime(board.get_time())
                            print("Check: Game over & new best time")
                            message="Congratulations! New Best Time: "+ str(board.get_bestTime)
                        else:
                            print("Check: Game over")
                            message="Congratulations! You won another puzzle!"
                        board = Grid(win,9, 9, 540, 540, False, difficulty, board.get_bestTime())
                    if not isTheBoardFilled:
                        print("Check: Board not filled ")
                        message="Board not filled"
                    if isTheBoardFilled and not isTheBoardSolved:
                        print("Check: Board filled, but not solved")
                        message="Board filled, but puzzle not solved"
                    display_message(win, colors, message)
                    time.sleep(3)
                    
                #arrow keys used to move around
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if board.selected:
                        row, col = board.selected
                        key = None
                        if col > 0:
                            board.select(row, col - 1)
                    else:
                        board.select(4,3)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if board.selected:
                        row, col = board.selected
                        key = None
                        if col < 8:
                            board.select(row, col + 1)
                    else:
                        board.select(4,5)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if board.selected:
                        row, col = board.selected
                        key = None
                        if row > 0:
                            board.select(row - 1, col)
                    else:
                        board.select(3,4)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if board.selected:
                        row, col = board.selected
                        key = None
                        if row < 8:
                            board.select(row + 1, col)
                    else:
                        board.select(5,4)
                #use esc key to force quit game
                if event.key == pygame.K_ESCAPE:
                    run = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)

                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key is not None:
            board.sketch(key)
  

        redraw_window(win, board, colors)

        pygame.display.update()

    save("board.json", board.board, board.backupBoard, board.get_bestTime(), board.get_time())

main()
pygame.quit()
