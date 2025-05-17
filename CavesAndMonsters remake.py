from flask import Flask, render_template, redirect, url_for, request
import os
from data import db_session
from data.users import User
from forms.user_registration import RegisterForm, math_test, choice
from forms.user_login import LoginForm
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
db_session.global_init("db/users.sqlite")
db_sess = db_session.create_session()
events = [1]
event_counter = 1


class Player:
    def __init__(self):
        self.hp = 100


player = Player()


class Weapon:
    def __init__(self, weapon_data):
        if weapon_data == 'палка':
            self.damage = 10
            self.chance = 5
            self.weapon_picture = ''
        if weapon_data == 'деревянный меч':
            self.damage = 13
            self.chance = 6
        if weapon_data == 'железный меч':
            self.damage = 15
            self.chance = 7
        if weapon_data == 'двуручный меч из кованной стали':
            self.damage = 30
            self.chance = 4
        if weapon_data == 'кинжал':
            self.damage = 9
            self.chance = 9
        if weapon_data == 'живой меч':
            self.damage = 21
            self.chance = 9


weapon = Weapon('палка')


class Enemy:
    def __init__(self, enemy_type):
        self.en_hp = 0
        self.en_dmg = 0
        if enemy_type == 'скелет':
            self.en_hp = 50
            self.en_dmg = 3
            self.enemy_picture = 'static/img/skeleton_standing.jpg'
        elif enemy_type == 'мимик':
            self.en_hp = 60
            self.en_dmg = 7
            self.enemy_picture = 'static/img/mimic.jpg'
        elif enemy_type == 'бафомета':
            self.en_hp = 100
            self.en_dmg = 10
            self.enemy_picture = 'static/img/bafometa.jpg'


class Fight:
    def __init__(self):
        self.defence_flag = True
        self.attack_flag = False
        self.st_attack_flag = False

    def attack(self):
        self.attack_flag = True
        self.defence_flag = False
        self.st_attack_flag = False

    def defence(self):
        self.attack_flag = False
        self.defence_flag = True

    def strong_attack(self):
        self.st_attack_flag = True
        self.attack_flag = True
        self.defence_flag = False


class Armor:
    def __init__(self, armor_data):
        if armor_data == 'кожаная броня':
            self.armor_hp = 50
            self.armor_b = True
        elif armor_data == 'железная броня':
            self.armor_hp = 100
            self.armor_b = True
        elif armor_data == 'живая броня':
            self.armor_hp = 200
            self.armor_b = True
        else:
            self.armor_hp = 0
            self.armor_b = False


def check_wpn(drop_wpn):
    if drop_wpn == 'деревянный меч':
        return 'static/img/wood_sword.jpg'
    if drop_wpn == 'железный меч':
        return 'static/img/iron_sword.jpg'
    if drop_wpn == 'двуручный меч из кованной стали':
        return 'static/img/big_sword.jpg'
    if drop_wpn == 'кинжал':
        return 'static/img/dagger.jpg'
    if drop_wpn == 'живой меч':
        return 'static/img/living_sword.jpg'


def check_arm(drop_arm):
    if drop_arm == 'кожаная броня':
        return 'static/img/leather_armor.jpg'
    if drop_arm == 'железная броня':
        return 'static/img/iron_armor.jpg'
    if drop_arm == 'живая броня':
        return 'static/img/living_armor.jpg'


armor = Armor('нет брони')
fight = Fight()
loot = ['деревянный меч', 'железный меч', 'двуручный меч из кованной стали', 'кинжал', 'живой меч', 'кожаная броня',
        'железная броня', 'живая броня']


