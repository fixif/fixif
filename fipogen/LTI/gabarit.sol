
dodebug = false;

procedure debug(l = ...) {
	  var i;
	  if (dodebug) then {
	     for i in l do write(i);
	     write("\n");
	  };
};

suppressmessage(183);

procedure productOfDenominators(p) {
	  var res, i, c, d;

	  res = 1;
	  for i from 0 to degree(p) do {
	      c = coeff(p, i);
	      d = denominator(c);
	      res = res * d;
	  };

	  if (res < 0) then {
	     res = -res;
	  };

	  return res;
};

/* Given a polynomial p, computes a polynomial q and an integer n such
   that

   q(z)/z^n = p(1/z)

   Does not work for anything else but a polynomial.
   
*/
procedure applyReciprocal(p) {
          var q, n, k;

          n = degree(p);
          q = 0;
          for k from 0 to n do {
              q = q + _x_^k * coeff(p, n - k);
          };
          q = horner(q);

          return { .q = q, .n = n };
};


/* Given a transfer function

   H(z) = b(z)/a(z)

   computes two polynomials p and q such that

   p(z)/q(z) = |H(z)|^2 = (b(z) * b(1/z))/(a(z) * a(1/z))

   Does not work if b and a are no polynomials.

*/
procedure modulusSquareFilter(b, a) {
          var p, q, bres, ares, bn, an, br, ar;

          bres = applyReciprocal(b);
          ares = applyReciprocal(a);

          br = bres.q; bn = bres.n;
          ar = ares.q; an = ares.n;

          p = b * br;
          q = a * ar;

          if ((an - bn) >= 0) then {
             p = _x_^(an - bn) * p;
          } else {
             q = _x_^(-(an - bn)) * q;
          };
          p = horner(p);
          q = horner(q);
          
          return { .p = p; .q = q };
};

/* Generic complex addition

   Given two structures a and b, both containing
   two fields .re and .im, a procedure baseAdd and
   an opaque data variable, computes the complex
   sum a + b, using baseAdd on both fields, providing
   data as third argument to baseAdd.

   Returns a structure with two fields .re and .im.

   Does not work for any inputs not having the right
   types.

*/
procedure genericComplexAdd(a, b, baseAdd, data) {
          return { .re = baseAdd(a.re, b.re, data), .im = baseAdd(a.im, b.im, data) };
};

/* Generic complex subtraction

   Given two structures a and b, both containing
   two fields .re and .im, a procedure baseSub and
   an opaque data variable, computes the complex
   difference a - b, using baseSub on both fields, providing
   data as third argument to baseSub.

   Returns a structure with two fields .re and .im.

   Does not work for any inputs not having the right
   types.

*/
procedure genericComplexSub(a, b, baseSub, data) {
          return { .re = baseSub(a.re, b.re, data), .im = baseSub(a.im, b.im, data) };
};

/* Generic complex multiplication

   Given two structures a and b, both containing
   two fields .re and .im, procedures baseMul, baseAdd and
   baseSub and an opaque data variable, computes the complex
   product a * b, using the base procedures on the fields, providing
   data as third argument to them.

   Returns a structure with two fields .re and .im.

   Does not work for any inputs not having the right
   types.

*/
procedure genericComplexMul(a, b, baseMul, baseAdd, baseSub, data) {
          return { .re = baseSub(baseMul(a.re, b.re, data), baseMul(a.im, b.im, data), data),
                   .im = baseAdd(baseMul(a.re, b.im, data), baseMul(a.im, b.re, data), data) };
};


/* Given a real polynomial p, an opaque data type X,
   a procedure baseCoeff transforming real coefficients into
   the same data type as the one of X, two procedures baseAdd
   and baseMul, taking two arguments of that opaque data type
   and an additional opaque data argument, evaluates the
   polynomial p in X.

   Returns p(X) as the opaque data type.

*/
procedure genericHorner(p, X, baseCoeff, baseAdd, baseMul, data) {
          var Y, n, i;

          n = degree(p);
          if (n < 0) then {
             Y = baseCoeff(0, data);
          } else {
            if (n == 0) then {
               Y = baseCoeff(coeff(p, 0), data);
            } else {
               Y = baseCoeff(coeff(p, n), data);
               for i from n - 1 to 0 by -1 do {
                   Y = baseAdd(baseCoeff(coeff(p, i), data), baseMul(X, Y, data), data);
               };
            };
          };

          return Y;
};

/* Given two rational functions a and b, both represented as
   structures containing two fields .p and .q representing the
   numerator and denominator polynomials respectively, computes the
   sum c = a + b, returning it as a structure containing two fields .p
   and .q.

   The additional data argument is ignored.
*/
procedure rationalAdd(a, b, data) {
          var p, q, r, s, u, v;
          p = a.p;
          q = a.q;
          r = b.p;
          s = b.q;
          if (q - s == 0) then {
             u = p + r;
             v = s;
          } else {
             u = p * s + r * q;
             v = q * s;
          };
          return { .p = u, .q = v };
};

/* Given two rational functions a and b, both represented as
   structures containing two fields .p and .q representing the
   numerator and denominator polynomials respectively, computes the
   difference c = a - b, returning it as a structure containing two fields .p
   and .q.

   The additional data argument is ignored.
*/
procedure rationalSub(a, b, data) {
          var p, q, r, s, u, v;
          p = a.p;
          q = a.q;
          r = b.p;
          s = b.q;
          if (q - s == 0) then {
             u = p - r;
             v = s;
          } else {
             u = p * s - r * q;
             v = q * s;
          };
          return { .p = u, .q = v };
};

