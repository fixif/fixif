
Fe = 16000;
Npts = 1024;

Fdebut = 1000;
Ffinal = 5000;

Q = 15;

Te = 1/Fe; 

t = 0:Te:(Npts-1)*Te;

y = 0.9 * chirp(t,Fdebut,(Npts-1)*Te,Ffinal);

yfix = round(y*2^Q);

    FileID = fopen('SignalSource.h','w');    
    
    fprintf(FileID, 'int TabX[%i] = {', Npts);
    
    
for i=1:length(yfix)-1
    
    fprintf(FileID, '%i, \n   ', yfix(i) );

end


    fprintf(FileID, '%i};', yfix(length(yfix)) );
    
    fclose(FileID);
    