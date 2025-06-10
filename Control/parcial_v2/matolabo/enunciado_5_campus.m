clear all; close all; clc

s = tf('s');

%{

syms x1 x2 u y;

x = [x1;x2];

f1 = u - sqrt(x1-x2);
f2 = sqrt(x1-x2)-sqrt(x2);

f = [f1;f2];

y = x2; 


A = jacobian(f, x);

B = jacobian(f, u);

C = jacobian(y, x);

D = jacobian(y, u);
%}

A = [-1/2 1/2; 1/2 -1];

B = [1;0];

C = [0 1];

D = 0;

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';


[Num, Den] = ss2tf(A,B,C,D);

P = zpk(roots(Num), roots(Den), 0.5);

Pap = zpk([],[],1);

Pmp = P;

figure();
bode(P, Pap, Pmp, optionss, {.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

C = db2mag(40.2)*zpk([-0.191],[0, -60.5],1);

L = minreal(P*C);


figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode( L, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

wgc = 0.589;

T_s = round(4/(wgc/tand(5.2/2)),4);

Pade = zpk([4/T_s],[-4/T_s],-1);

L_digit = L*Pade;

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode( L_digit, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%

S = 1/(1+L_digit);

CS = C*S;

T = 1-S;

PS = P*S;


figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode( S, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(CS, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(T, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(PS, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

step_options = stepDataOptions;
step_options.StepAmplitude = .2;

figure();
step(CS,step_options);
legend

figure();
step(T);
legend

C_digit = c2d(C,T_s);

