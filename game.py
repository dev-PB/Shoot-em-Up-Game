#=============================================================#
"""
Ryan Wilson
13/2/2018 TO 13/4/2018
GITHUB VERSION

This version has been edited to remove any personal or sensitive 
information. Due to the nature of the assignment, there are way 
more comments than necessary.
"""
#=============================================================#

#Importing modules
import pygame
import time
import random
import csv

#Initialising pygame
pygame.init()
clock = pygame.time.Clock()
FPS = 30
font = pygame.font.SysFont(None, 25)

# Defining some colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
orange = (255,140,0)

# Setting up the window
windowX = 800 # Width of the window
windowY = 600 # Height of the window
gameDisplay = pygame.display.set_mode((windowX, windowY)) # Creates the window
pygame.display.set_caption("Shoot 'em up!") # Titles the window

#=============================================================#
""" PROCEDURES """
#=============================================================#

""" This procedure will take in a message, an RGB value, and a position and will use them to display a message
with that message, with the text colour being specificed by the RGB value, at the position."""
def message_to_display(message, colour, position):
    message_text = font.render(message, True, colour)
    gameDisplay.blit(message_text, position)
    pygame.display.update()

""" This procedure will take in a message and a RGB value, and display on screen a perfectly centred message
with the colour of the text being specified by the RGB value"""
def message_to_display_centred(message, colour):
    def text_objects(text, colour):
        textSurface = font.render(text, True, colour)
        return textSurface, textSurface.get_rect()

    textSurf, textRect = text_objects(message, colour)
    textRect.center = (windowX / 2), (windowY / 2)
    gameDisplay.blit(textSurf, textRect)

""" This procedure will clear the screen, display a message that says "Goodbye!" and close the game"""
def closeGame():
    gameDisplay.fill(white)
    message_to_display_centred("Goodbye!", red)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()

""" This procedure will take in the parameter speed. It will randomly choose between true or false.
If the outcome is True, it will set movement speed to speed, if its False it'l set movement speed to
the negative version of speed. It will then return movementspeed."""
def enemy_movement(speed):
    enemy_direction = random.choice([True, False])
    if enemy_direction == True:
        movementspeed = speed
    else: movementspeed = -speed
    return movementspeed

""" This procedure takes in the player's health and points and displays them in the top right of the screen."""
def update_player_HUD(health, points):
    points_message = "Points:", points
    health_message = "Health:", health
    message_to_display(str(health_message), red, [windowX - windowX / 6, windowY / 20])
    message_to_display(str(points_message), red, [windowX - windowX / 6, windowY / 12])

""" This procedure loads the leaderboard from a CSV file, and stores it in an array of records called leaderboard.
It will then return the leaderboard array of records. """
def load_leaderboard():
    leaderboard = []
    input_file = open('leaderboard.csv','r')
    read_file = csv.reader(input_file)
    for line in read_file:
        leaderboard.append(line)
    return leaderboard

""" This procedure takes in an array of records, and saves it to a CSV file"""
def save_leaderboard(data):
    write_file = open('leaderboard.csv','w')
    writer = csv.writer(write_file, lineterminator='\n')
    writer.writerows(data)

""" This procedure takes in the player's name and points, as well as the leaderboard array of records. It will then
put the player's points and name into a record and put that record into the leaderboard array of records."""
def package_player_data(points, name, leaderboard):
    player_data = [points, name]
    leaderboard.append(player_data)
    return leaderboard

""" This procedure takes in the leaderboard array of records, and will return the index of the record with the
highest score"""
def find_max_value_index(array):
    counter = 0
    max_value = int(array[counter][0])
    max_index =  0
    for x in array: 
        if max_value < int(array[counter][0]): 
            max_value = int(array[counter][0])
            max_index = counter
        counter += 1
    return max_index

