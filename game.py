from time import sleep
from random import randint, choice
import os
import inspect
import ast

health_pot = {'health pot':1}
LINE = '---------------------------------------------'
DEFAULT_INFO = f'level--level1\nhealth--100\nmax_health--100\ndamage--3\nspeed--3\ndodge--0.05\ndifficulty--1\nitems--{health_pot}\ndwaboutit--20698947eaaipsrn4'

# Init and saving files
def save_file():
    print('\nSaving . . . ')
    player_info['health'] = int(player_info['health'])
    player_info['max_health'] = int(player_info['max_health'])
    player_info['damage'] = int(player_info['damage'])
    player_info['speed'] = int(player_info['speed'])
    player_info['dodge'] = float(player_info['dodge'])
    player_info['difficulty'] = int(player_info['difficulty'])
    player_info['dwaboutit'] = dw_formula()
    if os.path.isfile('savefile.txt'):
        os.remove('savefile.txt')
    text = ''
    for i in player_info:
        text = f'{text}{i}--{str(player_info[i])}\n'
    with open('savefile.txt', 'w') as file:
        file.write(text)
        os.system("attrib +h savefile.txt")
    sleep(0.5)
    print('Game saved!\n'+LINE)
    file.write

def start():
    global player_info
    try:
        with open(file='savefile.txt', mode='r') as file:
            filesave = [i.strip() for i in file]
            firsttime = False
    except FileNotFoundError:
        with open('savefile.txt', 'w') as file:
            file.write(DEFAULT_INFO)
            os.system("attrib +h savefile.txt")
        filesave = DEFAULT_INFO.split('\n')
        firsttime = True
    player_info = {}
    for i in filesave:
        _ = i.split('--')
        player_info[_[0]] = _[1]
    player_info['health'] = int(player_info['health'])
    player_info['max_health'] = int(player_info['max_health'])
    player_info['damage'] = int(player_info['damage'])
    player_info['speed'] = int(player_info['speed'])
    player_info['dodge'] = float(player_info['dodge'])
    player_info['difficulty'] = int(player_info['difficulty'])
    player_info['items'] = ast.literal_eval(player_info['items'])
    player_info['dwaboutit'] = str(player_info['dwaboutit'])
    if player_info['dwaboutit'] != dw_formula():
        print('HACKER, STOP TAMPERING WITH FILES')
        sleep(1)
        print('Shutting down PC in..')
        sleep(1)
        print('3')
        sleep(1)
        print('2')
        sleep(1)
        print('1')
        sleep(1)
        # os.system("shutdown /s /t 1")
        exit()
   
    if firsttime:
        level1()
    else:
        restart = False
        print(LINE+ '\nWould you like to continue from previous game? Yes/No')
        answer = input('> ' )
        while True:
            if answer.lower() == 'yes':
                print(LINE+'\nRetrieving save...\n')
                sleep(0.5)
                break
            elif answer.lower() == 'no':
                print( 'Yes if sure')
                answer = input('> ' )
                if answer.lower() == 'yes':
                    print( 'If you say so...\n'+LINE)
                    restart = True
                    break
                else:
                    print('Just like I thought...\n'+LINE)
                    break
            else:
                answer = input( 'Invalid. Try again\n> ' )
        if restart:
            if os.path.isfile('savefile.txt'):
                os.remove('savefile.txt')  
            start()
        else:
            level = player_info['level']
            if level == 'level1':
                level1()
            elif level == 'level2':
                level2()
            elif level == 'level3':
                level3()

    return player_info

def scaling(difficulty):
    # graph from desmos: https://www.desmos.com/calculator/iadsltru6s
    scaling = 1/4*(1.5**difficulty) + 0.75 if difficulty <= 5 else (1/4)*difficulty + 0.75
    return round(scaling, 0)

def healthbar(health, maxhealth):
    amountofbars = health / (maxhealth / 10)
    fullbar = '-' * int(round(amountofbars, 0)) + ' ' * int(round((10 - amountofbars), 0))
    return f'>{fullbar}< {health}/{maxhealth}'

