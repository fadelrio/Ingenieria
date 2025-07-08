close all;

W_o = ctrb(A_eq,B_eq);

rango = rank(W_o);

pol_car = charpoly(A_eq);

raices = roots(pol_car);

%K = acker(A_eq,B_eq,[-10 -10 -10]); sin control integral

%Con control integral

A_amp = [A_eq zeros(3,1); -C_eq 0];

B_amp = [B_eq;-D_eq];

K_amp = acker(A_amp,B_amp,[-5 -5 -5 -5]);

K = K_amp(1:3);

K_i = -K_amp(end);

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

%formula para multiplicidad multiple 
% wgc = sqrt(p*z)
%fase_pap = n(2atan(wgc/z)+2tan(P/wgc))180/pi
%n es la multiplicidad 

%L = Wo^-1*Wom*Lm
%Wo = [C ; CA]
%Wom = [1 0 0; a1 1 0; a2 a1 1]^-1
%Lm =[p1 -a1; p2-a2]

%K = Km*Wrm*Wr^-1

%Wrm = [B AB ...]
%Wrm =[1 a1 a2; 0 1 a1]^-1