/* Given two rational functions a and b, both represented as
   structures containing two fields .p and .q representing the
   numerator and denominator polynomials respectively, computes the
   product c = a * b, returning it as a structure containing two fields .p
   and .q.

   The additional data argument is ignored.
*/
procedure rationalMul(a, b, data) {
          var u, v;
          u = a.p * b.p;
          v = a.q * b.q;
          if (u == 0) then {
             v = 1;
          };
          return { .p = u, .q = v };
};

/* Given two functions a and b, mapping the reals to complex numbers,
   each of the form

   p/q + j * r/s

   computes the sum c = a + b, also of this form.

   Technically a and b are supposed to be structures, each
   containing two fields .re and .im that are themselves
   structures containing each two fields .p and .q for
   the numerator and denominator polynomials.

   The additional data field is ignored.

*/
procedure complexAdd(a, b, data) {
          return genericComplexAdd(a, b, rationalAdd, data);
};

/* Given two functions a and b, mapping the reals to complex numbers,
   each of the form

   p/q + j * r/s

   computes the product c = a * b, also of this form.

   Technically a and b are supposed to be structures, each
   containing two fields .re and .im that are themselves
   structures containing each two fields .p and .q for
   the numerator and denominator polynomials.

   The additional data field is ignored.

*/
procedure complexMul(a, b, data) {
          return genericComplexMul(a, b, rationalMul,
                                   rationalAdd,
                                   rationalSub,
                                   data);
};

/* Given a real number c, writes that real in the form

   c/1 + j * 0/1

   by forming a structure that can be taken in argument
   by the functions complexAdd and complexMul.

   The additional data field is ignored.

*/
procedure complexConst(c, data) {
          return { .re = { .p = c, .q = 1 }, .im = { .p = 0, .q = 1 } };
};

/* Let the unity circle be expressed as

   exp(j * omega) = (1 - t^2)/(1 + t^2) + j * (2 * t)/(1 + t^2)

   where t = tan(omega / 2).

   Given a polynomial p with real coefficients, mapping the reals onto
   the reals, returns a function of the form

   p/q + j * r/s

   such that

   p(t) / q(t) + j * r(t) / s(t) = p((1 - t^2)/(1 + t^2) + j * (2 * t)/(1 + t^2))

*/
procedure composePolynomialRationalParametrization(p) {
          return genericHorner(p, { .re = { .p = 1 - _x_^2, .q = 1 + _x_^2 },
                                    .im = { .p = 2 * _x_, .q = 1 + _x_^2 } },
                               complexConst,
                               complexAdd,
                               complexMul,
                               "blyad");
};

/* Given a real number c, returns the rational function

   c/1

   The additional data argument is ignored.
   
*/
procedure rationalConst(c, data) {
          return { .p = c, .q = 1 };
};


/* Given a polynomial p with real coefficients, mapping the reals onto
   the reals, computes the rational function

   r(xi)/s(xi) = p((1 - 2 * xi) / (xi * (1 - xi)))

*/
procedure composePolynomialInXi(p) {
          return genericHorner(p, { .p = 1 - 2 * _x_, .q = _x_ * (1 - _x_) },
                               rationalConst,
                               rationalAdd,
                               rationalMul,
                               "blyad");
};


/* Given b and a be two polynomials with real coefficients
   defining a filter

   H(z) = b(z) / a(z)

   returns a rational function

   p / q,

   as a structure with two fields .p and .q, each containing a
   polynomial with real coefficients, mapping the reals onto the
   reals.

   These two polynomials satisfy

   p(xi(t(omega))) / q(xi) = |H(exp(j * omega)|^2

   where

   t(omega) = tan(omega / 2)

   and

   xi(t) = (t + 2 - sqrt(t^2 + 4))/(2 * t).

   This means, with xi ranging in [0;1], t ranges in [-infty;infty]
   and omega ranges in [-pi;pi].

*/
procedure modulusSquareFilterInXi(b, a) {
          var hsq, P, Q, PR, QR, prp, prq, qrp, qrq, gp, gq;
          var up, uq, vp, vq, bp, bq, nbp, nbq;
	  var dp, dq;

          hsq = modulusSquareFilter(b, a);

          P = composePolynomialRationalParametrization(hsq.p);
          Q = composePolynomialRationalParametrization(hsq.q);

          PR = P.re; QR = Q.re;
          prp = PR.p; prq = PR.q;
          qrp = QR.p; qrq = QR.q;

          if (prq - qrq == 0) then {
             gp = prp;
             gq = qrp;
          } else {
             if (prp - qrp == 0) then {
                gp = qrq;
                gq = prq;
             } else {
                gp = prp * qrq;
                gq = prq * qrp;
             };
          };
          gp = horner(gp);
          gq = horner(gq);

          u = composePolynomialInXi(gp);
          v = composePolynomialInXi(gq);

          up = u.p; uq = u.q;
          vp = v.p; vq = v.q;

          if (uq - vq == 0) then {
             bp = up;
             bq = vp;
          } else {
             if (up - vp == 0) then {
                bp = vq;
                bq = uq;
             } else {
                bp = up * vq;
                bq = vp * uq;
             };
          };
          bp = horner(bp);
          bq = horner(bq);

	  ggt = gcd(bp, bq);

	  nbp = horner(simplify(horner(bp / ggt)));
	  nbq = horner(simplify(horner(bq / ggt)));
	  if ((degree(nbp) >= 0) &&
	      (degree(nbq) >= 0)) then {
	      bp = nbp;
	      bq = nbq;
	  };

	  dp = productOfDenominators(bp);
	  dq = productOfDenominators(bq);

	  bp = horner((dp * dq) * bp);
	  bq = horner((dp * dq) * bq);
	  
          return { .p = bp, .q = bq };
};

