# coding: utf-8
# -Apocalypse-
# Языки: Русский
# Жанр: Пошаговая стратегия
# Автор Loginus_Logi
# Версия: Alpha 0.9.0.1

from tkinter import *
import random
import time
from time import sleep

Block = False


class LevelMapPos:  # В разработке
    '''Класс генерации карт. (Заранье спланированная расстановка)'''

    def __init__(self, points, enemies, fires, player, exit):
        self.pos_points = points
        self.pos_enemies = enemies
        self.pos_fires = fires
        self.pos_player = player
        self.pos_exit = exit

    def get_points(self):
        return self.pos_points

    def get_enemies(self):
        return self.pos_enemies

    def get_player(self):
        return self.pos_player

    def get_exit(self):
        return self.pos_exit


class BaseCharacter:  # Базовый класс объектов
    """
    Базовый класс для создания объекта.
    Принимает картинку для инициализации.
    Создаёт объект на холсте с картинкой
    """

    def __init__(self, pic):
        global obj_pos
        pos = (random.randint(0, N_X - 1) * step,
               random.randint(0, N_Y - 1) * step)
        while pos in obj_pos:
            pos = (random.randint(0, N_X - 1) * step,
                   random.randint(0, N_Y - 1) * step)
        obj_pos.append(pos)
        self.name = None
        self.obj = canvas.create_image(pos, image=pic, anchor='nw')

    def get_direction(self):
        """Вызов движения"""
        pass


class StraightForwardEnemy(BaseCharacter):  # Пряпоходящий враг
    """
    Враг - "Прямоходящий"
    Тактика - Ходит только в одну сторону игнорируя огонь
    """

    def __init__(self):
        super().__init__(pic.straight_forward)
        self.dir = (random.choice([0, step, -step]), random.choice([0, step, -step]))
        self.name = 'Прямоходящий'

    def get_direction(self):
        global walls_pos
        hard_pos = walls_pos
        hard_pos = [(el[0], el[1]) for el in hard_pos]
        pos_e = canvas.coords(self.obj)
        while not (0 <= pos_e[0] + self.dir[0] <= step * N_X or 0 <= pos_e[1] + self.dir[1] <= step * N_Y) or (
        pos_e[0] + self.dir[0], pos_e[1] + self.dir[1]) in hard_pos:
            self.dir = (random.choice([0, step, -step]), random.choice([0, step, -step]))
        return self.dir


class BadSeeingEnemy(BaseCharacter):  # Плоховидящий враг
    """
    Враг - "Плоховидящий"
    Тактика - Ходит случайным образом
    """

    def __init__(self):
        super().__init__(pic.bad_seeing)
        self.name = 'Половидящий'

    def get_direction(self):
        global fires_pos, walls_pos
        hard_pos = fires_pos + [exit_pos] + walls_pos
        hard_pos = [(el[0], el[1]) for el in hard_pos]
        result = [(0, 0)]
        pos_e = canvas.coords(self.obj)
        if (pos_e[0] + step, pos_e[1]) not in hard_pos and pos_e[0] + step <= step * N_X:
            result.append((step, 0))
        if (pos_e[0], pos_e[1] + step) not in hard_pos and pos_e[1] + step <= step * N_Y:
            result.append((0, step))
        if (pos_e[0] - step, pos_e[1]) not in hard_pos and pos_e[0] - step >= 0:
            result.append((-step, 0))
        if (pos_e[0], pos_e[1] - step) not in hard_pos and pos_e[1] - step >= 0:
            result.append((0, -step))
        return random.choice(result)


