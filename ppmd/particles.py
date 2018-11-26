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
		rem = npart%nranks
		my_npart = int((f['particles']['ids'].shape[0]-rem)/nranks)
		if rem != 0 :
			if my_rank < rem:
				my_npart += 1
				my_li = my_npart*my_rank
				my_ui = my_npart*(my_rank+1)
			else:
				my_li = rem + my_npart*my_rank
				my_ui = rem + my_npart*(my_rank + 1)
		else:
			my_li = my_npart*my_rank
			my_ui = my_npart*(my_rank+1)
		my_ms = f['particles']['spec_masses']
		my_qs = f['particles']['spec_charges']
		my_ids = f['particles']['ids'][my_li:my_ui]
		my_types = f['particles']['types'][my_li:my_ui]
		my_rs = f['particles']['rs'][my_li:my_ui]
		my_vs = f['particles']['rs'][my_li:my_ui]
		my_fs = np.zeros(my_vs.shape)
		return Particles(my_ms, my_qs, my_ids, my_types, my_rs, my_vs, my_fs, params[GPK.DT])

	def integrate_vhalf(self):
		for i in range(len(self.ms)):
			vdt = self.dt/(2*self.ms[i])
			mask = self.types==i
			self.vs[mask, :] += vdt*self.fs[mask]


	def integrate_pos(self):
		self.rs = self.rs + self.dt*self.vs

	def get_lkinetic_energy(self):
		for i in range(len(self.ms)):
			self.energy += 0.5*self.ms[i]*np.sum(self.vs[self.types == i]**2)

	
	def get_total_energy(self, gcomm, orank=0):
		out = self.energy
		gcomm.reduce(out, root=orank)
		return out


	def get_total_particles(self, gcomm, orank=0):
		out = len(self.ids)
		gcomm.reduce(out, root=orank)
		return out


	def make_periodic(self, sim_bbox):
		self.rs = self.rs - sim_bbox.mins
		self.rs = self.rs % (sim_bbox.maxes-sim_bbox.mins)
		