@app.route('/reg', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают.")
        if len(form.password.data) < 8 or '123' in form.password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Ненадежный пароль")
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким логином уже существует.")
        for i in math_test:
            if i == '√529' and choice == 0 and form.submit_age.data != 529 ** 0.5:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Вы неправильно решили математическую задачу.")
            elif i == '9 * (-3)⁻²' and choice == 1 and form.submit_age.data != 9 * (-3 ** -2):
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Вы неправильно решили математическую задачу.")
            elif i == '(-276)⁻³⁵ / (-276)⁻³⁵' and choice == 2 and form.submit_age.data != (-276 ** -35) // (
                    -276 ** -35):
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Вы неправильно решили математическую задачу.")

        user = User(
            login=form.login.data,
            age=form.age.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/log')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/log', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.login == form.username.data).first()
        if user and user.check_password(form.password.data):
            return redirect("/main_menu")
        else:
            return render_template('login.html',
                                   title='Авторизация',
                                   form=form,
                                   message="Неверный логин или пароль",
                                   )
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/CaM_1')
def first_room():
    global armor
    return render_template('room.html', text="Вы - начинающий путешественник, родившийся в небольшом "
                                             "королевстве Вилтрумитов. Вам всего 23 года отроду, а вы уже большой "
                                             "любитель искать себе приключения на одно место. В этот раз вы "
                                             "отправились на поиски загадочной пещеры. Судя по легендам, которые вы "
                                             "слышали в местном трактире, где то в пещере спрятана тонна золота, а "
                                             "также загадочный артефакт, его то вы как раз и ищете...",
                           title='Глава 1: "Загадочный лес"', hp='100', req='first_room_2', decision=False,
                           arm=armor.armor_hp, dmg=weapon.damage, final=False, picture_url='static/img/forest.jpg')


@app.route('/CaM_2')
def first_room_2():
    return render_template('room.html', text="Пройдя дальше по загадочному лесу, вы наткнулись на "
                                             "странную дверь. Похоже это та дверь, которая ведет в нужную вам пещеру. "
                                             "'Легенды не врут' - подумали вы. По вашим ощущениям, вы стояли у двери "
                                             "целый час, не решаясь открыть ее, ведь зайдя в эту пещеру вы станете "
                                             "всемогущим. Вы все таки решились открыть дверь...",
                           title='Глава 1: "Загадочный лес"', hp='100', req='second_room', decision=False,
                           dmg=weapon.damage, arm=armor.armor_hp, picture_url='static/img/cave_door.jpg')


@app.route('/CaM_3')
def second_room():
    return render_template('room.html', text="Зайдя в дверь и пройдя чуть дальше, вы услышали, как "
                                             "дверь закрылась. Вы попытались открыть ее, но у вас ничего не вышло. "
                                             "'О как' - подумали вы. Кажется, в тот момент вы не сильно осознавали, во "
                                             "что влипли, ведь пути назад уже нет, а в руках у вас только палка.",
                           title='Глава 2: "Пещера"', hp='100', req='second_room_2', decision=False,
                           dmg=weapon.damage, arm=armor.armor_hp, picture_url='static/img/cave.jpg')


@app.route('/CaM_4')
def second_room_2():
    return render_template('room.html', text="Пройдя глубже в пещеру, вы наткнулись на какое-то "
                                             "подобие ритуальной комнаты. 'Ничего особенного' - подумали вы, как вдруг "
                                             "вы услышали шаги, с эхом разносящиеся по пещерам...",
                           title='Глава 2: "Пещера"', hp='100', req='skeleton', decision=False,
                           dmg=weapon.damage, arm=armor.armor_hp, picture_url='static/img/cave_2.jpg')


@app.route('/CaM_5')
def skeleton():
    global title
    title = 'Глава 2: "Пещера"'
    return render_template('room.html', text="Через несколько секунд в комнату зашел, как вам "
                                             "показалось, человек в мантии, но когда он подошел ближе, вы поняли, "
                                             "что перед вами сейчас стоит совсем не человек. Вы, мягко говоря, "
                                             "обомлели, немного даже опешили. Намерения неживого гостя вам не были до "
                                             "конца известны, поэтому вам нужно принять решение: сразиться со скелетом "
                                             "или выслушать его.",
                           title='Глава 2: "Пещера"', hp='100', decision=True, but_text1="Сразиться",
                           req1='skeleton_fight', but_text2='Выслушать', req2='skeleton_heard',
                           dmg=weapon.damage, arm=armor.armor_hp, picture_url='static/img/skeleton_standing.jpg')


