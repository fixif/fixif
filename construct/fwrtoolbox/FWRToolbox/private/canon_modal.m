% canon_modal
% based on Matlab 7.0
function [A B C D] = canon_modal(  Aq, Bq, Cq, Dq )
% Modal form
    [V,E] = eig(Aq);
    if isreal(Aq)
        lambda = diag(E);
        % Transformation to modal form based on eigenvectors
        k = 1;
        while k<=length(lambda)
            if imag(lambda(k)) ~= 0
                rel = real(lambda(k));
                iml = imag(lambda(k));
                T(:,k) = real(V(:,k)); 
                T(:,k+1) = imag(V(:,k));
                E(k:k+1,k:k+1) = [rel iml;-iml rel];
                k = k+2;
            else
                T(:,k) = V(:,k);
                k = k+1;
            end
        end
    else
        T = V;
    end
    A = E;
   
B = T\Bq;
C = Cq*T;
D=Dq;