--
-- Generated by VHDL export
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_signed.all;
entity o2_1 is
  port(
      i0    : IN std_logic;
      i1    : IN std_logic;
      q    : OUT std_logic
  );
end o2_1;



architecture behavioural of o2_1 is

component o2_x2
  port (
  i0	: IN STD_LOGIC;
  i1	: IN STD_LOGIC;
  q	: OUT STD_LOGIC
);
end component;


begin
  o2_x2_i0 : o2_x2
  port map(
       i1 => i1,
       i0 => i0,
       q => q
  );
end behavioural ;