class HunterEnemy(BaseCharacter):  # Враг охотник
    """
    Враг - "Охотник"
    Тактика - Ходит на тебя
    """

    def __init__(self):
        super().__init__(pic.hunter)
        self.name = 'Охотник'

    def get_direction(self):
        global fires_pos, walls_pos
        hard_pos = fires_pos + walls_pos + [exit_pos]
        hard_pos = [(el[0], el[1]) for el in hard_pos]
        pos_p = canvas.coords(player.obj)
        pos_e = canvas.coords(self.obj)
        # if abs(pos_p[0] - pos_e[0]) >= abs(pos_p[1] - pos_e[1]):
        #     pass
        # if abs(pos_p[0] - pos_e[0]) <= abs(pos_p[1] - pos_e[1]):
        #     pass
        if pos_p[0] < pos_e[0] and pos_p[1] < pos_e[1]:
            if (pos_e[0] - step, pos_e[1] - step) not in hard_pos:
                return (-step, -step)
            if (pos_e[0] - step, pos_e[1]) not in hard_pos:
                return (-step, 0)
            if (pos_e[0], pos_e[1] - step) not in hard_pos:
                return (0, -step)
            if (pos_e[0] - step, pos_e[1] + step) not in hard_pos:
                return (-step, step)
            if (pos_e[0] + step, pos_e[1] - step) not in hard_pos:
                return (step, -step)
        if pos_p[0] > pos_e[0] and pos_p[1] > pos_e[1]:
            if (pos_e[0] + step, pos_e[1] + step) not in hard_pos:
                return (step, step)
            if (pos_e[0] + step, pos_e[1]) not in hard_pos:
                return (step, 0)
            if (pos_e[0], pos_e[1] + step) not in hard_pos:
                return (0, step)
            if (pos_e[0] - step, pos_e[1] + step) not in hard_pos:
                return (-step, step)
            if (pos_e[0] + step, pos_e[1] - step) not in hard_pos:
                return (step, -step)
        if pos_p[1] < pos_e[1] and pos_p[0] > pos_e[0]:
            if (pos_e[0] + step, pos_e[1] - step) not in hard_pos:
                return (step, -step)
            if (pos_e[0], pos_e[1] - step) not in hard_pos:
                return (0, -step)
            if (pos_e[0] + step, pos_e[1]) not in hard_pos:
                return (step, 0)
            if (pos_e[0] + step, pos_e[1] + step) not in hard_pos:
                return (step, step)
            if (pos_e[0] - step, pos_e[1] - step) not in hard_pos:
                return (-step, -step)
        if pos_p[1] > pos_e[1] and pos_p[0] < pos_e[0]:
            if (pos_e[0] - step, pos_e[1] + step) not in hard_pos:
                return (-step, step)
            if (pos_e[0], pos_e[1] + step) not in hard_pos:
                return (0, step)
            if (pos_e[0] - step, pos_e[1]) not in hard_pos:
                return (-step, 0)
            if (pos_e[0] + step, pos_e[1] + step) not in hard_pos:
                return (step, step)
            if (pos_e[0] - step, pos_e[1] - step) not in hard_pos:
                return (-step, -step)
        if pos_p[0] < pos_e[0]:
            if (pos_e[0] - step, pos_e[1]) not in hard_pos:
                return (-step, 0)
            if (pos_e[0] - step, pos_e[1] + step) not in hard_pos:
                return (-step, step)
            if (pos_e[0] - step, pos_e[1] - step) not in hard_pos:
                return (-step, -step)
            if (pos_e[0], pos_e[1] + step) not in hard_pos:
                return (0, step)
            if (pos_e[0], pos_e[1] - step) not in hard_pos:
                return (0, -step)
        if pos_p[0] > pos_e[0]:
            if (pos_e[0] + step, pos_e[1]) not in hard_pos:
                return (step, 0)
            if (pos_e[0] + step, pos_e[1] + step) not in hard_pos:
                return (step, step)
            if (pos_e[0] + step, pos_e[1] - step) not in hard_pos:
                return (step, -step)
            if (pos_e[0], pos_e[1] + step) not in hard_pos:
                return (0, step)
            if (pos_e[0], pos_e[1] - step) not in hard_pos:
                return (0, -step)
        if pos_p[1] < pos_e[1]:
            if (pos_e[0], pos_e[1] - step) not in hard_pos:
                return (0, -step)
            if (pos_e[0] + step, pos_e[1] - step) not in hard_pos:
                return (step, -step)
            if (pos_e[0] - step, pos_e[1] - step) not in hard_pos:
                return (-step, -step)
            if (pos_e[0] + step, pos_e[1]) not in hard_pos:
                return (step, 0)
            if (pos_e[0] - step, pos_e[1]) not in hard_pos:
                return (-step, 0)
        if pos_p[1] > pos_e[1]:
            if (pos_e[0], pos_e[1] + step) not in hard_pos:
                return (0, step)
            if (pos_e[0] + step, pos_e[1] + step) not in hard_pos:
                return (step, step)
            if (pos_e[0] - step, pos_e[1] + step) not in hard_pos:
                return (-step, step)
            if (pos_e[0] + step, pos_e[1]) not in hard_pos:
                return (step, 0)
            if (pos_e[0] - step, pos_e[1]) not in hard_pos:
                return (-step, 0)
        return BadSeeingEnemy.get_direction(self)


