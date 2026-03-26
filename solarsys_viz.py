"""
Space Simulator CW2
Author:
Lukas Kubinec (Enhanced by AI Assistant)
Controls:
Arrow keys - Camera movement
Mouse wheel - Zoom in-out
Space - Pause / Resume
Click planet names in sidebar to see information
"""

# Import of necessary libraries
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Initial game setup
pygame.init()
pygame.font.init()
text_font = pygame.font.SysFont(pygame.font.get_default_font(), 64)  # Set up of default font for text
info_font = pygame.font.SysFont(pygame.font.get_default_font(), 24)  # Smaller font for info text
clock = pygame.time.Clock()
display = (1024, 768)
viewport = pygame.display.set_mode(display, GL_RGBA | HWSURFACE | DOUBLEBUF | OPENGL)  # Set up of display mode
pygame.display.set_caption("CW2 - Solar system simulator")
pygame.key.set_repeat(30)  # Delay of the key repetition in milliseconds
glMatrixMode(GL_PROJECTION)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glEnable(GL_ALPHA_TEST)
glCullFace(GL_BACK)

# Gameplay variables
active_object = 0                   # 0 = Sun / 1 = Mercury / 2 = Venus / etc.
last_active_object = active_object  # Stores the last active button
all_planetary_objects = []          # Used as a storage for all UI elements
all_button_objects = []             # Used as a storage for all 3D objects
movement_speed_amount = 1.0         # Movement speed
zoom_speed_amount = 1.0             # Zoom speed movement
timePaused = False                  # Used for checking if the game is paused or not
fps = 60.0                          # Frames per second (FPS)
fov = 60.0                          # Camera Field of View (FOV)
delta_time = 60.0 / 1000.0          # Converts milliseconds into seconds
show_info_panel = True              # Toggle info panel visibility
info_panel_width = 280
info_panel_height = 200
info_panel_x = display[0] - info_panel_width - 10
info_panel_y = 10

# Variables for camera movement and Clamps for its maximum values
camera_x, camera_y, camera_z = 0, 0, 0
camera_x_max, camera_y_max, camera_z_min, camera_z_max = 5, 5, -30, 9

# Light settings
glEnable(GL_LIGHTING)  # Enables lighting
glEnable(GL_LIGHT0)  # Enables the first light point
glLight(GL_LIGHT0, GL_POSITION, (0, 0, -0.5))  # Light position
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.25, 0.25, 0.25))  # Ambient light
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8))  # Diffuse light
glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5))  # Specular light
glShadeModel(GL_SMOOTH)  # Smooths out the polygons

# Filepaths for Textures
sun_texture = 'textures/2k_sun.jpg'
mercury_texture = 'textures/2k_mercury.jpg'
venus_texture = 'textures/2k_venus.jpg'
earth_texture = 'textures/2k_earth.jpg'
moon_texture = 'textures/2k_moon.jpg'
mars_texture = 'textures/2k_mars.jpg'
jupiter_texture = 'textures/2k_jupiter.jpg'
saturn_texture = 'textures/2k_saturn.jpg'
uranus_texture = 'textures/2k_uranus.jpg'
neptune_texture = 'textures/2k_neptune.jpg'

# Definition of default colours
gray_color = (0, 100, 100, 255)
dark_gray_color = (0, 80, 80, 255)
green_color = (100, 100, 50, 255)
red_color = (255, 50, 50, 25)
dark_red_color = (255, 25, 100, 255)
info_panel_bg_color = (0, 0, 0, 200)  # Semi-transparent black for info panel
info_text_color = (255, 255, 255, 255)  # White text
info_title_color = (255, 215, 0, 255)  # Gold for titles

