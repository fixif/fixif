bCoeffs = [|0x3fa3ea3102e2340e,
0x3f65ff8cac113966,
0xbf9edc7b158a682a,
0xbf927862bc974393,
0x3fa24dfe77ce1b12,
0x3fa42e0d3d71dcb8,
0xbfa705264c22b2e2,
0xbfb79f65d382e0c3,
0x3fa82e0dfb949e1d,
0x3fd3f72e3d3509ae,
0x3fdcba1335a78038,
0x3fd3f72e3d3509ae,
0x3fa82e0dfb949e1d,
0xbfb79f65d382e0c3,
0xbfa705264c22b2e2,
0x3fa42e0d3d71dcb8,
0x3fa24dfe77ce1b12,
0xbf927862bc974393,
0xbf9edc7b158a682a,
0x3f65ff8cac113966,
0x3fa3ea3102e2340e|];

aCoeffs = [|
1|];

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




