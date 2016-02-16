function writeSIF(R, filename)

format long
out = fopen(filename,'w');

[nt, nt] = size(R.J);
fprintf(out,'J %d %d',nt, nt);
fprintf(out, '\n');
if(nt ~=0)
for i=1:nt
    for j=1:nt
        fprintf(out, '%54.54f', R.J(i,j));
        fprintf(out, '\t');
    end
    fprintf(out, '\n');
end
fprintf(out, '\n');
end


[nx, nt] = size(R.K);
fprintf(out,'K %d %d',nx, nt);
fprintf(out, '\n');
if(nt ~=0 && nx ~= 0)
for i=1:nx
    for j=1:nt
        fprintf(out, '%54.54f', R.K(i,j));
        fprintf(out, '\t');
    end
    fprintf(out, '\n');
end
fprintf(out, '\n');
end

[ny, nt] = size(R.L);
fprintf(out,'L %d %d',ny, nt);
fprintf(out, '\n');
if(nt ~=0 && ny ~= 0)
for i=1:ny
    for j=1:nt
        fprintf(out, '%54.54f', R.L(i,j));
        fprintf(out, '\t');
    end
    fprintf(out, '\n');
end
fprintf(out, '\n');
end

[nt, nx] = size(R.M);
fprintf(out,'M %d %d',nt, nx);
fprintf(out, '\n');
if(nt ~=0 && nx ~= 0)
for i=1:nt
    for j=1:nx
        fprintf(out, '%54.54f', R.M(i,j));
        fprintf(out, '\t');
    end
    fprintf(out, '\n');
end
fprintf(out, '\n');
end

[nx, nx] = size(R.P);
fprintf(out,'P %d %d',nx, nx);
fprintf(out, '\n');
if(nx ~=0 && nx ~= 0)
for i=1:nx
    for j=1:nx
        fprintf(out, '%54.54f', R.P(i,j));
        fprintf(out, '\t');
    end
    fprintf(out, '\n');
end
fprintf(out, '\n');
end

[ny, nx] = size(R.R);
fprintf(out,'R %d %d',ny, nx);
fprintf(out, '\n');
if(ny ~=0 && nx ~= 0)
for i=1:ny
    for j=1:nx
        fprintf(out, '%54.54f', R.R(i,j));
        fprintf(out, '\t');
    end
    fprintf(out, '\n');
end
fprintf(out, '\n');
end

[nt, nu] = size(R.N);
fprintf(out,'N %d %d',nt, nu);
fprintf(out, '\n');
if(nt ~=0 && nu ~= 0)
for i=1:nt
    for j=1:nu
        fprintf(out, '%54.54f', R.N(i,j));
        fprintf(out, '\t');
    end
    fprintf(out, '\n');
end
fprintf(out, '\n');
end

[nx, nu] = size(R.Q);
fprintf(out,'Q %d %d',nx, nu);
fprintf(out, '\n');
if(nu ~=0 && nx ~= 0)
for i=1:nx
    for j=1:nu
        fprintf(out, '%54.54f', R.Q(i,j));
        fprintf(out, '\t');
    end
    fprintf(out, '\n');
end
fprintf(out, '\n');
end

[ny, nu] = size(R.S);
fprintf(out,'S %d %d',ny, nu);
fprintf(out, '\n');
if(ny ~=0 && nu ~= 0)
for i=1:ny
    for j=1:nu
        fprintf(out, '%54.54f', R.S(i,j));
        fprintf(out, '\t');
    end
    fprintf(out, '\n');
end
fprintf(out, '\n');
end


end
