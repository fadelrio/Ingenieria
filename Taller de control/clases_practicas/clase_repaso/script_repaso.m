close all; clear all; clc;

syms L L2 l h l1 l2 u real

L2 = simplify( solve( (L+L2)/l2 == L2/l1, L2 ) );
l =  simplify( solve( (h+L2)/l  == L2/l1, l  ) );

params = [sym('0.10') sym('0.40') sym('0.90')];

L2 = subs(L2, [l1 l2 L], params);
l  = subs(l,  [l1 l2 L], params);

V = simplify( ( ((h + L2)/3) * l^2 ) - ( (L2/3) * l1^2 ) );
Vdot = simplify( diff(V, h) )

g = sym('9.8');
d = sym('0.01065');
A = sym(pi) * (d/2)^2 * u;
Qo = sqrt(2*g*h) * A;
Qi = sym(1)/7500;

hdot = simplify( (Qi - Qo) / Vdot )
%%
h0 = sym('0.45');
u0 = subs( solve( hdot == 0, u ), h, h0 )

A = double( subs( jacobian(hdot, h), [h u], [h0 u0] ) )
B = double( subs( jacobian(hdot, u), [h u], [h0 u0] ) )
C = 1;
D = 0;

P = tf( ss(A, B, C, D) )

figure();

legs = [];

for h0 = [.1,.2,.3,.4,.5,.6,.7,.8]
    
    u0 = subs( solve( hdot == 0, u ), h, h0 );
    A = double( subs( jacobian(hdot, h), [h u], [h0 u0] ) );
    B = double( subs( jacobian(hdot, u), [h u], [h0 u0] ) );
    C = 1;
    D = 0;

    P = tf( ss(A, B, C, D) );
    bode(P);
    set(findall(gcf,'type','line'),'linewidth',1.5);
    
    legs = [legs;sprintf('h0 = %.2f', h0)];
    hold on
end
legend(legs);
grid();
hold off

h0 = sym('0.45');
u0 = subs( solve( hdot == 0, u ), h, h0 );

A = double( subs( jacobian(hdot, h), [h u], [h0 u0] ) );
B = double( subs( jacobian(hdot, u), [h u], [h0 u0] ) );
C = 1;
D = 0;

P = tf( ss(A, B, C, D) );

u0 = double(u0);
h0 = double(h0);
Qi = double(Qi);

%%
%looshafin
close all;

optionss=bodeoptions;
%optionss.MagVisible='off';
optionss.PhaseMatching='on';
optionss.PhaseMatchingValue=-170;
optionss.PhaseMatchingFreq=.0001;
optionss.Grid='on';

Cont = db2mag(-24)*zpk([-0.00237],[0 -0.02],-1);

L = minreal(P*Cont);

figure();

bode(L, optionss);
legend

S = 1/(1+L);
T = 1-S;

figure();
step(T);
    


%Simulink de el sistema controlado pasando del equilibrio a un nivel de
%0.35 mts y de el equilibrio a un nivel de 0.55 mts