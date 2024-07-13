import pygame
import random
import os
from PIL import Image, ImageDraw

# Create placeholder card images if not already present
def create_placeholder_images():
    if not os.path.exists("cards"):
        os.makedirs("cards")

    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    for suit in suits:
        for value in values:
            file_path = f"cards/{value}_of_{suit}.png"
            if not os.path.exists(file_path):
                img = Image.new('RGB', (80, 120), color = (73, 109, 137))
                d = ImageDraw.Draw(img)
                d.text((10,10), f"{value}\n{suit}", fill=(255,255,255))
                img.save(file_path)

create_placeholder_images()

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 80
CARD_HEIGHT = 120
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

# Load card images
card_images = {}
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

for suit in suits:
    for value in values:
        card_images[f"{value}_of_{suit}"] = pygame.transform.scale(
            pygame.image.load(os.path.join("cards", f"{value}_of_{suit}.png")),
            (CARD_WIDTH, CARD_HEIGHT)
        )

# Card class
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.image = card_images[f"{value}_of_{suit}"]

    def __repr__(self):
        return f"{self.value} of {self.suit}"

# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

# Game class
class Game:
    def __init__(self):
        self.deck = Deck()
        self.players = [Player("Player 1"), Player("Player 2")]
        self.community_cards = []
        self.current_player = 0
        self.pot = 0
        self.bet = 0
        self.phase = "deal"

    def deal(self):
        for _ in range(2):
            for player in self.players:
                player.hand.append(self.deck.draw())

    def flop(self):
        self.community_cards.append(self.deck.draw())
        self.community_cards.append(self.deck.draw())
        self.community_cards.append(self.deck.draw())

    def turn(self):
        self.community_cards.append(self.deck.draw())

    def river(self):
        self.community_cards.append(self.deck.draw())

    def next_phase(self):
        if self.phase == "deal":
            self.flop()
            self.phase = "flop"
        elif self.phase == "flop":
            self.turn()
            self.phase = "turn"
        elif self.phase == "turn":
            self.river()
            self.phase = "river"
        elif self.phase == "river":
            self.phase = "showdown"

    def start(self):
        # Set up display
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Texas Hold'em Poker")

        # Main game loop
        running = True
        self.deal()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 650 <= x <= 650 + BUTTON_WIDTH and 500 <= y <= 500 + BUTTON_HEIGHT:
                        self.bet = 10
                        self.pot += self.bet
                        self.next_phase()
                    elif 650 <= x <= 650 + BUTTON_WIDTH and 400 <= y <= 400 + BUTTON_HEIGHT:
                        self.next_phase()

            # Fill the background
            screen.fill(GREEN)

            # Draw player hands
            for i, player in enumerate(self.players):
                for j, card in enumerate(player.hand):
                    screen.blit(card.image, (10 + j * 90, 450 + i * 150))

            # Draw community cards
            for i, card in enumerate(self.community_cards):
                screen.blit(card.image, (200 + i * 90, 200))

            # Draw buttons
            pygame.draw.rect(screen, WHITE, (650, 500, BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(screen, WHITE, (650, 400, BUTTON_WIDTH, BUTTON_HEIGHT))
            font = pygame.font.Font(None, 36)
            bet_text = font.render('Bet', True, (0, 0, 0))
            check_text = font.render('Check', True, (0, 0, 0))
            screen.blit(bet_text, (675, 515))
            screen.blit(check_text, (665, 415))

            # Draw pot
            pot_text = font.render(f'Pot: ${self.pot}', True, WHITE)
            screen.blit(pot_text, (650, 50))

            # Update display
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.start()

    pygame.quit()
