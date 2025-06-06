clear all; clc
close all;

s = tf('s');

%P = zpk(1/((s+80)*(s+4)*(s-4)*(s^2+16)));

%Pap = zpk((s+4)/(s-4));

%Pmp = zpk(1/((s+80)*(s+4)*(s+4)*(s^2+16)));

P = zpk([],[-80 +4 -4 4*i -4*i],1);

Pap = zpk(-4,4,1);

Pmp = zpk([],[-80 -4 -4*i 4*i],1);

Z = 200/tand(20/2);

Pade = zpk([Z],[-Z],-1);
% -2Atand(200/z)= -20
%tg(20/2)=200/z
%z=200/(tg(20/2))


optionss = bodeoptions;
optionss.PhaseMatching = 'on';
optionss.PhaseMatchingValue = -170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';


figure();
bode(P,Pap,Pmp,optionss,{.01,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%C = db2mag(0)*zpk((s+4)^2/s);

%C = zpk((s+4)^4*(s+80)/(s*(s+10000)^4));%pongo 4 porque le pintó a angelopulo, quiero cancelar la fase que me dan los polos en el eje jw

C = db2mag(366)*zpk([-4 -4 -4 -4 -80],[0 -10000 -10000 -10000 -10000],1);

L = minreal(P*C);

PmpC = minreal(C*Pmp);

figure();
bode(L,optionss,{.01,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend


figure();
bode(PmpC,optionss,{.01,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend

figure();
bode(Pade,optionss,{.01,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend


figure();
L_digit = L*Pade;
bode(L_digit,optionss,{.01,100000});
set(findall(gcf,'type','line'),'linewidth',2);
legend


figure();
rlocus(L);

T = feedback(L_digit,1);
E = eig(T);

