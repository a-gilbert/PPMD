import numpy as np
import h5py
import glob
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_energy_data(fp):
    files = sorted(glob.glob("%s*" % fp))
    en = []
    for i in range(len(files)):
        f = h5py.File(files[i], 'r')
        if f['SimParams'].attrs['energy'] != 'not calculated':
            en.append(f['SimParams'].attrs['energy'])
        f.close()
    return np.array(en)


def get_sim_data(fn):
    f = h5py.File(fn, 'r')
    fs = []
    rs = []
    vs = []
    ids = []
    en = []
    en.append(f['SimParams'].attrs['energy'])
    for k in f.keys():
        if k != 'SimParams':
            g = f[k]
            fs.append(g['fs'][:])
            vs.append(g['vs'][:])
            rs.append(g['rs'][:])
            ids.append(g['ids'][:])
    fs = np.array(fs)
    fs = fs.reshape(fs.shape[0]*fs.shape[1], 3)
    rs = np.array(rs)
    rs = rs.reshape(fs.shape)
    vs = np.array(vs)
    vs = vs.reshape(fs.shape)
    ids = np.array(ids)
    ids = ids.reshape((fs.shape[0],))
    out = {'fs':fs, 'vs':vs,
          'rs':rs, 'ids':ids, 
           'en':np.array(en)}
    return out

def get_2body_data(fp):
    files = sorted(glob.glob("%s*.hdf5" % fp))
    re = []
    ri = []
    ve = []
    vi = []
    for f in files:
        data = get_sim_data(f)
        ids = data['ids']
        rs = data['rs']
        vs = data['vs']
        re.append(rs[ids==0])
        ri.append(rs[ids==1])
        ve.append(vs[ids==0])
        vi.append(vs[ids==1])
    re = np.array(re)
    re = re.reshape(1*re.shape[0], 3)
    ri = np.array(ri)
    ri = ri.reshape(1*ri.shape[0],3)
    ve = np.array(ve)
    ve = ve.reshape(1*ve.shape[0], 3)
    vi = np.array(vi)
    vi = vi.reshape(1*vi.shape[0], 3)
    out = {'re':re, 'ri':ri,
            've':ve, 'vi':vi}
    return out


def get_force(r1, r2, q1, q2, k):
    rinv = 1.0/np.sqrt(np.sum((r1-r2)**2))
    en = k*q1*q2*rinv
    out = en*rinv*rinv*(r1-r2)
    return out, en


def get_expected_trajectories(nsteps, ve0, vi0, re0, ri0, dt=0.001, me=1.0,
    mp=1836.2, k=1.0, qe=-1.0, qp=1.0):
    re = np.zeros((nsteps, len(re0)))
    re[0, :] = re0
    ri = np.zeros((nsteps, len(ri0)))
    ri[0, :] = ri0
    ve = np.zeros((nsteps, len(ve0)))
    ve[0, :] = ve0
    vi = np.zeros((nsteps, len(vi0)))
    vi[0, :] = vi0
    fe = np.zeros((nsteps, len(re0)))
    fi = np.zeros((nsteps, len(ri0)))
    f0, e0 = get_force(re0,ri0, qe, qp, k)
    fe[0, :] += f0
    fi[0, :] -= f0
    en = np.zeros(nsteps)
    en[0] = e0 + 0.5*me*np.sum(ve**2) + 0.5*mp*np.sum(vi**2)
    for i in range(1, nsteps):
        ve[i, :] = ve[i-1, :] + 0.5*(dt/me)*fe[i-1, :]
        vi[i, :] = vi[i-1, :] + 0.5*(dt/mp)*fi[i-1, :]
        re[i, :] = re[i-1, :] + dt*ve[i, :]
        ri[i, :] = ri[i-1, :] + dt*vi[i, :]
        f, e = get_force(re[i], ri[i], qe, qp, k)
        fe[i] = f
        fi[i] = -1*f
        ve[i] += 0.5*(dt/me)*f
        vi[i] -= 0.5*(dt/mp)*f
        en[i] = e + 0.5*me*np.sum(ve[i]**2) + 0.5*mp*np.sum(vi[i]**2)
    out = {'fi':fi, 'fe':fe,
          've':ve, 'vi':vi,
          're':re, 'ri':ri,
          'en':en}
    return out
    


def plot_trajectories(data, mdata):
    edata = get_expected_trajectories(data['re'].shape[0], data['ve'][0], data['vi'][0], 
            data['re'][0], data['ri'][0])
    plt.close('all')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(data['re'][:, 0], data['re'][:, 1], data['re'][:, 2], color='C0', 
            linestyle='-', label='1 Core Electron')
    ax.plot(data['ri'][:, 0], data['ri'][:, 1], data['ri'][:, 2], color='C1', 
            linestyle='-', label='1 Core Proton')
    ax.plot(mdata['re'][:, 0], mdata['re'][:, 1], mdata['re'][:, 2], color='C0', 
            linestyle='-.', label='2 Core Electron')
    ax.plot(mdata['ri'][:, 0], mdata['ri'][:, 1], mdata['ri'][:, 2], color='C1', 
            linestyle='-.', label='2 Core Proton')
    ax.plot(edata['re'][:, 0], edata['re'][:, 1], edata['re'][:, 2], color='C0', 
            linestyle='--', label='Answer Electron')
    ax.plot(edata['ri'][:, 0], edata['ri'][:, 1], edata['ri'][:, 2], color='C1', 
            linestyle='--', label='Answer Proton')
    ax.view_init(elev=45, azim=45)
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.savefig("Trajectory.eps")


score_en = get_energy_data("sDD")
mcore_en = get_energy_data("DD")
en_diff = np.absolute(score_en - mcore_en)/np.absolute(score_en)
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
plt.savefig("Energy.eps")



score_traj = get_2body_data('sDD')
mcore_traj = get_2body_data('DD')
plot_trajectories(score_traj, mcore_traj)
quit()



