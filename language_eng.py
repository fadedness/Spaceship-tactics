# -*- coding: utf-8 -*-

list_of_strings = [ "Singleplayer game",
                    "Add ships",
                    "Remove ships",
                    "Finish preparing",
                    "Exit",
                    "Points left",
                    ["laser", "laser", "laser", "laser", "laser", "laser"],
                    ["kinetic", "kinetic", "kinetic", "kinetic", "kinetic", "kinetic"],
                    ["plasma", "plasma", "plasma", "plasma", "plasma", "plasma"],
                    ["rocket", "rocket", "rocket", "rocket", "rocket", "rocket"],
                    ["rail", "rail", "rail", "rail", "rail", "rail"],
                    "against",
                    ["damage", "damage", "damage", "damage", "damage", "damage"],
                    ["defense", "defense", "defense", "defense", "defense", "defense"],
                    "weapon range",
                    "speed",
                    "movement range",
                    "accuracy",
                    "from",
                    "price",
                    "Light Fighter",
                    "Heavy Fighter",
                    "Frigate",
                    "Cruiser",
                    "dreadnought",
                    "Hot seat game",
                    "Network game",
                    "Player",
                    "Move and shoot",
                    "Move or shoot",
                    "Min",
                    "Max",
                    "destroyed",
                    "Give up",
                    "Animation\nSpeed",]

filename = "english_locale.txt"

class TextStrings():
    def __init__(self, a):
        self.singleplayer_game = a[0]
        self.add_ships = a[1]
        self.remove_ships = a[2]
        self.finish_preparing = a[3]
        self.exit_game = a[4]
        self.points_left = a[5]
        self.laser_damage_type = a[6]
        self.kinetic_damage_type = a[7]
        self.plasma_damage_type = a[8]
        self.rocket_damage_type = a[9]
        self.rail_damage_type = a[10]
        self.against = a[11]
        self.damage = a[12]
        self.defense = a[13]
        self.weapon_range = a[14]
        self.speed = a[15]
        self.movement_range = a[16]
        self.accuracy = a[17]
        self.from_ = a[18]
        self.price = a[19]
        self.light_fighter = a[20]
        self.heavy_fighter = a[21]
        self.frigate = a[22]
        self.cruiser = a[23]
        self.dreadnought = a[24]
        self.hot_seat_game = a[25]
        self.network_game = a[26]
        self.player = a[27]
        self.move_and_shoot_true = a[28]
        self.move_and_shoot_false = a[29]
        self.loc_min = a[30]
        self.loc_max = a[31]
        self.destroyed = a[32]
        self.give_up = a[33]
        self.animation_speed = a[34]

def load_file():
    with open(filename, "r") as f:
        a = f.readlines()
    f.close()
    for i in range(len(a)):
        a[i] = a[i].replace("\n", "")
    print(a)
    return a

def get_instance_of_class():
    #a = load_file()
    a = list_of_strings
    b = TextStrings(a)
    return b

text_strings = get_instance_of_class()