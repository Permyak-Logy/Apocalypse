# coding: utf-8
# -Apocalypse-
# Языки: Русский
# Жанр: Пошаговая стратегия
# Автор Loginus_Logi
# Версия: Alpha 0.8.2

from tkinter import *
import random
import time
from time import sleep

class LevelMapPos:
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

class Tactics:
    """Тактики врагов"""
    def move_right(enemy):
        """Тактика - движение врогов только вправо"""
        return step, 0
    
    def random_move(enemy):
        """Тактика - движение random"""
        global fires_pos
        result = [(0, 0)]
        pos_e = canvas.coords(enemy)
        if (pos_e[0] + step, pos_e[1]) not in fires_pos + [exit_pos] and pos_e[0] + step <= step * N_X:
            result.append((step, 0))
        if (pos_e[0], pos_e[1] + step) not in fires_pos + [exit_pos] and pos_e[1] + step <= step * N_Y:
            result.append((0, step))
        if (pos_e[0] - step, pos_e[1]) not in fires_pos + [exit_pos] and pos_e[0] - step >= 0:
            result.append((-step, 0))  
        if (pos_e[0], pos_e[1] - step) not in fires_pos + [exit_pos] and pos_e[1] - step >= 0:
            result.append((0, -step))
        return random.choice(result)
    
    def smart_move(enemy):
        """Тактика - движения врагов на тебя"""
        global fires_pos
        pos_p = canvas.coords(player)
        pos_e = canvas.coords(enemy)
        if abs(pos_p[0] - pos_e[0]) >= abs(pos_p[1] - pos_e[1]):
            pass
        if abs(pos_p[0] - pos_e[0]) <= abs(pos_p[1] - pos_e[1]):
            pass
        if pos_p[0] < pos_e[0] and pos_p[1] < pos_e[1]:
            if (pos_e[0] - step, pos_e[1] - step) not in fires_pos:
                return (-step, -step)
            if (pos_e[0] - step, pos_e[1]) not in fires_pos:
                return (-step, 0)
            if (pos_e[0], pos_e[1] - step) not in fires_pos:
                return (0, -step)
            if (pos_e[0] - step, pos_e[1] + step) not in fires_pos:
                return (-step, step)
            if (pos_e[0] + step, pos_e[1] - step) not in fires_pos:
                return (step, -step)
        if pos_p[0] > pos_e[0] and pos_p[1] > pos_e[1]:
            if (pos_e[0] + step, pos_e[1] + step) not in fires_pos:
                return (step, step)
            if (pos_e[0] + step, pos_e[1]) not in fires_pos:
                return (step, 0)
            if (pos_e[0], pos_e[1] + step) not in fires_pos:
                return (0, step)
            if (pos_e[0] - step, pos_e[1] + step) not in fires_pos:
                return (-step, step)
            if (pos_e[0] + step, pos_e[1] - step) not in fires_pos:
                return (step, -step)            
        if pos_p[1] < pos_e[1] and pos_p[0] > pos_e[0]:
            if (pos_e[0] + step, pos_e[1] - step) not in fires_pos:
                return (step, -step)
            if (pos_e[0], pos_e[1] - step) not in fires_pos:
                return (0, -step)
            if (pos_e[0] + step, pos_e[1]) not in fires_pos:
                return (step, 0)
            if (pos_e[0] + step, pos_e[1] + step) not in fires_pos:
                return (step, step)
            if (pos_e[0] - step, pos_e[1] - step) not in fires_pos:
                return (-step, -step)
        if pos_p[1] > pos_e[1] and pos_p[0] < pos_e[0]:
            if (pos_e[0] - step, pos_e[1] + step) not in fires_pos:
                return (-step, step)
            if (pos_e[0], pos_e[1] + step) not in fires_pos:
                return (0, step)
            if (pos_e[0] - step, pos_e[1]) not in fires_pos:
                return (-step, 0)
            if (pos_e[0] + step, pos_e[1] + step) not in fires_pos:
                return (step, step)
            if (pos_e[0] - step, pos_e[1] - step) not in fires_pos:
                return (-step, -step)            
        if pos_p[0] < pos_e[0]:
            if (pos_e[0] - step, pos_e[1]) not in fires_pos:
                return (-step, 0)
            if (pos_e[0] - step, pos_e[1] + step) not in fires_pos:
                return (-step, step)
            if (pos_e[0] - step, pos_e[1] - step) not in fires_pos:
                return (-step, -step)
            if (pos_e[0], pos_e[1] + step) not in fires_pos:
                return (0, step)
            if (pos_e[0], pos_e[1] - step) not in fires_pos:
                return (0, -step)
        if pos_p[0] > pos_e[0]:
            if (pos_e[0] + step, pos_e[1]) not in fires_pos:
                return (step, 0)
            if (pos_e[0] + step, pos_e[1] + step) not in fires_pos:
                return (step, step)
            if (pos_e[0] + step, pos_e[1] - step) not in fires_pos:
                return (step, -step)
            if (pos_e[0], pos_e[1] + step) not in fires_pos:
                return (0, step)
            if (pos_e[0], pos_e[1] - step) not in fires_pos:
                return (0, -step)            
        if pos_p[1] < pos_e[1]:
            if (pos_e[0], pos_e[1] - step) not in fires_pos:
                return (0, -step)
            if (pos_e[0] + step, pos_e[1] - step) not in fires_pos:
                return (step, -step)
            if (pos_e[0] - step, pos_e[1] - step) not in fires_pos:
                return (-step, -step)
            if (pos_e[0] + step, pos_e[1]) not in fires_pos:
                return (step, 0)
            if (pos_e[0] - step, pos_e[1]) not in fires_pos:
                return (-step, 0)            
        if pos_p[1] > pos_e[1]:
            if (pos_e[0], pos_e[1] + step) not in fires_pos:
                return (0, step)
            if (pos_e[0] + step, pos_e[1] + step) not in fires_pos:
                return (step, step)
            if (pos_e[0] - step, pos_e[1] + step) not in fires_pos:
                return (-step, step)
            if (pos_e[0] + step, pos_e[1]) not in fires_pos:
                return (step, 0)
            if (pos_e[0] - step, pos_e[1]) not in fires_pos:
                return (-step, 0)
        return Tactics.random_move(enemy)
    
    def immortal_move(enemy):
        """Тактика движения врагов на тебя игнорируя огонь"""
        pos_p = canvas.coords(player)
        pos_e = canvas.coords(enemy)
        if pos_p[0] < pos_e[0] and pos_p[1] < pos_e[1]:
            return (-step, -step)
        elif pos_p[0] > pos_e[0] and pos_p[1] > pos_e[1]:
            return (step, step)
        elif pos_p[1] < pos_e[1] and pos_p[0] > pos_e[0]:
            return (step, -step)
        elif pos_p[1] > pos_e[1] and pos_p[0] < pos_e[0]:
            return (-step, step)
        elif pos_p[0] < pos_e[0]:
            return (-step, 0)
        elif pos_p[0] > pos_e[0]:
            return (step, 0)
        elif pos_p[1] < pos_e[0]:
            return (0, -step)
        elif pos_p[1] > pos_e[1]:
            return (0, step)
        return (step, 0)
    
    def stealth_move(enemy):
        """Тактика засады"""
        pos_p = canvas.coords(player)
        pos_e = canvas.coords(enemy)
        a, b = 0, 0
        if abs(pos_p[0] - pos_e[0]) <= step and abs(pos_p[1] - pos_e[1]) <= step:
            a = pos_p[0] - pos_e[0]
            b = pos_p[1] - pos_e[1]
        return (a, b)

