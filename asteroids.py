import pygame
import time
import sys
import math
import random

VERSION = "0.0.4"
DEBUG = False

CL_BLACK = (0, 0, 0)
CL_WHITE = (255, 255, 255)
CL_LIGHT_GRAY = (200, 200, 200)
CL_DARK_GRAY = (50, 50, 50)

DISPLAY = (1000, 800)
DEFAULT_FONT_SIZE = 20

class Screen:
    def __init__(self) -> None:
        self.width = DISPLAY[0]
        self.height = DISPLAY[1]
        
        self.screen = pygame.display.set_mode(DISPLAY)
        pygame.display.set_caption(f"Asteroids - v{VERSION}")
        
        self.player = Player(self.screen)
        self.player_bullets = []
        self.asteroids = []
        self.saucers = []
        self.saucer_bullets = []
        
    def run(self):
        while True:
            for event in pygame.event.get():
                #== QUIT ==#
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                #== MOVE ==# 
                elif event.type == pygame.MOUSEMOTION:
                    self.player.rotate(degrees=self.player.get_angle(event.pos))
                    
                #== KEY ==#
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player_bullets.append(Bullet(self.player.direction, self.player.tip, self.screen))
                    
                        
                    elif event.key == pygame.K_ESCAPE:
                        direction = random.randint(0, 360)
                        if direction in range(0, 90):
                            start = (0, random.randint(0, self.height))
                        elif direction in range(90, 180):
                            start = (random.randint(0, self.width), self.height)
                        elif direction in range(180, 270):
                            start = (self.width, random.randint(0, self.height))
                        else:
                            start = (random.randint(0, self.width), 0)
                            
                        direction -= 45
                        size = random.choice(["L", "M", "S"])
                        self.asteroids.append(Asteroid(direction, start, self.screen, size))
                    
                    else:
                        self.player.move(event_key=event.key)
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        pass
                    else:
                        self.player.move(stop=event.key)
                    
            self.update()
            
            
    def update(self):
        self.screen.fill(CL_BLACK)
        
        self.player.update()
        
        for bullet in self.player_bullets:
            position = bullet.get_position()
            
            if position[0] < 0 or position[0] > self.width:
                self.player_bullets.remove(bullet)
                del bullet
                continue
            elif position[1] < 0 or position[1] > self.height:
                self.player_bullets.remove(bullet)
                del bullet
                continue
            
            bullet.update()
        for asteroid in self.asteroids:
            radius = asteroid.get_radius()
            position = asteroid.get_position()
            
            if position[0] < -radius or position[0] > self.width+radius:
                self.asteroids.remove(asteroid)
                del asteroid
                continue
            elif position[1] < -radius or position[1] > self.height+radius:
                self.asteroids.remove(asteroid)
                del asteroid
                continue
            
            asteroid.update()
            
        
        for point in self.player.get_points():
            for asteroid in self.asteroids:
                if asteroid.collides_with(point):
                    self.asteroids.remove(asteroid)
                    del asteroid
                    self.player.die()
                    print(self.player.lives)
                    break
            
        for player_bullet in self.player_bullets:
            bullet_position = player_bullet.get_position()
            
            for asteroid in self.asteroids:
                if asteroid.collides_with(bullet_position):
                    self.player_bullets.remove(player_bullet)
                    
                    astedoid_size = asteroid.get_size()
                    asteroid_position = asteroid.get_position()
                    asteroid_direction = asteroid.get_direction()
                    new_direction_1 = asteroid_direction + 45
                    new_direction_2 = asteroid_direction - 45
                    if astedoid_size == 10:
                        self.asteroids.append(Asteroid(new_direction_1, asteroid_position, self.screen, "M"))
                        self.asteroids.append(Asteroid(new_direction_2, asteroid_position, self.screen, "M"))                    
                    elif astedoid_size == 8:
                        self.asteroids.append(Asteroid(new_direction_1, asteroid_position, self.screen, "S"))
                        self.asteroids.append(Asteroid(new_direction_2, asteroid_position, self.screen, "S"))
                    
                    self.asteroids.remove(asteroid)
                    
        
        pygame.display.update()
        
        
