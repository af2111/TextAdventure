import os, random, time, platform
def clear():
    if platform.system() == "Linux" or platform.system("Darwin"):
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
#Item Class(Has a name, weight, price and type)
class Item:
    def __init__(self, name, weight, price, itemType):
        self.name = name
        self.weight = weight
        self.price = price
        self.type = itemType
        self.alreadyEquipped = False
#Weapon inherits from Item and has a stat damage as a bonus
class Weapon(Item):
    def __init__(self, name, weight, price, bonusStats):
        Item.__init__(self, name, weight, price, "Weapon")
        self.stats = bonusStats
class Armor(Item):
    def __init__(self, name, weight, price, bonusStats):
        Item.__init__(self, name, weight, price, "Armor")
        self.stats = bonusStats
#Inventory has Items, a maximal weight that it can hold
class Inventory:
    def __init__(self, maxWeight):
        self.maxWeight = maxWeight
        self.items = [Weapon("Stick", 2, 0, {"ap": 2})]
        self.currentslot = 0
    #Method to calculate the current weight of the inventory
    def CurrentWeight(self): 
        state = 0
        for item in self.items:
            if state + item.weight <= self.maxWeight:
                state += item.weight
        return state
    def swapSlot(self):
        while True:
            clear()
            s = input("Which slot do you wanna swap to?\n")
            try:
                if int(s) - 1 == self.currentslot:
                    clear()
                    print("You cant swap to your current slot!")
                    return
                elif int(s) - 1 < len(self.items) and int(s) - 1 >= 0:
                    self.currentslot = int(s) - 1
                    print(f"Swapped to slot {int(s)}")
                    return 1
                else:
                    clear()
                    print("You dont have anything in that slot!")
                    return
            except ValueError:
                clear()
                print("That is not a number.")
                return
    def giveBoni(self, player):
        for key1 in player.stats:
            for key2 in self.items[self.currentslot].stats:
                if key2 == key1: 
                    player.stats[key2] = 0
                    player.stats[key2] += player.basestats[key2] + self.items[self.currentslot].stats[key2]

    #Push an Item to the Inventory and checks if it doesnt overgo the weight limit
    def push(self, item):

        if self.CurrentWeight() + item.weight < self.maxWeight:
            self.items.append(item)
        else:
            print("Your inventory is full.")
            return 0
class Attack:
    def __init__(self, name, desc, attackType):
        self.name = name
        self.desc = desc
        self.type = attackType
    def attack(self):
        print("Attaaaaaack woooooooow amaaaaaaaaaaaaziiiiiiiingg")
class DmgAttack(Attack):
    def __init__(self, name, desc, dmg):
        Attack.__init__(self, name, desc, "Damage")
        self.stat = dmg
    def attack(self, attacker, target):
        target.stats["hp"] -= self.stat * attacker.stats["ap"] / target.stats["defense"]


    

#Class Character which is a parent class for every Monster and NPC and shouldnt be mistaken with the Player Class.         
class Character:
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats
class Monster(Character):
    def __init__(self, name, stats, attacks):
        Character.__init__(self, name, stats)
        self.attacks = attacks
#Player inherits from Character and has an inventory with 40 MaxWeight.
class Player(Character):
    def __init__(self, name, stats, basestats, attacks, armor):
        Character.__init__(self, name, stats)
        self.inventory = Inventory(40)
        self.attacks = attacks
        self.basestats = basestats
        self.armor = armor
#Field is a class to define every field on the map. 
class Field:
    def __init__(self, types, items, monsters):
        #get a random type from a list and set it as the type of the map
        self.type = random.choice(types)
        #get a random item from the list items and define it as the loot
        self.loot = random.choice(items)
        self.monsters = []
        self.monsters.append(random.choice(monsters))
#Map is a Class and can be initialized with a custom height and width
class Map:
    def __init__(self, width, height):
        self.state = []
        self.x = 5
        self.y = 5
        self.height = height
        self.width = width
        #Create a completely random map(2 dimensional list) that consists of instances of fields.
        monsters = [
            Monster("Bok", {
                "hp": 50,
                "ap": 10,
                "defense": 5
            }, [
                DmgAttack("Punch", "Hits you with its fist", 10),
                DmgAttack("Kick", "Kicks you with its Feet", 12)
            ]),
            Monster("Bak", {
                "hp": 100,
                "ap": 6,
                "defense": 7
            }, [
                DmgAttack("Punch", "Hits you with its fist", 10),
                DmgAttack("Kick", "Kicks you with its Feet", 12)
            ])
            
        ]
        for i in range(width):
            fields = []
            for i in range(height):
                fields.append(Field(["forest", "hills", "flatland", "desert"], [Weapon("Club", 5, 5, {"ap": 5}), Weapon("Wooden Sword", 3, 7, {"ap": 4})], monsters))
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
            print(f"Details about your field: \nType: {self.state[self.x][self.y].type}\nLoot: {self.getItems().name}\nMonsters: {len(self.state[self.x][self.y].monsters)}")
        except AttributeError:
            print(f"Details about your field: \nType: {self.state[self.x][self.y].type}\nLoot: Schon genommen!\n Monsters: {len(self.state[self.x][self.y].monsters)}")
    def getItems(self):
        return self.state[self.x][self.y].loot
    def removeLoot(self):
        self.state[self.x][self.y].loot = False
