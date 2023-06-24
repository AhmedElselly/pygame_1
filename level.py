import pygame
from settings import *
from support import *
from tiles import StaticTile, Crate, Coin, Palm, Tile
from enemy import Enemy
from decoration import *
from player import Player
from particles import ParticleEffect


class Level():
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # dust setup
        self.dust_sprite = pygame.sprite.GroupSingle()

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(
            terrain_layout, 'terrain')
        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        # crates
        crate_layouts = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layouts, 'crates')
        # coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')
        # fg_palms
        fg_palms_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palms_sprites = self.create_tile_group(
            fg_palms_layout, 'fg_palms')
        # bg_palms
        bg_palms_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palms_sprites = self.create_tile_group(
            bg_palms_layout, 'bg_palms')
        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(
            constraint_layout, 'constraint')

        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)
        self.clouds = Clouds(400, level_width, 30)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(
                            './gui/graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics(
                            './gui/graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y,
                                          './gui/graphics/coins/gold')
                        if val == '1':
                            sprite = Coin(tile_size, x, y,
                                          './gui/graphics/coins/silver')

                    if type == 'fg_palms':
                        if val == '0':
                            sprite = Palm(
                                tile_size, x, y, './gui/graphics/terrain/palm_small', 38)
                        if val == '1':
                            sprite = Palm(
                                tile_size, x, y, './gui/graphics/terrain/palm_large', 64)

                    if type == 'bg_palms':
                        sprite = Palm(tile_size, x, y,
                                      './gui/graphics/terrain/palm_bg', 38)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites:
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface,
                                    self.create_jump_particles)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load(
                        './gui/graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 10)
        else:
            pos += pygame.math.Vector2(10, -10)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palms_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False

        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palms_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):
        # sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        # background palms render
        self.bg_palms_sprites.update(self.world_shift)
        self.bg_palms_sprites.draw(self.display_surface)

        # terrain render
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # crate render
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass render
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # coins render
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # fg_palms render
        self.fg_palms_sprites.update(self.world_shift)
        self.fg_palms_sprites.draw(self.display_surface)

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)