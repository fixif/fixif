function displayR( st, R)
disp(st)
[add, mul]= computationalCost(R);
disp([' MsensH=' num2str(MsensH(R)) ', MsensPole=' num2str(MsensPole(R)) ', RNG=' num2str(RNG(R)) ', ' num2str(add) '+, ' num2str(mul) 'x']) 

