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
    -- states     signal xn 1 : state1 := 0;    signal xn 2 : state2 := 0;    signal xn 3 : state3 := 0;    signal xn 4 : state4 := 0;    signal xn 5 : state5 := 0;    signal xn 6 : state6 := 0;    signal xn 7 : state7 := 0;    signal xn 8 : state8 := 0;    signal xn 9 : state9 := 0;    signal xn10 : state10 := 0;    signal xn11 : state11 := 0;    signal xn12 : state12 := 0;    -- intermediate variables     signal T1 : intermediate_var1 := 0;    signal T2 : intermediate_var2 := 0;

begin
    -- intermediate variables    T1 <= (    (xn 7 * 123806) / 2**5 + (xn 8 * 92855) / 2**2 + (xn 9 * 116068) / 2**1 + xn10 * 77379 + (xn11 * 116068) / 2**1 + (xn12 * 92855) / 2**2 + (u    * 123806) / 2**5) / 2**18;    T2 <= (    (xn 1 * (-113552)) / 2**6 + (xn 2 * 106674) / 2**3 + (xn 3 * (-84339)) / 2**1 + xn 4 * 71918 + xn 5 * (-69870) + (xn 6 * 73475) / 2**1) / 2**13;    -- output(s)    y <= (    T1 + T2 * 2**10) / 2**10;

  S1: process(rstb,clk)
  begin
    if rstb = '0' then                  -- asynchronous reset
        xn 1 <= 0;        xn 2 <= 0;        xn 3 <= 0;        xn 4 <= 0;        xn 5 <= 0;        xn 6 <= 0;        xn 7 <= 0;        xn 8 <= 0;        xn 9 <= 0;        xn10 <= 0;        xn11 <= 0;        xn12 <= 0;
    elsif clk'event and clk = '1' then  -- rising clock edge
    -- states    xn 1 <=     xn 2;    xn 2 <=     xn 3;    xn 3 <=     xn 4;    xn 4 <=     xn 5;    xn 5 <=     xn 6;    xn 6 <= (    T1 + T2 * 2**10) / 2**10;    xn 7 <=     xn 8;    xn 8 <=     xn 9;    xn 9 <=     xn10;    xn10 <=     xn11;    xn11 <=     xn12;    xn12 <=     u;
    end if;  
  end process S1;

end RTL;