@app.route('/sk_h')
def skeleton_heard():
    global title, weapon, drop, armor
    title = 'Глава 2: "Пещера"'
    drop = random.choice(loot)
    print(drop)
    if 'кожаная броня' in drop or 'железная броня' in drop or 'живая броня' in drop:
        armor = Armor(drop)
    else:
        weapon = Weapon(drop)
    return render_template('room.html', text="Вы решили все таки поговорить с нечестивым приятелем, и "
                                             "он рассказал как им живется тут в пещерах, а также напомнил, что не все "
                                             f"ее жители так же добры к людям, как и он. Вдобавок он дал вам {drop}",
                           title=title, hp=str(player.hp), decision=False,
                           req='third_room', dmg=str(weapon.damage), arm=str(armor.armor_hp),
                           picture_url='static/img/skeleton_standing.jpg')


@app.route('/sk_fight')
def skeleton_fight():
    global enemy, req
    enemy = Enemy('скелет')
    req = 'third_room'
    return render_template('room.html', text="Вы решили долго не церемониться со стоящим перед вами "
                                             "Костяном и напали на него. Теперь вам предстоит битва...",
                           title=title, hp=str(player.hp), decision=False, fight=True,
                           but_text1="Сразиться", req1='attack', req2='defence', req3='strong_attack',
                           enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg, dmg=weapon.damage, arm=armor.armor_hp,
                           picture_url=enemy.enemy_picture)


@app.route('/at')
def attack():
    global armor
    if fight.attack_flag:
        return render_template('room.html', text="Перед атакой, нужно защититься.",
                               title=title, hp=str(player.hp), decision=False,
                               fight=True, dmg=weapon.damage,
                               but_text1="Сразиться", req1='attack', req2='defence', req3='strong_attack',
                               enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg, arm=armor.armor_hp,
                               picture_url=enemy.enemy_picture)
    else:
        if fight.st_attack_flag:
            fight.attack()
            enemy.en_hp -= weapon.damage * 2
            if enemy.en_hp <= 0:
                fight.defence()
                return render_template('room.html', text=f"Вы победили врага. ",
                                       title=title, hp=str(player.hp), decision=False,
                                       fight=False, req='third_room', dmg=weapon.damage, arm=armor.armor_hp,
                                       picture_url=enemy.enemy_picture)
            return render_template('room.html', text="Вы успешно провели сильную атаку и нанесли "
                                                     f"врагу {weapon.damage * 2} урона",
                                   title=title, hp=str(player.hp), decision=False,
                                   fight=True,
                                   but_text1="Сразиться", req1='attack', req2='defence', req3='strong_attack',
                                   enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg, dmg=weapon.damage, arm=armor.armor_hp,
                                   picture_url=enemy.enemy_picture)
        else:
            fight.attack()
            att = random.randrange(0, 11)
            if att <= weapon.chance:
                enemy.en_hp -= weapon.damage
                if enemy.en_hp <= 0:
                    fight.defence()
                    return render_template('room.html', text=f"Вы победили врага.",
                                           title=title, hp=str(player.hp), decision=False,
                                           fight=False, req=req, dmg=weapon.damage, arm=armor.armor_hp,
                                           picture_url=enemy.enemy_picture)
                return render_template('room.html', text="Вы успешно провели атаку и нанесли врагу "
                                                         f"{weapon.damage} урона",
                                       title=title, hp=str(player.hp), decision=False,
                                       fight=True,
                                       but_text1="Сразиться", req1='attack', req2='defence', req3='strong_attack',
                                       enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg, dmg=weapon.damage,
                                       arm=armor.armor_hp, picture_url=enemy.enemy_picture)
            else:
                if armor.armor_b:
                    armor.armor_hp -= enemy.en_dmg
                    if armor.armor_hp <= 0:
                        armor = Armor('нет брони')
                        armor.armor_b = False
                else:
                    player.hp -= enemy.en_dmg
                    if player.hp <= 0:
                        return render_template('room.html', text="Поздравляю, вы мертвы.",
                                               title='Смерть', hp=str(player.hp), decision=False,
                                               fight=False,
                                               death=True, dmg=weapon.damage, arm=armor.armor_hp,
                                               picture_url='static/img/death.jpg')
                    else:
                        return render_template('room.html', text="Вы не смогли провести атаку, ваше оружие "
                                                                 f"выпало у вас из рук и враг нанес вам {enemy.en_dmg} урона",
                                               title=title, hp=str(player.hp), decision=False,
                                               fight=True,
                                               but_text1="Сразиться", req1='attack', req2='defence',
                                               req3='strong_attack',
                                               enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg, dmg=weapon.damage,
                                               arm=armor.armor_hp, picture_url=enemy.enemy_picture)


