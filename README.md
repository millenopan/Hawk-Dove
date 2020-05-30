**Hawk-Dove, a well-known evolutionary game theory problem.**

My implementation here calls the animals Bunny and Wolf. The idea is that Bunny players will cooperate and split with one another, while Wolves will fight. Wolves fighting against each other will leave them worse off, and details on the other payout rates against different players are in the function fight(). What makes this interesting is that adjusting the numbers by a tiny bit could have a substantial impact on the game.

*fight()* - Our function that takes in two animals and returns the outcome between them. This is essentially our "matrix" for payout rates in the general sum game.
*Animal.reproduce()* - The idea here is that if the animal is at a certain multiple of how fast they consume food, they will reproduce.
This means that animals which dominate heavily will split and possibly control more, although some animals like the Wolf might do much better if there is no other Wolf animals to compete with. Changing the ratio of when an Animal can reproduce can also lead to very interesting games.
*play()* - shuffles players, pairs them and calls fight() between each pair.


I have also experiemented adding different animals like Bear, which consumes food at a faster rate, but also gets to make up for it with a large payout rate against other animals. Another idea that is present in the code is the Mutant, which gains an extra amount bonus food each time it survives a fight. This is represented with the attribute "good_gene". New Mutants reset this attribute to prevent an excess number of objects created.


test.py is a space where I run simulations of numerous games, and find statistics and calculations based on the results, such as which type of Animal dominates by the end, or how many average days it takes for the game to end where no animals are left or one type remains.


The inspiration of implementing this came from a lecture during my Game Theory course.
