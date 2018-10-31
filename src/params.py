"""Various enums and dicts to define the meta-state of a simulation."""

from enum import Enum 


class RefineCriteria(Enum):
	NONE = 0
	MAX_DEPTH = 1
	MAX_DENS = 2
	MAX_LENGTH = 3


class ForceType(Enum):
	EXACT = 0
	FMM = 1


class GlobalParams(dict):
	