@app.route('/df')
def defence():
    global armor
    if fight.defence_flag:
        return render_template('room.html', text="Перед тем как защититься, нужно атаковать.",
                               title=title, hp=str(player.hp), decision=False,
                               fight=True, but_text1="Сразиться", req1='attack', req2='defence', req3='strong_attack',
                               enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg, dmg=weapon.damage,
                               arm=armor.armor_hp, picture_url=enemy.enemy_picture)
    else:
        fight.defence()
        if fight.st_attack_flag:
            fight.attack_flag, fight.st_attack_flag = False, True
        defe = random.randrange(0, 11)
        if defe <= 7:
            return render_template('room.html', text="Вы успешно защитились от атаки врага и не "
                                                     "получили урона",
                                   title=title, hp=str(player.hp), decision=False,
                                   fight=True,
                                   but_text1="Сразиться", req1='attack', req2='defence', req3='strong_attack',
                                   enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg, dmg=weapon.damage,
                                   arm=armor.armor_hp, picture_url=enemy.enemy_picture)
        else:
            if armor.armor_b:
                armor.armor_hp -= enemy.en_dmg
                if armor.armor_hp <= 0:
                    armor = Armor('нет брони')
                    armor.armor_b = False
            else:
                player.hp -= enemy.en_dmg
                if player.hp <= 0:
                    return render_template('room.html', text="Поздравляю, вы мертвы.",
                                           title='Смерть', hp=str(player.hp), decision=False, fight=False,
                                           death=True, arm=armor.armor_hp,
                                           picture_url='static/img/death.jpg')
            return render_template('room.html', text="Вы не смогли защититься от атаки врага и "
                                                     f"получили {enemy.en_dmg} урона",
                                   title=title, hp=str(player.hp),
                                   decision=False, fight=True, but_text1="Сразиться", req1='attack',
                                   req2='defence', req3='strong_attack', enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg,
                                   arm=armor.armor_hp, dmg=weapon.damage, picture_url=enemy.enemy_picture)


@app.route('/r_e')
def random_event():
    global req
    global event_counter
    event = random.choice(events)
    if event_counter == 1:
        req = "fourth_room"
    if event == 1:
        event_counter += 1
        mimic_or_not = random.randrange(0, 4)
        if mimic_or_not >= 3:
            return render_template('room.html', text="Ходя по бесконечным пещерам и подземелиям, вы "
                                                     "наткнулись на сундук. Выглядит он довольно богато, открыть?",
                                   title=title, hp=str(player.hp),
                                   decision=True, fight=False, but_text1='Открыть', but_text2='Не открывать',
                                   req1='mimic_fight', req2=req, dmg=weapon.damage, arm=armor.armor_hp,
                                   picture_url='static/img/chest.jpg')
        else:
            return render_template('room.html', text="Ходя по бесконечным пещерам и подземелиям, вы "
                                                     "наткнулись на сундук. Выглядит он довольно богато, открыть?",
                                   title=title, hp=str(player.hp),
                                   decision=True, fight=False, but_text1='Открыть', but_text2='Не открывать',
                                   req1='add_weapon', req2=req, dmg=weapon.damage, arm=armor.armor_hp,
                                   picture_url='static/img/chest.jpg')


