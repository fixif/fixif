%       the function returns:
%  the Range for the Overflow Probability needed
%  the PDF estimation of the output for all the time dimension
%  the Variance estimation for the output for all the time dimension
function [range, pdf_y, ygrid, var_y]= KLE_range(X, h, P_over)


dim_t = size(h,2);
dim_e = size(h,1);
%NbTrajectories = 10000;
NbTrajectories = floor(size(X,2)./dim_t);


% KLE truncation
tr_err =0;


%total variance
var_out_total = zeros(1,2*dim_t-1);
y_KLE_rp_total = zeros(2*dim_t-1,NbTrajectories);


% a zero mean random process that will be discretized with the KLE
for i=1:dim_e
    
    mean_in = mean(X(i,:)); % consider the input stationary at the first order
    zero_mean_process = X(i,:) - mean_in;
    
    P_in = zeros(dim_t,NbTrajectories );
    % put the input into the matrix format for function call
    for J=1:NbTrajectories
        P_in(:,J) = zero_mean_process((J-1)*dim_t+1:J*dim_t);
    end
    
    [coeffs_in , lambda, phi, MU_in]= KLE_discretisation2(P_in, tr_err);
    
    dim_tr=size(coeffs_in,2);
    
    
    % find the KLE coeffs using the impulse response
    for j=1:dim_tr
        coeffs_KLE_out(:,j) = conv(h(i,:), coeffs_in(:,j));
    end
    
    % variance
    for k=1:2*dim_t-1
        var_out(k) = sum(coeffs_KLE_out(k,:).^2);
        
    end
    
    
    % compute samples for the output from input realizations
    for j=1:2*dim_t-1
        y_KLE_rp(j,:) =  sum(mean_in)*ones(1,size(MU_in,2));
        
        for k=1:dim_tr
            y_KLE_rp(j,:) =  y_KLE_rp(j,:) + coeffs_KLE_out(j,k)*MU_in(k,:);
        end
    end
    
    
    %total variance
    var_out_total = var_out_total + var_out;
    y_KLE_rp_total = y_KLE_rp_total + y_KLE_rp;

    
end


% estimate the PDF using kernel density estimation method

ygrid = linspace(min(min(y_KLE_rp_total)),max(max(y_KLE_rp_total)),1000);

P_y=ksdensity(y_KLE_rp_total(size(h,2),:),ygrid, 'kernel','epanechnikov','npoints', 1000);
    

r = [min(min(y_KLE_rp_total)),max(max(y_KLE_rp_total))];

%%%%% compute the range for the overflow probability
for i=2:size(ygrid,2)/2
    
    
    P_over_neg = trapz(ygrid(1:i),P_y(1:i));
    P_over_pos = trapz(ygrid(size(ygrid,2)-i:size(ygrid,2)),P_y(size(ygrid,2)-i:size(ygrid,2)));
    
    if ((P_over_neg + P_over_pos) > P_over )
        break;
    end
    
    r = [ygrid(i), ygrid(size(ygrid,2)-i)];
end



var_y = var_out_total(size(h,2));
pdf_y = P_y;
range = r;

