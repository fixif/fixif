library ieee;
use ieee.math_real.all;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;

library work;
use work.bidon.all;


--  A testbench has no ports.
entity adder_tb is
end adder_tb;

architecture behav of adder_tb is
	--  Declaration of the component that will be instantiated.
	component adder
	port (i0, i1 : in std_logic; ci : in std_logic; s : out std_logic; co : out std_logic);
	end component;

	--  Specifies which entity is bound with the component.
	for adder_0: adder use entity work.adder;
	signal i0, i1, ci, s, co : std_logic;

	begin
	--  Component instantiation.
	adder_0: adder
	port map (	i0 => i0,
					i1 => i1,
					ci => ci,
					s => s,
					co => co);

	--  This process does the real job.
process

variable rd : integer;
variable rdstd : std_logic_vector(31 downto 0);
variable res_sum : std_logic_vector(31 downto 0);

begin
	--  Check each pattern.
	for i in 1 to 10 loop
		--  Set the inputs.
		rd := RAND;
		rdstd := std_logic_vector(to_unsigned(rd,32));
		i0 <= rdstd(0);
		i1 <= rdstd(1);
		ci <= rdstd(2);
		--  Wait for the results.
		wait for 1 ns;
		--  Check the outputs.
		res_sum := std_logic_vector(to_unsigned(sum(rd),32));
		assert s = res_sum(0) report "bad sum value" severity error;
		assert co = ((i0 and i1) or (i0 and ci) or (i1 and ci)) report "bad carray out value" severity error;
	end loop;
assert false report "end of test" severity note;
--  Wait forever; this will finish the simulation.
wait;
end process;
end behav;