class SecretiveEnemy(BaseCharacter):  # Враг Стелс
    """
    Враг - "Стелс"
    Тактика - Ждёт и атакует на близком растоянии
    """

    def __init__(self):
        super().__init__(pic.secretive)
        self.name = 'Стелс'

    def get_direction(self):
        pos_p = canvas.coords(player.obj)
        pos_e = canvas.coords(self.obj)
        a, b = 0, 0
        if abs(pos_p[0] - pos_e[0]) <= step and abs(pos_p[1] - pos_e[1]) <= step:
            a = pos_p[0] - pos_e[0]
            b = pos_p[1] - pos_e[1]
        return (a, b)


class ImmortalEnemy(BaseCharacter):  # Враг бессмертный

    """
    Враг - "Бессмертный"
    Тактика - Ходит на тебя, игнорируя огонь
    """

    def __init__(self):
        super().__init__(pic.immortal)
        self.name = 'Бессмертный'

    def get_direction(self):
        global walls_pos
        hard_pos = walls_pos
        hard_pos = [(el[0], el[1]) for el in hard_pos]
        pos_p = canvas.coords(player.obj)
        pos_e = canvas.coords(self.obj)
        # if abs(pos_p[0] - pos_e[0]) >= abs(pos_p[1] - pos_e[1]):
        #     pass
        # if abs(pos_p[0] - pos_e[0]) <= abs(pos_p[1] - pos_e[1]):
        #     pass
        if pos_p[0] < pos_e[0] and pos_p[1] < pos_e[1]:
            if (pos_e[0] - step, pos_e[1] - step) not in hard_pos:
                return (-step, -step)
            if (pos_e[0] - step, pos_e[1]) not in hard_pos:
                return (-step, 0)
            if (pos_e[0], pos_e[1] - step) not in hard_pos:
                return (0, -step)
            if (pos_e[0] - step, pos_e[1] + step) not in hard_pos:
                return (-step, step)
            if (pos_e[0] + step, pos_e[1] - step) not in hard_pos:
                return (step, -step)
        if pos_p[0] > pos_e[0] and pos_p[1] > pos_e[1]:
            if (pos_e[0] + step, pos_e[1] + step) not in hard_pos:
                return (step, step)
            if (pos_e[0] + step, pos_e[1]) not in hard_pos:
                return (step, 0)
            if (pos_e[0], pos_e[1] + step) not in hard_pos:
                return (0, step)
            if (pos_e[0] - step, pos_e[1] + step) not in hard_pos:
                return (-step, step)
            if (pos_e[0] + step, pos_e[1] - step) not in hard_pos:
                return (step, -step)
        if pos_p[1] < pos_e[1] and pos_p[0] > pos_e[0]:
            if (pos_e[0] + step, pos_e[1] - step) not in hard_pos:
                return (step, -step)
            if (pos_e[0], pos_e[1] - step) not in hard_pos:
                return (0, -step)
            if (pos_e[0] + step, pos_e[1]) not in hard_pos:
                return (step, 0)
            if (pos_e[0] + step, pos_e[1] + step) not in hard_pos:
                return (step, step)
            if (pos_e[0] - step, pos_e[1] - step) not in hard_pos:
                return (-step, -step)
        if pos_p[1] > pos_e[1] and pos_p[0] < pos_e[0]:
            if (pos_e[0] - step, pos_e[1] + step) not in hard_pos:
                return (-step, step)
            if (pos_e[0], pos_e[1] + step) not in hard_pos:
                return (0, step)
            if (pos_e[0] - step, pos_e[1]) not in hard_pos:
                return (-step, 0)
            if (pos_e[0] + step, pos_e[1] + step) not in hard_pos:
                return (step, step)
            if (pos_e[0] - step, pos_e[1] - step) not in hard_pos:
                return (-step, -step)
        if pos_p[0] < pos_e[0]:
            if (pos_e[0] - step, pos_e[1]) not in hard_pos:
                return (-step, 0)
            if (pos_e[0] - step, pos_e[1] + step) not in hard_pos:
                return (-step, step)
            if (pos_e[0] - step, pos_e[1] - step) not in hard_pos:
                return (-step, -step)
            if (pos_e[0], pos_e[1] + step) not in hard_pos:
                return (0, step)
            if (pos_e[0], pos_e[1] - step) not in hard_pos:
                return (0, -step)
        if pos_p[0] > pos_e[0]:
            if (pos_e[0] + step, pos_e[1]) not in hard_pos:
                return (step, 0)
            if (pos_e[0] + step, pos_e[1] + step) not in hard_pos:
                return (step, step)
            if (pos_e[0] + step, pos_e[1] - step) not in hard_pos:
                return (step, -step)
            if (pos_e[0], pos_e[1] + step) not in hard_pos:
                return (0, step)
            if (pos_e[0], pos_e[1] - step) not in hard_pos:
                return (0, -step)
        if pos_p[1] < pos_e[1]:
            if (pos_e[0], pos_e[1] - step) not in hard_pos:
                return (0, -step)
            if (pos_e[0] + step, pos_e[1] - step) not in hard_pos:
                return (step, -step)
            if (pos_e[0] - step, pos_e[1] - step) not in hard_pos:
                return (-step, -step)
            if (pos_e[0] + step, pos_e[1]) not in hard_pos:
                return (step, 0)
            if (pos_e[0] - step, pos_e[1]) not in hard_pos:
                return (-step, 0)
        if pos_p[1] > pos_e[1]:
            if (pos_e[0], pos_e[1] + step) not in hard_pos:
                return (0, step)
            if (pos_e[0] + step, pos_e[1] + step) not in hard_pos:
                return (step, step)
            if (pos_e[0] - step, pos_e[1] + step) not in hard_pos:
                return (-step, step)
            if (pos_e[0] + step, pos_e[1]) not in hard_pos:
                return (step, 0)
            if (pos_e[0] - step, pos_e[1]) not in hard_pos:
                return (-step, 0)
        return BadSeeingEnemy.get_direction(self)


