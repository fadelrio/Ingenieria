close all; clear all; clc;

%% Constantes
k = 1.3806e-23; % [J/K] Constante del Boltzmann
q = 1.60223e-19; % [C] Carga del electron
T = 300; % [K] Temperatura de trabajo
vth = k*T/q; % [V] Tensión termica
line_width = 1.5;

%nombres de archivos

archivo_ic_transferencia = "Simulacion transferencia Ic.txt";
archivo_ib_transferencia = "Simulacion transferencia Ib.txt";
archivo_ic_salida = "Simulacion salida Ic.txt";

%lectura de archivos

data_ic_transf = dlmread(archivo_ic_transferencia, '\t', 1, 0);

data_ib_transf = dlmread(archivo_ib_transferencia, '\t', 1, 0);

data_ic_salida = dlmread(archivo_ic_salida, '\t', 1, 0);

%extracción de datos


vbe_transf = data_ib_transf(:, 1);

ib_transf = data_ib_transf(:, 2);

ic_transf = data_ic_transf(:, 2);

vce_salida = data_ic_salida(:, 1);

ic_salida = data_ic_salida(:, 2);

log_ic_transf = log(abs(ic_transf));

%graficos crudos

%ib transf
##figure();
##plot(vbe_transf, 1e3*ib_transf, 'b', 'LineWidth', line_width);
##title("ib transf");
##grid minor
##ylabel('Corriente [mA]');
##xlabel('Tension [V]');

%ic transf
##figure();
##plot(vbe_transf, 1e3*ic_transf, 'b', 'LineWidth', line_width);
##title("ic transf");
##grid minor
##ylabel('Corriente [mA]');
##xlabel('Tension [V]');

%ajuste curva de salida

vmin_ajuste_salida = -4;
vmax_ajuste_salida = -0.4;

indices_ajuste_salida = (vce_salida > vmin_ajuste_salida) & (vce_salida < vmax_ajuste_salida);

vce_ajuste_salida = vce_salida(indices_ajuste_salida);
ic_ajuste_salida = ic_salida(indices_ajuste_salida);

coef_ajuste_salida = polyfit(vce_ajuste_salida, ic_ajuste_salida, 1);

va_ajustado = -coef_ajuste_salida(2)/coef_ajuste_salida(1);

ic_salida_ajustada = coef_ajuste_salida(1)*vce_salida + coef_ajuste_salida(2);

vce_sat = -0.24

%ic salida
figure();
plot(vce_salida, 1e3*ic_salida, 'b', 'LineWidth', line_width);
hold on
plot(vce_ajuste_salida, 1e3*ic_ajuste_salida, 'r', 'LineWidth', line_width);
hold on
plot(vce_salida, 1e3*ic_salida_ajustada, '--g', 'LineWidth', line_width);
hold on
line([vce_sat vce_sat], [-2 0.5], "linestyle", "--", "color", "m", "LineWidth", line_width);
##title("ic salida");
grid minor
ylabel('Corriente [mA]');
xlabel('Tension [V]');
legend('I_C simulada', 'Valores de I_C tomados para el ajuste', ['Curva ajustada. V_A = ' num2str(va_ajustado) ' V'],['V_{CE(sat)} = ' num2str(vce_sat) ' V'],"location", "northwest")

%graficos logaritmicos y ajuste de is

vMin = -0.59; % Valor minimo del rango (en volts)
vMax = -0.4; % Valor maximo del rango (en volts)

indicesAjuste = (vbe_transf > vMin) & (vbe_transf < vMax);

vbe_ajuste = vbe_transf(indicesAjuste);
ic_ajuste = ic_transf(indicesAjuste);
log_ic_ajuste = log_ic_transf(indicesAjuste);

coefAjuste = polyfit(vbe_ajuste, log_ic_ajuste, 1);

% Calculo la corriente del diodo usando los parametros ajustados y el modelo exponencial
logIS = coefAjuste(2);
IS = exp(logIS); % Corriente de saturación en inversa
vth_ajuste = -1/coefAjuste(1);% pendiente
ic_ajustada = IS*exp(-vbe_transf/vth);



%ic transf
figure();
semilogy(vbe_transf, abs(ic_transf), 'b', 'LineWidth', line_width);
hold on;
plot(vbe_transf, abs(ib_transf), 'm', 'LineWidth', line_width);
hold on
plot(vbe_ajuste, abs(ic_ajuste), 'r', 'LineWidth', line_width);
hold on
plot(vbe_transf, abs(ic_ajustada), '--g', 'LineWidth', line_width)
grid minor
##title("ic transf log");
ylabel('Corriente [A]');
xlabel('Tension [V]');
legend('I_C simulada', 'I_B simulada', 'Valores de I_C tomados para el ajuste', ['Curva ajustada. I_S = ' num2str(IS) ' A'])
%ylim([1e-15 1]);

%ajuste ic/ib

vMin_beta = -0.68; % Valor minimo del rango (en volts)
vMax_beta = -0.58; % Valor maximo del rango (en volts)

indicesAjuste_beta = (vbe_transf > vMin_beta) & (vbe_transf < vMax_beta);
vbe_ajuste_beta = vbe_transf(indicesAjuste_beta);
ic_ajuste_beta = ic_transf(indicesAjuste_beta);
ib_ajuste_beta = ib_transf(indicesAjuste_beta);

coefAjuste_beta = polyfit(vbe_ajuste_beta,ic_ajuste_beta./ib_ajuste_beta , 0);

beta_ajustado = coefAjuste_beta(1);

ic_ib_grafico = ic_transf./ib_transf;

ic_ib_ajuste_grafico = ic_ajuste_beta./ib_ajuste_beta;


% ic/ib
figure();
plot(vbe_transf, ic_ib_grafico, 'b', 'LineWidth', line_width);
hold on
plot(vbe_ajuste_beta, ic_ib_ajuste_grafico, 'r', 'LineWidth', line_width);
hold on
line([-0.8 -0.4], [beta_ajustado beta_ajustado], "linestyle", "--", "color", "g", "LineWidth", line_width);
grid minor
%title("ic/ib transf");
ylabel('\beta');
xlabel('Tension [V]');
legend( 'I_C/I_B simulados', 'Valores de I_C/I_B tomados para el ajuste', ['Curva ajustada. \beta = ' num2str(beta_ajustado)], "location", "south")