def dw_formula():
    number = (player_info['health']**2 + player_info['damage']*player_info['difficulty'] + player_info['max_health']**2 + player_info['dodge']*200 + player_info['speed']**2)*999 + 696969
    itm = ''
    for i in player_info['items']:
        itm = itm+i[1]+i[2]*2+'ipsrn'+str(player_info['items'][i]**2+3)
    final = f'{int(number)}{itm}'
    # print('Code: '+final)
    return final

# Enemies
class Enemy():
    def __init__(self, multiplier):
        y = len(inspect.getmembers(Enemy, predicate=inspect.isfunction)) - 5
        x = randint(1, y+3)
        self.damage = 3 * multiplier + randint(-1, 1)
        self.health = 10 * multiplier + randint(-2, 2)
        self.speed = 3 * multiplier + (randint(-1, 1)/2)
        self.dodge = 0.05 + (randint(-2, 2)/100)
        if x <= y:
            self.attribute = choice(['attribute'+str(i) for i in range(1, y)])
            eval(compile('self.'+self.attribute+"()", "<strings>", "eval"))
        else:
            self.attribute = None
        self.health = round(self.health, 0)
        self.damage = round(self.damage, 0)
        self.speed = round(self.speed, 1)
        self.dodge = round(self.dodge, 2)
        self.max_health = self.health
        self.stats = {'damage':self.damage, 'health':self.health,'max_health': self.max_health, 'speed':self.speed, 'dodge':self.dodge, 'attribute':self.attribute}

    def __repr__(self):
        return ''.join([f'{i}: {self.stats[i]}, ' for i in self.stats])
    
    # Display system
    def __str__(self):
        difficulty = player_info['difficulty']
        text = [
            f'>>>  Enemy - lvl {difficulty}  <<<',
            f'Health:   {healthbar(self.health, self.max_health)}',
            f'Damage:   {self.damage}',
            f'Speed :   {self.speed}',
            f'Dodge :   {self.dodge}',
        ]
        return '\n'.join(text)

    def update_stats(self):
        self.stats = {'damage':self.damage, 'health':self.health,'max_health': self.max_health, 'speed':self.speed, 'dodge':self.dodge}
    
    def attribute1(self):    # glass cannon attribute
        self.health = self.health / 1.1
        self.damage = self.damage * 1.3

    def attribute2(self):    # tank attribute
        self.health = self.health * 1.5
        self.speed = self.speed / 1.5
        self.dodge = 0
    
    def attribute3(self):    # ninja attribute
        self.health = self.health / 1.2
        self.speed = self.speed * 2
        self.dodge = self.dodge * 2
    
    def attribute4(self):    # strength attribute
        self.speed = self.speed / 1.2
        self.damage = self.damage * 1.3
        self.dodge = self.dodge / 1.2

    def bossify(self):       # makes a boss
        self.health = self.health  * 1.6
        self.damage = self.damage * 1.6

class TutEnemy(Enemy):
    def __init__(self):
        self.damage = 1
        self.health = 5
        self.max_health = self.health
        self.speed = 2
        self.dodge = 0.05 
        self.stats = {'damage':self.damage, 'health':self.health, 'max_health': self.max_health, 'speed':self.speed, 'dodge':self.dodge}

# Commands
def commands_run(command, monsterstats):
    commands = ['battle', 'redo', 'shop', 'stats', 'items']
    if command == commands[0]:
        mstats = commands_battle(monsterstats)
        return mstats
    elif command == commands[1]:
        commands_redo()
        return monsterstats
    elif command == commands[2]:
        commands_shop()
        return monsterstats
    elif command == commands[3]:
        commands_stats()
        return monsterstats
    elif command == commands[4]:
        commands_items()
        return monsterstats
    else:
        print(f'{command} is not a command. Try again')
        command = input('> ')
        commands_run(command, monsterstats)
        return

