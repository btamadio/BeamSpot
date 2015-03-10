#!/usr/bin/env python

#Author: Brian Amadio
#email: btamadio@lbl.gov

#This class is used to determine the z-t distribution of collisions 
#Assumptions:
#Centered gaussian bunches, whose x and y components fully factorize
#Beam crossing angle = 0
#Centers of bunches coincide at z=0,t=0
#Both 1D and 2D functions are normalized over all z,t

#Example usage:
#a = timeCalc(0.01,0.05)
#a.get1D(0.01).Draw()

import os,sys
from ROOT import *
from math import *

class timeCalc:
    #sigmaZ1 is the width of the bunch moving in the positive z-direction
    def __init__(self,sigmaZ1,sigmaZ2):
        self._sigmaZ1 = sigmaZ1
        self._sigmaZ2 = sigmaZ2
        self._c = 299792458.
        self._zMin = -2*(sigmaZ1+sigmaZ2)
        self._zMax = 2*(sigmaZ1+sigmaZ2)
        self._tMin = self._zMin/self._c
        self._tMax = self._zMax/self._c
        self._func2 = TF2("func","[0]*exp((-(x-299792458*y)^2*[2]^2-(x+299792458*y)^2*[1]^2)/(2*[1]^2*[2]^2))",self._zMin,self._zMax,self._tMin,self._tMax)
        self._func2.SetParameter(0,self._c/(pi*sigmaZ1*sigmaZ2))
        self._func2.SetParameter(1,sigmaZ1)
        self._func2.SetParameter(2,sigmaZ2)
        self._func1 = TF1("func","[0]*exp((-([3]-299792458*x)^2*[2]^2-([3]+299792458*x)^2*[1]^2)/(2*[1]^2*[2]^2))",self._tMin,self._tMax)
        self._func1.SetParameter(0,self._c/(pi*sigmaZ1*sigmaZ2))
        self._func1.SetParameter(1,sigmaZ1)
        self._func1.SetParameter(2,sigmaZ2)
        self._func1.SetParameter(3,0)
        
    def get2D(self):
        return self._func2

    def get1D(self,z):
        self._func1.SetParameter(3,z)
        return self._func1