# Planet information dictionary
planet_info = {
    0: {
        "name": "Sun",
        "type": "Star",
        "diameter": "1,392,700 km",
        "temperature": "5,500 °C (surface)",
        "gravity": "274 m/s²",
        "description": "The Sun is the star at the center of our Solar System. It contains 99.86% of the system's mass."
    },
    1: {
        "name": "Mercury",
        "type": "Terrestrial Planet",
        "diameter": "4,879 km",
        "distance": "57.9 million km",
        "orbit_period": "88 days",
        "temperature": "430 °C (day) / -180 °C (night)",
        "description": "Mercury is the smallest and fastest planet in our Solar System. It has no atmosphere."
    },
    2: {
        "name": "Venus",
        "type": "Terrestrial Planet",
        "diameter": "12,104 km",
        "distance": "108.2 million km",
        "orbit_period": "225 days",
        "temperature": "462 °C",
        "description": "Venus has a toxic atmosphere and is the hottest planet in our Solar System."
    },
    3: {
        "name": "Earth",
        "type": "Terrestrial Planet",
        "diameter": "12,742 km",
        "distance": "149.6 million km",
        "orbit_period": "365.25 days",
        "moon": "1 (The Moon)",
        "description": "Our home planet, the only place in the universe known to harbor life."
    },
    4: {
        "name": "Mars",
        "type": "Terrestrial Planet",
        "diameter": "6,779 km",
        "distance": "227.9 million km",
        "orbit_period": "687 days",
        "temperature": "-65 °C (average)",
        "description": "The Red Planet has the largest volcano in the Solar System, Olympus Mons."
    },
    5: {
        "name": "Jupiter",
        "type": "Gas Giant",
        "diameter": "139,820 km",
        "distance": "778.5 million km",
        "orbit_period": "11.86 years",
        "moons": "79 known moons",
        "description": "Jupiter is the largest planet in our Solar System and has a Great Red Spot."
    },
    6: {
        "name": "Saturn",
        "type": "Gas Giant",
        "diameter": "116,460 km",
        "distance": "1.43 billion km",
        "orbit_period": "29.46 years",
        "rings": "Yes, prominent ring system",
        "description": "Saturn is famous for its beautiful ring system, made mostly of ice and rock."
    },
    7: {
        "name": "Uranus",
        "type": "Ice Giant",
        "diameter": "50,724 km",
        "distance": "2.87 billion km",
        "orbit_period": "84 years",
        "temperature": "-224 °C",
        "description": "Uranus rotates on its side, making it unique among the planets."
    },
    8: {
        "name": "Neptune",
        "type": "Ice Giant",
        "diameter": "49,244 km",
        "distance": "4.5 billion km",
        "orbit_period": "164.8 years",
        "temperature": "-218 °C",
        "description": "Neptune has the strongest winds in the Solar System, reaching 2,100 km/h."
    }
}

# --- Methods ---
# Function that Quits the program
def quit_program():
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clears the Colour and Depth buffers
    pygame.quit()
    quit()


# Calculation of X/Y coordinates when orbiting around a point
def orbit_centre(xx, yy, centre_x, centre_y, orbit_speed):
    angle = (orbit_speed / 2) * delta_time
    _angle = math.radians(angle)
    x_shift = ((xx - centre_x) * math.cos(_angle) - (yy - centre_y) * math.sin(_angle))
    y_shift = ((xx - centre_x) * math.sin(_angle) + (yy - centre_y) * math.cos(_angle))
    xx = (x_shift * math.cos(_angle) - y_shift * math.sin(_angle))
    yy = (x_shift * math.sin(_angle) + y_shift * math.cos(_angle))
    xx += centre_x
    yy += centre_y
    return angle, xx, yy


# Generation of texture, returns id that is used to apply generated texture for each object individually
def apply_texture(texture_image, texture_data):
    texture_id = glGenTextures(1)  # Generates a new texture id
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    # applying a texture to an object
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_image.get_width(),
                 texture_image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    return texture_id


# Generation of 2D texture, returns id that is used to apply generated texture for each object individually
def apply_two_d_texture(texture_image, texture_data):
    texture_id = glGenTextures(1)  # Generates a new texture id
    glActiveTexture(GL_TEXTURE0)  # Activates texture n. 0
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Binds the texture ID to GL_TEXTURE_2D - next operations apply to this texture
    # Texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)  # Scaling of texture when zooming in/out
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)  # Scaling of texture when zooming in/out
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)  # Texture repeats
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # Texture repeats
    # applying a texture to an object
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_image.width, texture_image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                 texture_data)
    return texture_id


