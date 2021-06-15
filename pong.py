import pygame, sys, random
from pygame.locals import *


class Block(pygame.sprite.Sprite):
    def __init__(self,path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

class Player(Block):
    def __init__(self,path,x_pos,y_pos,speed):
        super().__init__(path,x_pos,y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self,ball_group):
        self.rect.y += self.movement
        self.screen_constrain()

# class Upgrades(Block):
#     def __init__(self):
#         self.position = random.randint(200, 1000)
#         self.color = (223, 163, 49)
#         self.randomize_position
    
#     def randomize_position(self):
#         self.position = (random.randint(200, grid_width-1) * gridsize, random.randint(200, grid_height-1) * gridsize)

#     def draw(self, screen):
#         r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
#         pygame.draw.rect(screen, self.color, r)
#         pygame.draw.rect(screen, (29, 216, 228), r, 1)

class Ball(Block):
    def __init__(self,path,x_pos,y_pos,move_x,move_y,paddles):
        super().__init__(path,x_pos,y_pos)
        self.move_x = move_x * random.choice((1,-1))
        self.move_y = move_y * random.choice((1,-1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.move_x
            self.rect.y += self.move_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(wall_sound)
            self.move_y *= -1

        if pygame.sprite.spritecollide(self,self.paddles,False):
            pygame.mixer.Sound.play(paddle_sound)
            collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.move_x > 0:
                self.move_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.move_x < 0:
                self.move_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.move_y < 0:
                self.rect.top = collision_paddle.bottom
                self.move_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.move_y < 0:
                self.rect.bottom = collision_paddle.top
                self.move_y *= -1
        
        # if pygame.sprite.spritecollide(self,self.paddles,False):
        #     pass

    def reset_ball(self):
        self.active = False
        self.move_x *= random.choice((1,-1))
        self.move_y *= random.choice((1,-1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2,screen_height/2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = basic_font.render(str(countdown_number),True,accent_color)
        time_counter_rect = time_counter.get_rect(center = (screen_width/2,screen_height/2 + 50))
        pygame.draw.rect(screen,bg_color,time_counter_rect)
        screen.blit(time_counter,time_counter_rect)

class Opponent(Block):
    def __init__(self,path,x_pos,y_pos,speed):
        super().__init__(path,x_pos,y_pos)
        self.speed = speed

    def update(self,ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

class GameManager:
    def __init__(self,ball_group,paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        # Draws the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updates the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = basic_font.render(str(self.player_score),True,accent_color)
        opponent_score = basic_font.render(str(self.opponent_score),True,accent_color)

        player_score_rect = player_score.get_rect(midleft = (screen_width/2 +40,30))
        opponent_score_rect = opponent_score.get_rect(midright = (screen_width/2 -40,30))

        screen.blit(player_score,player_score_rect)
        screen.blit(opponent_score,opponent_score_rect)

# def drawGrid(screen):
#     for y in range(0, int(grid_height)):
#         x in range(0, int(grid_width))

#General setup
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()

#Display Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong Evolved')

# gridsize = 20
# grid_width = (screen_height/2) / gridsize
# grid_height = (screen_width/2) / gridsize

# Global Variables
bg_color = pygame.Color('#2F373F')
accent_color = (27,35,43)
basic_font = pygame.font.Font("freesansbold.ttf", 34)
paddle_sound = pygame.mixer.Sound("paddle.wav")
wall_sound = pygame.mixer.Sound("wall.wav")
score_sound = pygame.mixer.Sound("score.wav")
middle_line = pygame.Rect(screen_width/2 - 2,0,4,screen_height)

# Game objects
player = Player('Paddle.png',screen_width - 20, screen_height/2,5)
opponent = Opponent('Paddle.png',20,screen_width/2,5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('Ball.png',screen_width/2,screen_height/2,4,4,paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite,paddle_group)

# Menu data
font = pygame.font.SysFont(None, 200)
button_font = pygame.font.SysFont(None, 60)
options_font = pygame.font.SysFont(None, 80)
click = False

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# background = pygame.image.load('pong.jpg')

# Displays Main Menu and leads to game, options, exit
def main_menu():
    while True:

        screen.fill((0,0,0))
        #Image
        # screen.blit(background, (0,0))
        draw_text('PONG', font, (255, 255, 255), screen, 440, 60)

        mx, my = pygame.mouse.get_pos()

        # pos(horizontal, vertical,  width, height)
        button_1 = pygame.Rect(520,300,250,90)
        button_2 = pygame.Rect(520,400,250,90)
        button_3 = pygame.Rect(520,500,250,90)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        rect1 = pygame.draw.rect(screen, (255,255,255), button_1)
        new_game_text = button_font.render("New Game", False, (0, 0, 0))
        new_game_rect = new_game_text.get_rect(center=rect1.center)
        screen.blit(new_game_text, new_game_rect)

        rect2 = pygame.draw.rect(screen, (255,255,255), button_2)
        options_text = button_font.render("Options", False, (0, 0, 0))
        options_rect = options_text.get_rect(center=rect2.center)
        screen.blit(options_text, options_rect)

        rect3 = pygame.draw.rect(screen, (255,255,255), button_3)
        exit_text = button_font.render("Exit", False, (0, 0, 0))
        exit_rect = exit_text.get_rect(center=rect3.center)
        screen.blit(exit_text, exit_rect)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(120)

# Options Menu
def options():
    running = True
    while running:
        screen.fill((0,0,0))
        draw_text('Options', options_font, (255, 255, 255), screen, 480, 20)
        draw_text('Difficulty', button_font, (255, 255, 255), screen, 30, 150)
        draw_text('Volume', button_font, (255, 255, 255), screen, 30, 380)
        draw_text('Opponent', button_font, (255, 255, 255), screen, 30, 600)

        mx, my = pygame.mouse.get_pos()

        # pos(horizontal, vertical,  width, height)
        diff_1 = pygame.Rect(150,260,200,70)
        diff_2 = pygame.Rect(450,260,200,70)
        diff_3 = pygame.Rect(750,260,200,70)
        diff_4 = pygame.Rect(1000,800,200,70)

        opp_1 = pygame.Rect(150,690,240,70)
        opp_2 = pygame.Rect(450,690,240,70)

        if diff_1.collidepoint((mx, my)):
            if click:
                pass
        if diff_2.collidepoint((mx, my)):
            if click:
                pass
        if diff_3.collidepoint((mx, my)):
            if click:
                pass
        if diff_4.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()


        rect1 = pygame.draw.rect(screen, (255,255,255), diff_1)
        easy_text = button_font.render("Easy", False, (0, 0, 0))
        easy_rect = easy_text.get_rect(center=rect1.center)
        screen.blit(easy_text, easy_rect)

        rect2 = pygame.draw.rect(screen, (255,255,255), diff_2)
        medium_text = button_font.render("Medium", False, (0, 0, 0))
        medium_rect = medium_text.get_rect(center=rect2.center)
        screen.blit(medium_text, medium_rect)

        rect3 = pygame.draw.rect(screen, (255,255,255), diff_3)
        hard_text = button_font.render("Hard", False, (0, 0, 0))
        hard_rect = hard_text.get_rect(center=rect3.center)
        screen.blit(hard_text, hard_rect)

        rect4 = pygame.draw.rect(screen, (255,255,255), diff_4)
        exit_text = button_font.render("Exit", False, (0, 0, 0))
        exit_rect = exit_text.get_rect(center=rect4.center)
        screen.blit(exit_text, exit_rect)

        rect5 = pygame.draw.rect(screen, (255,255,255), opp_1)
        opp1_text = button_font.render("AI", False, (0, 0, 0))
        opp1_rect = opp1_text.get_rect(center=opp_1.center)
        screen.blit(opp1_text, opp1_rect)

        rect6 = pygame.draw.rect(screen, (255,255,255), opp_2)
        opp2_text = button_font.render("Player 2", False, (0, 0, 0))
        opp2_rect = opp2_text.get_rect(center=opp_2.center)
        screen.blit(opp2_text, opp2_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(120)

# Difficulty
def difficulty():
    while True:
        pass


# Game itself
def game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # this input now allows the player1 rect to move up and down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.movement += player.speed
                if event.key == pygame.K_UP:
                    player.movement -= player.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.movement -= player.speed
                if event.key == pygame.K_UP:
                    player.movement += player.speed
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # Background 
        screen.fill(bg_color)
        pygame.draw.rect(screen, accent_color, middle_line)

        # Run the Game
        game_manager.run_game()

        # Rendering
        pygame.display.flip()
        clock.tick(120)

main_menu()