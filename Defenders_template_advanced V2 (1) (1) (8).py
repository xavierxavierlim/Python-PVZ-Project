import pickle
import random

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }

defender_list = ['ARCHR', 'WALL']
monster_list = ['ZOMBI', 'WWOLF']
attacker_list = ['ARCHR']
alpha_list = ['A','B','C','D','E']
program_checker = None

defenders = {'ARCHR': {'name': 'Archer',
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       },
             
             'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      }
             }

monsters = {'ZOMBI': {'name': 'Zombie',
                      'maxHP': 15,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves' : 1,
                      'reward': 2
                      },

            'WWOLF': {'name': 'Werewolf',
                      'maxHP': 10,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves' : 2,
                      'reward': 3
                      }
            }

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]



fieldhp = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]




#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field():
    print('    1     2     3')
    print(' +-----+-----+-----+-----+-----+-----+-----+')
    for row in range(len(field)): #5
        print(chr(ord('A')+row),end="")
        
        for box in field[row]:
            if box == None:
                print('|{:5}'.format(''),end='')
            else:
                print('|{:5}'.format(box),end='')
                
        print('|')
        print(' ',end='')
        '''
        for boxhp in fieldhp[row]:
            if box == None:
                print('|{:5}'.format(''),end='')
            elif box in defenders:
                print('|{:2}/{:<2}'.format(boxhp, defenders[box]['maxHP']),end='')
            elif box in monsters:
                print('|{:2}/{:<2}'.format(boxhp, monsters[box]['maxHP']),end='')

        '''

        
        for column in range(7):
            box = field[row][column]
            boxhp = fieldhp[row][column]
            if box == None:
                print('|{:5}'.format(''),end='')
            elif box in defenders:
                print('|{:>2}/{:<2}'.format(boxhp, defenders[box]['maxHP']),end='')
            elif box in monsters:
                print('|{:>2}/{:<2}'.format(boxhp, monsters[box]['maxHP']),end='')
    
                    
        print('|')
        print(' +-----+-----+-----+-----+-----+-----+-----+')

            
    return


#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):
    print('Turn  {}     Threat = [{:10}]     Danger Level {}'.format(game_vars['turn'], '-' * game_vars['threat'], game_vars['danger_level']))
    print('Gold =  {}   Monsters killed = {}/{}'.format(game_vars['gold'], game_vars['monsters_killed'], game_vars['monster_kill_target']))
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name):
    # check if the position is valid
    # Valid position: A1, a1, D5
    # Invalid position: ALASJD, 93, A19

    if len(position) == 2 and position[0].upper() in ('A', 'B', 'C', 'D', 'E') and 1 <= int(position[1]) <= 3:
        #get the row and column
        row = ord(position[0].upper()) - ord('A')
        column = int(position[1]) - 1
        
        # place the unit
        # check if it is a defender or not
        #print(unit_name)
        #print(defenders)
        if unit_name in defenders:
            # unit is defender
            #defender_name = unit_name
            if field[row][column] == None:
                field[row][column] = unit_name
                #field[row][column] = defender_name
                fieldhp[row][column] = defenders[unit_name]['maxHP']

                #monster_advance(monster_list, field)
                #defender_attack(defender_list, field)
                #game_vars['turn'] += 1
        
            else:
                return [0, False]

        #draw_field()

        return True

    else:
        print('Invalid position')
        return [0, False]

    


#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, gold):                                    
    # show units that can be purchased
    for index in range(len(defender_list)+1): #3
        if index == 2:
            print("3. Don't buy")
            break
        print('{}. {} ({} gold)'.format(index + 1, defenders[defender_list[index]]['name'], defenders[defender_list[index]]['price']))
        
    while True:
        try:
            choice = int(input('Your choice? '))
            if choice>=1 and choice<=3:
                break
            else:
                print("Please choose an option between 1 and 3")
                continue
        except:
            print("Please choose an option between 1 and 3")
            continue

    
    if choice >= 1 and choice <= len(defender_list): #2
        #print('{},{}'.format(gold, defenders[defender_list[choice-1]]['price']))
        if defenders[defender_list[choice-1]]['price'] <= gold:
             
            while True:
                try:
                    position = input('Place where? ')
                    if (position[0].upper() in alpha_list) and int(position[1]) :
                        break
                    else:
                        print("Please enter a valid position")
                        continue
                except:
                    print("Please enter a valid position")
                    continue

            result = place_unit(field, position, defender_list[choice-1])
            

            # unit placed successfully - deduct the gold used
            if result == True:
                gold -= defenders[defender_list[choice-1]]['price']
                return [gold,True]
            else:
                return [game_vars['gold'], result[1]]
        else:
            print('You cannot afford this unit.')
            return [game_vars['gold'],False]
            
    elif choice == 3:
        print('Cancelled purchase')
        return [game_vars['gold'],None]

    return [gold, True]







