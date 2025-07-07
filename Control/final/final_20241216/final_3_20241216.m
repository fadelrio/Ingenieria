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
close all

T_s = 0.5;

Pade = zpk([4/T_s],[-4/T_s],-1);

Wgc = 4*tand(30/2)/T_s;

C = db2mag(138)*zpk([-0.02 -0.05861 -1.066],[0 -100 -100],1)*Pade;

%Para el Wgc = 2.14 obtenido por el muestreo de la digitalización, la
%ganancia es 179dB

Lmp = minreal(C*Pmp);

L = minreal(P*C);

S = 1/(1+L);

T = 1-S;

PS = P*S;

CS = C*S;

C_dig = c2d(C,T_s,'tustin');


figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(Lmp, L, optionss, {0.001,10});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
rlocus(L);
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
step(S);
legend

figure();
step(T);
legend

figure();
step(PS);
legend

figure();
step(CS);
legend