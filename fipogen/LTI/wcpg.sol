
__do_wcpg_binding = true;
if (isbound(__wcpg_already_bound)) then {
   if (__wcpg_already_bound) then {
      __do_wcpg_binding = false;
   };
};


if (__do_wcpg_binding) then {
   externalproc(__wcpg, "wcpg_bind.so", (list of constant, list of constant, list of constant, list of constant, integer, integer, integer, constant) -> list of constant);
   __wcpg_already_bound = true;
};

procedure wcpg(Amat, Bmat, Cmat, Dmat, n, p, q, eps) {
	  var res;

	  res = __wcpg(Amat, Bmat, Cmat, Dmat, n, p, q, eps);

	  return res;
};