#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(defender_list, field):
    numrow = -1
    for row in field:
        index_row = field.index(row)
        numrow += 1 #count no of rows
        rowdmg = 0
        dmg_list = []
        #defenderrow = 0
        for defender in attacker_list:
            if defender in row:#ARCHR #WALL
                #defenderrow += 1
                for num in range(row.count(defender)):
                    dmg = random.randint(defenders[defender]['min_damage'], defenders[defender]['max_damage'])
                    dmg_list.append(dmg)
                    rowdmg += dmg

        y = row.count(monster_list[0])
        x = row.count(monster_list[1])

        for monster in monster_list:
            if monster in row:
                try:
                    
                    for dmg in dmg_list:
                        print("{} in lane {} shoots {} for {} damage!".format(defender,alpha_list[index_row],monsters[monster]['name'],dmg))
                    index_monst = field[index_row].index(monster)
                    fieldhp[index_row][index_monst] -= rowdmg
                    if fieldhp[index_row][index_monst] <= 0:
                        fieldhp[index_row][index_monst] = None
                        field[index_row][index_monst] = None
                        game_vars['gold'] += monsters[monster]['reward']
                        game_vars['monsters_killed'] += 1
                        print("{} dies!".format(monster))
                        print("You have gained {} gold as a reward.".format(monsters[monster]['reward']))
                                    
                    else:
                        
                        continue
                                
                except:
                    print("smth wrong")
                    continue

            elif (y==1) and (x==1): 
                break
            elif (y==2) or (x==2):
                break
                        
                        
                
