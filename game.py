import os
import time
import random
import winsound

level=1
walls=30
thorns=50

winsound.PlaySound(".\\music\\Roots.wav",  winsound.SND_ALIAS | winsound.SND_ASYNC +winsound.SND_LOOP)

class Player:
  def __init__(self, x, y):
      self.x = x
      self.y = y
      self.health = 40
  
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
                  
              else:
                print("Your body is healthy but you enjoy the refreshment anyway")
                print("You gain 15 health.")
                player.health+=15
              
              grid[new_y][new_x] = '.'
                
              time.sleep(.8)
                

          elif isinstance(grid[new_y][new_x], Thorns):
              print("You tear away the thorns with your hands (It hurts..)")
              damage= random.randint(20,35)
              self.health -=damage
              print(f"You lose "+str(damage)+" health!")
              
              if self.health <= 0:
                  print("Wounds upon wounds you fall to the consuming darkness. ( Game over ) " )
                  winsound.PlaySound(".\\music\\rip.wav",  winsound.SND_ALIAS | winsound.SND_ASYNC)
                  time.sleep(7)
                  quit()
              grid[new_y][new_x] = '.'
              
              time.sleep(.8)

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
                time.sleep(.5)
            
            elif event == 'song':
                print("You hear a dark melody")
                print("The sadness cracks your very soul ")
                damage= random.randint(1,3)
                self.health -=damage
                print("You lose "+str(damage)+" health ")
                time.sleep(.6)
            
            elif event == 'nothing':
                print("Nothing happens, you struggle forward")
                time.sleep(.5)

            if self.health <= 0:
                print("Wounds upon wounds you fall to the consuming darkness.( Game over ) " )
                winsound.PlaySound(".\\music\\rip.wav",  winsound.SND_ALIAS | winsound.SND_ASYNC)
                time.sleep(7)
                quit()

      return True

class Door:
  def __init__(self, x, y):
      self.x = x
      self.y = y

class HealthObject:
  def __init__(self, x, y):
      self.x = x
      self.y = y
      self.value = random.randint(45, 75)


  def __str__(self):
      return 'F'

class Thorns:
 def __init__(self, x, y):
     self.x = x
     self.y = y

 def __str__(self):
     return 'T'

class Game:
  def __init__(self, player):
      self.player = player
      self.grid = [['#' for _ in range(22)] for _ in range(22)]
      for i in range(1, 21):
          for j in range(1, 21):
              self.grid[i][j] = '.'
      self.grid[5][5] = '#'
      self.add_random_walls(walls)
      self.door = self.add_random_door()
      self.add_random_health_objects(5)
      self.add_random_thorns(thorns)

  def add_random_walls(self, num_walls):
      for _ in range(num_walls):
          x = random.randint(1, 20)
          y = random.randint(1, 19)
          self.grid[y][x] = '#'

  def add_random_door(self):
      while True:
          x = random.randint(2, 19)
          y = random.randint(17, 19)
          if self.grid[y][x] != '#':
              self.grid[y][x] = 'D'
              return Door(x, y)

  def add_random_health_objects(self, num_objects):
      for _ in range(num_objects):
          x = random.randint(1, 20)
          y = random.randint(1, 16)
          self.grid[y][x] = HealthObject(x, y)

  def add_random_thorns(self, num_thorns):
      for _ in range(num_thorns):
          x = random.randint(1, 20)
          y = random.randint(1, 16)
          self.grid[y][x] = Thorns(x, y)

  def check_collision(self):
     if self.player.x == self.door.x and self.player.y == self.door.y:
       print('You go through the door.')
       global level 
       level += 1 # Increment level
       if level==5:
           winsound.PlaySound(".\\music\\Hope.wav",  winsound.SND_ALIAS | winsound.SND_ASYNC +winsound.SND_LOOP)
           print("You escape the forgotten dungeon  ")
           print("No more will the roots bind you ")
           print("      congratulations            ")
           input("   Press Enter to continue  ")
           os.system('cls' if os.name == 'nt' else 'clear') # clear console screen
           print("Programming by Chat Gpt 85%, Tommy Kwong 15%")
           print("Music By Tommy Kwong ")
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
     global walls
     global thorns
     walls+=10
     thorns+=50

     # Clear the grid of any previous wall objects
     for y in range(1, 17):
         for x in range(1, 17):
             if self.grid[y][x] == '#' or isinstance(self.grid[y][x], HealthObject) or isinstance(self.grid[y][x], Thorns):
                self.grid[y][x] = '.'

     # Generate new player
     playerX = random.randint(1, 5)
     playerY = random.randint(1, 5)
     old_Health=self.player.health
     self.player = Player(playerX, playerY)
     self.player.health=old_Health
     
     # Generate new door
     self.door = self.add_random_door()

     # Generate new walls
     self.add_random_walls(walls)
     self.add_random_health_objects(7)
     self.add_random_thorns(thorns)

     self.print_grid()
     self.check_collision()

  def print_grid(self):
   # Replace 'D' with '.'
   for y, row in enumerate(self.grid):
       for x, cell in enumerate(row):
           if cell == 'D':
               self.grid[y][x] = '.'

   os.system('cls' if os.name == 'nt' else 'clear') # clear console screen
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
    while True:
        self.print_grid()
        if not self.check_collision():
            break
        print(f"Player's Health: {self.player.health}") # Print player's health
        print(f"Dungeon Level: {level}") # Print player's level
        key = input('Enter move (wasd): ')
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
            time.sleep(0.6) # pause for 0.1 seconds
            self.check_collision()

print("                 The Roots that Bind                   ")
print("You wake up in a derelict dungeon. You see only overgrown thorns   " )
print("and crumbling walls surrounding you. " )
print("You feel a cold presence watching you in the shadows.  " )
print("You must act swiftly before the darkness consumes.  ")
print("                                               ")
input("         Press Enter to continue  ")
os.system('cls' if os.name == 'nt' else 'clear') # clear console screen


print("                 The Roots that Bind                   ")
print("           T=Thorns, F=Health, D=Door, #=Wall         ")
print("           After every movement press 'enter' ")
print("                                               ")
input("               Press Enter to continue  ")

playerX = random.randint(1, 5)
playerY = random.randint(1, 5)
player = Player(playerX, playerY)
game = Game(player)
game.play()