""" This leaderboard will use a selection sort in order to sort the leaderboard array of records by
score"""
def sort_leaderboard_highscore(unsorted_array):
    sorted_array = []
    for x in unsorted_array:
        highest_index = find_max_value_index(unsorted_array)
        sorted_array.append(unsorted_array[highest_index])
        unsorted_array[highest_index] = [0, "DUMMY_VALUE"]
    return sorted_array

""" This procedure will display a message telling the user how to return to the main menu from the leaderboard
screen"""
def display_leaderboard_controls():
    message_to_display("Press P to return to the main menu.", red, [30, windowY - windowY/6])

""" This procedure will display the leaderboard screen. It will first display all of the headings, and then it will load
and sort the leaderboard (by calling other procedures) and then display the top 10 scores. """
def display_leaderboard_highscore():
    gameDisplay.fill(white)
    message_to_display("Top 10 scores", red, [windowX/2.5, windowY/6 - 60])
    message_to_display("SCORE", red, [windowX/6, windowY/6 - 30])
    message_to_display("NAME", red, [windowX - (windowX/2), windowY/6 - 30])
    display_leaderboard_controls()
    counter = 0

    leaderboard = load_leaderboard()
    sorted_leaderboard = sort_leaderboard_highscore(leaderboard)

    for record in sorted_leaderboard:
        if counter < 10:
            score_to_display = str(record[0])
            name_to_display = str(record[1])

            message_to_display(score_to_display, black, [windowX/6, windowY/6 + (counter * 30)])
            message_to_display(name_to_display, black, [windowX - (windowX/2), windowY/6 + (counter * 30)])

            counter += 1
    pygame.display.update()

""" This procedure will display the gameover screen. It will take in the player's name, points and the amount of
enemies they have eliminated so that it can be displayed to them. It will also display a message instructing the
user to either press P to return to the main menu or press Q to quit the game. """
def display_gameover_screen(name, points, eliminations):
    gameDisplay.fill(white)
    message_to_display_centred("Game over, press P to return to the main menu or Q to quit.", red)
    stats_message_eliminations = name + " you eliminated " + str(eliminations) + " enemies"
    stats_message_points = "and collected " + str(points) + " points!"
    message_to_display(stats_message_eliminations, black, [windowX / 3.5, (windowY - windowY / 6) - 30])
    message_to_display(stats_message_points, black, [windowX / 2.5, windowY - windowY / 6])
    pygame.display.update()

""" This procedure will display the main menu screen."""
def display_menu_screen():
    gameDisplay.fill(white)
    message_to_display("Welcome to my game!", red, [windowX / 2.5, windowY / 6])
    message_to_display_centred("Press P to play, L to view the leaderboard or Q to quit", black)
    pygame.display.update()
    
