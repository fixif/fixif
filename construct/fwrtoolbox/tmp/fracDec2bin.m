function s=fracDec2bin(fra,n)

Z=fra;
for i=1:n
	v=2*Z;
	X=floor(v);
	Z=v-X;
	if X==1
		s(i)='1';
	else
		s(i)='0';
	end
end
