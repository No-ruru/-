import asyncio    #これが必須の奴
import pygame, sys, copy
pygame.init()
screen = pygame.display.set_mode((900, 800))
clock = pygame.time.Clock()
font = pygame.font.SysFont('', 32)

#マスの色の設定
white = (255,255,255)
black = (0,0,0)
gray = (192,192,192)
square_color = [white, black, gray]#白,黒,灰色

p_b = pygame.image.load("piece_black2.png")
p_w = pygame.image.load("piece_white2.png")
p_b_re = pygame.image.load("piece_black2_re.png")
p_w_re = pygame.image.load("piece_white2_re.png")

player1_img = [p_w_re, p_b_re]
player2_img = [p_w, p_b]

square_size, space = 112, 3#マスの一辺、マスとマスの間隔

#丸角の四角形を描画
async def panel(screen, color, x, y, size, rate=1/38):
    r = int(size * rate)
    #円の描画
    for i in range(2):
        for j in range(2):
            pygame.draw.circle(screen, color, (x+r+(size-r*2)*j, y+r+(size-r*2)*i), r)
    #長方形の描画
    pygame.draw.rect(screen, color, (x, y+r, r, size-r*2))
    pygame.draw.rect(screen, color, (x+r, y, size-r*2, size))
    pygame.draw.rect(screen, color, (x+r+size-r*2, y+r, r, size-r*2))


