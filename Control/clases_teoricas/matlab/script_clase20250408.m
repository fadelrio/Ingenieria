s = tf('s');
Pzpk = zpk([-1,1],[-2,2],12)
C = (s+1)/2
S = 1/(1+Pzpk*C)
%clear all; clc; close all; %para borrar todo lo guardado en memoria
S = minreal(1/(1+Pzpk*C))
S = minreal(feedback(1,Pzpk*C))
