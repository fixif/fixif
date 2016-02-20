function fp = quantif( fl, beta, alpha)

fp = 2^(-beta+alpha+1)*round( 2^(beta-alpha-1)*fl);

if ( max(fp)>=2^alpha ) | ( min(fp)<-2^alpha )
    error(['overflow! beta=' num2str(beta) ' alpha=' num2str(alpha) ' max(fl)=' num2str(max(fl)) ' min(fl)=' num2str(min(fl)) ]);
end