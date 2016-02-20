% transform string in order to remove some special LaTeX code
% for example "%3.F" is transformed in "\%3.F"

function S=latexize(str)

if ~isempty(str)
	if size(str,1)==1
		S = latexizeline( str);
	else
		S=[];
		for i=1:size(str,1)
			S = strvcat( S, latexizeline( str(i,:)) );
		end
	end
else
	S=[];
end

function L=latexizeline(line)
	%replace '%' by '\%'
	line = regexprep( line,'%', '\\%');
	
	%replace '_' by '\_', except in math mode $...$
	L =[];
	while ~isempty(line)
		if line(1)~='$'
			[str line] = strtok( line, '$$');
			str = regexprep( str, '_', '\\_');
		else
			[str line] = strtok( line, '$$');
			str = [ '$' str '$'];
			line=line(2:end);
		end
		L = [L  str];
	end
	line=L;

	%replace "'...'" par "\matlab{...}"
	L=[];
	while ~isempty(line)
		if line(1)~=''''
			[str line] = strtok( line, '''''');
		else
			[str line] = strtok( line, '''''');
			if ~isempty(line)
				str = [ '\matlab{' str '}'];
				line=line(2:end);
			else
				str = [ '''' str];
			end
		end
		L = [L  str];
	end
	line=L;
	
	%replace "..." par "\matlab{'...'}"
	L=[];
	while ~isempty(line)
		if line(1)~='""'
			[str line] = strtok( line, '""');
		else
			[str line] = strtok( line, '""');
			if ~isempty(line)
				str = [ '\matlab{''' str '''}'];
				line=line(2:end);
			else
				str = [ '"' str];
			end
		end
		L = [L  str];
	end	