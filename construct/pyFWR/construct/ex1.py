# Paramètres
g,T, xi, wc, pi = var('g T xi wc')
Fe=10;Fc=200
values = { pi:3.14159, g:(2*pi*Fc)**2, T:1/Fe, wc:2*pi*Fc, xi:0.5 }

# Coefficients de la fonction de transfert
b0 = g*T^2
b1 = 2*b0
b2 = b0
a0 = 4*xi*wc*T + wc^2*T^2 + 4
a1 = 2*wc^2*T^2 - 8
a2 = -4*xi*wc*T + wc^2*T^2 + 4

# 