procedure provePolynomialPositiveAtPoint(p, a) {
	  var res, Y, oldRationalMode;

	  Y = p([a]);
	  if (inf(Y) >= 0) then {
	     res = true;
	  } else {
	    if (sup(Y) <= 0) then {
	       res = false;
	    } else {
	       oldRationalMode = rationalmode;
	       rationalmode = on!;
	       pa = p(a);
	       Y = evaluate(pa, 1);
	       rationalmode = oldRationalMode!;
	       if (inf(Y) >= 0) then {
	       	  res = true;
	       } else {
	       	  res = false;
	       };
	    };
	  };
	  return res;
};

procedure wrappednumberrootsinner(p, dom) {
	  var nz, oldPrec, pp, i, oldDisplay;
	  var t;
	  
	  pp = prec;
	  for i from 0 to degree(p) do {
	      pp = max(pp, precision(coeff(p, i)));
	  };

	  oldPrec = prec;
	  prec = min(3 * pp, 24 * oldPrec)!;

	  t = time({ nz = numberroots(p, dom); });

	  prec = oldPrec!;
	  
	  return nz;
};

procedure wrappednumberrootstimed(p, dom) {
	  var res, i, Emin, q;

	  Emin = exponent(coeff(p, 0));
	  for i from 1 to degree(p) do {
	      Emin = min(Emin, exponent(coeff(p, i)));
	  };

	  q = 2^(-Emin) * p;

	  res = wrappednumberrootsinner(q, dom);

	  return res;
};

procedure wrappednumberroots(p, dom) {
	  var res, t;
	  var oldDisplay;

	  debug("starting wrappednumberroots");

	  t = time({ res = wrappednumberrootstimed(p, dom); }); 

	  debug("wrappednumberroots gave res = ", res, " and took ", ceil(1000 * t), "ms");

	  return res;
};

procedure wrappednumberrootsnomultiplicities(p, dom) {
	  var q, d;
	  var res;

	  res = wrappednumberroots(p, dom);

	  if (res > 0) then {
	      q = horner(simplify(horner(p / gcd(p, diff(p)))));
	      d = productOfDenominators(q);
	      q = horner(simplify(horner(d * q)));
	      res = wrappednumberroots(q, dom);
	  };

	  return res;
};

procedure provePolynomialPositiveBasicInnerWrap(p, dom) {
	  var res, a, b, v, h, t, tt, g, h;
	  var nz, dg, dh, rg, rh;

	  a = inf(dom);
	  b = sup(dom);

	  h = round((b - a) / 500, prec, RU);
	  t = true;
	  v = a;
	  while (t && (v <= b)) do {
	  	tt = provePolynomialPositiveAtPoint(p, v);
		if (!tt) then {
		   t = false;
		} else {
		   v = round(v + h, prec, RU);
		};
	  };
	  if (t) then {
	     t = provePolynomialPositiveAtPoint(p, a);
	  };
	  if (t) then {
	     t = provePolynomialPositiveAtPoint(p, b);
	  };

	  if (t) then {
	     nz = wrappednumberroots(p, dom);
	     if (nz > 0) then {
	     	if (nz == 1) then {
		   t = provePolynomialPositiveAtPoint(p, a);
		   if (t) then {
		      t = provePolynomialPositiveAtPoint(p, b);
		      if (t) then {
		      	 res = true;
		      } else {
		      	 res = false;
		      };
		   } else {
		      res = false;
		   };
		} else {
		   g = horner(gcd(p, diff(p)));
		   h = horner(simplify(horner(p / g)));
		   if ((degree(g) > 1) && (degree(h) > 1)) then {
		       dg = productOfDenominators(g);
		       dh = productOfDenominators(h);
		       g = horner(dg * g);
		       h = horner(dh * h);
		       rg = provePolynomialPositiveBasicInner(g, dom);
		       if (rg) then {
		       	  rh = provePolynomialPositiveBasicInner(h, dom);
			  if (rh) then {
			    res = true;
			  } else {
			    res = false;
			  };
		       } else {
		       	 g = horner(-g);
			 h = horner(-h);
			 rg = provePolynomialPositiveBasicInner(g, dom);
			 if (rg) then {
			    rh = provePolynomialPositiveBasicInner(h, dom);
			    if (rh) then {
			      res = true;
			    } else {
			      res = false;
			    };
			 } else {
			    res = false;
			 };
		       };
		   } else {
		      res = false;
                   };
		};
	     } else {
	        res = true;
	     };
	  } else {
	    res = false;
	  };

	  return res;
};

procedure provePolynomialPositiveBasicInner(p, dom) {
	  var res;

	  debug("Starting provePolynomialPositiveBasicInner");

	  res = provePolynomialPositiveBasicInnerWrap(p, dom);

	  debug("provePolynomialPositiveBasicInner finished, res = ", res);


	  return res;
};

procedure provePolynomialPositiveBasicRecurse(p, dom, n) {
	  var res;
	  var sda, sdb, m;

	  res = provePolynomialPositiveBasicInner(p, dom);

	  if ((!res) && (n > 0)) then {
	     m = min(max(round(mid(dom), prec, RN), inf(dom)), sup(dom));
	     sda = [inf(dom);m];
	     sdb = [m;sup(dom)];
	     res = provePolynomialPositiveBasicRecurse(p, sda, n - 1);
	     if (res) then {
	     	res = provePolynomialPositiveBasicRecurse(p, sdb, n - 1);
	     };
	  };

	  return res;
};

