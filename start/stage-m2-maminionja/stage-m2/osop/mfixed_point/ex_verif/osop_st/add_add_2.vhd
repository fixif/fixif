--
-- Generated by VHDL export
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_signed.all;
entity add_add_2 is
  port(
      oo    : OUT std_logic_vector( 15 downto 0);
      i0    : IN std_logic_vector( 15 downto 0);
      i1    : IN std_logic_vector( 15 downto 0);
      i2    : IN std_logic_vector( 15 downto 0);
      i3    : IN std_logic_vector( 15 downto 0)
  );
end add_add_2;



architecture behavioural of add_add_2 is

component add16
  port(
      i0    : IN std_logic_vector( 15 downto 0);
      i1    : IN std_logic_vector( 15 downto 0);
      o    : OUT std_logic_vector( 15 downto 0)
  );
end component;


component add_adder1
  port (
      oo    : OUT std_logic_vector( 31 downto 0);
      i0    : IN std_logic_vector( 15 downto 0);
      i1    : IN std_logic_vector( 15 downto 0)
);
end component;


component add_adder2
  port (
      oo    : OUT std_logic_vector( 31 downto 0);
      i0    : IN std_logic_vector( 15 downto 0);
      i1    : IN std_logic_vector( 15 downto 0)
);
end component;


signal i0_signal : std_logic_vector( 15 downto 0);
signal i1_signal : std_logic_vector( 15 downto 0);
signal i0_signal_inter : std_logic_vector( 31 downto 0);
signal i1_signal_inter : std_logic_vector( 31 downto 0);
begin
  iadd_add_2 : add16
  port map(
       i1 => i1_signal,
       i0 => i0_signal,
       o => oo
  );
  iop1 : add_adder1
  port map(
       oo => i0_signal_inter,
       i0 => i0,
       i1 => i1
  );
  i0_signal(0) <= i0_signal_inter(16);
  i0_signal(1) <= i0_signal_inter(17);
  i0_signal(2) <= i0_signal_inter(18);
  i0_signal(3) <= i0_signal_inter(19);
  i0_signal(4) <= i0_signal_inter(20);
  i0_signal(5) <= i0_signal_inter(21);
  i0_signal(6) <= i0_signal_inter(22);
  i0_signal(7) <= i0_signal_inter(23);
  i0_signal(8) <= i0_signal_inter(24);
  i0_signal(9) <= i0_signal_inter(25);
  i0_signal(10) <= i0_signal_inter(26);
  i0_signal(11) <= i0_signal_inter(27);
  i0_signal(12) <= i0_signal_inter(28);
  i0_signal(13) <= i0_signal_inter(29);
  i0_signal(14) <= i0_signal_inter(30);
  i0_signal(15) <= i0_signal_inter(31);
  iop2 : add_adder2
  port map(
       oo => i1_signal_inter,
       i0 => i2,
       i1 => i3
  );
  i1_signal(0) <= i1_signal_inter(16);
  i1_signal(1) <= i1_signal_inter(17);
  i1_signal(2) <= i1_signal_inter(18);
  i1_signal(3) <= i1_signal_inter(19);
  i1_signal(4) <= i1_signal_inter(20);
  i1_signal(5) <= i1_signal_inter(21);
  i1_signal(6) <= i1_signal_inter(22);
  i1_signal(7) <= i1_signal_inter(23);
  i1_signal(8) <= i1_signal_inter(24);
  i1_signal(9) <= i1_signal_inter(25);
  i1_signal(10) <= i1_signal_inter(26);
  i1_signal(11) <= i1_signal_inter(27);
  i1_signal(12) <= i1_signal_inter(28);
  i1_signal(13) <= i1_signal_inter(29);
  i1_signal(14) <= i1_signal_inter(30);
  i1_signal(15) <= i1_signal_inter(31);
end behavioural ;
