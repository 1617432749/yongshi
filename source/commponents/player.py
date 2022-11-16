import pygame
from .. import tools, setup
from .. import consatants as C
import json
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()
        self.life = 10

    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

    def setup_states(self):
        self.state = 'stand'
        self.face_right = True
        self.dead = False
        self.big = False
        self.can_jump = False
        self.can_attck = False
        self.hurt_immune = False
        self.Bstand = True
        self.Run = False
        self.Jump = False
        self.wattack = False
        self.bian = False
        self.skill = False

    def setup_velocities(self):
        speed = self.player_data['speed']
        self.x_vel = 0
        self.y_vel = 0

        self.max_walk_vel = speed['max_walk_speed']
        self.max_run_vel = speed['max_run_speed']
        self.max_y_vel = speed['max_y_velocity']
        self.jump_vel = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.run_accel = speed['run_accel']
        self.turn_accel = speed['turn_accel']
        self.gravity = C.GRAVITY
        self.anti_garavit = C.ANTI_GRAVITY

        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel

    def setup_timers(self):
        self.walking_timer = 0
        self.transitio_timer = 0
        self.death_timer = 0
        self.hurt_immune_timer = 0
        self.attack_timer = 0
        self.stand_timer = 0
        self.bianshen_timer = 0

    def load_images(self):
        sheet = setup.GRAPHICS['mario_bros']
        frame_rects = self.player_data['image_frames']

        self.right_small_normal_frames = []
        self.right_big_normal_frames = []
        self.left_small_normal_frames = []
        self.left_big_normal_frames = []
        self.big_rstand = []
        self.big_lstand = []
        self.run_r = []
        self.run_l = []
        self.Jump_r = []
        self.Jump_l = []
        self.rattack_frames = []
        self.lattack_frames = []
        self.bianshen_r = []
        self.bianshen_l = []

        self.small_normal_frames = [self.right_small_normal_frames, self.left_small_normal_frames]
        self.big_normal_frames = [self.right_big_normal_frames, self.left_big_normal_frames]
        self.big_stand = [self.big_rstand, self.big_lstand]
        self.run = [self.run_r, self.run_l]
        self.JUmp = [self.Jump_r, self.Jump_l]
        self.attack_frame = [self.rattack_frames, self.lattack_frames]
        self.bianshen = [self.bianshen_r, self.bianshen_l]

        self.all_frames = [
            self.right_small_normal_frames,
            self.right_big_normal_frames,
            self.left_small_normal_frames,
            self.left_big_normal_frames,
            self.rattack_frames,
            self.lattack_frames,
            self.big_rstand,
            self.big_lstand,
            self.run_r,
            self.run_l,
            self.Jump_r,
            self.Jump_l,
            self.bianshen_r,
            self.bianshen_l
        ]

        self.right_frames = self.right_small_normal_frames
        self.left_frames = self.left_small_normal_frames
        self.attackr_frames = self.rattack_frames
        self.attackl_frames = self.lattack_frames
        self.big_rstand_frames = self.big_rstand
        self.big_lstand_frames = self.big_lstand
        self.run_r_frames = self.run_r
        self.run_l_frames = self.run_l
        self.bianshen_l_frames = self.bianshen_r
        self.bianshen_r_frames = self.bianshen_r

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                              frame_rect['width'], frame_rect['height'], (0, 0, 0), 1)
                left_image = pygame.transform.flip(right_image, True, False)
                stand_image_r = tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                              frame_rect['width'], frame_rect['height'], (0, 0, 0), 1)
                stand_image_l = pygame.transform.flip(stand_image_r, True, False)
                run_r = tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                              frame_rect['width'], frame_rect['height'], (0, 0, 0), 1)
                run_l = pygame.transform.flip(run_r, True, False)
                jump_r = tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                              frame_rect['width'], frame_rect['height'], (0, 0, 0), 1)
                jump_l = pygame.transform.flip(jump_r, True, False)
                attackr_image = tools.get_image(sheet,frame_rect['x'], frame_rect['y'],
                                              frame_rect['width'], frame_rect['height'], (0, 0, 0), 1)
                attackl_image = pygame.transform.flip(jump_r, True, False)
                bianshen_r_image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                                frame_rect['width'], frame_rect['height'], (0, 0, 0), 1)
                bianshen_l_image = pygame.transform.flip(bianshen_r_image, True, False)
                if group == 'right_small_normal':
                    self.right_small_normal_frames.append(right_image)
                    self.left_small_normal_frames.append(left_image)
                if group == 'big_stand':
                    self.big_rstand.append(stand_image_r)
                    self.big_lstand.append(stand_image_l)
                if group == 'attack':
                    self.rattack_frames.append(attackr_image)
                    self.lattack_frames.append(attackl_image)
                if group == 'right_big_normal':
                    self.right_big_normal_frames.append(right_image)
                    self.left_big_normal_frames.append(left_image)
                if group == 'run':
                    self.run_r.append(run_r)
                    self.run_l.append(run_l)
                if group == 'jump':
                    self.Jump_r.append(jump_r)
                    self.Jump_l.append(jump_l)
                if group == 'skill':
                    self.bianshen_r.append(bianshen_r_image)
                    self.bianshen_l.append(bianshen_l_image)

        self.frame_index = 0
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self, keys):
        self.current_time = pygame.time.get_ticks()
        self.handle_states(keys)
        self.is_hurt_immune()

    def handle_states(self, keys):
        last_frame_bottom = self.rect.bottom
        last_frame_centerx = self.rect.centerx

        self.can_jump_or_not(keys)
        self.attack_allow(keys)

        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == C.MARIO_DEAD:
            self.die(keys)
        elif self.state == C.ATTACK:
            self.attack(keys)
        elif self.state == 'small2big':
            self.small2big(keys)
        elif self.state == 'big2small':
            self.big2small(keys)
        elif self.state == 'kk':
            self.kk(keys)

        if self.big == False:
            if self.face_right:
                self.image = self.right_frames[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.bottom = last_frame_bottom
                self.rect.centerx = last_frame_centerx
            else:
                self.image = self.left_frames[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.bottom = last_frame_bottom
                self.rect.centerx = last_frame_centerx
        else:
            if self.Bstand == True:
                if self.face_right:
                    self.image = self.big_rstand_frames[self.frame_index]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = last_frame_bottom
                    self.rect.centerx = last_frame_centerx
                else:
                    self.image = self.big_lstand_frames[self.frame_index]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = last_frame_bottom
                    self.rect.centerx = last_frame_centerx
            elif self.Run == True:
                if self.face_right and self.frame_index < 5:
                    self.image = self.run_r[self.frame_index]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = last_frame_bottom
                    self.rect.centerx = last_frame_centerx
                elif self.face_right == False and self.frame_index < 5:
                    self.image = self.run_l[self.frame_index]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = last_frame_bottom
                    self.rect.centerx = last_frame_centerx
            elif self.Jump == True:
                if self.face_right and self.frame_index < 9:
                    self.image = self.Jump_r[self.frame_index]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = last_frame_bottom
                    self.rect.centerx = last_frame_centerx
                elif self.face_right == False and self.frame_index < 9:
                    self.image = self.Jump_l[self.frame_index]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = last_frame_bottom
                    self.rect.centerx = last_frame_centerx
            elif self.wattack == True:
                if self.face_right and self.frame_index < 8:
                    self.image = self.rattack_frames [self.frame_index]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = last_frame_bottom
                    self.rect.centerx = last_frame_centerx
                elif self.face_right == False and self.frame_index < 8:
                    self.image = self.lattack_frames[self.frame_index]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = last_frame_bottom
                    self.rect.centerx = last_frame_centerx
            elif self.skill == True and self.big == True:
                if self.face_right and self.frame_index < 6:
                    self.image = self.bianshen_r_frames[self.frame_index]
                elif self.face_right == False and self.frame_index < 9:
                    self.image = self.bianshen_l_frames[self.frame_index]
    def can_jump_or_not(self, keys):
        if not keys[pygame.K_k]:
            self.can_jump = True

    def attack_allow(self, keys):
        if not keys[pygame.K_j]:
            self.can_attck = True

    def stand(self, keys):
        if self.big == False:
            self.frame_index = 0
        else:
            if self.current_time - self.stand_timer > 100:
                if self.frame_index < 9:
                    self.frame_index += 1
                else:
                    self.frame_index = 0
                self.stand_timer = self.current_time
        self.x_vel = 0
        self.y_vel = 0
        self.Bstand = True
        self.Run = False
        self.Jump = False
        self.wattack = False
        self.bian = False
        self.skill = False
        if keys[pygame.K_d]:
            self.face_right = False
            self.state = 'walk'
        elif keys[pygame.K_a]:
            self.face_right = True
            self.state = 'walk'
        elif keys[pygame.K_k] and self.can_jump:
            self.state = 'jump'
            if self.big:
                setup.SFX['big_jump'].play()
            else:
                setup.SFX['small_jump'].play()
            self.y_vel = self.jump_vel
        elif keys[pygame.K_j] and self.can_attck:
            self.state = C.ATTACK
            if self.big:
                setup.SFX['attack'].play()
        elif keys[pygame.K_1]:
            self.state = 'kk'
        elif keys[pygame.K_2]:
            self.small2big(keys)
    def kk(self, keys):
        self.Bstand = False
        self.Run = False
        self.Jump = False
        self.wattack = False
        self.bian = False
        self.skill = True
        if self.current_time - self.bianshen_timer > 60:
            if self.frame_index < 9:
                self.frame_index += 1
            else:
                self.frame_index = 0
                self.state = 'stand'
            self.bianshen_timer = self.current_time

    def attack(self, keys):
        self.Bstand = False
        self.Run = False
        self.Jump = False
        self.wattack = True
        self.bian = False
        self.skill = False
        if self.big == False:
            if self.current_time - self.attack_timer > 100 and self.can_attck:
                if self.frame_index < 1:
                    self.frame_index += 1
                else:
                    self.state = 'stand'
                    self.can_attck = False
                self.attack_timer = self.current_time
        else:
            if self.current_time - self.attack_timer > 50 and self.can_attck:
                if self.frame_index < 8:
                    self.frame_index += 1
                else:
                    self.state = 'stand'
                    self.can_attck = False
                self.attack_timer = self.current_time

    def walk(self, keys):
        self.Bstand = False
        self.Run = True
        self.Jump = False
        self.wattack = False
        self.bian = False
        self.skill = False
        if keys[pygame.K_j]:
            self.state = C.ATTACK
            if self.big:
                setup.SFX['attack'].play()
            self.max_x_vel = self.max_run_vel
            self.x_accel = self.run_accel
            if self.frame_index < 1 and self.current_time - self.attack_timer > 100 and self.can_attck:
                self.frame_index += 1
            else:
                self.frame_index = 0
            self.attack_timer = self.current_time
        else:
            self.max_x_vel = self.max_walk_vel
            self.x_accel = self.walk_accel

        if keys[pygame.K_k] and self.can_jump:
            self.state = 'jump'
            if self.big:
                setup.SFX['big_jump'].play()
            else:
                setup.SFX['small_jump'].play()
            self.y_vel = self.jump_vel

        if self.current_time - self.walking_timer >100:
            if self.frame_index < 4:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time
        if keys[pygame.K_d]:
            self.face_right = True
            if self.x_vel < 0:
                if self.big == False:
                    self.frame_index = 3
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_a]:
            self.face_right = False
            if self.x_vel > 0:
                if self.big == False:
                    self.frame_index = 3
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        else:
            if self.face_right:
                self.x_vel -= self.x_accel
                if self.x_vel < 0:
                    self.x_vel = 0
                    self.state = 'stand'
            else:
                self.x_vel += self.x_accel
                if self.x_vel > 0:
                    self.x_vel = 0
                    self.state = 'stand'

    def jump(self, keys):
        self.bianshen_timer = self.current_time
        self.y_vel += self.anti_garavit
        self.can_jump = False
        self.Bstand = False
        self.Run = False
        self.Jump = True
        self.wattack = False
        self.bian = False
        self.skill = False

        if self.y_vel >= 0:
            self.state = 'fall'

        if keys[pygame.K_d]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_a]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        if not keys[pygame.K_k]:
            self.state = 'fall'
        if keys[pygame.K_1]:
            self.state = 'kk'

    def fall(self, keys):
        self.y_vel = self.calc_vel(self.y_vel, self.gravity, self.max_y_vel)

    def die(self, keys):
        self.rect.y += self.y_vel
        self.y_vel += self.anti_garavit

    def go_die(self, game_info):
        self.dead = True
        game_info[C.MARIO_DEAD] = True
        self.y_vel = self.jump_vel
        self.frame_index = 1
        self.state = C.MARIO_DEAD
        self.death_timer = self.current_time

    def small2big(self, keys):
        if self.big == False:
            self.big = True
            self.state = 'walk'
            return self.big
        else:
            self.state = 'stand'
        self.big_rstand_frames = self.big_rstand
        self.big_lstand_frames = self.big_lstand

    def big2small(self, keys):
        global handle_states
        self.big = False
        self.state = 'walk'
        return self.big


    def calc_vel(self, vel, accel, max_vel, is_positive=True):
        if is_positive:
            return min(vel + accel, max_vel)
        else:
            return max(vel - accel, -max_vel)

    def calc_frame_duration(self):
        duration = -60 / self.max_run_vel * abs(self.x_vel) + 80
        return duration

    def is_hurt_immune(self):
        if self.hurt_immune:
            if self.hurt_immune_timer == 0:
                self.hurt_immune_timer = self.current_time
                self.bland_image = pygame.Surface((1, 1))
            elif self.current_time - self.hurt_immune_timer < 1000:
                if (self.current_time - self.hurt_immune_timer) % 100 < 50:
                    self.image = self.bland_image
            else:
                self.hurt_immune = False
                self.hurt_immune_timer = 0
