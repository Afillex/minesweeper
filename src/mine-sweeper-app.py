game_on = True
bombs = []

def minesweeper():
    import pygame,time,random
    pygame.init()
    running = True
    screen = pygame.display.set_mode((760,760))
    pygame.display.set_caption("MineSweeper")
    my_font = pygame.font.SysFont('Gill Sans', 30)
    game_over_ = pygame.font.SysFont('Gill Sans', 150)
    rects = []
    map_ = 16
    bom_num = 20
    #Functions

    def _restart(bom_num):
        global game_on,bombs

        game_on = True
        for i in rects:
            i[7] = i[6] = i[5] = i[4] = i[3] = 0
            i[2] = (255,255,255)
        bombs = []
        make_bomb(bom_num)
        check_bombs()

    def cr_grid(map_):
        for x in range(map_):
            for y in range(map_):
                col = (255,255,255)
                h = map_*2.5
                new_rect = pygame.Rect(h,h,h,h)
                new_rect.x,new_rect.y = x*map_*3,y*map_*3
                if len(rects) < map_**2:
                    rects.append([new_rect,(x,y),col,0,0,0,0,0])#Rect,coord,color,isbomb,near_bombs,is_clicked,is_checked,flagged

    def draw():
        for i in rects:
            if i[7]:
                pygame.draw.rect(screen, (75, 245, 66), i[0])
            else:
                pygame.draw.rect(screen, i[2], i[0])


    def check_collision():
        global game_on
        mouse_pos = pygame.mouse.get_pos()
        for i in rects:
            if mouse_pos == (0,0):
                pass
            elif i[0].collidepoint(mouse_pos) and not i[5]:
                i[2] = (125,125,125)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        i[7] = not i[7]
                        time.sleep(0.240)
                    if not i[3] and event.button == 1 and not i[7]:
                        i[5] = 1
                    else:
                        if event.button == 1 and not i[7]:
                            game_over = game_over_.render('BOOM!', False, (0,0,0))
                            game_on = False
                            screen.blit(game_over, (150,280))
                            pygame.display.update()

            else:
                if not i[5]:
                    i[2] = (255,255,255)

    def make_bomb(bom_num):
        rand_list = []
        while len(set(rand_list)) < bom_num:
            rand_list.append(random.randint(0,len(rects)-1))
        for i in set(rand_list):
            rects[i][3] = 1
            bombs.append(rects[i][1])

    def check_bombs():
        for i in rects:
            if not i[3]:
                x,y = i[1][0],i[1][1]
                for j in bombs:
                    for x_i in [-1,0,1]:
                        for y_i in [-1,0,1]:
                            if j == (x+x_i,y+y_i):
                                i[4] += 1

    def recursive_offset(rect,map_):
        if not rect[4] and not rect[6]:
            x,y = rect[1][0],rect[1][1]
            rect[2] = (176, 0, 169)
            rect[6] = 1
            rect[5] = 1
            if x != 0 and y != 0 and x != map_-1 and y != map_-1:
                for x_,y_ in [(1,0),(0,1),(-1,0),(0,-1)]:
                    if (map_*(x+x_) + y+y_) <= map_**2-1:
                        recursive_offset(rects[map_ * (x + x_) + y + y_],map_)
            elif x == 0 and y == 0:
                for x_, y_ in [(1, 0), (0, 1)]:
                    if (map_ * (x + x_) + y + y_) <= map_**2-1:
                        recursive_offset(rects[map_ * (x + x_) + y + y_],map_)
            elif x == map_-1 and y == map_-1:
                for x_, y_ in [(-1, 0),(0, -1)]:
                    if (map_ * (x + x_) + y + y_) <= map_**2-1:
                        recursive_offset(rects[map_ * (x + x_) + y + y_],map_)
            elif x == map_-1 and y == 0:
                for x_, y_ in [(-1, 0), (0, 1)]:
                    if (map_ * (x + x_) + y + y_) <= map_**2-1:
                        recursive_offset(rects[map_ * (x + x_) + y + y_],map_)
            elif x == 0 and y == map_-1:
                for x_, y_ in [(1, 0), (0, -1)]:
                    if (map_ * (x + x_) + y + y_) <= map_**2-1:
                        recursive_offset(rects[map_ * (x + x_) + y + y_],map_)
            elif x == 0:
                for x_,y_ in [(1,0),(0,1),(0,-1)]:
                    if (map_ * (x + x_) + y + y_) <= map_**2-1:
                        recursive_offset(rects[map_ * (x + x_) + y + y_],map_)
            elif y == 0:
                for x_,y_ in [(1,0),(-1,0),(0,1)]:
                    if (map_ * (x + x_) + y + y_) <= map_**2-1:
                        recursive_offset(rects[map_ * (x + x_) + y + y_],map_)
            elif x == map_-1:
                for x_,y_ in [(0,1),(-1,0),(0,-1)]:
                    if (map_ * (x + x_) + y + y_) <= map_**2-1:
                        recursive_offset(rects[map_ * (x + x_) + y + y_],map_)
            elif y == map_-1:
                for x_,y_ in [(1,0),(-1,0),(0,-1)]:
                    if (map_ * (x + x_) + y + y_) <= map_**2-1:
                        recursive_offset(rects[map_ * (x + x_) + y + y_],map_)
        else:
            rect[5] = 1
            rect[7] = 0
    def write_numbers():
        for i in rects:
            if i[5]:
                if i[4]:
                    screen.blit(my_font.render(f"{i[4]}", False, (0, 0, 0)), (i[0].x + 8, i[0].y - 2))
                    i[2] = (255, 206, 0)
                else:
                    if not i[6]:
                        recursive_offset(i,map_)
    #Game Loop
    cr_grid(map_)
    make_bomb(bom_num)
    check_bombs()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key = pygame.key.get_pressed()

        screen.fill("dark grey")
        draw()
        check_collision()
        write_numbers()

        if game_on:
            pygame.display.update()
        else:
            for j in bombs:
                rects[map_ * j[0] + j[1]][2] = (255, 0, 0)

        if key[pygame.K_r]:
            _restart(bom_num)

        #For CPU efficiency
        time.sleep(0.01)
minesweeper()