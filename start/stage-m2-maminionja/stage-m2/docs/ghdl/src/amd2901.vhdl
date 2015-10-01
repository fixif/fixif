library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity amd2901 is
	Port (
		i		:	in std_logic_vector(8 downto 0);
		d		:	in std_logic_vector(3 downto 0);
		a		:	in std_logic_vector(3 downto 0);
		b		:	in std_logic_vector(3 downto 0);

		y		:	out std_logic_vector (3 downto 0);
		noe 	:	in std_logic;

		clk	:	in  std_logic;

		cin	:	in  std_logic;
		ng		:	out  std_logic;
		np		:	out  std_logic;
		cout	:	out  std_logic;
		ovr	:	out  std_logic;
		zero	:	out std_logic;
		sign	:	out std_logic;

		q0		:	inout  std_logic;
		q3		:	inout  std_logic;
		r0		:	inout  std_logic;
		r3		:	inout  std_logic);
	end amd2901;

architecture behavior of amd2901 is

--Signaux de la MIcro INstruction décode
alias dst_ctl  :std_logic_vector(2 downto 0) is i(8 downto 6);		-- DESTINATION CONTROL (selectionne registres de destion du result de l'ALU) 
alias alu_ctl   :std_logic_vector(2 downto 0) is i(5 downto 3);		--  ALU FUNCTION ( Selectionne la fonction)
alias src_ctl   :std_logic_vector(2 downto 0) is i(2 downto 0);		-- ALU SOURCE (Selectionne les registres des 2 opérandes)




signal alu_out	: std_logic_vector(3 downto 0); ---output before tri-state buffer
signal ra, rb	: std_logic_vector(3 downto 0);
signal r, s		: std_logic_vector(3 downto 0);
signal accu		: std_logic_vector(3 downto 0);

type ram_array is array(15 downto 0) of std_logic_vector (3 downto 0);
signal ram  : ram_array;

signal rornotr : std_logic_vector(3 downto 0);
signal sornots : std_logic_vector(3 downto 0);
signal c_sum : std_logic_vector(3 downto 0);
signal sum : std_logic_vector(3 downto 0);

signal p : std_logic_vector(3 downto 0);
signal g : std_logic_vector(3 downto 0);
signal np_sum : std_logic;
signal ng_sum : std_logic;

begin
--------------------Mux-in-----------------------------
---decode alu operand r:

	with src_ctl select
		r <=	ra			when "000" |"001",
				"0000"	when "010"|"011"|"100",
				d			when others;

	with src_ctl select
		s <=	accu		when "000"|"010"|"110",
				rb			when "001"|"011",
				ra			when "100"|"101",
				"0000"	when others;

--------------------------------------------------------  Alu-----------------------------------


	
	with alu_ctl select
		rornotr <=	not r	when O"1" | O"5" | O"6",
						r		when others;

	sornots <= not s when alu_ctl = O"2" else s;

	c_sum <= (rornotr and sornots) or
				(rornotr and (c_sum(2 downto 0) & cin)) or
				(sornots and (c_sum(2 downto 0) & cin));

	sum <= rornotr xor sornots xor (c_sum(2 downto 0) & cin);

	p <= rornotr or sornots;
	g <= rornotr and sornots;
	np_sum <= not (p(3) and p(2) and p(1) and p(0));
	ng_sum <= not(g(3) or
					(p(3) and g(2)) or
					(p(3) and p(2) and g(1)) or
					(p(3) and p(2) and p(1) and g(0)));

	with alu_ctl select
		alu_out <=	sum				when O"0" | O"1" | O"2",
						r or s			when O"3",
						r and s			when O"4",
						(not r) and s	when O"5",
						r xor s			when O"6",
						not(r xor s)	when others;

	with alu_ctl select
		np <=	np_sum								when O"0" | O"1" | O"2",
				'0'									when O"3" | O"4" | O"5",
				g(3) or g(2) or g(1) or g(0)	when others;

	with alu_ctl select
		ng <=	ng_sum								 		when O"0" | O"1" | O"2",
				p(3) and p(2) and p(1) and p(0)		when O"3",
				not (g(3) or g(2) or g(1) or g(0))	when O"4" | O"5",
				(p(3) and g(3)) or
				(p(3) and p(2) and g(2)) or
				(p(3) and p(2) and p(1) and g(1)) or
				(p(3) and p(2) and p(1) and p(0))	when others;

	with alu_ctl select
		cout <=	c_sum(3)							 			when O"0" | O"1" | O"2",
					np_sum or cin								when O"3",
					g(3) or g(2) or g(1) or g(0) or cin	when O"4" | O"5",
					(p(3) and g(3)) or
					(p(3) and p(2) and g(2)) or
					(p(3) and p(2) and p(1) and g(1)) or
					(p(3) and p(2) and p(1) and p(0) and (g(0) or (not cin)))
																	when others;

	with alu_ctl select
		ovr <=	c_sum(2) xor c_sum(3)		 			when O"0" | O"1" | O"2",
					np_sum or cin								when O"3",
					not (g(3) or g(2) or g(1) or g(0)) or
													(not cin)	when O"4" | O"5",
					not ((p(3) and g(3)) or
					(p(3) and p(2) and g(2)) or
					(p(3) and p(2) and p(1) and g(1)) or
					(p(3) and p(2) and p(1) and p(0) and (g(0) or (not cin))))
																	when others;


	zero <='1' when (alu_out="0000") else '0';
	sign <=alu_out(3);

-----------------------------Mux-out-------------------

	mux_out : process(alu_out, dst_ctl, ra, noe)
	begin
		if (noe = '0') then
			if (dst_ctl = O"2") then
				y <= ra;
			else
				y <= alu_out;
			end if;
		else
			y <= "ZZZZ";
		end if;
	end process;

---------------------------accu-------------------   

	process(clk) 
	begin 
 		if rising_edge(clk) then
 			if dst_ctl = O"0" then accu <= alu_out;
 			elsif dst_ctl = O"4" then accu <= q3 & accu(3 downto 1);
 			elsif dst_ctl = O"6" then accu <= accu(2 downto 0) & q0;
			end if;
		end if;
	end process; 

	q3 <= accu(3) when (dst_ctl = O"6" or dst_ctl = O"7") else 'Z';
	q0 <= accu(0) when (dst_ctl = O"4" or dst_ctl = O"5") else 'Z';

------------------------------------------------------Ram---------------------------------------------

	process(clk)
	variable sh_out : std_logic_vector(3 downto 0);
	variable we : boolean;
	begin
		case dst_ctl is
			when O"4" | O"5" =>
				sh_out := r3 & alu_out(3 downto 1);
				we := true;
			when O"6" | O"7" =>
				sh_out := alu_out(2 downto 0) & r0;
				we := true;
			when O"2" | O"3" =>
				sh_out := alu_out;
				we := true;
			when others  =>
				we := false;
		end case;

 		if rising_edge(clk) then 
			if we then ram(to_integer(unsigned(b))) <= sh_out;
 			end if; 
		end if; 
	end process;

	ra<= ram(to_integer(unsigned(a)));
	rb<= ram(to_integer(unsigned(b)));

	r3 <= alu_out(3) when (dst_ctl = "111" or dst_ctl = "110") else 'Z';
	r0 <= alu_out(0) when (dst_ctl = "101" or dst_ctl = "100") else 'Z';
end;
