function psiU = psi(U)

[l,n] = size(U);
if l>n
	error('dimension!')
end

muU = mean(U,2);
psiU = zeros(l,l);

for i=1:l
	for j=1:l
%		psiU(i,j) = mean( (U(i,:) - muU(i)*ones(1,n)) .* (U(j,:) - muU(j,:)*ones(1,n)) , 2);
		psiU(i,j) = mean( U(i,:) .* U(j,:) , 2);
	end
end