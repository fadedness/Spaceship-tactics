# -*- coding: utf-8 -*-
# mini tactics game in development
# version 0.5
# by @fadedness (telegram)
# uses kivy
# https://github.com/fadedness/Spaceship-tactics
# game assets are from:
#                                   Credits:
# Includes free-to-use assets:
# Spaceship images and animations are from https://craftpix.net/file-licenses/ under freebie license
# Background space images are from Pexels (https://www.pexels.com/license/)
# by Adam Krypel, Hristo Fidanov, Alberlan Barros, Ludvig Hedenborg
# one from Free Nature Stock (https://freenaturestock.com/)
# two from Pixabay (https://pixabay.com/service/license/) by Kalhh-86169 and WikiImages-1897
# Sound effects are from https://www.zapsplat.com/license-type/standard-license/
# Game was inspired: first of all by Heroes of Might and Magic 3, secondly by Galaxy Online MMO (https://galaxyonline.io)
# The idea to mix these two games is by Andrei @a_investorpractice


from kivy.config import Config
Config.set("graphics", "width", "1024")#"200")#"1024")
Config.set("graphics", "height", "768")
Config.set("graphics", "resizable", 0)

import kivy 
kivy.require("2.0.0")
import functools
from time import sleep
from language_rus import text_strings
current_language = ["Russian"]
import random
from kivy.app import App
from kivy import platform
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
#from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.vector import Vector
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty, ReferenceListProperty, ListProperty, BooleanProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.graphics import Rectangle, Ellipse, PushMatrix, PopMatrix, Rotate
from kivy.animation import Animation

list_of_ship_images = ["images/ship2.png", "images/ship3.png", "images/ship4.png", "images/ship5.png", "images/ship6.png"]
empty_image = "images/empty.png"
laser_color = "F84646"
kinetic_color = "29BC94"
plasma_color = "4183D7"
rocket_color = "EBB237"
rail_color = "9977FF"
hex_grid_coords = [[((1, 1), 25.0, 200.0), ((1, 2), 127.0, 200.0), ((1, 3), 229.0, 200.0), ((1, 4), 331.0, 200.0), ((1, 5), 433.0, 200.0), ((1, 6), 535.0, 200.0), ((1, 7), 637.0, 200.0), ((1, 8), 739.0, 200.0), ((1, 9), 841.0, 200.0)], [((2, 1), 0.0, 277.0), ((2, 2), 102.0, 277.0), ((2, 3), 204.0, 277.0), ((2, 4), 306.0, 277.0), ((2, 5), 408.0, 277.0), ((2, 6), 510.0, 277.0), ((2, 7), 612.0, 277.0), ((2, 8), 714.0, 277.0), ((2, 9), 816.0, 277.0), ((2, 10), 918.0, 277.0)], [((3, 1), 25.0, 354.0), ((3, 2), 127.0, 354.0), ((3, 3), 229.0, 354.0), ((3, 4), 331.0, 354.0), ((3, 5), 433.0, 354.0), ((3, 6), 535.0, 354.0), ((3, 7), 637.0, 354.0), ((3, 8), 739.0, 354.0), ((3, 9), 841.0, 354.0)], [((4, 1), 0.0, 431.0), ((4, 2), 102.0, 431.0), ((4, 3), 204.0, 431.0), ((4, 4), 306.0, 431.0), ((4, 5), 408.0, 431.0), ((4, 6), 510.0, 431.0), ((4, 7), 612.0, 431.0), ((4, 8), 714.0, 431.0), ((4, 9), 816.0, 431.0), ((4, 10), 918.0, 431.0)], [((5, 1), 25.0, 508.0), ((5, 2), 127.0, 508.0), ((5, 3), 229.0, 508.0), ((5, 4), 331.0, 508.0), ((5, 5), 433.0, 508.0), ((5, 6), 535.0, 508.0), ((5, 7), 637.0, 508.0), ((5, 8), 739.0, 508.0), ((5, 9), 841.0, 508.0)], [((6, 1), 0.0, 585.0), ((6, 2), 102.0, 585.0), ((6, 3), 204.0, 585.0), ((6, 4), 306.0, 585.0), ((6, 5), 408.0, 585.0), ((6, 6), 510.0, 585.0), ((6, 7), 612.0, 585.0), ((6, 8), 714.0, 585.0), ((6, 9), 816.0, 585.0), ((6, 10), 918.0, 585.0)], [((7, 1), 25.0, 662.0), ((7, 2), 127.0, 662.0), ((7, 3), 229.0, 662.0), ((7, 4), 331.0, 662.0), ((7, 5), 433.0, 662.0), ((7, 6), 535.0, 662.0), ((7, 7), 637.0, 662.0), ((7, 8), 739.0, 662.0), ((7, 9), 841.0, 662.0)]]

hex_grid_coords_for_kv = [[(53.0, 203.0), (155.0, 203.0), (257.0, 203.0), (359.0, 203.0), (461.0, 203.0), (563.0, 203.0), (665.0, 203.0), (767.0, 203.0), (869.0, 203.0)], [(3.0, 280.0), (105.0, 280.0), (207.0, 280.0), (309.0, 280.0), (411.0, 280.0), (513.0, 280.0), (615.0, 280.0), (717.0, 280.0), (819.0, 280.0), (921.0, 280.0)], [(53.0, 357.0), (155.0, 357.0), (257.0, 357.0), (359.0, 357.0), (461.0, 357.0), (563.0, 357.0), (665.0, 357.0), (767.0, 357.0), (869.0, 357.0)], [(3.0, 434.0), (105.0, 434.0), (207.0, 434.0), (309.0, 434.0), (411.0, 434.0), (513.0, 434.0), (615.0, 434.0), (717.0, 434.0), (819.0, 434.0), (921.0, 434.0)], [(53.0, 511.0), (155.0, 511.0), (257.0, 511.0), (359.0, 511.0), (461.0, 511.0), (563.0, 511.0), (665.0, 511.0), (767.0, 511.0), (869.0, 511.0)], [(3.0, 588.0), (105.0, 588.0), (207.0, 588.0), (309.0, 588.0), (411.0, 588.0), (513.0, 588.0), (615.0, 588.0), (717.0, 588.0), (819.0, 588.0), (921.0, 588.0)], [(53.0, 665.0), (155.0, 665.0), (257.0, 665.0), (359.0, 665.0), (461.0, 665.0), (563.0, 665.0), (665.0, 665.0), (767.0, 665.0), (869.0, 665.0)]]

hex_grid_ids_and_states = [[] for i in range(7)]
for i in range(len(hex_grid_ids_and_states)):
    if i == 0:
        max_j = 9
    elif i % 2 != 0:
        max_j = 10
    else:
        max_j = 9
    for j in range(max_j):
        hex_grid_ids_and_states[i].append([])
        hex_grid_ids_and_states[i][j].append((i, j))   #   0   # coord or id
        hex_grid_ids_and_states[i][j].append(False)    #   1   # state of in range
        hex_grid_ids_and_states[i][j].append(False)    #   2   # state of highlighted
        hex_grid_ids_and_states[i][j].append(False)    #   3   # state of occupied by your ships
        hex_grid_ids_and_states[i][j].append(False)    #   4   # state of occupied by enemy ships
        hex_grid_ids_and_states[i][j].append(False)    #   5   # state of selected
        hex_grid_ids_and_states[i][j].append(False)    #   6   # state of in weapon range
print(hex_grid_ids_and_states)

class Ship():
    def __init__(self, name, s_id, price, attack, defense, weapon_range, accuracy, speed, movement, attack_type, defense_laser, defense_kinetic, defense_plasma, defense_rocket, defense_rail, move_and_shoot, imagefile, mirror_imagefile):
        self.name = name
        self.s_id = s_id
        self.price = price
        self.attack = attack
        self.defense = defense
        self.weapon_range = weapon_range
        self.accuracy = accuracy
        self.speed = speed
        self.movement = movement
        self.attack_type = attack_type
        self.defense_laser = defense_laser
        self.defense_kinetic = defense_kinetic
        self.defense_plasma = defense_plasma
        self.defense_rocket = defense_rocket
        self.defense_rail = defense_rail
        self.move_and_shoot = move_and_shoot
        self.imagefile = imagefile
        self.mirror_imagefile = mirror_imagefile
        self.image = Image(source = self.imagefile)
        self.image.size_hint = (None, None)
        self.size_x = 100
        self.size_y = 100
    def set_stat_text_card(self, name):
        loc_price = text_strings.price
        loc_damage = text_strings.damage[0]
        loc_defense = text_strings.defense[0]
        loc_defense_ = text_strings.defense[1]
        loc_weapon_range = text_strings.weapon_range
        loc_accuracy = text_strings.accuracy
        loc_speed = text_strings.speed
        loc_movement_range = text_strings.movement_range
        loc_move_and_shoot_true = text_strings.move_and_shoot_true
        loc_move_and_shoot_false = text_strings.move_and_shoot_false
        if self.attack_type == 0:
            loc_damage_type = text_strings.laser_damage_type[1]
            loc_damage_type_ = text_strings.laser_damage_type[0]
            loc_damage_type_color = laser_color
        elif self.attack_type == 1:
            loc_damage_type = text_strings.kinetic_damage_type[1]
            loc_damage_type_ = text_strings.kinetic_damage_type[0]
            loc_damage_type_color = kinetic_color
        elif self.attack_type == 2:
            loc_damage_type = text_strings.plasma_damage_type[1]
            loc_damage_type_ = text_strings.plasma_damage_type[0]
            loc_damage_type_color = plasma_color
        elif self.attack_type == 3:
            loc_damage_type = text_strings.rocket_damage_type[1]
            loc_damage_type_ = text_strings.rocket_damage_type[0]
            loc_damage_type_color = rocket_color
        elif self.attack_type == 4:
            loc_damage_type = text_strings.rail_damage_type[1]
            loc_damage_type_ = text_strings.rail_damage_type[0]
            loc_damage_type_color = rail_color
        if self.defense_laser == 100:
            loc_defense_color = laser_color
        elif self.defense_kinetic == 100:
            loc_defense_color = kinetic_color
        elif self.defense_plasma == 100:
            loc_defense_color = plasma_color
        elif self.defense_rocket == 100:
            loc_defense_color = rocket_color
        elif self.defense_rail == 100:
            loc_defense_color = rail_color
        #loc_defense_laser = text_strings.defense[1] + " " + text_strings.against + " " + text_strings.laser_damage_type[1] + " " + text_strings.damage[1]
        #loc_defense_kinetic = text_strings.defense[1] + " " + text_strings.against + " " + text_strings.kinetic_damage_type[1] + " " + text_strings.damage[1]
        #loc_defense_plasma = text_strings.defense[1] + " " + text_strings.against + " " + text_strings.plasma_damage_type[1] + " " + text_strings.damage[1]
        #loc_defense_rocket = text_strings.defense[1] + " " + text_strings.against + " " + text_strings.rocket_damage_type[1] + " " + text_strings.damage[1]
        #loc_defense_rail = text_strings.defense[1] + " " + text_strings.against + " " + text_strings.rail_damage_type[1] + " " + text_strings.damage[1]
        #loc_defense_laser = text_strings.from_ + " " + text_strings.laser_damage_type[1]
        #loc_defense_kinetic = text_strings.from_ + " " + text_strings.kinetic_damage_type[1]
        #loc_defense_plasma = text_strings.from_ + " " + text_strings.plasma_damage_type[1]
        #loc_defense_rocket = text_strings.from_ + " " + text_strings.rocket_damage_type[1]
        #loc_defense_rail = text_strings.from_ + " " + text_strings.rail_damage_type[1]
        self.stat_text_card_1 = "[b]%s[/b]\n%s: %s\n[color=#%s]%s: %s[/color]\n[color=#%s]%s: %s\n%s[/color]" % (name, loc_price, self.price, loc_damage_type_color, loc_damage, self.attack, loc_defense_color, loc_defense, self.defense, loc_damage_type_)
        if self.move_and_shoot == True:
            move_and_shoot_text = loc_move_and_shoot_true
        else:
            move_and_shoot_text = loc_move_and_shoot_false
        self.stat_text_card_2 = "%s: %s%%\n%s: %s\n%s: %s\n%s: %s\n%s" % (loc_accuracy, self.accuracy, loc_weapon_range, self.weapon_range, loc_speed, self.speed, loc_movement_range, self.movement, move_and_shoot_text)
        self.stat_text_card_3 = "[color=#%s]%s%% %s[/color]\n[color=#%s]%s%% %s[/color]\n[color=#%s]%s%% %s[/color]\n[color=#%s]%s%% %s[/color]\n[color=#%s]%s%% %s[/color]" % (laser_color, self.defense_laser, loc_defense_, kinetic_color, self.defense_kinetic, loc_defense_, plasma_color, self.defense_plasma, loc_defense_, rocket_color, self.defense_rocket, loc_defense_, rail_color, self.defense_rail, loc_defense_)

Light_Fighter = Ship(text_strings.light_fighter, 0, 500, 5, 55, 3, 80, 8, 5, 2, 60, 80, 100, 120, 140, True, "images/ship2.png", "images/z_ship2.png")
Heavy_Fighter = Ship(text_strings.heavy_fighter, 1, 1000, 11, 90, 4, 80, 7, 4, 0, 100, 60, 140, 80, 120, True, "images/ship3.png", "images/z_ship3.png")
Frigate = Ship(text_strings.frigate, 2, 1500, 15, 150, 5, 80, 6, 3, 1, 140, 100, 120, 60, 80, True, "images/ship4.png", "images/z_ship4.png")
Cruiser = Ship(text_strings.cruiser, 3, 2500, 22, 275, 6, 80, 5, 2, 3, 120, 140, 80, 100, 60, False, "images/ship5.png", "images/z_ship5.png")
Dreadnought = Ship(text_strings.dreadnought, 4, 4000, 44, 360, 7, 80, 4, 1, 4, 80, 120, 60, 140, 100, False, "images/ship6.png", "images/z_ship6.png")

# Balancing damage
Light_Fighter.attack = 18
Heavy_Fighter.attack = 44
Frigate.attack = 60
Cruiser.attack = 90
Dreadnought.attack = 176

Cruiser.weapon_range = 7
Dreadnought.weapon_range = 8

Light_Fighter.set_stat_text_card(text_strings.light_fighter)
Heavy_Fighter.set_stat_text_card(text_strings.heavy_fighter)
Frigate.set_stat_text_card(text_strings.frigate)
Cruiser.set_stat_text_card(text_strings.cruiser)
Dreadnought.set_stat_text_card(text_strings.dreadnought)
listofships = []
listofships.append(Light_Fighter)
listofships.append(Heavy_Fighter)
listofships.append(Frigate)
listofships.append(Cruiser)
listofships.append(Dreadnought)

def _set_animation_lists_projectile_shoot():
    my_list = []
    my_list.append(["images/animation/projectile_shoot/ship2/shot2_1.png", "images/animation/projectile_shoot/ship2/shot2_2.png", "images/animation/projectile_shoot/ship2/shot2_3.png", "images/animation/projectile_shoot/ship2/shot2_4.png", "images/animation/projectile_shoot/ship2/shot2_5.png", "images/animation/projectile_shoot/ship2/shot2_6.png"])
    my_list.append(["images/animation/projectile_shoot/ship3/shot3_1.png", "images/animation/projectile_shoot/ship3/shot3_2.png", "images/animation/projectile_shoot/ship3/shot3_3.png"])
    my_list.append(["images/animation/projectile_shoot/ship4/shot4_1.png", "images/animation/projectile_shoot/ship4/shot4_2.png", "images/animation/projectile_shoot/ship4/shot4_3.png", "images/animation/projectile_shoot/ship4/shot4_4.png", "images/animation/projectile_shoot/ship4/shot4_5.png"])
    my_list.append(["images/animation/projectile_shoot/ship5/shot5_1.png", "images/animation/projectile_shoot/ship5/shot5_2.png", "images/animation/projectile_shoot/ship5/shot5_3.png", "images/animation/projectile_shoot/ship5/shot5_4.png", "images/animation/projectile_shoot/ship5/shot5_5.png"])
    my_list.append(["images/animation/projectile_shoot/ship6/shot6_1.png", "images/animation/projectile_shoot/ship6/shot6_1.png", "images/animation/projectile_shoot/ship6/shot6_2.png", "images/animation/projectile_shoot/ship6/shot6_3.png", "images/animation/projectile_shoot/ship6/shot6_4.png"])
    my_list.append(["images/animation/projectile_shoot/ship2/z_shot2_1.png", "images/animation/projectile_shoot/ship2/z_shot2_2.png", "images/animation/projectile_shoot/ship2/z_shot2_3.png", "images/animation/projectile_shoot/ship2/z_shot2_4.png", "images/animation/projectile_shoot/ship2/z_shot2_5.png", "images/animation/projectile_shoot/ship2/z_shot2_6.png"])
    my_list.append(["images/animation/projectile_shoot/ship3/z_shot3_1.png", "images/animation/projectile_shoot/ship3/z_shot3_2.png", "images/animation/projectile_shoot/ship3/z_shot3_3.png"])
    my_list.append(["images/animation/projectile_shoot/ship4/z_shot4_1.png", "images/animation/projectile_shoot/ship4/z_shot4_2.png", "images/animation/projectile_shoot/ship4/z_shot4_3.png", "images/animation/projectile_shoot/ship4/z_shot4_4.png", "images/animation/projectile_shoot/ship4/z_shot4_5.png"])
    my_list.append(["images/animation/projectile_shoot/ship5/z_shot5_1.png", "images/animation/projectile_shoot/ship5/z_shot5_2.png", "images/animation/projectile_shoot/ship5/z_shot5_3.png", "images/animation/projectile_shoot/ship5/z_shot5_4.png", "images/animation/projectile_shoot/ship5/z_shot5_5.png"])
    my_list.append(["images/animation/projectile_shoot/ship6/shot6_1.png", "images/animation/projectile_shoot/ship6/z_shot6_1.png", "images/animation/projectile_shoot/ship6/z_shot6_2.png", "images/animation/projectile_shoot/ship6/z_shot6_3.png", "images/animation/projectile_shoot/ship6/z_shot6_4.png"])
    return my_list

