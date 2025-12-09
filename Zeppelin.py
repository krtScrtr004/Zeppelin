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


def draw():
    """Render all game graphics on screen"""
    # Draw the background image
    screen.blit("background", (0, 0))

    if not game_over:
        # Draw all game objects during active gameplay
        zeppelin.draw()
        enemy.draw()
        cave.draw()
        tree.draw()
        # Display current score in top-right corner
        screen.draw.text("Score : " + str(score), (700, 5), color = "black")
    else:
        # Display game over message with final score
        screen.draw.text(" You lose! \n Score : " + str(score), (350, 150), color = "black")


def on_mouse_down():
    """Handle mouse button press - make zeppelin ascend"""
    global up
    up = True
    # Move zeppelin up by 50 pixels when mouse is clicked
    zeppelin.y -= 50


def on_mouse_up():
    """Handle mouse button release - zeppelin stops ascending"""
    global up
    up = False



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

    # Only update game objects if game is still active
    if not game_over:
        if not up:
            zeppelin.y += 1 # Speed of descent

        # Update enemy position and animation
        if enemy.x > 0:
            # Move enemy from right to left across screen
            enemy.x -= 4
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
        cave.x -= 2
    else:
        # Reset cave to new random position and increment score
        cave.x = randint(800, 1600)
        score += 1

    # Update tree obstacle position
    if tree.right > 0:
        tree.x -= 2
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
