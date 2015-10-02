#!/bin/sh

if [ $# -eq 1 ]
then
    target=$1
    option1=""
    option2=""
else
    target="berlioz"
    option1="-p 8888"
    option2="-P 8888"
fi

#ssh $option1 $target 'rm -rf /dsk/l1/misc/ravoson/synopsys/*'
rm -rf /dsk/l1/misc/ravoson/synopsys/*
#scp $option2 *.vhd synth.tcl $target:~/tmp/fixed_point/
cp *.vhd synth.tcl /dsk/l1/misc/ravoson/synopsys/
cd /dsk/l1/misc/ravoson/synopsys/;source /users/soft/synopsis/synopsys2013.sh;dc_shell -f synth.tcl
#scp $option2 $target:~/tmp/fixed_point/*.txt .
cp /dsk/l1/misc/ravoson/synopsys/*.txt .
grep "Total cell area:" area.txt >> result
grep "data arrival time" timing.txt >> result
grep "Total" power.txt | tail -1 >> result