procedure provePolynomialPositiveBasic(p, dom) {
	  var res;
	  res = provePolynomialPositiveBasicRecurse(p, dom, 8);
	  return res;
};

procedure __provePolynomialPositiveInner(p, dom) {
	  var res, q, r, i, delta, t;

	  q = 0;
	  for i from 0 to degree(p) do {
	      q = q + round(coeff(p,i),2 * prec,RN) * _x_^i;
	  };
	  q = horner(q);
	  
	  r = p - q;
	  if (r == 0) then {
	     delta = [0];
	  } else {
	     delta = r(dom);
	  };
	  q = horner(inf(delta) + q);

	  t = provePolynomialPositiveBasic(q, dom);
	  if (t) then {
	     res = true;
	  } else {
	     if (r == 0) then {
	     	res = false;
	     } else {
	        res = provePolynomialPositiveBasic(p, dom);
             };
	  };

	  return res;
};

procedure mydirtyfindzerosinner(f, dom) {
	  var res, a;

	  res = dirtyfindzeros(f, dom);

	  for a in [| 0, inf(dom), sup(dom), mid(dom) |] do {
	     if (a in dom) then {
	        if (0 in evaluate(f, [a])) then {
	     	   res = a .: res;
	        };
	     };
	  };

	  return res;
};

procedure mydirtyfindzerostimed(f, dom) {
	  var r, res, a, b, c, h, sdom;

	  a = inf(dom);
	  b = sup(dom);
	  h = round((b - a) / 16,prec,RU);
	  res = [||];
	  for c from a to b - h by h do {
	      sdom = [ max(a, c); min(b, c + h) ];
	      r = mydirtyfindzerosinner(f, sdom);
	      res = res @ r;
	  };

	  return res;
};

procedure mydirtyfindzeros(f, dom) {
	  var res, t;

	  t = time({ res = mydirtyfindzerostimed(f, dom); });
	  
	  return res;
};

procedure __polynomialsZerosSafe(p, dom) {
	  var nbz, res, sdomA, sdomB, m;
	  var oldPoints, found;

	  nbz = wrappednumberrootsnomultiplicities(p, dom);

	  if (nbz == 0) then {
	     res = [||];
	  } else {
	    if (nbz == 1) then {
	       oldPoints = points;
	       found = false;
	       while ((!found) && (points <= 32 * oldPoints)) do {
	       	     res = mydirtyfindzeros(p, dom);
		     if (length(res) > 0) then {
		     	found = true;
		     } else {
		        points = ceil(ceil(points * 1.5)/2)*2 + 1;
		     };
	       };
	       if (!found) then {
	       	  res = mydirtyfindzeros(horner(simplify(horner(p/gcd(p,diff(p))))), dom);
	       };
	       points = oldPoints!;
	    } else {
	      m = min(max(round(mid(dom), prec, RN), inf(dom)), sup(dom));
	      sdomA = [inf(dom);m];
	      sdomB = [m;sup(dom)];
	      res = __polynomialsZerosSafe(p, sdomA) @ __polynomialsZerosSafe(p, sdomB);
	    };
	  };
	  return res;
};

procedure polynomialZerosInner(poly, dom) {
	  var d, p;
	  var nbz, res;
	  var oldPoints;
	  var t;

	  d = productOfDenominators(poly);
	  p = horner(d * poly);

	  oldPoints = points;
	  points = min(1001, oldPoints)!;
	  res = mydirtyfindzeros(p, dom);
	  points = oldPoints!;

	  t = time({ nbz = wrappednumberrootsnomultiplicities(p, dom); });

	  if (length(res) < nbz) then {

	     t = time({ res = __polynomialsZerosSafe(p, dom); });

	  };

	  return res;
};

procedure polynomialZeros(poly, dom) {
	  var res;
	  var oldPoints;

	  oldPoints = points;
	  points = min(oldPoints, ceil(ceil(degree(poly) * 2 * 1.05)/2)*2 + 1)!;

	  res = polynomialZerosInner(poly, dom);

	  if (0 in dom) then {
	     if (0 in evaluate(poly,[0])) then {
	     	res = 0 .: res;
	     };
	  };

	  res = sort(res);

	  points = oldPoints!;

	  return res;
};

procedure basicZeros(p, dom) {
          var res;
	  var oldPrec;

	  oldPrec = prec;
	  prec = ceil(1.05 * prec)!;

          if (degree(p) < 0) then {
             res = mydirtyfindzeros(p, dom);
          } else {
             res = polynomialZeros(p, dom);
          };

	  oldPrec = prec!;
	  
          return res;
};

procedure blowPointToInterval(z, p, a, b) {
          var pz;
	  var oldPrec;
	  
          oldPrec = prec;
	  prec = 2 * p!;
          if (z == 0) then {
             pz = [ -2^(-p); 2^(-p) ];
          } else {
             if (z > 0) then {
                pz = [ max(a, round(z * (1 - 2^(-p)),p,RD)); min(b, round(z * (1 + 2^(-p)),p,RU)) ];
             } else {
                pz = [ max(a, round(z * (1 + 2^(-p)),p,RD)); min(b, round(z * (1 - 2^(-p)),p,RU)) ];
             };
          };
	  prec = oldPrec!;

          return pz;
};

