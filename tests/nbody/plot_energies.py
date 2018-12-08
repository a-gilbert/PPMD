import numpy as np
import h5py
import glob
import matplotlib.pyplot as plt

ls = ['-', '--']
labels = ['ts1', 'ts2']

def get_energy_data(fp):
    files = sorted(glob.glob("%s*" % fp))
    en = []
    for i in range(len(files)):
        f = h5py.File(files[i], 'r')
        if f['SimParams'].attrs['energy'] != 'not calculated':
            en.append(f['SimParams'].attrs['energy'])
        f.close()
    return np.array(en)

sc_ens = []
mc_ens = []
diffs = []


for i in range(1, 3):
    sc_en = get_energy_data("scts%dDD" % i)
    mc_en = get_energy_data("mcts%dDD" % i)
    gmean = np.sqrt(np.average(mc_en)*np.average(sc_en))
    en_diff = np.absolute(sc_en - mc_en)/gmean
    sc_en = np.absolute(sc_en - sc_en[0])/np.absolute(sc_en[0])
    mc_en = np.absolute(mc_en - mc_en[0])/np.absolute(mc_en[0])
    sc_ens.append(sc_en)
    mc_ens.append(mc_en)
    diffs.append(en_diff)

steps = np.arange(len(sc_ens[0]))

plt.close('all')
for i in range(len(sc_ens)):
    sc_lab = "Single Core,%s" % labels[i]
    mc_lab = "Multi Core,%s" % labels[i]
    d_lab = "Difference,%s" % labels[i]
    plt.semilogy(steps, sc_ens[i], color='C0', linestyle=ls[i], label=sc_lab)
    plt.semilogy(steps, mc_ens[i], color='C1', linestyle=ls[i], label=mc_lab)
    plt.semilogy(steps, diffs[i], color='C2', linestyle=ls[i], label=d_lab) 
plt.xlabel("Step")
plt.ylabel("Relative Energy Drift/Energy Difference")
plt.legend()
plt.savefig("Energy.eps")
quit()
