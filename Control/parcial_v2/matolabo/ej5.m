clear all; clc 
close all; 

s = tf('s');

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

Pade = zpk([4],[-4],-1);
%{
Se me enojaron por usar esta forma, voy a ver si habia diferencia con la
forma piola.
*5 minutos despues* Al final era lo mismo, el controlador quedó igual
P = zpk(2/((s/5 +1)*(4*s+1)))*Pade;
Pmp = zpk(2/((s/5 +1)*(4*s+1)));
Pap = Pade;
%}

P = zpk([4],[-5,-4,-4],-2.5); %ya tiene el pade multiplicando

Pmp = zpk([], [-5,-4],2.5);

Pap = Pade;

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

C = db2mag(80)*inv(Pmp)/(s*(s+10000));

Lmp = minreal(C*Pmp);

L = minreal(P*C);

S = inv(1+L);

T = 1-S;

PS = minreal(P*S);

CS = minreal(C*S);

%%
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
step(T_PS); % Salida con referencia de escalon + perturbacion de entrada de escalon
legend

figure();
T_CS = S + CS;
step(T_CS); % Accion de control con referencia de escalon + perturbacion de entrada de escalon
legend

figure();
step(PS);
legend

figure();
step(CS);
legend

%%