procedure functionZerosSafe(p, dom) {
          var rawZeros, oldPrec, res, z, pz, y;
	  var oldPoints;
	  
          res = [||];

          oldPrec = prec;
	  oldPoints = points;
          prec = 4 * prec!;
	  points = ceil(ceil(points * 1.05)/2)*2 + 1!;
          rawZeros = basicZeros(p, dom);
          prec = oldPrec!;
	  points = oldPoints!;
          
          for z in rawZeros do {
              pz = blowPointToInterval(z, 2 * prec, inf(dom), sup(dom));
              y = p(pz);
              if (inf(y) * sup(y) <= 0) then {
                 res = pz .: res;
              };
          };

          return res;
};

procedure functionZerosLazy(p, dom) {
          var rawZeros, oldPrec, res, z, pz, y;
	  var oldPoints;
	  
          res = [||];

          oldPrec = prec;
	  oldPoints = points;
          prec = 4 * prec!;
	  points = max(301, ceil(ceil(points * 1.05)/2)*2 + 1)!;
          rawZeros = mydirtyfindzeros(p, dom);
          prec = oldPrec!;
	  points = oldPoints!;
          
          for z in rawZeros do {
              pz = blowPointToInterval(z, 2 * prec, inf(dom), sup(dom));
              y = p(pz);
              if (inf(y) * sup(y) <= 0) then {
                 res = pz .: res;
              };
          };

          return res;
};

procedure functionZerosTimed(p, dom, lazy) {
	  var res;

	  if (lazy) then {
	     res = functionZerosLazy(p, dom);
	  } else {
	     res = functionZerosSafe(p, dom);
	  };

	  return res;
};

procedure functionZeros(p, dom, lazy) {
	  var res, t;

	  t = time({ res = functionZerosTimed(p, dom, lazy); });

	  return res;
};

procedure functionNegativeAbscissaInnerWithLaziness(q, dom, lazy) {
          var pderiv, Z, z, y, res;
	  var p;
	  var t;

	  p = horner(q);

          res = [||];
          
          pderiv = diff(p);
          Z = functionZeros(pderiv, dom, lazy) @ [| blowPointToInterval(inf(dom), 2 * prec, inf(dom), sup(dom)), blowPointToInterval(sup(dom), 2 * prec, inf(dom), sup(dom)) |];
          for z in Z do {
	      t = time({ y = evaluate(horner(p(inf(z) + (sup(z) - inf(z)) * (_x_ + 0.5))),[-0.5;0.5]); });

	      if ((sup(y) <= 0) && (inf(y) < 0)) then {
	      	 res = { .failurePoint = z, .failureDomain = dom } .: res;
	      };
          };
          
          return res;
};

procedure functionNegativeAbscissaInner(q, dom) {
	  var res;

	  res = functionNegativeAbscissaInnerWithLaziness(q, dom, true);
	  if (res == [||]) then {
	     res = functionNegativeAbscissaInnerWithLaziness(q, dom, false);
	  };

	  return res;
};

procedure functionNegativeAbscissaTimed(q, dom) {
	  var res, a, b, c, h, sdom, r;

	  if (0 in dom) then {
	     res = [||];
	     a = inf(dom);
	     b = sup(dom);
	     h = round((b - a) / 5,prec,RU);
	     for c from a to b by h do {
	     	 sdom = [ max(a, c); min(b, round(c + h, prec, RU)) ];
		 r = functionNegativeAbscissaInner(q, sdom);
		 res = res @ r;
	     };
	  } else {
	     res = functionNegativeAbscissaInner(q, dom);
	  };

	  return res;
};

procedure functionNegativeAbscissa(p, dom) {
	  var res, t;

	  debug("Starting functionNegativeAbscissa");

	  t = time({ res = functionNegativeAbscissaTimed(p, dom); });

	  debug("functionNegativeAbscissa yielded ", res, " and took ", ceil(1000 * t), "ms");

	  return res;
};

/* Test whether the polynomial p with real coefficients,
   mapping the reals onto the reals, stays positive for
   all arguments taken in the domain dom.

   Returns a structure containing two fields .okay and .failures,
   explained below.

   There may be false negatives (the polynomial stays positive over
   all arguments but false is returned) but there must not be any
   false positives.

   The .okay field of the returned structure indicates whether or not
   p stays positive over dom. It contains a boolean.

   If the .okay field is true, the .failure field is an empty list.
   Otherwise, the .failure field contains a list of intervals, each
   enclosing a point where the polynomial is negative.
   The list does not need to be exhaustive, returning an empty list
   is authorized, too.
   
*/
procedure provePolynomialPositive(poly, dom) {
          var q, r, delta, pr, oldPrec, c, cc, t, p;
	  var d;

	  d = productOfDenominators(poly);
          p = horner(d * poly);

          q = 0;
          for i from 0 to degree(p) do {
              c = coeff(p, i);
              oldPrec = prec;
              prec = 2 * oldPrec!;
              cc := c;
              pr = precision(cc);
              prec = oldPrec!;
              q = q + round(c, max(prec * 2, pr), RN) * _x_^i;
          };
          q = horner(q);
          r = p - q;

          if (r == 0) then {
             delta = [0];
          } else {
             delta = r(dom);
          };
          q = horner(inf(delta) + q);
          
          t = __provePolynomialPositiveInner(q, dom);

          return t;
};