def commands_battle(monsterstats):
    print(LINE+'\nYou have engaged with the monster!')
    sleep(0.5)
    # print('Speed of you: ', player_info['speed'], ' Speed of monster: ', monsterstats['speed'])
    if player_info['speed'] > monsterstats['speed']:
        rng = randint(1, 100)
        if rng <= monsterstats['dodge']*100:
            print('monster dodged your attack!')
            mremaininghealth = monsterstats['health']
        else:
            mhealth = monsterstats['health']
            mmhealth = monsterstats['max_health']
            mremaininghealth = mhealth - player_info['damage']
            print(f"You damaged monster for {player_info['damage']}")
            print(f'Monster health: {healthbar(mremaininghealth, mmhealth)}')
        if mremaininghealth <= 0:
            if player_info['level'] == 'level2':
                print('You can\' kill it yet, finish the tutorial first')
                monsterstats['health'] = 5
                return monsterstats
            else:
                return 'dead'
        sleep(1.5)
        print("\n")
        rng = randint(1, 100)
        if rng <=player_info['dodge']*100:
            print('You dodged the monsters attack!')
        else:
            pmhealth = player_info['max_health']
            player_info['health'] = player_info['health'] - monsterstats['damage']
            phealth = player_info['health']
            print(f"You were damaged for {monsterstats['damage']}")
            print(f'Your health: {healthbar(phealth, pmhealth)}')
        if player_info['health'] <= 0:
            player_died()
            return
        sleep(1.5)
    else:
        rng = randint(1, 100)
        if rng <=player_info['dodge']*100:
            print('You dodged the monsters attack!')
        else:
            pmhealth = player_info['max_health']
            player_info['health'] = player_info['health'] - monsterstats['damage']
            phealth = player_info['health']
            print(f"You were damaged for {monsterstats['damage']}")
            print(f'Your health: {healthbar(phealth, pmhealth)}')
        if player_info['health'] <= 0:
            player_died()
            return
        sleep(1.5)
        print("\n")
        rng = randint(1, 100)
        if rng <= monsterstats['dodge']*100:
            print('monster dodged your attack!')
            mremaininghealth = monsterstats['health']
        else:
            mhealth = monsterstats['health']
            mmhealth = monsterstats['max_health']
            mremaininghealth = mhealth - player_info['damage']
            print(f"You damaged monster for {player_info['damage']}")
            print(f'Monster health: {healthbar(mremaininghealth, mmhealth)}')
        if mremaininghealth <= 0:
            if player_info['level'] == 'level2':
                print('You can\' kill it yet, finish the tutorial first\n')
                monsterstats['health'] = 5
                return monsterstats
            else:
                return 'dead'
        sleep(1.5)
    monsterstats['health'] = mremaininghealth
    return monsterstats

def commands_redo():
    pass

def commands_shop():
    pass

def commands_stats():
    difficulty = player_info['difficulty']
    health = player_info['health']
    max_health = player_info['max_health']
    damage = player_info['damage']
    speed = player_info['speed']
    dodge = player_info['dodge']
    text = [
        f'>>>  You - difficulty {difficulty} <<<',
        f'Health:   {healthbar(health, max_health)}',
        f'Damage:   {damage}',
        f'Speed :   {speed}',
        f'Dodge :   {dodge}',
    ]
    print('\n'.join(text))

def commands_items():
    print(LINE+"\nHere are your items, type its name to use it:")
    print('\n>ITEMS<')
    for i in player_info['items']:
        print('{}: x{}'.format(i, player_info['items'][i]))
    inpt = input('\nType an items name\n> ')
    if inpt.lower() == 'back':
        print('Leaving menu...\n'+LINE)
        return
    elif inpt.lower() in [i for i in player_info['items']]:
        if inpt.lower() == 'health pot':
            power = player_info['difficulty']*2 if player_info['difficulty'] > 3 else 6
            health_pot(power)
            if player_info['items']['health pot'] > 1:
                player_info['items']['health pot'] = player_info['items']['health pot'] - 1
            else:
                player_info['items'].pop('health pot')
        return
    else:
        print('\nNot an item. Type the item again, or type \'back\' to leave menu.')
        sleep(1)
        commands_items()
        return

def player_died():
    print('You have died lmao')
    sleep(1)
    print('You can do better next time! GLHF again')
    sleep(1)
    print('Thanks for playing')
    sleep(1)
    print('Made by TitanPlayz100\n'+LINE)
    sleep(1)
    print('To skip the tutorial, type \'skip\' at the first prompt, thank me later')
    sleep(2)
    if os.path.isfile('savefile.txt'):
        os.remove('savefile.txt')
    exit()

