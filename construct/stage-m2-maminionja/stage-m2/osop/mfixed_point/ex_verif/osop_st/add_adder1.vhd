--
-- Generated by VHDL export
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_signed.all;
entity add_adder1 is
  port(
      oo    : OUT std_logic_vector( 31 downto 0);
      i0    : IN std_logic_vector( 15 downto 0);
      i1    : IN std_logic_vector( 15 downto 0)
  );
end add_adder1;



architecture behavioural of add_adder1 is

component add32
  port(
      i0    : IN std_logic_vector( 31 downto 0);
      i1    : IN std_logic_vector( 31 downto 0);
      o    : OUT std_logic_vector( 31 downto 0)
  );
end component;


component mul_mult_t0
  port (
      i0    : IN std_logic_vector( 15 downto 0);
      oo    : OUT std_logic_vector( 31 downto 0)
);
end component;


component mul_mult_xn3
  port (
      i0    : IN std_logic_vector( 15 downto 0);
      oo    : OUT std_logic_vector( 31 downto 0)
);
end component;


signal i0_signal : std_logic_vector( 31 downto 0);
signal i1_signal : std_logic_vector( 31 downto 0);
signal i0_signal_inter : std_logic_vector( 31 downto 0);
signal i1_signal_inter : std_logic_vector( 31 downto 0);
begin
  iadd_adder1 : add32
  port map(
       i1 => i1_signal,
       i0 => i0_signal,
       o => oo
  );
  iop1 : mul_mult_t0
  port map(
       oo => i0_signal_inter,
       i0 => i0
  );
  i0_signal(0) <= i0_signal_inter(0);
  i0_signal(1) <= i0_signal_inter(1);
  i0_signal(2) <= i0_signal_inter(2);
  i0_signal(3) <= i0_signal_inter(3);
  i0_signal(4) <= i0_signal_inter(4);
  i0_signal(5) <= i0_signal_inter(5);
  i0_signal(6) <= i0_signal_inter(6);
  i0_signal(7) <= i0_signal_inter(7);
  i0_signal(8) <= i0_signal_inter(8);
  i0_signal(9) <= i0_signal_inter(9);
  i0_signal(10) <= i0_signal_inter(10);
  i0_signal(11) <= i0_signal_inter(11);
  i0_signal(12) <= i0_signal_inter(12);
  i0_signal(13) <= i0_signal_inter(13);
  i0_signal(14) <= i0_signal_inter(14);
  i0_signal(15) <= i0_signal_inter(15);
  i0_signal(16) <= i0_signal_inter(16);
  i0_signal(17) <= i0_signal_inter(17);
  i0_signal(18) <= i0_signal_inter(18);
  i0_signal(19) <= i0_signal_inter(19);
  i0_signal(20) <= i0_signal_inter(20);
  i0_signal(21) <= i0_signal_inter(21);
  i0_signal(22) <= i0_signal_inter(22);
  i0_signal(23) <= i0_signal_inter(23);
  i0_signal(24) <= i0_signal_inter(24);
  i0_signal(25) <= i0_signal_inter(25);
  i0_signal(26) <= i0_signal_inter(26);
  i0_signal(27) <= i0_signal_inter(27);
  i0_signal(28) <= i0_signal_inter(28);
  i0_signal(29) <= i0_signal_inter(29);
  i0_signal(30) <= i0_signal_inter(30);
  i0_signal(31) <= i0_signal_inter(31);
  iop2 : mul_mult_xn3
  port map(
       oo => i1_signal_inter,
       i0 => i0
  );
  i1_signal(0) <= i1_signal_inter(0);
  i1_signal(1) <= i1_signal_inter(1);
  i1_signal(2) <= i1_signal_inter(2);
  i1_signal(3) <= i1_signal_inter(3);
  i1_signal(4) <= i1_signal_inter(4);
  i1_signal(5) <= i1_signal_inter(5);
  i1_signal(6) <= i1_signal_inter(6);
  i1_signal(7) <= i1_signal_inter(7);
  i1_signal(8) <= i1_signal_inter(8);
  i1_signal(9) <= i1_signal_inter(9);
  i1_signal(10) <= i1_signal_inter(10);
  i1_signal(11) <= i1_signal_inter(11);
  i1_signal(12) <= i1_signal_inter(12);
  i1_signal(13) <= i1_signal_inter(13);
  i1_signal(14) <= i1_signal_inter(14);
  i1_signal(15) <= i1_signal_inter(15);
  i1_signal(16) <= i1_signal_inter(16);
  i1_signal(17) <= i1_signal_inter(17);
  i1_signal(18) <= i1_signal_inter(18);
  i1_signal(19) <= i1_signal_inter(19);
  i1_signal(20) <= i1_signal_inter(20);
  i1_signal(21) <= i1_signal_inter(21);
  i1_signal(22) <= i1_signal_inter(22);
  i1_signal(23) <= i1_signal_inter(23);
  i1_signal(24) <= i1_signal_inter(24);
  i1_signal(25) <= i1_signal_inter(25);
  i1_signal(26) <= i1_signal_inter(26);
  i1_signal(27) <= i1_signal_inter(27);
  i1_signal(28) <= i1_signal_inter(28);
  i1_signal(29) <= i1_signal_inter(29);
  i1_signal(30) <= i1_signal_inter(30);
  i1_signal(31) <= i1_signal_inter(31);
end behavioural ;
