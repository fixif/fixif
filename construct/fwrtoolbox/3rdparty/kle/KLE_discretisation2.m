% KLE discretisation from samples
% the input must be a zero mean process 
% matrix form (P) for faster simulation

function [coeffs, LAM ,PHI, rv]= KLE_discretisation2(P, tr_err)
	

	%covariance matrix
	C = (1/(size(P,2)-1))*P*P';

	%eigenvalues and eigenvectors of the covariance matrix

	[PHI LAMBDA] = eig(C);


    
    [LAM INDEX] = sort(diag(LAMBDA),'descend');
    LAMBDA = diag(LAM);
    
    for j = 1:size(PHI,2)
        B(:,j) = PHI(:,INDEX(j)); 
    end
    PHI = B;
        
    
	%trace of the covariance matrix is the sum of all eigenvalues
	TraceC=trace(C);

	%compute the truncation error for the KLE
	Err = 100;
	SUM_LAMBDA = 0;
	J=1;
 
 	while (Err >= tr_err) && (J<=size(LAMBDA,1)),
 		SUM_LAMBDA = SUM_LAMBDA + LAMBDA(J,J);
		Err = 1 - SUM_LAMBDA/TraceC;
		J=J+1;
	end


	% KLE coeffs
    for i=1:J-1  
        x_i(:,i) = sqrt(LAMBDA(i,i))*PHI(:,i);
    end
    

	%%% find the all the RV for the KLE
	lam = 1./diag(sqrt(LAMBDA));
	lam = diag(lam);

	F_lambda = PHI(:,1:J-1) * lam(1:J-1,1:J-1);
	F_lambda = F_lambda';

	MU = F_lambda * P;

    
    LAM = sqrt(LAM);
	coeffs = x_i;
	rv=MU;