#defender_attack(defender_list, field)

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(field, monster_list): #row, column
    for row in range(len(field)):
        for box in field[row]:

            if box == 'WWOLF':   
                moves = monsters['WWOLF']['moves']
                index = field[row].index(box)
                if index - moves <= -1 or index - 1 <= -1:
                    return [False, box]
                if field[row][index - 1] in defender_list:
                    dmg = random.randint(monsters[box]['min_damage'], monsters[box]['max_damage'])
                    #defenders[field[row][index - monsters[box]['moves']]]['currentHP'] -= dmg
                    fieldhp[row][index - 1] -= dmg #defender takes damage
                    print("{} in lane {} attacks {} for {} damage!".format(box,alpha_list[row],field[row][index - 1],dmg))
                    if fieldhp[row][index - 1] <= 0: #defender dies
                        print("{} dies!".format(field[row][index - 1]))
                        #hp = fieldhp[row][index]
                        field[row][index - 1] = None
                        #field[row][index] = None

                        fieldhp[row][index - 1] = None
                        #fieldhp[row][index] = None                    
                    break

                elif field[row][index - 2] == None:
                    field[row][index-2] = 'WWOLF'
                    field[row][index] = None
                    fieldhp[row][index-2] = fieldhp[row][index]
                    fieldhp[row][index] = None
                    print("WWOLF Advances in lane {}".format(alpha_list[row]))

                    if field[row][index - 2 - 1] in defender_list: #ZOMBI, WOLF
                        dmg = random.randint(monsters[box]['min_damage'], monsters[box]['max_damage'])
                        #defenders[field[row][index - monsters[box]['moves']]]['currentHP'] -= dmg
                        fieldhp[row][index - 2 - 1] -= dmg #defender takes damage
                        print("{} in lane {} attacks {} for {} damage!".format(box,alpha_list[row],field[row][index - 2 - 1],dmg))
                        
                        if fieldhp[row][index - 2 - 1] <= 0: #defender dies
                            print("{} dies!".format(field[row][index - 2 - 1]))
                            #hp = fieldhp[row][index]
                            field[row][index - 2 - 1] = None
                            #field[row][index] = None
                            fieldhp[row][index - 2 - 1] = None
                            #fieldhp[row][index] = None

                        break
                    else:
                        break

                elif field[row][index - 1] == None:
                    field[row][index-1] = 'WWOLF'
                    field[row][index] = None
                    fieldhp[row][index-1] = fieldhp[row][index]
                    fieldhp[row][index] = None
                    print("{} advances in lane {}".format(box,alpha_list[row]))

                    if field[row][index - 1 - 1] in defender_list: #ZOMBI, WOLF
                        dmg = random.randint(monsters[box]['min_damage'], monsters[box]['max_damage'])
                        #defenders[field[row][index - monsters[box]['moves']]]['currentHP'] -= dmg
                        fieldhp[row][index - 1 - 1] -= dmg #defender takes damage
                        print("{} in lane {} attacks {} for {} damage!".format(box,alpha_list[row],field[row][index - 1 - 1],dmg))
                        if fieldhp[row][index - 1 - 1] <= 0: #defender dies
                            print("{} dies!".format(field[row][index - 1 - 1]))
                            hp = fieldhp[row][index]
                            field[row][index - 1 - 1] = None
                            #field[row][index] = None
                            fieldhp[row][index - 1 - 1] = None
                            #fieldhp[row][index] = None
                        break
                    else:
                        break

                elif field[row][index - 2] == monster_list:
                    field[row][index-1] = 'WWOLF'
                    field[row][index] = None
                    fieldhp[row][index-1] = fieldhp[row][index]
                    fieldhp[row][index] = None
                    print("WWOLF Advances in lane {}".format(alpha_list[row]))
                    continue

                elif field[row][index - 2 - 1] == monster_list:
                    field[row][index-2] = 'WWOLF'
                    field[row][index] = None
                    fieldhp[row][index-2] = fieldhp[row][index]
                    fieldhp[row][index] = None
                    print("WWOLF Advances in lane {}".format(alpha_list[row]))
                    continue
             
            if box == 'ZOMBI':
                
                moves = monsters['ZOMBI']['moves']
                index = field[row].index(box)
                if index - moves <= -1:
                    return [False, box]

                if field[row][index - 1] in defender_list:
                    dmg = random.randint(monsters[box]['min_damage'], monsters[box]['max_damage'])
                    
                    
                    #defenders[field[row][index - monsters[box]['moves']]]['currentHP'] -= dmg

                    fieldhp[row][index - 1] -= dmg #defender takes damage
                    print("{} in Lane {} attacks {} for {} damage!".format(box,alpha_list[row],field[row][index - 1],dmg))
                        
                    if fieldhp[row][index - 1] <= 0:
                        print("{} dies!".format(field[row][index - 1]))
                        #hp = fieldhp[row][index]
                        field[row][index - 1] = None
                        #field[row][index] = None

                        fieldhp[row][index - 1] = None
                        #fieldhp[row][index] = None
                
                if field[row][index - 1] == None:
                    
                    field[row][index - 1] = box
                    field[row][index] = None
                    fieldhp[row][index - 1] = fieldhp[row][index]
                    fieldhp[row][index] = None
                    print("{} advances in Lane {}".format(box,alpha_list[row]))
                
                    if field[row][index - 1 - 1] in defender_list: #ZOMBI, WOLF
                        dmg = random.randint(monsters[box]['min_damage'], monsters[box]['max_damage'])
                        #print("{} advances in Lane {}".format(box,alpha_list[row]))
                        print('{} attacks {} for {} damage!'.format(box, field[row][index - 1 - 1], dmg))
                        
                    
                        #defenders[field[row][index - monsters[box]['moves']]]['currentHP'] -= dmg

                        fieldhp[row][index - 1 - 1] -= dmg #defender takes damage
                        
                        if fieldhp[row][index - 1 -1] <= 0: #if defender dies
                            print("{} dies!".format(field[row][index - 1 - 1]))
                            hp = fieldhp[row][index]
                            field[row][index - 1 - 1] = None
                            #field[row][index] = None

                            fieldhp[row][index - 1 -1] = None
                            #fieldhp[row][index] = None

                elif field[row][index - 1 - 1] in monster_list:
                    continue

                elif field[row][index - 1] in monster_list:
                    continue
                
    '''
    for row in range(len(fieldhp)): #5
        for box in fieldhp[row]:
            # hard code, works
            if box == monsters[monster_list[0]]['currentHP']:
                index = fieldhp[row].index(box)
                
                if fieldhp[row][index-1] == None:
                    fieldhp[row][index-1] = monsters[monster_list[0]]['currentHP']
                    fieldhp[row][index] = None
                if fieldhp[row][index-1] != None:
                    fieldhp[row][index] = fieldhp[row][index]

            # no hard code, doesnt work
            #for monster in monster_list:
                #if box == monsters[monster]['currentHP']:
                    #index = fieldhp[row].index(box)
                    #if fieldhp[row][index - monsters[monster]['moves']] == None:
                        #fieldhp[row][index - monsters[monster]['moves']] = monster_list[monster]['currentHP']
                        #fieldhp[row][index] = None
                        



    '''



