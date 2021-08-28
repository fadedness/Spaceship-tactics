# -*- coding: utf-8 -*-

list_of_strings = [ "Одиночная игра",
                    "Добавить корабли",
                    "Убрать корабли",
                    "Закончить приготовления",
                    "Выход",
                    "Очков осталось",
                    ["лазерный", "лазерного", "лазерному", "лазерный", "лазерным", "лазерном"],
                    ["кинетический", "кинетического", "кинетическому", "кинетический", "кинетическим", "кинетическом"],
                    ["плазменный", "плазменного", "плазменному", "плазменный", "плазменным", "плазменном"],
                    ["ракетный", "ракетного", "ракетному", "ракетный", "ракетным", "ракетном"],
                    ["рельсовый", "рельсового", "рельсовому", "рельсовый", "рельсовым", "рельсовом"],
                    "против",
                    ["урон", "урона", "урону", "урон", "уроном", "уроне"],
                    ["защита", "защиты", "защите", "защиту", "защитой", "защите"],
                    "дальность орудий",
                    "скорость",
                    "дальность передвижения",
                    "меткость",
                    "от",
                    "стоимость",
                    "Лёгкий истребитель",
                    "Тяжёлый истребитель",
                    "Фригат",
                    "Крейсер",
                    "Дредноут",
                    "Hot seat режим",
                    "Сетевая игра",
                    "Игрок",
                    "Движение и атака",
                    "Движение или атака",
                    "Мин",
                    "Макс",
                    "уничтожено",
                    "Сдаться",
                    "Скорость\nанимации",]

filename = "russian_locale.txt"

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