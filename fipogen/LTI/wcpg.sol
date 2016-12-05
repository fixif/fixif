   
externalproc(__wcpg, "fipogen/LTI/wcpg_bind.so", (list of constant, list of constant, list of constant, list of constant, integer, integer, integer, constant) -> list of constant);

procedure wcpg(Amat, Bmat, Cmat, Dmat, n, p, q, eps) {
	  var res;

	  res = __wcpg(Amat, Bmat, Cmat, Dmat, n, p, q, eps);

	  return res;
};