class Player:
    def __init__(self, screen, lives=3) -> None:
        self.screen = screen
        
        self.direction = math.radians(0)
        self.position = (self.screen.get_width()/2, self.screen.get_height()/2)
        self.tip = 0
        self.points = []
        
        self.speed = 0.1
        self.velocity = [0, 0]
        self.last_key = [None, None]
        
        self.score = 0
        self.lives = lives
        
        self.tip_length = 20
        self.wing_length = 40
        self.back_depth = 30
        
        self.tip_angle = math.radians(45) /2
        
        self.tip = (self.position[0] + self.tip_length, self.position[1])
        
        right_cos = math.cos( self.tip_angle )
        right_sin = math.sin( self.tip_angle )
        left_cos = math.cos( - self.tip_angle )
        left_sin = math.sin( - self.tip_angle )
        right_wing = (self.tip[0] - self.wing_length*right_cos, self.tip[1] + self.wing_length*right_sin)
        left_wing = (self.tip[0] - self.wing_length*left_cos, self.tip[1] + self.wing_length*left_sin)

        right_back = (self.tip[0] - self.back_depth*right_cos, self.tip[1] + self.back_depth*right_sin)
        left_back = (self.tip[0] - self.back_depth*left_cos, self.tip[1] + self.back_depth*left_sin)
        
        self.points.append(self.tip)
        self.points.append(right_wing)
        self.points.append(right_back)
        self.points.append(left_back)
        self.points.append(left_wing)
        pygame.draw.polygon(self.screen, CL_WHITE, self.points, 2)
        
        
    def _draw(self):
        pygame.draw.polygon(self.screen, CL_WHITE, self.points, 2)
        
    def update(self):
        delta_x = self.velocity[0]
        delta_y = self.velocity[1]
        
        if self.position[0] < 0:
            delta_x += self.screen.get_width()
        elif self.position[0] > DISPLAY[0]:
            delta_x -= self.screen.get_width()
        if self.position[1] < 0:
            delta_y += self.screen.get_height()
        elif self.position[1] > DISPLAY[1]:
            delta_y -= self.screen.get_height()
            
        self.position = (self.position[0] + delta_x, self.position[1] + delta_y)
        for i, point in enumerate(self.points):
            self.points[i] = (point[0] + delta_x, point[1] + delta_y)
        self.tip = self.points[0]
        
        self._draw()
        
    def rotate(self, degrees=None, radians=None):
        if degrees is not None:
            self.direction = math.radians(degrees)
        else:
            self.direction = radians
        
        self.tip = (self.position[0] + self.tip_length*math.cos(self.direction), self.position[1] - self.tip_length*math.sin(self.direction))
        right_cos = math.cos( self.direction + self.tip_angle )
        right_sin = math.sin( self.direction + self.tip_angle )
        left_cos = math.cos( self.direction - self.tip_angle )
        left_sin = math.sin( self.direction - self.tip_angle )
        
        right_wing = (self.tip[0] - self.wing_length*right_cos, self.tip[1] + self.wing_length*right_sin)
        left_wing = (self.tip[0] - self.wing_length*left_cos, self.tip[1] + self.wing_length*left_sin)

        right_back = (self.tip[0] - self.back_depth*right_cos, self.tip[1] + self.back_depth*right_sin)
        left_back = (self.tip[0] - self.back_depth*left_cos, self.tip[1] + self.back_depth*left_sin)
        
        self.points = []
        self.points.append(self.tip)
        self.points.append(right_wing)
        self.points.append(right_back)
        self.points.append(left_back)
        self.points.append(left_wing)
        self.update()
    
    def get_angle(self, coordinate):
        delta_x = coordinate[0] - self.position[0]
        delta_y = -(coordinate[1] - self.position[1])
        
        if delta_x == 0 or delta_y == 0:
            if delta_x == 0:
                return 90 if delta_y > 0 else 270
            else:
                return 0 if delta_x > 0 else 180
        
        return math.degrees(math.atan2(delta_y, delta_x))
    
    def move(self, event_key=None, stop=None):
        # directions = ["U", "D", "L", "R"]
        
        if event_key is not None:
            if event_key == pygame.K_w:
                self.last_key[1] = pygame.K_w
            elif event_key == pygame.K_s:
                self.last_key[1] = pygame.K_s
            elif event_key == pygame.K_d:
                self.last_key[0] = pygame.K_d
            elif event_key == pygame.K_a:
                self.last_key[0] = pygame.K_a
        elif stop is not None:
            if stop == self.last_key[0]:
                self.last_key[0] = None
            elif stop == self.last_key[1]:
                self.last_key[1] = None
        else:
            return 
        
        for key in self.last_key:
            if event_key == pygame.K_w:
                self.velocity[1] -= self.speed
            elif event_key == pygame.K_s:
                self.velocity[1] += self.speed
            elif event_key == pygame.K_d:
                self.velocity[0] += self.speed
            elif event_key == pygame.K_a:
                self.velocity[0] -= self.speed
        
        if self.last_key[0] is None:
           self.velocity[0] = 0
        if self.last_key[1] is None:
            self.velocity[1] = 0 
        
        self.update()
        
    def get_points(self):
        return self.points
    
    def reset(self):
        self.position = (DISPLAY[0]/2, DISPLAY[1]/2)
        
        self.tip = (self.position[0] + self.tip_length, self.position[1])
        
        right_cos = math.cos( self.tip_angle )
        right_sin = math.sin( self.tip_angle )
        left_cos = math.cos( - self.tip_angle )
        left_sin = math.sin( - self.tip_angle )
        right_wing = (self.tip[0] - self.wing_length*right_cos, self.tip[1] + self.wing_length*right_sin)
        left_wing = (self.tip[0] - self.wing_length*left_cos, self.tip[1] + self.wing_length*left_sin)

        right_back = (self.tip[0] - self.back_depth*right_cos, self.tip[1] + self.back_depth*right_sin)
        left_back = (self.tip[0] - self.back_depth*left_cos, self.tip[1] + self.back_depth*left_sin)
        
        self.points.append(self.tip)
        self.points.append(right_wing)
        self.points.append(right_back)
        self.points.append(left_back)
        self.points.append(left_wing)
        pygame.draw.polygon(self.screen, CL_WHITE, self.points, 2)
        
    def die(self):
        print("die")
        
        self.lives -= 1
        
        if self.lives == 0:
            print("end game")
            pygame.quit()
            sys.exit()
            
        self.__init__(self.screen, self.lives)
        time.sleep(1)
        
        
        
        
