import pstats
import numpy as np
import matplotlib.pyplot as plt
import glob


ntrials = len(glob.glob("1ranks_t*.profile"))

profs = sorted(glob.glob("*.profile"))
nranks = int(len(profs)/ntrials)
ranks = list(range(1, nranks+1))
grpd_profs = []

avg_times = []



for i in ranks:
    iprofs = []
    for j in range(ntrials):
        iprofs.append(profs[i*j])
    grpd_profs.append(iprofs)

for grp in grpd_profs:
    l = len(grp)
    avg_t = 0.0
    for f in grp:
        s = pstats.Stats(f)
        avg_t += s.total_tt
    avg_t = avg_t/l
    avg_times.append(avg_t)

plt.plot(ranks, avg_times)
plt.xlabel("ranks")
plt.ylabel(r"Program Runtime (s)")
plt.title("Strong Scaling of PPMD")
plt.savefig("StrongScaling.eps")


    
