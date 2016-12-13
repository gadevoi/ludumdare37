#!/usr/bin/env python3
import random

import pygame
from pygame.locals import *
from Plant3D import Plant
import pygame.freetype
from TextBox import TextBox
from PlantGroup import PlantGroup
from NameTag import NameTag
from popup_menu import PopupMenu
import inputbox
from DNA import DNA
from DeadSprite import DeadSprite, RadSprite
from ButtonSprite import ButtonSprite

dnas = [DNA("bush", 15, 0.34, "A", [("A", "[&FL!A]/////'[&FL!A]///////'[&FL!A]", 1),
                                    ("F", "S/////F", 0.33),
                                    ("S", "S[//&&L][//^^L]FS", 0.33),
                                    ("S", "SFS", 0.33),
                                    ("S", "FL", 1),
                                    ("L", "b", 0.1),
                                    ("L", "['''^^{-f+f+f-|-f+f+f}]", 1)]),
        DNA("albertina", 10, 0.8, "/A", [("A", "+['A+b]--//['--L]I['++L]-['Ab]++Ab", .7),
                                    ("A", "I+['A+b]--//['--L]I['++L]-[Ab]++Ab", .3),
                                   ("I", "FS[!//&&L][!//^^L]FS", 1),
                                   ("S", "SFS", 1),
                                   ("L", "['{+f-ff-f+f|+f-ff-f}]", 1),
                                   ("b", "[&&&P'/W////W////W////W////W]", 0.1),
                                   ("P", "FF", 1),
                                   ("W", "['^F][{&&&&-f+f|-f+f}]", 1)]),
        DNA("santiv", 25, 0.33, "A", [("A", "[&SL!A]/////'[&SL!A]///////'[!!^FFL]", 1),
                                    ("F", "S/////F", 0.33),
                                    ("S", "S[\\&&L][//^'A]FS", 0.33),
                                    ("S", "SFS", 0.33),
                                    ("S", "FL", 1),
                                    ("L", "b", 0.1),
                                    ("L", "['''^^{-f+^f^f/ff+ff-|-f+fff+f^f}]", 1)]),
        DNA("lettuce", 2, 1, "A", [("A", "['''&L&LA]/////'['''&L&LA]///////'['''&L&LA]", 1),
                                      ("F", "S/////F", 0.33),
                                      ("S", "S[\\&&L][//^'A]FS", 0.33),
                                      ("S", "SFS", 0.33),
                                      ("S", "FL", 1),
                                      ("L", "b", 0.1),
                                      ("L", "['''^^{-ff+ff+ff-|-ff+ff+ff}]", 1)])
        ]

dna_dict = {}
for dna in dnas:
    dna_dict[dna.name] = dna

plant_pos = [(175, 178),
             (88, 348),
             (173, 458),
             (281, 378),
             (397, 448),
             (531, 450),
             (656, 423),
             (486, 194)]
plant_names = ["plant1",
               "plant2",
               "plant3",
               "plant4",
               "plant5",
               "plant6",
               "plant8",
               "plant9"]

plant_dict = {}

speed = "normal"
speeds = {"fastest" : 50,
          "fast" : 150,
          "normal" : 300,
          "slow" : 500,
          "slowest" : 700}

