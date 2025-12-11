from random import randint

WIDTH = 800
HEIGHT = 600

# Initialize player sprite (zeppelin) at center of screen
zeppelin = Actor("zeppelin")
zeppelin.pos = 400, 300

# Initialize enemy sprite at random position off-screen to the right
enemy = Actor("enemy-up")
enemy.pos = randint(800, 1600), randint(10, 200)

# Initialize cave obstacle at random position off-screen
cave = Actor("cave")
cave.pos = randint(800, 1600), 460

# Initialize tree obstacle at random position off-screen
tree = Actor("tree")
tree.pos = randint(800, 1600), 450

# Game state variables
enemy_up = True  # Tracks enemy wing animation state
up = False  # Tracks if mouse is held down (zeppelin ascending)
game_over = False  # Tracks if game has ended
score = 0  # Player's current score
number_of_updates = 0  # Counter for enemy wing flapping animation

# Menu state variables
menu_active = True  # Tracks if main menu is displayed
difficulty = "medium"  # Current difficulty: easy, medium, hard

# Difficulty settings (descent speed, enemy speed, obstacle speed)
difficulty_settings = {
    "easy": {"descent": 0.5, "enemy_speed": 2, "obstacle_speed": 1},
    "medium": {"descent": 1, "enemy_speed": 4, "obstacle_speed": 2},
    "hard": {"descent": 1.5, "enemy_speed": 6, "obstacle_speed": 3}
}

# Menu button rectangles for click detection
easy_button = Rect((300, 250), (200, 50))
medium_button = Rect((300, 320), (200, 50))
hard_button = Rect((300, 390), (200, 50))


def draw():
    """Render all game graphics on screen"""
    # Draw the background image
    screen.blit("background", (0, 0))

    if menu_active:
        # Draw main menu
        screen.draw.text("ZEPPELIN", center=(400, 150), fontsize=60, color="black")
        screen.draw.text("Select Difficulty:", center=(400, 200), fontsize=30, color="black")
        
        # Draw difficulty buttons
        screen.draw.filled_rect(easy_button, "green")
        screen.draw.text("EASY", center=easy_button.center, fontsize=30, color="white")
        
        screen.draw.filled_rect(medium_button, "orange")
        screen.draw.text("MEDIUM", center=medium_button.center, fontsize=30, color="white")
        
        screen.draw.filled_rect(hard_button, "red")
        screen.draw.text("HARD", center=hard_button.center, fontsize=30, color="white")
        
        screen.draw.text("Click to start!", center=(400, 500), fontsize=20, color="black")
    elif not game_over:
        # Draw all game objects during active gameplay
        zeppelin.draw()
        enemy.draw()
        cave.draw()
        tree.draw()
        # Display current score and difficulty in top-right corner
        screen.draw.text("Score: " + str(score), (700, 5), color="black")
        screen.draw.text("Difficulty: " + difficulty.upper(), (650, 25), color="black")
    else:
        # Display game over message with final score
        screen.draw.text("You lose!\nScore: " + str(score), center=(400, 250), fontsize=40, color="black")
        screen.draw.text("Click to return to menu", center=(400, 350), fontsize=25, color="black")


def on_mouse_down(pos):
    """Handle mouse button press - menu navigation or zeppelin ascend"""
    global up, menu_active, difficulty, game_over, score
    
    if menu_active:
        # Check which difficulty button was clicked
        if easy_button.collidepoint(pos):
            difficulty = "easy"
            start_game()
        elif medium_button.collidepoint(pos):
            difficulty = "medium"
            start_game()
        elif hard_button.collidepoint(pos):
            difficulty = "hard"
            start_game()
    elif game_over:
        # Return to menu after game over
        menu_active = True
        game_over = False
        score = 0
    else:
        # Make zeppelin ascend during gameplay
        up = True
        zeppelin.y -= 50


def on_mouse_up():
    """Handle mouse button release - zeppelin stops ascending"""
    global up
    up = False


def start_game():
    """Initialize/reset game state when starting a new game"""
    global menu_active, game_over, score, number_of_updates, up
    menu_active = False
    game_over = False
    score = 0
    number_of_updates = 0
    up = False
    
    # Reset zeppelin position
    zeppelin.pos = 400, 300
    
    # Reset enemy position
    enemy.pos = randint(800, 1600), randint(10, 200)
    enemy.image = "enemy-up"
    
    # Reset obstacles
    cave.pos = randint(800, 1600), 460
    tree.pos = randint(800, 1600), 450



def flap():
    """Animate enemy wings by toggling between up and down images"""
    global enemy_up
    if enemy_up:
        # Change to wings-down image
        enemy.image = "enemy-down"
        enemy_up = False
    else:
        # Change to wings-up image
        enemy.image = "enemy-up"
        enemy_up = True


def update():
    """Update game state each frame - handles movement, collisions, and scoring"""
    global game_over, score, number_of_updates

    # Skip updates if in menu
    if menu_active:
        return

    # Only update game objects if game is still active
    if not game_over:
        # Get current difficulty settings
        settings = difficulty_settings[difficulty]
        
        if not up:
            zeppelin.y += settings["descent"]  # Speed of descent based on difficulty

        # Update enemy position and animation
        if enemy.x > 0:
            # Move enemy from right to left across screen
            enemy.x -= settings["enemy_speed"]
            # Animate wings every 10 frames
            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            # Reset enemy to new random position when it leaves screen
            enemy.x = randint(800, 1600)
            enemy.y = randint(10, 200)
            score += 1
            number_of_updates = 0

        # Update cave obstacle position
        if cave.right > 0:
            cave.x -= settings["obstacle_speed"]
        else:
            # Reset cave to new random position and increment score
            cave.x = randint(800, 1600)
            score += 1

        # Update tree obstacle position
        if tree.right > 0:
            tree.x -= settings["obstacle_speed"]
        else:
            # Reset tree to new random position and increment score
            tree.x = randint(800, 1600)
            score += 1

        # Check if zeppelin hit top or bottom of screen
        if zeppelin.top < 0 or zeppelin.bottom > 560:
            game_over = True

        # Check for collisions with any obstacles
        if (zeppelin.collidepoint(enemy.x, enemy.y) or
            zeppelin.collidepoint(cave.x, cave.y) or
            zeppelin.collidepoint(tree.x, tree.y)):
            game_over = True
