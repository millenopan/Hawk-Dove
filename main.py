import random, statistics as stat, copy

'''
    MAIN.PY - This file is where the bulk of the code happens.
    Start() is how we run a simulation of our entire population once with
    the number of Animals provided and which kind of Animal clearly labeled.
    The Start() method also returns statistical data used to calculate interesting
    outcomes.



    Many different classes of Animals have been implemented below. Besides the
    Hawk and Dove class, all the other classes are unique with a certain defining
    characteristic.
    Some things I've experimented with:

    ### Bear [NOT LISTED ANYMORE] - Higher food consumption but wins fights with better payouts.
    E.G. --> [100,0] against Doves, [150,0] against Hawks, [-75,-75] against Bears.
    this idea was interesting at first, but upon simulation it clearly just leads to
    one Bear killing off the rest of the species before dying off. Any excess Bears
    will likely lead to a similar case, but faster.

    ### Mutant - This animal grows stronger with each interaction it survives. It primarily
    plays like a Dove, with a unique attribute: essentially, you gain some "bonus" points
    regardless of the interaction outcome. This was the most unique Animal I've come
    up with: A very small increase of just 4 points (Relative to 100 being the max value)
    leads to this going head-to-head in survivalability to Hawks. This likely can be
    grinded out for a perfectly balanced value depending on average days survived by an animal.

    ### Tit - The 'Tit for Tat' playstyle, implemented here. Unfortunately, this works poorly in
    a game with only Doves and Hawks: You are at too far a disadvantage if you play in a
    Tit for Tat style and face against a Hawk. It is arguably the same as a pure Dove strategy.
    (Tit for Tat plays the previous interaction's opponent's move, copying almost as if it was
    in retaliation to the population. If there is none, where the simulation just started,
    Tit defaults to playing as a Dove.)

    ### Human - This animal tries to play randomly with a varying probability, denoted
    as the human_magic_number attribute. This starts off as V/2C, the equilibrium value
    in a balanced setting. However, it changes relative to how many Wolves, Doves and Humans
    that are left in the game. Currently, it seems like based on how reproduction is coded,
    where I have made it a fixed value of around 4x the food consumption amount to reproduce,
    this Animal is just a little bit weaker than the Hawk.




    Overall, a very fun project. The most interesting moments came early on, where
    running one or two simulations felt like a new world was genuinely being created
    and lived out by these animals. Tinkering with small values, and coming up with
    new types of Animals also gave this simple game a lot more depth and possibilities
    to look into.


    If I ever came back, I think the first things I would do would be:

        1. Implement the GUI to have adjustable payoff matrices, starting animals,
        number of simulations, and statistical graphs.
        2. Potentially change how reproduction works: The simplicity of the one used
        here is alright, but I think there is a lot more depth that could be added
        that would make each simulation more interesting depending on this major aspect.



'''

class Animal:
    def __init__(self):
        self.alive = True
        self.food = 100
        self.food_consumption = 50
        self.id = 'Animal'

    def cycle(self):
        self.food -= self.food_consumption
        if self.food <= 0:
            self.alive = False

    def reproduce(self): ##reproduce at 4x food consumption amount
        if self.food >= self.food_consumption * 4:
            self.food //= 2
            x = copy.deepcopy(self)
            if hasattr(self, 'good_gene'):
                x.good_gene = 0
            return x


    def __str__(self):
        return self.id + ", Food: " + str(self.food)
    def __repr__(self):
        return self.id + ", Food: " + str(self.food)


class Dove(Animal): ##Dove: always plays nice
    def __init__(self):
        Animal.__init__(self)
        self.id = 'Dove'

class Hawk(Animal): ##Hawk: always plays mean
    def __init__(self):
        Animal.__init__(self)
##        self.food = 150
##        self.food_consumption = 75
        self.id = 'Hawk'

class Mutant(Animal): ##positive extra payout from each surviving encounter
    def __init__(self):
        Animal.__init__(self)
##        self.food = 250
##        self.food_consumption = 125
        self.id = 'Mutant'
        self.good_gene = 0

class Tit(Animal): ##tit for tat strategy
    def __init__(self):
        Animal.__init__(self)
        self.id = 'Tit'
        self.strat = 'Dove'

    def new_strat(self, last_strat):
        self.strat = last_strat

class Human(Animal): ## V/2C: Equilibrium point
    human_magic_number = 0.4 ##only used for our human fights. Defaults at 0.4.
    def __init__(self):
        Animal.__init__(self)
        self.id = 'Human'


