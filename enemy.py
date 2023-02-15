import pygame
from colorspy import *
import random

class Enemy:
    def __init__(self, x, y, data, sprite_sheet, animation_steps, flip):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]

        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(x, y, 80, 260)

        self.hit = False

        self.alive = True
        self.health = 100
        self.update_time = 0
        self.flip = flip

        self.jump = False
        self.running = False
        self.attacking = False
        self.attack_cooldown = 0

        self.magic_fx = pygame.mixer.Sound('Assets/audio/magic.wav')
        self.magic_fx.set_volume(0.25)
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

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.attacking:
            self.update_action(3)
        elif self.running:
            self.update_action(1)
        elif self.hit:
            self.update_action(5)
        else:
            self.update_action(0)  # idle
        animation_cooldown = 50

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.hit = False
            self.attacking = False

            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1

    def move(self, screen_width, screen_height, target):
        if not self.pause_btn:
            if self.alive:
                speed = 1
                # change in x and y coordinates
                dx = 0
                dy = 0
                # self.attack(target)
                self.running = False
                self.attack(target)
                # if target is not nearby, move on its own


                if self.attack_cooldown <= 10:
                    if self.rect.centerx < target.rect.centerx:
                        dx += speed
                        self.running = True
                    else:
                        dx -= speed
                        self.running = True

                self.rect.y += dy
                self.rect.x += dx

                if target.rect.centerx > self.rect.centerx:
                    self.flip = False
                else:
                    self.flip = True

                    if self.attack_cooldown > 0:
                        self.attack_cooldown -= 1

                # check if player on screen
                if self.rect.left + dx < 0:
                    dx = -self.rect.left
                if self.rect.right + dx > screen_width:
                    dx = screen_width - self.rect.right



    def attack(self, target):
        # print('here')
        attacking_rect = pygame.Rect(self.rect.centerx - (2.2 * self.rect.width * self.flip), self.rect.y,
                                     2.2 * self.rect.width, self.rect.height)
        # pygame.draw.rect(surface, blue, attacking_rect)

        if self.attack_cooldown <= 0:
            if attacking_rect.colliderect(target.rect):
                self.magic_fx.play()
                self.attacking = True
                target.health -= 5
                target.hit = True
                self.attack_cooldown = 60

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (
        self.rect.x - (self.offset[0] * self.image_scale) - 180, self.rect.y - (self.offset[1] * self.image_scale)))

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