""" This procedure will ask the player to input their name. It will take in keypresses, and combine
them into a string. It will then validate the user's input by checking that they have inputted a name
with atleast one character, and no more than 10 characters. If the name passes the validation, it will
return the inputted name"""
def get_player_name():
    done_typing = False
    name = ""
    while done_typing == False:
        gameDisplay.fill(white)
        message_to_display_centred("Type your name below. Press backspace to delete a letter. Press enter when finished.", black)
        message_to_display(name, red, [windowX / 6, windowY - windowY / 6])
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        leaderboard_screen = False
                        gameRunning = False
                        closeGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        name += ("q")
                    if event.key == pygame.K_w:
                        name += ("w")
                    if event.key == pygame.K_e:
                        name += ("e")
                    if event.key == pygame.K_r:
                        name += ("r")
                    if event.key == pygame.K_t:
                        name += ("t")
                    if event.key == pygame.K_y:
                        name += ("y")
                    if event.key == pygame.K_u:
                        name += ("u")
                    if event.key == pygame.K_i:
                        name += ("i")
                    if event.key == pygame.K_o:
                        name += ("o")
                    if event.key == pygame.K_p:
                        name += ("p")
                    if event.key == pygame.K_a:
                        name += ("a")
                    if event.key == pygame.K_s:
                        name += ("s")
                    if event.key == pygame.K_d:
                        name += ("d")
                    if event.key == pygame.K_f:
                        name += ("f")
                    if event.key == pygame.K_g:
                        name += ("g")
                    if event.key == pygame.K_h:
                        name += ("h")
                    if event.key == pygame.K_j:
                        name += ("j")
                    if event.key == pygame.K_k:
                        name += ("k")
                    if event.key == pygame.K_l:
                        name += ("l")
                    if event.key == pygame.K_z:
                        name += ("z")
                    if event.key == pygame.K_x:
                        name += ("x")
                    if event.key == pygame.K_c:
                        name += ("c")
                    if event.key == pygame.K_v:
                        name += ("v")
                    if event.key == pygame.K_b:
                        name += ("b")
                    if event.key == pygame.K_n:
                        name += ("n")
                    if event.key == pygame.K_m:
                        name += ("m")
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if name == "": # Input validation to make sure they have entered something
                            message_to_display("Please enter a name!", red, [windowX / 2.5, windowY / 6])
                            time.sleep(1)
                        elif len(name) > 10: # Input validation to make sure they have not entered a string thats too long
                            message_to_display("Too long! Enter a name with up to 10 characters.", red, [windowX / 5, windowY / 6])
                            time.sleep(1)
                        else: # If the user's input passes the input validation, breaks the while loop and returns the name
                            done_typing = True
                            
                    if event.key == pygame.K_BACKSPACE:
                        if name != "":
                            name = name[:-1]
                
                pygame.display.update()
    return name

#=============================================================#
""" GAME LOOP """
#=============================================================#