#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------

def spawn_monster(field, monster_list):
    monster_checker = True
    for i in range(5):
        for x in field[i]:
            for y in monster_list:
                if x == y:
                    monster_checker = False
                    #print('There is already a monster')
        #if i in field:
            #monster_checker = False
            
    if monster_checker ==True:
        index = random.randint(0, 4)
        random_monster = random.randint(0, 1)
        field[index][6] = monster_list[random_monster]
        #monsters[monster_list[0]]['currentHP'] = monsters[monster_list[0]]['maxHP']
        
        fieldhp[index][6] = monsters[monster_list[random_monster]]['maxHP']

    
        
#spawn_monster(field, monster_list)
#monster_advance(field, monster_list)



#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game():
    file = open("game.txt","wb")
    pickle.dump(game_vars,file)

    pickle.dump(field,file)
    pickle.dump(fieldhp,file)
    file.close()

                            
    print("Game saved.")

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game():
    global field
    global fieldhp
    global game_vars
    file = open("game.txt","rb")
    game_vars = pickle.load(file)
    field = pickle.load(file)
    fieldhp = pickle.load(file)
    return

#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 1
    game_vars['monster_kill_target'] = 5
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 100
    game_vars['threat'] = 0
    game_vars['danger_level'] = 1
    

#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()


# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
while True:
    show_main_menu()
    try:
        choice = int(input('Your choice? '))

        if choice == 1:
            initialize_game()
            break
        elif choice == 2:
            load_game()
            print('2. Load saved game')
            break
        elif choice == 3:
            print("You have Quit this game. Thank you for playing!!")
            program_checker = False
            break
    except:
        print('Do not understand your choice')
        continue

# main game loop
if program_checker != False:
    while True:
        if game_vars['turn'] % 12 == 0:
            game_vars['danger_level'] += 1
            monsters['ZOMBI']['min_damage'] += 1
            monsters['ZOMBI']['max_damage'] += 1
            monsters['ZOMBI']['reward'] += 1
            monsters['ZOMBI']['maxHP'] += 1
            monsters['WWOLF']['min_damage'] += 1
            monsters['WWOLF']['max_damage'] += 1
            monsters['WWOLF']['reward'] += 1
            monsters['WWOLF']['maxHP'] += 1
        
        if game_vars['threat'] >= 10:
            game_vars['threat'] -= 10

            index = random.randint(0, 4)
            random_monster = random.randint(0, 1)
            field[index][6] = monster_list[random_monster]
            #monsters[monster_list[0]]['currentHP'] = monsters[monster_list[0]]['maxHP']
            fieldhp[index][6] = monsters[monster_list[random_monster]]['maxHP']

        spawn_monster(field, monster_list)
        draw_field() # print the field
        #print(fieldhp)
        #print(field)
        show_combat_menu(game_vars) # print the combat menu
        if game_vars['monsters_killed'] >= game_vars['monster_kill_target']:
            print("You have protected this city! You win!")
            break

        while True:
            try:
                choice = int(input('Your choice? '))
                break
            except:
                print('Choose a number between 1 and 4')
                continue



        
        # buy units
        if choice == 1:
            print('Buy Units')
            gold_left = game_vars['gold']
            gold_left = buy_unit(field, game_vars['gold']) # call the buy units function
            if gold_left[1] == None or gold_left[1] == False:
                    continue
            try:
                game_vars['gold'] = gold_left[0]
                #print(game_vars)
                defender_attack(defender_list, field)
                a = monster_advance(field, monster_list)
                game_vars['gold'] += 1
                game_vars['turn'] += 1
                num = random.randint(1, game_vars['danger_level'])
                game_vars['threat'] += num
            except:
                continue
            try:
                if a[0] == False:
                    print('A {} has reached this city. All is lost.\nYou have lost the game!'.format(a[1]))
                    break
            except:
                continue

        elif choice == 2:
            print('End turn')
            defender_attack(defender_list, field)
            a = monster_advance(field,monster_list)       
            game_vars['gold'] += 1
            game_vars['turn'] += 1
            try:
                if a[0] == False:
                    print('A {} has reached this city. All is lost.\nYou have lost the game!'.format(a[1]))
                    break
            except:
                continue

        elif choice == 3:
            save_game()

        elif choice == 4:
            print('Quit game')
            break
        else:
            print('Please enter a valid choice.')