class Enemy:
    def __init__(self, taktic, pic):
        self.taktic = taktic
        self.pic = pic
    
    def get_data(self):
        return self.taktic, self.pic


def tick():
    """Время в настройках"""
    label_time.after(200, tick)
    label_time['text'] = 'Время ' + time.strftime('%H:%M:%S')


def getV(settings):
    """Изменение настроек мира"""
    global N_POINTS, bonus, N_FIRES, N_ENEMIES
    N_POINTS, bonus, N_FIRES, N_ENEMIES = levels[str(level_map.get())]


def move_wrap(canvas, obj, move, it=None):
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
        if canvas.coords(player) == canvas.coords(p):
            bonus += int(random.randint(2, 5))
            canvas.move(p, step * N_X, step * N_Y)
            points.remove(p)
    if bonus:
        label.config(text=("Бонус \"Замри\" кол-во ходов:", (bonus)))
    if not bonus:
        label.config(text="Найди выход")
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        finish = True
        master.bind("<KeyPress>", do_nothing)
    if not finish:
        for f in fires:
            if canvas.coords(player) == canvas.coords(f):
                label.config(text="Ты проиграл!")
                finish = True
                master.bind("<KeyPress>", do_nothing)
        for e in enemies:
            if canvas.coords(player) == canvas.coords(e[0]):
                label.config(text="Ты проиграл!")
                finish = True
    if finish:
        master.bind("<KeyPress>", do_nothing)


