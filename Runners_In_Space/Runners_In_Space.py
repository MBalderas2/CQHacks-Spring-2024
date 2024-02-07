import pygame
import random
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set volume for music and sound effects
music_volume = 0.5  # Lower the music volume to 50%
sound_effects_volume = 1.0  # Set sound effects volume to 100%

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)  # Color for the shield
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Text font
font = pygame.font.SysFont(None, 36)

# Title Font
title_font = pygame.font.Font(None, 72)

# Start Screen Title
title_text = "Runners in Space"
title_surface = title_font.render(title_text, True, WHITE)
title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2,
                                            SCREEN_HEIGHT // 4))

# Set the window title
pygame.display.set_caption("Runners in Space")

# Screen dimensions
width, height = SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Text for muting music and sound effects
mute_music_text = font.render("Press 'm' to mute music", True, WHITE)
mute_sound_text = font.render("Press 's' to mute sound effects", True, WHITE)

sound_effects_enabled = True
music_enabled = True

# Game variables
high_score = 0
level = 1
score = 0
lives = 3
invun = 0
game_active = False  # Indicates if the game is active or in menu mode
random_seed = random.randint(0, 1000000)
obstacles = []  # To store obstacles

# Load sound effects
explosion_sfx = pygame.mixer.Sound('explosion.mp3')
bounce_sfx = pygame.mixer.Sound('bounce.mp3')

# Load and play menu music
pygame.mixer.music.load('MenuMusic.mp3')
pygame.mixer.music.play(-1)
# Play infinitely
in_game_music = 'GameMusic.mp3'

# Load images
rocket_image = pygame.image.load('rocket.png').convert_alpha()
rock_image = pygame.image.load('moon.png').convert_alpha()
moon_background = pygame.image.load('space.jpg').convert()
moon_background = pygame.transform.scale(moon_background, (width, height))
MenuImage = pygame.image.load("space.jpg").convert_alpha()
InGame_Image = pygame.image.load("In_Game_Space.jpg").convert_alpha()

# Resize images
rocket_image = pygame.transform.scale(rocket_image, (64, 64))
rock_image_small = pygame.transform.scale(rock_image, (24, 24))

#Game Over Text
game_over_text = "GAME OVER"
game_over_surface = font.render(game_over_text, True, WHITE)
game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


# Frame rate
clock = pygame.time.Clock()


