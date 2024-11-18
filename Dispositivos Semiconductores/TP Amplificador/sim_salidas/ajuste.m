


close all;
clear all;
clc;




k0      = 2.0;    % Valor inicial para el parámetro k.
vt0     = 4.0;    % Valor inicial para el parámetro VT.
lambda0 = 0.1;    % Valor inicial para el parámetro Lambda.
vdd     = 9.0;    % Tensión VDD utilizada en la fuente.
min_vt  = 1.0;    % Máximo valor posible que se espera para VT,
                  % debe ser menor que VDD.

delimiter = '\t'; % Caracter utilizado para separar valores en
                  % los archivos .csv

% Nombres de los archivos con los datos en el siguiente orden:
% 1. Tensiones vgs (en orden: vgs1, ..., vgs6)
% 2. Tensiones vds e id para la vgs1 (id=id1= 50uA)
% 3. Tensiones vds e id para la vgs2 (id=id2=100uA)
% 4. Tensiones vds e id para la vgs3 (id=id3=150uA)
% 5. Tensiones vds e id para la vgs4 (id=id4=200uA)
% 6. Tensiones vds e id para la vgs5 (id=id5=250uA)
% 7. Tensiones vds e id para la vgs6 (id=id6=300uA)
file_vgs_list = 'sim_vgs.csv';
file_vds_id_1 = 'sim_salida_vgs1.csv';
file_vds_id_2 = 'sim_salida_vgs2.csv';
file_vds_id_3 = 'sim_salida_vgs3.csv';
file_vds_id_4 = 'sim_salida_vgs4.csv';
file_vds_id_5 = 'sim_salida_vgs5.csv';
file_vds_id_6 = 'sim_salida_vgs6.csv';









vgs_list = dlmread(file_vgs_list, delimiter, 1, 0);
vds_id_1 = dlmread(file_vds_id_1, delimiter, 2, 0);
vds_id_2 = dlmread(file_vds_id_2, delimiter, 2, 0);
vds_id_3 = dlmread(file_vds_id_3, delimiter, 2, 0);
vds_id_4 = dlmread(file_vds_id_4, delimiter, 2, 0);
vds_id_5 = dlmread(file_vds_id_5, delimiter, 2, 0);
vds_id_6 = dlmread(file_vds_id_6, delimiter, 2, 0);

vgs1 = ones(size(vds_id_1)(1), 1)*vgs_list(1);
vgs2 = ones(size(vds_id_2)(1), 1)*vgs_list(2);
vgs3 = ones(size(vds_id_3)(1), 1)*vgs_list(3);
vgs4 = ones(size(vds_id_4)(1), 1)*vgs_list(4);
vgs5 = ones(size(vds_id_5)(1), 1)*vgs_list(5);
vgs6 = ones(size(vds_id_6)(1), 1)*vgs_list(6);

data1 = [vgs1, vds_id_1];
data2 = [vgs2, vds_id_2];
data3 = [vgs3, vds_id_3];
data4 = [vgs4, vds_id_4];
data5 = [vgs5, vds_id_5];
data6 = [vgs6, vds_id_6];

data = [data1; data2; data3; data4; data5; data6];

params0 = [k0, vt0, lambda0];



function id = id_mosfet(vgs, vds, k, vt, lambda_)
  vdssat = vgs-vt;
  id_corte = 0.0;
  id_triodo = 2.0 * k * (vgs - vt - vds/2.0) * vds * (1.0 + lambda_ * vds);
  id_sat = k * ((vgs-vt)^2.0) * (1.0 + lambda_ * vds);

  if vgs <= vt
    id = id_corte;
    return
  end

  if vds <= vdssat
    id = id_triodo;
    return
  end

  id = id_sat;

end




function error_ = mse(k, vt, lambda_, vgs_vec, vds_vec, id_vec, min_vt)

  id_error_list = [];
  %for vgs, vds, id_real in zip(vgs_vec, vds_vec, id_vec):
  for i = 1:length(id_vec)
    vgs = vgs_vec(i);
    vds = vds_vec(i);
    id_real = id_vec(i);
    id_calc = id_mosfet(vgs, vds, k, vt, lambda_);
    id_error = (id_calc - id_real);
    if vds < vgs-min_vt
      continue
    end
    id_error_list = [id_error_list id_error];
  end

  error_ = mean(id_error_list.^2);