class Bullet:
    def __init__(self, direction, start, screen):
        self.direction = direction
        self.position = start
        
        self.velocity = 0.2
        self.delta_x = self.velocity * math.cos(self.direction)
        self.delta_y = self.velocity * math.sin(self.direction)
        
        self.screen = screen
        self.radius = 4
        
    def update(self):
        self.position = (self.position[0] + self.delta_x, self.position[1] - self.delta_y)
        pygame.draw.circle(self.screen, CL_WHITE, self.position, self.radius)
        
    def get_position(self):
        return self.position
    
    def get_radius(self):
        return self.radius
    
class Asteroid():
    def __init__(self, direction, start, screen, size):
        self.screen = screen
        self.direction = math.radians(direction)
        self.position = start
        
        self.velocity = 0.1  
        self.delta_x = self.velocity * math.cos(self.direction)
        self.delta_y = self.velocity * math.sin(self.direction)
        self.corners = []
        
        if size == "L":
            self.corner_count = 10
            self.radius = 40
                
        elif size == "M":
            self.corner_count = 8
            self.radius = 35
            
        elif size == "S":
            self.corner_count = 6
            self.radius = 25
        
        
        change = 360/(self.corner_count+1)
        for corner in range(self.corner_count):
            distance = random.randint(self.radius-5, self.radius+5)
            angle = corner*change + random.randint(0, int(change))
            
            d_x = distance * math.cos(math.radians(angle))
            d_y = distance * math.sin(math.radians(angle))
            
            self.corners.append((d_x, d_y))
            
    def update(self):
        self.position = (self.position[0] + self.delta_x, self.position[1] - self.delta_y)
        self._draw()
        
    def _draw(self):
        polygon = [(self.position[0]+corner[0], self.position[1]+corner[1]) for corner in self.corners]
        pygame.draw.polygon(self.screen, CL_WHITE, polygon, 2)
        
    def get_position(self):
        return self.position
    
    def get_radius(self):
        return self.radius
    
    def collides_with(self, coordinate):
        if (coordinate[0] > self.position[0]-self.radius) and (coordinate[0] < self.position[0]+self.radius):
            if (coordinate[1] > self.position[1]-self.radius) and (coordinate[1] < self.position[1]+self.radius):
                return True
        
        return False
    
    def get_size(self):
        return self.corner_count
    
    def get_direction(self):
        return math.degrees(self.direction)
    
    