class Fight:
    def __init__(self, player, opponents):
        self.player = player
        self.opponents = opponents
        self.turnCount = 0
    def loop(self):
        while len(self.opponents) > 0:
            if self.turnCount % 2 == 0:
                self.playerTurn()
                self.turnCount += 1
            elif self.turnCount % 2 == 1:
                for opponent in self.opponents:
                    self.opponentTurn(opponent, self.player)
                    self.turnCount += 1
            if self.player.stats["hp"] <= 0:
                exit("You died!")
            for opponent in self.opponents:
                if opponent.stats["hp"] <= 0:
                    self.opponents.remove(opponent)
        print("You won!")
    def chooseAttack(self):
        print("Attacks:")
        for attack in self.player.attacks:
            print(str(self.player.attacks.index(attack) + 1) + f": {attack.name}")
        print("Opponents:")
        for opponent in self.opponents:
            print(opponent.name)
        while True:
            try:
                chosen = self.player.attacks[int(input("Which attack do you choose?")) - 1]
                target = self.opponents[int(input("Which opponent do you want to target?")) - 1]
                clear()
            except ValueError:
                clear()
                print("That's not a number!")
            except IndexError:
                clear()
                print(f"You dont have an attack there! / That opponent doesnt exist")
            else:
                return [chosen, target]

    def playerTurn(self):
        chosenValues = self.chooseAttack()
        attack = chosenValues[0]
        target = chosenValues[1]
        attack.attack(self.player, target)
        print(f"You attacked your opponent with {attack.name}")
        print(f"He's now at {target.stats['hp']}")
        time.sleep(2)
        clear()
    def opponentTurn(self, attacker, target):
        attack = random.choice(attacker.attacks)
        attack.attack(attacker, target)
        print(f"{attacker.name} hit you with {attack.name}")
        print(f"You're now at {target.stats['hp']}")
        time.sleep(2)
        clear()
def print_help(p, m):
    for key in cmds:
        print(key)
def forward(p, m):
    m.forward()
def left(p, m):
    m.left()
def getArmorBoni(p, m):
    for piece in p.armor:
        for key in p.armor[piece].stats:
            for key2 in p.stats:
                if key == key2:
                    combinedStat = 0
                    for piece in p.armor:
                        combinedStat += p.armor[piece].stats[key]
                    p.stats[key] = p.basestats[key] + combinedStat 
def showarmor(p, m):
    for piece in p.armor:
        print(piece + p.armor[piece].name)


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
def swapSlot(p, m):
    p.inventory.swapSlot()
def equip(p, m):
    p.inventory.giveBoni(p)
def stats(p, m):
    for key in p.stats:
        print(f"{key}: {p.stats[key]}")
def fight(p, m):
    fight = Fight(p, m.state[m.x][m.y].monsters)
    fight.loop()

cmds = {
    "help": print_help,
    "forward": forward,
    "left": left,
    "right": right,
    "backwards": backwards,
    "inventory": inventory,
    "pickup": pickup,
    "quit": quit_game,
    "exit": quit_game,
    "slot": swapSlot,
    "stats": stats,
    "fight": fight,
    "equip": equip,
    "armor": showarmor
}
if __name__ == "__main__":
    clear()
    name = input("Choose a name\n")
    clear()
    stats = {
        "hp": 100,
        "ap": 10,
        "defense": 10
    }
    basestats = {
        "hp": 100,
        "ap": 10,
        "defense": 10
    }
    leatherBoots = Armor("Leather Boots", 2, 1, {
        "defense": 1
    })
    leatherLeggings = Armor("Leather Leggings", 3, 2, {
        "defense": 2
    })
    leatherJacket = Armor("Leather Jacket", 4, 3, {
        "defense": 5
    })
    leatherCap = Armor("Leather Cap", 2, 1, {
        "defense": 2
    })
    p = Player(name, stats, basestats, [DmgAttack("Hit", "Hit your opponent with your equipped Weapon.", 10)], {
        "boots": leatherBoots,
        "leggings": leatherLeggings,
        "jacket": leatherJacket,
        "cap": leatherCap
    })
    m = Map(10, 10)
    getArmorBoni(p, m)
    print("You wake up. You have nothing but a stick, a bag and some clothes.")
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