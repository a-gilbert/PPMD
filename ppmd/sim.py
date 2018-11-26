"""The entry class for the entire simulation framework."""
import numpy as np
from ppmd.params import GlobalParams, GPK, PartitionScheme, ParticleIC,\
SpatialBoundaries, ForceType
from ppmd.region import Bbox
from ppmd.dataio import DataManager
from ppmd.particles import Particles
from ppmd.forces import CPUExactForceCalculator



class SimSystem(object):

	def __init__(self, gcomm, in_file, units):
		#set simulation parameters
		self._sim_params = GlobalParams(in_file, gcomm, gcomm.Get_rank())
		self.data_manager = DataManager(self._sim_params)
		if self._sim_params[GPK.PSCHEME] == PartitionScheme.NONE:
			self.loc_bbox = self._sim_params[GPK.BBOX]
		elif self._sim_params[GPK.PSCHEME] == PartitionScheme.GRID: 
			self.loc_bbox = self.init_fixed_grid(gcomm)
		elif self._sim_params[GPK.PSCHEME] == PartitionScheme.TREE:
			pass
		elif self._sim_params[GPK.PSCHEME] == PartitionScheme.FOREST:
			self.loc_bbox = self.init_fixed_grid(gcomm)
		self.loc_particles = self.init_particles(gcomm)
		self.data_manager.write_data(gcomm, self._sim_params, self.loc_bbox, self.loc_particles)

	def init_fixed_grid(self, gcomm):
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

	def init_particles(self, gcomm):
		if self._sim_params[GPK.PIC][0] == ParticleIC.CUSTOM:
			loc_particles = Particles.from_custom(gcomm, self._sim_params)
			self._sim_params[GPK.NSPEC] = loc_particles.ms.shape[0]
			loc_npart = [loc_particles.ids.shape[0]]
			gcomm.allreduce(loc_npart)
			self._sim_params[GPK.NPART] = loc_npart[0]
			return loc_particles
		elif self._sim_params[GPK.PIC][0] == ParicleIC.RESTART:
			pass
		

	def step(self, gcomm, units):
		self.loc_particles.integrate_vhalf()
		self.loc_particles.integrate_pos()
		if self._sim_params[GPK.SBTYPE] == SpatialBoundaries.PERIODIC:
			self.loc_particles.make_periodic(self._sim_params[GPK.BBOX])
		calc_energy = self._sim_params[GPK.ENERGY]
		if calc_energy:
			calc_energy = self._sim_params[GPK.CSTEP]%self._sim_params[GPK.ENERGYF]
		if self._sim_params[GPK.FTYPE] == ForceType.EXACT:
			if self._sim_params[GPK.GPUS] == False:
				CPUExactForceCalculator.run(gcomm, self.loc_particles, units, calc_energy)	
			else:
				pass
		elif self._sim_params[GPK.FTYPE] == ForceType.FMM:
			pass
		else:
			if gcomm.Get_rank() == 0:
				print("How did you get here?!")
		self.loc_particles.integrate_vhalf()
		self.loc_particles.get_lkinetic_energy()
		self._sim_params[GPK.CSTEP] -= 1
		self.data_manager.write_data(gcomm, self._sim_params, self.loc_bbox, 
		self.loc_particles)
		