class Text:
    def __init__(self, top_left, length=1, size=None) -> None:
        self.top_left = top_left
        self.length = length
        self.size = size if size is not None else DEFAULT_FONT_SIZE
        
        self.text = ["" for _ in range(self.length)]
        
        self.letter_height = self.size
        self.letter_width = int(self.size / 2)
        self.padding = int(size * 0.1)
        self.line_width = int(self.size * 0.25)
        
    def single_letter(self, index, letter_code):
        letter_top_left = (self.top_left[0] + index * (self.letter_width + 2*self.padding) + self.padding, self.top_left[1]+self.padding)
        bin_code = bin(letter_code)[2:].split()
        
        polygon = [(0, 0) for i in range(4)]
        polygon[0] = letter_top_left
        polygon[1] = (letter_top_left[0] + self.letter_width, letter_top_left[1])
        polygon[2] = (letter_top_left[0] + self.letter_width - self.line_width, letter_top_left[1] + self.line_width)
        polygon[3] = (letter_top_left[0] + self.line_width, letter_top_left[1] + self.line_width)
        
        if bin_code[0] == "1":
            pygame.draw.polygon(screen, CL_WHITE, polygon)        
        else:
            pygame.draw.polygon(screen, CL_DARK_GRAY, polygon)
        pygame.draw.polygon(screen, CL_LIGHT_GRAY, polygon, 1)
        
        polygon[0] = (letter_top_left[0] + self.letter_width, letter_top_left[1])
        polygon[1] = (letter_top_left[0] + self.letter_width, letter_top_left[1] + self.letter_width)
        polygon[2] = (letter_top_left[0] + self.letter_width - self.line_width, letter_top_left[1] + self.letter_width - self.line_width)
        polygon[3] = (letter_top_left[0] + self.letter_width - self.line_width, letter_top_left[1] + self.line_width)
        
        if bin_code[1] == "1":
            pygame.draw.polygon(screen, CL_WHITE, polygon)        
        else:
            pygame.draw.polygon(screen, CL_DARK_GRAY, polygon)
        pygame.draw.polygon(screen, CL_LIGHT_GRAY, polygon, 1)
        
    def update_text(self, text):
        self.text = text
        
        for i, letter in enumerate(text):
            self.single_letter(i, hex(ord(letter)))
      
    def get_letter_code(self, letter):
        if letter == " ":
            return "00000000"
        elif letter == "A":
            return "01100001"  
        
if __name__ == "__main__":
    pygame.init()
    screen = Screen()
    screen.run()   