function [ymin, ymax] = WCPG(H,xmin,xmax)
dc = dcgain(H);
[Yimp Timp] = impulse(H,1e5);
b = squeeze(sum(abs(Yimp)));

xm = (xmin+xmax)/2;
xr = (xmax-xmin)/2;

ym = xm*dc;
yr = xr*b;

ymin = ym - yr;
ymax = ym + yr;