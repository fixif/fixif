%Purpose:
% Set of options for the ASA algorithm (through asamin)
%
%Syntax:
%	myoptions_asamin
%
%Parameters:
%
% $Id: mesoptions_asamin.m 27 2006-03-31 01:07:52Z thib $


asamin('reset');
asamin('set','rand_seed', round(now*1e5));
%asamin('set','asa_out_file','R_opt.log');
asamin('set','test_in_cost_func',0);

asamin('set','limit_acceptances',1e6);           %10000
asamin('set','limit_generated',1e6);             %9999
asamin('set','limit_invalid',1e6);               %10000
asamin('set','accepted_to_generated_ratio',1e-12);   %1e-6

asamin('set','cost_precision',1e-18);               %1e-18
asamin('set','maximum_cost_repeat',5);             %5
asamin('set','number_cost_samples',5);             %5
asamin('set','temperature_ratio_scale',1e-8);       %1-e4
asamin('set','cost_parameter_scale_ratio',1);       %1
asamin('set','temperature_anneal_scale',100);       %100

asamin('set','user_initial_parameters',1);          %1
asamin('set','sequential_parameters',-1);           %-1
asamin('set','initial_parameter_temperature',1e0);    %1

asamin('set','acceptance_frequency_modulus',1e2);   %100        %1e8
asamin('set','generated_frequency_modulus',1e4);  %1000         %1e10
asamin('set','reanneal_cost',1);
asamin('set','reanneal_parameters',1);

asamin('set','delta_x',0.001);

%Description:
%	One can change this script and put its preferred parameters.\\
%	It is important to remark that these parameters could, of course,
%	be passed to asamin through the options of the
%	\funcName[@FWS/optim]{optim} method

%See also: <@FWS/optim>