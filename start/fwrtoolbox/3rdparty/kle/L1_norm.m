function [range]=L1_norm(dynSourceMin, dynSourceMax, Hg, NbPtsH)

Coeff = abs(impulse(Hg, NbPtsH));
range = [sum(Coeff) * dynSourceMin , sum(Coeff) * dynSourceMax];
