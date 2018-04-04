% vite codé...

function S = OpModalrho2FWS(varargin)

R = OpModalrho2FWR(varargin{:});

S = FWS( R, [], @RfunOpModalrho, { varargin{:} }, 'Wcii', diag(R.Wc) );



function [R, cost_flag] = RfunOpModalrho( Rini, paramsValue, dataFWS )

    R = OpModalrho2FWR( dataFWS{:}, paramsValue{1} );
    cost_flag=1;