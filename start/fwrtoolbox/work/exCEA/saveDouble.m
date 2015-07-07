
function saveDouble( name, var)

fout = fopen(name, 'w');

for i=1:length(var)
	s = sprintf( '%.255g', var(i) );
	fwrite( fout, s);
	fwrite( fout, 13);
end

fclose( fout);

