import arcade
import arcade.gui
from arcade.experimental.lights import Light, LightLayer
import random
import math
SCREEN_TITLE = "Игра"

SPRITE_IMAGE_SIZE = 128
SPRITE_SCALING_PLAYER = 0.3
SPRITE_SCALING_TILES = 0.3

SPRITE_SIZE = int(SPRITE_IMAGE_SIZE*SPRITE_SCALING_PLAYER)

SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15

SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT

GRAVITY = 1500
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 1.0

PLAYER_FRICTION = 1.0
WALL_FRICTION = 1
DYNAMIC_ITEM_FRICTION = 0.6

PLAYER_MASS = 2.0

PLAYER_MAX_HORIZONTAL_SPEED = 200
PLAYER_MAX_VERTICAL_SPEED = 1600

PLAYER_JUMP = 7700
PLAYER_MOVE_FORCE_ON_GROUND = 8000

VIEWPORT_MARGIN = 200

PARTICLE_GRAVITY = 0.05
PARTICLE_FADE_RATE = 10
PARTICLE_MIN_SPEED = 2.5
PARTICLE_SPEED_RANGE = 2.5
PARTICLE_COUNT = 20
PARTICLE_RADIUS = 3

PARTICLE_COLORS = [arcade.color.ORANGE,
                   arcade.color.SAFETY_YELLOW,
                   arcade.color.LAVA,
                   arcade.color.PERIDOT,
                   arcade.color.MUSTARD]

PARTICLE_SPARKLE_CHANCE = 0.02

class Particle(arcade.SpriteCircle):
    def __init__(self, my_list):
        color = random.choice(PARTICLE_COLORS)

        super().__init__(PARTICLE_RADIUS, color)
        
        self.normal_texture = self.texture
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

        self.my_alpha = 255

    def update(self):
        """ Update the particle """
        if self.my_alpha <= PARTICLE_FADE_RATE:
            # Исчез, удалить
            self.remove_from_sprite_lists()
        else:
            # Обновлять
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= PARTICLE_GRAVITY

            # Должны ли мы сверкать этим?
            if random.random() <= PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(int(self.width),
                                                          arcade.color.WHITE)
            else:
                self.texture = self.normal_texture

class InstructionView(arcade.View):
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def __init__(self):
        self.is_alive = True
        super().__init__()
        arcade.set_background_color(arcade.color.OLD_HELIOTROPE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",
                                                   anchor_y="center_y",
                                                   child=self.v_box))
        
        start_button = arcade.gui.UIFlatButton(text="Начать игру",width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))
        
        
        start_button.on_click = self.on_click_open
        
        quit_button = arcade.gui.UIFlatButton(text="Выход",width=200)
        self.v_box.add(quit_button)
        
        quit_button.on_click = self.close1
        
    def on_draw(self):
        if self.is_alive:
            self.clear()
            self.manager.draw()
            arcade.draw_text('Инопришеленец',
                            self.window.width/2,
                            start_y=400,
                            color=arcade.color.WHITE,
                            font_size=50,
                            anchor_x="center")
        
    def on_click_open(self,event):
        if self.is_alive:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        
    def close1(self,event):
        self.is_alive = False
        arcade.close_window()
    
        
class GameOverView(arcade.View):
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def __init__(self):
        self.is_alive = True
        super().__init__()
        arcade.set_background_color(arcade.color.OLD_HELIOTROPE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",
                                                   anchor_y="center_y",
                                                   child=self.v_box))
        
        start_over = arcade.gui.UIFlatButton(text="Начать заново",width=200)
        self.v_box.add(start_over.with_space_around(bottom=20))
        
        main_screen = arcade.gui.UIFlatButton(text="Выход",width=200)
        self.v_box.add(main_screen.with_space_around(bottom=20))
        
        
        start_over.on_click = self.on_click_open
        main_screen.on_click = self.close2
        
    def on_draw(self):
        if self.is_alive:
            self.clear()
            self.manager.draw()
            arcade.draw_text('Вы проиграли!',
                         self.window.width/2,
                         start_y=400,
                         color=arcade.color.WHITE,
                         font_size=50,
                         anchor_x="center")
        
    def on_click_open(self,event):
        if self.is_alive:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        
    def close2(self,event):
        self.is_alive = False
        arcade.close_window() 

class GameWinView(arcade.View):
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def __init__(self):
        self.is_alive = True
        super().__init__()
        arcade.set_background_color(arcade.color.OLD_HELIOTROPE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",
                                                   anchor_y="center_y",
                                                   child=self.v_box))
        
        start_over = arcade.gui.UIFlatButton(text="Начать заново",width=200)
        self.v_box.add(start_over.with_space_around(bottom=20))
        
        main_screen = arcade.gui.UIFlatButton(text="Выход",width=200)
        self.v_box.add(main_screen.with_space_around(bottom=20))
        
        
        start_over.on_click = self.on_click_open
        main_screen.on_click = self.close3
        
    def on_draw(self):
        if self.is_alive:
            self.clear()
            self.manager.draw()
            arcade.draw_text('Вы выиграли!',
                            self.window.width/2,
                            start_y=400,
                            color=arcade.color.WHITE,
                            font_size=50,
                            anchor_x="center")
        
    def close3(self,event):
        self.is_alive = False
        arcade.close_window() 
        
    def on_click_open(self,event):
        if self.is_alive:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
    
