from random import *
import math

from Clases.GameOver import *
from Clases.Pause import *
from Clases.PowerUp import *
from Clases.Tienda import *
from Clases.Boss import *
from Clases.Bullet import *
from Clases.MainCharacter import *
from Clases.Weapon import *
from Clases.Winner import *
from Clases.Enemy import *
from Clases.Menu import *
from Clases.Moneda import *


class Game(arcade.View):
    def __init__(self):
        super().__init__()

        # lists
        self.player_list = None
        self.bullet_list = None
        self.enemy_list = None
        self.powerUpList = None
        self.weapon_list = None
        self.invisible_list = None
        self.bomb_list = None
        self.lista_monedas = None
        self.boss_list = None
        self.bullet_boss = None
        self.music_list = None

        # main character and bullet sprites
        self.player_sprite = None
        self.bullet_sprite = None
        self.weapon = None
        self.invisible = None
        self.bomb = None

        # max number of enemies
        self.max_enemies = None

        # map sprites
        self.paredes = None
        self.suelo = None
        self.cosas = None
        self.obstaculos = None
        self.obstaculos_2 = None
        self.perfeccionar = None
        self.cuerpos = None
        self.sangre = None
        self.escaleras = None
        self.background = None
        self.botes = None

        # physics
        self.physics_paredes = None
        self.physics_cosas = None
        self.physics_obstaculos = None
        self.physics_paredes_enemy = None
        self.physics_obstaculos2 = None
        self.physics_perfeccionar = None
        self.physics_cuerpos = None
        self.physics_sangre = None
        self.physics_enemy_list = None

        # number of the room the player is
        self.current_room = 0

        # indicador lista de objetos a displayear
        self.selling = None

        # collision
        self.collision_enemy = None
        self.collision_main_character = None

        # movement of the enemies when main character is dead
        self.movement = False

        # counters
        self.score = None
        self.spawn_cd = None
        self.time = None
        self.time_quotient = None
        self.tiempo_vida = None

        self.start = False
        self.space = False

        self.finish_0 = False
        self.finish_1 = False
        self.finish_2 = False
        self.finish_3 = False
        self.enemy_death = False

        self.tienda = None
        self.shop = None
        self.shop_list = None

        # PowerUps
        self.powerUpAguja = None
        self.powerUpListAguja = None
        self.powerUpTriple = None
        self.powerUpListTriple = None
        self.powerUpLejia = None
        self.powerUpListLejia = None
        self.cd = None
        self.triple = False
        self.cd_triple = None
        self.dissapear = True
        self.cd_dissapear = None
        self.legia = False
        self.boss_triple = False
        self.boss_enemy = False

        self.music = None
        self.music_bool = True

        self.music_0 = False

        # booleans
        self.jeringa1_activa = True
        self.jeringa2_activa = False
        self.jeringa3_activa = False
        self.pause_done = False

        # Roof vida
        self.vida = None
        self.vida_2 = None
        self.rectangle_right_hearts = None

    def setup(self):
        """
        Set up the game and initialize the variables. Call this function to restart the game
        """
        # Set up the lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.weapon_list = arcade.SpriteList()
        self.powerUpList = arcade.SpriteList()
        self.invisible_list = arcade.SpriteList()
        self.physics_paredes_enemy = arcade.SpriteList()
        self.physics_enemy_list = arcade.SpriteList()
        self.physics_paredes = arcade.SpriteList()
        self.physics_cosas = arcade.SpriteList()
        self.physics_obstaculos = arcade.SpriteList()
        self.physics_paredes_enemy = arcade.SpriteList()
        self.physics_obstaculos2 = arcade.SpriteList()
        self.physics_perfeccionar = arcade.SpriteList()
        self.physics_cuerpos = arcade.SpriteList()
        self.physics_sangre = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()
        self.shop_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()
        self.bullet_boss = arcade.SpriteList()

        self.powerUpListAguja = arcade.SpriteList()
        self.powerUpListTriple = arcade.SpriteList()
        self.powerUpListLejia = arcade.SpriteList()
        self.lista_monedas = arcade.SpriteList()

        self.background = arcade.SpriteList()
        self.music_list = []

        # Set up the player
        self.player_sprite = MainCharacter(sprites_folder + os.path.sep + "protagonista.png", sprite_scaling,
                                           3, 200)
        self.player_list.append(self.player_sprite)

        self.weapon = Weapon(bullet_folder + os.path.sep + "jeringa1.png", self.player_sprite.center_x + 15,
                             self.player_sprite.center_y - 5, 90)
        self.weapon_list.append(self.weapon)

        # La tienda
        self.tienda = Tienda()
        # The entrances is the first room
        self.entrance()

        # Set up the max number of enemies
        self.max_enemies = 10

        # Set up counters
        self.score = 0
        # -------------------------------------------------------------------------------
        self.time = 60
        self.cd = 0
        self.spawn_cd = 0
        self.cd_dissapear = 0
        self.cd_triple = 0
        self.tiempo_vida = 5

        self.rectangle_right_hearts = 540

    def reset_things(self):

        self.player_sprite.go_right = False
        self.player_sprite.go_left = False
        self.player_sprite.go_up = False
        self.player_sprite.go_down = False
        self.player_sprite.shooting_right = False
        self.player_sprite.shooting_left = False
        self.player_sprite.shooting_up = False
        self.player_sprite.shooting_down = False
        self.pause_done = False

    # Rooms created
    def entrance(self):
        # load map
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "entrada.tmx")

        # load layers
        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo ", 1)
        self.cosas = arcade.tilemap.process_layer(my_map, "cosas", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.escaleras = arcade.tilemap.process_layer(my_map, "escalera", 1)

        # bomb
        if not self.finish_0:
            self.bomb = arcade.Sprite(resources_folder + os.path.sep + "bombaAntivirus.png", 1, center_x=320,
                                      center_y=320)
            self.bomb_list.append(self.bomb)

        if len(self.bomb_list) != 0 and self.finish_0:
            self.bomb.kill()

        # physics layers and player
        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)
        self.physics_cosas = arcade.PhysicsEngineSimple(self.player_sprite, self.cosas)
        self.physics_obstaculos = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos)

        # enemies
        self.create_enemies()

        bool_music = True
        if bool_music:
            self.music = arcade.load_sound(music_folder + os.path.sep + "music_room1-2.wav")
            arcade.play_sound(self.music)
            return bool_music == False

    def room_1(self):
        # load map
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "planta1.tmx")

        # load layers
        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo ", 1)
        self.obstaculos_2 = arcade.tilemap.process_layer(my_map, "obstaculos 2", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.escaleras = arcade.tilemap.process_layer(my_map, "escalera", 1)

        # bomb
        if not self.finish_1:
            self.bomb = arcade.Sprite(resources_folder + os.path.sep + "bombaAntivirus.png", 1, center_x=320,
                                      center_y=320)
            self.bomb_list.append(self.bomb)

        if len(self.bomb_list) != 0 and self.finish_1:
            self.bomb.kill()

        # physics layers and player
        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)
        self.physics_obstaculos = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos)
        self.physics_obstaculos2 = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos_2)

        # enemies
        self.create_enemies()

        bool_music = True
        if bool_music:
            self.music = arcade.load_sound(music_folder + os.path.sep + "music_room1-2.wav")
            arcade.play_sound(self.music)
            return bool_music == False

    def room_2(self):
        # load map
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "planta2.tmx")

        # load layers
        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo", 1)
        self.obstaculos_2 = arcade.tilemap.process_layer(my_map, "obstaculos2", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.perfeccionar = arcade.tilemap.process_layer(my_map, "perfeccionar", 1)
        self.cuerpos = arcade.tilemap.process_layer(my_map, "cuerpos", 1)
        self.sangre = arcade.tilemap.process_layer(my_map, "sangre", 1)
        self.escaleras = arcade.tilemap.process_layer(my_map, "escalera", 1)

        # bomb
        if not self.finish_2:
            self.bomb = arcade.Sprite(resources_folder + os.path.sep + "bombaAntivirus.png", 1, center_x=320,
                                      center_y=320)
            self.bomb_list.append(self.bomb)
        if len(self.bomb_list) != 0 and self.finish_2:
            self.bomb.kill()

        # physics layers and player
        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)
        self.physics_obstaculos = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos)
        self.physics_obstaculos2 = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos_2)
        self.physics_perfeccionar = arcade.PhysicsEngineSimple(self.player_sprite, self.perfeccionar)
        self.physics_cuerpos = arcade.PhysicsEngineSimple(self.player_sprite, self.cuerpos)
        self.physics_sangre = arcade.PhysicsEngineSimple(self.player_sprite, self.sangre)

        # enemies
        self.create_enemies()

        bool_music = True
        if bool_music:
            self.music = arcade.load_sound(music_folder + os.path.sep + "music_room3-4.wav")
            arcade.play_sound(self.music)
            return bool_music == False

    def room_3(self):
        # load map
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "planta3.tmx")

        # load layers
        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo", 1)
        self.sangre = arcade.tilemap.process_layer(my_map, "sangre", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.cuerpos = arcade.tilemap.process_layer(my_map, "cuerpos", 1)
        self.escaleras = arcade.tilemap.process_layer(my_map, "escalera", 1)

        # bomb
        if not self.finish_3:
            self.bomb = arcade.Sprite(resources_folder + os.path.sep + "bombaAntivirus.png", 1, center_x=350,
                                      center_y=320)
            self.bomb_list.append(self.bomb)

        if len(self.bomb_list) != 0 and self.finish_3:
            self.bomb.kill()

        # physics layers and player
        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)
        self.physics_obstaculos = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos)
        self.physics_cuerpos = arcade.PhysicsEngineSimple(self.player_sprite, self.cuerpos)
        self.physics_sangre = arcade.PhysicsEngineSimple(self.player_sprite, self.sangre)

        # enemies
        self.create_enemies()

        bool_music = True
        if bool_music:
            self.music = arcade.load_sound(music_folder + os.path.sep + "music_room3-4.wav")
            arcade.play_sound(self.music)
            return bool_music == False

    def rooftop(self):
        # load map
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "azotea.tmx")

        background = arcade.Sprite(maps_folder + os.path.sep + "fondo azotea.png", center_x=320, center_y=320)
        self.background.append(background)

        # load layers
        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo", 1)
        self.escaleras = arcade.tilemap.process_layer(my_map, "escalera", 1)

        # physics layers and player
        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)

        self.create_boss()

    def shop_room(self):
        # load map
        arcade.tilemap.read_tmx(maps_folder + os.path.sep + "tienda.tmx")

        # physics layers and player
        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)

    def room_draw(self):
        # drawing layers
        # Entrance
        if self.current_room == 0:
            self.paredes.draw()
            self.suelo.draw()
            self.cosas.draw()
            self.obstaculos.draw()
            self.escaleras.draw()

        # Room 1
        if self.current_room == 1:
            self.paredes.draw()
            self.suelo.draw()
            self.obstaculos.draw()
            self.obstaculos_2.draw()
            self.escaleras.draw()

        # Room 2
        if self.current_room == 2:
            self.paredes.draw()
            self.suelo.draw()
            self.obstaculos.draw()
            self.obstaculos_2.draw()
            self.perfeccionar.draw()
            self.sangre.draw()
            self.cuerpos.draw()
            self.escaleras.draw()

        # Room 3
        if self.current_room == 3:
            self.paredes.draw()
            self.suelo.draw()
            self.obstaculos.draw()
            self.sangre.draw()
            self.cuerpos.draw()
            self.escaleras.draw()

        if self.current_room == 4:
            self.background.draw()
            self.paredes.draw()
            self.suelo.draw()
            self.escaleras.draw()
            self.vida = arcade.draw_lrtb_rectangle_filled(100, 540, 600, 575,
                                                          arcade.csscolor.RED)
            self.vida = arcade.draw_lrtb_rectangle_filled(100, self.rectangle_right_hearts, 600, 575,
                                                          arcade.csscolor.GREEN)

        if self.current_room == 5:
            self.paredes.draw()
            self.suelo.draw()
            self.obstaculos.draw()
            self.obstaculos_2.draw()
            self.botes.draw()

        # Tienda
        if self.current_room == 6:
            self.paredes.draw()
            self.suelo.draw()
            self.tienda.draw_tendero()
            arcade.draw_text("TENDERO: Compra algunos de estos productos que te pueden ayudar", 45, 105, arcade.color.BLACK, 15)
            arcade.draw_text("a derrotar al virus", 45, 75, arcade.color.BLACK, 15)
            if self.selling == 0:
                self.tienda.draw_obj_planta_baja()
            elif self.selling == 1:
                self.tienda.draw_obj_planta1()
            elif self.selling == 2:
                self.tienda.draw_obj_planta2()
            elif self.selling == 3:
                self.tienda.draw_obj_planta3()

    def room_update(self):

        # map update
        # Entrance -> Room 1
        if self.player_sprite.center_y > 630 and 323 < self.player_sprite.center_x < 380 and self.current_room == 0:
            if self.finish_0:
                self.current_room = 1
                self.room_1()
                self.player_sprite.center_y = 620
                self.player_sprite.center_x = 448
                self.shop.kill()
            if not self.finish_0:
                self.player_sprite.center_y = 630

        # Entrance -> Shop
        if self.player_sprite.center_x <= 0 and self.current_room == 0:
            if self.finish_0:
                self.current_room = 6
                self.selling = 0
                self.shop_room()
                self.player_sprite.center_y = screen_height / 2
                self.player_sprite.center_x = 630
                self.shop.kill()

        # Room 1 -> Room 2
        if self.player_sprite.center_y > 635 and 258 < self.player_sprite.center_x < 316 and self.current_room == 1:
            if self.finish_1:
                self.current_room = 2
                self.room_2()
                self.player_sprite.center_y = 30
                self.player_sprite.center_x = 288
                self.shop.kill()
            if not self.finish_1:
                self.player_sprite.center_y = 635

        # Room 1 -> Shop
        if self.player_sprite.center_x <= 0 and self.current_room == 1:
            if self.finish_1:
                self.current_room = 6
                self.selling = 1
                self.shop_room()
                self.player_sprite.center_y = screen_height / 2
                self.player_sprite.center_x = 630
                self.shop.kill()

        # Room 2 -> Room 3
        if self.player_sprite.center_y > 635 and 258 < self.player_sprite.center_x < 316 and self.current_room == 2:
            if self.finish_2:
                self.current_room = 3
                self.room_3()
                self.player_sprite.center_y = 30
                self.player_sprite.center_x = 256
                self.shop.kill()
            if not self.finish_2:
                self.player_sprite.center_y = 635

        # Room 2 -> Shop
        if self.player_sprite.center_x <= 0 and self.current_room == 2:
            if self.finish_2:
                self.current_room = 6
                self.selling = 2
                self.shop_room()
                self.player_sprite.center_y = screen_height / 2 - 42
                self.player_sprite.center_x = 600
                self.shop.kill()

        # Room 3 -> Rooftop
        if self.player_sprite.center_y > 635 and 514 < self.player_sprite.center_x < 573 and self.current_room == 3:
            self.current_room = 4
            self.rooftop()
            self.shop.kill()
            self.player_sprite.center_y = 30
            self.player_sprite.center_x = 70

        # Room 3 -> Shop
        if self.player_sprite.center_x <= 0 and self.current_room == 3:
            if self.finish_3:
                self.current_room = 6
                self.selling = 3
                self.shop_room()
                self.player_sprite.center_y = screen_height / 2
                self.player_sprite.center_x = 635
                self.shop.kill()

        # Rooftop -> Outside
        if self.player_sprite.center_y > 387 and self.current_room == 4:
            self.player_sprite.center_y = 387
        if self.player_sprite.center_x > 640 and self.current_room == 4:
            self.player_sprite.center_x = 620
        if self.player_sprite.center_x < 10 and self.current_room == 4:
            self.player_sprite.center_x = 10
        if self.player_sprite.center_y < 10 and self.current_room == 4:
            self.player_sprite.center_y = 10

        # Going down stairs
        # Room 3 -> Room 2
        if self.player_sprite.center_y < 10 and 226 < self.player_sprite.center_x < 284 and self.current_room == 3:
            self.current_room = 2
            self.room_2()
            self.player_sprite.center_y = 620
            self.player_sprite.center_x = 288

        # Room 2 -> Room 1
        if self.player_sprite.center_y < 10 and 256 < self.player_sprite.center_x < 320 and self.current_room == 2:
            self.current_room = 1
            self.room_1()
            self.player_sprite.center_y = 620
            self.player_sprite.center_x = 300

        # Room 1 -> Entrance
        if self.player_sprite.center_y > 640 and 418 < self.player_sprite.center_x < 476 and self.current_room == 1:
            self.current_room = 0
            self.entrance()
            self.player_sprite.center_y = 620
            self.player_sprite.center_x = 352

        # Shop -> Entrance
        if self.player_sprite.center_x >= screen_width and self.selling == 0:
            self.current_room = 0
            self.entrance()
            self.player_sprite.center_y = screen_height / 2
            self.player_sprite.center_x = 10

        # Shop -> Room 1
        if self.player_sprite.center_x >= screen_width and self.selling == 1:
            self.current_room = 1
            self.room_1()
            self.player_sprite.center_y = screen_height / 2
            self.player_sprite.center_x = 10

        # Shop -> Room 2
        if self.player_sprite.center_x >= screen_width and self.selling == 2:
            self.current_room = 2
            self.room_2()
            self.player_sprite.center_y = screen_height / 2 + 70
            self.player_sprite.center_x = 15

        # Shop -> Room 3
        if self.player_sprite.center_x >= screen_width and self.selling == 3:
            self.current_room = 3
            self.room_3()
            self.player_sprite.center_y = screen_height / 2
            self.player_sprite.center_x = 10

        self.room_update_2()

    def room_update_2(self):
        # update physics
        # Entrance
        if self.current_room == 0:
            self.physics_paredes.update()
            self.physics_cosas.update()
            self.physics_obstaculos.update()
            for bullet in self.bullet_list:
                if arcade.check_for_collision_with_list(bullet, self.obstaculos) or arcade.check_for_collision_with_list(bullet, self.cosas):
                    bullet.kill()
            if len(self.enemy_list) == 0 and self.enemy_death:
                self.enemy_death = False
                self.finish_0 = True
                self.shop = arcade.Sprite(resources_folder + os.path.sep + "cartel tienda.png", 1, center_x=32,
                                          center_y=305)
                self.shop_list.append(self.shop)
            if len(self.enemy_list) > 0:
                self.finish_0 = False

        # Room 1
        if self.current_room == 1:
            self.physics_paredes.update()
            self.physics_obstaculos.update()
            self.physics_obstaculos2.update()
            if len(self.enemy_list) == 0 and self.enemy_death:
                self.enemy_death = False
                self.finish_1 = True
                self.shop = arcade.Sprite(resources_folder + os.path.sep + "cartel tienda.png", 1, center_x=32,
                                          center_y=305)
                self.shop_list.append(self.shop)
            if len(self.enemy_list) > 0:
                self.finish_1 = False
            for bullet in self.bullet_list:
                if arcade.check_for_collision_with_list(bullet, self.obstaculos) or arcade.check_for_collision_with_list(bullet, self.obstaculos_2):
                    bullet.kill()

        # Room 2
        if self.current_room == 2:
            self.physics_paredes.update()
            self.physics_obstaculos.update()
            self.physics_obstaculos2.update()
            self.physics_perfeccionar.update()
            self.physics_sangre.update()
            self.physics_cuerpos.update()
            if len(self.enemy_list) == 0 and self.enemy_death:
                self.enemy_death = False
                self.finish_2 = True
                self.shop = arcade.Sprite(resources_folder + os.path.sep + "cartel tienda.png", 1, center_x=32,
                                          center_y=400)
                self.shop_list.append(self.shop)
            if len(self.enemy_list) > 0:
                self.finish_2 = False
            for bullet in self.bullet_list:
                if arcade.check_for_collision_with_list(bullet, self.obstaculos) or arcade.check_for_collision_with_list(
                        bullet, self.obstaculos_2) or arcade.check_for_collision_with_list(bullet, self.cuerpos):
                    bullet.kill()

        # Room 3
        if self.current_room == 3:
            self.physics_paredes.update()
            self.physics_sangre.update()
            self.physics_cuerpos.update()
            self.physics_obstaculos.update()
            for bullet in self.bullet_list:
                if arcade.check_for_collision_with_list(bullet, self.obstaculos) or arcade.check_for_collision_with_list(bullet, self.cuerpos):
                    bullet.kill()
            if len(self.enemy_list) == 0 and self.enemy_death:
                self.enemy_death = False
                self.finish_3 = True
                self.shop = arcade.Sprite(resources_folder + os.path.sep + "cartel tienda.png", 1, center_x=32,
                                          center_y=335)
                self.shop_list.append(self.shop)
            if len(self.enemy_list) > 0:
                self.finish_3 = False

        # Rooftop & tienda
        if self.current_room == 4 or self.current_room == 6:
            self.physics_paredes.update()

    def create_enemies(self):
        if self.start:
            max_number = 0
            random_number = 0
            if self.current_room == 0:
                max_number = 5
                random_number = randint(1, 2)
            if self.current_room == 1:
                max_number = 8
                random_number = randint(1, 3)
            if self.current_room == 2:
                max_number = 11
                random_number = randint(2, 3)
            if self.current_room == 3:
                max_number = 14
                random_number = randint(2, 4)
            if len(self.enemy_list) < max_number:
                for enemy in range(random_number):
                    pos_x = 0
                    pos_y = 0
                    place_choice = randint(0, 3)
                    foe_choice = randint(0, 2)

                    if place_choice == 0:
                        pos_x = randint(610, 640)
                        if self.current_room == 0 or self.current_room == 1:
                            pos_y = 300
                        if self.current_room == 2:
                            pos_y = 270
                        if self.current_room == 3:
                            pos_y = 330
                    if place_choice == 1:
                        pos_x = randint(0, 30)
                        if self.current_room == 0 or self.current_room == 1:
                            pos_y = 300
                        if self.current_room == 2:
                            pos_y = 390
                        if self.current_room == 3:
                            pos_y = 330
                    if place_choice == 2:
                        if self.current_room == 0:
                            pos_x = randint(0, 30)
                            pos_y = 300
                        if self.current_room == 1:
                            pos_x = randint(0, 30)
                            pos_y = 360
                        if self.current_room == 2:
                            pos_x = 390
                            pos_y = randint(610, 640)
                        if self.current_room == 3:
                            pos_x = 300
                            pos_y = randint(610, 640)
                    if place_choice == 3:
                        if self.current_room == 0:
                            pos_x = randint(610, 640)
                            pos_y = 300
                        if self.current_room == 1:
                            pos_x = 330
                            pos_y = randint(0, 30)
                        if self.current_room == 2:
                            pos_x = 390
                            pos_y = randint(610, 640)
                        if self.current_room == 3:
                            pos_x = 300
                            pos_y = randint(610, 640)

                    if foe_choice == 0:
                        enemy = Enemy(sprites_folder + os.path.sep + "enemigo1.png",
                                      1, pos_x, pos_y, 2, 1)
                    elif foe_choice == 1:
                        enemy = Enemy(sprites_folder + os.path.sep + "enemigo2.png",
                                      1, pos_x, pos_y, 3, 1)
                    elif foe_choice == 2:
                        enemy = Enemy(sprites_folder + os.path.sep + "enemigo3.png",
                                      1, pos_x, pos_y, 5, 1)

                    self.enemy_list.append(enemy)

    def create_enemies2(self, boss, max_number, random_number):
        if len(self.enemy_list) < max_number:
            for enemy in range(random_number):
                pos_x = boss.center_x
                pos_y = boss.center_y
                foe_choice = randint(0, 2)

                if foe_choice == 0:
                    enemy = Enemy(sprites_folder + os.path.sep + "enemigo1.png",
                                  1, pos_x, pos_y, 1, 1)
                elif foe_choice == 1:
                    enemy = Enemy(sprites_folder + os.path.sep + "enemigo2.png",
                                  1, pos_x, pos_y, 2, 1)
                elif foe_choice == 2:
                    enemy = Enemy(sprites_folder + os.path.sep + "enemigo3.png",
                                  1, pos_x, pos_y, 4, 1)

                self.enemy_list.append(enemy)

    def waves(self):
        if 40 <= self.time_quotient <= 59:
            if self.spawn_cd % 190 == 0:
                self.create_enemies()
        if 10 <= self.time_quotient <= 40:
            if self.spawn_cd % 160 == 0:
                self.create_enemies()
        if 10 >= self.time_quotient:
            if self.spawn_cd % 130 == 0:
                self.create_enemies()
        if self.time_quotient < 0:
            self.max_enemies = 0
            self.start = False
            self.time = 60
            self.enemy_death = True

    def create_boss(self):
        boss = Boss(sprites_folder + os.path.sep + "jefe final.png", 1, 300, 400, 100, 5)
        self.boss_list.append(boss)

    def update_boss(self):
        for boss in self.boss_list:
            boss.movement()
            if 80 <= boss.number_of_hearts <= 100:
                if self.cd % 30 == 0:
                    self.boss_shoot(boss)
            if 50 <= boss.number_of_hearts < 80:
                self.boss_triple = True
                if self.cd % 30 == 0:
                    self.boss_shoot(boss)
            if 40 <= boss.number_of_hearts < 50:
                if self.spawn_cd % 190 == 0:
                    self.create_enemies2(boss, 10, randint(2, 4))
            if 30 <= boss.number_of_hearts < 40:
                if self.spawn_cd % 150 == 0:
                    self.create_enemies2(boss, 15, randint(2, 4))
            if 25 <= boss.number_of_hearts < 30:
                if self.spawn_cd % 110 == 0:
                    self.create_enemies2(boss, 20, randint(2, 4))
            if 0 <= boss.number_of_hearts < 25:
                if self.cd % 30 == 0:
                    self.boss_shoot(boss)
                if self.spawn_cd % 190 == 0:
                    self.create_enemies2(boss, 20, randint(2, 4))

            for enemy in self.enemy_list:
                self.collision_enemy = arcade.check_for_collision_with_list(enemy, self.enemy_list)
                for i in range(len(self.collision_enemy)):
                    self.physics_enemy_list = arcade.PhysicsEngineSimple(self.collision_enemy[i], self.enemy_list)

        # collisions player - boss
        for bullet in self.bullet_list:
            if arcade.check_for_collision_with_list(bullet, self.paredes):
                bullet.kill()
            collision_bullet_boss = arcade.check_for_collision_with_list(bullet, self.boss_list)
            for boss in collision_bullet_boss:
                if self.dissapear:
                    bullet.kill()
                if boss.number_of_hearts > 0:
                    boss.number_of_hearts -= 1
                if boss.number_of_hearts <= 0:
                    boss.kill()
                    winner = Winner()
                    self.window.show_view(winner)
                    music = True
                    if music:
                        victory = arcade.load_sound(music_folder + os.path.sep + "victory.wav")
                        arcade.play_sound(victory)
                        return music == False

        for bullet in self.bullet_boss:
            if arcade.check_for_collision_with_list(bullet, self.player_list):
                self.player_sprite.number_of_hearts -= 1
                if self.dissapear:
                    bullet.kill()
                if self.player_sprite.number_of_hearts == 0:
                    arcade.pause(1)
                    game_over = GameOver()
                    self.window.show_view(game_over)

    def boss_shoot(self, boss):
        bullet = Bullet(bullet_folder + os.path.sep + "gota1.png", 1)
        bullet.center_x = boss.center_x
        bullet.center_y = boss.center_y
        bullet.change_y = -5
        self.bullet_boss.append(bullet)

        if self.boss_triple:
            bullet = Bullet(bullet_folder + os.path.sep + "gota2.png", 1)
            bullet.center_x = boss.center_x + 20
            bullet.center_y = boss.center_y
            bullet.change_y = -5
            self.bullet_boss.append(bullet)

            bullet = Bullet(bullet_folder + os.path.sep + "gota3.png", 1)
            bullet.center_x = boss.center_x - 20
            bullet.center_y = boss.center_y
            bullet.change_y = -5
            self.bullet_boss.append(bullet)

    def shoot(self, direction, dir):

        # create bullet sprite
        """if self.current_room == 0:"""
        bullet = None
        if self.jeringa1_activa:
            bullet = Bullet(bullet_folder + os.path.sep + "gota1.png", sprite_scaling / 2)
        elif self.jeringa2_activa:
            bullet = Bullet(bullet_folder + os.path.sep + "gota2.png", sprite_scaling / 2)
        elif self.jeringa3_activa:
            bullet = Bullet(bullet_folder + os.path.sep + "gota3.png", sprite_scaling / 2)
        self.bullet_list.append(bullet)

        """if self.current_room == 1:
            bullet = Bullet(bullet_folder + os.path.sep + "gota2.png", sprite_scaling / 2)
            self.bullet_list.append(bullet)"""

        if direction == "right" or direction == "left" or direction == "up" or direction == "down" or \
                direction == "right_up" or direction == "right_down" or direction == "left_up" or direction == "left_down":
            shoot = arcade.load_sound(sound_folder + os.path.sep + "disparo.wav")
            arcade.play_sound(shoot)

        if direction == "right":
            bullet.center_x = self.weapon.center_x + 10
            bullet.center_y = self.weapon.center_y + 1
            bullet.change_x = bullet.speed
            bullet.angle = 90
            if dir is None:
                dir = "right"
                if self.triple and dir == "right":
                    self.shoot("right_down", "right")
                    self.shoot("right_up", "right")
        if direction == "left":
            bullet.center_x = self.weapon.center_x - 10
            bullet.center_y = self.weapon.center_y
            bullet.change_x = -bullet.speed
            bullet.angle = 270
            if dir is None:
                dir = "left"
                if self.triple and dir == "left":
                    self.shoot("left_down", "left")
                    self.shoot("left_up", "left")
        if direction == "up":
            bullet.center_x = self.weapon.center_x
            bullet.center_y = self.weapon.center_y + 10
            bullet.change_y = bullet.speed
            bullet.angle = 180
            if dir is None:
                dir = "up"
                if self.triple and dir == "up":
                    self.shoot("left_up", "up")
                    self.shoot("right_up", "up")
        if direction == "down":
            bullet.center_x = self.weapon.center_x
            bullet.center_y = self.weapon.center_y - 10
            bullet.change_y = -bullet.speed
            bullet.angle = 0
            if dir is None:
                dir = "down"
                if self.triple and dir == "down":
                    self.shoot("right_down", "down")
                    self.shoot("left_down", "down")
        if direction == "right_up":
            bullet.center_x = self.weapon.center_x + 10
            bullet.center_y = self.weapon.center_y + 10
            bullet.change_x = bullet.speed / math.sqrt(2)
            bullet.change_y = bullet.speed / math.sqrt(2)
            bullet.angle = 135
            if dir is None:
                dir = "right_up"
                if self.triple and dir == "right_up":
                    self.shoot("right", "right_up")
                    self.shoot("up", "right_up")
        if direction == "right_down":
            bullet.center_x = self.weapon.center_x + 10
            bullet.center_y = self.weapon.center_y - 10
            bullet.change_x = bullet.speed / math.sqrt(2)
            bullet.change_y = -bullet.speed / math.sqrt(2)
            bullet.angle = 45
            if dir is None:
                dir = "right_down"
                if self.triple and dir == "right_down":
                    self.shoot("down", "right_down")
                    self.shoot("right", "right_down")
        if direction == "left_up":
            bullet.center_x = self.weapon.center_x - 10
            bullet.center_y = self.weapon.center_y + 10
            bullet.change_x = -bullet.speed / math.sqrt(2)
            bullet.change_y = bullet.speed / math.sqrt(2)
            bullet.angle = 225
            if dir is None:
                dir = "left_up"
                if self.triple and dir == "left_up":
                    self.shoot("left", "left_up")
                    self.shoot("up", "left_up")
        if direction == "left_down":
            bullet.center_x = self.weapon.center_x - 10
            bullet.center_y = self.weapon.center_y - 10
            bullet.change_x = -bullet.speed / math.sqrt(2)
            bullet.change_y = -bullet.speed / math.sqrt(2)
            bullet.angle = 315
            if dir is None:
                dir = "left_down"
                if self.triple and dir == "left_down":
                    self.shoot("down", "left_down")
                    self.shoot("left", "left_down")

    def update_shooting(self, player_sprite):

        # shooting
        self.cd += 2

        if self.cd % 30 == 0:
            if player_sprite.shooting_right and player_sprite.shooting_up:
                self.shoot("right_up", None)
            elif player_sprite.shooting_left and player_sprite.shooting_up:
                self.shoot("left_up", None)
            elif player_sprite.shooting_right and player_sprite.shooting_down:
                self.shoot("right_down", None)
            elif player_sprite.shooting_left and player_sprite.shooting_down:
                self.shoot("left_down", None)
            elif player_sprite.shooting_right:
                self.shoot("right", None)
            elif player_sprite.shooting_up:
                self.shoot("up", None)
            elif player_sprite.shooting_left:
                self.shoot("left", None)
            elif player_sprite.shooting_down:
                self.shoot("down", None)

    def collision(self, delta_time):

        # collision enemy-player, enemy-enemy and death
        for enemy in self.enemy_list:
            # game over if player is hit
            if arcade.check_for_collision(self.player_sprite, enemy):
                self.player_sprite.number_of_hearts -= 1
                # borrado de todos los enemigos
                self.legia = True
                # vuelta al punto central de la pantalla
                self.player_sprite.respawn()
                if self.player_sprite.number_of_hearts == 0:
                    arcade.pause(1)
                    music = True
                    game_over = GameOver()
                    self.window.show_view(game_over)
                    if music:
                        game_over = arcade.load_sound(music_folder + os.path.sep + "game_over.wav")
                        arcade.play_sound(game_over)
                        return music == False

            # enemy movement
            enemy.movement(self.player_sprite)

            # enemies physics
            self.collision_enemy = arcade.check_for_collision_with_list(enemy, self.enemy_list)
            for i in range(len(self.collision_enemy)):
                self.physics_enemy_list = arcade.PhysicsEngineSimple(self.collision_enemy[i], self.enemy_list)

            # bullet disappears, not creation of enemies and the stop
            if self.movement:
                enemy.speed = 0
                self.max_enemies = len(self.enemy_list)
                if self.dissapear:
                    for bullet in self.bullet_list:
                        bullet.kill()

        # collisions bullet - enemy
        for bullet in self.bullet_list:
            if arcade.check_for_collision_with_list(bullet, self.paredes):
                bullet.kill()
            collision_bullet_enemy = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            # enemy actualization of hearts
            for enemy in collision_bullet_enemy:
                # dissapear
                if self.dissapear:
                    bullet.kill()
                if enemy.number_of_hearts > 0:
                    if self.jeringa1_activa:
                        enemy.number_of_hearts -= 1
                    elif self.jeringa2_activa:
                        enemy.number_of_hearts -= 2
                    elif self.jeringa3_activa:
                        enemy.number_of_hearts -= 3
                if enemy.number_of_hearts <= 0:
                    self.powerUps_drop(enemy, randint(0, 19))
                    enemy.kill()
                    self.score += 1
                    music = True
                    if music:
                        death = arcade.load_sound(sound_folder + os.path.sep + "death.wav")
                        arcade.play_sound(death)
                        return music == False
            collision_bullet_boss = arcade.check_for_collision_with_list(bullet, self.boss_list)
            for boss in collision_bullet_boss:
                bullet.kill()
                if boss.number_of_hearts > 0:
                    boss.number_of_hearts -= 1
                    self.rectangle_right_hearts -= 4.4
                if boss.number_of_hearts == 0:
                    boss.kill()
                    win = Winner()
                    self.window.show_view(win)

        start_the_wave = arcade.check_for_collision_with_list(self.player_sprite, self.bomb_list)
        if start_the_wave and self.space:
            self.bomb.kill()
            self.start = True

        # objetos tienda
        if self.current_room == 6:

            # planta baja
            if self.selling == 0:
                for item in self.tienda.objetos_planta_baja:
                    if arcade.check_for_collision(self.player_sprite, item):
                        if item == self.tienda.botas and item.num_colisiones == 0:
                            if self.player_sprite.money >= item.precio:
                                self.player_sprite.money -= item.precio
                                item.num_colisiones += 1
                                item.recogido = True
                                self.player_sprite.speed = 250
                                item.kill()

            # primera planta
            elif self.selling == 1:
                for item in self.tienda.objetos_planta1:
                    if arcade.check_for_collision(self.player_sprite, item):
                        # jeringa2
                        if item == self.tienda.jeringa2 and item.num_colisiones == 0:
                            if self.player_sprite.money >= item.precio:
                                self.player_sprite.money -= item.precio
                                item.num_colisiones += 1
                                item.recogido = True
                                self.weapon.kill()
                                self.weapon = Weapon(bullet_folder + os.path.sep + "jeringa2.png",
                                                     self.player_sprite.center_x + 15, self.player_sprite.center_y - 5, 90)
                                self.weapon_list.append(self.weapon)
                                self.jeringa1_activa = False
                                self.jeringa3_activa = False
                                self.jeringa2_activa = True
                                item.kill()
                        # botas
                        elif item == self.tienda.botas and item.num_colisiones == 0:
                            if self.player_sprite.money >= item.precio:
                                self.player_sprite.money -= item.precio
                                item.num_colisiones += 1
                                item.recogido = True
                                self.player_sprite.speed = 250
                                item.kill()

            # segunda planta
            elif self.selling == 2:
                for item in self.tienda.objetos_planta2:
                    if arcade.check_for_collision(self.player_sprite, item):
                        # botas
                        if item == self.tienda.botas and item.num_colisiones == 0:
                            if self.player_sprite.money >= item.precio:
                                self.player_sprite.money -= item.precio
                                item.num_colisiones += 1
                                item.recogido = True
                                self.player_sprite.speed = 250
                                item.kill()
                        # jeringa3
                        elif item == self.tienda.jeringa3 and item.num_colisiones == 0:
                            if self.player_sprite.money >= item.precio:
                                self.player_sprite.money -= item.precio
                                item.num_colisiones += 1
                                item.recogido = True
                                self.weapon.kill()
                                self.weapon = Weapon(bullet_folder + os.path.sep + "jeringa3.png",
                                                     self.player_sprite.center_x + 15,
                                                     self.player_sprite.center_y - 5, 90)
                                self.weapon_list.append(self.weapon)
                                self.jeringa1_activa = False
                                self.jeringa3_activa = True
                                self.jeringa2_activa = False
                                item.kill()

            # tercera planta
            elif self.selling == 3:
                for item in self.tienda.objetos_planta3:
                    if arcade.check_for_collision(self.player_sprite, item):
                        if item == self.tienda.corazon and item.num_colisiones == 0:
                            if self.player_sprite.money >= item.precio:
                                self.player_sprite.money -= item.precio
                                item.num_colisiones += 1
                                item.recogido = True
                                self.player_sprite.number_of_hearts += 1
                                item.kill()

        self.powerUps_coins_update(delta_time)
        self.update_boss()

    def powerUps_drop(self, enemy, number):

        if number == 0:
            self.powerUpAguja = PowerUp(powerups_folder + os.path.sep + "powerUpAguja.png", enemy.center_x, enemy.center_y, self.tiempo_vida)
            self.powerUpListAguja.append(self.powerUpAguja)

        elif number == 1:
            self.powerUpTriple = PowerUp(powerups_folder + os.path.sep + "powerUpTriple.png", enemy.center_x, enemy.center_y, self.tiempo_vida)
            self.powerUpListTriple.append(self.powerUpTriple)

        elif number == 2:
            self.powerUpLejia = PowerUp(powerups_folder + os.path.sep + "poweUpLejia.png", enemy.center_x, enemy.center_y, self.tiempo_vida)
            self.powerUpListLejia.append(self.powerUpLejia)

        elif 3 <= number <= 4:
            self.lista_monedas.append(
                Moneda(powerups_folder + os.path.sep + "moneda1.png", 1, enemy.center_x, enemy.center_y, self.tiempo_vida))

        elif number == 5:
            self.lista_monedas.append(
                Moneda(powerups_folder + os.path.sep + "moneda5.png", 5, enemy.center_x, enemy.center_y, self.tiempo_vida))

    def powerUps_coins_update(self, delta_time):

        # powerUp legia
        for powerUpLejia in self.powerUpListLejia:
            powerUpLejia.tiempo_vida -= 1 * delta_time
            if powerUpLejia.tiempo_vida <= 0:
                powerUpLejia.kill()
            elif arcade.check_for_collision_with_list(self.player_sprite, self.powerUpListLejia):
                self.legia = True
                powerUpLejia.kill()

        if self.legia:
            for enemy in self.enemy_list:
                enemy.kill()
                if len(self.enemy_list) == 0:
                    self.legia = False

        # powerUp triple disparo
        for powerUpTriple in self.powerUpListTriple:
            powerUpTriple.tiempo_vida -= 1 * delta_time
            if powerUpTriple.tiempo_vida <= 0:
                powerUpTriple.kill()
            elif arcade.check_for_collision_with_list(self.player_sprite, self.powerUpListTriple):
                self.triple = True
                powerUpTriple.kill()

        if self.triple:
            self.cd_triple += delta_time
            if self.cd_triple > 6:
                self.triple = False
                self.cd_triple = 0

        # powerUp agujas
        for powerUpAguja in self.powerUpListAguja:
            powerUpAguja.tiempo_vida -= 1 * delta_time
            if powerUpAguja.tiempo_vida <= 0:
                powerUpAguja.kill()
            elif arcade.check_for_collision_with_list(self.player_sprite, self.powerUpListAguja):
                powerUpAguja.kill()
                self.dissapear = False

        if not self.dissapear:
            self.cd_dissapear += delta_time
            if self.cd_dissapear > 6:
                self.dissapear = True
                self.cd_dissapear = 0

        for coin in self.lista_monedas:
            coin.tiempo_vida -= 1 * delta_time
            if coin.tiempo_vida <= 0:
                coin.kill()
            elif arcade.check_for_collision(self.player_sprite, coin):
                self.player_sprite.money += coin.valor
                coin.kill()

    def display_vidas_personaje(self):

        i = 0
        for heart in range(self.player_sprite.number_of_hearts):
            arcade.Sprite(sprites_folder + os.path.sep + "protagonista.png", 1, center_x=550 + i, center_y=30).draw()
            i += 20

    def on_update(self, delta_time):
        """ Movement and game logic """  # collisions go here

        if self.pause_done:
            self.reset_things()

        # Counters
        self.spawn_cd += 1
        if self.start:
            self.time -= delta_time
        self.time_quotient = self.time // 1

        # Room updates
        self.room_update()

        # waves
        self.waves()

        # provisional
        self.update_shooting(self.player_sprite)

        for weapon in self.weapon_list:
            weapon.update_self(self.player_sprite, delta_time)

        # update everything
        self.collision(delta_time)
        self.player_list.update()
        self.bullet_list.update()
        self.bullet_boss.update()
        self.enemy_list.update()
        self.bomb_list.update()
        self.physics_enemy_list.update()
        self.powerUpListAguja.update()
        self.powerUpListTriple.update()
        self.powerUpListLejia.update()

    def on_draw(self):
        """
        Render the screen
        """
        arcade.start_render()

        # draw of the map
        # Room entrance
        self.room_draw()

        # contadores
        arcade.draw_text(f"Score: {self.score}", 550, 615, arcade.color.WHITE, 15)
        arcade.draw_text(f"Time wave: {int(self.time_quotient)}", 400, 615, arcade.color.WHITE, 15)
        arcade.draw_text(f": {self.player_sprite.money}", 490, 20, arcade.color.WHITE, 15)

        # dibujar vidas personaje
        self.display_vidas_personaje()

        # dibujar moneda
        arcade.Sprite(powerups_folder + os.path.sep + "moneda1.png", center_x=480, center_y=30).draw()

        # draw all sprites
        self.bomb_list.draw()
        self.powerUpListAguja.draw()
        self.powerUpListTriple.draw()
        self.powerUpListLejia.draw()
        self.lista_monedas.draw()
        self.weapon_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.bullet_boss.draw()
        self.enemy_list.draw()
        self.boss_list.draw()
        self.shop_list.draw()

    def on_key_press(self, key, modifiers):

        # move character
        if key == arcade.key.W:
            self.player_sprite.go_up = True
        if key == arcade.key.A:
            self.player_sprite.go_left = True
        if key == arcade.key.S:
            self.player_sprite.go_down = True
        if key == arcade.key.D:
            self.player_sprite.go_right = True

        # player shooting
        if key == arcade.key.RIGHT:
            if not self.player_sprite.shooting_left and (not self.player_sprite.shooting_up
                                                         and not self.player_sprite.shooting_down):
                self.shoot("right", None)
            self.player_sprite.shooting_right = True
            self.cd = 0
        if key == arcade.key.LEFT:
            if not self.player_sprite.shooting_right and (not self.player_sprite.shooting_up
                                                          and not self.player_sprite.shooting_down):
                self.shoot("left", None)
            self.player_sprite.shooting_left = True
            self.cd = 0
        if key == arcade.key.UP:
            if not self.player_sprite.shooting_left and (not self.player_sprite.shooting_right
                                                         and not self.player_sprite.shooting_down):
                self.shoot("up", None)
            self.player_sprite.shooting_up = True
            self.cd = 0
        if key == arcade.key.DOWN:
            if not self.player_sprite.shooting_left and (not self.player_sprite.shooting_up
                                                         and not self.player_sprite.shooting_right):
                self.shoot("down", None)
            self.player_sprite.shooting_down = True
            self.cd = 0

        if key == arcade.key.SPACE:
            self.space = True

        if key == arcade.key.ESCAPE:
            self.pause_done = True
            pause_view = Pause(self)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.go_up = False
        if key == arcade.key.A:
            self.player_sprite.go_left = False
        if key == arcade.key.S:
            self.player_sprite.go_down = False
        if key == arcade.key.D:
            self.player_sprite.go_right = False

        if key == arcade.key.RIGHT:
            self.player_sprite.shooting_right = False
        if key == arcade.key.LEFT:
            self.player_sprite.shooting_left = False
        if key == arcade.key.UP:
            self.player_sprite.shooting_up = False
        if key == arcade.key.DOWN:
            self.player_sprite.shooting_down = False

        if key == arcade.key.SPACE:
            self.space = False