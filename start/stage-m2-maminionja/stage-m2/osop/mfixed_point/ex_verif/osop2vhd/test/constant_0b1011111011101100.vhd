--
-- Generated by VHDL export
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_signed.all;
entity constant_0b1011111011101100 is
  port(
      o    : OUT std_logic_vector( 15 downto 0)
  );
end constant_0b1011111011101100;



architecture behavioural of constant_0b1011111011101100 is

component zero_1
  port(
      nq    : OUT std_logic
  );
end component;


component one_1
  port(
      q    : OUT std_logic
  );
end component;


signal zero_s0 : std_logic;
signal zero_s1 : std_logic;
signal one_s2 : std_logic;
signal one_s3 : std_logic;
signal zero_s4 : std_logic;
signal one_s5 : std_logic;
signal one_s6 : std_logic;
signal one_s7 : std_logic;
signal zero_s8 : std_logic;
signal one_s9 : std_logic;
signal one_s10 : std_logic;
signal one_s11 : std_logic;
signal one_s12 : std_logic;
signal one_s13 : std_logic;
signal zero_s14 : std_logic;
signal one_s15 : std_logic;
begin
  zero_1_i0 : zero_1
  port map(
       nq => zero_s0
  );
  o(0) <= zero_s0;
  zero_1_i1 : zero_1
  port map(
       nq => zero_s1
  );
  o(1) <= zero_s1;
  one_1_i2 : one_1
  port map(
       q => one_s2
  );
  o(2) <= one_s2;
  one_1_i3 : one_1
  port map(
       q => one_s3
  );
  o(3) <= one_s3;
  zero_1_i4 : zero_1
  port map(
       nq => zero_s4
  );
  o(4) <= zero_s4;
  one_1_i5 : one_1
  port map(
       q => one_s5
  );
  o(5) <= one_s5;
  one_1_i6 : one_1
  port map(
       q => one_s6
  );
  o(6) <= one_s6;
  one_1_i7 : one_1
  port map(
       q => one_s7
  );
  o(7) <= one_s7;
  zero_1_i8 : zero_1
  port map(
       nq => zero_s8
  );
  o(8) <= zero_s8;
  one_1_i9 : one_1
  port map(
       q => one_s9
  );
  o(9) <= one_s9;
  one_1_i10 : one_1
  port map(
       q => one_s10
  );
  o(10) <= one_s10;
  one_1_i11 : one_1
  port map(
       q => one_s11
  );
  o(11) <= one_s11;
  one_1_i12 : one_1
  port map(
       q => one_s12
  );
  o(12) <= one_s12;
  one_1_i13 : one_1
  port map(
       q => one_s13
  );
  o(13) <= one_s13;
  zero_1_i14 : zero_1
  port map(
       nq => zero_s14
  );
  o(14) <= zero_s14;
  one_1_i15 : one_1
  port map(
       q => one_s15
  );
  o(15) <= one_s15;
end behavioural ;