class PauseView(arcade.View):
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        arcade.set_background_color(arcade.color.OLD_HELIOTROPE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",
                                                   anchor_y="center_y",
                                                   child=self.v_box))
        
        start_over = arcade.gui.UIFlatButton(text="Продолжить",width=200)
        self.v_box.add(start_over.with_space_around(bottom=20))
        
        main_screen = arcade.gui.UIFlatButton(text="Выход",width=200)
        self.v_box.add(main_screen.with_space_around(bottom=20))
        
        
        start_over.on_click = self.on_click_open
        
    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text('Пауза',
                         self.window.width/2,
                         start_y=400,
                         color=arcade.color.WHITE,
                         font_size=50,
                         anchor_x="center") 
        
    def on_click_open(self,event):
        self.window.show_view(self.game_view)
        
class GameView(arcade.View, arcade.Window):
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
    def __init__(self):
        super().__init__()
        self.player = None
        self.player_list = None
        self.physics_engine = None
        self.wall_list = None
        self.coin_list = None
        self.saw_list = None
        self.is_alive = True
        self.camera = None
        self.s = 0
        self.hearts = 3
        self.background = None
        
        self.torch = None
        self.torch_list = None
        
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        
        self.physics_engine = None
        
        self.view_left = 0
        self.view_bottom = 0
        
        self.light_layer = None
        self.player_light = None
        
        self.explosions_list = None
        
    def setup(self):
        self.player_list = arcade.SpriteList
        self.wall_list = arcade.SpriteList
        self.saw_list = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()
        self.background = arcade.SpriteList()
        self.torch_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        
        self.jump = arcade.load_sound(":resources:sounds/jump3.wav")
        self.kill_sound = arcade.load_sound(":resources:sounds/fall1.wav")
        self.coin_sonnd = arcade.load_sound(":resources:sounds/coin5.wav")
        
        self.view_left = 0
        self.view_bottom = 0
        
        radius = 230
        mode = 'soft'
        color = arcade.csscolor.WHITE
        self.player_light = Light(0, 0, radius, color, mode)
        
        self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.light_layer.set_background_color(arcade.color.BRIGHT_LILAC)
            
        self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.light_layer.set_background_color(arcade.color.BRIGHT_LILAC)
        self.light_layer.add(self.player_light)
            
        map_name = ":resources:/tiled_maps/map.json"
        tile_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES)
        
        self.coin_list = tile_map.sprite_lists['Coins']
        self.wall_list = tile_map.sprite_lists['Platforms']
        
        for x in range(-128,2500,128):
            for y in range(-128,1000,128):
                sprite=arcade.Sprite(":resources:images/tiles/planetCenter.png")
                sprite.position=x,y
                self.background.append(sprite)

        self.coin_list.append(arcade.Sprite(":resources:images/items/coinGold.png",
                                            0.3,
                                            center_x=825,
                                            center_y= 250))
        self.coin_list.append(arcade.Sprite(":resources:images/items/coinGold.png",
                                            0.5,
                                            center_x=1850,
                                            center_y= 70))
        
        self.player = arcade.Sprite(":resources:images/alien/alienBlue_front.png",
                                    SPRITE_SCALING_PLAYER,
                                    center_x= 20,
                                    center_y= 200)
        
        self.saw_list.append(arcade.Sprite(":resources:images/enemies/sawHalf.png",
                                           0.3,
                                           center_x=55,
                                           center_y=55))
        self.saw_list.append(arcade.Sprite(":resources:images/enemies/sawHalf.png",
                                           0.3,
                                           center_x=252,
                                           center_y=171))
        self.saw_list.append(arcade.Sprite(":resources:images/enemies/sawHalf.png",
                                           0.3,
                                           center_x=709,
                                           center_y=55))
        self.saw_list.append(arcade.Sprite(":resources:images/enemies/sawHalf.png",
                                           0.3,
                                           center_x=1361,
                                           center_y=55))
        self.saw_list.append(arcade.Sprite(":resources:images/enemies/sawHalf.png",
                                           0.3,
                                           center_x=1535,
                                           center_y=55))
        
        radius_torch = 120
        mode_torch = 'soft'
        color_torch = arcade.color.WHITE
        self.torch_light1 = Light(0, 0, radius_torch, color_torch, mode_torch)
        self.light_layer.add(self.torch_light1)
        
        self.torch_light2 = Light(0, 0, radius_torch, color_torch, mode_torch)
        self.light_layer.add(self.torch_light2)
        
        self.torch_light3 = Light(0, 0, radius_torch, color_torch, mode_torch)
        self.light_layer.add(self.torch_light3)
        
        self.torch1 = arcade.Sprite(":resources:images/tiles/torch2.png",
                                             0.3,
                                             center_x=100,
                                             center_y=70)
        
        self.torch2 = arcade.Sprite(":resources:images/tiles/torch2.png",
                                             0.3,
                                             center_x=1010,
                                             center_y=170)
        
        self.torch3 = arcade.Sprite(":resources:images/tiles/torch2.png",
                                             0.3,
                                             center_x=1500,
                                             center_y=170)
        
        self.torch_list.append(self.torch1)
        self.torch_list.append(self.torch2)
        self.torch_list.append(self.torch3)
        
        damping = DEFAULT_DAMPING
        graviti = (0, -GRAVITY)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping, gravity=graviti)
        
        self.camera = arcade.Camera(self.window.width,self.window.height)
        
        self.physics_engine.add_sprite(self.player,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type='player',
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)
        
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type='wall',
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)
        
        self.physics_engine.add_sprite_list(self.saw_list,
                                            collision_type='saw')

        def saw_hit_handler(spike_sprite, _player_sprite, _arbiter, _space, _data):
            if self.hearts > 1:
                self.hearts -= 1
                coin = self.coin_list
                self.setup()
                self.coin_list = coin
                return
            else:
                self.kill_sound.play()
                self.is_alive = False
                view = GameOverView()
                self.window.show_view(view)

        self.physics_engine.add_collision_handler("saw", "player", post_handler=saw_hit_handler)
        
    def on_key_press(self,key,modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
           self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.UP or key == arcade.key.W:
            self.jump.play()
            if self.physics_engine.is_on_ground(self.player):
                impulse = (0,PLAYER_JUMP)
                self.physics_engine.apply_impulse(self.player,impulse)
            self.up_pressed = True
        if key==arcade.key.ESCAPE:
            pause = PauseView(self)
            self.window.show_view(pause)
            
    def on_key_release(self,key,modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
           self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
    
    def on_update(self,delta_time):
        if self.is_alive: 
        
            self.center_camera_to_player()
            
            self.player_light.position = self.player.position
            self.torch_light1.position = self.torch1.position
            self.torch_light2.position = self.torch2.position
            self.torch_light3.position = self.torch3.position
            
            self.scroll_screen()
            
            self.explosions_list.update()
            
            coins_hit = arcade.check_for_collision_with_list(
                self.player, self.coin_list)
            
            if self.player.center_x < 0:
                sas = GameOverView()
                self.window.show_view(sas)
            
            for coin in coins_hit:
                for i in range(PARTICLE_COUNT):
                    particle = Particle(self.explosions_list)
                    particle.position = coin.position
                    self.explosions_list.append(particle)
                
                self.coin_sonnd.play()
                coin.remove_from_sprite_lists()
                self.s += 1    
                if self.s == 6 :
                    win = GameWinView()
                    self.window.show_view(win)
                    
            if self.left_pressed and not self.right_pressed:
                force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
                self.physics_engine.apply_force(self.player, force)
                self.physics_engine.set_friction(self.player, 0)
                
            elif self.right_pressed and not self.left_pressed:
                force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
                self.physics_engine.apply_force(self.player, force)
                self.physics_engine.set_friction(self.player, 0)
                
            else:
                self.physics_engine.set_friction(self.player, 1.0)
            
        self.physics_engine.step()
        
    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)
        
        if screen_center_x < 0:
            screen_center_x = 0
            
        if screen_center_y < 0:
            screen_center_y = 0
            
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)
        
    def on_resize(self,width,height):
        self.scroll_screen()
        
    def scroll_screen(self):
        
        left_boundary = self.view_left + VIEWPORT_MARGIN
        
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            
        right_boundary = self.view_left + self.window.width - VIEWPORT_MARGIN
        
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            
        top_boundary = self.view_bottom + self.window.height - VIEWPORT_MARGIN
        
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)
        
        arcade.set_viewport(self.view_left,
                            self.window.width + self.view_left,
                            self.view_bottom,
                            self.window.height + self.view_bottom)
        
    def on_draw(self):
        self.clear()
        
        self.camera.use()

        with self.light_layer:
            self.background.draw()
            self.torch_list.draw()
            self.wall_list.draw()
            self.coin_list.draw()
            self.saw_list.draw()
            self.explosions_list.draw()
            self.player.draw()
        
        self.light_layer.draw(ambient_color=arcade.color.BYZANTIUM)
        
        arcade.draw_text(
            f'монеты: {self.s}/6',
            self.camera.position.x + 10,
            10,
            arcade.color.WHITE,
            20
        )
        
        arcade.draw_text(
            f'жизни: {self.hearts}',
            self.camera.position.x + 10,
            535,
            arcade.color.WHITE,
            20
        )
        
window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
start_view = InstructionView()
window.show_view(start_view)
arcade.run()
    
