import numpy as np
from pyprimesieve import factorize
from scipy.spatial import Rectangle


class Bbox(Rectangle):

	def __init__(self, lleft, uright):
		super(Bbox, self).__init__(uright, lleft)

	def get_len(self, i):
		return self.maxes[i] - self.mins[i]

	def get_lens(self):
		return self.maxes - self.mins

	def get_lleft(self):
		return self.mins

	def get_uright(self):
		return self.maxes

	def get_center(self):
		out = self.mins + 0.5*(self.maxes-self.mins)
		return out

		
class GlobalBbox(Bbox):

	def __init__(self, comm, lleft, uright):
		super(GlobalBbox, self).__init__(lleft, uright)
		self.set_grid(comm)

	def set_grid(self, comm):
		n = comm.Get_size()
		d = len(self.mins)
		if d == 1:
			self.grid = np.array([n])
		else:
			fs = factorize(n)
			for i in range(len(fs)):
				pf = fs.pop(0)
				pf = [pf[0]]*pf[1]
				fs = fs + pf
			fs.reverse()
			while len(fs) < d:
				fs.append(1)
			self.grid = []
			for i in range(d):
				self.grid.append(fs.pop())
			while len(fs) > 0:
				li = self.grid.index(min(self.grid))
				self.grid[li] = self.grid[li]*fs.pop()
			#match the spatial dim with greatest lengths 
			#to grid dims of greatest length
			lord = self.get_lens()
			lord = lord.argsort()
			temp = sorted(self.grid)
			for i in range(len(lord)):
				self.grid[lord[i]] = temp[i]
			self.grid = np.array(self.grid)