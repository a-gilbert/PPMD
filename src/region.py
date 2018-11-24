import numpy as np


class Bbox(object):

	def __init__(self, lleft, uright):
		super(Bbox, self).__init__()
		self.val = np.array([lleft, uright])

	def get_len(self, i):
		return self.val[1][i] - self.val[0][i]

	def get_volume(self):
		return np.prod(self.val[1]-self.val[0])

	def get_lleft(self):
		return self.val[0]

	def get_uright(self):
		return self.val[1]

	def get_center(self):
		out = self.val[0] + 0.5*(self.val[1]-self.val[0])
		return out