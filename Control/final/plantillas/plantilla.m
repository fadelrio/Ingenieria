clear all; clc 
close all; 

s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

P = zpk(0,0,0);
Pmp = zpk(0,0,0);
Pap = zpk(0,0,0);

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
bode(P, Pmp, Pap, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%

C = db2mag(0)*zpk(0,0,0);

Lmp = minreal(C*Pmp);

L = minreal(P*C);

S = 1/(1+L);

T = 1-S;

PS = P*S;

CS = C*S;


figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(Lmp, L, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
rlocus(L);
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%

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