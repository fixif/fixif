bCoeffs = [|
0.000187872684291354489442144037880666474 ,
-0.000563567035769839408398951263734488748 ,
0.000375694354461414089553505935015209616 ,
0.000375694354461414089553505935015209616 ,
-0.000563567035769839408398951263734488748 ,
0.000187872684291354489442144037880666474 
|];

aCoeffs = [|
1,
-4.989216395071317755594009213382378220558 ,
9.956976990745104671987064648419618606567 ,
-9.935631971923312377725778787862509489059 ,
4.957198554483320585006822511786594986916 ,
-0.989327178227829562295880805322667583823
|];

b = 0;
for i from 0 to length(bCoeffs) - 1 do {
    b = b + bCoeffs[i] * _x_^i;
};
b = horner(b);

a = 0;
for i from 0 to length(aCoeffs) - 1 do {
    a = a + aCoeffs[i] * _x_^i;
};
a = horner(a);

