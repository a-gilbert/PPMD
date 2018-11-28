"""Module for a number of different force calculations"""
import numpy as np

class CPUFBExactForceCalculator(object):

    @classmethod
    def run(cls, gcomm, lpart, units, calc_energy):
        lpart.fs[:, :] = 0.0
        if calc_energy:
            lpart.energy = 0.0
        CPUFBExactForceCalculator.get_loc_force(lpart, units, calc_energy)
        if gcomm.Get_size() > 1:
            CPUFBExactForceCalculator.get_all_nloc_force(gcomm, lpart, units, 
            calc_energy)

    @classmethod
    def get_loc_force(cls, lpart, units, calc_energy):
        c = units['k']
        for j in range(len(lpart.ids)):
            for i in range(0, j):
                dr = lpart.rs[i] - lpart.rs[j]
                rinv = 1.0/np.sqrt(np.sum(dr**2))
                en = c*lpart.qs[lpart.types[i]]*lpart.qs[lpart.types[j]]*rinv
                if calc_energy:
                    lpart.energy += en
                en = en*rinv*rinv*dr
                lpart.fs[i] += en
                lpart.fs[j] -= en


    @classmethod
    def get_all_nloc_force(cls, gcomm, lpart, units, calc_energy):
        my_rank = gcomm.Get_rank()
        s = gcomm.Get_size()
        if s == 2:
            niter = 1
        else:
            niter = s - 2
        for i in range(niter):
            urank = (i + my_rank + 1)%s
            lrank = (my_rank - i - 1)%s
            CPUFBExactForceCalculator.get_nloc_force(gcomm, urank, lrank, lpart, 
            units, calc_energy)


    
    @classmethod
    def get_nloc_force(cls, gcomm, urank, lrank, lpart, units, calc_energy):
        #number of particles im about to get
        npart = CPUFBExactForceCalculator.get_npart(gcomm, urank, len(lpart.ids))
        nltypes_buf = np.zeros(npart, dtype=int)
        nlrs_buf = np.zeros((npart, lpart.rs.shape[1]))
        #send types to urank, recv types from lrank
        gcomm.Sendrecv(lpart.types, urank, recvbuf=nltypes_buf)
        #send positions and receive, destinations/sources as above
        gcomm.Sendrecv(lpart.rs, urank, recvbuf=nlrs_buf)
        #calc forces
        case = urank==lrank and gcomm.Get_rank()<urank
        CPUFBExactForceCalculator.get_force(lpart, nltypes_buf, nlrs_buf, units, 
        calc_energy, case)
        #buf to get force from higher rank
        nlforce_buf = np.zeros(lpart.fs.shape)
        gcomm.Sendrecv(nlrs_buf, lrank, recvbuf=nlforce_buf)
        lpart.fs[:, :] += nlforce_buf



    @classmethod
    def get_npart(cls, gcomm, drank, npart):
        buf = np.array([npart])
        gcomm.Sendrecv_replace(buf, drank)
        return buf[0]


    @classmethod
    def get_force(cls, lpart, nltypes, nlrs, units, calc_energy, case):
        c = units['k']
        for i in range(len(nltypes)):
            netf = np.zeros(nlrs.shape[1])
            for j in range(len(lpart.ids)):
                dr = nlrs[i] - lpart.rs[j]
                rinv = 1.0/np.sqrt(np.sum(dr**2))
                en = c*lpart.qs[nltypes[i]]*lpart.qs[lpart.types[j]]*rinv
                if case:
                    en = en*0
                if calc_energy:
                    lpart.energy += en
                en = en*rinv*rinv*dr
                netf += en
                lpart.fs[j, :] -= en
            nlrs[i, :] = netf