# Items
def health_pot(power):
    player_info['health'] = player_info['health'] +int(power)
    if player_info['health'] > player_info['max_health']:
        player_info['health'] = player_info['max_health']
    print(f'Your health was restored by {power}')
    print(healthbar(player_info['health'], player_info['max_health']))

# Levels
def level1():
    sleep(1)
    print('Hello there..')
    sleep(1)
    print('Welcome to >>InfiniteShowdown™<< game!' )
    sleep(3)
    print('The objective of the game is to survive through an\n infinitely generated amount of randomised levels...')
    sleep(3)
    print('\nYou will earn coins and items throughout the game,\n but the enemies will scale in strenght as well\nThere is a BOSS level every 5 levels,\n bosses have double health and damage')
    sleep(5)
    print('There wil be a short tutorial, then the game will begin...')
    if 'skip' in input('\nAre you ready? ').lower():
        level3()
        return
    print('Doesn\'t matter, lets go!\n'+LINE)
    sleep(2)
    print('There are several commands you may need to know...')
    sleep(1)
    print('type:\n  redo - soft reset from last savepoint\n  shop - access a large array of items to buy for\n         temporary or permanent buffs\n  battle - continue battle\n  stats - shows your stats')
    sleep(5)
    print('simple commands, really...')
    sleep(1)
    print('STOP READING, a monster is approaching us,\n         -=MENACINGLY=-')
    sleep(1)
    print('I\'ll teach you the mechanics throughout this fight!\n')
    sleep(1)
    level2()
    return

def level2():
    player_info['level'] = 'level2'
    save_file()
    dummy = TutEnemy()
    print(dummy)
    sleep(1.5)
    print('\nHere is your first Enemy!')
    sleep(1)
    print('To battle it, type \'battle\' (casing doesnt matter)')
    inpt = input('> ')
    if 'battle' in inpt.lower():
        print('\nGood job!\nYou get how to play well!\n')
    else:
        print('\nOk, I get it, your a rebel who doesn\'t listen to instructions.')
        sleep(2)
        print('Well, you must know what you\'re doing!')
        sleep(2)
        print('Na, JK')
        print('You probably just mispelt the command or something\nI\'ll give you the benefit of the doubt\nNext time type the command correctly')
        sleep(1.5)
    dummy.stats = commands_run(inpt, dummy.stats)
    sleep(0.5)
    print('\nYou can see your stats by typing \'stats\'')
    inpt = input('> ')
    dummy.stats = commands_run(inpt, dummy.stats)
    sleep(1)
    print('\nNeat, right?\nBut wait, there\'s more!')
    sleep(1)
    print('\nHeres a healing potion, try using it by typing \'items\'')
    inpt = input('> ')
    dummy.stats = commands_run(inpt, dummy.stats)
    print('\nAs well as dropping items, you can buy them\n from the shop, use \'shop\'')
    inpt = input('> ')
    dummy.stats = commands_run(inpt, dummy.stats)
    print('Great job, you have basically mastered everything. \n\nSaving Occurs automatically every level completion\n so you need not worry of that.')
    sleep(3)
    print('\nThe rest of the game is up to you to discover, \ntry to beat as many monsters as you can as well!')
    sleep(1)
    print('GLHF! - Made by TitanPlayz100')
    player_info['difficulty'] = player_info['difficulty'] + 1
    level3()
    return

def level3():
    player_info['level'] = 'level3'
    save_file()
    enemy = Enemy(scaling(player_info['difficulty']))
    print(enemy)
    not_dead = True
    while not_dead:
        inpt = input('> ')
        enemy.stats = commands_run(inpt, enemy.stats)
        if enemy.stats == 'dead':
            not_dead = False
            sleep(1)
            print(f'You have defeated the monster\nGood job')
            sleep(1)
            pmhealth = player_info['max_health']
            player_info['health'] = player_info['health'] + player_info['max_health']*0.5
            phealth = player_info['health']
            if player_info['health'] > player_info['max_health']:
                player_info['health'] = player_info['max_health']
                phealth = player_info['health']
            print(f'Your health: {healthbar(phealth, pmhealth)}')
            print(f'You have been healed for 50%, go get em!\n'+LINE)
            player_info['difficulty'] = player_info['difficulty'] + 1
            sleep(1)
            level3()
            return

# start
start()
