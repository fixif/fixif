%======================
% procude documentation
function processFile( rep_m, rep_tex, fileName, tablefile)

keyList = { 'Purpose', 'Syntax', 'Parameters', 'Description', 'Example', 'See also', 'References'};
ikey = 0;	% index of the keyword we currently are in
numL = 0;	% number of the line processed
prop=cell(length(keyList),1);
endl=13; tab='	';

% open file
mfile = fopen( fullfile( rep_m, [fileName '.m']),'r' );
texfile = fopen( fullfile( rep_tex, [fileName '.tex']),'w' );

% find keywords
while ~feof(mfile)

	% obtain the next line
	L = fgetl(mfile);
	numL = numL+1;
	
	% examine this line
	if isempty(L)	% empty line
		ikey = 0;
	else
		key = regexp( L, '^%\w([\w ])*\w:', 'match');	% find a word (with possible espace inside) that is between % and :, at the beginning of the line 
		if ~isempty(key)	% is there a keyword ?
			ikey = find( strcmp(key{1}(2:end-1), keyList));
			if isempty(ikey)
				display(['in file ' fullfile( rep_m, [fileName '.m']) ', line ' num2str(numL) ':"' key{1} '" is not a correct keyword']);
				ikey = 0;
			else
				prop{ikey} = strvcat( prop{ikey}, strtrim(L(length(key{1})+1:end)) );
			end
		elseif L(1)=='%'	% is it a comment
			if ikey~=0
				id = regexp( L, '%\s*\$Id.*\$');
				if isempty(id)				
					prop{ikey} = strvcat( prop{ikey}, strtrim(L(2:end)) );
				end
			end
		else				% so it's code
			ikey = 0;
		end
	end
	

end



% write texfile
	%mfileName2 = strrep( fileName,'_', '\\_');
fwrite( texfile, [ '\begin{command}[' className(rep_m) removeUnderscore(fileName) ']{' latexize(fileName) '}' endl]);

% write tablefile
purp=prop{1};
if ~isempty(purp)
	fwrite( tablefile, [ tab '\hline ' funcName(fileName,rep_m) ' & ' latexize(purp(1,:)) '\\' endl]);
end

% 1. Purpose
fwrite( texfile, [ tab '\desc{Purpose}' endl]);
fwritel( texfile, latexize(prop{1}));
if isempty(prop{1})
	display( ['file ' fullfile( rep_m, [fileName '.m']) ' doesn''t have a "Purpose" keyword']);
end

% 2. Syntax
fwrite( texfile, [ tab '\desc{Syntax}' endl]);
syn=prop{2};
for i=1:size(syn,1)
	if i~=size(syn,1)
		endllatex = '\\';
	else
		endllatex = '';
	end
	fwrite( texfile, ['\matlab{' latexize(syn(i,:)) '}' endllatex endl]);
end
if isempty(prop{2})
	display( ['file ' fullfile( rep_m, [fileName '.m']) ' doesn''t have a "Syntax" keyword']);
end

% 3. Parameters
if ~isempty(prop{3})
	fwrite( texfile, [ tab '\desc{Parameters}' endl ]);
	par=prop{3};
	fwrite( texfile, [ tab tab '\begin{tabular}{l@{\ :\ }p{9cm}}' endl ]);
	for i=1:size(par,1)
		pari=par(i,:);
		col=findstr(pari,':');
		if isempty(col)
			fwrite( texfile, [ ' & ' latexize(pari(1:end)) '\\' endl]);
		else
			fwrite( texfile, [ '\matlab{' latexize(pari(1:col(1)-1)) '} & ' latexize(pari(col(1)+1:end)) '\\' endl]);
		end
	end
	fwrite( texfile, [ tab tab '\end{tabular}' endl ]);
end
	

% 4. Description'
if ~isempty(prop{4})
	fwrite( texfile,[ tab '\desc{Description}' endl ]);
	fwritel( texfile, prop{4});

end

% 5. Example
if ~isempty(prop{5})
	fwrite( texfile, [ tab '\desc{Example}' endl ]);
	fwritel( texfile, prop{5});
end

% 6. See also
if ~isempty(prop{6})
	fwritel( texfile, [ tab '\desc{See also}' endl ]);
	see=prop{6};
	for i=1:size(see,1)
		seefunc = regexp( see(i,:), '<([\w_@/])*>', 'tokens');
		for j=1:length(seefunc)
			if j>1 | i>1
				fwrite( texfile, ', ');
			end
			fwrite( texfile, funcName(cell2mat(seefunc{j}),''));
		end
	end
	fwrite( texfile, endl);
end

% 7. References
if ~isempty(prop{7})
	fwrite( texfile, [ tab '\desc{References}' endl ]);
	fwritel( texfile, prop{7});
end


fwrite( texfile, '\end{command}');
fwrite( texfile, endl);
fwrite( texfile, endl);
fwrite( texfile, endl);

%close
fclose( mfile);
fclose( texfile);



% write a multiple lines string with a end-of-line
function fwritel( file, str)
endl=13;
for i=1:size(str,1)
	fwrite( file, [ strtrim( str(i,:)) endl]);
end


% remove the underscore of a name
function str = removeUnderscore( name)
str = regexprep( name, '_', '');


% generate the correct call of function \matlab - \hyperlink
function str = funcName( name, rep_m)
i=[0 find(name=='/')];
lastname = name(i(end)+1:end);
str = [ '\funcName[' className(rep_m) removeUnderscore(name) ']{' latexize(lastname) '}' ];


% find the name of the class
function str = className( rep)
	ans = regexp( rep, '/(\@\w*)', 'tokens');
	if isempty(ans)
		str = '';
	else
		str = [ cell2mat(ans{1}) '/' ];
	end
