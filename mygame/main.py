import pygame
import sys
import logging

from classes import *

# Configure logging settings
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler('game.log', mode='w')])


# Initialize Pygame
pygame.init()
# Initialize Pygame Font
pygame.font.init()
font = pygame.font.Font(None, 36)

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30

# Load Images
player_img = pygame.image.load("player.png")
npc_img = pygame.image.load("npc.png")
map_img = pygame.image.load("map.png")





# Create game objects



move1 = Battle.Move("Tackle", 10, 0.95)
move2 = Battle.Move("Scratch", 8, 0.9)
move3 = Battle.Move("Tail Whip", 5, 1.0)

# Create monster instances
player_monster1 = Monster(100, 100, pygame.image.load("player_monster1.png"), "Player Monster 1", 1000, 20, 10, [move1, move2, move3])
player_monster2 = Monster(200, 100, pygame.image.load("player_monster2.png"), "Player Monster 2", 100, 20, 10,[move1, move2, move3])

npc_monster1 = Monster(300, 100, pygame.image.load("npc_monster1.png"), "NPC Monster 1", 100, 20, 10,[move1, move2, move3])
npc_monster2 = Monster(400, 100, pygame.image.load("npc_monster2.png"), "NPC Monster 2", 100, 20, 10,[move1, move2, move3])

# Create game objects
player = Player(400, 300)
player.team = [player_monster1, player_monster2]  # Add monsters to the player's team

npcs = pygame.sprite.Group()
npcs.add(NPC(200, 200, "Hello! How are you?", [npc_monster1]))
npcs.add(NPC(600, 400, "Welcome to our town!", [npc_monster2]))

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Map")

# Set up the clock
clock = pygame.time.Clock()

# Game loop
running = True
battle_active = False
interacting_npc = None
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    # Handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            logging.info('QUIT GAME')
            running = False
        if event.type == pygame.KEYDOWN:
            logging.info('keydown')
            if event.key == pygame.K_z and not battle_active:
                logging.info('non battle key press: z')
                if interacting_npc is None:
                    collided_npcs = pygame.sprite.spritecollide(player, npcs, False)
                    for npc in collided_npcs:
                        interacting_npc = npc
                        logging.info('npc interacting with player')
                        npc.interact(player, screen, font)
            if interacting_npc:
                if event.key == pygame.K_y:
                    logging.info('player says yes to battle')
                    if interacting_npc.dialogue_state == "wait_for_answer":
                        interacting_npc.dialogue_state = "battle"
                        battle = interacting_npc.interact(player, screen, font)
                        if battle:
                            battle_active = True
                            interacting_npc = None
                if event.key == pygame.K_n:
                    logging.info('player says no to battle')
                    if interacting_npc.dialogue_state == "wait_for_answer":
                        interacting_npc.dialogue_state = "ask"
                        interacting_npc = None

    # Update game objects
    if not battle_active:
        player.update(keys)

    if battle_active:


        battle.handle_input(events)
        battle_done = battle.update(events)
        if battle_done:
            logging.info('ending battle')
            battle_active = False
            # Handle the end of the battle
            if not battle.npc_team:  # Check if the NPC team is empty
                logging.info('empty team for npc')

                if interacting_npc is not None:  # Add this check
                    logging.info('npc defeated check')
                    interacting_npc.defeated = True
                interacting_npc = None

    # Draw everything
    if not battle_active:

        screen.blit(map_img, (0, 0))
        screen.blit(player.image, player.rect)
        npcs.draw(screen)
        if interacting_npc:
            if interacting_npc.dialogue_state == "wait_for_answer":
                interacting_npc.render_text(screen, interacting_npc.current_message + " Do you want to battle? (Y/N)")
            elif interacting_npc.dialogue_state == "ask":
                interacting_npc.render_text(screen, interacting_npc.current_message)
    else:
        battle.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
