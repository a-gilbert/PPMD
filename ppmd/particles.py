import numpy as np 
import h5py
from ppmd.params import GPK


class Particles(object):

	def __init__(self, ms, qs, ids, types, rs, vs, fs, dt):
		super(Particles, self).__init__()
		self.ms = ms
		self.qs = qs
		self.ids = ids
		self.types = types
		self.rs = rs
		self.vs = vs
		self.fs = fs
		self.energy = 0.0
		self.dt = dt

	@classmethod
	def from_restart(cls, gcomm, params):
		pass

	@classmethod
	def from_custom(cls, gcomm, params):
		f = h5py.File(params[GPK.PIC][1], 'r')
		ms = f['particles']['spec_masses']
		qs = f['particles']['spec_charges']
		my_rank = gcomm.Get_rank()
		nranks = gcomm.Get_size()
		npart = f['particles']['ids'].shape[0]
		remp = npart%nranks
		remc = nranks%npart
		if remc > 0 and my_rank > remc:
			my_npart = 0
		else:
			my_npart = int((npart - remp)/nranks)
			if remp != 0 :
				if my_rank < remp:
					my_npart += 1
					my_li = my_npart*my_rank
					my_ui = my_npart*(my_rank+1)
				else:
					my_li = remp + my_npart*my_rank
					my_ui = remp + my_npart*(my_rank + 1)
			else:
				my_li = my_npart*my_rank
				my_ui = my_npart*(my_rank+1)
		my_ms = np.array(f['particles']['spec_masses'])
		my_qs = np.array(f['particles']['spec_charges'])
		if my_npart != 0:
			my_ids = np.array(f['particles']['ids'][my_li:my_ui]).astype(int)
			my_types = np.array(f['particles']['types'][my_li:my_ui]).astype(int)
			my_rs = np.array(f['particles']['rs'][my_li:my_ui]).astype(float)
			my_vs = np.array(f['particles']['vs'][my_li:my_ui]).astype(float)
			my_fs = np.zeros(my_vs.shape)
		else:
			my_ids = np.empty((1,), dtype=int)
			my_types = np.empty((1,), dtype=int)
			my_rs = np.empty((1, params[GPK.DIMS]))
			my_vs = np.empty_like(my_rs)
			my_fs = np.empty_like(my_rs)
		return Particles(my_ms, my_qs, my_ids, my_types, my_rs, my_vs, my_fs, params[GPK.DT])

	def integrate_vhalf(self):
		for i in range(len(self.ms)):
			vdt = self.dt/(2*self.ms[i])
			mask = self.types==i
			self.vs[mask, :] += vdt*self.fs[mask]


	def integrate_pos(self):
		self.rs = self.rs + self.dt*self.vs

	def add_lkinetic_energy(self):
		for i in range(len(self.ms)):
			self.energy += 0.5*self.ms[i]*np.sum(self.vs[self.types == i]**2)

	
	def get_total_energy(self, gcomm, orank=0):
		out = np.array([0.0])
		gcomm.Reduce(np.array([self.energy]), out, root=orank)
		return out[0]


	def get_total_particles(self, gcomm, orank=0):
		out = np.array([0])
		#buf = np.array([len(self.ids)])
		gcomm.Reduce(np.array([len(self.ids)]), out, root=orank)
		return out[0]


	def make_periodic(self, sim_bbox):
		self.rs = self.rs - sim_bbox.maxes
		self.rs = (self.rs % (sim_bbox.maxes-sim_bbox.mins)) + sim_bbox.mins
		



