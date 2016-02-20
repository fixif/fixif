function displayR_BOBF( st, R, Sys)
disp(st)
[add, mul]= computationalCost(R);
disp(['BO: MsensH=' num2str(MsensH(R),'%0.5g') ', MsensPole=' num2str(MsensPole(R),'%0.5g') ', RNG=' num2str(RNG(R),'%0.5g') ', ' num2str(add) '+, ' num2str(mul) 'x']) 
disp(['BF: MsensH=' num2str(MsensH_cl(R,Sys),'%0.5g') ', MsensPole=' num2str(MsensPole_cl(R,Sys),'%0.5g') ', RNG=' num2str(RNG_cl(R,Sys),'%0.5g') ', ' num2str(add) '+, ' num2str(mul) 'x']) 

