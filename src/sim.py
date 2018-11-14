"""The entry class for the entire simulation framework."""
from params import GlobalParams, GPK



class SimSystem(object):

	def __init__(self, in_file, comm, rank):
		#set simulation parameters
		self._sim_params = GlobalParams(in_file, comm, rank)
		self.grid = Grid()

	
	def balance(self):
		pass


	def step(self):
		pass 