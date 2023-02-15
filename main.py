from colorspy import *
import pygame
from sys import exit
from fighters import Fighter
from enemy import Enemy
pygame.init()

# Create game window
# screen_width = 1200
# screen_height = 640
screen_width = 1200
screen_height = 640
clock = pygame.time.Clock() # set frame rate

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Street Fighters")

# background music
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.45)
# pygame.mixer.music.play(-1, 0.0, 500)


# Load in background image
background = pygame.image.load('assets/background/bg_image.jpg').convert_alpha()
street_map = pygame.image.load('assets/background/map_2.jpg').convert_alpha()
main_menu = pygame.image.load('assets/background/mainmenu.webp').convert_alpha()

# load sprite sheets
martial_sheet = pygame.image.load('assets/images/warrior/Sprites/warrior.png').convert_alpha()
wizard_sheet = pygame.image.load('assets/images/wizard/Sprites/wizard.png').convert_alpha()

# idle, run, up, down, attack1, attack2, attack3
martial_animation_steps = [10, 8, 1, 7, 7, 3, 7]
wizard_animation_steps = [8, 8, 1, 8, 8, 3, 7]

warrior_scale = 4.5
warrior_size = 162
warrior_offset = [85, 45]
warrior_data = [warrior_size, warrior_scale, warrior_offset]

wizard_scale = 4
wizzard_size = 250
wizard_offset = [80, 105]
wizzard_data = [wizzard_size, wizard_scale, wizard_offset]
# Create instances of Fighter
fighter_1 = Fighter(200, 300, False, warrior_data, martial_sheet, martial_animation_steps)
enemy = Enemy(800, 310, wizzard_data, wizard_sheet, wizard_animation_steps, True)

street_fighter_font = pygame.font.Font('assets/fonts/sff.ttf', 30)
game_active = False
# function to draw health bars
def draw_health_bar(health,x, y):
    ratio = health / 100
    pygame.draw.rect(screen, white, (x - 1, y - 1, 402, 32))
    pygame.draw.rect(screen, red, (x, y, 400, 30))
    pygame.draw.rect(screen, lime_green, (x, y, 400 * ratio, 30))

    health_text = street_fighter_font.render(f'{health}', False, red)
    health_text_rect = health_text.get_rect(center = (x + 50, y + 18))
    screen.blit(health_text, health_text_rect)


# function to draw loading screen
game_name_font = pygame.font.Font('assets/fonts/turok.ttf', 100)
game_name = game_name_font.render('Pixel Fighters!', False, white_smoke)
game_name_rect = game_name.get_rect(center = (600, 50))

background_map = None
map_num = 0
check_start_menu = True
check_pause_menu = False

def start_menu(screen):
    global game_active, check_start_menu, background_map, map_num
    if not game_active and not check_pause_menu:
        screen.blit(main_menu, (0,0))
        map_1 = pygame.transform.scale(background, (320, 210))
        map_1_rect = map_1.get_rect(center = (420, 310))

        map_2 = pygame.transform.scale(street_map, (320, 210))
        map_2_rect = map_2.get_rect(center = (800, 310))
        screen.blit(map_1, map_1_rect)
        screen.blit(map_2, map_2_rect)
        screen.blit(game_name, game_name_rect)
        mouse_buttons = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if mouse_buttons[0]:
            if map_1_rect.collidepoint(pos):
                background_map =  pygame.image.load('assets/background/bg_image.jpg').convert_alpha()
                game_active = True
                check_start_menu = False
                map_num = 1
            elif map_2_rect.collidepoint(pos):
                background_map = pygame.image.load('assets/background/map_2.jpg').convert_alpha()
                game_active = True
                check_start_menu = False
                map_num = 2



resume_btn = pygame.image.load('Assets/buttons/button_resume.png')
resume_btn_rect = resume_btn.get_rect(center = (600, 180))

quit_btn = pygame.image.load('Assets/buttons/button_quit.png')
quit_btn_rect = quit_btn.get_rect(center = (600, 440))

options_btn = pygame.image.load('Assets/buttons/button_options.png')
options_btn_rect = options_btn.get_rect(center = (600, 310))
def pause_button(screen, player, target):
    global game_active, check_start_menu, check_pause_menu
    if not check_start_menu:
        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE] and not player.pause_btn:
            player.pause_btn = True
            target.pause_btn = True
            game_active = False
            screen.fill(cadet_blue)
            screen.blit(options_btn, options_btn_rect)
            screen.blit(quit_btn, quit_btn_rect)
            screen.blit(resume_btn, resume_btn_rect)
            check_pause_menu = True
        else:
            mouse_buttons = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            if mouse_buttons[0]:
                if resume_btn_rect.collidepoint(pos):
                    game_active = True
                    player.pause_btn = False
                    target.pause_btn = False
                elif quit_btn_rect.collidepoint(pos):
                    pygame.quit()
                    exit()


# Function to draw background image
def draw_background():
    if map_num == 1:
        screen.blit(background_map, (0, 0))
    else:
        screen.blit(background_map, (0, -60))
    # screen.blit(street_map, (0, -60))

def run():
    while True:
        clock.tick(60)
        start_menu(screen)
        # draw_loading_screen(screen, event_list)
        if game_active:
            # move fighters
            fighter_1.move(screen_width, screen_height, enemy)
            # fighter_2.move(screen_width, screen_height, screen, fighter_1)
            enemy.move(screen_width, screen_height, fighter_1)
            # enemy_group.draw(screen)
            # Draw all our elements
            # enemy.draw2(screen)
            draw_background()

            # draw statsa
            draw_health_bar(fighter_1.health, 30, 30)
            draw_health_bar(enemy.health, 770, 30)

            fighter_1.update()
            enemy.update()

            fighter_1.draw(screen)
            enemy.draw(screen)
            # update everything
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pause_button(screen, fighter_1, enemy)
        pygame.display.update()

run()