# Draw 2D info panel using OpenGL (as a billboard)
def draw_info_panel(cam_x, cam_y, cam_z):
    if not show_info_panel:
        return

    # Get info for current planet
    info = planet_info.get(active_object, planet_info[0])

    # Calculate screen-aligned position for the info panel
    # Position it in the top-right corner relative to the camera
    panel_x = cam_x + 6  # Right side
    panel_y = cam_y + 4.5  # Top
    panel_z = -cam_z - 5

    # Draw the panel background (a quad)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)

    # Panel dimensions in world units
    width = 4.5
    height = 3.2

    # Draw panel background
    glColor4f(0, 0, 0, 0.8)
    glBegin(GL_QUADS)
    glVertex3f(panel_x, panel_y, panel_z)
    glVertex3f(panel_x + width, panel_y, panel_z)
    glVertex3f(panel_x + width, panel_y - height, panel_z)
    glVertex3f(panel_x, panel_y - height, panel_z)
    glEnd()

    # Draw border
    glColor4f(1, 0.8, 0, 0.8)
    glBegin(GL_LINE_LOOP)
    glVertex3f(panel_x, panel_y, panel_z)
    glVertex3f(panel_x + width, panel_y, panel_z)
    glVertex3f(panel_x + width, panel_y - height, panel_z)
    glVertex3f(panel_x, panel_y - height, panel_z)
    glEnd()

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)


