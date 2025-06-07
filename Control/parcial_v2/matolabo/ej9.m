clear all; clc 
close all; 

s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

%frecuencia de cruce: 77.9 rad/s, margen para Pade: 19.2°

T_s = 0.0085;

Pade = zpk([4/T_s],[-4/T_s],-1);

P = zpk([],[4,-4,-80],80);
Pmp = zpk([],[-4,-4,-80],80);
Pap = zpk([-4],[4],1);

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

%busco frecuencia de cruce 18 rad/s. Al hacer propio el controlador me pasó
%a 19 rad/s

%puedo ir de 116dB a 138dB

%con los 130dB estoy piola con el overshoot

%ahora recalculo el pade y me fijo que pasa con el overshu

%funca, chetou

C = db2mag(130)*zpk([-4, -4, -80],[0,-1800,-1800],1);

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

L_Pade = L*Pade;

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(L,L_Pade , optionss, {0.1,100000});
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
step(T,5);
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