class MainHero(BaseCharacter):
    """
    Главный персонаж
    Управляется нажатием клавишь из функции key_pressed
    """

    def __init__(self):
        global obj_pos
        super().__init__(pic.player)
        self.name = 'Главный персонаж'
        pos = canvas.coords(self.obj)
        obj_pos += [(pos[0] + step, pos[1]), (pos[0] - step, pos[1]),
                    (pos[0], pos[1] + step), (pos[0], pos[1] - step),
                    (pos[0] + step, pos[1] + step), (pos[0] - step, pos[1] - step),
                    (pos[0] + step, pos[1] - step), (pos[0] - step, pos[1] + step)]


class Fire(BaseCharacter):
    """
    Огонь
    При наступлении на него объектом MainHero игра заканчивается поражением
    """

    def __init__(self):
        global fires_pos
        super().__init__(pic.fire)
        fires_pos.append(canvas.coords(self.obj))


class Point(BaseCharacter):
    """
    Бонус "Замри"
    При наступлении на него объектом класса MainHero враги останавливаются на
    случайное кол-во ходов
    """

    def __init__(self):
        super().__init__(pic.point)
        self.name = 'Бонус "Замри"'


class Exit(BaseCharacter):
    """
    Выход
    При наступлении на него объектом класса MainHero игра заканчивается победой
    """

    def __init__(self):
        global obj_pos
        super().__init__(pic.exit)
        pos = canvas.coords(self.obj)
        obj_pos += [(pos[0] + step, pos[1]), (pos[0] - step, pos[1]),
                    (pos[0], pos[1] + step), (pos[0], pos[1] - step),
                    (pos[0] + step, pos[1] + step), (pos[0] - step, pos[1] - step),
                    (pos[0] + step, pos[1] - step), (pos[0] - step, pos[1] + step)]


