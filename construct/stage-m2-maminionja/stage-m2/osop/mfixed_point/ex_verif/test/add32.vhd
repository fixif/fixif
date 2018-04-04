--
-- Generated by VHDL export
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_signed.all;
entity add32 is
  port(
      i0    : IN std_logic_vector( 31 downto 0);
      i1    : IN std_logic_vector( 31 downto 0);
      o    : OUT std_logic_vector( 31 downto 0)
  );
end add32;



architecture behavioural of add32 is

component pigibus32
  port(
      a    : IN std_logic_vector( 31 downto 0);
      b    : IN std_logic_vector( 31 downto 0);
      pi    : OUT std_logic_vector( 31 downto 0);
      gi    : OUT std_logic_vector( 31 downto 0)
  );
end component;


component pgtree32slansky
  port(
      pi    : IN std_logic_vector( 31 downto 0);
      gi    : IN std_logic_vector( 31 downto 0);
      p    : OUT std_logic_vector( 31 downto 0);
      g    : OUT std_logic_vector( 31 downto 0)
  );
end component;


component buf_1
  port(
      i    : IN std_logic;
      q    : OUT std_logic
  );
end component;


component xr2_1
  port(
      i0    : IN std_logic;
      i1    : IN std_logic;
      q    : OUT std_logic
  );
end component;