# Button class for menu
class Button:

  def __init__(self, color, x, y, width, height, text=''):
    self.color = color
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.text = text

  def draw(self, win, outline=None):
    if outline:
      pygame.draw.rect(
          win, outline,
          (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
    pygame.draw.rect(win, self.color,
                     (self.x, self.y, self.width, self.height), 0)
    if self.text != '':
      text = font.render(self.text, 1, WHITE)
      win.blit(text,
               (self.x + (self.width / 2 - text.get_width() / 2), self.y +
                (self.height / 2 - text.get_height() / 2)))

  def isOver(self, pos):
    if self.x < pos[0] < self.x + self.width and self.y < pos[
        1] < self.y + self.height:
      return True
    return False

# At the global level
game_paused = False
resume_button = Button(GREEN, 300, 200, 200, 50, 'Resume')
main_menu_button = Button(RED, 300, 300, 200, 50, 'Main Menu')

# Centering buttons
start_button = pygame.Rect(100, 500, 200, 50)
exit_button = pygame.Rect(500, 500, 200, 50)
sound_button = Button(BLUE, 50, height - 60, 150, 40, 'Toggle Sound')
music_button = Button(BLUE, width - 200, height - 60, 150, 40, 'Toggle Music')


# Toggle music and sound effects
def toggle_music():
  global music_enabled
  music_enabled = not music_enabled
  if music_enabled:
    pygame.mixer.music.set_volume(
        music_volume)  # Adjust the volume when music is enabled
    if game_active:
      pygame.mixer.music.load(in_game_music)
    else:
      pygame.mixer.music.load('MenuMusic.mp3')
    pygame.mixer.music.play(-1)
  else:
    pygame.mixer.music.stop()


# Adjust volume settings immediately for initial states
pygame.mixer.music.set_volume(music_volume)
explosion_sfx.set_volume(sound_effects_volume)
bounce_sfx.set_volume(sound_effects_volume)


def toggle_sound_effects():
  global sound_effects_enabled
  sound_effects_enabled = not sound_effects_enabled
  # Adjust the volume of sound effects directly
  explosion_sfx.set_volume(
      sound_effects_volume if sound_effects_enabled else 0)
  bounce_sfx.set_volume(sound_effects_volume if sound_effects_enabled else 0)


# Toggle music and sound effects in menu
def toggle_music_in_menu():
  global music_enabled
  music_enabled = not music_enabled
  if music_enabled:
    pygame.mixer.music.load('MenuMusic.mp3')
    pygame.mixer.music.play(-1)
  else:
    pygame.mixer.music.stop()


def toggle_sound_effects_in_menu():
  global sound_effects_enabled
  sound_effects_enabled = not sound_effects_enabled


# Reset the game state
def reset_game():
    global score, lives, level, obstacles, game_active, invun, music_enabled
    score = 0
    lives = 3
    level = 1
    obstacles = []
    game_active = True
    invun = 0

    # Stop the menu music and start the game music here
    if music_enabled:
        pygame.mixer.music.stop()  # Ensure the menu music is stopped
        pygame.mixer.music.load(in_game_music)  # Load the game music
        pygame.mixer.music.play(-1)  # Play the game music indefinitely


def main_menu():
  global game_active
  if music_enabled:
      pygame.mixer.music.load('MenuMusic.mp3')
      pygame.mixer.music.play(-1)  # Loop the menu music

  # Fade-in effect
  fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
  fade_surface.fill(BLACK)
  for alpha in range(255, -1, -5):  # Start from 255 to 0, step by -5
      fade_surface.set_alpha(alpha)
      screen.blit(fade_surface, (0, 0))
      pygame.display.update()
      pygame.time.delay(30)  # Delay to make the fade-in visible

  running = True
  image_rect = MenuImage.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

  # Scale the rocket image to make it twice as big
  scaled_rocket_image = pygame.transform.scale(rocket_image, (230, 230))

  # Rotate the scaled rocket image to point at 150 degrees
  rotated_rocket_image = pygame.transform.rotate(scaled_rocket_image, 45)

  while running:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False
              pygame.quit()
              sys.exit()
          elif event.type == pygame.MOUSEBUTTONDOWN:
              if start_button.collidepoint(pygame.mouse.get_pos()):
                  print("Start button clicked!")
                  reset_game()
                  running = False
              elif exit_button.collidepoint(pygame.mouse.get_pos()):
                  print("Exit button clicked!")
                  running = False
                  pygame.quit()
                  sys.exit()

      screen.fill(WHITE)
      screen.blit(MenuImage, image_rect)
      screen.blit(title_surface, title_rect)

      # Display the rotated and scaled ship image on the main menu
      ship_rect = rotated_rocket_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
      screen.blit(rotated_rocket_image, ship_rect)

      pygame.draw.rect(screen, BLACK, start_button)
      pygame.draw.rect(screen, BLACK, exit_button)
      start_text = font.render("Start", True, WHITE)
      exit_text = font.render("Exit", True, WHITE)
      screen.blit(start_text, (start_button.x + 80, start_button.y + 15))
      screen.blit(exit_text, (exit_button.x + 90, exit_button.y + 15))
      pygame.display.update()



def game_over():
  global game_active, score, high_score, game_paused
  game_active = False
  high_score = max(score, high_score)
  Game_Over_Screen()

def Game_Over_Screen():
    global running

    running = True

    # Getting thr current time when the game over screen starts
    start_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Calculating the elasped time from when the Game Over screen began
        elapsed_time = pygame.time.get_ticks() - start_time

        screen.fill(BLACK)

        screen.blit(game_over_surface, game_over_rect)

        pygame.display.flip()

        clock.tick(FPS)

        # ICreating a 3 second delay before moving back to the main menu
        if elapsed_time >= 3000:
            running = False
            # Calling the main_menu function to transition to the main menu
            main_menu()

def display_score_and_high_score():
  global score, high_score
  # Display score at the top right corner
  score_text = font.render(f"Score: {score}", True, WHITE)
  high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
  level_text = font.render(f"Level: {level - 1}", True, WHITE)
  screen.blit(score_text, (width - score_text.get_width() - 10, 10))
  screen.blit(high_score_text, (width - high_score_text.get_width() - 10,
                                50))  # Display high score below score
  screen.blit(level_text, (width - level_text.get_width() - 10, 90))


# Main game loop
def main():
  global lives, score, game_active, sound_effects_enabled, music_enabled, game_paused, level

  if game_active and music_enabled:
    pygame.mixer.music.load(in_game_music)
    pygame.mixer.music.play(-1)  # Loop in-game music
  else:
    pygame.mixer.music.stop()

  while game_active:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:  # Toggle sound effects
          toggle_sound_effects()
        elif event.key == pygame.K_m:  # Toggle music
          toggle_music()
        elif event.key == pygame.K_p:  # Handle 'P' for pause
          game_paused = not game_paused
          if game_paused:
            pygame.mixer.music.pause()  # Optional: Pause music
            pause_screen()  # Call pause_screen function to display pause menu
          else:
            pygame.mixer.music.unpause()  # Optional: Unpause music
      elif event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if not game_paused: 
      image_rect = InGame_Image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))  
      screen.blit(InGame_Image, image_rect)
      mouse_x, _ = pygame.mouse.get_pos()

      draw_obstacles()
      draw_player(mouse_x)
      display_score_and_high_score()
      display_lives()

      # Display mute text for music and sound effects
      screen.blit(mute_music_text, (width - mute_music_text.get_width() - 10, height - 60))
      screen.blit(mute_sound_text, (10, height - 60))

      # Check for game over condition
      if lives <= 0:
        explosion_sfx.play()
        game_over()

      pygame.display.flip()

      if score % 1500 == 0:
        level += 1

      score += 1
      clock.tick(FPS * (1 + level * 0.1))