""" This procedure is the main game loop"""
def gameLoop():
    """ The following variables that are being initialised control what screen the user will see."""
    gameRunning = True # While this is True, the whole game will run.
    gameOver = False # When this is True, the user will be on the gameover screen
    menu = True # When this is True, the user will be on the main menu
    leaderboard_screen = False # When this is true, the user will be on the leaderboard screen
    game_active = False # When this is true, the user will be on the gameplay screen
    
    """ The following variables control the player's attributes such as their size and colour. """
    player_colour = blue # The player's colour
    player_x = windowX / 2  # The player's X coordinate
    player_y = windowY - (windowY / 6)  # The player's Y coordinate
    player_x_change = 0 # The amount of pixels the player will move in either direction (Negative values moves them left, positive moves them right)
    player_size_x = 20  # The player's width
    player_size_y = 40  # The player's height
    player_health = 5 # The player's health points
    player_points = 0 # The player's points
    player_bullet_speed = -20 # The amount of pixels the player's bullet will travel each frame (will be a negative so it can move up)
    player_bullet_active = False # Booleon to control if the player has a bullet on screen currently
    player_bullet_x = 0 # X coordinate of the player's bullet
    player_bullet_y = 0 # Y coordinate of the player's bullet
    player_elimination_count = 0 # The number of enemies eliminated by the player
    

    """ The following variables control the enemy's attributes such as their size and colour. """
    enemy_colour = red # The enemy's colour
    enemy_x = windowX / 2  # The enemy's X coordinate
    enemy_y = windowY / 6  # The enemy's Y coordinate
    enemy_x_change = 0 # The amount of pixels the enemy will move in either direction (Negative values moves them left, positive moves them right)
    enemy_size_x = 20  # The enemy's width
    enemy_size_y = 40  # The enemy's height
    enemy_bullet_speed = 20 # The amount of pixels the enemy's bullet will travel each frame (will be a positive so it can move down)
    enemy_bullet_active = False # Booleon to control if the enemy has a bullet on screen currently
    enemy_bullet_x = 0 # X coordinate of the enemy's bullet
    enemy_bullet_y = 0 # Y coordinate of the enemy's bullet

    while gameRunning == True:
        
        #=============================================================#
        """ MAIN MENU LOOP 
        While this loop is active, the user will be on the main menu."""
        #=============================================================#
        if menu == True:
            leaderboard = load_leaderboard()
            display_menu_screen()

            """ The following loop checks for events, such as pressing a
            key on the keyboard. If the Q key is pressed, the game exits.
            If the L key is pressed, the user will be taken to the leaderboard
            screen. If the P key is pressed, the user will be taken to the name
            input screen."""

            while menu == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        menu = False
                        gameRunning = False
                        closeGame()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            menu = False
                            gameRunning = False
                            closeGame()
                        if event.key == pygame.K_l:
                            leaderboard_screen = True
                            menu = False

                        if event.key == pygame.K_p:
                            player_name = get_player_name()
                            menu = False
                            game_active = True

        #=============================================================#
        """ LEADERBOARD LOOP 
        While this loop is active, the player will be on the leaderboard
        screen."""
        #=============================================================#

        if leaderboard_screen == True:
            display_leaderboard_highscore()

            """ The following loop checks for events, such as pressing a
            key on the keyboard. If P key is pressed, the user will be
            taken back to the main menu screen."""

            while leaderboard_screen == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        leaderboard_screen = False
                        gameRunning = False
                        closeGame()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            leaderboard_screen = False
                            menu = True
                        
        #=============================================================#
        """ GAME OVER LOOP 
        While this loop is active, the user will be on the gameover
        screen."""
        #=============================================================#
        if gameOver == True:
            game_active = False
            display_gameover_screen(player_name, player_points, player_elimination_count)

            """ The following loop checks for events, such as pressing a
            key on the keyboard. If P key is pressed, the user will be
            taken back to the main menu screen. If the Q key is pressed,
            the game will close."""

            while gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            menu = False
                            gameRunning = False
                            closeGame()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameOver = False
                            closeGame()
                        if event.key == pygame.K_p:
                            gameLoop()

        #=============================================================#
        """ GAME PLAY LOOP 
        This section of code is for the gameplay screen."""
        #=============================================================#
        if game_active == True:

            """ The following loop checks for events, such as pressing a
            key on the keyboard. If the left arrow key is pressed, the user
            will move left. If the right arrow key is pressed, the user will
            move right. If the user presses X, they will fire a projectile."""

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # When the user presses the X button
                    gameRunning = False
                    game_active = False
                    closeGame()

                if event.type == pygame.KEYDOWN: # Handles key presses
                    if event.key == pygame.K_LEFT:
                        player_x_change = -player_size_x
                    if event.key == pygame.K_RIGHT:
                        player_x_change = player_size_x
                    if event.key == pygame.K_x:
                        if player_bullet_active == False:
                            player_bullet_active = True
                            player_bullet_x = player_x
                            player_bullet_y = player_y

                if event.type == pygame.KEYUP: # Handles key releases
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player_x_change = 0
            
            """ This checks where the enemy wants to move """
            enemy_x_change = enemy_movement(enemy_size_x)

            """ This section of code makes sure the player and enemy cant go out of bounds
            off of the screen. """

            if player_x >= windowX: # Stops the player from leaving the screen
                player_x_change = 0
                player_x = windowX - (player_size_x + 1)

            if player_x < 0: # Stops the player from leaving the screen
                player_x_change = 0
                player_x = 1

            if enemy_x >= windowX: # Stops the enemy from leaving the screen
                enemy_x_change = 0
                enemy_x = windowX - (enemy_size_x + 1)

            if enemy_x < 0: # Stops the enemy from leaving the screen
                enemy_x_change = 0
                enemy_x = 1

            """ This section of code moves the player and enemy depending on where
            each of them have decided to move """
            player_x += player_x_change # Moves the player
            enemy_x += enemy_x_change # Moves the enemy

            gameDisplay.fill(white) # Sets the background colour

            """ This section of code draws the player and enemy's characters """
            # Draws the player
            pygame.draw.rect(gameDisplay, player_colour, [player_x,player_y,
                                                          player_size_x,player_size_y])

            # Draws the enemy
            pygame.draw.rect(gameDisplay, enemy_colour, [enemy_x,enemy_y,
                                                         enemy_size_x,enemy_size_y])
            
            """ This section of code controls the player's bullet. It checks if the bullet is
            out of bounds and removes it if it is. If it isnt, it continues to move and draw
            the bullet """
            # Code for player's bullet
            if player_bullet_active == True:
                if player_bullet_y < 0: # Checks to see if the player's bullet is out of bounds
                    player_bullet_active = False
                    player_bullet_x = player_x
                    player_bullet_y = player_y

                else: # If the bullet is still being fired, it continues to move
                    player_bullet_y += player_bullet_speed
                    pygame.draw.rect(gameDisplay, green, [player_bullet_x, player_bullet_y,
                                                    player_size_x / 2,player_size_y/2])

            """ This section of code controls the player's bullet. It checks if the bullet is
            out of bounds and removes it if it is. If it isnt, it continues to move and draw
            the bullet. If the enemy does not have a bullet already active, it checks to see
            if the enemy wants to fire a bullet."""
            # Code for enemy's bullet
            if enemy_bullet_active == True:
                if enemy_bullet_y > windowY: # Checks to see if the enemy's bullet is out of bounds
                    enemy_bullet_active = False
                    enemy_bullet_x = enemy_x
                    enemy_bullet_y = enemy_y

                else: # If the bullet is still being fired, it continues to move
                    enemy_bullet_y += enemy_bullet_speed
                    pygame.draw.rect(gameDisplay, orange, [enemy_bullet_x, enemy_bullet_y,
                                                    enemy_size_x / 2,enemy_size_y/2])
            
            else: # If they have no bullets, randomly fire one
                enemy_fire_attempt = random.choice([True, False])
                if enemy_fire_attempt == True:
                    enemy_bullet_active = True
                    enemy_bullet_x = enemy_x
                    enemy_bullet_y = enemy_y

            """ This section checks to see if the player has been hit, and if they have it deducts
            from the player's health """
            # Checks to see if the player has been hit
            if enemy_bullet_x >= player_x and enemy_bullet_x <= player_x + player_size_x:
                if enemy_bullet_y >= player_y and enemy_bullet_y < player_y + player_size_y:
                    player_health -= 1
                    enemy_bullet_active = False
                    enemy_bullet_y = 0
                    enemy_bullet_x = 0

            """ This section of code checks to see if the enemy has been hit. If they have,
            it eliminates the enemy, rewards the player and creates a new enemy. """
            if player_bullet_x >= enemy_x and player_bullet_x <= enemy_x + enemy_size_x:
                if player_bullet_y <= enemy_y + enemy_size_y and player_bullet_y >= enemy_y:
                    player_points += 5
                    player_bullet_active = False
                    player_bullet_y = 0
                    player_bullet_x = 0
                    player_elimination_count += 1
                    enemy_colour = white
                    pygame.draw.rect(gameDisplay, enemy_colour, [enemy_x,enemy_y,
                                                         enemy_size_x,enemy_size_y])
                    update_player_HUD(player_health, player_points)
                    elimination_message = str(player_elimination_count) + " enemies eliminated!"
                    message_to_display_centred(elimination_message, red)
                    pygame.display.update()
                    time.sleep(1)
                    enemy_x = windowX / 2
                    enemy_colour = red

            """ This section checks to see if the player is out of lives. If they are, it takes them
            to the gameover screen """
            if player_health == 0:
                leaderboard = package_player_data(player_points, player_name, leaderboard)
                save_leaderboard(leaderboard)
                gameOver = True

            """ This line updates the player's health and points indicators"""
            update_player_HUD(player_health, player_points)
        pygame.display.update() # Renders the graphics
        clock.tick(FPS) # Moves the game forward a set amount of frames

gameLoop() # Call the game loop
closeGame() # Closes the game.
