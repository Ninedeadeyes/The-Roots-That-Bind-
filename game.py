import os
import time
import random
import winsound

winsound.PlaySound(".\\music\\Roots.wav",  winsound.SND_ALIAS | winsound.SND_ASYNC +winsound.SND_LOOP)
os.system("mode con cols=80 lines=35")

walls = 35
thorns = 55
level = 1
health_object = 6

class Stats:
    def __init__(self,walls,thorns,level,health_object):
      self.walls = walls
      self.thorns = thorns
      self.level =level
      self.health_object=health_object

class Player:
  def __init__(self, x, y):
      self.x = x
      self.y = y
      self.health = 50
  
  def move(self, dx, dy, grid):
      new_x = self.x + dx
      new_y = self.y + dy
      if grid[new_y][new_x] != '#':
          
          if isinstance(grid[new_y][new_x], HealthObject):
              found=random.choice(["whisky","dried meat","herbs"])
              print("You find some, "+found+". It should provide some comfort")
              
              if self.health<251:
                  self.health += grid[new_y][new_x].value
                  print(f"You gained {grid[new_y][new_x].value} health.")
                  print("         ")
                  
              else:
                print("Your body is healthy but you enjoy the refreshment anyway")
                print("You gain 15 health.")
                self.health+=15
              
              grid[new_y][new_x] = '.'

          elif isinstance(grid[new_y][new_x], Thorns):
              print("You tear away the thorns with your hands (It hurts..)")
              damage= random.randint(20,35)
              self.health -=damage
              print(f"You lose "+str(damage)+" health!")
              print("         ")
              
              if self.health <= 0:
                  print("Wounds upon wounds you fall to the consuming darkness. ( Game over ) " )
                  winsound.PlaySound(".\\music\\rip.wav",  winsound.SND_ALIAS | winsound.SND_ASYNC)
                  time.sleep(7)
                  quit()
              grid[new_y][new_x] = '.'
              
          else:
            grid[self.y][self.x] = '.'
            self.x = new_x
            self.y = new_y
            # Random event that reduces player's health
            event = random.choice(['ghost', 'song',"nothing"])
            if event == 'ghost':
                damage= random.randint(2,7)
                self.health -=damage
                print("You feel a cold presence touching you..")
                print("You lose "+str(damage)+" health ")
                print("         ")
 
            elif event == 'song':
                print("You hear a dark melody")
                print("The sadness cracks your very soul ")
                damage= random.randint(1,3)
                self.health -=damage
                print("You lose "+str(damage)+" health ")
                
            
            elif event == 'nothing':
                print("Nothing happens, you struggle forward")
                print("         ")
                print("         ")
                
            if self.health <= 0:
                print("Wounds upon wounds you fall to the consuming darkness.( Game over ) " )
                winsound.PlaySound(".\\music\\rip.wav",  winsound.SND_ALIAS | winsound.SND_ASYNC)
                time.sleep(7)
                quit()

      else:
            print("A wall blocks your path")
            print("")
            print("")
      
      return True
      
class Door:
  def __init__(self, x, y):
      self.x = x
      self.y = y

class HealthObject:
  def __init__(self, x, y):
      self.x = x
      self.y = y
      self.value = random.randint(40, 75)

  def __str__(self):
      return 'F'

class Thorns:
 def __init__(self, x, y):
     self.x = x
     self.y = y

 def __str__(self):
     return 'T'

