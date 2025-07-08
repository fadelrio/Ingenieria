clear all; close all; clc

syms x1 x2 x3 u y;

x = [x1;x2;x3];


m = 1600;
T_m = 190;
w_m = 420;
beta = 0.4;
g = 9.8;
C_r = 0.01;
ro = 1.3;
C_d = 0.32;
A_var = 2.4;
tita = 4;
alfa_n = 12;
w_n = 2*pi;

f1 = (alfa_n/m)*x2*T_m*(1-beta*((alfa_n*x1)/w_m)^2)-g*sind(tita)-g*C_r-(1/(2*m))*ro*C_d*A_var*x1^2;

f2 = x3;

f3 = (w_n)^2*u-2*w_n*x3-(w_n)^2*x2;

f = [f1;f2;f3];

y = x1;

A = jacobian(f,x);

B = jacobian(f,u);

C = jacobian(y,x);

D = jacobian(y,u);

%equilibrio

x1e =20;

x2e =(m*(g*sind(tita)+g*C_r+(1/(2*m))*ro*C_d*A_var*x1e^2))/(alfa_n*T_m*(1-beta*(((alfa_n*x1e)/w_m)-1)^2));

x3e =0;

ye =x1e;

ue =x2e;

%%

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

%P = V(s)/Û(s) resulta una planta inestable, ya que tiene un polo en el
%semiplano derecho.


s = tf('s');
Pmp = P;

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.1;
optionss.Grid='on';

figure();
bode(P, Pmp, optionss, {0.0001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%
close all;

wgc = 0.0697;

fase_ts = 28.3;

T_s = 4*tand(fase_ts/2)/wgc;

Pade = zpk([4/T_s],[-4/T_s],-1);

C = db2mag(-5)*zpk([-0.02526],[-10 0],1);

%Para el controlador primero cancelo el polo más pequeño, ya que me
%interfiere con la dinamica que necesito para cumplir con las pautas de
%diseño (especialmente con la cota de la acción de control), luego ajusto
%la ganancia para cumplir con dicha cota, y finalmente ajusto el T_s,
%dandole la fase que me falta para llegar a los 60° de margen de fase. Mas
%adelante en el codigo se grafican los step() de T y U, para un primer
%ajuste de el controlador, pero el último ajuste se realizó con el
%Simulink. Cabe destacar que a la hora de diseñar se le dió más prioridad a
%la cota de U que a el tiempo de establecimiento, ya que, teniendo en
%cuenta el modelo fisico, resulta más importante no romper el actuador que
%tener una respuesta rápida.
%Para el cambio de angulo, en el simulink se tomó a tita como una entrada
%mas del sistema, y se agregó un escalón de entrada para pasar de 4° a 5°
%de inclinación. Este tipo de perturbación es una perturbación de entrada
%de escalón y es rechazada por el controlador, ya que cuenta con acción
%integral. (Se puede ver cambiando de posición los switches)

C_dig = c2d(C,3.4709,'tustin');
C_pade = C*Pade;

L = minreal(P*C);

L_pade = L*Pade;

figure();
bode(L, L_pade, optionss, {0.0001,100});
set(findall(gcf,'type','line'),'linewidth',2);
legend

%%
%chequeo las respuestas al escalón, para ver el tiempo de establecimiento

S=1/(1+L_pade); 
T=1-S; 
PS=minreal(P*S); 
CS=minreal(C*S); 

step_options = stepDataOptions('StepAmplitude',4);

figure();
step(T,step_options);
set(findall(gcf,'type','line'),'linewidth',2);
legend

%Sé que la transferencia U/Û es: w_n^2/(s+w_n)^2

U_u = zpk([],[-w_n -w_n],w_n^2);

%Se que la transferencia Û/R es C*S, entonces, para ver la transferencia
%U/R evalúo U_u*C*S

U = CS*U_u;

figure();
step(U,100,step_options);
set(findall(gcf,'type','line'),'linewidth',2);
legend

