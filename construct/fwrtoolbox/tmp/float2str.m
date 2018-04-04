

function str=float2str(X)

[F,E]=log2(X);
str =  [ num2str(F*2^53,'%30.0f') '*2^' num2str(E-53) ];