def _set_animation_lists_projectile_move():
    my_list = []
    my_list.append(["images/animation/projectile_move/ship2/shot2_asset.png"])
    my_list.append(["images/animation/projectile_move/ship3/shot3_asset.png"])
    my_list.append(["images/animation/projectile_move/ship4/shot4_asset.png"])
    my_list.append(["images/animation/projectile_move/ship5/shot5_asset.png"])
    my_list.append(["images/animation/projectile_move/ship6/shot6_asset.png"])
    my_list.append(["images/animation/projectile_move/ship2/z_shot2_asset.png"])
    my_list.append(["images/animation/projectile_move/ship3/z_shot3_asset.png"])
    my_list.append(["images/animation/projectile_move/ship4/z_shot4_asset.png"])
    my_list.append(["images/animation/projectile_move/ship5/z_shot5_asset.png"])
    my_list.append(["images/animation/projectile_move/ship6/z_shot6_asset.png"])
    return my_list

def _set_animation_lists_projectile_hit():
    my_list = []
    my_list.append(["images/animation/projectile_hit/ship2/shot2_exp1.png", "images/animation/projectile_hit/ship2/shot2_exp2.png", "images/animation/projectile_hit/ship2/shot2_exp3.png", "images/animation/projectile_hit/ship2/shot2_exp4.png", "images/animation/projectile_hit/ship2/shot2_exp5.png"])
    my_list.append(["images/animation/projectile_hit/ship3/shot3_exp1.png", "images/animation/projectile_hit/ship3/shot3_exp2.png", "images/animation/projectile_hit/ship3/shot3_exp3.png", "images/animation/projectile_hit/ship3/shot3_exp4.png"])
    my_list.append(["images/animation/projectile_hit/ship4/shot4_exp1.png", "images/animation/projectile_hit/ship4/shot4_exp2.png", "images/animation/projectile_hit/ship4/shot4_exp3.png", "images/animation/projectile_hit/ship4/shot4_exp4.png", "images/animation/projectile_hit/ship4/shot4_exp5.png", "images/animation/projectile_hit/ship4/shot4_exp6.png", "images/animation/projectile_hit/ship4/shot4_exp7.png", "images/animation/projectile_hit/ship4/shot4_exp8.png"])
    my_list.append(["images/animation/projectile_hit/ship5/shot5_exp1.png", "images/animation/projectile_hit/ship5/shot5_exp2.png", "images/animation/projectile_hit/ship5/shot5_exp3.png", "images/animation/projectile_hit/ship5/shot5_exp4.png", "images/animation/projectile_hit/ship5/shot5_exp5.png", "images/animation/projectile_hit/ship5/shot5_exp6.png", "images/animation/projectile_hit/ship5/shot5_exp7.png", "images/animation/projectile_hit/ship5/shot5_exp8.png"])
    my_list.append(["images/animation/projectile_hit/ship6/shot6_exp1.png", "images/animation/projectile_hit/ship6/shot6_exp2.png", "images/animation/projectile_hit/ship6/shot6_exp3.png", "images/animation/projectile_hit/ship6/shot6_exp4.png", "images/animation/projectile_hit/ship6/shot6_exp5.png", "images/animation/projectile_hit/ship6/shot6_exp6.png", "images/animation/projectile_hit/ship6/shot6_exp7.png", "images/animation/projectile_hit/ship6/shot6_exp8.png", "images/animation/projectile_hit/ship6/shot6_exp9.png", "images/animation/projectile_hit/ship6/shot6_exp10.png"])
    my_list.append(["images/animation/projectile_hit/ship2/z_shot2_exp1.png", "images/animation/projectile_hit/ship2/z_shot2_exp2.png", "images/animation/projectile_hit/ship2/z_shot2_exp3.png", "images/animation/projectile_hit/ship2/z_shot2_exp4.png", "images/animation/projectile_hit/ship2/z_shot2_exp5.png"])
    my_list.append(["images/animation/projectile_hit/ship3/z_shot3_exp1.png", "images/animation/projectile_hit/ship3/z_shot3_exp2.png", "images/animation/projectile_hit/ship3/z_shot3_exp3.png", "images/animation/projectile_hit/ship3/z_shot3_exp4.png"])
    my_list.append(["images/animation/projectile_hit/ship4/z_shot4_exp1.png", "images/animation/projectile_hit/ship4/z_shot4_exp2.png", "images/animation/projectile_hit/ship4/z_shot4_exp3.png", "images/animation/projectile_hit/ship4/z_shot4_exp4.png", "images/animation/projectile_hit/ship4/z_shot4_exp5.png", "images/animation/projectile_hit/ship4/z_shot4_exp6.png", "images/animation/projectile_hit/ship4/z_shot4_exp7.png", "images/animation/projectile_hit/ship4/z_shot4_exp8.png"])
    my_list.append(["images/animation/projectile_hit/ship5/z_shot5_exp1.png", "images/animation/projectile_hit/ship5/z_shot5_exp2.png", "images/animation/projectile_hit/ship5/z_shot5_exp3.png", "images/animation/projectile_hit/ship5/z_shot5_exp4.png", "images/animation/projectile_hit/ship5/z_shot5_exp5.png", "images/animation/projectile_hit/ship5/z_shot5_exp6.png", "images/animation/projectile_hit/ship5/z_shot5_exp7.png", "images/animation/projectile_hit/ship5/z_shot5_exp8.png"])
    my_list.append(["images/animation/projectile_hit/ship6/z_shot6_exp1.png", "images/animation/projectile_hit/ship6/z_shot6_exp2.png", "images/animation/projectile_hit/ship6/z_shot6_exp3.png", "images/animation/projectile_hit/ship6/z_shot6_exp4.png", "images/animation/projectile_hit/ship6/z_shot6_exp5.png", "images/animation/projectile_hit/ship6/z_shot6_exp6.png", "images/animation/projectile_hit/ship6/z_shot6_exp7.png", "images/animation/projectile_hit/ship6/z_shot6_exp8.png", "images/animation/projectile_hit/ship6/z_shot6_exp9.png", "images/animation/projectile_hit/ship6/z_shot6_exp10.png"])
    return my_list

def _set_animation_lists_ship_destroyed():
    my_list = []
    my_list.append(["images/animation/ship_destroyed/ship2/Ship2_Explosion_000.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_004.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_005.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_008.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_009.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_010.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_013.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_014.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_015.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_016.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_019.png", "images/animation/ship_destroyed/ship2/Ship2_Explosion_021.png"])
    my_list.append(["images/animation/ship_destroyed/ship3/Ship3_Explosion_000.png", "images/animation/ship_destroyed/ship3/Ship3_Explosion_004.png", "images/animation/ship_destroyed/ship3/Ship3_Explosion_005.png", "images/animation/ship_destroyed/ship3/Ship3_Explosion_007.png", "images/animation/ship_destroyed/ship3/Ship3_Explosion_009.png", "images/animation/ship_destroyed/ship3/Ship3_Explosion_012.png", "images/animation/ship_destroyed/ship3/Ship3_Explosion_013.png", "images/animation/ship_destroyed/ship3/Ship3_Explosion_015.png", "images/animation/ship_destroyed/ship3/Ship3_Explosion_018.png", "images/animation/ship_destroyed/ship3/Ship3_Explosion_019.png", "images/animation/ship_destroyed/ship3/Ship3_Explosion_021.png"])
    my_list.append(["images/animation/ship_destroyed/ship4/Ship4_Explosion_000.png", "images/animation/ship_destroyed/ship4/Ship4_Explosion_003.png", "images/animation/ship_destroyed/ship4/Ship4_Explosion_005.png", "images/animation/ship_destroyed/ship4/Ship4_Explosion_007.png", "images/animation/ship_destroyed/ship4/Ship4_Explosion_008.png", "images/animation/ship_destroyed/ship4/Ship4_Explosion_012.png", "images/animation/ship_destroyed/ship4/Ship4_Explosion_013.png", "images/animation/ship_destroyed/ship4/Ship4_Explosion_015.png", "images/animation/ship_destroyed/ship4/Ship4_Explosion_018.png", "images/animation/ship_destroyed/ship4/Ship4_Explosion_019.png", "images/animation/ship_destroyed/ship4/Ship4_Explosion_020.png"])
    my_list.append(["images/animation/ship_destroyed/ship5/Ship5_Explosion_001.png", "images/animation/ship_destroyed/ship5/Ship5_Explosion_003.png", "images/animation/ship_destroyed/ship5/Ship5_Explosion_006.png", "images/animation/ship_destroyed/ship5/Ship5_Explosion_007.png", "images/animation/ship_destroyed/ship5/Ship5_Explosion_008.png", "images/animation/ship_destroyed/ship5/Ship5_Explosion_011.png", "images/animation/ship_destroyed/ship5/Ship5_Explosion_013.png", "images/animation/ship_destroyed/ship5/Ship5_Explosion_014.png", "images/animation/ship_destroyed/ship5/Ship5_Explosion_017.png", "images/animation/ship_destroyed/ship5/Ship5_Explosion_019.png", "images/animation/ship_destroyed/ship5/Ship5_Explosion_020.png"])
    my_list.append(["images/animation/ship_destroyed/ship6/Ship6_Explosion_000.png", "images/animation/ship_destroyed/ship6/Ship6_Explosion_004.png", "images/animation/ship_destroyed/ship6/Ship6_Explosion_005.png", "images/animation/ship_destroyed/ship6/Ship6_Explosion_007.png", "images/animation/ship_destroyed/ship6/Ship6_Explosion_009.png", "images/animation/ship_destroyed/ship6/Ship6_Explosion_011.png", "images/animation/ship_destroyed/ship6/Ship6_Explosion_013.png", "images/animation/ship_destroyed/ship6/Ship6_Explosion_016.png", "images/animation/ship_destroyed/ship6/Ship6_Explosion_017.png", "images/animation/ship_destroyed/ship6/Ship6_Explosion_019.png", "images/animation/ship_destroyed/ship6/Ship6_Explosion_021.png"])
    my_list.append(["images/animation/ship_destroyed/ship2/z_Ship2_Explosion_000.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_004.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_005.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_008.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_009.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_010.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_013.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_014.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_015.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_016.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_019.png", "images/animation/ship_destroyed/ship2/z_Ship2_Explosion_021.png"])
    my_list.append(["images/animation/ship_destroyed/ship3/z_Ship3_Explosion_000.png", "images/animation/ship_destroyed/ship3/z_Ship3_Explosion_004.png", "images/animation/ship_destroyed/ship3/z_Ship3_Explosion_005.png", "images/animation/ship_destroyed/ship3/z_Ship3_Explosion_007.png", "images/animation/ship_destroyed/ship3/z_Ship3_Explosion_009.png", "images/animation/ship_destroyed/ship3/z_Ship3_Explosion_012.png", "images/animation/ship_destroyed/ship3/z_Ship3_Explosion_013.png", "images/animation/ship_destroyed/ship3/z_Ship3_Explosion_015.png", "images/animation/ship_destroyed/ship3/z_Ship3_Explosion_018.png", "images/animation/ship_destroyed/ship3/z_Ship3_Explosion_019.png", "images/animation/ship_destroyed/ship3/z_Ship3_Explosion_021.png"])
    my_list.append(["images/animation/ship_destroyed/ship4/z_Ship4_Explosion_000.png", "images/animation/ship_destroyed/ship4/z_Ship4_Explosion_003.png", "images/animation/ship_destroyed/ship4/z_Ship4_Explosion_005.png", "images/animation/ship_destroyed/ship4/z_Ship4_Explosion_007.png", "images/animation/ship_destroyed/ship4/z_Ship4_Explosion_008.png", "images/animation/ship_destroyed/ship4/z_Ship4_Explosion_012.png", "images/animation/ship_destroyed/ship4/z_Ship4_Explosion_013.png", "images/animation/ship_destroyed/ship4/z_Ship4_Explosion_015.png", "images/animation/ship_destroyed/ship4/z_Ship4_Explosion_018.png", "images/animation/ship_destroyed/ship4/z_Ship4_Explosion_019.png", "images/animation/ship_destroyed/ship4/z_Ship4_Explosion_020.png"])
    my_list.append(["images/animation/ship_destroyed/ship5/z_Ship5_Explosion_001.png", "images/animation/ship_destroyed/ship5/z_Ship5_Explosion_003.png", "images/animation/ship_destroyed/ship5/z_Ship5_Explosion_006.png", "images/animation/ship_destroyed/ship5/z_Ship5_Explosion_007.png", "images/animation/ship_destroyed/ship5/z_Ship5_Explosion_008.png", "images/animation/ship_destroyed/ship5/z_Ship5_Explosion_011.png", "images/animation/ship_destroyed/ship5/z_Ship5_Explosion_013.png", "images/animation/ship_destroyed/ship5/z_Ship5_Explosion_014.png", "images/animation/ship_destroyed/ship5/z_Ship5_Explosion_017.png", "images/animation/ship_destroyed/ship5/z_Ship5_Explosion_019.png", "images/animation/ship_destroyed/ship5/z_Ship5_Explosion_020.png"])
    my_list.append(["images/animation/ship_destroyed/ship6/z_Ship6_Explosion_000.png", "images/animation/ship_destroyed/ship6/z_Ship6_Explosion_004.png", "images/animation/ship_destroyed/ship6/z_Ship6_Explosion_005.png", "images/animation/ship_destroyed/ship6/z_Ship6_Explosion_007.png", "images/animation/ship_destroyed/ship6/z_Ship6_Explosion_009.png", "images/animation/ship_destroyed/ship6/z_Ship6_Explosion_011.png", "images/animation/ship_destroyed/ship6/z_Ship6_Explosion_013.png", "images/animation/ship_destroyed/ship6/z_Ship6_Explosion_016.png", "images/animation/ship_destroyed/ship6/z_Ship6_Explosion_017.png", "images/animation/ship_destroyed/ship6/z_Ship6_Explosion_019.png", "images/animation/ship_destroyed/ship6/z_Ship6_Explosion_021.png"])
    return my_list

# not used
def _set_animation_lists_ship_move():
    my_list = []
    my_list.append(["images/animation/ship_move/ship2/Ship2_normal_flight_001.png", "images/animation/ship_move/ship2/Ship2_normal_flight_003.png", "images/animation/ship_move/ship2/Ship2_normal_flight_005.png", "images/animation/ship_move/ship2/Ship2_normal_flight_007.png"])
    my_list.append(["images/animation/ship_move/ship3/Ship3_normal_flight_001.png", "images/animation/ship_move/ship3/Ship3_normal_flight_003.png", "images/animation/ship_move/ship3/Ship3_normal_flight_005.png", "images/animation/ship_move/ship3/Ship3_normal_flight_007.png"])
    my_list.append(["images/animation/ship_move/ship4/Ship4_normal_flight_001.png", "images/animation/ship_move/ship4/Ship4_normal_flight_003.png", "images/animation/ship_move/ship4/Ship4_normal_flight_004.png", "images/animation/ship_move/ship4/Ship4_normal_flight_006.png"])
    my_list.append(["images/animation/ship_move/ship5/Ship5_normal_flight_002.png", "images/animation/ship_move/ship5/Ship5_normal_flight_003.png", "images/animation/ship_move/ship5/Ship5_normal_flight_004.png", "images/animation/ship_move/ship5/Ship5_normal_flight_006.png"])
    my_list.append(["images/animation/ship_move/ship6/Ship6_normal_flight_000.png", "images/animation/ship_move/ship6/Ship6_normal_flight_002.png", "images/animation/ship_move/ship6/Ship6_normal_flight_004.png", "images/animation/ship_move/ship6/Ship6_normal_flight_006.png"])
    my_list.append(["images/animation/ship_move/ship2/z_Ship2_normal_flight_001.png", "images/animation/ship_move/ship2/z_Ship2_normal_flight_003.png", "images/animation/ship_move/ship2/z_Ship2_normal_flight_005.png", "images/animation/ship_move/ship2/z_Ship2_normal_flight_007.png"])
    my_list.append(["images/animation/ship_move/ship3/z_Ship3_normal_flight_001.png", "images/animation/ship_move/ship3/z_Ship3_normal_flight_003.png", "images/animation/ship_move/ship3/z_Ship3_normal_flight_005.png", "images/animation/ship_move/ship3/z_Ship3_normal_flight_007.png"])
    my_list.append(["images/animation/ship_move/ship4/z_Ship4_normal_flight_001.png", "images/animation/ship_move/ship4/z_Ship4_normal_flight_003.png", "images/animation/ship_move/ship4/z_Ship4_normal_flight_004.png", "images/animation/ship_move/ship4/z_Ship4_normal_flight_006.png"])
    my_list.append(["images/animation/ship_move/ship5/z_Ship5_normal_flight_002.png", "images/animation/ship_move/ship5/z_Ship5_normal_flight_003.png", "images/animation/ship_move/ship5/z_Ship5_normal_flight_004.png", "images/animation/ship_move/ship5/z_Ship5_normal_flight_006.png"])
    my_list.append(["images/animation/ship_move/ship6/z_Ship6_normal_flight_000.png", "images/animation/ship_move/ship6/z_Ship6_normal_flight_002.png", "images/animation/ship_move/ship6/z_Ship6_normal_flight_004.png", "images/animation/ship_move/ship6/z_Ship6_normal_flight_006.png"])
    return my_list

def _set_animation_list_offset_projectile_shoot():
    my_list = []
    my_list.append((53, -4))
    my_list.append((40, -4))
    my_list.append((60, -10))
    my_list.append((55, -7))
    my_list.append((50, -9))
    my_list.append((-60, -4))
    my_list.append((-70, -4))
    my_list.append((-60, -10))
    my_list.append((-70, -7))
    my_list.append((-70, -7))
    return my_list

def _set_animation_list_offset_projectile_move():
    my_list = []
    my_list.append((3, -4))
    my_list.append((-10, -4))
    my_list.append((15, -10))
    my_list.append((5, -4))
    my_list.append((0, -4))
    my_list.append((-15, -4))
    my_list.append((5, -4))
    my_list.append((-10, -4))
    my_list.append((-20, -4))
    my_list.append((-15, -4))
    return my_list

def _set_animation_list_offset_projectile_hit():
    my_list = []
    my_list.append((-20, -4))
    my_list.append((-25, -4))
    my_list.append((-15, -4))
    my_list.append((-15, -4))
    my_list.append((-10, -4))
    my_list.append((0, -4))
    my_list.append((0, -4))
    my_list.append((0, -4))
    my_list.append((0, -4))
    my_list.append((0, -4))
    return my_list

