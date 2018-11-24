import numpy as np 
from params import GPK


class Particles(object):

	def __init__(self, ntypes, ids, types, ms, qs, rs, vs, fs, dt):
		super(Particles, self).__init__()
		self.ids = ids
		self.types = types
		self.ms = ms
		self.qs = qs
		self.rs = rs
		self.vs = vs
		self.fs = fs
		self.dt = dt


	def integrate_vhalf(self):
		for i in range(ntypes):
			vdt = self.dt/(2*self.ms[i])
			mask = self.types==i
			self.vs[mask] += vdt*self.fs[mask]


	def integrate_pos(self):
		self.rs = self.rs + self.dt*self.vs


	def make_periodic(self, sim_bbox):
		self.rs = self.rs - sim_bbox[0]
		self.rs = self.rs % (sim_bbox[1]-sim_bbox[0])
		



