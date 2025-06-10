clear all; close all; clc

syms x1 x2 x3 u y;

x = [x1;x2;x3];

p = 20;

alfa = 0.25*(6/pi)^2;

f1 = p*u -p*x1;

f2 = x3;

f3 = -alfa*abs(x2)*x2+sin(x2)-abs(x3)*x3+x1;

f = [f1;f2;f3];

y = x2;

A = jacobian(f,x);

B = jacobian(f,u);

C = jacobian(y,x);

D = jacobian(y,u);


%equilibrio-------

x1e = -1/4;
x2e = pi/6;
x3e = 0;
ue = -1/4;
ye = pi/6;

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
Pap = zpk(0,0,1);
Pmp = P;

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

figure();
bode(P,Pap,Pmp, optionss, {.01,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

C = db2mag(172)*zpk([-20, -1,-1],[0, -445,-445,-445],1/20);

L = minreal(P*C);

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode( L, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

wgc = 4.74;

T_s = 4/(wgc/tand(4.3/2));

Pade = zpk([4/T_s],[-4/T_s],-1);

L_digit = L*Pade;

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode( L,L_digit, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

S = 1/(1+L_digit);

T = 1-S;

PS = P*S;

CS = C*S;

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