def key_pressed(event):
    """Считование нажатий клавишь и вызов движений у врага"""
    global bonus, finish
    if event.keysym == 'space':
        move_wrap(canvas, player, (0, 0))
    elif event.keysym in {'Up', 'w', 'W'}:
        move_wrap(canvas, player, (0, -step))
    elif event.keysym in {'Down', 's', 'S'}:
        move_wrap(canvas, player, (0, step))
    elif event.keysym in {'Left', 'a', 'A'}:
        move_wrap(canvas, player, (-step, 0))
    elif event.keysym in {'Right', 'd', 'D'}:
        move_wrap(canvas, player, (step, 0))
    elif event.keysym == 'Escape':
        return close()
    elif event.keysym in {'r'}:
        return prepare_and_start()
    else:
        return
    check_move()
    if not bonus and not finish:
        for enemy in enemies:
            direction = enemy[1](enemy[0]) # вызвать функцию перемещения у "врага"
            move_wrap(canvas, enemy[0], direction, it=enemy[1]) # произвести  перемещение
    if bonus:
        bonus -= 1
    check_move()


def prepare_and_start():
    """Генерация игры (перезапуск)"""
    global player, exit, fires, enemies, points, bonus, finish, fires_pos, exit_pos
    canvas.delete("all")
    # canvas2 = canvas.create_image((0, 0), image=canvas_pic, anchor='nw')
    finish = False
    label.config(text="Найди выход")
    obj_pos = []
    fires_pos = []
    # Генерация игрока
    player_pos = (random.randint(0, N_X - 1) * step, 
                  random.randint(0, N_Y - 1) * step)
    obj_pos += [(player_pos[0] + step, player_pos[1]),
                (player_pos[0] - step, player_pos[1]),
                (player_pos[0], player_pos[1] + step),
                (player_pos[0], player_pos[1] - step),
                (player_pos[0] + step, player_pos[1] + step),
                (player_pos[0] - step, player_pos[1] - step),
                (player_pos[0] + step, player_pos[1] - step),
                (player_pos[0] - step, player_pos[1] + step), exit_pos]    
    obj_pos.append(player_pos)
    player = canvas.create_image(
        (player_pos[0],player_pos[1]), image=player_pic, anchor='nw')
    # Генерация Выхода
    exit_pos = (random.randint(0, N_X - 1) * step, 
                random.randint(0, N_Y - 1) * step)
    while exit_pos in obj_pos:
        exit_pos = (random.randint(0, N_X - 1) * step, 
                    random.randint(0, N_Y - 1) * step)
    obj_pos += [(exit_pos[0] + step, exit_pos[1]),
                (exit_pos[0] - step, exit_pos[1]),
                (exit_pos[0], exit_pos[1] + step),
                (exit_pos[0], exit_pos[1] - step),
                (exit_pos[0] + step, exit_pos[1] + step),
                (exit_pos[0] - step, exit_pos[1] - step),
                (exit_pos[0] + step, exit_pos[1] - step),
                (exit_pos[0] - step, exit_pos[1] + step), exit_pos]
    exit = canvas.create_image(
        (exit_pos[0],exit_pos[1]), image=exit_pic, anchor='nw')
    # Генерация бонусов
    points = []
    for i in range(N_POINTS):
        point_pos = (random.randint(0, N_X - 1) * step, 
                     random.randint(0, N_Y - 1) * step)
        while point_pos in obj_pos:
            point_pos = (random.randint(0, N_X - 1) * step, 
                         random.randint(0, N_Y - 1) * step)
        obj_pos.append(point_pos)
        point = canvas.create_image(
            (point_pos[0],point_pos[1]), image=point_pic, anchor='nw')
        points.append(point)
    # Генерация врагов
    enemies = []
    for i in range(N_ENEMIES):
        enemy_pos = (random.randint(0, N_X - 1) * step, 
                     random.randint(0, N_Y - 1) * step)
        while enemy_pos in obj_pos:
            enemy_pos = (random.randint(0, N_X - 1) * step, 
                         random.randint(0, N_Y - 1) * step)
        obj_pos.append(enemy_pos)
        lev, pic = random.choice(moves_zombie)
        enemy = canvas.create_image(
            (enemy_pos[0],enemy_pos[1]), image=pic, anchor='nw')
        enemies.append((enemy, lev))
    # Генерация огня
    fires = []
    for i in range(N_FIRES):
        fire_pos = (random.randint(0, N_X - 1) * step,
                    random.randint(0, N_Y - 1) * step)
        while fire_pos in obj_pos or fire_pos in fires_pos:
            fire_pos = (random.randint(0, N_X - 1) * step,
                        random.randint(0, N_Y - 1) * step)
        fires_pos.append(fire_pos)
        fire = canvas.create_image(
            (fire_pos[0],fire_pos[1]), image=fire_pic, anchor='nw')
        fires.append(fire)
    master.bind("<KeyPress>", key_pressed)