def draw_obstacles():
  global level, obstacles

  if len(obstacles) < 6 + level:
      for _ in range(6 + level - len(obstacles)):
          ob_x = random.randint(0, width - 24)
          ob_y = random.randint(-height, 0)
          obstacles.append([ob_x, ob_y])

  for ob in obstacles:
      ob[1] += level  # Move obstacles down
      if ob[1] > height:
          obstacles.remove(ob)
          ob_x = random.randint(0, width - 24)
          ob_y = random.randint(-height, 0)
          obstacles.append([ob_x, ob_y])
      screen.blit(rock_image_small, (ob[0], ob[1]))

def draw_player(mouse_x):
  global lives, invun, score
  player_x = max(0, min(width - 64, mouse_x - 32))
  player_y = int(height * 0.8) - 32

  player_center = (player_x + 32, player_y + 32)
  player_radius = 30  # The radius of the player's circular hitbox

  if invun > 0:
      # Flash the circle outline between yellow and blue every 20 frames (0.33 seconds)
      if invun % 20 < 10:
          # Draw the blue shield outline
          pygame.draw.circle(screen, BLUE, player_center, player_radius, 2)
      else:
          # Draw the yellow shield outline
          pygame.draw.circle(screen, YELLOW, player_center, player_radius, 2)
      invun -= 1
  else:
      if check_collision(player_center, player_radius):
          # Decrement lives first to check the correct condition
          lives -= 1
          if lives > 0:
              # Play bounce sound effect if it's not the last life
              bounce_sfx.play()
              invun = 240  # 4 seconds of invulnerability (at 60 FPS)
          else:
              # If it's the last life, play the explosion sound effect
              explosion_sfx.play()
              game_over()  # Call game_over immediately after playing the sound

  # Draw the ship without any colors inside the circle
  screen.blit(rocket_image, (player_x, player_y))


def check_collision(player_center, player_radius):
  for ob in obstacles:
      ob_center = (ob[0] + 12, ob[1] + 12)  # Assuming obstacles are 24x24
      ob_radius = 6  # Half of the width of the obstacle

      distance = pygame.math.Vector2(player_center[0] - ob_center[0],
                                     player_center[1] - ob_center[1]).length()

      if distance < player_radius + ob_radius:
          return True
  return False

def pause_screen():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Resume game
                    paused = False

        # Draw the pause menu background
        screen.fill(BLACK)
        pause_text = font.render("Paused", True, WHITE)
        resume_text = font.render("Press 'P' to resume", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - pause_text.get_height() // 2))
        screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()
        clock.tick(5)  # Lower tick rate in pause menu


def display_lives():
  small_ship = pygame.transform.scale(rocket_image, (32, 32))
  for i in range(lives):  # Display as many ship images as lives left
    screen.blit(small_ship,
                (10 + i * (small_ship.get_width() + 5), 10))  # Top left corner


# Start the game from the main menu
main_menu()

# Run the main game loop
while True:
  if game_active:
    main()
  else:
    main_menu()