class Wall(BaseCharacter):
    """
    Стена
    Не возможно зайти на этот объект любым другим объектом
    """

    def __init__(self):
        global walls_pos
        super().__init__(pic.wall)
        walls_pos.append(canvas.coords(self.obj))


class Decor(BaseCharacter):
    """
    Декорация
    Объекты для красоты мира
    """

    def __init__(self):
        super().__init__(pic.veg)


class Picture:
    """
    ВСе картинки используемые в игре
    """

    def __init__(self):
        self.player = PhotoImage(file="images/doctor1.png")  # Игрок
        self.fire = PhotoImage(file="images/fire_1.1.png")  # Огонь
        self.exit = PhotoImage(file="images/tardis2.png")  # Выход
        self.straight_forward = PhotoImage(file="images/enemy0.png")  # Враг "Никакой"
        self.bad_seeing = PhotoImage(file="images/enemy1.png")  # Враг "Глупый"
        self.hunter = PhotoImage(file="images/enemy2.png")  # Враг "Умный"
        self.secretive = PhotoImage(file="images/enemy3.png")  # Враг "Крыса"
        self.immortal = PhotoImage(file="images/enemy4.2.png")  # Враг "Бессмертный"
        self.point = PhotoImage(file="images/point_1.1.png")  # Бонус
        self.wall = PhotoImage(file="images/wall1.png")  # Стена
        self.veg = PhotoImage(file="images/veg1.png")  # Растительность


def tick():
    """Время в настройках"""
    label_time.after(200, tick)
    label_time['text'] = 'Время ' + time.strftime('%H:%M:%S')


def getV(settings):
    """Меню изменения настроек мира"""
    global N_POINTS, bonus, N_FIRES, N_ENEMIES, N_WALLS
    N_POINTS, bonus, N_FIRES, N_ENEMIES, N_WALLS = levels[str(level_map.get())]


def move_wrap(canvas, obj, move):
    """Движение врага"""
    canvas.move(obj, move[0], move[1])
    if canvas.coords(obj)[1] <= 0:
        canvas.move(obj, 0, step * N_Y)
    if canvas.coords(obj)[1] >= step * N_Y:
        canvas.move(obj, 0, -(step * N_Y))
    if canvas.coords(obj)[0] <= 0:
        canvas.move(obj, step * N_X, 0)
    if canvas.coords(obj)[0] >= step * N_X:
        canvas.move(obj, -(step * N_X), 0)


def do_nothing(event):
    """Завершение игры"""
    if event.keysym == 'Escape':
        close()
    elif event.keysym in {'r', 'R', 'к', 'К'}:
        prepare_and_start()


def check_move():
    """Проверка событий"""
    global bonus, finish
    for p in points:
        if canvas.coords(player.obj) == canvas.coords(p.obj):
            bonus += int(random.randint(2, 5))
            canvas.move(p.obj, step * N_X, step * N_Y)
            points.remove(p)
    if bonus:
        label.config(text=("Бонус \"Замри\" кол-во ходов: {}".format(bonus)))
    if not bonus:
        label.config(text="Найди выход")
    if canvas.coords(player.obj) == canvas.coords(exit.obj):
        label.config(text="Победа!")
        finish = 1
        master.bind("<KeyPress>", do_nothing)
    if not finish:
        for f in fires:
            if canvas.coords(player.obj) == canvas.coords(f.obj):
                label.config(text="Ты проиграл!")
                finish = 2
        for e in enemies:
            if canvas.coords(player.obj) == canvas.coords(e.obj):
                label.config(text="Ты проиграл!")
                finish = 2
    if finish:
        if finish == 1:
            label.config(text="Победа!")
        elif finish == 2:
            label.config(text="Ты проиграл!")
        master.bind("<KeyPress>", do_nothing)


