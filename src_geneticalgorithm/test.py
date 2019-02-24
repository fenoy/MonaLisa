import numpy as np
import  matplotlib.pyplot as plt

def tournament_selection(tournament_size, fitness, last):
    for _ in range(last):
        tournament = np.random.choice(fitness, tournament_size, replace=False)
        best = max(tournament)
        yield best

fitness = [i for i in range(10000)]

selected = [ind for ind in tournament_selection(8, fitness, 10000)]

plt.hist(selected, normed=True)
plt.xlabel("Position selected")
plt.ylabel("Frequency")
plt.ticklabel_format(style="sci", axis="both", scilimits=(0,0))
plt.xlim(0,10000)
#plt.ylim(0,0.5)
plt.show()