def _set_animation_list_offset_ship_destroyed():
    my_list = []
    my_list.append((-4, 1))
    my_list.append((-51, -50))
    my_list.append((-50, -50))
    my_list.append((-29, -34))
    my_list.append((-37, -39))
    my_list.append((5, 1))
    my_list.append((-49, -50))
    my_list.append((-50, -50))
    my_list.append((-29, -35))
    my_list.append((-38, -39))
    return my_list

def _set_animation_list_offset_ship_move():
    my_list = []
    my_list.append((-50, 7))
    my_list.append((-53, 7))
    my_list.append((-58, 9))
    my_list.append((-55, 13))
    my_list.append((-60, 7))
    my_list.append((35, 7))
    my_list.append((43, 7))
    my_list.append((48, 9))
    my_list.append((45, 13))
    my_list.append((50, 7))
    return my_list

animation_list_projectile_shoot = _set_animation_lists_projectile_shoot()
animation_list_projectile_move = _set_animation_lists_projectile_move()
animation_list_projectile_hit = _set_animation_lists_projectile_hit()
animation_list_ship_destroyed = _set_animation_lists_ship_destroyed()
animation_list_ship_move = _set_animation_lists_ship_move()

animation_list_offset_projectile_shoot = _set_animation_list_offset_projectile_shoot()
animation_list_offset_projectile_move = _set_animation_list_offset_projectile_move()
animation_list_offset_projectile_hit = _set_animation_list_offset_projectile_hit()
animation_list_offset_ship_destroyed = _set_animation_list_offset_ship_destroyed()
animation_list_offset_ship_move = _set_animation_list_offset_ship_move()

sound_ship_id = 0

ship_2_shoot_sound = SoundLoader.load("sounds/ship4_shoot_zapsplat_science_fiction_gun_weapon_powerful_cannon_blaster_003_71704.mp3")
ship_3_shoot_sound = SoundLoader.load("sounds/ship4_shoot_zapsplat_science_fiction_gun_weapon_powerful_cannon_blaster_003_71704.mp3")
ship_4_shoot_sound = SoundLoader.load("sounds/ship4_shoot_zapsplat_science_fiction_gun_weapon_powerful_cannon_blaster_003_71704.mp3")
ship_5_shoot_sound = SoundLoader.load("sounds/ship4_shoot_zapsplat_science_fiction_gun_weapon_powerful_cannon_blaster_003_71704.mp3")
ship_6_shoot_sound = SoundLoader.load("sounds/ship6_shoot_zapsplat_science_fiction_impact_explosion_spacecraft_blow_up_my_missile_003_63117.mp3")
ship_2_shoot_sound.volume = 0.25
ship_3_shoot_sound.volume = 0.25
ship_4_shoot_sound.volume = 0.25
ship_5_shoot_sound.volume = 0.25
ship_6_shoot_sound.volume = 0.25
ships_shoot_sound = []
ships_shoot_sound.append(ship_2_shoot_sound)
ships_shoot_sound.append(ship_3_shoot_sound)
ships_shoot_sound.append(ship_4_shoot_sound)
ships_shoot_sound.append(ship_5_shoot_sound)
ships_shoot_sound.append(ship_6_shoot_sound)

ship_2_move_sound = SoundLoader.load("sounds/ship2_move_zapsplat_science_fiction_spacecraft_flyby_whizz_past_fast_002_62707.mp3")
ship_3_move_sound = SoundLoader.load("sounds/ship3_move_zapsplat_science_fiction_space_vehicle_whoosh_past_001_45017.mp3")
ship_4_move_sound = SoundLoader.load("sounds/ship4_move_zapsplat_science_fiction_space_vehicle_whoosh_past_002_45018.mp3")
ship_5_move_sound = SoundLoader.load("sounds/ship5_move_zapsplat_science_fiction_space_vehicle_whoosh_past_003_45019.mp3")
ship_6_move_sound = SoundLoader.load("sounds/ship6_move_zapsplat_science_fiction_space_vehicle_whoosh_past_010_45026.mp3")
ship_2_move_sound.volume = 0.25
ship_3_move_sound.volume = 0.25
ship_4_move_sound.volume = 0.25
ship_5_move_sound.volume = 0.25
ship_6_move_sound.volume = 0.25
ships_move_sound = []
ships_move_sound.append(ship_2_move_sound)
ships_move_sound.append(ship_3_move_sound)
ships_move_sound.append(ship_4_move_sound)
ships_move_sound.append(ship_5_move_sound)
ships_move_sound.append(ship_6_move_sound)

ship_2_explosion_sound = SoundLoader.load("sounds/ship2_explosion_zapsplat_science_fiction_distant_explosion_003_62573.mp3")
ship_3_explosion_sound = SoundLoader.load("sounds/ship2_explosion_zapsplat_science_fiction_distant_explosion_003_62573.mp3")
ship_4_explosion_sound = SoundLoader.load("sounds/ship2_explosion_zapsplat_science_fiction_distant_explosion_003_62573.mp3")
ship_5_explosion_sound = SoundLoader.load("sounds/ship2_explosion_zapsplat_science_fiction_distant_explosion_003_62573.mp3")
ship_6_explosion_sound = SoundLoader.load("sounds/ship2_explosion_zapsplat_science_fiction_distant_explosion_003_62573.mp3")
ship_2_explosion_sound.volume = 0.25
ship_3_explosion_sound.volume = 0.25
ship_4_explosion_sound.volume = 0.25
ship_5_explosion_sound.volume = 0.25
ship_6_explosion_sound.volume = 0.25
ships_explosion_sound = []
ships_explosion_sound.append(ship_2_explosion_sound)
ships_explosion_sound.append(ship_3_explosion_sound)
ships_explosion_sound.append(ship_4_explosion_sound)
ships_explosion_sound.append(ship_5_explosion_sound)
ships_explosion_sound.append(ship_6_explosion_sound)

ship2_rotate_lr = ["images/z_Ship2.png", "images/Ship2_r4.png", "images/Ship2_r3.png", "images/Ship2_r2.png", "images/Ship2_r1.png", "Ship2.png"]
ships_rotate_lr = []
ships_rotate_lr.append(ship2_rotate_lr)

ship2_rotate_rl = ["images/Ship2.png", "images/Ship2_r1.png", "images/Ship2_r2.png", "images/Ship2_r3.png", "images/Ship2_r4.png", "z_Ship2.png"]
ships_rotate_rl = []
ships_rotate_rl.append(ship2_rotate_rl)

def _is_odd(number):
    if number % 2:
        return True
    else:
        return False

def _my_round_up(number):
    if int(number) != 0:
        num_mod = number % int(number)
        if num_mod != 0:
            return _my_truncate(number, 0) + 1
        else:
            return number
    elif number == 0:
        return number
    else:
        return number + 1

def _my_truncate(n, decimals):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def _separator_for_output(number):
    number_str = str(number)
    digits = len(number_str)
    if digits <= 3:
        return number_str
    else:
        div = digits // 3
        div_mod = digits % 3
        separ_count = div
        position = div_mod
        if div_mod == 0:
            separ_count -= 1
            str_num = number_str[0:3]
            position += 3
        else:
            str_num = number_str[0:div_mod]
        for i in range(separ_count):
            str_num += ' ' + number_str[position:position+3]
            position += 3
    return str_num

class MenuScreen(Screen):
    loc_singleplayer_game = text_strings.singleplayer_game
    loc_hot_seat_game = text_strings.hot_seat_game
    loc_network_game = text_strings.network_game
    loc_exit_game = text_strings.exit_game
    english_flag = "images/english_flag.png"
    russian_flag = "images/russian_flag.png"
    backgroud_image = "images/pexels-free-nature-stock-1564280.jpg"
    btn_singleplayer_game = ObjectProperty()
    btn_hot_seat_game = ObjectProperty()
    btn_network_game = ObjectProperty()
    btn_exit_game = ObjectProperty()
    def change_language_to_russian(self):
        global current_language
        global text_strings
        if current_language != "Russian":
            del text_strings
            from language_rus import text_strings
            current_language = "Russian"
            self.update_locale()
            
    def change_language_to_english(self):
        global current_language
        global text_strings
        if current_language != "English":
            del text_strings
            from language_eng import text_strings
            current_language = "English"
            self.update_locale()
    
    def update_locale(self):
        self.loc_singleplayer_game = text_strings.singleplayer_game
        self.loc_hot_seat_game = text_strings.hot_seat_game
        self.loc_network_game = text_strings.network_game
        self.loc_exit_game = text_strings.exit_game
        self.loc_give_up = text_strings.give_up
        self.btn_singleplayer_game.text = self.loc_singleplayer_game
        self.btn_hot_seat_game.text = self.loc_hot_seat_game
        self.btn_network_game.text = self.loc_network_game
        self.btn_exit_game.text = self.loc_exit_game
        game_screen.btn_give_up.text = self.loc_give_up
        Light_Fighter.set_stat_text_card(text_strings.light_fighter)
        Heavy_Fighter.set_stat_text_card(text_strings.heavy_fighter)
        Frigate.set_stat_text_card(text_strings.frigate)
        Cruiser.set_stat_text_card(text_strings.cruiser)
        Dreadnought.set_stat_text_card(text_strings.dreadnought)
        arrangemenu_screen.redraw_selected_ship()
    def change_screen_to_arrangemenu(self):
        sm.current = "Arrange Menu Screen"
        Clock.schedule_once(arrangemenu_screen.reinit_and_update_locale, -1)
    def change_screen_to_game(self):
        sm.current = "Game Screen"
        game_screen.init_random_image_background(self)
        #game_screen.try_to_place()
        Clock.schedule_once(game_screen.reinit_and_update_locale, -1)
    def start_singleplayer_game(self):
        pass
    def start_network_game(self):
        pass
    def start_hot_seat_game(self):
        game_screen.player_1_type = 1
        game_screen.player_2_type = 1
        game_screen.current_player = 1
        game_screen.game_type = 2
        game_screen.in_animation = False
        self.change_screen_to_arrangemenu()
    def exit_app(self):
        app.stop(self)

