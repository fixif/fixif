% diplay the closed-loop measure values

function disp_cl( R, Plant, MHopt, MPopt, RNGopt)

MH = MsensH_cl( R, Plant);
Mpole = MsensPole_cl( R, Plant);
Mst = Mstability( R, Plant);
MRNG = RNG_cl(R, Plant);
[Plus,Fois] = computationalCost(R);
NbOp = [ num2str(Plus) '+ ' num2str(Fois) '*'];

if nargin>2
    MTO = TradeOffMeasure_cl(R, Plant, MHopt, MPopt, RNGopt);
end

str = [ 'MH=' num2str(MH,'%.5g') ];
str = [ str '  Mpole=' num2str(Mpole,'%.5g') ];
str = [ str '  Mstability=' num2str(Mst,'%.5g') ];
str = [ str '  RNG=' num2str(MRNG,'%.5g') ];
if nargin>2
    str = [ str '  TO=' num2str(MTO,'%.5g') ];
end
str = [ str '  NbOp=' NbOp ];

disp(str);
disp(' ');