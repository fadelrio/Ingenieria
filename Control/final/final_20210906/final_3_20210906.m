clear all; close all; clc

syms x1 x2 u y;

x = [x1;x2];

f1 = u - sqrt(x1-x2);

f2 = sqrt(x1-x2)-sqrt(x2);

f = [f1;f2];

%%
y = x1;

A = jacobian(f,x);

B = jacobian(f,u);

C = jacobian(y,x);

D = jacobian(y,u);


%equilibrio-------

x1e = 8;
x2e = 4;
ue = 2;
ye = 8;

A = subs(A, str2sym({'x1','x2','u','y'}),{x1e,x2e,ue,ye});
B = subs(B, str2sym({'x1','x2','u','y'}),{x1e,x2e,ue,ye});
C = subs(C, str2sym({'x1','x2','u','y'}),{x1e,x2e,ue,ye});
D = subs(D, str2sym({'x1','x2','u','y'}),{x1e,x2e,ue,ye});

A_eq = double(A);
B_eq = double(B);
C_eq = double(C);
D_eq = double(D);


[Num,Den] = ss2tf(A_eq,B_eq,C_eq,D_eq);

P = zpk(ss(A_eq,B_eq,C_eq,D_eq));

%Es estable!!!

%%
s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

Pmp = P;

figure();
bode(P, Pmp, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%
close all;

wgc = 9.99;

fase = 30.9;

T_s = 4*tand(fase/2)/wgc;

Pade = zpk([4/T_s],[-4/T_s],-1);

C = db2mag(20)*zpk([],[0],1)*zpk([-0.09549],[],1);

C_simu = C;

C = C*Pade;

Lmp = minreal(C*Pmp);

L = minreal(P*C);

S = 1/(1+L);

T = 1-S;

PS = P*S;

CS = C*S;


figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(Lmp, L, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
rlocus(L);
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%
close all;

figure();
step(S);
legend

figure();
step(T);
legend

figure();
T_PS = T + PS;
step(T_PS); % Salida con referencia de escalón + perturbacion de entrada de escalón
legend

figure();
T_CS = S + CS;
step(T_CS); %Acción de control con referencia de escalon + pertubacion de entrada escalón
legend

figure();
step(PS);
legend

figure();
step(CS);
legend
