import pygame.font


class Menu:

    def __init__(self):
        """Initialize button attributes."""
        self.show_scores = False
        self.fontb = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 46)

    def main(self, play_button, score_button, screen):
        play_button.draw_button()
        score_button.draw_button()

        fonta = pygame.font.Font(None, 144)
        texta = fonta.render("SPACE", 1, (255, 255, 255))
        widtha, heighta = fonta.size("SPACE")
        recta = pygame.Rect(screen.get_width() / 2 - widtha / 2, screen.get_height() / 8, widtha, heighta)
        screen.blit(texta, recta)

        self.fontb = pygame.font.Font(None, 72)
        textb = self.fontb.render("INVADERS", 1, (0, 255, 0))
        widthb, heightb = self.fontb.size("INVADERS")
        rectb = pygame.Rect(screen.get_width() / 2 - widthb / 2, screen.get_height() / 8 + heighta, widthb, heightb)
        screen.blit(textb, rectb)

        self.points(screen, 'images/a1-1.png', "= 10 PTS", 8)
        self.points(screen, 'images/a2-1.png', "= 20 PTS", 9)
        self.points(screen, 'images/a3-1.png', "= 40 PTS", 10)
        self.points(screen, 'images/ralien.png', "= ???", 11)

    def scores(self, score_button, screen):
        score_button.draw_button()
        fonta = pygame.font.Font(None, 72)
        texta = fonta.render("ALL-TIME", 1, (255, 255, 255))
        widtha, heighta = fonta.size("ALL-TIME")
        recta = pygame.Rect(screen.get_width() / 2 - widtha / 2, screen.get_height() / 20, widtha, heighta)
        screen.blit(texta, recta)
        self.fontb = pygame.font.Font(None, 72)
        textb = self.fontb.render("HIGH SCORES:", 1, (255, 255, 255))
        widthb, heightb = self.fontb.size("HIGH SCORES:")
        rectb = pygame.Rect(screen.get_width() / 2 - widthb / 2, screen.get_height() / 20 + heighta, widthb, heightb)
        screen.blit(textb, rectb)
        with open('hs.txt'):
            hscores = [line.rstrip('\n') for line in open('hs.txt')]
            top_scores = []
        for i in range(0, 9):
            max1 = 0
            for j in range(len(hscores)):
                if int(hscores[j]) > max1:
                    max1 = int(hscores[j])
            hscores.remove(str(max1))
            top_scores.append(max1)
        for i in range(0, 9):
            current_score = top_scores[i]
            font = pygame.font.Font(None, 46)
            text = font.render(str(i+1) + ". " + str(current_score), 1, (255, 255, 255))
            width, height = font.size(str(i+1) + ". " + str(current_score))
            rect = pygame.Rect(0, rectb.bottom + 75 * (i + 1), width, height)
            rect.left = rectb.left
            screen.blit(text, rect)

    def points(self, screen, image, msg, y):
        self.font = pygame.font.Font(None, 46)
        text = self.font.render(msg, 1, (255, 255, 255))
        width, height = self.font.size(msg)
        rect = pygame.Rect(screen.get_width() / 2 - width / 2, screen.get_height() * y / 20 + height, width, height)
        screen.blit(text, rect)

        image = pygame.image.load(image)
        recti = image.get_rect()
        recti.y = screen.get_height() * y / 20 + height
        recti.x = screen.get_width() * 4 / 10 - recti.width / 2
        screen.blit(image, recti)