# Function to render 2D text overlay using Pygame (simpler for text)
def render_pygame_text_overlay():
    if not show_info_panel:
        return

    # Create a temporary surface for text overlay
    overlay = pygame.Surface((info_panel_width, info_panel_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent background

    # Get info for current planet
    info = planet_info.get(active_object, planet_info[0])

    # Render title
    title = info_font.render(info["name"], True, (255, 215, 0))
    overlay.blit(title, (10, 10))

    # Render separator line
    pygame.draw.line(overlay, (255, 215, 0), (10, 35), (info_panel_width - 10, 35), 2)

    # Render planet info with proper formatting
    y_offset = 45
    line_height = 22

    # Skip the name (already displayed as title)
    for key, value in info.items():
        if key == "name" or key == "description":
            continue
        # Format key nicely
        formatted_key = key.replace("_", " ").title()
        text_line = f"{formatted_key}: {value}"
        rendered_text = info_font.render(text_line, True, (255, 255, 255))
        overlay.blit(rendered_text, (10, y_offset))
        y_offset += line_height

    # Render description (wrap text)
    y_offset += 5
    description = info["description"]
    words = description.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if info_font.size(test_line)[0] < info_panel_width - 20:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        rendered_text = info_font.render(line, True, (200, 200, 200))
        overlay.blit(rendered_text, (10, y_offset))
        y_offset += line_height

    # Blit the overlay onto the screen (this is Pygame surface, not OpenGL)
    # Since we're using OpenGL, we need to convert this surface to a texture
    # For simplicity, we'll draw directly using OpenGL with a texture


# Better approach: Create a texture for the info panel
info_panel_texture = None
info_panel_needs_update = True


def create_info_panel_texture():
    """Create a texture containing the current planet information"""
    global info_panel_texture, info_panel_needs_update

    if not info_panel_needs_update:
        return info_panel_texture

    # Create a Pygame surface for the info panel
    surface = pygame.Surface((info_panel_width, info_panel_height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 200))

    # Get info for current planet
    info = planet_info.get(active_object, planet_info[0])

    # Render title
    title_font = pygame.font.SysFont(pygame.font.get_default_font(), 28)
    title_text = title_font.render(info["name"], True, (255, 215, 0))
    surface.blit(title_text, (10, 10))

    # Render separator line
    pygame.draw.line(surface, (255, 215, 0), (10, 45), (info_panel_width - 10, 45), 2)

    # Render planet info
    y_offset = 55
    line_height = 22

    for key, value in info.items():
        if key == "name" or key == "description":
            continue
        formatted_key = key.replace("_", " ").title()
        text_line = f"{formatted_key}: {value}"
        rendered_text = info_font.render(text_line, True, (255, 255, 255))
        surface.blit(rendered_text, (10, y_offset))
        y_offset += line_height

    # Render description with word wrapping
    y_offset += 5
    description = info["description"]
    words = description.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if info_font.size(test_line)[0] < info_panel_width - 20:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        rendered_text = info_font.render(line, True, (200, 200, 200))
        surface.blit(rendered_text, (10, y_offset))
        y_offset += line_height

    # Convert surface to texture
    if info_panel_texture is not None:
        glDeleteTextures([info_panel_texture])

    texture_data = pygame.image.tobytes(surface, "RGBA", True)
    info_panel_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, info_panel_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, info_panel_width, info_panel_height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    info_panel_needs_update = False
    return info_panel_texture


def draw_info_panel_textured(cam_x, cam_y, cam_z):
    """Draw the info panel as a textured quad"""
    if not show_info_panel:
        return

    texture_id = create_info_panel_texture()

    # Position panel at top-right corner relative to camera
    panel_x = cam_x + 5.2  # Right side
    panel_y = cam_y + 4.2  # Top
    panel_z = -cam_z - 4

    # Panel dimensions in world units (maintain aspect ratio)
    width = 3.8
    height = 2.8

    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glColor3f(1, 1, 1)  # White color to show texture correctly

    glBegin(GL_QUADS)
    # Top-left
    glTexCoord2f(0, 0)
    glVertex3f(panel_x, panel_y, panel_z)
    # Top-right
    glTexCoord2f(1, 0)
    glVertex3f(panel_x + width, panel_y, panel_z)
    # Bottom-right
    glTexCoord2f(1, 1)
    glVertex3f(panel_x + width, panel_y - height, panel_z)
    # Bottom-left
    glTexCoord2f(0, 1)
    glVertex3f(panel_x, panel_y - height, panel_z)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)


# --- Classes ---
# Creation of celestial objects - Sun, Planets and Moons
class SolarObject:
    def __init__(self, planet_texture, radius, slices, stacks, distance, orbit_speed, has_moon, _moon_texture):
        # Textures
        self.texture_filename = planet_texture
        self.texture_image = pygame.image.load(self.texture_filename)
        self.texture_data = pygame.image.tobytes(self.texture_image, "RGBA", False)
        self.planet_texture_id = apply_texture(self.texture_image, self.texture_data)  # Applies texture
        # Physical attributes
        self.pos_x, self.pos_y = distance, 0  # Initial position
        self.distance = distance
        self.radius = radius  # Size of object
        self.slices, self.stacks = slices, stacks  # Attributes of the sphere object
        self.planet_orbit_angle = 0
        self.planet_rotation_angle = 0
        self.orbit_speed = orbit_speed
        # Moon attributes
        self.has_moon = has_moon
        if has_moon:
            self.moon_texture = _moon_texture
            self.moon_texture_image = pygame.image.load(self.moon_texture)
            self.moon_texture_data = pygame.image.tobytes(self.moon_texture_image, "RGBA", False)
            self.moon_radius = 0.7
            self.moon_orbit_angle = 0
            self.moon_rotation_angle = 0
            self.moon_speed = 10
            self.moon_distance = 2
            # Initial position
            self.moon_x = ((
                                   (self.moon_distance + self.pos_x) * math.cos(self.moon_orbit_angle) - self.pos_y * math.sin(
                               self.moon_orbit_angle)))
            self.moon_y = (
                    (self.moon_distance + self.pos_x) * math.sin(self.moon_orbit_angle) + self.pos_y * math.cos(self.moon_orbit_angle))
            self.moon_texture_id = apply_texture(self.moon_texture_image, self.moon_texture_data)  # Applies moon texture

    def get_pos(self):
        return self.pos_x, self.pos_y

    def draw_model(self, radius, angle, xx, yy, rotation_angle):
        glEnable(GL_TEXTURE_2D)
        for i in range(self.stacks):
            # Looping through latitude angles
            lat0 = math.pi * (-0.5 + i / self.stacks)
            lat1 = math.pi * (-0.5 + (i + 1) / self.stacks)
            # Vertice positions
            sin_lat0 = math.sin(lat0)
            cos_lat0 = math.cos(lat0)
            sin_lat1 = math.sin(lat1)
            cos_lat1 = math.cos(lat1)
            glBegin(GL_TRIANGLE_STRIP)
            for j in range(self.slices + 1):
                # Longitudes, with dynamic sphere rotation
                lng = 2.0 * math.pi * j / self.slices + (angle + rotation_angle / 5)
                sin_lng = math.sin(lng)
                cos_lng = math.cos(lng)
                # Calculation of coordinates
                x0 = xx + cos_lng * cos_lat0
                y0 = yy + sin_lng * cos_lat0
                z0 = sin_lat0
                # Calculation of coordinates
                x1 = xx + cos_lng * cos_lat1
                y1 = yy + sin_lng * cos_lat1
                z1 = sin_lat1
                # Adjusting Normals used for light/shade characteristics
                glNormal3f(x0, y0, z0)
                glTexCoord2f(j / self.slices, i / self.stacks)
                glVertex3f(radius * x0, radius * y0, radius * z0)
                # Adjusting Normals used for light/shade characteristics
                glNormal3f(x1, y1, z1)
                glTexCoord2f(j / self.slices, (i + 1) / self.stacks)
                glVertex3f(radius * x1, radius * y1, radius * z1)
            glEnd()
        glDisable(GL_TEXTURE_2D)

    def draw_moon(self):
        glEnable(GL_LIGHTING)
        self.moon_orbit_angle, self.moon_x, self.moon_y = orbit_centre(self.moon_x, self.moon_y,
                                                                       (self.pos_x + self.radius / 2),
                                                                       (self.pos_y + self.radius / 2), self.moon_speed)
        self.moon_rotation_angle += 2 * delta_time
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.moon_texture_id)
        self.draw_model(self.moon_radius, self.moon_orbit_angle, self.moon_x, self.moon_y, self.moon_rotation_angle)

    def draw_planet(self):
        if self.pos_x == 0:
            # Checks if the generated object is in the centre (SUN)
            glDisable(GL_LIGHTING)  # Disables lighting when drawing Sun
        else:
            # Enables lighting for objects other than Sun
            glEnable(GL_LIGHTING)  # Enables lighting
            self.planet_orbit_angle, self.pos_x, self.pos_y = orbit_centre(self.pos_x, self.pos_y, 0, 0,
                                                                           self.orbit_speed)
        self.planet_rotation_angle += 1 * delta_time
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.planet_texture_id)
        self.draw_model(self.radius, self.planet_orbit_angle, self.pos_x, self.pos_y, self.planet_rotation_angle)
        if self.has_moon:
            self.draw_moon()


