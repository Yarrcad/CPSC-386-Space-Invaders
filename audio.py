import pygame


class Audio:
    def __init__(self):
        # Create mixer for audio.
        pygame.mixer.init()
        pygame.mixer.set_num_channels(5)
        self.oscia = pygame.mixer.Channel(1)
        self.oscib = pygame.mixer.Sound("audio/osci.wav")
        self.exploa = pygame.mixer.Channel(2)
        self.explob = pygame.mixer.Sound("audio/explo.wav")
        self.pewa = pygame.mixer.Channel(4)
        self.pewb = pygame.mixer.Sound("audio/pew.wav")
        self.omin = pygame.mixer.Channel(0)
        self.omina = pygame.mixer.Sound("audio/omina.wav")
        self.ominb = pygame.mixer.Sound("audio/ominb.wav")
        self.ominc = pygame.mixer.Sound("audio/ominc.wav")
        self.omind = pygame.mixer.Sound("audio/omind.wav")

    @staticmethod
    def play():
        # Play background music.
        pygame.mixer_music.set_volume(.5)
        pygame.mixer.music.play()