class Game:
  def __init__(self, player,stats):
      self.player = player
      self.stats=stats
      self.grid = [['#' for _ in range(22)] for _ in range(22)]
      for i in range(1, 21):
          for j in range(1, 21):
              self.grid[i][j] = '.'
      self.grid[5][5] = '#'
      self.add_random_walls(self.stats.walls)
      self.door = self.add_random_door()
      self.add_random_health_objects(5)
      self.add_random_thorns(self.stats.thorns)

  def add_random_walls(self, num_walls):
      for _ in range(num_walls):
          x = random.randint(1, 20)
          y = random.randint(1, 18)
          self.grid[y][x] = '#'

  def add_random_health_objects(self, num_objects):
      for _ in range(num_objects):
          x = random.randint(1, 20)
          y = random.randint(1, 18)
          self.grid[y][x] = HealthObject(x, y)

  def add_random_thorns(self, num_thorns):
      for _ in range(num_thorns):
          x = random.randint(1, 20)
          y = random.randint(1, 20)
          if self.grid[y][x]!='D':
              self.grid[y][x] = Thorns(x, y)

  def add_random_door(self):
          x = random.randint(1, 20)
          y = random.randint(19, 20)
          self.grid[y][x] = 'D'
          return Door(x, y)

  def check_collision(self):
     if self.player.x == self.door.x and self.player.y == self.door.y:
       self.stats.level += 1 # Increment level
       if self.stats.level==6:
           winsound.PlaySound(".\\music\\Hope.wav",  winsound.SND_ALIAS | winsound.SND_ASYNC +winsound.SND_LOOP)
           print("You escape the forgotten dungeon  ")
           print("No more will the roots bind you ")
           print("         ")
           print("      Congratulations            ")
           input("   Press Enter to continue  ")
           print("\033c", end="")   # clear console screen
           print("Programming by Chat Gpt, Tommy Kwong ")
           print("Music By Tommy Kwong ")
           print("         ")
           input("click any button to quit the game")
           quit()
       print('Go in any direction to continue')
       self.create_new_game_state()
     elif self.player.health <= 0:
       
       print("Wounds upon wounds you fall to the consuming darkness. ( Game Over ) ")
       winsound.PlaySound(".\\music\\rip.wav",  winsound.SND_ALIAS | winsound.SND_ASYNC)
       time.sleep(7)
       quit()
     return True

  def create_new_game_state(self):
     print("\033c", end="")   # clear console screen
     print('You step through the door and climb a staircase.')
     print('You reach another floor where the thorns have grown more feral and abundant')
     print("It is almost like the dungeon does not want you to leave... ")
     self.stats.walls+=7
     self.stats.thorns+=55

     # Clear the grid of any previous wall objects
     for y in range(1, 21):
         for x in range(1, 21):
             if self.grid[y][x] == '#' or isinstance(self.grid[y][x], HealthObject) or isinstance(self.grid[y][x], Thorns):
                self.grid[y][x] = '.'

     # Generate new player
     self.player.x = random.randint(1,20)
     self.player.y = random.randint(1,3)

     # Generate new door
     self.door = self.add_random_door()

     # Generate new walls
     self.add_random_walls(self.stats.walls)
     self.add_random_health_objects(self.stats.health_object)
     self.add_random_thorns(self.stats.thorns)

     self.print_grid()
     self.check_collision()

  def print_grid(self):
   # Replace 'D' with '.'
   for y, row in enumerate(self.grid):
       for x, cell in enumerate(row):
           if cell == 'D':
               self.grid[y][x] = '.'

   
   for y, row in enumerate(self.grid):
       for x, cell in enumerate(row):
           if x == self.player.x and y == self.player.y:
               print('@', end='')
           elif x == self.door.x and y == self.door.y:
               print('D', end='')
           else:
               print(cell, end='')
       print()

  def play(self):
    while True:                # clear console screen
        self.print_grid()
        if not self.check_collision():
            break
        print(f"Player's Health: {self.player.health}") # Print player's health
        print(f"Dungeon Level: {self.stats.level}") # Print player's level
        print(str(self.stats.thorns)+" "+str(self.stats.walls)+" "+str(self.stats.health_object)) # Print player's level
        key = input('Enter move (wasd): ')
        print("\033c", end="") 
        if key == 'w':
            if not self.player.move(0, -1, self.grid):
               break
        elif key == 'a':
            if not self.player.move(-1, 0, self.grid):
               break
        elif key == 's':
            if not self.player.move(0, 1, self.grid):
               break
        elif key == 'd':
            if not self.player.move(1, 0, self.grid):
               break
        else:
            print('Invalid move')
            print('')
            print('')
            self.check_collision()

print("                 The Roots that Bind                   ")
print("                                               ")
print("You wake up in a derelict dungeon. You see only overgrown thorns   " )
print("and crumbling walls surrounding you. " )
print("You feel a cold presence watching you in the shadows.  " )
print("You must act swiftly before the darkness consumes.  ")
print("                                               ")
input("         Press Enter to continue  ")
print("\033c", end="")   # clear console screen
print("                 The Roots that Bind                   ")
print("                                               ")
print("           T=Thorns, F=Health, D=Door, #=Wall         ")
print("        Survive through 5 floors to reach the exit         ")
print("           After every movement press 'enter' ")
print("                                               ")
input("               Press Enter to continue  ")
print("\033c", end="") 
print("         ")
print("         ")
print("         ")

playerX = random.randint(1, 5)
playerY = random.randint(1, 5)
player = Player(playerX, playerY)
stats = Stats(walls,thorns,level,health_object)
game = Game(player,stats)
game.play()
