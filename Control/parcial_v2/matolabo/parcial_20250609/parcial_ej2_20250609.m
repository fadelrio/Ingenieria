clear all; close all; clc

syms x1 x2 x3 u y;

x = [x1;x2;x3];

p = 1000;

alfa = sin(pi/4)/(pi/4)^3;

f1 = -p*x1+p*u;

f2 = x3;

f3 = -alfa*x2^3+sin(x2)-x3+x1;

f = [f1;f2;f3];

%%
y = x2;

A = jacobian(f,x);

B = jacobian(f,u);

C = jacobian(y,x);

D = jacobian(y,u);


%equilibrio-------

x1e = 0;
x2e = pi/4;
x3e = 0;
ue = 0;
ye = x2e;

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

Pap = zpk(1);
Pmp = P;

figure();
bode(P,Pap,Pmp,optionss, {.01,10000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%

C = db2mag(214)*zpk((s^2+s+1.994)/s)*zpk([],[-10000 -10000],1);

L = minreal(C*P);

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(L, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend


L = minreal(P*C);

S = 1/(1+L);

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
step(PS);
legend

figure();
step(CS);
legend
