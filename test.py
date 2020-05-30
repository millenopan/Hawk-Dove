import random, statistics as stat, copy
import main

'''
    TEST.PY - For statistical testing only. Shorthand file to run multiple simulations
    for me to check certain strategies when pit against others: Messing around with
    payout rates, starting # of Animals, modifying reproduction rate, etc.


'''



raw = [main.start() for _ in range(100)]
day_results, winners = [], []
for result in raw:
    day_results += [result[0]]
    winners += [result[1]]


day_results = list(filter(lambda x: x < 100, day_results))
day_results.sort()

doves = len(list(filter(lambda x: x == 'Dove', winners)))
hawks = len(list(filter(lambda x: x == 'Hawk', winners)))
mutants = len(list(filter(lambda x: x == 'Mutant', winners)))
tits = len(list(filter(lambda x: x == 'Tit', winners)))

mean = stat.mean(day_results)
median = stat.median(day_results)
popsd = stat.pstdev(day_results)



print()
print()
print("Day Result List: ")
print(day_results)
print("Days Ended: ")
print(len(day_results))
print()
print('Doves Won: ' + str(doves))
print('Hawks Won: ' + str(hawks))
print('Mutants Won: ' + str(mutants))
print('Tits Won: ' + str(tits))
print()
print("Mean: " + str(mean))
print("Median: " + str(median))
print("SD: " + str(popsd))