procedure provePolynomialPositiveWithFailureReport(poly, dom) {
          var t, res, failures;
	  var oldDisplay;

          t = provePolynomialPositive(poly, dom);

          if (t) then {
             res = { .okay = true; .failures = [||] };
          } else {
             failures = functionNegativeAbscissa(horner(poly), dom);
             res = { .okay = false; .failures = failures };
          };

          return res;
};

procedure checkRatioPolynomialsBetweenMinusOneAndOne(p, q, dom) {
          var res, y, r;
          
          /* We have to establish the fact that

             forall xi in dom . -1 <= p(xi)/q(xi) <= 1

             Start by establishing that q is not the zero polynomial.
             
          */
          if (horner(q) == 0) then {
             /* Here, q is the zero polynomial. The property cannot be
                satisfied.
             */
             res = { .okay = false; .failures = [| { .failurePoint = [mid(dom)], .failureDomain = dom } |] };
          } else {
             /* Here q is not the zero polynomial.

                Continue by checking whether dom is reduced to one point.

                If dom is reduced to one point, we may just evaluate
                p/q at that point and check.

             */
             if (inf(dom) == sup(dom)) then {
                y = (p/q)(dom);
                if (y in [-1;1]) then {
                   res = { .okay = true, .failures = [||] };
                } else {
                   res = { .okay = false, .failures = [| { .failurePoint = dom, .failureDomain = dom } |] };
                };
             } else {
                /* Here, dom is not reduced to one point. As it is an
                   interval, we may use continuity arguments (at least on
                   one side).

		   If

		   forall xi in dom . (q^2 - p^2)(xi) >= 0

		   then

		   forall xi in dom . p^2(xi) <= q^2(xi)

		   meaning that

		   forall xi in dom . (p^2/q^2)(xi) <= 1,

		   - at least by continuity -

		   which implies that

		   forall xi in dom . -1 <= (p/q)(xi) <= 1

                */
		r = horner(q^2 - p^2);
		res = provePolynomialPositiveWithFailureReport(r, dom);
             };
          };

          return res;
};

procedure checkRatioPolynomialsBetweenBoundsHammer(p, q, dom, betaInf, betaSup) {
          var betaMid, pprime, qprime, res, betaPrime, psecond, qsecond, y;

          /* If betaInf > betaSup, the property must be false

             If betaInf = betaSup, p/q must be constant, which
             we can exclude in our case. 

          */
          if (betaInf >= betaSup) then {
             res = { .okay = false; .failures = [| { .failureDomain = dom, .failurePoint = [mid(dom)] } |] };
          } else {
              /* Here, we always have betaInf <= betaSup.
	      
	         We start by a simple evaluation test.

		 We evaluate p/q over dom using interval
		 arithmetic. If the result stays between the bounds,
		 everything's fine.
		 
              */
              y = (p/q)(dom);
              if ((betaInf <= inf(y)) && (sup(y) <= betaSup)) then {
                 res = { .okay = true; .failures = [||] };
              } else {
	         /* We have betaInf <= betaSup and our simple
	            evaluation test has failed.
		   
                    Translate the problem along the y-axis:

	            betaInf <= p/q <= betaSup

	            is equivalent to

	            betaInf - betaMid <= (p - betaMid * q)/q <= betaSup - betaMid.

	            With betaMid = (betaInf + betaSup) / 2, we have

		    betaInf - betaMid = - (betaSup - betaMid).

		    Therefore we can reduce the problem to

		    -betaPrime <= pprime/qprime <= betaPrime

		    with

		    betaPrime = (betaSup - betaInf) / 2

		    and

		    pprime = p - betaMid * q

		    and

		    qprime = q.

		    Remark that as betaInf <= betaSup, betaPrime >= 0.

	         */
	         betaMid = (betaInf + betaSup) / 2;
	         betaPrime = round((betaSup - betaInf)/2,prec,RD);
	         pprime = p - betaMid * q;
	         qprime = q;
	      
	         /* Scale the problem

	            The problem

		    -betaPrime <= pprime/qprime <= betaPrime

		    is equivalent to

		    -1 <= pprime/(betaPrime * qprime) <= 1.

		    In the case when betaPrime is equal to zero,
		    the equivalence does not hold; the code however
		    will anyway answer "failure" in this case.

	         */
                 psecond = horner(pprime);
	         qsecond = horner(betaPrime * qprime);
	      
	         /* Now solve the reduced problem */
	         res = checkRatioPolynomialsBetweenMinusOneAndOne(psecond, qsecond, dom);
     	     };
	  };
	  return res;
};

procedure checkRatioPolynomialsBetweenBoundsLazy(p, q, dom, betaInf, betaSup) {
	  var P, Q, res, t, r;

	  P = p;
	  Q = q;
	  t = provePolynomialPositive(Q, dom);
	  if (!t) then {
	     P = -p;
	     Q = -q;
	     t = provePolynomialPositive(Q, dom);
	  };
	  if (t) then {
	     /* Here Q stays positive over the whole domain dom

	        To show that betaInf <= P/Q <= betaSup,

		we show that

		(i)  betaSup * Q - P >= 0

		and

		(ii) P - betaInf * Q >= 0

	     */
	     r = horner(betaSup * Q - P);
	     t = provePolynomialPositive(r, dom);
	     if (t) then {
	     	r = horner(P - betaInf * Q);
		t = provePolynomialPositive(r, dom);
		res = t;
	     } else {
	        res = false;
	     };
	  } else {
	     res = false;
	  };

	  return res;
};

