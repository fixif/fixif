-- Test Bench for filter
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.all;
use IEEE.STD_LOGIC_SIGNED.all;
use STD.TEXTIO.ALL;

library work;
use work.FP_type.all;

entity test_filter is
end test_filter;

architecture test of test_filter is

  constant Tclk : time := 10 ns;        -- clock period

  -- External signals 
  signal clk            : std_logic := '0';
  signal rstb           : std_logic := '0';

  signal u              : datain := 0;
  signal y              : dataout := 0;

  -- Internals signals


component  myFilter
  port (
    rstb    : in  std_logic; -- asynchronous reset asynchrone active low
    clk     : in  std_logic; -- global clock
    u       : in  datain; -- input data
    y       : out dataout); -- filtered output
end component;

begin

  fil : myFilter
        PORT MAP (rstb,clk,u,y); 

  reset_all_bidules : process
  begin
    rstb   <= '0';
    wait for 100 ns;
    while true loop
      rstb <= '1';
      wait for 100 ns;
    end loop;
  end process;

 fast_clk : process
  begin
    clk <= '0';
    wait for 0 ns;
    while true loop
      clk <= '1';
      wait for Tclk/2;
      clk <= '0';
      wait for Tclk/2;
    end loop;
  end process;


  read_file_data : process
     file file_data : text open read_mode is "./DATA.dat";
     file file_data_write : text open write_mode is "./OUT_DATA.dat";
     variable l : line;
     variable tu : datain := 0;
     variable ty : dataout := 0;
   begin
     readline(file_data, l);          -- first line

     wait until rstb='1';
     wait until clk'event and clk='1';       
     while not endfile(file_data) loop
       readline(file_data, l);          -- next line
       read(l, tu);                      -- extract from line l       
       u <= tu;

       wait until clk'event and clk='1';

       ty := y;
       write(l,ty);
       writeline(file_data_write,l);
     end loop;
     wait;
   end process;



end test;

-- Configuration
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_arith.all;

configuration cfg_filter of test_filter is
        for test
        end for;
end cfg_filter;
