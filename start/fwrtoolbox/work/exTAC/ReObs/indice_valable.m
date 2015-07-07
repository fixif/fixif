
function ok = indice_valable(indice, poles, ind_com, ind_obs)

% on teste les poles complexes conjugués
ok=1;
for j=1:length(indice)
	
	if ( isreal(poles(indice(j)))==0 )
		% on a affaire à un pole complexe
		% donc on recherche si son conjugué est là aussi
		okj=0;
		for k=1:length(indice)
			if ( poles(indice(k))==conj(poles(indice(j))) )
				okj=1;
				break;
			end
		end
	else
		okj = 1;
	end
	if (okj==0)
		ok=0;
		break;
	end	
end

% il nous faut autant de non commandable que dans ind_com
if length(find( abs(ind_com(indice))<1e-12 )) ~= length( find(abs(ind_com)<1e-12) )
	ok=0;
end
% if faut que les non observables ne soit pas dans la liste non plus
non_obs = find( abs(ind_obs)<1e-12 );
for j=1:length(indice)
	for k=1:length(non_obs)
		if indice(j)==non_obs(k)
			ok=0;
			break;
		end
	end
end