def key_pressed(event):
    """Считование нажатий клавишь и вызов движений у врага и игрока"""
    global bonus, finish
    x, y = canvas.coords(player.obj)
    if event.keysym == 'space':
        move_wrap(canvas, player.obj, (0, 0))
    elif (event.keysym in {'Up', 'w', 'W'} and
          [x, y - step] not in walls_pos and
          (y > 0 or (y == 0 and [x, N_Y * step] not in walls_pos))):
        move_wrap(canvas, player.obj, (0, -step))
    elif (event.keysym in {'Down', 's', 'S'} and
          [x, y + step] not in walls_pos and
          (y < N_Y * step or ([y == N_Y * step] and [x, 0] not in walls_pos))):
        move_wrap(canvas, player.obj, (0, step))
    elif (event.keysym in {'Left', 'a', 'A'} and
          [x - step, y] not in walls_pos and
          (x > 0 or (x == 0 and [N_X * step, y] not in walls_pos))):
        move_wrap(canvas, player.obj, (-step, 0))
    elif (event.keysym in {'Right', 'd', 'D'} and
          [x + step, y] not in walls_pos and
          (x < N_X * step or (x == N_X * step and [0, y] not in walls_pos))):
        move_wrap(canvas, player.obj, (step, 0))
    elif event.keysym == 'Escape':
        return close()
    elif event.keysym in {'r'}:
        return prepare_and_start()
    else:
        return
    check_move()
    if not bonus and not finish:
        for enemy in enemies:
            direction = enemy.get_direction()  # вызвать функцию перемещения у "врага"
            move_wrap(canvas, enemy.obj, direction)  # произвести  перемещение
    if bonus:
        bonus -= 1
    check_move()


def prepare_and_start():
    """Генерация игры (перезапуск)"""
    global exit, player, fires, enemies, points, bonus, finish, fires_pos, exit_pos, obj_pos, walls_pos, exit_pos
    print('\n')
    canvas.delete("all")
    label.config(text="Найди выход")
    finish = False
    bonus = 0
    obj_pos.clear()
    fires_pos.clear()
    walls_pos.clear()

    # Генерация игрока
    player = MainHero()

    # Генерация Выхода
    exit = Exit()
    exit_pos = canvas.coords(exit.obj)

    # Генерация бонусов
    points = [Point() for _ in range(N_POINTS)]

    # Генерация врагов
    enemies = [(random.choice(moves_zombie))() for _ in range(N_ENEMIES)]

    # Генерация огня
    fires = [Fire() for _ in range(N_FIRES)]

    # Генерация Стен
    walls = [Wall() for _ in range(N_WALLS)]

    # Генерация декораций
    # decoration = [BaseCharacter() for _ in range(random.randint(0, N_X * N_Y - len(obj_pos)) - 1)]

    master.bind("<KeyPress>", key_pressed)


def close():
    """Выход из игры"""
    settings.destroy()
    settings.quit()
    master.destroy()
    master.quit()


