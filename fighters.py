import pygame
from colorspy import *


class Fighter:
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.rect = pygame.Rect(x, y, 80, 260)
        self.velocity_y = -10

        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]

        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]

        self.attack_type = 0
        self.attacking = False
        self.hit = False

        self.running = False
        self.jump = False

        self.health = 100
        self.flip = flip
        self.update_time = pygame.time.get_ticks()
        self.attack_cooldown = 0

        self.alive = True
        self.sword_fx = pygame.mixer.Sound('assets/audio/sword.wav')
        self.sword_fx.set_volume(0.25)

        self.pause_btn = False

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img = pygame.transform.scale(temp_img,
                                                  (self.size * self.image_scale + 80, self.size * self.image_scale))
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, target):

        if not self.pause_btn:
            speed = 10
            gravity = 2
            # change in x and y coordinates
            dx = 0
            dy = 0
            # get presses
            self.running = False
            self.attack_type = 0

            key = pygame.key.get_pressed()

            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            # check if player is not attack
            if not self.attacking and target.health > 0:
                if key[pygame.K_a]:
                    dx -= speed
                    self.flip = True
                    self.running = True
                if key[pygame.K_d]:
                    dx += speed
                    self.running = True

                if key[pygame.K_SPACE] and not self.jump:
                    self.velocity_y -= 30
                    self.jump = True

                if key[pygame.K_f] or key[pygame.K_e]:
                    # determine attack type
                    if key[pygame.K_f]:
                        self.attack_type = 1
                    elif key[pygame.K_e]:
                        self.attack_type = 2
                    self.attack(target)

            # apply gravity
            self.velocity_y += gravity
            dy += self.velocity_y

            # check if player on screen
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
            if self.rect.bottom + dy > screen_height - 90:
                self.velocity_y = 0
                self.jump = False
                dy = screen_height - self.rect.bottom - 90

            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            # update player pos
            self.rect.x += dx
            self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        if self.hit:
            self.update_action(5)
        elif self.attacking:
            self.sword_fx.play()
            if self.attack_type == 1:  # attack 1
                self.update_action(3)
            elif self.attack_type == 2:  # attack 2
                self.update_action(4)
        elif self.running:
            self.update_action(1)  # running
        else:
            self.update_action(0)  # idle

        animation_cooldown = 50

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1

            if self.action == 3 or self.action == 4:
                self.attacking = False
                self.attack_cooldown = 20

            # check if damage was taken
            if self.action == 5:
                self.hit = False
                self.attacking = False
                self.attack_cooldown = 20

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (
        self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2.2 * self.rect.width * self.flip), self.rect.y,
                                         2.2 * self.rect.width, self.rect.height)

            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
