clear all; clc 
close all; 

s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

P = zpk([50 50],[1 1],1);
Pmp = zpk([-50 -50],[-1 -1],1);

Pap1 = zpk([50 50],[-50 -50],1);
Pap2 = zpk([-1 -1],[1 1],1);
Pap = Pap1*Pap2;

% El menor retraso de fase que me da el Pap es de -64.4 a frecuencia 7
% rad/s. Eso me da un margen de fase máximo de 180-90-64.4 = 25.5°

figure();
bode(Pap, Pap1, Pap2, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
bode(P, Pmp, Pap, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%
    
C = db2mag(17)*zpk([],[0],1)*inv(Pmp);

%Int 1: cancelo toda la Pmp y agrego acción integral (Estuve un rato xq había escrito mal la planta. Como siempre, soy re gil)
%La ganancia para que mi wgc esté en 7 rad/s es de 17dB
%como se esperaba, el margen de fase es de 25.6°

Lmp = minreal(C*Pmp);

L = minreal(P*C);

S = 1/(1+L);

T = 1-S;

PS = P*S;

CS = C*S;


figure();
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=20;
bode(Lmp, L, optionss, {0.1,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
rlocus(L);
set(findall(gcf,'type','line'),'linewidth',2);
legend

% También me pide el margen de estabilidad, para eso tengo que graficar el
% bode de S

figure();
bode(S, optionss, {0.1, 1000000});
set(findall(gcf,'type','line'),'linewidth',2);

% Margen de estabilidad:

S_m = 1/db2mag(7.46);

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