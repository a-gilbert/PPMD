"""The entry class for the entire simulation framework."""
import numpy as np
from params import GlobalParams, GPK
from region import Bbox



class SimSystem(object):

	def __init__(self, in_file, gcomm):
		#set simulation parameters
		self._sim_params = GlobalParams(in_file, gcomm, gcomm.Get_rank())
		self.loc_bbox = self.init_bbox()

	def init_bbox(self):
		rank = gcomm.Get_rank()
		grid = self._sim_params[GPK.BBOX].grid
		glo_lleft = self._sim_params[GPK.BBOX].get_lleft()
		if len(grid) == 1:
			lrank = self._sim_params[GPK.BBOX].get_volume()/grid[0]
			loc_lleft = glo_lleft + rank*lrank
			loc_uright = glo_lleft + (rank+1)*lrank
		else:
			ls = self._sim_params[GPK.BBOX].get_lens()/grid
			if len(grid) == 2:
				j = rank%grid[1]
				i = int((rank-j)/grid[1])
				#two corners, bottom rear left, and top upper right
				c1 = np.array([i, j])
				c2 = np.array([i+1, j+1])

			if len(grid) == 3:
				k = rank%grid[2]
				j = int(((rank-k)/grid[2])%grid[1])
				i = int((rank-k-grid[2]*j)/(grid[1]*grid[2]))
				c1 = np.array([i, j, k])
				c2 = np.array([i+1, j+1, k+1])
			loc_lleft = glo_lleft + c1*ls
			loc_uright = glo_lleft + c2*ls
		return Bbox(loc_lleft, loc_uright)

	def balance(self):
		pass


	def step(self):
		pass 