def main():
    # SETUP
    pygame.init()
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF)
    pygame.display.set_caption("Garden of Eden")

    background = pygame.image.load('bg.png').convert()
    background = background.convert()

    dead_icon = pygame.image.load('dead.png').convert_alpha()

    rad_icon = pygame.image.load('rad.png').convert_alpha()

    font = pygame.freetype.Font("CrimsonText-Regular.ttf", size=16)
    textbox = TextBox(font)

    plants = []

    plants_group = PlantGroup()
    dead_group = pygame.sprite.Group()
    for i in range(len(plant_pos)):
        x, y = plant_pos[i]
        name = plant_names[i]
        p = Plant(x, y, random.choice(dnas))
        p.name = name
        p.tree = ""

        plant_dict[name] = p
        plants.append(p)
        plants_group.add(p)
        dead_group.add(DeadSprite(dead_icon, p))
        dead_group.add(RadSprite(rad_icon, p))

    nametag_group = pygame.sprite.Group()

    button_group = pygame.sprite.Group()
    button_group.add(ButtonSprite("menu", font, 710, 510))


    pygame.mixer.music.load('marsbound.mp3')
    pygame.mixer.music.play(-1)

    introduction(screen, font)
    screen.blit(background, (0, 0))


    TICKEVENT = pygame.USEREVENT+1
    TURNEVENT = pygame.USEREVENT+2
    pygame.time.set_timer(TICKEVENT, speeds[speed])
    pygame.time.set_timer(TURNEVENT, 30)

    α = 0.0
    t = " "
    mouse_x_ref = 0
    last_mouse_buttons = (False, False, False)
    rotating = False
    rotating_plants_group = pygame.sprite.LayeredDirty()

    def rename(plant):
        old_name = p.name
        plant_dict.pop(old_name)

        ok = False
        message = ""

        while not ok:
            new_name = inputbox.ask(screen, "{}new name for {}".format(message, p.name))
            if len(new_name) <= 0:
                message = "empty :( "
            elif new_name in plant_dict.keys():
                message = "already used :( "
            else:
                ok = True
                plant.name = new_name
                plant_dict[new_name] = p
        screen.blit(background, (0,0))
    def kill(plant):
        plant.tree = ""
        plant.energy = 0
    def plant_dna(plant, dna):
        plant.reset(dna)
        plant.name
    def harvest(plant):
        if (plant.has_fruit()):
            new_dna = plant.dna.copy()
            ok = False
            message = ""
            while not ok:
                new_name = inputbox.ask(screen, "{}name for new DNA".format(message))
                if len(new_name) <= 0:
                    message = "empty :( "
                elif new_name in dna_dict.keys():
                    message = "already used :( "
                else:
                    ok = True
                    new_dna.name = new_name
                    dna_dict[new_name] = new_dna
                    dnas.append(new_dna)
                    plant.tree.replace("b", "", 1)

            screen.blit(background, (0,0))
        else:
            textbox.say("{} has no fruit, can't harvest DNA".format(plant.name))

    def cross(fruit, dna):
        if plant.has_fruit():
            new_dna = plant.dna.cross(dna)
            ok = False
            message = ""
            while not ok:
                new_name = inputbox.ask(screen, "{}name for new DNA".format(message))
                if len(new_name) <= 0:
                    message = "empty :( "
                elif new_name in dna_dict.keys():
                    message = "already used :( "
                else:
                    ok = True
                    new_dna.name = new_name
                    dna_dict[new_name] = new_dna
                    dnas.append(new_dna)
                    plant.tree.replace("b", "", 1)

            screen.blit(background, (0,0))
        else:
            textbox.say("{} has no fruit, can't cross DNA".format(plant.name))

    def delete_dna(dna_name):
        dnas.remove(dna_dict.pop(dna_name))
        textbox.say("{} has been deleted".format(dna_name))

    # Event loop
    while 1:
        hovered_plants = [s for s in plants if s.rect.collidepoint(pygame.mouse.get_pos())]

        for event in pygame.event.get():
            if event.type == QUIT:
                return

            elif event.type == USEREVENT and event.code == "MENU":
                if event.name == "set speed...":
                    pygame.time.set_timer(TICKEVENT, speeds[event.text])
                    textbox.say("Speed set to {}".format(event.text))
                elif event.name == "delete DNA ..." and event.text in dna_dict:
                    delete_dna(event.text)
                elif event.text == "rename" and event.name in plant_dict.keys():
                    rename(plant_dict[event.name])
                elif event.text == "kill" and event.name in plant_dict.keys():
                    kill(plant_dict[event.name])
                elif event.text == "harvest" and event.name in plant_dict.keys():
                    harvest(plant_dict[event.name])
                elif len(event.name) > 14 and event.name[:14] == "plant seed to " and event.text in dna_dict:
                    plant_name = event.name[14:-3]
                    seed_name = event.text
                    if plant_name in plant_dict:
                        plant_dna(plant_dict[plant_name], dna_dict[seed_name])
                    else:
                        print(plant_name)
                elif len(event.name) > 6 and event.name[:6] == "cross " and event.text in dna_dict.keys():
                    plant_name = event.name[6:-8]
                    seed_name = event.text
                    print("{} <-> {}".format(plant_name, seed_name))
                    if plant_name in plant_dict:
                        cross(plant_dict[plant_name], dna_dict[seed_name])

            elif event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    rotating = True
                    mouse_pos = pygame.mouse.get_pos()
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                    rotating_plants_group.empty()

                    mouse_x_ref = mouse_pos[0]
                    rotating_plants_group.add(hovered_plants)
                last_mouse_buttons = pygame.mouse.get_pressed()
            elif event.type == MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if hovered_plants and last_mouse_buttons[2]:
                    hovered_plants.sort(key=lambda p: abs(mouse_pos[0] - p.x) + abs(mouse_pos[1] - p.y))
                    plant = hovered_plants[0]
                    PopupMenu(get_menu_data(plant))
                    screen.blit(background, (0,0))

                elif len([s for s in button_group if s.rect.collidepoint(pygame.mouse.get_pos())]) > 0 and last_mouse_buttons[0]:
                    PopupMenu(get_menu_data(None))
                    screen.blit(background, (0, 0))

                rotating = False
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                rotating_plants_group.empty()

            elif event.type == TICKEVENT:
                for p in plants_group:
                    if p.y < 200:
                        p.dna.random_mutation()
                plants_group.update()
                dead_group.update()

        if rotating:
            for p in rotating_plants_group.sprites():
                p.α = (mouse_x_ref - pygame.mouse.get_pos()[0]) / 50
                p.dirty = 1


        #########
        # ERASE #
        #########
        screen.blit(background, textbox.rect, textbox.rect)

        plants_group.clear(screen, background)
        nametag_group.clear(screen, background)
        dead_group.clear(screen, background)

        ########
        # DRAW #
        ########
        plants_group.draw(screen)
        dead_group.draw(screen)
        button_group.draw(screen)


        screen.blit(textbox.surface, textbox.rect)

        nametag_group.empty()
        for p in hovered_plants:
            nametag_group.add(NameTag(p, font))

        nametag_group.update()
        nametag_group.draw(screen)


        pygame.display.flip()

