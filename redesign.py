import numpy as np
from numpy import cos, sin, radians, degrees, arctan
import matplotlib.pyplot as plt

class Redesign:

	def __init__(self, filename, ref=None):
		self.filename 	= filename
		self.Cn 		= self.load_pert(self.filename)
		self.dP_dphi 	= self.gen_dP_dphi()
		self.ref 		= ref
		self.phis 		= np.arange(0,361, 1)
		self.alfa_stars = degrees(self.astar(radians(self.phis)))
		# This handles the mod operator in eq 9 : cos(|phi/2 - alpha|)
		self.alfa_stars[self.alfa_stars>90] -= 180

		self.redesign()

	def load_pert(self, filename):
		"""
		Loads Fourier coeificients from pert file. 
		This file can be generated from XFoil - MDES-> Pert
		Zeroth coeifficient has to be added in, complying Lighthill constraints
		ie: a0, b0 = 0
		"""
		Cn = np.loadtxt(filename, skiprows=2, usecols=(1,2))
		Cn = np.insert(Cn, 0, [0., 0.], axis=0)
		return Cn

	def gen_dP_dphi(self):
		"""
		creates function dP(phi)/d_phi of Eq 9 of NASA TM 80210
		derivation can be found in the docs
		"""
		return lambda phi: sum([(m*bm*cos(m*phi) - m*am*sin(m*phi)) 
								for m,(am, bm) in enumerate(self.Cn)])

	def astar(self, phi):
		"""
		retuns alfa* from P' and phi.
		derivation can be found in the docs
		"""
		return (phi/2) - arctan(-2* self.dP_dphi(phi))

	def redesign(self):
		fig, ax = plt.subplots()

		ax.plot(self.phis/6, self.alfa_stars, label="Calculated", lw=1)

		if self.ref:
			x,y = np.array(self.ref).T
			ax.plot(x,y ,'o', color='red', markersize=2, label="Ref")
			ax.plot(x,y , color='red', lw=1)

		ax.set_title(self.filename)
		ax.set_xlabel("Nu")
		ax.set_ylabel("Alpha* [deg]")
		ax.invert_xaxis()
		ax.grid()
		ax.legend(frameon=False)
		plt.show(block=False)

if __name__ == "__main__":

	e587_ref =  [[12.5000,-15.92], [14.5000, -6.42], [16.5000,  1.08], [18.5000,  5.58], [20.5000,  7.08], [22.5000,  8.28], 
				 [24.5000,  9.48], [26.5000, 10.68], [28.5000, 11.88], [30.5000, 12.88], [32.5155, 13.58], [34.5000,  3.70], 
				 [36.5000,  4.50], [42.5000,  5.20], [44.5000,  4.90], [46.5000,  4.60], [48.5000, 17.00], [60.0000,  6.00]]

	r = Redesign("E587.pert", e587_ref)
	# r = Redesign("NLF1015.pert")
	