end





options = optimset(        'Display'    , 'off');
options = optimset(options,'TolX'       , 1e-10);
options = optimset(options,'TolFun'     , 1e-10);
options = optimset(options,'MaxIter'    , 10000);
options = optimset(options,'MaxFunEvals', 10000);
for i = 1:3
  objective_function = @(params) mse(params(1), params(2), params(3),
                                     data(:,1), data(:,2), data(:,3),
                                     min_vt);
  params = fminsearch(objective_function, params0, options);
  k = params(1);
  vt = params(2);
  lambda_ = params(3);
  str = sprintf("%d: k = %f; V_T = %f; Lambda = %f", i, k, vt, lambda_);
  disp(str)
  min_vt = vt - 0.1;
end

str = sprintf("Los parámetros finales son:\n-> k = %f;\n-> V_T = %f;\n-> Lambda = %f;", k, vt, lambda_);
disp(str)


%figure();
%hold on;
%grid on;
%vds = vdd;
%vgs_vec = linspace(0.0,vdd,50);
%id_vec = [];
%for i = 1:length(vgs_vec)
%  vgs = vgs_vec(i);
%  vds = vgs;
%  id_vec = [id_vec id_mosfet(vgs, vds, k, vt, lambda_)];
%end
%plot(vgs_vec, id_vec);
%id_vec = [];
%for i = 1:length(vgs_vec)
%  vgs = vgs_vec(i);
%  id_vec = [id_vec id_mosfet(vgs, vds, k, vt, lambda_)];
%end
%plot(vgs_vec, id_vec)
%xlabel('V_{GS}')
%ylabel('I_D')





figure();
hold on;
grid();
step1 = max(floor(length(data1(:,1))/50), 1);
step2 = max(floor(length(data2(:,1))/50), 1);
step3 = max(floor(length(data3(:,2))/50), 1);
step4 = max(floor(length(data4(:,2))/50), 1);
step5 = max(floor(length(data5(:,2))/50), 1);
step6 = max(floor(length(data6(:,2))/50), 1);
plot(data1(1:step1:end,2), data1(1:step1:end,3), 'x')
plot(data2(1:step2:end,2), data2(1:step2:end,3), 'x')
plot(data3(1:step3:end,2), data3(1:step3:end,3), 'x')
plot(data4(1:step4:end,2), data4(1:step4:end,3), 'x')
plot(data5(1:step5:end,2), data5(1:step5:end,3), 'x')
plot(data6(1:step6:end,2), data6(1:step6:end,3), 'x')
vds_vec = linspace(0.0,vdd,50);
for i = 1:length(vgs_list)
  vgs = vgs_list(i);
  id_vec = [];
  for j = 1:length(vds_vec)
    vds = vds_vec(j);
    id_vec = [id_vec id_mosfet(vgs, vds, k, vt, lambda_)];
  end
  plot(vds_vec, id_vec);
end
xlabel('V_{DS}')
ylabel('I_D')
legends = {};
legends = {legends{:}, 'Simulacioens I_{D1}'};
legends = {legends{:}, 'Simulacioens I_{D2}'};
legends = {legends{:}, 'Simulacioens I_{D3}'};
legends = {legends{:}, 'Simulacioens I_{D4}'};
legends = {legends{:}, 'Simulacioens I_{D5}'};
legends = {legends{:}, 'Simulacioens I_{D6}'};
legends = {legends{:}, 'Curva Teórica I_{D1}'};
legends = {legends{:}, 'Curva Teórica I_{D2}'};
legends = {legends{:}, 'Curva Teórica I_{D3}'};
legends = {legends{:}, 'Curva Teórica I_{D4}'};
legends = {legends{:}, 'Curva Teórica I_{D5}'};
legends = {legends{:}, 'Curva Teórica I_{D6}'};
legend(legends)