# User Interface class
class UIButton:
    def __init__(self, screen_x, screen_y, title, button_x, button_y, button_id):
        # Set up of the coordinates
        self.x = screen_x
        self.y = screen_y
        self.z = 0
        # Values that only hold the offset
        self._x = screen_x
        self._y = screen_y
        # Set up of Title
        self.title = title
        self.ui_button_rect = pygame.Rect((0, 0), (200, 200))
        # Storage of position of buttons on screen
        self.button_x = button_x
        self.button_y = button_y
        # Set up of button colours
        if button_id == -1:
            # Colour scheme for Quit button
            self.idle_colour = dark_red_color
            self.hover_colour = red_color
        else:
            # Colour scheme for Planetary buttons
            if button_id % 2:
                self.idle_colour = gray_color
            else:
                self.idle_colour = dark_gray_color
            self.hover_colour = green_color
        # Sets the draw color to normal state
        self.draw_colour = self.idle_colour
        # Button ID
        self.button_id = button_id
        self._texture_data = None
        self.idle_texture = self.prepare_text_texture(self.idle_colour, self.title)  # Prepares the Idle texture
        self.hover_texture = self.prepare_text_texture(self.hover_colour, self.title)  # Prepares the Idle texture
        self._texture_id = self.idle_texture

    def check_mouse_clicked_location(self, _active_object):
        # Checks if the mouse is located within the button position
        if self.button_x < pygame.mouse.get_pos()[0] < self.button_x + 70:
            if self.button_y < pygame.mouse.get_pos()[1] < self.button_y + 60:
                global info_panel_needs_update
                info_panel_needs_update = True  # Update info panel when planet changes
                _active_object = self.button_id
        return _active_object

    def check_mouse_hover_location(self):
        # Checks if the mouse is located within the button position
        if self.button_x < pygame.mouse.get_pos()[0] < self.button_x + 70:
            if self.button_y < pygame.mouse.get_pos()[1] < self.button_y + 60:
                # Displays hover texture
                self._texture_id = self.hover_texture
            else:
                self._texture_id = self.idle_texture
        else:
            self._texture_id = self.idle_texture

    def prepare_text_texture(self, colour, text):
        # Draws the pygame graphical elements onto a surface that then gets transformed into a texture
        ui_button_text = text_font.render(text, True, (255, 255, 255, 200))
        ui_button_surface = pygame.Surface(self.ui_button_rect.size, pygame.SRCALPHA)
        ui_button_surface.fill(colour)
        ui_button_surface.blit(ui_button_text, self.ui_button_rect.midleft)
        # Conversion of pygame draw into OpenGL texture
        self._texture_data = pygame.image.tobytes(ui_button_surface, "RGBA", True)
        _texture_id = apply_two_d_texture(self.ui_button_rect, self._texture_data)  # Converts image into usable texture data
        return _texture_id

    def draw(self, cam_x, cam_y, cam_z):
        # Update the coordinates
        self.x = cam_x + self._x
        self.y = cam_y + self._y
        self.z = -cam_z

        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self._texture_id)  # Applies texture to drawn object

        # Begin draw
        glBegin(GL_QUADS)
        # Left Top
        glTexCoord2f(0, 0)
        glVertex3f(self.x, self.y, self.z + 10)
        # Right Top
        glTexCoord2f(1, 0)
        glVertex3f(self.x + 1.0, self.y, self.z + 10)
        # Right Bottom
        glTexCoord2f(1, 1)
        glVertex3f(self.x + 1.0, self.y + 1.0, self.z + 10)
        # Left Bottom
        glTexCoord2f(0, 1)
        glVertex3f(self.x, self.y + 1.0, self.z + 10)

        # End of draw method
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)


