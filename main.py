import ursina.shaders.screenspace_shaders.ssao
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


class Player(FirstPersonController, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gravity = 1
        self.model = 'cube'
        self.texture = 'samolet_texture.png'
        self.color = color.lime
        self.origin = (0,-0.5,0)
        self.mouse_sensitivity = Vec2(80, 80)
        self.jump_height = 30
        self.speed = 50
        self.double_sided = True
        self.shader = ursina.shaders.lit_with_shadows_shader
        #self.camera_pivot = self.origin

    def jump(self):
        #if not self.grounded:
        #    return
        self.grounded = False
        self.animate_y(self.y + self.jump_height, self.jump_up_duration, resolution=int(1 // time.dt),
                       curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)

    def input(self, key):
        if key == 'space hold':
            self.jump()
        if key == 'space':
            self.jump()
        if key == 'left shift hold':
            self.speed = 100
        else:
            self.speed = 50


class Ground(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scale = Vec3(100,1,40)
        #self.rotation_y = 90
        self.model = 'plane'
        self.texture = 'tex_plane_grad_rot_alpha.png'


        #self.collision = True
        self.position = Vec3(0, 0, 0)
        self.double_sided = True
        self.collider = 'mesh'
        self.alpha = 0.1
        #self.rotation_x = 45
        self.flag = True

        self.shader = ursina.shaders.lit_with_shadows_shader

    def update(self):
        if self.flag:
            self.alpha += 0.001
            if self.alpha > 0.9:
                self.flag = False
        else:
            self.alpha -= 0.001
            if self.alpha < 0.1:
                self.flag = True


app = Ursina()

EditorCamera()
player = Player()

print(camera.z)
#camera.z = -20


ground = Ground()
g1 =duplicate(ground, rotation_x=90, y=20, z=20)
g2 =duplicate(ground, rotation_x=90, y=20, z=-20)
g3 =duplicate(ground, y=40)
#for i in range(1, 10):
#    gr = duplicate(ground, x=i*1000)
tree = Entity(model='low_poly_tree.obj', texture='tex_tree_low_1',position=Vec3(0, 0, 0), scale=Vec3(3,3,3))




#g1 = duplicate(ground,z=-20, rotation_x=120)

sky = Sky(texture='qq.hdr')

from ursina.shaders import lit_with_shadows_shader # you have to apply this shader to enties for them to receive shadows.



DirectionalLight(parent=Entity(), y=-2, z=3, shadows=False)
# Create an Entity for handling pausing an unpausing.
# Make sure to set ignore_paused to True so the pause handler itself can still receive input while the game is paused.
pause_handler = Entity(ignore_paused=True)
pause_text = Text('Пауза', origin=(0,0), scale=2, enabled=False) # Make a Text saying "PAUSED" just to make it clear when it's paused.


'''def update():
    
    if player.y < 0:
        player.y = 0
    if player.z > 19.5:
        player.z = 19.5
    if player.z < -19.5:
        player.z = -19.5
'''

def input(key):
    if key == 'scroll down':
        camera.z += 1
        print(camera.z)
    if key == 'scroll up':
        camera.z -= 1
        print(camera.z)

def pause_handler_input(key):
    if key == 'escape':
        application.paused = not application.paused # Pause/unpause the game.
        pause_text.enabled = application.paused     # Also toggle "PAUSED" graphic.

pause_handler.input = pause_handler_input   # Assign the input function to the pause handler.


app.run()