if __name__ == '__main__' and not Block:
    ##                            Запуск главного окна
    master = Tk()
    master.title('-Apocalypse-')

    ##                                 Картинки
    pic = Picture()
    #################################  Сложности   #############################
    levels = {  # Уровни карты
        '1': (2, 2, 2, 1, 0),
        '2': (2, 2, 3, 4, 0),
        '3': (1, 1, 10, 7, 0),
        '4': (0, 0, 30, 10, 0),
        '5': (0, 0, 50, 15, 0),
        '6': (0, 0, 70, 23, 0),
        '7': (0, 0, 90, 25, 0),
        '8': (0, 0, 110, 30, 0),
        '9': (0, 0, 0, 1, 40)}

    levels_enemy = {  # Уровни зомби
        'Прямоходящий': [StraightForwardEnemy],
        'Плоховидящий': [BadSeeingEnemy],
        'Охотник': [HunterEnemy],
        'Стелс': [SecretiveEnemy],
        'Бессмертный': [ImmortalEnemy],
        'Все виды': [StraightForwardEnemy, BadSeeingEnemy, HunterEnemy,
                     SecretiveEnemy, ImmortalEnemy]
    }

    ##############################   Данные карты   ############################
    step = 68  # Размер клетки
    N_X = 14  # Размер сетки по оси ОХ
    N_Y = 14  # Размер сетки по оси ОУ
    fires_pos, exit_pos, obj_pos, walls_pos = [], None, [], []  # Позиции

    ##                     Названия некоторых внутриигровых переменных
    # N_POINTS Число клеток с бонусом
    # bonus Число ходов бонуса "Замри!" в начале
    # N_FIRES Число клеток, заполненных огнем
    # N_ENEMIES Число врагов
    # N_WALLS Число клеток со стеной

    ##                                 Меню в консоли
    print('\t\t\t\t\t\t\t-Apocalypse-\n')
    a = None
    while a != '1':
        print(
            '\n========================================================================================================================')
        print('"1" Начать игру')
        print('"2" Правила игры')
        print('"3" Управление')
        print('"4" Справка')
        print('"5" Обновления')
        print('"6" Выйти из игры')
        a = input('Действие: ')
        if a == '1':
            break
        elif a == '2':
            print('\nЦель игры: Дойти до дома и не попаться зомби.')
            print('\t\t\tВиды зомби\n')
            print('Прямоходящий - ходит только на право игонорируя огонь')
            print('Глупый       - ходит случайно')
            print('Умный        - ходит на тебя')
            print('Стес         - сидит в засаде и атакует при приближении')
            print('Бессмертный  - ходит на тебя игнорируя огонь')
            print('\nБонус замри - замораживает врагов на случайное кол-во ходов')
        elif a == '3':
            print()
            print(' Up    - Движение вверх')
            print('Down   - Движение вниз')
            print('Left   - Движение на лево')
            print('Right  - Движение на право')
            print('space  - Пропустить ход')
            print('  r    - Перезапустить игру')
            print('Escape - Выйти из игры')
            print('\nРекомендуется поставить язык eng после первой генерации карты')
            print('для задействования всех клавишь (события не реагируют на рус раскладку)')
        elif a == '4':
            print('\nВерсия игры Alpha 0.6\n')
            print('Геймдизайнер, программист - непокоримый и непостижимый Loginus_Logi')
            print('Геймдизайтер, художник    - великий, могучий, ужасный и добрый... снова великий Landrus13!')
            print('Тестировщик               - Fantom')
            print('\nИгра развивается и находится в закрытой Alpha разработке')
        elif a == '5':
            print('\nБыли созданы в коде классы всех возможных объектов, а также добавлена заготовка для "Стен".')
            print('По сути в игру ничего нового не добавилось, только немного переработан код')
        elif a == '6':
            print('\nВы уверены? (y/n)')
            b = input().lower()
            if b == 'y':
                print('\nСпс вам за пользование программой!')
                sleep(3)
                break
            elif b == 'n':
                continue
            print('\nОшибка!')
        else:
            print('\nОшибка!')
    print(
        '========================================================================================================================')

    ##                                Старт меню настроек
    settings = Tk()
    settings.title('Настройки игры')
    settings.geometry('500x200')
    label_time = Label(settings, font='sans 20')
    label_time.pack()
    label_time.after_idle(tick)
    labal_text = Label(settings, text='Уровень генерации карты')
    labal_text.pack()
    level_map = Scale(settings, orient=HORIZONTAL,
                      length=300, from_=1, to=9,
                      tickinterval=1, resolution=1)
    level_map.pack()
    button1 = Button(settings, text="Сохранить")
    button1.pack()
    button1.bind("<Button-1>", getV)

    ##                                     Старт игры
    if a == '1':
        print('Уровни генерации карты:', '; '.join(list(levels.keys())))
        akt = input('\nВведите уровень сложности карты: ')
        while akt not in levels:
            print('\nТакого уровня нет повторите попытку.')
            akt = input('Введите уровень сложности карты: ')
        N_POINTS, bonus, N_FIRES, N_ENEMIES, N_WALLS = levels[akt]
        print('\n---------')
        print('\nВиды зомби:', '; '.join(list(levels_enemy.keys())))
        akt_2 = input('\nВведите вид: ')
        while akt_2 not in levels_enemy:
            print('\nНет такого вида')
            akt_2 = input('\nВведите вид: ')
        moves_zombie = levels_enemy[akt_2]
        label = Label(master, text="Найди выход")
        label.pack()
        canvas = Canvas(master, bg='#175917', height=N_Y * step, width=N_X * step)
        canvas.pack()
        restart = Button(master, text="Начать заново", command=prepare_and_start)
        out = Button(master, text="Выйти", command=close)
        restart.pack()
        out.pack()
        prepare_and_start()
        settings.after(500, settings.mainloop)
        master.mainloop()