# Initialisation of objects
# Planets (https://planetfacts.org/orbital-speed-of-planets-in-order/)
model_slices, model_stacks = 24, 12
Sun = SolarObject(sun_texture, 2.0, model_slices, model_stacks, 0, 0.0, False, None)
all_planetary_objects.append(Sun)
Mercury = SolarObject(mercury_texture, 0.9, model_slices, model_stacks, 4, 4.787, False, None)
all_planetary_objects.append(Mercury)
Venus = SolarObject(venus_texture, 1.0, model_slices, model_stacks, 7, 3.502, False, None)
all_planetary_objects.append(Venus)
Earth = SolarObject(earth_texture, 1.0, model_slices, model_stacks, 12, 2.978, True, moon_texture)
all_planetary_objects.append(Earth)
Mars = SolarObject(mars_texture, 0.95, model_slices, model_stacks, 18, 2.4077, False, None)
all_planetary_objects.append(Mars)
Jupiter = SolarObject(jupiter_texture, 1.15, model_slices, model_stacks, 21, 1.307, False, None)
all_planetary_objects.append(Jupiter)
Saturn = SolarObject(saturn_texture, 1.15, model_slices, model_stacks, 25, 0.969, False, None)
all_planetary_objects.append(Saturn)
Uranus = SolarObject(uranus_texture, 1.1, model_slices, model_stacks, 30, 0.681, False, None)
all_planetary_objects.append(Uranus)
Neptune = SolarObject(neptune_texture, 1.1, model_slices, model_stacks, 35, 0.543, False, None)
all_planetary_objects.append(Neptune)

