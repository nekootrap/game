import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Игра"
GRAVITY=1500
DEFAULT_DAMPING=1.0
PLAYER_DAMPING=0.4
PLAYER_FRICTION=1.0
WALL_FRICTION=0.7
DYNAMIC_ITEM_FRICTION=0.6
PLAYER_MASS=2.0
PLAYER_MAX_HORIZONTAL_SPEED=450
PLAYER_MAX_VERTICAL_SPEED=1600

def load_texture_pair(filename):
   return [
       arcade.load_texture(filename),
       arcade.load_texture(filename, flipped_horizontally=True),
   ]

class Person(arcade.AnimatedTimeBasedSprite):
    def __init__(self):
        super().__init__(scale=0.8,)
        self.person_face_direction = 0
        self.run = []
        self.cur_texture = 0
        self.stopp = arcade.load_texture_pair(":resources:images/alien/alienBlue_front.png")
        for i in range(1, 3):
            texture = arcade.load_texture_pair(f":resources:images/alien/alienBlue_walk{i}.png")
            self.run.append(texture)
        self.texture = self.stopp[0]
        
    def update_animation(self, delta_time: float = 1 / 60 ):
        if self.change_x < 0 and self.person_face_direction == 0:
            self.person_face_direction = 1
        elif self.change_x > 0 and self.person_face_direction == 1:
            self.person_face_direction = 0

        if self.change_x == 0:
            self.texture = self.stopp[self.person_face_direction]
            return
        self.texture = self.run[int(self.cur_texture)][self.person_face_direction]
        
        self.cur_texture += 0.2
        if self.cur_texture >= 2:
            self.cur_texture = 0
            
        
        
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.GRAY)
    
        self.wall = arcade.SpriteList()
        for x in range(0, 1200, 90):
            self.ground = arcade.Sprite(":resources:images/tiles/planetMid.png", 0.7)
            self.ground.center_x = x
            self.ground.center_y = 32
            self.wall.append(self.ground)
            
        self.pl = Person()
        self.pl.center_x = 50
        self.pl.center_y = 320
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.pl, gravity_constant=1, walls=self.wall)
        # self.physics_engine = arcade.PymunkPhysicsEngine
        
        self.coin = ":resources:images/items/coinGold.png"
        self.platform = ":resources:images/tiles/planetHalf_mid.png"
        
        self.wall.append(arcade.Sprite(self.platform, center_x=32, center_y=300))
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.pl.change_y = 20
        if key == arcade.key.UP:
            self.pl.change_y = 6
        elif key == arcade.key.LEFT:
            self.pl.change_x = -5
        elif key == arcade.key.RIGHT:
            self.pl.change_x = 5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.pl.change_x = 0
        elif key == arcade.key.UP:
            self.pl.change_y = 0
                
    def setup(self):
        None
                
    def update(self, delta_time: float):
        self.pl.update_animation()
        self.physics_engine.update()
        
    def on_draw(self):
        self.clear()
        self.pl.draw()
        self.wall.draw()
        # arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.bg_layer1)
        
mygame = Game()

arcade.run()