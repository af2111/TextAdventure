import os, random, time, platform
#Item Class(Has a name, weight, price and type)
class Item:
    def __init__(self, name, weight, price, itemType):
        self.name = name
        self.weight = weight
        self.price = price
        self.type = itemType
#Weapon inherits from Item and has a stat damage as a bonus
class Weapon(Item):
    def __init__(self, name, weight, price, damage):
        Item.__init__(self, name, weight, price, "Weapon")
        self.damage = damage
#Inventory has Items, a maximal weight that it can hold
class Inventory:
    def __init__(self, maxWeight):
        self.maxWeight = maxWeight
        self.items = [Weapon("Stick", 2, 0, 1)]
    #Method to calculate the current weight of the inventory
    def CurrentWeight(self): 
        state = 0
        for item in self.items:
            if state + item.weight <= self.maxWeight:
                state += item.weight
        return state
    #Push an Item to the Inventory and checks if it doesnt overgo the weight limit
    def push(self, item):
        if self.CurrentWeight() + item.weight < self.maxWeight:
            self.items.append(item)
        else:
            print("Your inventory is full.")
            return 0

#Class Character which is a parent class for every Monster and NPC and shouldnt be mistaken with the Player Class.         
class Character:
    def __init__(self, name, hp, ap):
        self.name = name
        self.hp = hp
        self.ap = ap
#Player inherits from Character and has an inventory with 40 MaxWeight.
class Player(Character):
    def __init__(self, name, hp, ap):
        Character.__init__(self, name, hp, ap)
        self.inventory = Inventory(40)
#Field is a class to define every field on the map. 
class Field:
    def __init__(self, types, items):
        #get a random type from a list and set it as the type of the map
        self.type = random.choice(types)
        #get a random item from the list items and define it as the loot
        self.loot = random.choice(items)
#Map is a Class and can be initialized with a custom height and width
class Map:
    def __init__(self, width, height):
        self.state = []
        self.x = 5
        self.y = 5
        self.height = height
        self.width = width
        #Create a completely random map(2 dimensional list) that consists of instances of fields.
        for i in range(width):
            fields = []
            for i in range(height):
                fields.append(Field(["forest", "hills", "flatland", "desert"], [Weapon("Club", 5, 5, 5), Weapon("Wooden Sword", 3, 7, 4)]))
            self.state.append(fields)
    def forward(self):
        if self.x == self.height - 1:
            print("You see a big wall that you cant climb over.")
        else:
            print("Moved forward.")
            self.x += 1
            self.printState()
    def right(self):
        if self.y == self.width - 1:
            print("You see a big wall that you cant climb over.")
        else:
            self.y += 1
            print("Moved right.")
            self.printState()
    def backwards(self):
        if self.x == 0:
            print("You see a big wall that you cant climb over.")
        else:
            self.x -= 1
            print("Moved backwards.")
            self.printState()
    def left(self):
        if self.y == 0:
            print("You see a big wall that you cant climb over.")
        else:
            self.y -= 1
            print("Moved left.")
            self.printState()
    def printState(self):
        try:
            print(f"Details about your field: \nType: {self.state[self.x][self.y].type}\nLoot: {self.getItems().name}")
        except AttributeError:
            print(f"Details about your field: \nType: {self.state[self.x][self.y].type}\nLoot: Schon genommen!")
    def getItems(self):
        return self.state[self.x][self.y].loot
    def removeLoot(self):
        self.state[self.x][self.y].loot = False
def print_help(p, m):
    for key in cmds:
        print(key)
def forward(p, m):
    m.forward()
def left(p, m):
    m.left()

def right(p, m):
    m.right()
def quit_game(p, m):
    exit("Ded.")
def backwards(p, m):
    m.backwards()
def inventory(p, m):
    for i in range(len(p.inventory.items)):
        print(f"{i + 1}. {p.inventory.items[i].name}, Type {p.inventory.items[i].type}, Weight: {p.inventory.items[i].weight}, Price: {p.inventory.items[i].price}")
    print(f"\nTotal Weight: {p.inventory.CurrentWeight()}")
def pickup(p, m):
    if m.getItems():
        if p.inventory.push(m.getItems()) != 0:
            m.removeLoot()
            print("Picked up item!")
    else:
        print("Item already picked up!")
def clear():
    if platform.system() == "Linux" or platform.system("Darwin"):
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
cmds = {
    "help": print_help,
    "forward": forward,
    "left": left,
    "right": right,
    "backwards": backwards,
    "inventory": inventory,
    "pickup": pickup,
    "quit": quit_game,
    "exit": quit_game
}
if __name__ == "__main__":
    clear()
    name = input("Choose a name\n")
    clear()
    p = Player(name, 100, 10)
    m = Map(10, 10)
    print("You wake up. You have nothing but a stick and a bag.")
    time.sleep(1.4)
    print("type \"help\" for help")
    m.printState()
    while True:
        cmd = input("> ").lower().split(" ")
        clear()
        if cmd[0] in cmds:
            cmds[cmd[0]](p, m)
        else:
            print(f"BOKE {name.upper()} BOKE (Der Befehl \"{cmd[0]}\" existiert nicht)")