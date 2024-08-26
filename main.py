import pygame
from pygame.locals import *
from sys import exit
import time
from intro import run_intro
from scene01 import run_corridor_scene
from screen_manager import screen

def main():
    run_intro()
    run_corridor_scene()

if __name__ == "__main__":
    main()

