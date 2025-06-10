clear all;close all;clc

s=tf('s');

P = zpk([],[-2 2 20 -20],1);

Pap1=zpk([-20],[20],1);
Pap2=zpk([-2],[2],1);
Pap= Pap1*Pap2;
Pmp=zpk([],[-2 -2 -20 -20],1);

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=1;
optionss.Grid='on';

figure();
bode(Pap1,Pap2,Pap,optionss,{.1,10000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
bode(Pap,P,optionss,{.1,10000});
set(findall(gcf,'type','line'),'linewidth',2);
legend
%%
%En base a Pap, buscando un retraso de fase de 25°, propongo Wgc = 100

C=db2mag(470.7)*zpk([-2 -2 -20 -20],[0 -20000 -20000 -20000 -20000 -20000],1);
L=minreal(P*C);

%Para que Wgc se encuentre en 100, se utilizó un K de db2mag(470), pero
%eligiendo este punto, el margen de fase resulta de 63.4°, por lo que se
%utiliza una ganancia levemente mayor, para obtener los 65°, para poder
%dejar los 5° planteados en un principio.
%No mecionado en parte escrita: los polos en -20000 se agregaron para que
%el controlador sea propio, el criterio fue elejir una valor que esté lo
%suficientemente alejado de mi Wgc como para que no me afecte al analisis
%previo.

% GRUPO DE LAS 4.
S=1/(1+L);
T=1-S;
PS=minreal(P*S);
CS=minreal(C*S);

%finalmente, como se especificó en la parte escrita, se calcula el T_s
%teniendo en cuenta los 5 grados dejados para este, y el Wgc;

Wgc = 107;

T_s = 4/(Wgc/tand(5/2));

Pade = zpk([4/T_s],[-4/T_s],-1);

L_digit = L*Pade;


% Bodes

optionss.MagVisible='on';
freqrange={10^-1,100000};

figure();
optionss.PhaseMatchingValue=-180;
optionss.PhaseMatchingFreq=20;
bode(L,L_digit,optionss,freqrange);title('L');
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%

figure();
bode(S,optionss,freqrange);title('S')
set(findall(gcf,'type','line'),'linewidth',2);

% S tiene un sobrepico de ganancia de 0.225dB, por lo que el margen de
% estabilidad resultará
S_m = 1/db2mag(0.225);

%S_m = 0.9744


figure();
bode(T,optionss,freqrange);title('T')
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
bode(PS,optionss,freqrange);title('PS')
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
bode(CS,optionss,freqrange);title('CS')
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%

%cambio el template para que se vea cada una en una figura, asi está mas
%grande

time=1;

%El step de T me da la salida ante un escalón de referencia
figure();
step(S,T,time);title('S & T');grid on

figure();
step(PS,5);title('PS');grid on

%El step de CS me da la acción de control ante un escalón de referencia
figure();
step(CS,0.01);title('CS');grid on
set(findall(gcf,'type','line'),'linewidth',2);

