import pygame


class Audio:
    def __init__(self):
        # Create mixer for audio.
        pygame.mixer.init()
        pygame.mixer.set_num_channels(5)
        self.oscia = pygame.mixer.Channel(1)
        self.oscib = pygame.mixer.Sound("osci.wav")
        self.exploa = pygame.mixer.Channel(2)
        self.explob = pygame.mixer.Sound("explo.wav")
        self.pewa = pygame.mixer.Channel(4)
        self.pewb = pygame.mixer.Sound("pew.wav")
        self.omin = pygame.mixer.Channel(0)
        self.omina = pygame.mixer.Sound("omina.wav")
        self.ominb = pygame.mixer.Sound("ominb.wav")
        self.ominc = pygame.mixer.Sound("ominc.wav")
        self.omind = pygame.mixer.Sound("omind.wav")

    @staticmethod
    def play():
        # Play background music.
        pygame.mixer_music.set_volume(.5)
        pygame.mixer.music.play()