@app.route('/m_fight')
def mimic_fight():
    global enemy
    enemy = Enemy('мимик')
    return render_template('room.html', text="Открыв судук вы поняли, что перед вами находится совсем "
                                             "не сундук...",
                           title=title, hp=str(player.hp), decision=False,
                           fight=True, req1='attack', req2='defence', req3='strong_attack', enemy_hp=enemy.en_hp,
                           enemy_dmg=enemy.en_dmg, dmg=weapon.damage, arm=armor.armor_hp,
                           picture_url='static/img/mimic.jpg')


@app.route('/add_weapon')
def add_weapon():
    global drop
    drop = random.choice(loot)
    if 'меч' in drop or 'кинжал' in drop:
        return render_template('room.html', text=f"Открыв судук вы увидели в нем {drop}, взять?",
                               title=title, hp=str(player.hp), decision=True,
                               but_text1='Взять', but_text2='Не брать', req1='add_wpn', req2=req,
                               arm=armor.armor_hp, fight=False, dmg=weapon.damage, picture_url=check_wpn(drop))
    else:
        return render_template('room.html', text=f"Открыв судук вы увидели в нем {drop}, взять?",
                               title=title, hp=str(player.hp), decision=True,
                               but_text1='Взять', but_text2='Не брать', req1='add_wpn', req2=req,
                               arm=armor.armor_hp, fight=False, dmg=weapon.damage, picture_url=check_arm(drop))


@app.route('/add_wpns')
def add_wpn():
    global weapon, armor, drop
    if 'меч' in drop or 'кинжал' in drop:
        weapon = Weapon(drop)
    else:
        armor = Armor(drop)
        armor.armor_hp = 100
    return render_template('room.html', text=f"Вы подобрали {drop}",
                           title=title, hp=str(player.hp), decision=False,
                           arm=armor.armor_hp, fight=False, req=req, dmg=str(weapon.damage),
                           picture_url=check_arm(drop))


@app.route('/CaM_6')
def third_room():
    global title
    title = 'Глава 3: "Подземелья"'
    return render_template('room.html', text="Пройдя дальше, вы и сами не заметили, как оказались "
                                             "в каких-то подземельях. Они показались вам до жути знакомыми, но "
                                             "вспомнить, где вы их видели, вы так и не смогли...",
                           title=title, hp=str(player.hp), req='random_event',
                           decision=False, fight=False, dmg=weapon.damage, arm=str(armor.armor_hp),
                           picture_url='static/img/dungeon.jpg')


@app.route('/CaM_7')
def fourth_room():
    global title
    title = 'Глава 4: "Глубь подземелий"'
    return render_template('room.html', text="Вы уже сами не до конца понимали, сколько вы находитесь "
                                             "в этой пещере. По ощущениям вы ходите в этой пещере уже несколько лет. "
                                             "Чем дольше вы ищете этот артефакт, тем больше вы теряете себя. Вы "
                                             "нередко задумываетесь, нужно ли было заходить в ту злосчастную дверь. "
                                             "Но какая разница, ведь пути назад все равно нет, да и вы уже не помните, "
                                             "как дошли до сюда.",
                           title=title, hp=str(player.hp), req='fourth_room_2', arm=armor.armor_hp,
                           decision=False, dmg=weapon.damage, fight=False, picture_url='static/img/traveller.jpg')


