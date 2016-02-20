library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.STD_LOGIC_arith.all;
use IEEE.STD_LOGIC_SIGNED.all;
library work;
use work.FP_types.all;

entity myFilter is
  port (
    rstb    : in  std_logic; -- asynchronous reset asynchrone active low
    clk     : in  std_logic; -- global clock
    u       : in  datain; -- input data
    y       : out dataout); -- filtered output
end myFilter;

architecture RTL of myFilter is
    -- states     signal xn1 : state1 := 0;    signal xn2 : state2 := 0;    -- intermediate variables     signal T1 : intermediate_var1 := 0;    signal T2 : intermediate_var2 := 0;

begin
    -- intermediate variables    T1 <= (    xn1 * 2**7 + u * 2**5) / 2**8;    T2 <=     xn2;    -- output(s)    y <=     T1;

  S1: process(rstb,clk)
  begin
    if rstb = '0' then                  -- asynchronous reset
        xn1 <= 0;        xn2 <= 0;
    elsif clk'event and clk = '1' then  -- rising clock edge
    -- states    xn1 <= (    T1  * (-116) + T2 * 2**6 + xn1 * 2**5 + u * 2**5) / 2**5;    xn2 <= (    T1  * (-127) + xn2 * 2**7 + u * 2**6) / 2**7;
    end if;  
  end process S1;

end RTL;