def start():
    end = False
    test_animals = [Dove() for _ in range(10)] + [Hawk() for _ in range(10)] + [Human() for _ in range(10)]

    print(test_animals)
    day_count = 0
    winner = ''
    while len(test_animals) > 1 and day_count < 100: ##hard cap of 100 days: otherwise, equilibrium reached
        hum_denom, hum_num = 1, 0                     #STARTING FROM HERE...
        for i in test_animals:
            if i.id == 'Hawk' or i.id == 'Human':
                hum_num += 1
            hum_denom += 1
        Human.human_magic_number = hum_num/hum_denom #...TO THIS LINE, we have the adapting play strategy from Humans.

        day_count += 1 ##day tracker
        play(test_animals)
        for a in test_animals: a.cycle() ##run one cycle
        copied = list(test_animals) ##reproduction implementation below
        for a in copied:
            temp = a.reproduce()
            if hasattr(temp, 'alive'):
                test_animals += [temp]
        print(cleanup(test_animals)) ##cleans up

        if (test_animals and ##only one Animal type remains
                (all(i.id == 'Dove' for i in test_animals) or
                ##all(i.id == 'Mutant' for i in test_animals) or
                all(i.id == 'Human' for i in test_animals) or
                all(i.id == 'Hawk' for i in test_animals))):
            winner = test_animals[0].id
            break

    if len(test_animals) == 1:
        winner = test_animals[0].id
    print()
    return day_count, winner


def play(players): ##conducts fights for all players
    random.shuffle(players)
    group1 = players[:len(players)//2]
    group2 = players[len(players)//2:]
    pairs = zip(group1, group2)
    for p1, p2 in pairs:
        result = fight(p1, p2)
        p1.food += result[0]
        p2.food += result[1]

def cleanup(animals): ##removes dead Animals
    temp = list(animals)
    for x in temp:
        if not x.alive:
            animals.remove(x)
    return animals

def fight(p1, p2): ##payouts for players based on their type

    if p1.id == 'Dove' and p2.id == 'Dove':
        return [50, 50]
    elif p1.id == 'Hawk' and p2.id == 'Hawk':
        return [-75, -75]
    elif p1.id == 'Dove' and p2.id == 'Hawk':
        return [0, 100]
    elif p1.id == 'Hawk' and p2.id == 'Dove':
        return [100, 0]

    ###NOTE: WE CANNOT HAVE MORE THAN ONE OF THE FOLLOWING IN A POPULATION: (MUTANT, TIT, HUMAN)
    elif p1.id == 'Mutant' and p2.id == 'Dove':
        p1.good_gene += 4
        return [50 + p1.good_gene, 50]
    elif p1.id == 'Dove' and p2.id == 'Mutant':
        p2.good_gene += 4
        return [50, 50 + p2.good_gene]
    elif p1.id == 'Mutant' and p2.id == 'Hawk':
        p1.good_gene += 4
        return [p1.good_gene, 100]
    elif p1.id == 'Hawk' and p2.id == 'Mutant':
        p2.good_gene += 4
        return [100, p2.good_gene]
    elif p1.id == 'Mutant' and p2.id == 'Mutant':
        return [p1.good_gene, p2.good_gene]

    elif p1.id == 'Tit' and p2.id == 'Dove':
        if p1.strat == 'Dove': return [50,50]
        else: return [100,0]
        p1.new_strat('Dove')
    elif p1.id == 'Dove' and p2.id == 'Tit':
        if p2.strat == 'Dove': return [50,50]
        else: return [0, 100]
        p1.new_strat('Dove')
    elif p1.id == 'Tit' and p2.id == 'Hawk':
        if p1.strat == 'Dove': return [0, 100]
        else: return [-75, -75]
        p1.new_strat('Hawk')
    elif p1.id == 'Hawk' and p2.id == 'Tit':
        if p2.strat == 'Dove': return [100, 0]
        else: return [-75, -75]
        p1.new_strat('Hawk')
    elif p1.id == 'Tit' and p2.id == 'Tit':
        return [50, 50] ##models kin altruism



    elif p1.id == 'Human' and p2.id == 'Dove':
        if random.random() > Human.human_magic_number: return [50,50]
        else: return [100,0]
    elif p1.id == 'Dove' and p2.id == 'Human':
        if random.random() > Human.human_magic_number: return [50,50]
        else: return [0, 100]
    elif p1.id == 'Human' and p2.id == 'Hawk':
        if random.random() > Human.human_magic_number: return [0, 100]
        else: return [-75, -75]
    elif p1.id == 'Hawk' and p2.id == 'Human':
        if random.random() > Human.human_magic_number: return [100, 0]
        else: return [-75, -75]
    elif p1.id == 'Human' and p2.id == 'Human':
        roll1, roll2 = random.random(), random.random()
        if roll1 > Human.human_magic_number and roll2 > Human.human_magic_number: return [50, 50]
        elif roll1 <= Human.human_magic_number and roll2 > Human.human_magic_number: return [100, 0]
        elif roll1 > Human.human_magic_number and roll2 <= Human.human_magic_number: return [0, 100]
        elif roll1 <= Human.human_magic_number and roll2 <= Human.human_magic_number: return [-75, -75]





    else: ##if for some reason the above doesn't include our fight id
        return [0, 0]
