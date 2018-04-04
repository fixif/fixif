function [Y,X,T] = realize_step( R, U, X0)

% comme realize mais juste une étape
% peut utiliser intlab

[l,m,n,p] = size(R);

%T = zeros(l,1);
JT = R.M*X0+R.N*U;
for k=1:l
    T0=0;
    for l=1:k-1
        T0=R.J(k,l)*T(l);
    end
    T(k) = JT(k) - T0;
end

X = R.K*T + R.P*X0 + R.Q*U;
Y = R.L*T + R.R*X0 + R.S*U;

end