async def main():    #これが必須の奴
  
  #盤面の初期値
  board_color = [[0 for _ in range(5)] for _ in range(5)] #各マスの色
  board_x, board_y = 199, 74#canvasに対する盤の左上の座標

  #駒の初期位置
  player1_piece = [[4,0], [4,1], [4,2], [4,3], [4,4]]
  player2_piece = [[0,0], [0,1], [0,2], [0,3], [0,4]]
  piece_position = [[0 for _ in range(5) ]for _ in range(5)]
  #初期の手持ちのパネル
  player1_panel = [1,1,1,2]
  player2_panel = [1,1,1,2]

  player_piece = [player1_piece, player2_piece]
  player_panel = [player1_panel, player2_panel]

  board_xy = [[x,y] for x in range(5) for y in range(5)]
  #選択中の駒
  select_pre = [-1,-1]
  select_piece = [-1,-1]

  #マウスの位置
  mouse_x,mouse_y = -1,-1   

  #何か選択しているか
  select = False  

  while True:
      screen.fill(white)
      
      tap = False
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
          
          if event.type == pygame.MOUSEBUTTONDOWN:
              mouse_x, mouse_y = event.pos #マウスの位置を取得
              tap = True

      panel_xy = [] #タップした時のパネルの選択肢
      for i in range(2):
            for j in range(4):
                if player_panel[i][j] != 0: panel_xy.append([5+i, j])
      piece_xy = player1_piece + player2_piece #タップした時のコマの選択肢
    
      

      if tap:#画面をタップした時の盤面におけるマスの座標、手持ちのパネルの座標
            #player1の持ちパネル
            if board_x+615 <= mouse_x and mouse_x <= board_x+615+square_size and board_y+180 <= mouse_y and mouse_y <= board_y+180+square_size*4+space*3:
                mouse_x = 5
                mouse_y = (mouse_y-(board_y+179)) // (square_size + 3)
            #player2の持ちパネル
            elif board_x-15-square_size <= mouse_x and mouse_x <= board_x-15 and board_y-37 <= mouse_y and mouse_y <= board_y-37+square_size*4+space*3:
                mouse_x = 6
                mouse_y = 3 - (mouse_y-(board_y-37))//(square_size + 3)
            elif mouse_x < board_x+10 or board_x+600-10 < mouse_x or mouse_y < board_y+10 or board_y+600-10 < mouse_y: 
                mouse_x, mouse_y = -1, -1
            #盤上のマス
            else:
                mouse_x = (mouse_x - board_x-10) // (580//5)
                mouse_y = (mouse_y - board_y-10) // (580//5)

            if [mouse_x, mouse_y] in piece_xy + panel_xy: 
                select = True
                select_pre = copy.deepcopy([mouse_x, mouse_y])

            elif  [mouse_x, mouse_y] in board_xy and not [mouse_x, mouse_y] in piece_xy and select: 
                select = False
                select_piece = copy.deepcopy([mouse_x, mouse_y])
            
            else :
                select = False
                select_pre = [-1,-1]

      #パネルを選択中のときにタップしたら
      if tap and not select and select_pre[0] in [5, 6] and player_panel[(6-select_pre[0]+1)%2][select_pre[1]] != 0:
            if select_pre[0] == 5:
                board_color[select_piece[1]][select_piece[0]] = player_panel[0][select_pre[1]]
                player_panel[0][select_pre[1]] = 0
            elif select_pre[0] == 6:
                board_color[select_piece[1]][select_piece[0]] = player_panel[1][select_pre[1]]
                player_panel[1][select_pre[1]] = 0
            select_pre = [-1,-1]
            select_piece = [-1,-1]

      #コマを選択しているときにタップしたら
      elif tap and not select and select_piece in board_xy and not select_piece in piece_xy + panel_xy:

            if select_pre in player1_piece: 
                player_piece[0].remove(select_pre)
                player_piece[0].append(select_piece) 
            elif select_pre in player2_piece: 
                player_piece[1].remove(select_pre)
                player_piece[1].append(select_piece) 

            select_pre = [-1,-1]
            select_piece = [-1,-1]




      #検証用
      text = font.render(f'{mouse_x}', True, (0, 0, 255))
      if tap :screen.blit(text, (0, 0))
      ##


      #盤が中央になるように再設定
      w, h = pygame.display.get_surface().get_size()
      board_x = (w - 600) // 2
      board_y = (h - 600) // 2

      panel_xy = [] #タップした時のパネルの選択肢
      for i in range(2):
            for j in range(4):
                if player_panel[i][j] != 0: panel_xy.append([5+i, j])

      piece_xy = player1_piece + player2_piece #タップした時のコマの選択肢


      #盤を描画
      await panel(screen, (205,205,205), board_x, board_y, 600)
      for i in range(1,6):
        for j in range(1,6):
            square_x = board_x+11+space*j+square_size*(j-1)
            square_y = board_y+11+space*i+square_size*(i-1)
            await panel(screen, square_color[board_color[i-1][j-1]], square_x, square_y, square_size)

      for i in range(5):
            #player1
            img = player1_img[0]
            piece_x = player1_piece[i][0]
            piece_y = player1_piece[i][1]
            if board_color[piece_y][piece_x] == 1: img = player1_img[1]
            screen.blit(img, (board_x+11+space*(piece_x+1)+square_size*piece_x, board_y+11+space*(piece_y+1)+square_size*piece_y))
            #player2
            img = player2_img[0]
            piece_x = player2_piece[i][0]
            piece_y = player2_piece[i][1]
            if board_color[piece_y][piece_x] == 1: img = player2_img[1]
            screen.blit(img, (board_x+11+space*(piece_x+1)+square_size*piece_x, board_y+11+space*(piece_y+1)+square_size*piece_y))
    
      #手持ちのパネルを表示する
      for i in range(4):
            #player1
            panel_x = board_x+600+15
            panel_y = board_y+180+space*i+square_size*i
            await panel(screen, square_color[player1_panel[i]], panel_x, panel_y, square_size)
            #player2
            panel_x = board_x-15-square_size
            panel_y = board_y-37+space*i+square_size*i
            await panel(screen, square_color[player2_panel[3-i]], panel_x, panel_y, square_size)
        
      pygame.display.update()
      clock.tick(30)
      await asyncio.sleep(0)    #これが必須の奴

asyncio.run(main())    #これが必須の奴