def close():
    """Выход из игры"""
    settings.destroy()
    settings.quit()
    master.destroy()
    master.quit()
    


##                            Запуск главного окна
master = Tk()
master.title('-Apocalypse-')


################################   Картинки   ##################################
player_pic = PhotoImage(file="images/doctor.png") # Игрок
fire_pic = PhotoImage(file="images/fire_1.1.png") # Огонь
exit_pic = PhotoImage(file="images/tardis2.png") # Выход
enemy0_pic = PhotoImage(file="images/enemy0.png") # Враг "Никакой"
enemy1_pic = PhotoImage(file="images/enemy1.png") # Враг "Глупый"
enemy2_pic = PhotoImage(file="images/enemy2.png") # Враг "Умный"
enemy3_pic = PhotoImage(file="images/enemy3.png") # Враг "Крыса"
enemy4_pic = PhotoImage(file="images/enemy4.2.png") # Враг "Бессмертный"
point_pic = PhotoImage(file="images/point_1.1.png") # Бонус


#################################   Сложности   ################################
levels = { # Уровни сложностей
    '1': (2, 2, 2, 1),
    '2': (2, 2, 3, 4),
    '3': (1, 1, 10, 7),
    '4': (0, 0, 30, 10),
    '5': (0, 0, 50, 15),
    '6': (0, 0, 70, 23),
    '7': (0, 0, 90, 25),
    '8': (0, 0, 110, 30),
    '9':  (4, 0, 30, 1)}



levels_enemy = { # Уровни зомби
    'Прямоходящий': [(Tactics.move_right, enemy0_pic)],
    'Глупые': [(Tactics.random_move, enemy1_pic)],
    'Умные': [(Tactics.smart_move, enemy2_pic)],
    'Стелс': [(Tactics.stealth_move, enemy3_pic)],
    'Бессмертные': [(Tactics.immortal_move, enemy4_pic)],
    'Все виды': [(Tactics.move_right, enemy0_pic),
            (Tactics.random_move, enemy1_pic),
            (Tactics.smart_move, enemy2_pic),
            (Tactics.stealth_move, enemy3_pic),
            (Tactics.immortal_move, enemy4_pic)]}


############################   Данные карты   ##################################
step = 68  # Размер клетки
N_X = 16   # Размер сетки по оси ОХ
N_Y = 10   # Размер сетки по оси ОУ
fires_pos, exit_pos = None, None # Позиции

###########################################
# N_POINTS Число клеток с бонусом
# bonus Число ходов бонуса "Замри!" в начале
# N_FIRES Число клеток, заполненных огнем
# N_ENEMIES Число врагов
###########################################

##                                 Меню в консоли
print('\t\t\t\t\t\t\t-Apocalypse-\n')
a = None
while a != '1':
    print('\n========================================================================================================================')
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
        print('\nУлучшена тактика движения умных врагов (они теперь будут немного паться обходить огонь).')
        print('Переработана механика создания врагов и добавлена заготовка для запланированных уровней')
    elif a ==  '6':
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
print('========================================================================================================================')


##                                  Старт меню настроек
settings = Tk()
settings.title('Настройки игры')
settings.geometry('500x200')
label_time = Label(settings, font='sans 20')
label_time.pack()
label_time.after_idle(tick)
labal_text = Label(settings, text='Уровень генерации карты')
labal_text.pack()
level_map = Scale(settings, orient=HORIZONTAL,
                  length=300, from_=1 ,to=9 ,
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
    N_POINTS, bonus, N_FIRES, N_ENEMIES = levels[akt]
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