procedure __checkRatioPolynomialsBetweenBoundsInner(p, q, dom, betaInf, betaSup) {
	  var res, t;

	  t = checkRatioPolynomialsBetweenBoundsLazy(p, q, dom, betaInf, betaSup);
	  if (t) then {
	     res = { .okay = true; .failures = [||] };
	  } else {
	     res = checkRatioPolynomialsBetweenBoundsHammer(p, q, dom, betaInf, betaSup);
	  };

	  return res;	  
};


procedure splitDomain(dom, splitPoints) {
	  var res, s, t, R, d;

	  if (splitPoints == [||]) then {
	     res = [| dom |];
	  } else {
             s = head(splitPoints);
	     t = tail(splitPoints);
	     R = splitDomain(dom, t);
	     res = [||];
	     for d in R do {
	     	 if ((inf(d) < sup(s) && (sup(s) < sup(d))) ||
		     (inf(d) < inf(s) && (inf(s) < sup(d)))) then {
		     if ((inf(d) < sup(s) && (sup(s) < sup(d))) &&
		         (inf(d) < inf(s) && (inf(s) < sup(d)))) then {
			 res = [inf(d);inf(s)] .: ( s .: ( [sup(s);sup(d)] .: res));
	             } else {
		         if (inf(d) < sup(s) && (sup(s) < sup(d))) then {
			    res = [ inf(d) ; sup(s) ] .: ( [sup(s); sup(d)] .: res);
			 } else {
                            res = [ inf(d) ; inf(s) ] .: ( [inf(s); sup(d)] .: res);
			 };
		     };
		 } else {
		   res = d .: res;
		 };
	     };
	  };

	  return res;
};

procedure checkRatioPolynomialsBetweenBoundsSafe(p, q, dom, betaInf, betaSup) {
	  var zerosQ, okay, failures, splitDomains;

	  zerosQ = functionZeros(q, dom, false);

	  splitDomains = splitDomain(dom, zerosQ);

	  okay = true;
	  failures = [||];
	  for d in splitDomains do {
	      R = __checkRatioPolynomialsBetweenBoundsInner(p, q, d, betaInf, betaSup);
	      okay = okay && (R.okay);
	      failures = failures @ (R.failures);
	  };
	  
	  return { .okay = okay, .failures = failures };
};

procedure checkRatioPolynomialsBetweenBounds(p, q, dom, betaInf, betaSup) {
	  var res;

	  if (betaInf > betaSup) then {
	     res = { .okay = false, .failures = [||] };
	  } else {
	     res = checkRatioPolynomialsBetweenBoundsSafe(p, q, dom, betaInf, betaSup);
	  };

	  return res;
};

procedure omegaDomainToXiDomain(Omega, t) {
	  var XiDom, redOmega, TDom, a, b, c, d, e, f, xit, tanpi, recprTByPi;

	  if (t == pi) then {
	     recprTByPi = 1;
	  } else {
	     if ((t == 2 * pi) || (t == pi * 2)) then {
	     	recprTByPi = 1/2;
	     } else {
	        recprTByPi = simplify(pi / t);
	     };
	  };

	  redOmega = [inf(Omega); sup(Omega)] / recprTByPi;
	  if (sup(redOmega) - inf(redOmega) >= 2) then {
	     XiDom = [0;1];
	  } else {
	     while (sup(redOmega) > 1) do {
	     	   redOmega = redOmega - 2;
	     };
	     while (inf(redOmega) < -1) do {
	     	   redOmega = redOmega + 2;
	     };

	     aa = inf(redOmega / 2);
	     bb = sup(redOmega / 2);

	     tanpi = tan(pi * _x_);
	     if (aa == -1/2) then {
	        if (bb >= 1/2) then {
		   TDom = [-infty; infty];
		} else {
                   TDom = [-infty; sup(tanpi([bb])) ];
		};
             } else {
	       if (bb == 1/2) then {
                  if (aa <= -1/2) then {
		     TDom = [-infty; infty];
		  } else {
                     TDom = [inf(tanpi([aa]));infty];
		  };
	       } else {
	       	 TDom = tanpi([aa;bb]);
	       };
	     };

	     a = inf(TDom);
	     b = sup(TDom);
	     xit = (_x_ + 2 - sqrt(_x_^2 + 4)) / (2 * _x_);

	     if (b == infty) then {
	      	c = [0];
	     } else {
	        c = xit([b]);
	     };
	     if (-a == infty) then {
	      	d = [1];
	     } else {
	        d = xit([a]);
	     };
	     e = inf(c);
	     if (inf(d) < e) then {
	     	e = inf(d);
	     };
	     if (e < 0) then {
	     	e = 0;
	     };
	     f = sup(c);
	     if (sup(d) > f) then {
	     	f = sup(d);
	     };
	     if (f > 1) then {
	     	f = 1;
	     };

	     XiDom = [ e, f ];
	  };
	  return XiDom;
};

procedure xiDomainToOmegaDomain(Xi) {
	  var TDom, a, b, c, d, e, f, txi, OmegaDomByPi, g, h;

	  a = inf(Xi);
	  b = sup(Xi);

	  txi = (1 - 2 * _x_) / (_x_ * (1 - _x_));

	  if (b == 1) then {
             c = -[infty];
	  } else {
	     if (b == 0) then {
                c = [infty];
	     } else {
	        c = txi([b]);
             };
	  };
	  if (a == 0) then {
             d = [infty];
	  } else {
	     if (a == 1) then {
	     	d = -[infty];
	     } else {
	        d = txi([a]);
             };
	  };

	  e = inf(c);
	  if (inf(d) < e) then {
	  	e = inf(d);
	  };
	  f = sup(c);
	  if (sup(d) > f) then {
	  	f = sup(d);
	  };

	  TDom = [ e, f ];

	  OmegaDomByPi = (2 * atan(TDom)) / pi;

	  g = inf(OmegaDomByPi);
	  h = sup(OmegaDomByPi);
	  if (g < -1) then {
	     g = -1;
	  };
	  if (h > 1) then {
	     h = 1;
	  };

	  return { .Omega = [ g; h ], .t = pi };
};