class ArrangeMenuScreen(Screen):
    loc_finish_preparing = text_strings.finish_preparing
    loc_add_ships = text_strings.add_ships
    loc_remove_ships = text_strings.remove_ships
    loc_points_left = text_strings.points_left
    loc_player = text_strings.player
    loc_points_left_lbl = loc_player + " 1:" + loc_points_left
    lbl_points_left = ObjectProperty()
    btn_finish_preparing = ObjectProperty()
    btn_add_ships = ObjectProperty()
    btn_remove_ships_1 = ObjectProperty()
    btn_remove_ships_2 = ObjectProperty()
    btn_remove_ships_3 = ObjectProperty()
    btn_remove_ships_4 = ObjectProperty()
    btn_remove_ships_5 = ObjectProperty()
    btn_remove_ships_6 = ObjectProperty()
    btn_remove_ships_7 = ObjectProperty()
    points_left = ObjectProperty()
    selected_ship = ObjectProperty()
    selected_ship_stats_1 = ObjectProperty()
    selected_ship_stats_2 = ObjectProperty()
    selected_ship_stats_3 = ObjectProperty()
    selected_ship_number = ObjectProperty()
    selected_ship_number_label = ObjectProperty()
    arrange_squad_1 = ObjectProperty()
    arrange_squad_2 = ObjectProperty()
    arrange_squad_3 = ObjectProperty()
    arrange_squad_4 = ObjectProperty()
    arrange_squad_5 = ObjectProperty()
    arrange_squad_6 = ObjectProperty()
    arrange_squad_7 = ObjectProperty()
    arrange_squad_label_1 = ObjectProperty()
    arrange_squad_label_2 = ObjectProperty()
    arrange_squad_label_3 = ObjectProperty()
    arrange_squad_label_4 = ObjectProperty()
    arrange_squad_label_5 = ObjectProperty()
    arrange_squad_label_6 = ObjectProperty()
    arrange_squad_label_7 = ObjectProperty()
    arrange_selected_ship = list_of_ship_images[0]
    arrange_selected_counter = 0
    points_left_num = 10000000
    arrange_max_number = int(points_left_num / Light_Fighter.price)
    empty_image = "images/empty.png"
    plate_image = "images/plate.png"
    selected_ships = []
    finish_validated = BooleanProperty(False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(pos = self.pos, size = self.size, source = "images/science-fiction-4761925_1280.png")
        self.arrange_selected_ship = list_of_ship_images[0]
        self.arrange_selected_counter = 0
        self.redraw_selected_ship()
    def on_size(self, *args):
        self.bg.size = self.size
    def reinit_and_update_locale(self, *args):
        self.selected_ships.clear()
        self.loc_finish_preparing = text_strings.finish_preparing
        self.loc_add_ships = text_strings.add_ships
        self.loc_remove_ships = text_strings.remove_ships
        self.loc_points_left = text_strings.points_left
        if game_screen.game_type == 1 or game_screen.game_type == 2:
            self.loc_points_left_lbl = self.loc_player + " " + str(game_screen.current_player) + ": " + self.loc_points_left
        else:
            pass
        self.lbl_points_left.text = self.loc_points_left_lbl
        self.btn_finish_preparing.text = self.loc_finish_preparing
        self.btn_add_ships.text = self.loc_add_ships
        self.btn_remove_ships_1.text = self.loc_remove_ships
        self.btn_remove_ships_2.text = self.loc_remove_ships
        self.btn_remove_ships_3.text = self.loc_remove_ships
        self.btn_remove_ships_4.text = self.loc_remove_ships
        self.btn_remove_ships_5.text = self.loc_remove_ships
        self.btn_remove_ships_6.text = self.loc_remove_ships
        self.btn_remove_ships_7.text = self.loc_remove_ships
        self.redraw_fully_squad_ship()
    def arrange_next_ship(self):
        if self.arrange_selected_counter == 4:
            self.arrange_selected_counter = 0
            self.arrange_selected_ship = list_of_ship_images[self.arrange_selected_counter]
        else:
            self.arrange_selected_counter += 1
            self.arrange_selected_ship = list_of_ship_images[self.arrange_selected_counter]
        self.arrange_max_number = int(self.points_left_num / listofships[self.arrange_selected_counter].price)
        self.redraw_selected_ship()
        #self.selected_ship_stats.text = "[color=#ff0000]Attack[/color]\n[color=#0000ff]Defense[/color]"
    def arrange_previous_ship(self):
        if self.arrange_selected_counter == 0:
            self.arrange_selected_counter = 4
            self.arrange_selected_ship = list_of_ship_images[self.arrange_selected_counter]
        else:
            self.arrange_selected_counter -= 1
            self.arrange_selected_ship = list_of_ship_images[self.arrange_selected_counter]
        self.arrange_max_number = int(self.points_left_num / listofships[self.arrange_selected_counter].price)
        self.redraw_selected_ship()
    def redraw_selected_ship(self):
        self.selected_ship.source = self.arrange_selected_ship
        if self.arrange_selected_counter == 0:
            self.selected_ship_stats_1.text = Light_Fighter.stat_text_card_1
            self.selected_ship_stats_2.text = Light_Fighter.stat_text_card_2
            self.selected_ship_stats_3.text = Light_Fighter.stat_text_card_3
        elif self.arrange_selected_counter == 1:
            self.selected_ship_stats_1.text = Heavy_Fighter.stat_text_card_1
            self.selected_ship_stats_2.text = Heavy_Fighter.stat_text_card_2
            self.selected_ship_stats_3.text = Heavy_Fighter.stat_text_card_3
        elif self.arrange_selected_counter == 2:
            self.selected_ship_stats_1.text = Frigate.stat_text_card_1
            self.selected_ship_stats_2.text = Frigate.stat_text_card_2
            self.selected_ship_stats_3.text = Frigate.stat_text_card_3
        elif self.arrange_selected_counter == 3:
            self.selected_ship_stats_1.text = Cruiser.stat_text_card_1
            self.selected_ship_stats_2.text = Cruiser.stat_text_card_2
            self.selected_ship_stats_3.text = Cruiser.stat_text_card_3
        elif self.arrange_selected_counter == 4:
            self.selected_ship_stats_1.text = Dreadnought.stat_text_card_1
            self.selected_ship_stats_2.text = Dreadnought.stat_text_card_2
            self.selected_ship_stats_3.text = Dreadnought.stat_text_card_3
        self.selected_ship_number.max = self.arrange_max_number
    def redraw_fully_squad_ship(self):
        self.arrange_squad_1.source = empty_image
        self.arrange_squad_label_1.text = ""
        self.btn_remove_ships_1.opacity = 0
        self.btn_remove_ships_1.disabled = True
        self.arrange_squad_2.source = empty_image
        self.arrange_squad_label_2.text = ""
        self.btn_remove_ships_2.opacity = 0
        self.btn_remove_ships_2.disabled = True
        self.arrange_squad_3.source = empty_image
        self.arrange_squad_label_3.text = ""
        self.btn_remove_ships_3.opacity = 0
        self.btn_remove_ships_3.disabled = True
        self.arrange_squad_4.source = empty_image
        self.arrange_squad_label_4.text = ""
        self.btn_remove_ships_4.opacity = 0
        self.btn_remove_ships_4.disabled = True
        self.arrange_squad_5.source = empty_image
        self.arrange_squad_label_5.text = ""
        self.btn_remove_ships_5.opacity = 0
        self.btn_remove_ships_5.disabled = True
        self.arrange_squad_6.source = empty_image
        self.arrange_squad_label_6.text = ""
        self.btn_remove_ships_6.opacity = 0
        self.btn_remove_ships_6.disabled = True
        self.arrange_squad_7.source = empty_image
        self.arrange_squad_label_7.text = ""
        self.btn_remove_ships_7.opacity = 0
        self.btn_remove_ships_7.disabled = True
        i = 0
        if i < len(self.selected_ships):
            self.arrange_squad_1.source = list_of_ship_images[self.selected_ships[i][0]]
            self.arrange_squad_label_1.text = _separator_for_output(self.selected_ships[i][1])
            self.btn_remove_ships_1.opacity = 1
            self.btn_remove_ships_1.disabled = False
            i += 1
        if i < len(self.selected_ships):
            self.arrange_squad_2.source = list_of_ship_images[self.selected_ships[i][0]]
            self.arrange_squad_label_2.text = _separator_for_output(self.selected_ships[i][1])
            self.btn_remove_ships_2.opacity = 1
            self.btn_remove_ships_2.disabled = False
            i += 1
        if i < len(self.selected_ships):
            self.arrange_squad_3.source = list_of_ship_images[self.selected_ships[i][0]]
            self.arrange_squad_label_3.text = _separator_for_output(self.selected_ships[i][1])
            self.btn_remove_ships_3.opacity = 1
            self.btn_remove_ships_3.disabled = False
            i += 1
        if i < len(self.selected_ships):
            self.arrange_squad_4.source = list_of_ship_images[self.selected_ships[i][0]]
            self.arrange_squad_label_4.text = _separator_for_output(self.selected_ships[i][1])
            self.btn_remove_ships_4.opacity = 1
            self.btn_remove_ships_4.disabled = False
            i += 1
        if i < len(self.selected_ships):
            self.arrange_squad_5.source = list_of_ship_images[self.selected_ships[i][0]]
            self.arrange_squad_label_5.text = _separator_for_output(self.selected_ships[i][1])
            self.btn_remove_ships_5.opacity = 1
            self.btn_remove_ships_5.disabled = False
            i += 1
        if i < len(self.selected_ships):
            self.arrange_squad_6.source = list_of_ship_images[self.selected_ships[i][0]]
            self.arrange_squad_label_6.text = _separator_for_output(self.selected_ships[i][1])
            self.btn_remove_ships_6.opacity = 1
            self.btn_remove_ships_6.disabled = False
            i += 1
        if i < len(self.selected_ships):
            self.arrange_squad_7.source = list_of_ship_images[self.selected_ships[i][0]]
            self.arrange_squad_label_7.text = _separator_for_output(self.selected_ships[i][1])
            self.btn_remove_ships_7.opacity = 1
            self.btn_remove_ships_7.disabled = False
            i += 1
        self.points_left.text = _separator_for_output(self.points_left_num)
        self.selected_ship_number.max = self.arrange_max_number
    def validate_finish(self):
        # (self, name, s_id, sq_id, player_id, quantity, attack, defense, weapon_range, accuracy, speed, movement, attack_type, defense_laser, defense_kinetic, defense_plasma, defense_rocket, defense_rail, imagefile)
        if game_screen.game_type == 2:
            if len(self.selected_ships) != 0 and game_screen.current_player == 1:
                for i in range(len(self.selected_ships)):
                    game_screen.player_1_fleet.append(Squadron(listofships[self.selected_ships[i][0]], self.selected_ships[i][0], i, 1, self.selected_ships[i][1], listofships[self.selected_ships[i][0]].attack, listofships[self.selected_ships[i][0]].defense, listofships[self.selected_ships[i][0]].weapon_range, listofships[self.selected_ships[i][0]].accuracy, listofships[self.selected_ships[i][0]].speed, listofships[self.selected_ships[i][0]].movement, listofships[self.selected_ships[i][0]].attack_type, listofships[self.selected_ships[i][0]].defense_laser, listofships[self.selected_ships[i][0]].defense_kinetic, listofships[self.selected_ships[i][0]].defense_plasma, listofships[self.selected_ships[i][0]].defense_rocket, listofships[self.selected_ships[i][0]].defense_rail, listofships[self.selected_ships[i][0]].move_and_shoot, listofships[self.selected_ships[i][0]].imagefile, self.plate_image))
                print("\n\nPlayer 1 Fleet length %s\n\n" % (len(game_screen.player_1_fleet)))
                self.selected_ships.clear()
                self.arrange_selected_ship = list_of_ship_images[0]
                self.arrange_selected_counter = 0
                self.points_left_num = 10000000
                self.points_left.text = _separator_for_output(10000000)
                self.arrange_max_number = int(self.points_left_num / Light_Fighter.price)
                self.selected_ship_number.value = 1
                self.selected_ship_number.max = self.arrange_max_number
                self.selected_ship_number_label.text = "0"
                self.loc_points_left_lbl = self.loc_player + " 2: " + self.loc_points_left
                self.lbl_points_left.text = self.loc_points_left_lbl
                game_screen.current_player = 2
                self.redraw_selected_ship()
                self.redraw_fully_squad_ship()
            elif len(self.selected_ships) != 0 and game_screen.current_player == 2:
                for i in range(len(self.selected_ships)):
                    game_screen.player_2_fleet.append(Squadron(listofships[self.selected_ships[i][0]], self.selected_ships[i][0], 7 + i, 2, self.selected_ships[i][1], listofships[self.selected_ships[i][0]].attack, listofships[self.selected_ships[i][0]].defense, listofships[self.selected_ships[i][0]].weapon_range, listofships[self.selected_ships[i][0]].accuracy, listofships[self.selected_ships[i][0]].speed, listofships[self.selected_ships[i][0]].movement, listofships[self.selected_ships[i][0]].attack_type, listofships[self.selected_ships[i][0]].defense_laser, listofships[self.selected_ships[i][0]].defense_kinetic, listofships[self.selected_ships[i][0]].defense_plasma, listofships[self.selected_ships[i][0]].defense_rocket, listofships[self.selected_ships[i][0]].defense_rail, listofships[self.selected_ships[i][0]].move_and_shoot, listofships[self.selected_ships[i][0]].mirror_imagefile, self.plate_image))
                print("\n\nPlayer 2 Fleet length %s\n\n" % (len(game_screen.player_2_fleet)))
                self.selected_ships.clear()
                self.arrange_selected_ship = list_of_ship_images[0]
                self.arrange_selected_counter = 0
                self.points_left_num = 10000000
                self.points_left.text = _separator_for_output(10000000)
                self.arrange_max_number = int(self.points_left_num / Light_Fighter.price)
                self.selected_ship_number.value = 1
                self.selected_ship_number.max = self.arrange_max_number
                self.selected_ship_number_label.text = "0"
                self.loc_points_left_lbl = self.loc_player + " 1: " + self.loc_points_left
                self.lbl_points_left.text = self.loc_points_left_lbl
                game_screen.current_player = 1
                self.redraw_selected_ship()
                self.redraw_fully_squad_ship()
                self.finish_validated = True
            if self.finish_validated:
                self.finish_validated = False
                game_screen.turn_of_player = 1
                menu_screen.change_screen_to_game()
                Clock.schedule_once(game_screen.init_players_fleets, -1)
    def arrange_add_ship(self):
        if len(self.selected_ships) < 7:
            if self.selected_ship_number.value <= int(self.points_left_num / listofships[self.arrange_selected_counter].price) and self.selected_ship_number.value != 0:
                self.selected_ships.append([self.arrange_selected_counter, int(self.selected_ship_number.value)])
                self.points_left_num -= int(int(self.selected_ship_number.value) * listofships[self.arrange_selected_counter].price)
                self.arrange_max_number = int(self.points_left_num / listofships[self.arrange_selected_counter].price)
                self.redraw_fully_squad_ship()
        print(self.selected_ships)
    def arrange_remove_ship(self, s_id):
        if s_id < len(self.selected_ships):
            a = self.selected_ships.pop(s_id)
            self.points_left_num += int(a[1] * listofships[a[0]].price)
            self.arrange_max_number = int(self.points_left_num / listofships[self.arrange_selected_counter].price)
            self.redraw_fully_squad_ship()
        print(self.selected_ships)
    def arrange_change_selected_number_label(self):
        self.selected_ship_number_label.text = _separator_for_output(int(self.selected_ship_number.value))

class GameScreen(Screen):
    list_of_images = []
    list_of_images.append("images/pexels-adam-krypel-6498990.jpg")
    list_of_images.append("images/pexels-hristo-fidanov-1252890.jpg")
    list_of_images.append("images/pexels-pixabay-2150.jpg")
    list_of_images.append("images/pexels-ludvig-hedenborg-3753160.jpg")
    list_of_images.append("images/pexels-alberlan-barros-7311920.jpg")
    list_of_images.append("images/pexels-adam-krypel-6498994.jpg")
    background_image = ObjectProperty()
    label_preview_attack = ObjectProperty()
    label_preview_attack_text = StringProperty()
    label_selected_ship_stats_1 = ObjectProperty()
    label_selected_ship_stats_2 = ObjectProperty()
    label_selected_ship_stats_3 = ObjectProperty()
    label_temp_result = ObjectProperty()
    #animation_animation_speed = ObjectProperty()
    #animation_movement_speed = ObjectProperty()
    animation_animation_speed_label = ObjectProperty()
    btn_give_up = ObjectProperty()
    self_hex_grid_coords = hex_grid_coords
    self_hex_grid_coords_for_kv = hex_grid_coords_for_kv
    src_hexagon_4 = StringProperty("images/hexagon_4.png")
    src_hexagon_5 = StringProperty("images/hexagon_5.png")
    src_hexagon_6 = StringProperty("images/hexagon_6.png")
    src_hexagon_7 = StringProperty("images/hexagon_7.png")
    src_hexagon_8 = StringProperty("images/hexagon_8.png")
    src_hexagon_border = StringProperty("images/hexagon_border.png")
    src_empty = StringProperty("images/empty_small.png")
    
    list_of_hexes = ListProperty()
    list_of_hexes_y_1 = ListProperty()
    list_of_hexes_y_2 = ListProperty()
    list_of_hexes_y_3 = ListProperty()
    list_of_hexes_y_4 = ListProperty()
    list_of_hexes_y_5 = ListProperty()
    list_of_hexes_y_6 = ListProperty()
    list_of_hexes_y_7 = ListProperty()
    highlighted_hex = ListProperty()
    selected_hex = ListProperty()
    selected_hex_stats = ListProperty()
    
    SPEED = 6   #NumericProperty(10)
    EXHAUST_ANIMATION = 30
    ANIMATION_SPEED = 10
    action_animation_dt = 0
    action_counter_1 = 0
    action_counter_2 = 0
    action_counter_3 = 0
    action_counter_done = False
    action_type = StringProperty()
    action_x0 = 0   #NumericProperty()
    action_y0 = 0   #NumericProperty()
    action_x1 = 0   #NumericProperty()
    action_y1 = 0   #NumericProperty()
    action_current_x = 0
    action_current_y = 0
    action_pos_x0 = 0   #NumericProperty()
    action_pos_y0 = 0   #NumericProperty()
    action_pos_x1 = 0   #NumericProperty()
    action_pos_y1 = 0   #NumericProperty()
    action_speed_x = NumericProperty()
    action_speed_y = NumericProperty()
    action_speed = ReferenceListProperty(action_speed_x, action_speed_y)
    action_text_card = ""
    action_projectile_id = 0
    action_mirrored_offset = 0
    action_squadron = ListProperty()
    
    debug = False
    squadron_order_list = ListProperty()
    to_remove_from_list = ListProperty()
    actions_list = ListProperty()
    turn_number = NumericProperty(1)
    update_in_action = BooleanProperty(False)
    in_animation = BooleanProperty(False)
    is_paused = BooleanProperty(False)
    block_mouse_pos = BooleanProperty(False)
    current_squadron_index = 0
    time_to_change_selected = False
    shoot_after_move = False
    current_player = NumericProperty()
    # 1 - Local Player - 2 - AI - 3 - Network Player
    player_1_type = NumericProperty()
    player_2_type = NumericProperty()
    game_type = NumericProperty()
    player_1_fleet = ListProperty()
    player_2_fleet = ListProperty()
    turn_of_player = NumericProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.init_random_image_background()
        self.init_hex_grid()
        #self.try_to_place()
        Window.bind(mouse_pos=self.mouse_pos)
        Clock.schedule_once(self.try_to_place, 1)
        self.selected_hex_stats.append("")
        self.selected_hex_stats.append("")
        self.selected_hex_stats.append("")
    
    def reinit_and_update_locale(self, *args):
        self.loc_give_up = text_strings.give_up
        self.btn_give_up.text = self.loc_give_up
        self.loc_animation_label = text_strings.animation_speed
        self.animation_animation_speed_label.text = self.loc_animation_label
    
    def init_players_fleets(self, *args):
        player_1_start_hexes = [(6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]
        player_2_start_hexes = [(6, 8), (5, 9), (4, 8), (3, 9), (2, 8), (1, 9), (0, 8)]
        #   put_on_game_field(self, widget, x, y, size_x, size_y, hex_y, hex_x)
        for i in range(len(self.player_1_fleet)):
            self.player_1_fleet[i].put_on_game_field(widget = self, x = self.self_hex_grid_coords_for_kv[player_1_start_hexes[i][0]][player_1_start_hexes[i][1]][0], y = self.self_hex_grid_coords_for_kv[player_1_start_hexes[i][0]][player_1_start_hexes[i][1]][1], size_x = 100, size_y = 100, hex_y = player_1_start_hexes[i][0], hex_x = player_1_start_hexes[i][1])
            hex_grid_ids_and_states[player_1_start_hexes[i][0]][player_1_start_hexes[i][1]][3] = True
            self.list_of_hexes[player_1_start_hexes[i][0]][player_1_start_hexes[i][1]].source = self.src_hexagon_4
        for i in range(len(self.player_2_fleet)):
            self.player_2_fleet[i].put_on_game_field(widget = self, x = self.self_hex_grid_coords_for_kv[player_2_start_hexes[i][0]][player_2_start_hexes[i][1]][0], y = self.self_hex_grid_coords_for_kv[player_2_start_hexes[i][0]][player_2_start_hexes[i][1]][1], size_x = 100, size_y = 100, hex_y = player_2_start_hexes[i][0], hex_x = player_2_start_hexes[i][1])
            hex_grid_ids_and_states[player_2_start_hexes[i][0]][player_2_start_hexes[i][1]][4] = True
            self.list_of_hexes[player_2_start_hexes[i][0]][player_2_start_hexes[i][1]].source = self.src_hexagon_5
        if self.game_type == 1:
            Clock.schedule_interval(self.update_game_type_1, 1.0 / 60.0)
        elif self.game_type == 2:
            Clock.schedule_interval(self.update_game_type_2, 1.0 / 60.0)
        elif self.game_type == 3:
            Clock.schedule_interval(self.update_game_type_3, 1.0 / 60.0)
        self.turn_number = 1
        self.update_in_action = False
        self.in_animation = False
        self.is_paused = False
        self.squadron_order_list.clear()
        speed_to_match = [listofships[i].speed for i in range(len(listofships))]
        ships_to_arrange = []
        remove_index = []
        unable_to_find = False
        for k in range(len(speed_to_match)):
            ships_to_arrange.clear()
            remove_index.clear()
            for i in range(len(self.player_1_fleet)):
                if speed_to_match[k] == self.player_1_fleet[i].speed:
                    ships_to_arrange.append(self.player_1_fleet[i])
            for i in range(len(self.player_2_fleet)):
                if speed_to_match[k] == self.player_2_fleet[i].speed:
                    ships_to_arrange.append(self.player_2_fleet[i])
            #for i in range(len(ships_to_arrange)):
                #print("Ship = %s, Player = %s\n\n\n" % (ships_to_arrange[i].s_id, ships_to_arrange[i].player_id))
            cur_pl = 1
            
            for j in range(15):
                for i in range(len(ships_to_arrange)):
                    if ships_to_arrange[i].player_id == cur_pl:
                        self.squadron_order_list.append(ships_to_arrange[i])
                        remove_index.append(i)
                        if cur_pl == 1:
                            cur_pl = 2
                        else:
                            cur_pl = 1
                #print(remove_index)
                #print("")
                #print(len(ships_to_arrange))
                #print("")
                for i in range(len(remove_index) - 1, -1, -1):
                    #print("i = %s" % (i))
                    ships_to_arrange.pop(remove_index[i])
                #print(len(ships_to_arrange))
                remove_index.clear()
                if len(ships_to_arrange) != 0:
                    left_pl = ships_to_arrange[0].player_id
                else:
                    unable_to_find = True
                if not unable_to_find:
                    unable_to_find = True
                    for i in range(len(ships_to_arrange)):
                        if ships_to_arrange[i].player_id != left_pl:
                            unable_to_find = False
                            break
                if unable_to_find or j == 14:
                    print("unable to find! j = ", j)
                    for i in range(len(ships_to_arrange)):
                        self.squadron_order_list.append(ships_to_arrange[i])
                    ships_to_arrange.clear()
                    break
        
        #for i in range(len(test_list)):
        #    print("Ship = %s, Player = %s" % (test_list[i].s_id, test_list[i].player_id))
        for i in range(len(self.squadron_order_list)):
            print("Ship = %s, Player = %s, i = %s" % (self.squadron_order_list[i].s_id, self.squadron_order_list[i].player_id, i))
        self.current_player = self.squadron_order_list[0].player_id
        self.turn_of_player = self.current_player
        self.try_to_change_selected(self.squadron_order_list[0].tile[0], self.squadron_order_list[0].tile[1])
        self.calc_in_range(self.squadron_order_list[0], self.squadron_order_list[0].tile[0], self.squadron_order_list[0].tile[1])
        self.try_to_change_selected_labels(self.squadron_order_list[0].s_id)
        self.current_squadron_index = 0
        self.time_to_change_selected = False
        self.shoot_after_move = False
        #self.selected_hex[0] = self.squadron_order_list[0].tile[0]
        #self.selected_hex[1] = self.squadron_order_list[0].tile[1]
        #hex_grid_ids_and_states[self.selected_hex[0]][self.selected_hex[1]][5] = True
        #self.squadron_order_list.append(self.player_1_fleet[0])
        self.to_remove_from_list.clear()
        self.animation_squadron = Squadron(listofships[0], 0, 100, 1, 1, listofships[0].attack, listofships[0].defense, listofships[0].weapon_range, listofships[0].accuracy, listofships[0].speed, listofships[0].movement, listofships[0].attack_type, listofships[0].defense_laser, listofships[0].defense_kinetic, listofships[0].defense_plasma, listofships[0].defense_rocket, listofships[0].defense_rail, listofships[0].move_and_shoot, listofships[0].imagefile, "images/plate.png")
        self.animation_squadron.put_on_game_field(widget = self, x = dp(53), y = dp(203), size_x = dp(100), size_y = dp(100), hex_y = -19, hex_x = -19)
        self.animation_squadron.image.source = self.src_empty
        self.animation_squadron.plate_image.source = self.src_empty
        self.animation_squadron.image.opacity = 1
        self.animation_squadron.plate_image.opacity = 1
        self.animation_squadron.label.opacity = 0
        self.animation_image = Image(source = self.src_empty, pos = (dp(53), dp(203)), allow_stretch = True)
        self.animation_image.size = (dp(115), dp(115))
        self.animation_squadron.plate_image.add_widget(self.animation_image)
    
    def change_animation_speed(self, value):
        self.ANIMATION_SPEED = int(value)
    
    def try_to_place(self, *args):
        #self.list_of_hexes.append(Hexagon(widget = self.background_image, x = dp(25), y = dp(200)))
        self.highlighted_hex.append(-1)
        self.highlighted_hex.append(-1)
        self.selected_hex.append(-1)
        self.selected_hex.append(-1)
        with self.canvas:
            for x in range(len(self.self_hex_grid_coords_for_kv[0])):
                self.list_of_hexes_y_1.append(Image(source = self.src_hexagon_border, pos = self.self_hex_grid_coords_for_kv[0][x], size = (dp(100), dp(100))))
            for x in range(len(self.self_hex_grid_coords_for_kv[1])):
                self.list_of_hexes_y_2.append(Image(source = self.src_hexagon_border, pos = self.self_hex_grid_coords_for_kv[1][x], size = (dp(100), dp(100))))    
            for x in range(len(self.self_hex_grid_coords_for_kv[2])):
                self.list_of_hexes_y_3.append(Image(source = self.src_hexagon_border, pos = self.self_hex_grid_coords_for_kv[2][x], size = (dp(100), dp(100))))
            for x in range(len(self.self_hex_grid_coords_for_kv[3])):
                self.list_of_hexes_y_4.append(Image(source = self.src_hexagon_border, pos = self.self_hex_grid_coords_for_kv[3][x], size = (dp(100), dp(100))))
            for x in range(len(self.self_hex_grid_coords_for_kv[4])):
                self.list_of_hexes_y_5.append(Image(source = self.src_hexagon_border, pos = self.self_hex_grid_coords_for_kv[4][x], size = (dp(100), dp(100))))
            for x in range(len(self.self_hex_grid_coords_for_kv[5])):
                self.list_of_hexes_y_6.append(Image(source = self.src_hexagon_border, pos = self.self_hex_grid_coords_for_kv[5][x], size = (dp(100), dp(100))))
            for x in range(len(self.self_hex_grid_coords_for_kv[6])):
                self.list_of_hexes_y_7.append(Image(source = self.src_hexagon_border, pos = self.self_hex_grid_coords_for_kv[6][x], size = (dp(100), dp(100))))
            self.list_of_hexes.append(self.list_of_hexes_y_1)
            self.list_of_hexes.append(self.list_of_hexes_y_2)
            self.list_of_hexes.append(self.list_of_hexes_y_3)
            self.list_of_hexes.append(self.list_of_hexes_y_4)
            self.list_of_hexes.append(self.list_of_hexes_y_5)
            self.list_of_hexes.append(self.list_of_hexes_y_6)
            self.list_of_hexes.append(self.list_of_hexes_y_7)

    def try_to_change(self, y, x, *args):
        #self.list_of_hexes[y][x].source = self.src_hexagon_4
        #state_in_range = hex_grid_ids_and_states[y][x][1]
        #state_highlighted = hex_grid_ids_and_states[y][x][2]
        #state_you_occupy = hex_grid_ids_and_states[y][x][3]
        #state_enemy_occupies = hex_grid_ids_and_states[y][x][4]
        #state_selected = hex_grid_ids_and_states[y][x][5]
        old_y = self.highlighted_hex[0]
        old_x = self.highlighted_hex[1]
        if old_y >= 0 and old_x >= 0:
            if hex_grid_ids_and_states[old_y][old_x][3] and not hex_grid_ids_and_states[old_y][old_x][6]:
                if not hex_grid_ids_and_states[old_y][old_x][5]:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_4
                else:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_6
            elif hex_grid_ids_and_states[old_y][old_x][3] and hex_grid_ids_and_states[old_y][old_x][6]:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_7
            elif hex_grid_ids_and_states[old_y][old_x][4] and not hex_grid_ids_and_states[old_y][old_x][6]:
                if not hex_grid_ids_and_states[old_y][old_x][5]:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_5
                else:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_6
            elif hex_grid_ids_and_states[old_y][old_x][4] and hex_grid_ids_and_states[old_y][old_x][6]:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_7
            elif hex_grid_ids_and_states[old_y][old_x][1] and not hex_grid_ids_and_states[old_y][old_x][3] and not hex_grid_ids_and_states[old_y][old_x][4]:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_8
            else:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_border
            hex_grid_ids_and_states[old_y][old_x][2] = False
        
        if x >= 0 and y >= 0:
            self.list_of_hexes[y][x].source = self.src_hexagon_6
            self.highlighted_hex[0] = y
            self.highlighted_hex[1] = x
            hex_grid_ids_and_states[y][x][2] = True
        else:
            self.highlighted_hex[0] = -1
            self.highlighted_hex[1] = -1
    
    def try_to_change_general(self, old_y, old_x, *args):
        #self.list_of_hexes[y][x].source = self.src_hexagon_4
        #state_in_range = hex_grid_ids_and_states[y][x][1]
        #state_highlighted = hex_grid_ids_and_states[y][x][2]
        #state_you_occupy = hex_grid_ids_and_states[y][x][3]
        #state_enemy_occupies = hex_grid_ids_and_states[y][x][4]
        #state_selected = hex_grid_ids_and_states[y][x][5]
        #state_in_weapon_range = hex_grid_ids_and_states[y][x][6]
        if old_x >= 0 and old_y >= 0:
            if hex_grid_ids_and_states[old_y][old_x][3] and not hex_grid_ids_and_states[old_y][old_x][6]:
                if not hex_grid_ids_and_states[old_y][old_x][5]:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_4
                else:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_6
            elif hex_grid_ids_and_states[old_y][old_x][3] and hex_grid_ids_and_states[old_y][old_x][6]:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_7
            elif hex_grid_ids_and_states[old_y][old_x][4] and not hex_grid_ids_and_states[old_y][old_x][6]:
                if not hex_grid_ids_and_states[old_y][old_x][5]:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_5
                else:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_6
            elif hex_grid_ids_and_states[old_y][old_x][4] and hex_grid_ids_and_states[old_y][old_x][6]:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_7
            elif hex_grid_ids_and_states[old_y][old_x][1] and not hex_grid_ids_and_states[old_y][old_x][3] and not hex_grid_ids_and_states[old_y][old_x][4]:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_8
            else:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_border
    
    def try_to_change_selected(self, y, x, *args):
        #self.list_of_hexes[y][x].source = self.src_hexagon_4
        #state_in_range = hex_grid_ids_and_states[y][x][1]
        #state_highlighted = hex_grid_ids_and_states[y][x][2]
        #state_you_occupy = hex_grid_ids_and_states[y][x][3]
        #state_enemy_occupies = hex_grid_ids_and_states[y][x][4]
        #state_selected = hex_grid_ids_and_states[y][x][5]
        old_y = self.selected_hex[0]
        old_x = self.selected_hex[1]
        if old_x >= 0 and old_y >= 0:
            hex_grid_ids_and_states[old_y][old_x][5] = False
            if hex_grid_ids_and_states[old_y][old_x][3] and not hex_grid_ids_and_states[old_y][old_x][6]:
                if not hex_grid_ids_and_states[old_y][old_x][5]:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_4
                else:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_6
            elif hex_grid_ids_and_states[old_y][old_x][3] and hex_grid_ids_and_states[old_y][old_x][6]:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_7
            elif hex_grid_ids_and_states[old_y][old_x][4] and not hex_grid_ids_and_states[old_y][old_x][6]:
                if not hex_grid_ids_and_states[old_y][old_x][5]:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_5
                else:
                    self.list_of_hexes[old_y][old_x].source = self.src_hexagon_6
            elif hex_grid_ids_and_states[old_y][old_x][4] and hex_grid_ids_and_states[old_y][old_x][6]:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_7
            elif hex_grid_ids_and_states[old_y][old_x][1] and not hex_grid_ids_and_states[old_y][old_x][3] and not hex_grid_ids_and_states[old_y][old_x][4]:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_8
            else:
                self.list_of_hexes[old_y][old_x].source = self.src_hexagon_border
        if x >= 0 and y >= 0:
            self.list_of_hexes[y][x].source = self.src_hexagon_6
            self.selected_hex[0] = y
            self.selected_hex[1] = x
            hex_grid_ids_and_states[y][x][5] = True
        else:
            self.selected_hex[0] = -1
            self.selected_hex[1] = -1
    
    def try_to_change_selected_labels(self, ship_id, *args):
        i = ship_id
        stat_text_card_1 = listofships[i].stat_text_card_1
        stat_text_card_2 = listofships[i].stat_text_card_2
        stat_text_card_3 = listofships[i].stat_text_card_3
        self.selected_hex_stats.clear()
        self.selected_hex_stats.append(stat_text_card_1)
        self.selected_hex_stats.append(stat_text_card_2)
        self.selected_hex_stats.append(stat_text_card_3)
        self.label_selected_ship_stats_1.text = self.selected_hex_stats[0]
        self.label_selected_ship_stats_2.text = self.selected_hex_stats[1]
        self.label_selected_ship_stats_3.text = self.selected_hex_stats[2]
    
    def change_screen_to_menu(self):
        """
        if self.current_player == 2:
            self.current_player = 1
        else:
            self.current_player = 2
        """
        for i in range(len(self.player_1_fleet)):
            self.player_1_fleet[i].remove_from_game_field(widget = self)
        for i in range(len(self.player_2_fleet)):
            self.player_2_fleet[i].remove_from_game_field(widget = self)
        self.player_1_fleet.clear()
        self.player_2_fleet.clear()
        self.highlighted_hex[0] = -1
        self.highlighted_hex[1] = -1
        self.selected_hex[0] = -1
        self.selected_hex[1] = -1
        self.actions_list.clear()
        self.label_preview_attack.text = ""
        self.label_selected_ship_stats_1.text = ""
        self.label_selected_ship_stats_2.text = ""
        self.label_selected_ship_stats_3.text = ""
        self.label_temp_result.text = ""
        for i in range(len(hex_grid_ids_and_states)):
            if i == 0:
                max_j = 9
            elif i % 2 != 0:
                max_j = 10
            else:
                max_j = 9
            for j in range(max_j):
                hex_grid_ids_and_states[i][j][1] = False
                hex_grid_ids_and_states[i][j][2] = False
                hex_grid_ids_and_states[i][j][3] = False
                hex_grid_ids_and_states[i][j][4] = False
                hex_grid_ids_and_states[i][j][5] = False
                hex_grid_ids_and_states[i][j][6] = False
                self.list_of_hexes[i][j].source = self.src_hexagon_border
        sm.current = "Menu Screen"
    
    def on_touch_down(self, touch):
        if touch.pos[0] >= 0 and touch.pos[0] <= 1024 and touch.pos[1] >= 200 and touch.pos[1] <= 768 and not self.block_mouse_pos:
            found, xxx, yyy = _find_pos_of_tile(dp(touch.pos[0]), dp(touch.pos[1]))
            if sm.current == "Game Screen" and not self.in_animation and not self.update_in_action and not self.is_paused:
                if self.game_type == 1 and self.current_player == 1:
                    pass
                elif self.game_type == 2:
                    #found, xxx, yyy = _find_pos_of_tile(dp(touch.pos[0]), dp(touch.pos[1]))
                    if found:
                        number_by_order = 0
                        for k in range(yyy + 1):
                            if k == yyy:
                                number_by_order += xxx + 1
                            elif k == 0:
                                number_by_order += 9
                            elif k % 2 != 0:
                                number_by_order += 10
                            else:
                                number_by_order += 9
                        print("Touched y = %s, x = %s\n number by order = %s\nx = %s, y = %s" % (yyy + 1, xxx + 1, number_by_order, self.self_hex_grid_coords_for_kv[yyy][xxx][0], self.self_hex_grid_coords_for_kv[yyy][xxx][1]))
                        if self.current_player == 1:
                            if self.selected_hex[0] == yyy and self.selected_hex[1] == xxx:
                                pass
                            else:
                                if hex_grid_ids_and_states[yyy][xxx][3] and self.debug:
                                    self.try_to_change_selected(yyy, xxx)
                                    ffound = False
                                    for f in range(len(self.player_1_fleet)):
                                        if self.player_1_fleet[f].tile[0] == yyy and self.player_1_fleet[f].tile[1] == xxx:
                                            squadron = self.player_1_fleet[f]
                                            ffound = True
                                            break
                                    if ffound:
                                        self.calc_in_range(squadron, yyy, xxx)
                                elif hex_grid_ids_and_states[yyy][xxx][4] and hex_grid_ids_and_states[yyy][xxx][6]:
                                    yy = self.selected_hex[0]
                                    xx = self.selected_hex[1]
                                    ffound = False
                                    for f in range(len(self.player_1_fleet)):
                                        if self.player_1_fleet[f].tile[0] == yy and self.player_1_fleet[f].tile[1] == xx:
                                            squadron = self.player_1_fleet[f]
                                            ffound = True
                                            break
                                    fffound = False
                                    for f in range(len(self.player_2_fleet)):
                                        if self.player_2_fleet[f].tile[0] == yyy and self.player_2_fleet[f].tile[1] == xxx:
                                            enemy = self.player_2_fleet[f]
                                            fffound = True
                                            break
                                    if ffound and fffound:
                                        print("move_projectile to yyy = %s, xxx = %s, pos_x = %s, pos_y = %s" %(yyy, xxx, self.self_hex_grid_coords_for_kv[yyy][xxx][0], self.self_hex_grid_coords_for_kv[yyy][xxx][1]))
                                        if self.self_hex_grid_coords_for_kv[yyy][xxx][0] > self.self_hex_grid_coords_for_kv[yy][xx][0]:
                                            direction = "lr"
                                        else:
                                            direction = "rl"
                                        action = {"action_type": "shoot_projectile", "ship_id": squadron.s_id, "direction": direction, "pos_x0": self.self_hex_grid_coords_for_kv[yy][xx][0], "pos_y0": self.self_hex_grid_coords_for_kv[yy][xx][1]}
                                        self.actions_list.append(action)
                                        action = {"action_type": "move_projectile", "ship_id": squadron.s_id, "direction": direction, "pos_x0": self.self_hex_grid_coords_for_kv[yy][xx][0], "pos_y0": self.self_hex_grid_coords_for_kv[yy][xx][1], "pos_x1": self.self_hex_grid_coords_for_kv[yyy][xxx][0], "pos_y1": self.self_hex_grid_coords_for_kv[yyy][xxx][1]}
                                        self.actions_list.append(action)
                                        action = {"action_type": "hit_projectile", "ship_id": squadron.s_id, "direction": direction, "pos_x1": self.self_hex_grid_coords_for_kv[yyy][xxx][0], "pos_y1": self.self_hex_grid_coords_for_kv[yyy][xxx][1]}
                                        self.actions_list.append(action)
                                        action = {"action_type": "deal_damage", "squadron": squadron, "enemy": enemy, "pos_x0": self.self_hex_grid_coords_for_kv[yyy][xxx][0], "pos_y0": self.self_hex_grid_coords_for_kv[yyy][xxx][1]}
                                        self.actions_list.append(action)
                                        self.selected_hex[0] = -1
                                        self.selected_hex[1] = -1
                                        hex_grid_ids_and_states[yy][xx][5] = False
                                        hex_grid_ids_and_states[yyy][xxx][6] = False
                                        self.reset_in_range(True)
                                        self.list_of_hexes[yy][xx].source = self.src_hexagon_border
                                        self.list_of_hexes[yyy][xxx].source = self.src_hexagon_border
                                elif not hex_grid_ids_and_states[yyy][xxx][3] and not hex_grid_ids_and_states[yyy][xxx][4] and hex_grid_ids_and_states[yyy][xxx][1]:
                                    ffound = False
                                    s_y = self.selected_hex[0]
                                    s_x = self.selected_hex[1]
                                    for f in range(len(self.player_1_fleet)):
                                        if self.player_1_fleet[f].tile[0] == s_y and self.player_1_fleet[f].tile[1] == s_x:
                                            squadron = self.player_1_fleet[f]
                                            ffound = True
                                            break
                                    if ffound:
                                        if self.self_hex_grid_coords_for_kv[yyy][xxx][0] > self.self_hex_grid_coords_for_kv[s_y][s_x][0]:
                                            direction = "lr"
                                        else:
                                            direction = "rl"
                                        print("move_ship to yyy = %s, xxx = %s, pos_x = %s, pos_y = %s" %(yyy, xxx, self.self_hex_grid_coords_for_kv[yyy][xxx][0], self.self_hex_grid_coords_for_kv[yyy][xxx][1]))
                                        #squadron.move_ship(self.self_hex_grid_coords_for_kv[yyy][xxx][0], self.self_hex_grid_coords_for_kv[yyy][xxx][1], xxx, yyy)
                                        self.selected_hex[0] = -1
                                        self.selected_hex[1] = -1
                                        hex_grid_ids_and_states[s_y][s_x][3] = False
                                        #hex_grid_ids_and_states[yyy][xxx][3] = True
                                        hex_grid_ids_and_states[s_y][s_x][5] = False
                                        self.reset_in_range(True)
                                        self.list_of_hexes[s_y][s_x].source = self.src_hexagon_border
                                        action = {"action_type": "animation_move", "ship_id": squadron.s_id, "direction": direction, "squadron": squadron, "y0": s_y, "x0": s_x, "y1": yyy, "x1": xxx, "pos_x0": self.self_hex_grid_coords_for_kv[s_y][s_x][0], "pos_y0": self.self_hex_grid_coords_for_kv[s_y][s_x][1], "pos_x1": self.self_hex_grid_coords_for_kv[yyy][xxx][0], "pos_y1": self.self_hex_grid_coords_for_kv[yyy][xxx][1]}
                                        print(action)
                                        self.actions_list.append(action)
                        elif self.current_player == 2:
                            if self.selected_hex[0] == yyy and self.selected_hex[1] == xxx:
                                pass
                            else:
                                if hex_grid_ids_and_states[yyy][xxx][4] and self.debug:
                                    self.try_to_change_selected(yyy, xxx)
                                    ffound = False
                                    for f in range(len(self.player_2_fleet)):
                                        if self.player_2_fleet[f].tile[0] == yyy and self.player_2_fleet[f].tile[1] == xxx:
                                            squadron = self.player_2_fleet[f]
                                            ffound = True
                                            break
                                    if ffound:
                                        self.calc_in_range(squadron, yyy, xxx)
                                elif hex_grid_ids_and_states[yyy][xxx][3] and hex_grid_ids_and_states[yyy][xxx][6]:
                                    yy = self.selected_hex[0]
                                    xx = self.selected_hex[1]
                                    ffound = False
                                    for f in range(len(self.player_2_fleet)):
                                        if self.player_2_fleet[f].tile[0] == yy and self.player_2_fleet[f].tile[1] == xx:
                                            squadron = self.player_2_fleet[f]
                                            ffound = True
                                            break
                                    fffound = False
                                    for f in range(len(self.player_1_fleet)):
                                        if self.player_1_fleet[f].tile[0] == yyy and self.player_1_fleet[f].tile[1] == xxx:
                                            enemy = self.player_1_fleet[f]
                                            fffound = True
                                            break
                                    if ffound and fffound:
                                        if self.self_hex_grid_coords_for_kv[yyy][xxx][0] > self.self_hex_grid_coords_for_kv[yy][xx][0]:
                                            direction = "lr"
                                        else:
                                            direction = "rl"
                                        action = {"action_type": "shoot_projectile", "ship_id": squadron.s_id, "direction": direction, "pos_x0": self.self_hex_grid_coords_for_kv[yy][xx][0], "pos_y0": self.self_hex_grid_coords_for_kv[yy][xx][1]}
                                        self.actions_list.append(action)
                                        action = {"action_type": "move_projectile", "ship_id": squadron.s_id, "direction": direction, "pos_x0": self.self_hex_grid_coords_for_kv[yy][xx][0], "pos_y0": self.self_hex_grid_coords_for_kv[yy][xx][1], "pos_x1": self.self_hex_grid_coords_for_kv[yyy][xxx][0], "pos_y1": self.self_hex_grid_coords_for_kv[yyy][xxx][1]}
                                        self.actions_list.append(action)
                                        action = {"action_type": "hit_projectile", "ship_id": squadron.s_id, "direction": direction, "pos_x1": self.self_hex_grid_coords_for_kv[yyy][xxx][0], "pos_y1": self.self_hex_grid_coords_for_kv[yyy][xxx][1]}
                                        self.actions_list.append(action)
                                        action = {"action_type": "deal_damage", "squadron": squadron, "enemy": enemy, "pos_x0": self.self_hex_grid_coords_for_kv[yyy][xxx][0], "pos_y0": self.self_hex_grid_coords_for_kv[yyy][xxx][1]}
                                        self.actions_list.append(action)
                                        self.selected_hex[0] = -1
                                        self.selected_hex[1] = -1
                                        hex_grid_ids_and_states[yy][xx][5] = False
                                        hex_grid_ids_and_states[yyy][xxx][6] = False
                                        self.reset_in_range(True)
                                        self.list_of_hexes[yy][xx].source = self.src_hexagon_border
                                        self.list_of_hexes[yyy][xxx].source = self.src_hexagon_border
                                elif not hex_grid_ids_and_states[yyy][xxx][3] and not hex_grid_ids_and_states[yyy][xxx][4] and hex_grid_ids_and_states[yyy][xxx][1]:
                                    ffound = False
                                    s_y = self.selected_hex[0]
                                    s_x = self.selected_hex[1]
                                    for f in range(len(self.player_2_fleet)):
                                        if self.player_2_fleet[f].tile[0] == s_y and self.player_2_fleet[f].tile[1] == s_x:
                                            squadron = self.player_2_fleet[f]
                                            ffound = True
                                            break
                                    if ffound:
                                        if self.self_hex_grid_coords_for_kv[yyy][xxx][0] > self.self_hex_grid_coords_for_kv[s_y][s_x][0]:
                                            direction = "lr"
                                        else:
                                            direction = "rl"
                                        print("move_ship to yyy = %s, xxx = %s, pos_x = %s, pos_y = %s" %(yyy, xxx, self.self_hex_grid_coords_for_kv[yyy][xxx][0], self.self_hex_grid_coords_for_kv[yyy][xxx][1]))
                                        #squadron.move_ship(self.self_hex_grid_coords_for_kv[yyy][xxx][0], self.self_hex_grid_coords_for_kv[yyy][xxx][1], xxx, yyy)
                                        self.selected_hex[0] = -1
                                        self.selected_hex[1] = -1
                                        hex_grid_ids_and_states[s_y][s_x][4] = False
                                        #hex_grid_ids_and_states[yyy][xxx][4] = True
                                        hex_grid_ids_and_states[s_y][s_x][5] = False
                                        self.reset_in_range(True)
                                        self.list_of_hexes[s_y][s_x].source = self.src_hexagon_border
                                        action = {"action_type": "animation_move", "ship_id": squadron.s_id, "direction": direction, "squadron": squadron, "y0": s_y, "x0": s_x, "y1": yyy, "x1": xxx, "pos_x0": self.self_hex_grid_coords_for_kv[s_y][s_x][0], "pos_y0": self.self_hex_grid_coords_for_kv[s_y][s_x][1], "pos_x1": self.self_hex_grid_coords_for_kv[yyy][xxx][0], "pos_y1": self.self_hex_grid_coords_for_kv[yyy][xxx][1]}
                                        self.actions_list.append(action)
            if self.selected_hex[0] >= 0 and self.selected_hex[1] >= 0:
                ffound = False
                s_y = self.selected_hex[0]
                s_x = self.selected_hex[1]
                for f in range(len(self.player_1_fleet)):
                    if self.player_1_fleet[f].tile[0] == s_y and self.player_1_fleet[f].tile[1] == s_x:
                        squadron = self.player_1_fleet[f]
                        ffound = True
                        break
                if not ffound:
                    for f in range(len(self.player_2_fleet)):
                        if self.player_2_fleet[f].tile[0] == s_y and self.player_2_fleet[f].tile[1] == s_x:
                            squadron = self.player_2_fleet[f]
                            ffound = True
                            break
                if ffound:
                    i = squadron.s_id
                    stat_text_card_1 = listofships[i].stat_text_card_1
                    stat_text_card_2 = listofships[i].stat_text_card_2
                    stat_text_card_3 = listofships[i].stat_text_card_3
                    self.selected_hex_stats.clear()
                    self.selected_hex_stats.append(stat_text_card_1)
                    self.selected_hex_stats.append(stat_text_card_2)
                    self.selected_hex_stats.append(stat_text_card_3)
                    self.label_selected_ship_stats_1.text = self.selected_hex_stats[0]
                    self.label_selected_ship_stats_2.text = self.selected_hex_stats[1]
                    self.label_selected_ship_stats_3.text = self.selected_hex_stats[2]
            else:
                self.selected_hex_stats.clear()
                self.selected_hex_stats.append("")
                self.selected_hex_stats.append("")
                self.selected_hex_stats.append("")
                self.label_selected_ship_stats_1.text = self.selected_hex_stats[0]
                self.label_selected_ship_stats_2.text = self.selected_hex_stats[1]
                self.label_selected_ship_stats_3.text = self.selected_hex_stats[2]
        else:
            return super(GameScreen, self).on_touch_down(touch)
    
    def mouse_pos(self, window, pos):
        if sm.current == "Game Screen" and not self.in_animation and not self.update_in_action and not self.is_paused and not self.block_mouse_pos:
            #print("mouse_pos: x = %s, y = %s" % (pos[0], pos[1]))
            found, xxx, yyy = _find_pos_of_tile(dp(pos[0]), dp(pos[1]))
            if self.game_type == 1 and self.current_player == 1:
                if found:
                    if self.highlighted_hex[0] == yyy and self.highlighted_hex[1] == xxx:
                        pass
                    else:
                        self.try_to_change(yyy, xxx)
                else:
                    pass
                    #print("--------")
            elif self.game_type == 2:
                if found:
                    if self.highlighted_hex[0] == yyy and self.highlighted_hex[1] == xxx:
                        pass
                    else:
                        self.try_to_change(yyy, xxx)
                else:
                    #print("--------")
                    self.try_to_change(yyy, xxx)
            if found:
                yy = self.selected_hex[0]
                xx = self.selected_hex[1]
                ffound = False
                for f in range(len(self.player_1_fleet)):
                    if self.player_1_fleet[f].tile[0] == yy and self.player_1_fleet[f].tile[1] == xx:
                        squadron = self.player_1_fleet[f]
                        ffound = True
                        break
                if not ffound:
                    for f in range(len(self.player_2_fleet)):
                        if self.player_2_fleet[f].tile[0] == yy and self.player_2_fleet[f].tile[1] == xx:
                            squadron = self.player_2_fleet[f]
                            ffound = True
                            break
                fffound = False
                for f in range(len(self.player_2_fleet)):
                    if self.player_2_fleet[f].tile[0] == yyy and self.player_2_fleet[f].tile[1] == xxx:
                        enemy = self.player_2_fleet[f]
                        fffound = True
                        break
                if not fffound:
                    for f in range(len(self.player_1_fleet)):
                        if self.player_1_fleet[f].tile[0] == yyy and self.player_1_fleet[f].tile[1] == xxx:
                            enemy = self.player_1_fleet[f]
                            fffound = True
                            break
                #if hex_grid_ids_and_states[yyy][xxx][6] and self.current_player == 1:
                #elif hex_grid_ids_and_states[yyy][xxx][6] and self.current_player == 2:
                if ffound and fffound:
                    self.label_preview_attack_text = squadron.deal_damage(enemy, True, 0, 0)
                    self.label_preview_attack.text = self.label_preview_attack_text
                else:
                    self.label_preview_attack.text = ""
                if fffound:
                    if hex_grid_ids_and_states[yyy][xxx][3] or hex_grid_ids_and_states[yyy][xxx][4]:
                        i = enemy.s_id
                        stat_text_card_1 = listofships[i].stat_text_card_1
                        stat_text_card_2 = listofships[i].stat_text_card_2
                        stat_text_card_3 = listofships[i].stat_text_card_3
                        self.label_selected_ship_stats_1.text = stat_text_card_1
                        self.label_selected_ship_stats_2.text = stat_text_card_2
                        self.label_selected_ship_stats_3.text = stat_text_card_3
                else:
                    self.label_selected_ship_stats_1.text = self.selected_hex_stats[0]
                    self.label_selected_ship_stats_2.text = self.selected_hex_stats[1]
                    self.label_selected_ship_stats_3.text = self.selected_hex_stats[2]
    
    def reset_in_range(self, empty, *args):
        if len(args) == 0:
            for i in range(7):
                if i == 0:
                    max_j = 9
                elif i % 2 != 0:
                    max_j = 10
                else:
                    max_j = 9
                for j in range(max_j):
                    if empty:
                        hex_grid_ids_and_states[i][j][1] = False
                        hex_grid_ids_and_states[i][j][6] = False
                    self.try_to_change_general(i, j)
        else:
            print("reset_in_range with *args")
            if args[0] == True:
                for i in range(7):
                    if i == 0:
                        max_j = 9
                    elif i % 2 != 0:
                        max_j = 10
                    else:
                        max_j = 9
                    for j in range(max_j):
                        hex_grid_ids_and_states[i][j][1] = False
                        self.try_to_change_general(i, j)
    
    def play_sound_ships_move(self, *args):
        global sound_ship_id
        ships_move_sound[sound_ship_id].play()
    
    def play_sound_ships_shoot(self, *args):
        global sound_ship_id
        ships_shoot_sound[sound_ship_id].play()
    
    def play_sound_ships_explode(self, *args):
        global sound_ship_id
        ships_explosion_sound[sound_ship_id].play()
    
    def calc_in_range(self, squadron, y, x, *args):
        self.reset_in_range(True)
        mvrng = squadron.movement
        wpnrng = squadron.weapon_range
        if len(args) == 0:
            cur_y = y
            cur_x = x
            for i in range(y - mvrng, y + mvrng + 1):
                if i >= 0 and i <= 6:
                    #print("\ni = %s\n" % (i))
                    if i == 0:
                        max_j = 9
                    elif i % 2 != 0:
                        max_j = 10
                    else:
                        max_j = 9
                    for j in range(x - mvrng, x + mvrng + 1):
                        if j >= 0 and j < max_j:
                            #print("\nmax_j = %s\nj = %s\n" % (max_j, j))
                            rng = calc_range_between(y, x, i, j, max_j)
                            if rng <= mvrng:
                                if not hex_grid_ids_and_states[i][j][3] and not hex_grid_ids_and_states[i][j][4]:
                                    hex_grid_ids_and_states[i][j][1] = True
        target_in_range = False
        cur_y = y
        cur_x = x
        for i in range(y - wpnrng, y + wpnrng + 1):
            if i >= 0 and i <= 6:
                #print("\ni = %s\n" % (i))
                if i == 0:
                    max_j = 9
                elif i % 2 != 0:
                    max_j = 10
                else:
                    max_j = 9
                for j in range(x - wpnrng, x + wpnrng + 1):
                    if j >= 0 and j < max_j:
                        #print("\nmax_j = %s\nj = %s\n" % (max_j, j))
                        rng = calc_range_between(y, x, i, j, max_j)
                        if rng <= wpnrng:
                            if hex_grid_ids_and_states[i][j][3] and self.current_player == 2:
                                hex_grid_ids_and_states[i][j][6] = True
                                target_in_range = True
                            elif hex_grid_ids_and_states[i][j][4] and self.current_player == 1:
                                hex_grid_ids_and_states[i][j][6] = True
                                target_in_range = True
        if len(args) == 0:
            self.reset_in_range(False)
        else:
            if args[0] == True:
                self.reset_in_range(False, True)
        return target_in_range
    
    def init_random_image_background(self, *args):
        i = random.randint(0, len(self.list_of_images) - 1)
        self.background_image.source = self.list_of_images[i]
    
    def init_hex_grid(self, *args):
        hex_grid_lb = []
        g_offset_y = 203
        for k in range(0, 7):
            hex_grid_lb.append([])
            if k == 0:
                coef = 0.5
                current_max_x_number = 9
                g_offset_x = 53
            elif (k % 2) != 0:
                coef = 0
                current_max_x_number = 10
                g_offset_x = 3
            else:
                coef = 0.5
                current_max_x_number = 9
                g_offset_x = 53
            for i in range(0, current_max_x_number):
                xxx = g_offset_x + 100 * i + 2 * i
                yyy = g_offset_y + 75 * k + 2 * k
                hex_grid_lb[k].append((dp(xxx), dp(yyy)))
        print(hex_grid_lb)
    
    def update_game_type_1(self, dt):
        time_factor = dt*60
    
    def update_game_type_2(self, dt):
        global sound_ship_id
        if not self.is_paused:
            time_factor = dt*60
            if len(self.actions_list) > 0  and not self.update_in_action:
                action = self.actions_list.pop(0)
                self.action_type = action.get("action_type")
                if self.action_type == "animation_move":
                    self.animation_image.size = (dp(115), dp(115))
                    self.action_projectile_id = action.get("ship_id")
                    self.action_direction = action.get("direction")
                    self.action_squadron.append(action.get("squadron"))
                    self.action_y0 = action.get("y0")
                    self.action_x0 = action.get("x0")
                    self.action_y1 = action.get("y1")
                    self.action_x1 = action.get("x1")
                    self.action_pos_y0 = action.get("pos_y0")
                    self.action_pos_x0 = action.get("pos_x0")
                    self.action_pos_y1 = action.get("pos_y1")
                    self.action_pos_x1 = action.get("pos_x1")
                    self.action_current_x = self.action_pos_x0
                    self.action_current_y = self.action_pos_y0
                    distance_x = abs(self.action_pos_x1 - self.action_pos_x0)
                    distance_y = abs(self.action_pos_y1 - self.action_pos_y0)
                    if distance_x > distance_y:
                        self.action_speed_x = self.SPEED
                        self.action_speed_y = self.action_speed_x * distance_y / distance_x
                    else:
                        self.action_speed_y = self.SPEED
                        self.action_speed_x = self.action_speed_y * distance_x / distance_y
                    if self.action_pos_x1 < self.action_pos_x0:
                        self.action_speed_x *= -1
                    if self.action_pos_y1 < self.action_pos_y0:
                        self.action_speed_y *= -1
                    self.action_animation_dt = 0
                    self.action_counter_1 = 0
                    self.action_counter_2 = 0
                    self.action_counter_3 = 0
                    self.action_counter_done = False
                    self.in_animation = True
                    self.update_in_action = True
                    sound_ship_id = self.action_squadron[0].s_id
                    Clock.schedule_once(self.play_sound_ships_move)
                    if not self.action_squadron[0].move_and_shoot:
                        self.time_to_change_selected = True
                        self.shoot_after_move = False
                    else:
                        self.shoot_after_move = True
                        self.do_once_set_shoot_and_move = True
                
                #   action = {"action_type": "shoot_projectile", "ship_id": squadron.s_id, "direction": direction, "pos_x0": self.self_hex_grid_coords_for_kv[yy][xx][0], "pos_y0": self.self_hex_grid_coords_for_kv[yy][xx][1]}
                
                #   action = {"action_type": "move_projectile", "ship_id": squadron.s_id, "direction": "lr", "pos_x0": self.self_hex_grid_coords_for_kv[yy][xx][0], "pos_y0": self.self_hex_grid_coords_for_kv[yy][xx][1], "pos_x1": self.self_hex_grid_coords_for_kv[yyy][xxx][0], "pos_y1": self.self_hex_grid_coords_for_kv[yyy][xxx][1]}
                
                #   action = {"action_type": "hit_projectile", "ship_id": self.s_id, "direction": direction, "pos_x1", "pos_y1"}
                
                #    action = {"action_type": "deal_damage", "direction": direction, "squadron": squadron, "enemy": enemy}
                
                #   action = {"action_type": "destroy_squadron", "squadron": enemy, "x": enemy.tile[1], "y": enemy.tile[0], "pos_x": xxx, "pos_y": yyy, "quantity": enemy.quantity_str, "text_card": text_card}
                
                #   action = {"action_type": "damage_squadron", "squadron": enemy, "x": enemy.tile[1], "y": enemy.tile[0], "pos_x": xxx, "pos_y": yyy, "quantity": quantity, "text_card": text_card}
                
                elif self.action_type == "shoot_projectile":
                    self.animation_image.size = (dp(115), dp(115))
                    self.action_projectile_id = action.get("ship_id")
                    self.action_direction = action.get("direction")
                    if self.action_direction == "lr":
                        self.action_mirrored_offset = 0
                    else:
                        self.action_mirrored_offset = 5
                    self.action_pos_x0 = action.get("pos_x0")
                    self.action_pos_y0 = action.get("pos_y0")
                    #self.action_current_x = self.action_pos_x0
                    #self.action_current_y = self.action_pos_y0
                    self.action_counter_1 = 0
                    self.action_counter_2 = 0
                    self.action_counter_3 = 0
                    self.action_counter_done = False
                    if self.action_direction == "lr":
                        self.action_mirrored_offset = 0
                    else:
                        self.action_mirrored_offset = 5
                    self.animation_image.allow_stretch = True
                    self.animation_image.pos = (self.action_pos_x0 + dp(animation_list_offset_projectile_shoot[self.action_projectile_id + self.action_mirrored_offset][0]), self.action_pos_y0 + dp(animation_list_offset_projectile_shoot[self.action_projectile_id + self.action_mirrored_offset][1]))
                    self.animation_image.opacity = 1
                    self.action_animation_dt = 0
                    self.in_animation = True
                    self.update_in_action = True
                    self.block_mouse_pos = True
                    sound_ship_id = self.action_projectile_id
                    Clock.schedule_once(self.play_sound_ships_shoot)
                
                elif self.action_type == "move_projectile":
                    self.action_projectile_id = action.get("ship_id")
                    self.action_direction = action.get("direction")
                    if self.action_direction == "lr":
                        self.action_mirrored_offset = 0
                    else:
                        self.action_mirrored_offset = 5
                    self.action_pos_x0 = action.get("pos_x0")
                    self.action_pos_y0 = action.get("pos_y0")
                    self.action_pos_x1 = action.get("pos_x1") + dp(animation_list_offset_projectile_move[self.action_projectile_id + self.action_mirrored_offset][0])
                    self.action_pos_y1 = action.get("pos_y1") + dp(animation_list_offset_projectile_move[self.action_projectile_id + self.action_mirrored_offset][1])
                    self.action_current_x = self.action_pos_x0
                    self.action_current_y = self.action_pos_y0
                    self.action_counter_1 = 0
                    self.action_counter_2 = 0
                    self.action_counter_3 = 0
                    self.action_counter_done = False
                    distance_x = abs(self.action_pos_x1 - self.action_pos_x0)
                    distance_y = abs(self.action_pos_y1 - self.action_pos_y0)
                    if distance_x > distance_y:
                        self.action_speed_x = self.SPEED * 1.5
                        self.action_speed_y = self.action_speed_x * distance_y / distance_x * 1.17
                        time_ = distance_x / self.action_speed_x
                    else:
                        self.action_speed_y = self.SPEED * 1.75
                        self.action_speed_x = self.action_speed_y * distance_x / distance_y
                        time_ = distance_y / self.action_speed_y
                    if self.action_pos_x1 < self.action_pos_x0:
                        self.action_speed_x *= -1
                    if self.action_pos_y1 < self.action_pos_y0:
                        self.action_speed_y *= -1
                    #self.animation_image.opacity = 1
                    self.action_animation_dt = 0
                    self.in_animation = True
                    self.update_in_action = True
                    self.action_counter_2 = Animation(x = dp(self.action_pos_x1), y = dp(self.action_pos_y1), t = "linear")
                    self.action_counter_2.start(self.animation_image)
                
                elif self.action_type == "hit_projectile":
                    self.action_projectile_id = action.get("ship_id")
                    self.action_direction = action.get("direction")
                    if self.action_direction == "lr":
                        self.action_mirrored_offset = 0
                    else:
                        self.action_mirrored_offset = 5
                    self.action_pos_x1 = action.get("pos_x1") + dp(animation_list_offset_projectile_hit[self.action_projectile_id + self.action_mirrored_offset][0])
                    self.action_pos_y1 = action.get("pos_y1") + dp(animation_list_offset_projectile_hit[self.action_projectile_id + self.action_mirrored_offset][1])
                    self.action_counter_1 = 0
                    self.action_counter_2 = 0
                    self.action_counter_3 = 0
                    self.action_counter_done = False
                    #self.animation_image.opacity = 1
                    self.action_animation_dt = 0
                    self.in_animation = True
                    self.update_in_action = True
                
                elif self.action_type == "deal_damage":
                    self.action_squadron.append(action.get("squadron"))
                    self.action_squadron.append(action.get("enemy"))
                    self.action_direction = action.get("direction")
                    self.action_pos_x0 = action.get("pos_x0")
                    self.action_pos_y0 = action.get("pos_y0")
                    self.action_animation_dt = 0
                    self.action_counter_1 = 0
                    self.action_counter_2 = 0
                    self.action_counter_3 = 0
                    self.action_counter_done = False
                    if self.action_direction == "lr":
                        self.action_mirrored_offset = 0
                    else:
                        self.action_mirrored_offset = 5
                    self.in_animation = True
                    self.update_in_action = True
                    self.time_to_change_selected = True
                
                elif self.action_type == "destroy_squadron":
                    self.action_squadron.append(action.get("squadron"))
                    self.action_squadron.append(action.get("enemy"))
                    for i in range(len(self.squadron_order_list)):
                        if self.squadron_order_list[i].sq_id == self.action_squadron[1].sq_id:
                            self.to_remove_from_list.append(i)
                            break
                    self.action_x0 = action.get("x")
                    self.action_y0 = action.get("y")
                    self.action_projectile_id = self.action_squadron[1].s_id
                    if self.action_squadron[1].direction == "lr":
                        self.action_mirrored_offset = 0
                    else:
                        self.action_mirrored_offset = 5
                    self.action_pos_x0 = action.get("pos_x") + dp(animation_list_offset_ship_destroyed[self.action_projectile_id + self.action_mirrored_offset][0])
                    self.action_pos_y0 = action.get("pos_y") + dp(animation_list_offset_ship_destroyed[self.action_projectile_id + self.action_mirrored_offset][1])
                    self.action_text_card = action.get("text_card")
                    self.animation_image.allow_stretch = False
                    if self.action_squadron[1].s_id == 0:
                        self.animation_image.size = (dp(100), dp(100))
                    elif self.action_squadron[1].s_id == 1:
                        self.animation_image.size = (dp(200), dp(200))
                    elif self.action_squadron[1].s_id == 2:
                        self.animation_image.size = (dp(200), dp(200))
                    elif self.action_squadron[1].s_id == 3:
                        self.animation_image.size = (dp(160), dp(160))
                    elif self.action_squadron[1].s_id == 4:
                        self.animation_image.size = (dp(175), dp(175))
                    self.action_animation_dt = 0
                    self.action_counter_1 = 0
                    self.action_counter_2 = 0
                    self.action_counter_3 = 0
                    self.action_counter_done = False
                    #self.list_of_hexes[self.action_squadron[1].tile[0]][self.action_squadron[1].tile[1]].source = self.src_hexagon_border
                    self.action_squadron[1].image.opacity = 0
                    self.action_squadron[1].plate_image.opacity = 0
                    self.action_squadron[1].label.opacity = 0
                    self.animation_image.opacity = 1
                    self.animation_image.pos = (self.action_pos_x0, self.action_pos_y0)
                    #self.animation_image.source = animation_list_ship_destroyed[self.action_projectile_id + self.action_mirrored_offset][0]
                    self.in_animation = True
                    self.update_in_action = True
                    self.block_mouse_pos = False
                    sound_ship_id = self.action_squadron[1].s_id
                    Clock.schedule_once(self.play_sound_ships_explode)
                
                elif self.action_type == "damage_squadron":
                    self.action_squadron.append(action.get("squadron"))
                    self.action_squadron.append(action.get("enemy"))
                    self.action_x0 = action.get("x")
                    self.action_y0 = action.get("y")
                    self.action_pos_x0 = action.get("pos_x")
                    self.action_pos_y0 = action.get("pos_y")
                    self.action_text_card = action.get("text_card")
                    self.action_animation_dt = 0
                    self.action_counter_1 = 0
                    self.action_counter_2 = 0
                    self.action_counter_3 = 0
                    self.action_counter_done = False
                    self.in_animation = True
                    self.update_in_action = True
                    self.block_mouse_pos = False
            
            #-----------------------------------------------
            
            if self.in_animation and self.update_in_action:
                if self.action_type == "animation_move":
                    #self.action_squadron[0].move_with_vector(self.action_speed)
                    if not self.action_counter_done:
                        self.action_squadron[0].move_ship_animation(self.action_pos_x1, self.action_pos_y1)
                        self.action_counter_done = True
                    self.action_animation_dt += dt
                    max_len = len(animation_list_ship_move[self.action_projectile_id + self.action_mirrored_offset])
                    if self.action_animation_dt >= dt * self.EXHAUST_ANIMATION * self.action_counter_1 and self.action_counter_done:
                        if self.action_counter_1 < max_len:
                            #print(self.action_counter_1)
                            self.animation_image.source = animation_list_ship_move[self.action_projectile_id + self.action_mirrored_offset][self.action_counter_1]
                        self.action_counter_1 += 1
                        if self.action_counter_1 == max_len:
                            self.action_counter_1 = 0
                    #temp = Vector(*self.action_speed) + self.action_squadron[0].image.pos
                    #self.action_current_x = temp[0]
                    #self.action_current_y = temp[1]
                    self.action_current_x = self.action_squadron[0].image.pos[0]
                    self.action_current_y = self.action_squadron[0].image.pos[1]
                    #print("cur_x = %s, cur_y = %s" % (self.action_current_x, self.action_current_y))
                    x_in_place = False
                    y_in_place = False
                    if self.action_speed_x < 0:
                        if self.action_current_x <= self.action_pos_x1:
                            x_in_place = True
                    else:
                        if self.action_current_x >= self.action_pos_x1:
                            x_in_place = True
                    if self.action_speed_y < 0:
                        if self.action_current_y <= self.action_pos_y1:
                            y_in_place = True
                    else:
                        if self.action_current_y >= self.action_pos_y1:
                            y_in_place = True
                    if x_in_place and y_in_place:
                        self.action_squadron[0].move_ship_animation_finish(self.action_pos_x1, self.action_pos_y1, self.action_x1, self.action_y1)
                        self.animation_image.source = self.src_empty
                        self.in_animation = False
                        self.update_in_action = False
                        self.action_squadron.clear()
                
                elif self.action_type == "shoot_projectile":
                    self.action_animation_dt += dt
                    if self.action_animation_dt >= dt * self.ANIMATION_SPEED * self.action_counter_1 and not self.action_counter_done and self.action_counter_1 < len(animation_list_projectile_shoot[self.action_projectile_id + self.action_mirrored_offset]):
                        self.animation_image.source = animation_list_projectile_shoot[self.action_projectile_id + self.action_mirrored_offset][self.action_counter_1]
                        self.action_counter_1 += 1
                        if self.action_counter_1 == len(animation_list_projectile_shoot[self.action_projectile_id + self.action_mirrored_offset]):
                            self.action_counter_done = True
                    elif self.action_counter_done:
                        self.animation_image.source = animation_list_projectile_move[self.action_projectile_id + self.action_mirrored_offset][0]
                        #self.animation_image.opacity = 0
                        self.in_animation = False
                        self.update_in_action = False
                        self.action_squadron.clear()
                
                elif self.action_type == "move_projectile":
                    #self.action_counter_2.start(self.animation_image)
                    #self.action_animation_dt += dt
                    #if self.action_animation_dt >= time_factor * 5:
                    #    self.action_counter_2 += Animation(x = dp(self.action_pos_x1), y = dp(self.action_pos_y1), duration = time_factor * 5)
                    #    self.action_counter_2.start(self.animation_image)
                    #temp = Vector(*self.action_speed) + self.animation_image.pos
                    #self.animation_image.pos = temp
                    #self.action_current_x = temp[0]
                    #self.action_current_y = temp[1]
                    self.action_current_x = self.animation_image.pos[0]
                    self.action_current_y = self.animation_image.pos[1]
                    x_in_place = False
                    y_in_place = False
                    #print("\ncurr x = %s, target x = %s\ncurr y = %s, target y = %s\n" % (self.action_current_x, self.action_pos_x1, self.action_current_y, self.action_pos_y1))
                    if self.action_speed_x < 0:
                        if self.action_current_x <= self.action_pos_x1:
                            x_in_place = True
                    else:
                        if self.action_current_x >= self.action_pos_x1:
                            x_in_place = True
                    if self.action_speed_y < 0:
                        if self.action_current_y <= self.action_pos_y1:
                            y_in_place = True
                    else:
                        if self.action_current_y >= self.action_pos_y1:
                            y_in_place = True
                    if x_in_place and y_in_place:
                        self.animation_image.source = self.src_empty
                        self.action_counter_2.cancel_all(self.animation_image)
                        #self.animation_image.opacity = 0
                        self.in_animation = False
                        self.update_in_action = False
                        self.action_squadron.clear()
                
                elif self.action_type == "hit_projectile":
                    self.animation_image.pos = (self.action_pos_x1, self.action_pos_y1)
                    self.action_animation_dt += dt
                    if self.action_animation_dt >= dt * self.ANIMATION_SPEED * self.action_counter_1 and not self.action_counter_done and self.action_counter_1 < len(animation_list_projectile_hit[self.action_projectile_id + self.action_mirrored_offset]):
                        self.animation_image.source = animation_list_projectile_hit[self.action_projectile_id + self.action_mirrored_offset][self.action_counter_1]
                        self.action_counter_1 += 1
                        if self.action_counter_1 == len(animation_list_projectile_hit[self.action_projectile_id + self.action_mirrored_offset]):
                            self.action_counter_done = True
                    elif self.action_counter_done:
                        self.animation_image.source = self.src_empty
                        #self.animation_image.opacity = 0
                        self.in_animation = False
                        self.update_in_action = False
                        self.action_squadron.clear()
                        #self.actions_list.clear()
                
                elif self.action_type == "deal_damage":
                    self.action_squadron[0].deal_damage(self.action_squadron[1], False, self.action_pos_x0, self.action_pos_y0)
                    #self.try_to_change(-1, -1)
                    #self.try_to_change_selected(-1, -1)
                    self.action_squadron.clear()
                    self.in_animation = False
                    self.update_in_action = False
                
                elif self.action_type == "destroy_squadron":
                    self.action_animation_dt += dt
                    if self.action_animation_dt >= dt * self.ANIMATION_SPEED * self.action_counter_1 and not self.action_counter_done and self.action_counter_1 < len(animation_list_ship_destroyed[self.action_projectile_id + self.action_mirrored_offset]):
                        self.animation_image.source = animation_list_ship_destroyed[self.action_projectile_id + self.action_mirrored_offset][self.action_counter_1]
                        self.action_counter_1 += 1
                        if self.action_counter_1 == len(animation_list_ship_destroyed[self.action_projectile_id + self.action_mirrored_offset]):
                            self.action_counter_done = True
                    elif self.action_counter_done:
                        self.animation_image.source = self.src_empty
                        #self.animation_image.opacity = 0
                        
                        self.label_temp_result.text = self.action_text_card
                        self.list_of_hexes[self.action_squadron[1].tile[0]][self.action_squadron[1].tile[1]].source = self.src_hexagon_border
                        hex_grid_ids_and_states[self.action_squadron[1].tile[0]][self.action_squadron[1].tile[1]][1] = False
                        hex_grid_ids_and_states[self.action_squadron[1].tile[0]][self.action_squadron[1].tile[1]][2] = False
                        hex_grid_ids_and_states[self.action_squadron[1].tile[0]][self.action_squadron[1].tile[1]][3] = False
                        hex_grid_ids_and_states[self.action_squadron[1].tile[0]][self.action_squadron[1].tile[1]][4] = False
                        hex_grid_ids_and_states[self.action_squadron[1].tile[0]][self.action_squadron[1].tile[1]][5] = False
                        hex_grid_ids_and_states[self.action_squadron[1].tile[0]][self.action_squadron[1].tile[1]][6] = False
                        self.action_squadron[1].remove_from_game_field(widget = self)
                        self.action_squadron[1].tile[0] = -17
                        self.action_squadron[1].tile[1] = -17
                        
                        if self.current_player == 1:
                            self.list_of_hexes[self.action_squadron[0].tile[0]][self.action_squadron[0].tile[1]].source = self.src_hexagon_4
                        if self.current_player == 2:
                            self.list_of_hexes[self.action_squadron[0].tile[0]][self.action_squadron[0].tile[1]].source = self.src_hexagon_5
                        hex_grid_ids_and_states[self.selected_hex[0]][self.selected_hex[1]][5] = False
                        self.selected_hex[0] = -1
                        self.selected_hex[1] = -1
                        self.reset_in_range(True)
                        #self.try_to_change_selected(self.selected_hex[0], self.selected_hex[1])
                        self.selected_hex_stats.clear()
                        self.selected_hex_stats.append("")
                        self.selected_hex_stats.append("")
                        self.selected_hex_stats.append("")
                        self.label_selected_ship_stats_1.text = ""
                        self.label_selected_ship_stats_2.text = ""
                        self.label_selected_ship_stats_3.text = ""
                        self.in_animation = False
                        self.update_in_action = False
                        self.action_squadron.clear()
                
                elif self.action_type == "damage_squadron":
                    self.label_temp_result.text = self.action_text_card
                    self.action_squadron[1].update_quantity_str()
                    self.action_squadron[1].label.text = self.action_squadron[1].quantity_str
                    if self.current_player == 1:
                        self.list_of_hexes[self.action_squadron[0].tile[0]][self.action_squadron[0].tile[1]].source = self.src_hexagon_4
                    if self.current_player == 2:
                        self.list_of_hexes[self.action_squadron[0].tile[0]][self.action_squadron[0].tile[1]].source = self.src_hexagon_5
                    self.action_squadron.clear()
                    hex_grid_ids_and_states[self.selected_hex[0]][self.selected_hex[1]][5] = False
                    self.selected_hex[0] = -1
                    self.selected_hex[1] = -1
                    self.reset_in_range(True)
                    #self.try_to_change_selected(self.selected_hex[0], self.selected_hex[1])
                    self.selected_hex_stats.clear()
                    self.selected_hex_stats.append("")
                    self.selected_hex_stats.append("")
                    self.selected_hex_stats.append("")
                    self.label_selected_ship_stats_1.text = ""
                    self.label_selected_ship_stats_2.text = ""
                    self.label_selected_ship_stats_3.text = ""
                    self.in_animation = False
                    self.update_in_action = False
                    
            if not self.update_in_action and not self.in_animation and len(self.actions_list) == 0:
                if self.time_to_change_selected:
                    if len(self.squadron_order_list) >= 1:
                        left_pl = self.squadron_order_list[0].player_id
                        time_to_end = True
                        for i in range(len(self.squadron_order_list)):
                            if self.squadron_order_list[i].player_id != left_pl and i not in self.to_remove_from_list:
                                time_to_end = False
                                break
                        if time_to_end:
                            self.is_paused = True
                            return
                    for i in range(len(self.squadron_order_list)):
                        print("Previous: Ship = %s, Squadron = %s, Player = %s, i = %s" % (self.squadron_order_list[i].s_id, self.squadron_order_list[i].sq_id, self.squadron_order_list[i].player_id, i))
                    print("\n\nList of ships to remove: %s" % (self.to_remove_from_list))
                    print("Previous: Turn of player = %s, current player = %s, turn number = %s" % (self.turn_of_player, self.current_player, self.turn_number))
                    print("Previous squadron: ship = %s, sq_id = %s, player = %s\n" % (self.squadron_order_list[self.current_squadron_index].s_id, self.squadron_order_list[self.current_squadron_index].sq_id, self.squadron_order_list[self.current_squadron_index].player_id))
                    self.current_squadron_index += 1
                    for i in range(len(self.to_remove_from_list)):
                        if self.current_squadron_index == self.to_remove_from_list[i]:
                            self.current_squadron_index += 1
                    if self.current_squadron_index >= len(self.squadron_order_list):
                        self.current_squadron_index = 0
                        self.to_remove_from_list.sort()
                        for i in range(len(self.to_remove_from_list) - 1, -1, -1):
                            print("Length of squadron_order_list = ", len(self.squadron_order_list))
                            print("To remove index = ", self.to_remove_from_list[i])
                            self.squadron_order_list.pop(self.to_remove_from_list[i])
                        for i in range(len(self.squadron_order_list)):
                            print("Ship = %s, Squadron = %s, Player = %s, i = %s" % (self.squadron_order_list[i].s_id, self.squadron_order_list[i].sq_id, self.squadron_order_list[i].player_id, i))
                        self.to_remove_from_list.clear()
                        
                        if len(self.squadron_order_list) >= 1:
                            left_pl = self.squadron_order_list[0].player_id
                            time_to_end = True
                            for i in range(len(self.squadron_order_list)):
                                if self.squadron_order_list[i].player_id != left_pl:
                                    time_to_end = False
                                    break
                        if time_to_end:
                            self.is_paused = True
                            return
                        else:
                            self.turn_number += 1
                    self.current_player = self.squadron_order_list[self.current_squadron_index].player_id
                    self.turn_of_player = self.current_player
                    self.selected_hex[0] = self.squadron_order_list[self.current_squadron_index].tile[0]
                    self.selected_hex[1] = self.squadron_order_list[self.current_squadron_index].tile[1]
                    self.try_to_change_selected(self.selected_hex[0], self.selected_hex[1])
                    self.calc_in_range(self.squadron_order_list[self.current_squadron_index], self.selected_hex[0], self.selected_hex[1])
                    self.try_to_change_selected_labels(self.squadron_order_list[self.current_squadron_index].s_id)
                    self.time_to_change_selected = False
                    print("\nList of ships to remove: %s" % (self.to_remove_from_list))
                    print("Turn of player = %s, current player = %s, turn number = %s" % (self.turn_of_player, self.current_player, self.turn_number))
                    print("Current squadron: ship = %s, sq_id = %s, player = %s\n\n" % (self.squadron_order_list[self.current_squadron_index].s_id, self.squadron_order_list[self.current_squadron_index].sq_id, self.squadron_order_list[self.current_squadron_index].player_id))
                elif self.shoot_after_move and self.do_once_set_shoot_and_move:
                    self.selected_hex[0] = self.squadron_order_list[self.current_squadron_index].tile[0]
                    self.selected_hex[1] = self.squadron_order_list[self.current_squadron_index].tile[1]
                    self.try_to_change_selected(self.selected_hex[0], self.selected_hex[1])
                    if not self.calc_in_range(self.squadron_order_list[self.current_squadron_index], self.selected_hex[0], self.selected_hex[1], True):
                        hex_grid_ids_and_states[self.selected_hex[0]][self.selected_hex[1]][5] = False
                        self.selected_hex[0] = -1
                        self.selected_hex[1] = -1
                        self.reset_in_range(True)
                        #self.try_to_change_selected(self.selected_hex[0], self.selected_hex[1])
                        self.selected_hex_stats.clear()
                        self.selected_hex_stats.append("")
                        self.selected_hex_stats.append("")
                        self.selected_hex_stats.append("")
                        self.label_selected_ship_stats_1.text = ""
                        self.label_selected_ship_stats_2.text = ""
                        self.label_selected_ship_stats_3.text = ""
                        self.time_to_change_selected = True
                        self.shoot_after_move = False
                    else:
                        self.try_to_change_selected_labels(self.squadron_order_list[self.current_squadron_index].s_id)
                    self.do_once_set_shoot_and_move = False
                    
    
    def update_game_type_3(self, dt):
        time_factor = dt*60

def _find_pos_of_tile(x, y):
    yyy = -100
    xxx = -100
    for i in range(7):
        if i == 0:
            max_j = 9
        elif i % 2 != 0:
            max_j = 10
        else:
            max_j = 9
        for j in range(max_j):
            if _check_dot_inside_borders(game_screen.list_of_hexes[i][j].pos[0], game_screen.list_of_hexes[i][j].pos[1], dp(x), dp(y)):
                yyy = i
                xxx = j
                return True, xxx, yyy
    return False, xxx, yyy

def _check_dot_inside_borders(pos_x, pos_y, xx, yy):
    x = xx - pos_x
    y = yy - pos_y
    x_1 = 50
    y_1 = 0
    x_2 = 100
    y_2 = 25
    x_3 = 100
    y_3 = 75
    x_4 = 50
    y_4 = 100
    x_5 = 0
    y_5 = 75
    x_6 = 0
    y_6 = 25
    #print("x = %s, y = %s" % (x, y))
    if x >= x_6 and x <= x_1 and y >= y_1 and y <= y_4:
        y_on_line_1 = (0 - x) / 2 + (25)
        y_on_line_2 = (x) / 2 + (75)
        #print("x = %s, y_on_line_1 = %s" % (x, y_on_line_1))
        #print("x = %s, y_on_line_2 = %s" % (x, y_on_line_2))
        if y >= y_on_line_1 and y <= y_on_line_2:
            return True
        else:
            return False
    elif x >= x_1 and x <= x_2 and y >= y_1 and y <= y_4:
        y_on_line_3 = (x - 50) / 2 + (0)
        y_on_line_4 = (50 - x) / 2 + (100)
        #print("x = %s, y_on_line_3 = %s" % (x, y_on_line_3))
        #print("x = %s, y_on_line_4 = %s" % (x, y_on_line_4))
        if y >= y_on_line_3 and y <= y_on_line_4:
            return True
        else:
            return False

def calc_range_between(y, x, i, j, max_j):
    y1 = x
    x1 = y
    y2 = j
    x2 = i
    du = x2 - x1
    dv = (y2 + x2 // 2) - (y1 + x1 // 2)
    return max(abs(du), abs(dv)) if ((du >= 0 and dv >= 0) or (du < 0 and dv < 0)) else abs(du) + abs(dv)

def _get_damage_color(attack_type):
    if attack_type == 0:
        loc_damage_type_color = laser_color
    elif attack_type == 1:
        loc_damage_type_color = kinetic_color
    elif attack_type == 2:
        loc_damage_type_color = plasma_color
    elif attack_type == 3:
        loc_damage_type_color = rocket_color
    elif attack_type == 4:
        loc_damage_type_color = rail_color
    return loc_damage_type_color

"""
class Plate(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self.rotation = Rotation(angle=self.angle, origin=self.center)

        with self.canvas.after:
            PopMatrix()
"""
class Squadron():
    #wgt_pos_0 = NumericProperty(0)
    #wgt_pos_1 = NumericProperty(0)
    #wgt_pos = ReferenceListProperty(wgt_pos_0, wgt_pos_1)
    def __init__(self, name, s_id, sq_id, player_id, quantity, attack, defense, weapon_range, accuracy, speed, movement, attack_type, defense_laser, defense_kinetic, defense_plasma, defense_rocket, defense_rail, move_and_shoot, imagefile, platefile):
        self.name = name
        self.s_id = s_id
        self.sq_id = sq_id
        self.player_id = player_id
        self.quantity = quantity
        self.attack = attack
        self.defense = defense
        self.weapon_range = weapon_range
        self.accuracy = accuracy
        self.speed = speed
        self.movement = movement
        self.attack_type = attack_type
        self.defense_laser = defense_laser
        self.defense_kinetic = defense_kinetic
        self.defense_plasma = defense_plasma
        self.defense_rocket = defense_rocket
        self.defense_rail = defense_rail
        self.move_and_shoot = move_and_shoot
        self.imagefile = imagefile
        self.platefile = platefile
        self.image = Image(source = self.imagefile)
        if self.image.source[7] == "z":
            self.direction = "rl"
        else:
            self.direction = "lr"
        self.image.size_hint = (None, None)
        #self.size_x = 100
        #self.size_y = 100
        self.quantity_str = _separator_for_output(self.quantity)
        self.plate_image = Image(source = self.platefile)
        self.plate_image.size_hint = (None, None)
        self.label = Label(text = self.quantity_str, color = (0, 0, 0, 1), font_size = dp(12))
        self.label.size_hint = (None, None)
        self.health = self.defense * self.quantity
        self.tile = []
    def put_on_game_field(self, widget, x, y, size_x, size_y, hex_y, hex_x):
        self.size_x = dp(size_x)
        self.size_y = dp(size_y)
        self.image.pos = (dp(x), dp(y))
        self.image.size = (dp(size_x), dp(size_y))
        self.plate_image.pos = (dp(x), dp(y))
        self.plate_image.size = (dp(size_x), dp(size_y))
        self.label.pos = (dp(x), dp(y) - dp(30))
        self.tile.append(hex_y)
        self.tile.append(hex_x)
        game_screen.add_widget(self.image)
        self.plate_image.add_widget(self.label)
        self.image.add_widget(self.plate_image)
        #self.wgt_pos_0 = self.image.pos[0]
        #self.wgt_pos_1 = self.image.pos[1]
    def remove_from_game_field(self, widget):
        widget.remove_widget(self.label)
        widget.remove_widget(self.plate_image)
        widget.remove_widget(self.image)
    def move_with_vector(self, speed):
        self.image.pos = Vector(*speed) + self.image.pos
        self.plate_image.pos = Vector(*speed) + self.plate_image.pos
        self.label.pos = Vector(*speed) + self.label.pos
        #self.wgt_pos_0 = self.image.pos[0]
        #self.wgt_pos_1 = self.image.pos[0]
    def move_ship(self, x, y, xxx, yyy):
        self.image.pos = (dp(x), dp(y))
        self.plate_image.pos = (dp(x), dp(y))
        self.label.pos = (dp(x), dp(y) - dp(30))
        self.tile[0] = yyy
        self.tile[1] = xxx
    def move_ship_animation(self, x, y):
        l_index = self.s_id if self.player_id == 1 else self.s_id + 5
        game_screen.animation_image.allow_stretch = False
        game_screen.animation_image.source = animation_list_ship_move[l_index][0]
        offset_x = animation_list_offset_ship_move[l_index][0]
        offset_y = animation_list_offset_ship_move[l_index][1]
        game_screen.animation_image.pos = (self.image.pos[0] + offset_x, self.image.pos[1] - offset_y)
        anim = Animation(x = x, y = y, t = "in_out_cubic")
        anim_move = Animation(x = x + offset_x, y = y - offset_y, t = "in_out_cubic")
        anim.start(self.image)
        anim.start(self.plate_image)
        anim.start(self.label)
        anim_move.start(game_screen.animation_image)
    def move_ship_animation_finish(self, x, y, xxx, yyy):
        self.image.pos = (dp(x), dp(y))
        self.plate_image.pos = (dp(x), dp(y))
        self.label.pos = (dp(x), dp(y) - dp(30))
        self.tile[0] = yyy
        self.tile[1] = xxx
        if game_screen.current_player == 1:
            hex_grid_ids_and_states[yyy][xxx][3] = True
        else:
            hex_grid_ids_and_states[yyy][xxx][4] = True
        game_screen.try_to_change(-1, -1)
        game_screen.try_to_change_selected(-1, -1)
    def update_quantity_str(self):
        self.quantity = int(_my_round_up(self.health / self.defense))
        self.quantity_str = _separator_for_output(self.quantity)
    def calc_damage_modifier(self, attack_type):
        if attack_type == 0:
            defense_mod = self.defense_laser
        elif attack_type == 1:
            defense_mod = self.defense_kinetic
        elif attack_type == 2:
            defense_mod = self.defense_plasma
        elif attack_type == 3:
            defense_mod = self.defense_rocket
        elif attack_type == 4:
            defense_mod = self.defense_rail
        damage_mod = _my_truncate(1 + (100 - defense_mod) / 100, 2)
        return damage_mod
    def deal_damage(self, enemy, theory, enemy_pos_x0, enemy_pos_y0):
        loc_damage_type_color = _get_damage_color(self.attack_type)
        loc_min_color = "00FF00"
        loc_max_color = "FF0000"
        loc_damage = text_strings.damage[1]
        if enemy.s_id == 0:
            loc_name = text_strings.light_fighter
        elif enemy.s_id == 1:
            loc_name = text_strings.heavy_fighter
        elif enemy.s_id == 2:
            loc_name = text_strings.frigate
        elif enemy.s_id == 3:
            loc_name = text_strings.cruiser
        elif enemy.s_id == 4:
            loc_name = text_strings.dreadnought
        loc_min = text_strings.loc_min
        loc_max = text_strings.loc_max
        loc_destroyed = text_strings.destroyed
        damage_mod = enemy.calc_damage_modifier(self.attack_type)
        if theory:
            min_damage = int(self.attack * damage_mod * self.quantity * self.accuracy / 100)
            min_quantity = int(min_damage / enemy.defense) if enemy.health - min_damage >= 0 else enemy.quantity
            max_damage = int(self.attack * damage_mod * self.quantity * 100 / 100)
            max_quantity = int(max_damage / enemy.defense) if enemy.health - max_damage >= 0 else enemy.quantity
            text_card = "[color=#%s]%s:\n%s %s\n-%s %s\n[/color][color=#%s]%s:\n%s %s\n-%s %s[/color]" % (loc_min_color, loc_min, min_damage, loc_damage, min_quantity, loc_name, loc_max_color, loc_max, max_damage, loc_damage, max_quantity, loc_name)
            return text_card
        else:
            accuracy = random.randint(self.accuracy, 101)
            damage = _my_truncate(self.attack * damage_mod * self.quantity * accuracy / 100, 2)
            quantity = int(damage / enemy.defense) if enemy.health - damage >= 0 else int(enemy.quantity)
            enemy.health -= damage
            #found, xxx, yyy = _find_pos_of_tile(enemy.tile[1], enemy.tile[0])
            #print("\n\n\n_____\n%s, %s\n\n\n" % (xxx, yyy))
            #action = {"action_type": "hit_projectile", "ship_id": self.s_id, "direction": direction, "squadron": self, "enemy": enemy, "x": enemy.tile[1], "y": enemy.tile[0], "pos_x": xxx, "pos_y": yyy}
            #game_screen.actions_list.append(action)
            if enemy.health <= 0:
                text_card = "[color=#%s]%s %s\n%s[/color]" % (loc_damage_type_color, _separator_for_output(quantity), loc_name, loc_destroyed)
                #text_card = "[color=#%s]%s %s\n-%s %s[/color]" % (loc_damage_type_color, _separator_for_output(int(_my_truncate(damage, 0))), loc_damage, _separator_for_output(quantity), loc_name)
                action = {"action_type": "destroy_squadron", "ship_id": enemy.s_id, "squadron": self, "enemy": enemy, "x": enemy.tile[1], "y": enemy.tile[0], "pos_x": enemy_pos_x0, "pos_y": enemy_pos_y0, "quantity": enemy.quantity_str, "text_card": text_card}
                game_screen.actions_list.append(action)
            else:
                text_card = "[color=#%s]%s %s\n-%s %s[/color]" % (loc_damage_type_color, _separator_for_output(int(_my_truncate(damage, 0))), loc_damage, _separator_for_output(quantity), loc_name)
                action = {"action_type": "damage_squadron", "squadron": self, "enemy": enemy, "x": enemy.tile[1], "y": enemy.tile[0], "pos_x": enemy_pos_x0, "pos_y": enemy_pos_y0, "quantity": quantity, "text_card": text_card}
                game_screen.actions_list.append(action)
        #hit = True if random.randint(1, 101) <= self.accuracy else False

class SpaceshipTacticsApp(App):
    def build(self):
        global sm
        global game_screen
        global menu_screen
        global arrangemenu_screen
        my_transition = NoTransition()
        sm = ScreenManager(transition = my_transition)
        game_screen = GameScreen(name = "Game Screen")
        menu_screen = MenuScreen(name = "Menu Screen")
        arrangemenu_screen = ArrangeMenuScreen(name = "Arrange Menu Screen")
        sm.add_widget(menu_screen)
        sm.add_widget(game_screen)
        sm.add_widget(arrangemenu_screen)
        return sm
    def on_stop(self):
        print("Exiting the application")
        pass

if __name__ == "__main__":
    app = SpaceshipTacticsApp()
    print("starting the application")
    app.run()