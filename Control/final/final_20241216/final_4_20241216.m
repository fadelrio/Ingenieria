clear all; close all; clc

syms x1 x2 x3 u y;

x = [x1;x2;x3];

p = 0.02;

f1 = (x3-sqrt(x1-x2))/(x1^2);

f2 = (sqrt(x1-x2)-sqrt(x2))/(x2^2);

f3 = -p*x3+p*u;

f = [f1;f2;f3];

%%
y = x2;

A = jacobian(f,x);

B = jacobian(f,u);

C = jacobian(y,x);

D = jacobian(y,u);


%equilibrio-------

x1e = 2;
x2e = 1;
x3e = 1;
ue = -0.02;
ye = 1;

A = subs(A, str2sym({'x1','x2','x3','u','y'}),{x1e,x2e,x3e,ue,ye});
B = subs(B, str2sym({'x1','x2','x3','u','y'}),{x1e,x2e,x3e,ue,ye});
C = subs(C, str2sym({'x1','x2','x3','u','y'}),{x1e,x2e,x3e,ue,ye});
D = subs(D, str2sym({'x1','x2','x3','u','y'}),{x1e,x2e,x3e,ue,ye});

A_eq = double(A);
B_eq = double(B);
C_eq = double(C);
D_eq = double(D);


[Num,Den] = ss2tf(A_eq,B_eq,C_eq,D_eq);

P = zpk(ss(A_eq,B_eq,C_eq,D_eq));
%%

s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

figure();
bode(P, optionss, {0.001,10});
set(findall(gcf,'type','line'),'linewidth',2);
legend
%%
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
