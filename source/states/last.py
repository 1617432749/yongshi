from ..commponents import info
import pygame
from .. import tools, setup
from .. import sound
from .. import consatants as C
from ..commponents import player, stuff, boss, enemy
import os
import json

class Last:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = C.MAIN_MENU
        self.duration = 5000
        self.timer = 0
        self.info = info.Info(C.LAST, self.game_info)
        self.load_map_data()
        self.setup_background()
        self.setup_start_positions()
        self.setup_player()
        self.setup_ground_Items()
        self.steup_bricks_and_box()
        self.setup_enemies()
        self.setup_checkpoints()


        self.overhead_info_display = info.Info(C.LAST, self.game_info)
        self.sound_manager = sound.Sound(self.overhead_info_display)

    def load_map_data(self):
        file_name = 'last.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

    def setup_background(self):
        self.image_name = self.map_data['image_name']
        self.background = setup.GRAPHICS[self.image_name]
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width*C.BG_LAST),
                                                                   int(rect.height*3.8)))
        self.background_rect = self.background.get_rect()
        self.game_window = setup.SCREEN.get_rect()
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))

    def setup_start_positions(self):
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))
        self.start_x, self.end_x, self.player_x, self.player_y = self.positions[0]

    def setup_player(self):
        self.player = player.Player('mario')
        self.player.rect.x = self.game_window.x + self.player_x
        self.player.rect.bottom = self.player_y

    def setup_ground_Items(self):
        self.ground_items_group = pygame.sprite.Group()
        for name in ['ground', 'wall']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))
    def steup_bricks_and_box(self):
        self.brick_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()

        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                x, y = brick_data['x'], brick_data['y']
                brick_type = brick_data['type']
                if brick_type == 0:
                    if 'brick_num' in brick_data:
                        # TODO batch
                        pass
                    else:
                        self.brick_group.add(brick.Brick(x, y, brick_type, None))
                elif brick_type == 1:
                    self.brick_group.add(brick.Brick(x, y, brick_type, self.coin_group))
                else:
                    self.brick_group.add(brick.Brick(x, y, brick_type, self.powerup_group))

        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x, y = box_data['x'], box_data['y']
                box_type = box_data['type']
                if box_type == 1:
                    self.box_group.add(box.Box(x, y, box_type, self.coin_group))
                else:
                    self.box_group.add(box.Box(x, y, box_type, self.powerup_group))
    def setup_enemies(self):
        self.dying_group = pygame.sprite.Group()
        self.shell_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group_dict = {}
        for enemy_group_data in self.map_data['enemy']:
            group = pygame.sprite.Group()
            for enemy_group_id, enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                    group.add(enemy.create_enemy(enemy_data))
                self.enemy_group_dict[enemy_group_id] = group

    def setup_checkpoints(self):
        self.checkpoint_group = pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x, y, w, h = item['x'], item['y'], item['width'], item['height']
            checkpoint_type = item['type']
            enemy_groupid = item.get('enemy_groupid')
            self.checkpoint_group.add(stuff.Checkpoint(x, y, w, h, checkpoint_type, enemy_groupid))
    def update(self, surface, keys):
        self.curren_time = pygame.time.get_ticks()
        self.player.update(keys)
        self.sound_manager.update(self.game_info, self.player)

        if self.player.dead:
            if self.curren_time - self.player.death_timer > 3000:
                self.finished = True
                self.update_game_info()
        # if self.player.rect.centerx > 8200:
        #     self.finished = True
        #     state = self.player.state
        #     return state
        # elif self.is_frozen():
        #     pass
        else:
            self.update_player_position()
            self.check_checkpoints()
            self.check_if_go_die()
            self.update_game_window()
            # self.brick_group.update()
            # self.box_group.update()
            self.enemy_group.update(self)
            self.dying_group.update(self)
            self.shell_group.update(self)
            # self.coin_group.update()
            # self.powerup_group.update(self)

        self.draw(surface)

    def update_player_position(self):
        self.player.rect.x += self.player.x_vel
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
        self.check_x_collisions()

        # if not self.player.dead:
        self.player.rect.y += self.player.y_vel
        self.check_y_collisions()

    def check_x_collisions(self):
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        if ground_item:
            self.adjust_player_x(ground_item)
    def check_y_collisions(self):
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        if ground_item:
            self.adjust_player_y(ground_item)
        self.check_will_fall(self.player)
    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel = 0

    def adjust_player_y(self, sprite):
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.y_vel = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'
        else:
            self.player.y_vel = 7
            self.player.rect.top = sprite.rect.bottom
            self.player.state = 'fall'
    def update_game_window(self):
        third = self.game_window.x + self.game_window.width / 3
        third2 = self.game_window.x + self.game_window.width*2 / 3
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.end_x:
            self.game_window.x += self.player.x_vel
        elif self.player.x_vel < 0 and self.player.rect.centerx < third2 and self.game_window.left > self.start_x:
            self.game_window.x += self.player.x_vel
        if self.player.rect.centerx >= 989:
            self.start_x = 989

    def draw(self, surface):
        self.game_ground.blit(self.background, self.game_window, self.game_window)
        self.game_ground.blit(self.player.image, self.player.rect)
        # self.powerup_group.draw(self.game_ground)
        # self.brick_group.draw(self.game_ground)
        # self.box_group.draw(self.game_ground)
        self.enemy_group.draw(self.game_ground)
        self.dying_group.draw(self.game_ground)
        self.shell_group.draw(self.game_ground)
        # self.coin_group.draw(self.game_ground)

        surface.blit(self.game_ground, (0, 0), self.game_window)
        self.info.draw(surface)

    def check_will_fall(self, sprite):
        sprite.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_group)
        collided_sprite = pygame.sprite.spritecollideany(sprite, check_group)
        if not collided_sprite and sprite.state != 'jump' :
            sprite.state = 'fall'
        sprite.rect.y -= 1
    def check_checkpoints(self):
        checkpoint = pygame.sprite.spritecollideany(self.player, self.checkpoint_group)
        if checkpoint:
            if checkpoint.checkpoint_type == 0:
                self.enemy_group.add(self.enemy_group_dict[str(checkpoint.enemy_groupid)])
            checkpoint.kill()

    def check_if_go_die(self):
        if self.player.rect.y > C.SCREEN_H:
            self.player.go_die(self.game_info)

    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.next = C.GAME_OVER
            self.sound_manager.stop_music()
        else:
            self.next = C.LOAD_SCREEN