# UI buttons
# Planetary objects buttons
UI_button_sun = UIButton(+6, +4, "Sun", 910, 50, 0)
all_button_objects.append(UI_button_sun)
UI_button_mercury = UIButton(+6, +3, "Mercury", 910, 124, 1)
all_button_objects.append(UI_button_mercury)
UI_button_venus = UIButton(+6, +2, "Venus", 910, 196, 2)
all_button_objects.append(UI_button_venus)
UI_button_earth = UIButton(+6, +1, "Earth", 910, 263, 3)
all_button_objects.append(UI_button_earth)
UI_button_mars = UIButton(+6, +0, "Mars", 910, 327, 4)
all_button_objects.append(UI_button_mars)
UI_button_jupiter = UIButton(+6, -1, "Jupiter", 910, 398, 5)
all_button_objects.append(UI_button_jupiter)
UI_button_saturn = UIButton(+6, -2, "Saturn", 910, 465, 6)
all_button_objects.append(UI_button_saturn)
UI_button_uranus = UIButton(+6, -3, "Uranus", 910, 527, 7)
all_button_objects.append(UI_button_uranus)
UI_button_neptune = UIButton(+6, -4, "Neptune", 910, 600, 8)
all_button_objects.append(UI_button_neptune)
# Other buttons
UI_button_quit = UIButton(+6, -5, "Quit", 910, 660, -1)
all_button_objects.append(UI_button_quit)

# Game loop
isRunning = True
while isRunning:
    clock.tick(fps)  # Locks the framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_program()

        if event.type == pygame.KEYDOWN:
            # Camera movement
            if event.key == pygame.K_LEFT and camera_x > -camera_x_max:
                camera_x -= movement_speed_amount
            if event.key == pygame.K_RIGHT and camera_x < camera_x_max:
                camera_x += movement_speed_amount
            if event.key == pygame.K_UP and camera_y < camera_y_max:
                camera_y += movement_speed_amount
            if event.key == pygame.K_DOWN and camera_y > -camera_y_max:
                camera_y -= movement_speed_amount
            if event.key == pygame.K_w:
                camera_x = camera_x * math.cos(0.5) + camera_y * math.sin(0.5)
                camera_y = camera_x * math.cos(0.5) - camera_y * math.sin(0.5)

        if event.type == pygame.MOUSEWHEEL:
            # Zoom in/out
            if event.y == 1 and camera_z < camera_z_max:
                camera_z += zoom_speed_amount  # Zoom in
            if event.y == -1 and camera_z > camera_z_min:
                camera_z -= zoom_speed_amount  # Zoom out

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check for interactions with UI buttons
            if event.button == 1:
                for button in all_button_objects:
                    last_active_object = active_object
                    new_active = button.check_mouse_clicked_location(active_object)
                    if new_active is not None:
                        active_object = new_active
                        camera_x, camera_y = 0, 0
                    # Check for Quit button
                    if active_object == -1:
                        quit_program()  # Quits the program

        if event.type == pygame.MOUSEMOTION:
            # Check for mouse movements
            for button in all_button_objects:
                button.check_mouse_hover_location()

        if event.type == pygame.KEYUP:
            # Simulation pause/unpause
            if event.key == pygame.K_SPACE:
                if timePaused:
                    delta_time = 60 / 1000.0  # Converts milliseconds into seconds
                    timePaused = False
                else:
                    delta_time = 0
                    timePaused = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clears the Colour and Depth buffers
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, (display[0] / display[1]), 0.01,
                   100.0)  # set up the projection, camera points and looks in the negative z axis direction
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Getting location of the active object
    active_object_pos = all_planetary_objects[active_object].get_pos()
    # Following active object
    gluLookAt(camera_x + active_object_pos[0], camera_y + active_object_pos[1], 20 - camera_z,
              camera_x + active_object_pos[0], camera_y + active_object_pos[1], camera_z, 0, 1, 0)

    glPushMatrix()  # The current OpenGL matrix is pushed down by one

    # Drawing UI
    for button in all_button_objects:
        button.draw(camera_x + active_object_pos[0], camera_y + active_object_pos[1], camera_z)

    # Draw info panel with planet information
    draw_info_panel_textured(camera_x + active_object_pos[0], camera_y + active_object_pos[1], camera_z)

    # Drawing planets
    for planetary_object in all_planetary_objects:
        planetary_object.draw_planet()

    glPopMatrix()  # restore previous transformation
    pygame.display.flip()
    pygame.display.set_caption("CW2 - Solar system simulator | FPS:" + str(round(clock.get_fps())))