procedure translateBetaBoundsToSquare(betaInf, betaSup) {
	  var res;

	  if (betaInf * betaSup < 0) then {
	     res = { .betaInf = 0, .betaSup = round(min(betaInf^2, betaSup^2),prec,RD) };
	  } else {
	     if (betaSup <= 0) then {
	     	res = { .betaInf = round(betaSup^2,prec,RU), .betaSup = round(betaInf^2,prec,RD) };
	     } else {
	        res = { .betaInf = round(betaInf^2,prec,RU), .betaSup = round(betaSup^2,prec,RD) };
	     };
	  };

	  return res;
};

procedure checkModulusFilterInSpecificationWithSquareFilterInXiOneCase(p, q, s) {
	  var okay, issues, boundsSquared, betaInfSquare, betaSupSquare, Xi, R, f;
	  var failurePointOmegaWithFactor, y, failurePointOmega, ySq, w, subDomain;
	  var subDomainOmegaWithFactor;
	  
	  okay = false;
	  issues = [||];
	  
	  boundsSquared = translateBetaBoundsToSquare(s.betaInf, s.betaSup);
	  betaInfSquare = boundsSquared.betaInf;
	  betaSupSquare = boundsSquared.betaSup;

	  Xi = omegaDomainToXiDomain(s.Omega, s.omegaFactor);

	  R = checkRatioPolynomialsBetweenBounds(p, q, Xi, betaInfSquare, betaSupSquare);

	  okay = R.okay;
	  for w in R.failures do {
	      f = w.failurePoint;
	      subDomain = w.failureDomain;
	      ySq = evaluate(horner(p(inf(f) + (sup(f) - inf(f)) * (_x_ + 0.5)))/horner(q(inf(f) + (sup(f) - inf(f)) * (_x_ + 0.5))), [-0.5;0.5]);
	      if ((inf(ySq) < 0) && (sup(ySq) >= 0)) then {
	      	 ySq = [0; sup(ySq)];
	      };
	      y = sqrt(ySq);
	      failurePointOmegaWithFactor = xiDomainToOmegaDomain(f);
	      failurePointOmega = failurePointOmegaWithFactor.Omega * simplify(failurePointOmegaWithFactor.t / s.omegaFactor);
              subDomainOmegaWithFactor = xiDomainToOmegaDomain(subDomain);
	      subDomainOmega = subDomainOmegaWithFactor.Omega * simplify(subDomainOmegaWithFactor.t / s.omegaFactor);
	      issues = { .specification = s, .subdomainOmega = subDomainOmega, .subdomainOmegaFactor = s.omegaFactor, .omega = failurePointOmega, .omegaFactor = s.omegaFactor, .H = y } .: issues;
	  };

	  return { .okay = okay; .issue = issues; .specification = s };
};

procedure checkModulusFilterInSpecificationWithSquareFilterInXi(p, q, specifications) {
	  var okay, resDetails, s, r;

	  okay = true;
	  resDetails = [||];
	  for s in specifications do {
	      r = checkModulusFilterInSpecificationWithSquareFilterInXiOneCase(p, q, s);
	      resDetails = r .: resDetails;
	      okay = okay && r.okay;
	  };

	  return { .okay = okay, .results = resDetails };
};

procedure __checkModulusFilterInSpecificationInner(b, a, specifications) {
	  var T, p, q, R;

	  T = modulusSquareFilterInXi(b, a);
	  p = T.p; q = T.q;

	  R = checkModulusFilterInSpecificationWithSquareFilterInXi(p, q, specifications);

	  R.p = p;
	  R.q = q;

	  return R;
};

procedure checkModulusFilterInSpecification(b, a, specifications, p) {
	  var t, r;
	  var oldPrec, oldPoints;
	  
	  oldPrec = prec;
	  prec = p!;
	  oldPoints = points;
	  points = ceil(ceil(4 * max(degree(b),degree(a),40)) / 2) * 2 + 1!;
	  t = time({
	               r = __checkModulusFilterInSpecificationInner(b, a, specifications);
	           });

          r.computeTime = t;
	  r.a = a;
	  r.b = b;
	  r.specifications = specifications;
	  prec = oldPrec!;
	  points = oldPoints!;

	  return r;
};

procedure presentResults(res) {
	  var i, k;

	  write("Overall check okay: ", res.okay, "\n");
	  if (!res.okay) then {
	     write("The following issues have been found:\n");
	     for i in res.results do {
	     	 for k in i.issue do {
		     write("Issue in subdomain Omega = ", k.subdomainOmegaFactor, " * ", k.subdomainOmega, " at omega = ", k.omegaFactor, " * ", k.omega, ": |H(exp(j*omega))| should be between ", round(k.specification.betaInf, 4 * prec, RU), " and ", round(k.specification.betaSup, 4 * prec, RD), " but evaluates to ", k.H, " = 10^(", 20 * log10(k.H)," / 20)\n");
		 };
	     };
	  };
	  write("Computing this result took ", ceil(res.computeTime * 1000), "ms\n");
};

