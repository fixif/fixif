%Purpose:
% Create the associated fixed-point algorithm in VHDL.
% Two files are generated "xxxx_entity.vhd" and "xxx_types.vhd" where
% xxxx is the name given ("myFilter" by default)
%
%Syntax:
% implementVHDL( R,fileName)
%
%Parameters:
% R: FWR object
% fileName: name of the function (default='myFilter')
%
% $Id$

function implementVHDL( R, fileName)

% args
if nargin<2
    fileName='myFilter';
end

% FPIS?
if isempty(R.FPIS)
    error( 'The realization must have a valid FPIS');
end


% parameters
tabu = '    ';
endl = 13;
isPnut = any(any( tril(R.P,-1)) ); % is the lower triangular part of R.P non null ???

%=================
% variables' names
% output(s)
if (R.p==1)
    strY = 'y';
else
    strY = [ setstr( ones(R.p,1)*'y' ) num2str((1:R.p)') ];
end
% states
strXn = [ setstr( ones(R.n,1)*'xn' ) num2str((1:R.n)') ];
% input(s)
if (R.m==1)
    strU = 'u';
else
    strU = [ setstr( ones(R.m,1)*'u' ) num2str((1:R.m)') ];
end
% intermediate variables
strT = [ setstr( ones(R.l,1)*'T' ) num2str((1:R.l)') ];


%=================
% FP_types.vhd

% open files
FP_types = fopen('FP_types.vhd.template','r');
myFP_types = fopen([ fileName '_types.vhd'],'w');

% date
copyUntilSharps( FP_types, myFP_types); % ##DATE##
fwrite( myFP_types, datestr(now));

% input
copyUntilSharps( FP_types, myFP_types); % ##DEFINE TYPES##
fwrite( myFP_types, [ tabu '-- input data with FP format (' num2str(R.FPIS.betaU) ',' num2str(R.FPIS.betaU-R.FPIS.gammaU-1) ',' num2str(R.FPIS.gammaU) ')' endl ] );
fwrite( myFP_types, [ tabu 'subtype datain is ' VHDLRange(R.FPIS.betaU) ';' endl endl ] );

% output
fwrite( myFP_types, [ tabu '-- filtered output data with FP format (' num2str(R.FPIS.betaY) ',' num2str(R.FPIS.betaY-R.FPIS.gammaY-1) ',' num2str(R.FPIS.gammaY) ')' endl ] );
fwrite( myFP_types, [ tabu 'subtype dataout is ' VHDLRange(R.FPIS.betaY) ';' endl ] );

% states
fwrite( myFP_types, [ endl tabu '-- states ' endl] );
for i=1:R.n
    fwrite( myFP_types, [ tabu 'subtype state' num2str(i) ' is ' VHDLRange(R.FPIS.betaX(i)) ';   -- format (' num2str(R.FPIS.betaX(i)) ',' num2str(R.FPIS.betaX(i)-R.FPIS.gammaX(i)-1) ',' num2str(R.FPIS.gammaX(i)) ')' endl ] );
end

% intermediate variables
fwrite( myFP_types, [ endl tabu '-- intermediate variables ' endl] );
for i=1:R.l
    fwrite( myFP_types, [ tabu 'subtype intermediate_var' num2str(i) ' is ' VHDLRange(R.FPIS.betaT(i)) ';   -- format (' num2str(R.FPIS.betaT(i)) ',' num2str(R.FPIS.betaT(i)-R.FPIS.gammaT(i)-1) ',' num2str(R.FPIS.gammaT(i)) ')' endl ] );
end

% close files
copyUntilSharps( FP_types, myFP_types);
fclose(FP_types); fclose(myFP_types);


%==============
% FP_entity.vhd

% open files
FP_entity = fopen('FP_entity.vhd.template','r');
myFP_entity = fopen([ fileName '_entity.vhd'],'w');
copyUntilSharps( FP_entity, myFP_entity); % ##FILTER NAME##
fwrite( myFP_entity, fileName);
copyUntilSharps( FP_entity, myFP_entity); % ##FILTER NAME##
fwrite( myFP_entity, fileName);
copyUntilSharps( FP_entity, myFP_entity); % ##FILTER NAME##
fwrite( myFP_entity, fileName);
copyUntilSharps( FP_entity, myFP_entity); % ##SIGNALS##

% declaration of signals
fwrite( myFP_entity, [ endl tabu '-- states ' endl] );
for i=1:R.n
    fwrite( myFP_entity, [ tabu 'signal ' strXn(i,:) ]);
    fwrite( myFP_entity, [ ' : state' num2str(i) ' := 0;' endl ] );
end
fwrite( myFP_entity, [ endl tabu '-- intermediate variables ' endl] );
for i=1:R.l
    fwrite( myFP_entity, [ tabu 'signal ' strT(i,:) ' : intermediate_var' num2str(i) ' := 0;' endl] );
end

% intermediate variables J.T = M.X(k) + N.U(k)
copyUntilSharps( FP_entity, myFP_entity);   % ##INTERMEDIATE VARIABLES AND OUTPUT##
if (R.l>0)
     fwrite( myFP_entity, [ endl tabu '-- intermediate variables' endl ] );
end
for i=1:R.l
    fwrite( myFP_entity, [ tabu strT(i,:) ' <= ' ...
            scalprodVHDL( [ -R.J(i,1:i-1) R.M(i,:) R.N(i,:) ],...
                  strvcat( strT(1:i-1,:), strXn, strU  ),...
                  R.FPIS.gammaZ(i,[1:i-1 R.l+1:end]),...
                  R.FPIS.shiftZ(i,[1:i-1 R.l+1:end]),...
                  R.FPIS.shiftADD(i)) ';' endl ] );
end

% output Y(k) = R.X(k) + code.U(k) + L.T
fwrite( myFP_entity, [ endl tabu '-- output(s)' endl ] );
for i=1:R.p
    fwrite( myFP_entity, [ tabu strY(i,:) ' <= ' ...
            scalprodVHDL( R.Z(R.l+R.n+i,:) ,...
                  strvcat( strT, strXn, strU),...
                  R.FPIS.gammaZ(R.l+R.n+i,:),...
                  R.FPIS.shiftZ(R.l+R.n+i,:),...
                  R.FPIS.shiftADD(i+R.l+R.n) ) ';' endl ] );
end


% Asynchronous reset
copyUntilSharps( FP_entity, myFP_entity);   % ##RESET##
for i=1:R.n
    fwrite( myFP_entity, [ tabu tabu strXn(i,:) ' <= 0;' endl ] );
end


% states
copyUntilSharps( FP_entity, myFP_entity);   % ##STATES##
fwrite( myFP_entity, [ endl tabu '-- states' endl ] ); 
for i=1:R.n
        fwrite( myFP_entity, [ tabu strXn(i,:) ' <= ' ...
                scalprodVHDL( R.Z(R.l+i,:) ,...
                    strvcat( strT, strXn, strU),...
                    R.FPIS.gammaZ(R.l+i,:),...
                    R.FPIS.shiftZ(R.l+i,:),...
                    R.FPIS.shiftADD(i+R.l) ) ';' endl ] );
end
fwrite( myFP_entity, endl);



% close files
copyUntilSharps( FP_entity, myFP_entity);
fclose(FP_entity); fclose(myFP_entity);




%=========================================
% copy from src to dest until item appears
function copyUntilSharps( src, dest, item)

while ~feof(src)
    c=fread(src,1);
    if c=='#'
        c=fread(src,1);
        if c=='#'
            while fread(src,1)~='#'; end;
            fread(src,1);
            break;
        else
            fwrite(dest,c);
        end
    end
    fwrite(dest,c);
end


%===============================================
% return the signed integer range with beta bits
function S = VHDLRange( beta)
S = [ 'integer range -2**' num2str(beta-1) ' to 2**' num2str(beta-1) '-1' ];


%===================================
% remove redondant value in a vector
% [8 1 8 2 1 8] becomes [1 2 8]
function v = redon(v)
v=sort(v);
for i=length(v):-1:2
    if v(i)==v(i-1)
        v(i)=[];
        i=i-1;
    end
end

%===================
% code for the shift
function S = shiftcode( str, shift)

if shift<0
    S = [ str '* 2**' num2str(-shift) ];
elseif shift==0
    S = str;
else
    S = [ str '/ 2**' num2str(shift) ];
end



%Description:
% 	Generate two VHDL files (named "myFilter\_entity.vhd" and "myFilter\_types.vhd" by default)
%	that realizes the fixed-point algorithm corresponding to the
%	realization.\\
% 	All the wordlengths and the fixed-point positions should be first computed by adjusting the FPIS with
% 	\funcName{@FWR/setFPIS}.\\
%	The files \matlab{@FWR/private/FP\_types.vhd.template} and \matlab{@FWR/private/FP\_entity.vhd.template} are used as a
%	template.

%Example:
% 	This function produces a \texttt{myFilter\_types.vhdl} file
% 	\begin{lstlisting}[language=VHDL]
% 	library IEEE;
% 	use IEEE.STD_LOGIC_1164.all;
% 	use IEEE.STD_LOGIC_arith.all;
% 	use IEEE.STD_LOGIC_SIGNED.all;
% 
% 	-- purpose: filtering (generic fixed-point specificatin)
% 	-- type   : sequential/arithmetic
% 	-- inputs : u(n)
% 	-- output : y(n) 
% 	-- author : automatically generated by 
% 	-- date   : 08-Dec-2008 18:41:00
% 
% 
% 	package FP_types is
% 
% 		-- input data with FP format (16,4,11)
% 		subtype datain is integer range -2**15 to 2**15-1;
% 
% 		-- filtered output data with FP format (16,4,11)
% 		subtype dataout is integer range -2**15 to 2**15-1;
% 
% 		-- states 
% 		subtype state1 is integer range -2**15 to 2**15-1;   -- format (16,5,10)
% 		subtype state2 is integer range -2**15 to 2**15-1;   -- format (16,4,11)
% 		subtype state3 is integer range -2**15 to 2**15-1;   -- format (16,3,12)
% 
% 		-- intermediate variables 
% 
% 	end FP_types;
% 	\end{lstlisting}
%
% 	It also produces a \texttt{myFilter\_entity.vhdl} file
% 	\begin{lstlisting}[language=VHDL]
% 	library IEEE;
% 	use IEEE.STD_LOGIC_1164.all;
% 	use IEEE.STD_LOGIC_arith.all;
% 	use IEEE.STD_LOGIC_SIGNED.all;
% 	library work;
% 	use work.FP_types.all;
% 
% 	entity myFilter is
% 	  port (
% 		rstb    : in  std_logic; -- asynchronous reset asynchrone active low
% 		clk     : in  std_logic; -- global clock
% 		u       : in  datain; -- input data
% 		y       : out dataout); -- filtered output
% 	end myFilter;
% 
% 	architecture RTL of myFilter is
% 
% 		-- states 
% 		signal xn1 : state1 := 0;
% 		signal xn2 : state2 := 0;
% 		signal xn3 : state3 := 0;
% 
% 		-- intermediate variables 
% 
% 	begin
% 
% 		-- output(s)
% 		y <= (    xn1 * 22006 + xn2 * 5304 + xn3 * 650 + u   * 1614) / 2**14;
% 
% 	  S1: process(rstb,clk)
% 	  begin
% 		if rstb = '0' then                  -- asynchronous reset
% 			xn1 <= 0;
% 			xn2 <= 0;
% 			xn3 <= 0;
% 		elsif clk'event and clk = '1' then  -- rising clock edge
% 
% 		-- states
% 		xn1 <= (    xn1 * 18120 + xn2 * (-8813) + xn3 * 239 + u   * 11003) / 2**15;
% 		xn2 <= (    xn1 * 17627 + xn2 * 1591 + xn3 * (-2919) + u   * (-5304)) / 2**14;
% 		xn3 <= (    xn1 * 3824 + xn2 * 23349 + xn3 * (-2387) + u   * 5196) / 2**15;
% 
% 		end if;  
% 	  end process S1;
% 
% 	end RTL;
% 	\end{lstlisting}

%See also: <@FWR/implementLaTeX>, <@FWR/implementMATLAB>