def introduction(screen, font):
    background = pygame.image.load('stars.png').convert()
    screen.blit(background, (0,0))
    text = ["    Nothing tops space as a barren, unnatural environment.",
            "    Astronauts who had no prior interest in gardening spend hours tending experimental ",
            "    greenhouses. \"They are our love,\" said cosmonaut Vladislav Volkov of the tiny ",
            "    flax plants - with which they shared the confines of Salyut 1, the first Soviet space station. ",
            "    At least in orbit, you can look out the window and see the natural world below. ",
            "    On a Mars mission, once astronauts lose sight of Earth, they'll be nothing to see ",
            "    outside the window. \"You'll be bathed in permanent sunlight, so you won't ever see ",
            "    any stars,\" astronaut Andy Thomas explained to me. \"All you'll see is black.\" ",
            "            --Mary Roach.",
            "", "",
            "You were sent on Mars to test the viability of farming on the red planet. ",
            "The hope is that you find a plant that can start the process of making the atmosphere ",
            "breathable. For the moment there is not enough oxygen and you are condemned to stay ",
            "in your single-room space lab. ", "",
            "You have with you the seed of some plants from earth.  Your job is to cross ",
            "them to find the best DNA possible. Once a plant has grown enough, you can ",
            "cross it with one of the DNA strands you collected, giving you a new, mutant, DNA. ",
            "You can also put your plants near the windows. The radiation from the sun will ",
            "cause random mutations in its genome. ",
            "-> Right click on the opening of a flower pot to plant a seed. ",
            "-> Right click on a plant to interact, Left click to rotate it ",
            "-> If it's too slow, you can speed it up with the menu in the bottom right ",
            "", "", "CLICK TO CONTINUE "
            ]
    for i in range(len(text)):
        for j in range(len(text[i])):
            t, r = font.render(text[i][:j], fgcolor=(255, 255, 255))
            screen.blit(background,  r.move(10, 10 + 20*i), r.move(10, 10 + 20*i))
            screen.blit(t, r.move(10, 10 + 20*i))
            pygame.display.flip()
            pygame.time.wait(10)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN or (event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
                return

def get_menu_data(plant):
    dna_names = [dna.name for dna in dnas]
    if plant is None:
        dna_names.insert(0, "delete DNA ")
        return ("menu",
                ("set speed",
                 "fastest",
                 "fast",
                 "normal",
                 "slow",
                 "slowest"),
                tuple(dna_names))
    else:
        if len(plant.tree) > 0:
            dna_names.insert(0, "cross {} with".format(plant.name))
            return (plant.name,
                    "rename",
                    tuple(dna_names),
                    "harvest",
                    "kill")
        else:
            dna_names.insert(0, "plant seed to {}".format(plant.name))
            return (plant.name,
                    tuple(
                        dna_names
                    ))


if __name__ == '__main__':
    main()
