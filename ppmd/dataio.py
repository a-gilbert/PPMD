import h5py
import numpy as np
from ppmd.params import GPK, RefineCriteria, ForceType, Units, PartitionScheme, \
SpatialBoundaries, ForceBoundaries, ParticleIC


class DataManager(object):

    def __init__(self, params):
        super(DataManager, self).__init__()
        if params[GPK.OUTUN] == True:
            self.fn = "%s.hdf5" % params[GPK.OUTFN]
        else:
            self.fn = "%s%08d.hdf5" % (params[GPK.OUTFN], params[GPK.CSTEP])
    
    def update(self, params):
        if params[GPK.OUTUN] == True:
            pass
        else:
            self.fn = "%s%08d.hdf5" % (params[GPK.OUTFN], params[GPK.CSTEP])

    def _write_sim_data(self, gref, params, tenergy, tpart, masses, qs):
        if params[GPK.UNITS] == Units.DIMENSIONLESS:
            gref.attrs['Units'] = np.string_("dimensionless")
        elif params[GPK.UNITS] == Units.CGS:
            gref.attrs['Units'] = np.string_("cgs")
        elif params[GPK.UNITS] == Units.SI:
            gref.attrs['Units'] = np.string_("si")
        gref.attrs['Dimensions'] = params[GPK.DIMS]
        gref.attrs['Bbox'] = np.array([params[GPK.BBOX].mins, 
        params[GPK.BBOX].maxes])
        if params[GPK.SBTYPE] == SpatialBoundaries.FIXED:
            gref.attrs['SpatialBC'] = np.string_('Fixed')
        elif params[GPK.SBTYPE] == SpatialBoundaries.PERIODIC:
            gref.attrs['SpatialBC'] = np.string_('Periodic')
        if params[GPK.FBTYPE] == ForceBoundaries.FIXED:
            gref.attrs['ForceBC'] = np.string_('Fixed')
        elif params[GPK.FBTYPE] == ForceBoundaries.PERIODIC:
            gref.attrs['ForceBC'] = np.string_('Periodic')
        if params[GPK.PSCHEME] == PartitionScheme.NONE:
            gref.attrs['PartitionScheme'] = np.string_('None')
        elif params[GPK.PSCHEME] == PartitionScheme.GRID:
            gref.attrs['PartitionScheme'] = np.string_('Grid')
        elif params[GPK.PSCHEME] == PartitionScheme.TREE:
            gref.attrs['PartitionScheme'] = np.string_('Tree')
        elif params[GPK.PSCHEME] == PartitionScheme.FOREST:
            gref.attrs['PartitionScheme'] = np.string_('Forest')
        rref = gref.create_group("RefinementCriteria")
        if len(params[GPK.RCRIT]) == 0:
            rref.attrs['None']
        else:
            for i in params[GPK.RCRIT]:
                crit = i[0]
                val = i[1]
                if crit == RefineCriteria.MAX_DENS:
                    rref.attrs['max_dens'] = val
                elif crit == RefineCriteria.MAX_DEPTH:
                    rref.attrs['max_depth'] = val
        gref.attrs['cstep'] = params[GPK.CSTEP]
        gref.attrs['ctime'] = params[GPK.DT]*params[GPK.CSTEP]
        gref.attrs['npart'] = tpart
        if params[GPK.ENERGY] == True:
            if params[GPK.CSTEP] % params[GPK.ENERGYF] == 0:
                gref.attrs['energy'] = tenergy
        gref.attrs['nspec'] = params[GPK.NSPEC]
        gref.attrs['spec_masses'] = masses
        gref.attrs['spec_charges'] = qs
        gref.attrs['using_gpus'] = True if params[GPK.GPUS] == True else False
        gref.attrs['dt'] = params[GPK.DT]


    #currently serialized since h5py is being difficult
    def write_data(self, gcomm, params, bbox, particles):
        gcomm.Barrier()
        if gcomm.Get_rank() == 0:
            print("At serialized IO.")
        #collectives require everyone to call the function.
        en = particles.get_total_energy(gcomm)
        np = particles.get_total_particles(gcomm)
        if gcomm.Get_rank() == 0:
            f = h5py.File(self.fn, 'a')
            if params[GPK.OUTUN] == True:
                g = f.create_group("DD%08d" % params[GPK.CSTEP])
            else:
                g = f
            simg = g.create_group("SimParams")
            for i in range(gcomm.Get_size()):
                g.create_group("Rank%08d" % i)
            self._write_sim_data(simg, params, en, np, particles.ms, 
                particles.qs)
            f.flush()
            f.close()
        for i in range(gcomm.Get_size()):
            if i == gcomm.Get_rank():
                f = h5py.File(self.fn, 'a')
                if params[GPK.OUTUN] == True:
                    g = f['DD%08d' % params[GPK.CSTEP]]
                else:
                    g = f
                my_g = g['Rank%08d' % gcomm.Get_rank()]
                my_g.attrs['bbox'] = [bbox.mins, bbox.maxes]
                my_g.attrs['npart'] = len(particles.types)
                my_g.create_dataset("ids", data=particles.ids)
                my_g.create_dataset("types", data=particles.types)
                my_g.create_dataset("rs", data=particles.rs)
                my_g.create_dataset("vs", data=particles.vs)
                my_g.create_dataset("fs", data=particles.fs)
                f.flush()
                f.close()
            gcomm.Barrier()
        if gcomm.Get_rank() == 0:
            print("IO finished.")