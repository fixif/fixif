library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.STD_LOGIC_arith.all;
use IEEE.STD_LOGIC_SIGNED.all;
library work;
use work.FP_types.all;

entity filter is
  port (
    rstb    : in  std_logic; -- asynchronous reset asynchrone active low
    clk     : in  std_logic; -- global clock
    u       : in  datain; -- input data
    v       : out dataout); -- filtered output
end filter;

architecture RTL of filter is
    -- states     signal xn1 : state1 := 0;    signal xn2 : state2 := 0;    signal xn3 : state3 := 0;    signal xn4 : state4 := 0;    -- intermediate variables     signal T1 : intermediate_var1 := 0;    signal T2 : intermediate_var2 := 0;    signal T3 : intermediate_var3 := 0;    signal T4 : intermediate_var4 := 0;    -- accumulators     signal Acc1 : accumulator1 :=0;    signal Acc2 : accumulator2 :=0;    signal Acc3 : accumulator3 :=0;    signal Acc4 : accumulator4 :=0;    signal Acc5 : accumulator5 :=0;    signal Acc6 : accumulator6 :=0;    signal Acc7 : accumulator7 :=0;    signal Acc8 : accumulator8 :=0;    signal Acc9 : accumulator9 :=0;

begin

  S1: process(rstb,clk)
  begin
    if rstb = '0' then                  -- asynchronous reset
        xn1 <= 0;        xn2 <= 0;        xn3 <= 0;        xn4 <= 0;
    elsif clk'event and clk = '1' then  -- rising clock edge
    -- intermediate variables    Acc1 <= xn1 * 15729;    Acc1 <= Acc1 + (u   * 8386) / 2**15;    T1 <= Acc1/ 2**14;    Acc2 <= xn2 * 15729;    T2 <= Acc2/ 2**14;    Acc3 <= xn3 * 15729;    T3 <= Acc3/ 2**14;    Acc4 <= xn4 * 15729;    T4 <= Acc4/ 2**14;    -- output(s)    Acc9 <= (T1) * 2**15;    y <= Acc9/ 2**15;    -- states    Acc5 <= T1  * 11859;    Acc5 <= Acc5 + (T2) * 2**13;    Acc5 <= Acc5 + (xn1 * 13107) / 2**2;    Acc5 <= Acc5 + (u   * 13539) / 2**14;    xn1 <= Acc5/ 2**13;    Acc6 <= T1  * -9951;    Acc6 <= Acc6 + (T3) * 2**11;    Acc6 <= Acc6 + (xn2 * 16384) / 2**1;    Acc6 <= Acc6 + (u   * 8741) / 2**11;    xn2 <= Acc6/ 2**14;    Acc7 <= T1  * 10571;    Acc7 <= Acc7 + (T4) * 2**10;    Acc7 <= Acc7 + xn3 * 9830;    Acc7 <= Acc7 + (u   * 10654) / 2**8;    xn3 <= Acc7/ 2**14;    Acc8 <= (T1  * -10470) / 2**1;    Acc8 <= Acc8 + xn4 * 11469;    Acc8 <= Acc8 + (u   * 10308) / 2**5;    xn4 <= Acc8/ 2**14;
    end if;  
  end process S1;

end RTL;