@app.route('/CaM_8')
def fourth_room_2():
    global drop, req
    drop = random.choice(loot)
    req = 'fifth_room'
    return render_template('room.html', text="Походив так еще неизвестное количество времени, вы "
                                             "почуствовали, как сотрясается земля, а перед собой вы увидели странную "
                                             "дверь. С дверями у вас опыт такой себе, но вы подумали: "
                                             "'попытка не пытка' и все таки зашли в нее. за дверью вы увидели "
                                             "целую толпу скелетов, смотрящих рок концерт. Кажется кто-то потерял "
                                             f"{drop}, взять?",
                           title=title, hp=str(player.hp), req='fifth_room',
                           decision=True, but_text1='Взять', req1='add_wpn', but_text2='Не брать', req2='fifth_room',
                           dmg=weapon.damage, fight=False, arm=armor.armor_hp, picture_url='static/img/concert.jpg')


@app.route('/CaM_9')
def fifth_room():
    return render_template('room.html', text="Спустившись в подобие тронного зала, вы услышали шаги.",
                           title=title, hp=str(player.hp), req='baf_fight',
                           decision=False, dmg=weapon.damage, fight=False, arm=armor.armor_hp,
                           picture_url='static/img/tron.jpg')


@app.route('/f_fight')
def baf_fight():
    global enemy, req
    enemy = Enemy('бафомета')
    req = 'final'
    return render_template('room.html', text="Вам придется сразиться с самим повелителем ада...",
                           title=title, hp=str(player.hp), decision=False,
                           fight=True, req1='attack', req2='defence', req3='strong_attack', enemy_hp=enemy.en_hp,
                           enemy_dmg=enemy.en_dmg, dmg=weapon.damage, arm=armor.armor_hp,
                           picture_url='static/img/bafometa.jpg')


@app.route('/CaM_10')
def final():
    return render_template('room.html', text="Вы победили, правда было уже слишком поздно...",
                           title=title, hp=str(player.hp), req='baf_fight',
                           decision=False, dmg=weapon.damage, fight=False, arm=armor.armor_hp, final=True,
                           picture_url='static/img/kingdom.jpg')


@app.route('/sa')
def strong_attack():
    if fight.attack_flag and fight.st_attack_flag:
        return render_template('room.html', text="Перед атакой, нужно защититься.",
                               title=title, hp=str(player.hp), decision=False,
                               fight=True, dmg=weapon.damage,
                               but_text1="Сразиться", req1='attack', req2='defence', req3='strong_attack',
                               enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg, arm=armor.armor_hp,
                               picture_url=enemy.enemy_picture)
    elif fight.st_attack_flag:
        return render_template('room.html', text="Вы уже приготовили сильную атаку, осталось только "
                                                 "атаковать...",
                               title=title, hp=str(player.hp), decision=False,
                               fight=True, dmg=weapon.damage,
                               but_text1="Сразиться", req1='attack', req2='defence', req3='strong_attack',
                               enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg, arm=armor.armor_hp,
                               picture_url=enemy.enemy_picture)
    else:
        fight.strong_attack()
        return render_template('room.html', text=f"Вы приготовили сильную атаку, защищайтесь...",
                               title=title, hp=str(player.hp), decision=False, arm=armor.armor_hp,
                               fight=True, dmg=weapon.damage,
                               but_text1="Сразиться", req1='attack', req2='defence', req3='strong_attack',
                               enemy_hp=enemy.en_hp, enemy_dmg=enemy.en_dmg,
                               picture_url=enemy.enemy_picture)





@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')


@app.route('/')
def ret():
    return render_template('first.html')


@app.route('/reg')
def redirect_reg():
    return redirect(url_for('register'))


@app.route('/log')
def redirect_log():
    return redirect(url_for('login'))


@app.route('/action', methods=['POST'])
def playCaM():
    data = request.json
    if data['button'] == 'b3':
        os.system('CavesAndMonsters.exe')
        return ''
    else:
        return ''


if __name__ == '__main__':
    app.run('127.0.0.1', 8080, debug=True)
