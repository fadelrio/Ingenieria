clear all;close all; clc


A = [1 1 -2; 0 1 1; 0 0 1];

B = [1; 0; 1];

C = [2 0 0];

D = 0;

pol_car = charpoly(A);

raices_buscadas = [-2 -1+1j -1-1j];

pol_buscado = poly(raices_buscadas);

a1 = pol_car(2);
a2 = pol_car(3);
a3 = pol_car(4);

p1 = pol_buscado(2);
p2 = pol_buscado(3);
p3 = pol_buscado(4);

W_r = [B A*B A*A*B];

W_r_monio = inv([1 a1 a2; 0 1 a1; 0 0 1]);

K = [p1-a1 p2-a2 p3-a3]*W_r_monio/W_r;

K_r = -inv([C*inv(A-B*K)*B]);
