from math import *

def cosine_Interpolate(pos,mu):
	mu2 = (1-cos(mu*pi))/2
	return(pos[0]*(1-mu2)+pos[1]*mu2)