signal pi2_a : std_logic_vector( 31 downto 0);
signal gi2_a : std_logic_vector( 31 downto 0);
signal p2_a : std_logic_vector( 31 downto 0);
signal g2_a : std_logic_vector( 31 downto 0);
signal buf_o0 : std_logic;
signal bool_o1 : std_logic;
signal bool_o2 : std_logic;
signal bool_o3 : std_logic;
signal bool_o4 : std_logic;
signal bool_o5 : std_logic;
signal bool_o6 : std_logic;
signal bool_o7 : std_logic;
signal bool_o8 : std_logic;
signal bool_o9 : std_logic;
signal bool_o10 : std_logic;
signal bool_o11 : std_logic;
signal bool_o12 : std_logic;
signal bool_o13 : std_logic;
signal bool_o14 : std_logic;
signal bool_o15 : std_logic;
signal bool_o16 : std_logic;
signal bool_o17 : std_logic;
signal bool_o18 : std_logic;
signal bool_o19 : std_logic;
signal bool_o20 : std_logic;
signal bool_o21 : std_logic;
signal bool_o22 : std_logic;
signal bool_o23 : std_logic;
signal bool_o24 : std_logic;
signal bool_o25 : std_logic;
signal bool_o26 : std_logic;
signal bool_o27 : std_logic;
signal bool_o28 : std_logic;
signal bool_o29 : std_logic;
signal bool_o30 : std_logic;
signal bool_o31 : std_logic;
begin
  pigibus32_i0 : pigibus32
  port map(
       a => i0,
       b => i1,
       pi => pi2_a,
       gi => gi2_a
  );
  pgtree32slansky_i1 : pgtree32slansky
  port map(
       g => g2_a,
       p => p2_a,
       pi => pi2_a,
       gi => gi2_a
  );
  buf_1_i2 : buf_1
  port map(
       q => buf_o0,
       i => pi2_a(0)
  );
  o(0) <= buf_o0;
  xr2_1_i3 : xr2_1
  port map(
       i1 => g2_a(0),
       i0 => pi2_a(1),
       q => bool_o1
  );
  o(1) <= bool_o1;
  xr2_1_i4 : xr2_1
  port map(
       i1 => g2_a(1),
       i0 => pi2_a(2),
       q => bool_o2
  );
  o(2) <= bool_o2;
  xr2_1_i5 : xr2_1
  port map(
       i1 => g2_a(2),
       i0 => pi2_a(3),
       q => bool_o3
  );
  o(3) <= bool_o3;
  xr2_1_i6 : xr2_1
  port map(
       i1 => g2_a(3),
       i0 => pi2_a(4),
       q => bool_o4
  );
  o(4) <= bool_o4;
  xr2_1_i7 : xr2_1
  port map(
       i1 => g2_a(4),
       i0 => pi2_a(5),
       q => bool_o5
  );
  o(5) <= bool_o5;
  xr2_1_i8 : xr2_1
  port map(
       i1 => g2_a(5),
       i0 => pi2_a(6),
       q => bool_o6
  );
  o(6) <= bool_o6;
  xr2_1_i9 : xr2_1
  port map(
       i1 => g2_a(6),
       i0 => pi2_a(7),
       q => bool_o7
  );
  o(7) <= bool_o7;
  xr2_1_i10 : xr2_1
  port map(
       i1 => g2_a(7),
       i0 => pi2_a(8),
       q => bool_o8
  );
  o(8) <= bool_o8;
  xr2_1_i11 : xr2_1
  port map(
       i1 => g2_a(8),
       i0 => pi2_a(9),
       q => bool_o9
  );
  o(9) <= bool_o9;
  xr2_1_i12 : xr2_1
  port map(
       i1 => g2_a(9),
       i0 => pi2_a(10),
       q => bool_o10
  );
  o(10) <= bool_o10;
  xr2_1_i13 : xr2_1
  port map(
       i1 => g2_a(10),
       i0 => pi2_a(11),
       q => bool_o11
  );
  o(11) <= bool_o11;
  xr2_1_i14 : xr2_1
  port map(
       i1 => g2_a(11),
       i0 => pi2_a(12),
       q => bool_o12
  );
  o(12) <= bool_o12;
  xr2_1_i15 : xr2_1
  port map(
       i1 => g2_a(12),
       i0 => pi2_a(13),
       q => bool_o13
  );
  o(13) <= bool_o13;
  xr2_1_i16 : xr2_1
  port map(
       i1 => g2_a(13),
       i0 => pi2_a(14),
       q => bool_o14
  );
  o(14) <= bool_o14;
  xr2_1_i17 : xr2_1
  port map(
       i1 => g2_a(14),
       i0 => pi2_a(15),
       q => bool_o15
  );
  o(15) <= bool_o15;
  xr2_1_i18 : xr2_1
  port map(
       i1 => g2_a(15),
       i0 => pi2_a(16),
       q => bool_o16
  );
  o(16) <= bool_o16;
  xr2_1_i19 : xr2_1
  port map(
       i1 => g2_a(16),
       i0 => pi2_a(17),
       q => bool_o17
  );
  o(17) <= bool_o17;
  xr2_1_i20 : xr2_1
  port map(
       i1 => g2_a(17),
       i0 => pi2_a(18),
       q => bool_o18
  );
  o(18) <= bool_o18;
  xr2_1_i21 : xr2_1
  port map(
       i1 => g2_a(18),
       i0 => pi2_a(19),
       q => bool_o19
  );
  o(19) <= bool_o19;
  xr2_1_i22 : xr2_1
  port map(
       i1 => g2_a(19),
       i0 => pi2_a(20),
       q => bool_o20
  );
  o(20) <= bool_o20;
  xr2_1_i23 : xr2_1
  port map(
       i1 => g2_a(20),
       i0 => pi2_a(21),
       q => bool_o21
  );
  o(21) <= bool_o21;
  xr2_1_i24 : xr2_1
  port map(
       i1 => g2_a(21),
       i0 => pi2_a(22),
       q => bool_o22
  );
  o(22) <= bool_o22;
  xr2_1_i25 : xr2_1
  port map(
       i1 => g2_a(22),
       i0 => pi2_a(23),
       q => bool_o23
  );
  o(23) <= bool_o23;
  xr2_1_i26 : xr2_1
  port map(
       i1 => g2_a(23),
       i0 => pi2_a(24),
       q => bool_o24
  );
  o(24) <= bool_o24;
  xr2_1_i27 : xr2_1
  port map(
       i1 => g2_a(24),
       i0 => pi2_a(25),
       q => bool_o25
  );
  o(25) <= bool_o25;
  xr2_1_i28 : xr2_1
  port map(
       i1 => g2_a(25),
       i0 => pi2_a(26),
       q => bool_o26
  );
  o(26) <= bool_o26;
  xr2_1_i29 : xr2_1
  port map(
       i1 => g2_a(26),
       i0 => pi2_a(27),
       q => bool_o27
  );
  o(27) <= bool_o27;
  xr2_1_i30 : xr2_1
  port map(
       i1 => g2_a(27),
       i0 => pi2_a(28),
       q => bool_o28
  );
  o(28) <= bool_o28;
  xr2_1_i31 : xr2_1
  port map(
       i1 => g2_a(28),
       i0 => pi2_a(29),
       q => bool_o29
  );
  o(29) <= bool_o29;
  xr2_1_i32 : xr2_1
  port map(
       i1 => g2_a(29),
       i0 => pi2_a(30),
       q => bool_o30
  );
  o(30) <= bool_o30;
  xr2_1_i33 : xr2_1
  port map(
       i1 => g2_a(30),
       i0 => pi2_a(31),
       q => bool_o31
  );
  o(31) <= bool_o31;
end behavioural ;
