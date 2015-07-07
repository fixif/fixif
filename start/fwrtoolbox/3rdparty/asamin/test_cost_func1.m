function [cost_value, cost_flag] = test_cost_func1 (x)
%
%  $Id: test_cost_func1.m,v 1.27 2004/10/03 03:23:06 ssakata Exp ssakata $
%

display('t')


s_i = 0.2;
t_i = 0.05;
c_r = 0.15;

q_n = 0.0;
parameter_dimension = 4;

for i = 1 : parameter_dimension,
  j = mod(i-1,4);
  switch (j)
     case 0, d_i = 1.0;
     case 1, d_i = 1000.0;
     case 2, d_i = 10.0;
     otherwise, d_i = 100.0;
  end
  if x(i) > 0.0
    k_i = fix(x(i) / s_i + 0.5);
  elseif x(i) < 0.0
    k_i = fix(x(i) / s_i - 0.5);
  else
    k_i = 0;
  end

  if abs (k_i * s_i - x(i)) < t_i
    if k_i < 0
      z_i = k_i * s_i + t_i;
    elseif k_i > 0
      z_i = k_i * s_i - t_i;
    else
      z_i = 0.0;
    end
    q_n = q_n + c_r * d_i * z_i * z_i;
  else
    q_n = q_n + d_i * x(i) * x(i);
  end
end;  
cost_value = q_n;
cost_flag=1;
