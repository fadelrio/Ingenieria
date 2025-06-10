

A = [-1/64 1/16; 0 -4];

B = [0; 4];

C = [-3/64 0];

D = 0;

[Num,Den] = ss2tf(A,B,C,D);


clear all; clc 
close all; 

s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

P = zpk([],[-4, -0.0156],-0.0117);
Pmp = zpk([],[-4, -0.0156],-0.0117);
Pap = zpk(0,0,1);

T_s = 0.1036;

Pade = zpk([4/T_s],[-4/T_s],-1);

%{
Pap1 = zpk(0,0,0);
Pap2 = zpk(0,0,0);
Pap = Pap1*Pap2;

figure();
bode(Pap, Pap1, Pap2, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%}

figure();
bode(P, Pmp, Pap, optionss, {0.001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%
close all;

C = db2mag(18.1)*zpk([-0.0156],[0],-1/0.0117);

C_digit = c2d(C, T_s,'tustin');

Lmp = minreal(C*Pmp);

L = minreal(P*C*Pade);

S = 1/(1+L);

T = 1-S;

PS = P*S;

CS = C*S;


figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(Lmp, L, optionss, {0.00001,10});
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