

function v = tradeoffMeasureError (R, ETF, EP)

v = error_tf(R)/ETF + error_pole(R)/EP;

