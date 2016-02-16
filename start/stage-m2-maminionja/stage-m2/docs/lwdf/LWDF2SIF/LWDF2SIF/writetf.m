function writetf(H, filename)

format long
out = fopen(filename,'w');

n = length(H.num{1});
num = H.num{1};

m = length(H.den{1});
denum = H.den{1};

fprintf(out, 'num \n');
for i=1:n
     fprintf(out, '%54.54e', num(i));
     fprintf(out, '\n');
end
fprintf(out, 'denum \n');
for i=1:m
     fprintf(out, '%54.54e', denum(i));
     fprintf(out, '\n');
end

        
end