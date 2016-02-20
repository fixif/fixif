function overflowDynamicProcess(workspaceF2F, pathGeneratedFile)

addpath( pathGeneratedFile);
fprintf('\n ajout chemin:  ');
fprintf(pathGeneratedFile);
addpath( workspaceF2F);
fprintf('\n ajout chemin:  ');
fprintf(workspaceF2F);

fprintf('debut CalculDyn.m ');
fprintf('argument:  ');
fprintf(pathGeneratedFile);
fprintf('\n');



pathFileValeurHgDb = strcat(pathGeneratedFile , 'DynNode.xml');
fid=fopen(pathFileValeurHgDb,'w');
%fprintf(fid,'%d,',33);
%newPath;
ParamDynFT;


%NbPtsH = 999; % 10000 découpage dans KLE_range
NbPtsH = 199; % 50000 
%NbPtsH = 99; % 100000

% initialisation de la dynamique des noeuds autre que source
for i = 1 : nombreNoeudInter,
    Noeud(TabNumeroInter(i)).Dyn(1) = 0;
    Noeud(TabNumeroInter(i)).Dyn(2) = 0;
end

for i = 1 : nombreSortie,
    Noeud(TabNumeroSortie(i)).Dyn(1) = 0;
    Noeud(TabNumeroSortie(i)).Dyn(2) = 0;
end

for i = 1 : nombreSource,
	
	Ix = TabNumeroEntree(i);

        for j = 1 : nombreNoeud,
	
		Iy = j;		
		m = size(Hg(Ix,Iy).tf,1);
		
            if ( m ~= 0 )
		
                if(Noeud(Iy).Deb == -1) % Noeud non taggé, execution norme L1
                    [range] = L1_norm(Noeud(Ix).Dyn(1), Noeud(Ix).Dyn(2), Hg(Ix,Iy).tf, NbPtsH);
                else % Noeud taggé, execution overflow
                    Coeff = impulse(Hg(Ix,Iy).tf , NbPtsH);
                	[range, pdf_y, ygrid, var_y] = KLE_range(Noeud(Ix).DynOver, Coeff.', Noeud(Iy).Deb);
                end
                
                Noeud(Iy).Dyn(1) = Noeud(Iy).Dyn(1) + range(1);
                Noeud(Iy).Dyn(2) = Noeud(Iy).Dyn(2) + range(2);
            end
        end
end

fprintf(fid,'<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n');
fprintf(fid,'<Dyn>\n');

for i = 1 : nombreNoeud,
	fprintf(fid,'<node id=\"%2i\">\n',i);
	%fprintf(fid,'<attr key=\"NumeroGraph\" value=\"%2i\"/>\n',i+1); 
	fprintf(fid,'<attr key=\"DynMax\" value=\"%e\"/>\n',Noeud(i).Dyn(2));
	fprintf(fid,'<attr key=\"DynMin\" value=\"%e\"/>\n',Noeud(i).Dyn(1));
    fprintf(fid,'</node>\n');
    
    %fprintf(fid,'%2f\n', Noeud(i).Dyn); 
end
fprintf(fid,'</Dyn>');
fclose(fid);
%fclose(fidC);
