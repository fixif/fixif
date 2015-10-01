--
-- Generated by VHDL export
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_signed.all;
entity mul_mult_xn2 is
  port(
      i0    : IN std_logic_vector( 15 downto 0);
      oo    : OUT std_logic_vector( 31 downto 0)
  );
end mul_mult_xn2;



architecture behavioural of mul_mult_xn2 is

component constant_0b1001111001110111
  port(
      o    : OUT std_logic_vector( 15 downto 0)
  );
end component;


component mul16_16
  port(
      i0    : IN std_logic_vector( 15 downto 0);
      i1    : IN std_logic_vector( 15 downto 0);
      o    : OUT std_logic_vector( 31 downto 0)
  );
end component;


signal cst : std_logic_vector( 15 downto 0);
signal cst_o0 : std_logic_vector( 15 downto 0);
begin
  constant_0b1001111001110111_i0 : constant_0b1001111001110111
  port map(
       o => cst_o0
  );
  cst(0) <= cst_o0(0);
  cst(1) <= cst_o0(1);
  cst(2) <= cst_o0(2);
  cst(3) <= cst_o0(3);
  cst(4) <= cst_o0(4);
  cst(5) <= cst_o0(5);
  cst(6) <= cst_o0(6);
  cst(7) <= cst_o0(7);
  cst(8) <= cst_o0(8);
  cst(9) <= cst_o0(9);
  cst(10) <= cst_o0(10);
  cst(11) <= cst_o0(11);
  cst(12) <= cst_o0(12);
  cst(13) <= cst_o0(13);
  cst(14) <= cst_o0(14);
  cst(15) <= cst_o0(15);
  imul_xn2 : mul16_16
  port map(
       i1 => cst,
       i0 => i0,
       o => oo
  );
end behavioural ;
