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
    -- states     signal xn1 : state1 := 0;    signal xn2 : state2 := 0;    signal xn3 : state3 := 0;    signal xn4 : state4 := 0;    signal xn5 : state5 := 0;    -- intermediate variables     signal T1 : intermediate_var1 := 0;    signal T2 : intermediate_var2 := 0;    signal T3 : intermediate_var3 := 0;    signal T4 : intermediate_var4 := 0;    signal T5 : intermediate_var5 := 0;

begin
    -- intermediate variables    T1 <= (    xn1 * 2**7 + (u   * 99) / 2**13) / 2**7;    T2 <=     xn2;    T3 <=     xn3;    T4 <=     xn4;    T5 <=     xn5;    -- output(s)    y <=     T1;

  S1: process(rstb,clk)
  begin
    if rstb = '0' then                  -- asynchronous reset
        xn1 <= 0;        xn2 <= 0;        xn3 <= 0;        xn4 <= 0;        xn5 <= 0;
    elsif clk'event and clk = '1' then  -- rising clock edge
    -- states    xn1 <= (    (T1  * (-88)) / 2**6 + T2 * 2**1 + xn1 * 2**7 + (u   * 99) / 2**12) / 2**7;    xn2 <= (    (T1  * (-117)) / 2**7 + T3 + xn2 * 2**7 + (u   * 82) / 2**17) / 2**7;    xn3 <= (    (T1  * (-85)) / 2**7 + T4 + xn3 * 2**7 + (u   * 110) / 2**11) / 2**7;    xn4 <= (    (T1  * (-89)) / 2**8 + T5 / 2**2 + xn4 * 2**7 + (u   * 66) / 2**16) / 2**7;    xn5 <= (    (T1  * (-105)) / 2**8 + xn5 * 2**7 + (u   * 105) / 2**9) / 2**7;
    end if;  
  end process S1;

end RTL;

