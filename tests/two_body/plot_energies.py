import numpy as np
import h5py
import glob
import matplotlib.pyplot as plt

def get_energy_data(fp):
    files = sorted(glob.glob("%s*" % fp))
    en = []
    for i in range(len(files)):
        f = h5py.File(files[i], 'r')
        if f['SimParams'].attrs['energy'] != 'not calculated':
            en.append(f['SimParams'].attrs['energy'])
        f.close()
    return np.array(en)


score_en = get_energy_data("sDD")
mcore_en = get_energy_data("DD")
en_diff = np.absolute(score_en - mcore_en)
score_en = np.absolute(score_en - score_en[0])/np.absolute(score_en[0])
mcore_en = np.absolute(mcore_en - mcore_en[0])/np.absolute(mcore_en[0])

steps = np.arange(len(score_en))

plt.close('all')
plt.semilogy(steps, score_en, label="Single Core")
plt.semilogy(steps, mcore_en, label="Multi Core")
plt.semilogy(steps, en_diff, label="Difference")
plt.xlabel("Step")
plt.ylabel("Relative Energy Drift/Energy Difference")
plt.legend()
plt.savefig("Energy.png")
quit()



