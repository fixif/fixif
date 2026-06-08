bCoeffs = [|0xbf401e59ea02c133,
0x3f8039fc4013bf2a,
0x3f606a64806bd000,
0xbf79c628bffaac6d,
0xbf749934c5777693,
0x3f7d91d9ddfe71c6,
0x3f842384ffa4b4a2,
0xbf7aa9af49afc0d3,
0xbf907d5e57006dbe,
0x3f696ba878929aad,
0x3f980201bd9a0902,
0x3f71c8af57176a36,
0xbf9ff4182867236a,
0xbf924554a513e746,
0x3fa3bccffe189650,
0x3fa5687dd11da7d5,
0xbfa6d63ce6f17a53,
0xbfb7922e76caf13a,
0x3fa8e0f312519a45,
0x3fd40fec58770d19,
0x3fdccd132bf5475b,
0x3fd40fec58770d19,
0x3fa8e0f312519a45,
0xbfb7922e76caf13a,
0xbfa6d63ce6f17a53,
0x3fa5687dd11da7d5,
0x3fa3bccffe189650,
0xbf924554a513e746,
0xbf9ff4182867236a,
0x3f71c8af57176a36,
0x3f980201bd9a0902,
0x3f696ba878929aad,
0xbf907d5e57006dbe,
0xbf7aa9af49afc0d3,
0x3f842384ffa4b4a2,
0x3f7d91d9ddfe71c6,
0xbf749934c5777693,
0xbf79c628bffaac6d,
0x3f606a64806bd000,
0x3f8039fc4013bf2a,
0xbf401e59ea02c133|];

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

