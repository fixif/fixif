/* -*-mode:c++-*- *********************************************************
 *                                                                        *
 *  Algorithmic C (tm) Datatypes                                          *
 *                                                                        *
 *  Software Version: 2.6                                                 *
 *                                                                        *
 *  Release Date    : Tue Jun 28 10:00:45 PDT 2011                        *
 *  Release Type    : Production                                          *
 *  Release Build   : 2.6.0                                               *
 *                                                                        *
 *  Copyright 2008, Mentor Graphics Corporation,                     *
 *                                                                        *
 *  All Rights Reserved.                                                  *
 *                                                                        *
 **************************************************************************
 *                                                                        *
 *  The most recent version of this package can be downloaded from:       *
 *     http://www.mentor.com/products/c-based_design/ac_datatypes         *
 *                                                                        *
 **************************************************************************
 *                                                                        *
 *  IMPORTANT - THIS SOFTWARE IS COPYRIGHTED AND SUBJECT TO LICENSE       *
 *  RESTRICTIONS                                                          *
 *                                                                        *
 *  THE LICENSE THAT CONTROLS YOUR USE OF THE SOFTWARE IS:                *
 *     ALGORITHMIC C DATATYPES END-USER LICENSE AGREEMENT                 *
 *                                                                        *
 *  THESE COMMENTS ARE NOT THE LICENSE.  PLEASE CONSULT THE FULL LICENSE  *
 *  FOR THE ACTUAL TERMS AND CONDITIONS WHICH IS LOCATED AT THE BOTTOM    *
 *  OF THIS FILE.                                                         *
 *                                                                        *  
 *  CAREFULLY READ THE LICENSE AGREEMENT BEFORE USING THE SOFTWARE.       *
 *                                                                        *  
 *       *** MODIFICATION OF THE SOFTWARE IS NOT AUTHORIZED ***           *
 *                                                                        *
 **************************************************************************
 *                                                                        *
 *  YOUR USE OF THE SOFTWARE INDICATES YOUR COMPLETE AND UNCONDITIONAL    *
 *  ACCEPTANCE OF THE TERMS AND CONDITIONS SET FORTH IN THE LICENSE. IF   *
 *  YOU DO NOT  AGREE TO THE LICENSE TERMS AND CONDITIONS, DO NOT USE THE *
 *  SOFTWARE, REMOVE IT FROM YOUR SYSTEM, AND DESTROY ALL COPIES.         *
 *                                                                        *
 *************************************************************************/
                                                                                                                     
/*
//  Source:         ac_complex.h
//  Description:    complex type with parameterized type that can be:
//                    - C integer types
//                    - C floating point types
//                    - ac_int
//                    - ac_fixed
//                  ac_complex based on C integers, based on ac_int, and based on ac_fixed can
//                  be mixed  
//  Author:         Andres Takach, Ph.D.
*/

#ifndef __AC_COMPLEX_H
#define __AC_COMPLEX_H

#include <ac_fixed.h>

#if ( AC_VERSION == 1 && AC_VERSION_MINOR < 4 )
#error ac_complex requires ac_int/ac_fixed header files versions 1.4 or above 
#endif

#ifdef __AC_NAMESPACE
namespace __AC_NAMESPACE {
#endif

template<typename T> class ac_complex;
 
namespace ac {
  // specializations after definition of ac_complex
  template<typename T>
  struct rt_ac_complex_T {
    template<typename T2>
    struct op1 {
      typedef typename T::template rt_T< ac_complex<T2> >::mult mult;
      typedef typename T::template rt_T< ac_complex<T2> >::plus plus;
      typedef typename T::template rt_T< ac_complex<T2> >::minus2 minus;
      typedef typename T::template rt_T< ac_complex<T2> >::minus minus2;
      typedef typename T::template rt_T< ac_complex<T2> >::logic logic;
      typedef typename T::template rt_T< ac_complex<T2> >::div2 div;
      typedef typename T::template rt_T< ac_complex<T2> >::div div2;
    };
  };

  template<typename T, typename T2>
  struct rt2 {
    typedef typename map<T>::t map_T;
    typedef typename map<T2>::t map_T2;
    typedef typename map_T::template rt_T< map_T2 >::mult mult;
    typedef typename map_T::template rt_T< map_T2 >::plus plus;
    typedef typename map_T::template rt_T< map_T2 >::minus minus;
    typedef typename map_T::template rt_T< map_T2 >::minus2 minus2;
    typedef typename map_T::template rt_T< map_T2 >::logic logic;
    typedef typename map_T::template rt_T< map_T2 >::div div;
    typedef typename map_T::template rt_T< map_T2 >::div2 div2;
  };
}  // namespace ac

template<typename T>
class ac_complex {
public:   // temporary workaround
  T _r;
  T _i;
  typedef typename ac::map<T>::t map_T;
  typedef typename map_T::rt_unary::mag_sqr T_sqr;
  typedef typename ac::map<T_sqr>::t map_T_sqr; 
  typedef typename ac::map<typename map_T::rt_unary::mag>::t map_T_mag; 
public:
  typedef T element_type;
  template<typename T2>
  struct rt_T {
    typedef typename ac::map<T2>::t map_T2;
    typedef typename ac::rt_ac_complex_T<map_T2>::template op1<map_T>::mult mult;
    typedef typename ac::rt_ac_complex_T<map_T2>::template op1<map_T>::plus plus;
    typedef typename ac::rt_ac_complex_T<map_T2>::template op1<map_T>::minus minus;
    typedef typename ac::rt_ac_complex_T<map_T2>::template op1<map_T>::minus2 minus2;
    typedef typename ac::rt_ac_complex_T<map_T2>::template op1<map_T>::logic logic;
    typedef typename ac::rt_ac_complex_T<map_T2>::template op1<map_T>::div div;
    typedef typename ac::rt_ac_complex_T<map_T2>::template op1<map_T>::div2 div2;
    typedef ac_complex<T> arg1;
  };

  struct rt_unary {
    typedef typename map_T_sqr::template rt_T<map_T_sqr>::plus  mag_sqr;
    typedef typename map_T_mag::template rt_T<map_T_mag>::plus  mag;   // overly conservative for signed 
    typedef ac_complex<typename map_T::rt_unary::neg>  neg;
    template<unsigned N>
    struct set {
      typedef ac_complex<typename map_T::rt_unary::template set<N>::sum> sum;
    };
  };

  ac_complex() { }
  template<typename T2>
  ac_complex(const ac_complex<T2> &c) {
    _r = c.r();
    _i = c.i();
  }
  template<typename T2>
  ac_complex(const T2 &r) {
    _r = r;
    _i = 0;
  }
  template<typename T2, typename T3>
  ac_complex(const T2 &r, const T3 &i) {
    _r = r;
    _i = i;
  }
  const T &r() const { return _r; }
  const T &i() const { return _i; }
  T &r() { return _r; }
  T &i() { return _i; }
  const T &real() const { return _r; }
  const T &imag() const { return _i; }
  T &real() { return _r; }
  T &imag() { return _i; }
  template<typename T2>
  void set_r(const T2 &r) { _r = r;}
  template<typename T2>
  void set_i(const T2 &i) { _i = i;}

  // The following had to be moved to be non-member functions because of what I believe is a bug
  //   in some compilers that error out due to ambiguity
#if 0
  template<typename T2>
  typename rt_T< ac_complex<T2> >::plus operator +(const ac_complex<T2> &op2) const {
    typename rt_T< ac_complex<T2> >::plus res( _r + op2.r(), _i + op2.i() );
    return res;
  }

  template<typename T2>
  typename rt_T<T2>::plus operator +(const T2 &op2) const {
    typename rt_T<T2>::plus res( _r + op2, _i ); 
    return res;
  }

  template<typename T2>
  typename rt_T< ac_complex<T2> >::minus operator -(const ac_complex<T2> &op2) const {
    typename rt_T< ac_complex<T2> >::minus res( _r - op2.r(), _i - op2.i() ); 
    return res;
  }

  template<typename T2>
  typename rt_T<T2>::minus operator -(const T2 &op2) const {
    typename rt_T<T2>::minus res( _r - op2, _i ); 
    return res;
  }

  template<typename T2>
  typename rt_T< ac_complex<T2> >::mult operator *(const ac_complex<T2> &op2) const {
    typename rt_T< ac_complex<T2> >::mult res( _r*op2.r() - _i*op2.i(), _i*op2.r() + _r*op2.i() ); 
    return res;
  }

  template<typename T2>
  typename rt_T<T2>::mult operator *(const T2 &op2) const {
    typename rt_T<T2>::mult res( _r*op2, _i*op2 ); 
    return res;
  }

  template<typename T2>
  typename rt_T< ac_complex<T2> >::div operator /(const ac_complex<T2> &op2) const {
    typename ac_complex<T2>::rt_unary::mag_sqr d = op2.mag_sqr();
    typename rt_T< ac_complex<T2> >::div res((_r*op2.r() + _i*op2.i())/d, (_i*op2.r() - _r*op2.i())/d);
    return res; 
  }

  template<typename T2>
  typename rt_T<T2>::div operator /(const T2 &op2) const {
    ac_complex< typename T::template rt_T<T2>::div > res( _r/op2, _i/op2 );
    return res; 
  }
#endif

  template<typename T2>
  ac_complex &operator +=(const ac_complex<T2> &op2) {
    _r += op2.r();
    _i += op2.i();
    return *this;
  }

  template<typename T2>
  ac_complex &operator +=(const T2 &op2) {
    _r += op2;
    return *this;
  }

  template<typename T2>
  ac_complex &operator -=(const ac_complex<T2> &op2) {
    _r -= op2.r();
    _i -= op2.i();
    return *this;
  }
 
  template<typename T2>
  ac_complex &operator -=(const T2 &op2) {
    _r -= op2;
    return *this;
  }

  template<typename T2>
  ac_complex &operator *=(const ac_complex<T2> &op2) {
    T r0 = _r*op2.r() - _i*op2.i(); 
    _i = _r*op2.i() + _i*op2.r(); 
    _r = r0;
    return *this;
  }

  template<typename T2>
  ac_complex &operator *=(const T2 &op2) {
    _r = _r*op2; 
    _i = _i*op2;
    return *this;
  }

  template<typename T2>
  ac_complex &operator /=(const ac_complex<T2> &op2) {
    typename ac_complex<T2>::rt_unary::mag_sqr d = op2.mag_sqr();
    T r0 = (_r*op2.r() + _i*op2.i())/d;
    _i = (_i*op2.r() - _r*op2.i())/d;
    _r = r0;
    return *this;
  }

  template<typename T2>
  ac_complex &operator /=(const T2 &op2) {
    _r = _r/op2; 
    _i = _i/op2;
    return *this;
  }

  // Arithmetic Unary --------------------------------------------------------
  ac_complex operator +() {
    return *this;
  }
  typename rt_unary::neg operator -() const {
    typename rt_unary::neg res(-_r, -_i);
    return res;
  }

  // ! ------------------------------------------------------------------------
  bool operator ! () const {
    return !_r && !_i; 
  }

  typename rt_unary::neg conj() const {
    typename rt_unary::neg res(_r, -_i);
    return res;
  }

  typename rt_unary::mag_sqr mag_sqr() const {
    return _r*_r + _i*_i;
  }

  ac_complex< ac_int<2,true> > sign_conj() const {
    return ac_complex< ac_int<2,true> >(
      _r ? (_r < 0 ? -1 : 1) : 0,
      _i ? (_i < 0 ? 1 : -1) : 0
    );
  }

  inline static std::string type_name() {
    typedef typename ac::map<T>::t map_T;
    std::string r = "ac_complex<";
    r += map_T::type_name();
    r += '>';
    return r; 
  }
#if defined(SYSTEMC_H)
inline friend void sc_trace(sc_core::sc_trace_file *tf, const ac_complex<T> &a, const std::string &name)
{
  sc_trace(tf, a.real(), name + ".r");
  sc_trace(tf, a.imag(), name + ".i");
}
#endif

};

namespace ac {
  // with T2 == ac_complex
  template<typename T2>
  struct rt_ac_complex_T< ac_complex<T2> > {
    template<typename T>
    struct op1 {
      typedef ac_complex<typename ac::rt2<T,T2>::plus> plus;
      typedef ac_complex<typename ac::rt2<T,T2>::minus> minus;
      typedef ac_complex<typename ac::rt2<T,T2>::minus2> minus2;
      typedef ac_complex<typename ac::rt2<T,T2>::logic> logic;
      typedef ac_complex<typename ac::rt2<T,T2>::div> div;
      typedef ac_complex<typename ac::rt2<T,T2>::div2> div2;
      typedef ac_complex<typename ac::rt2<
          typename ac::rt2<typename ac::rt2<T,T2>::mult, typename ac::rt2<T,T2>::mult>::plus,
          typename ac::rt2<typename ac::rt2<T,T2>::mult, typename ac::rt2<T,T2>::mult>::minus
        >::logic> mult;
    };
  };
  // with T2 == ac_fixed
  template<int W2, int I2, bool S2>
  struct rt_ac_complex_T< ac_fixed<W2,I2,S2> > {
    typedef ac_fixed<W2,I2,S2> T2;
    template<typename T>
    struct op1 {
      typedef ac_complex<typename T::template rt_T<T2>::plus> plus;
      typedef ac_complex<typename T::template rt_T<T2>::minus> minus;
      typedef ac_complex<typename T::template rt_T<T2>::minus2> minus2;
      typedef ac_complex<typename T::template rt_T<T2>::logic> logic;
      typedef ac_complex<typename T::template rt_T<T2>::div> div;
      typedef ac_complex<typename T::template rt_T<T2>::div2> div2;   // ???
      typedef ac_complex<typename T::template rt_T<T2>::mult> mult; 
    };
  };
  // with T2 == ac_int
  template<int W2, bool S2>
  struct rt_ac_complex_T< ac_int<W2,S2> > {
    typedef ac_int<W2,S2> T2;
    template<typename T>
    struct op1 {
      typedef ac_complex<typename T::template rt_T<T2>::plus> plus;
      typedef ac_complex<typename T::template rt_T<T2>::minus> minus;
      typedef ac_complex<typename T::template rt_T<T2>::minus2> minus2;
      typedef ac_complex<typename T::template rt_T<T2>::logic> logic;
      typedef ac_complex<typename T::template rt_T<T2>::div> div;
      typedef ac_complex<typename T::template rt_T<T2>::div2> div2;   // ???
      typedef ac_complex<typename T::template rt_T<T2>::mult> mult; 
    };
  };
  // with T2 == c_type<TC>
  template<typename TC>
  struct rt_ac_complex_T< c_type<TC> > {
    typedef c_type<TC> T2;
    template<typename T>
    struct op1 {
      typedef ac_complex<typename T::template rt_T<T2>::plus> plus;
      typedef ac_complex<typename T::template rt_T<T2>::minus> minus;
      typedef ac_complex<typename T::template rt_T<T2>::minus2> minus2;
      typedef ac_complex<typename T::template rt_T<T2>::logic> logic;
      typedef ac_complex<typename T::template rt_T<T2>::div> div;
      typedef ac_complex<typename T::template rt_T<T2>::div2> div2;   // ???
      typedef ac_complex<typename T::template rt_T<T2>::mult> mult; 
    };
  };
}

template<typename T, typename T2>
inline typename ac_complex<T>::template rt_T<ac_complex<T2> >::plus operator +(const ac_complex<T> &op, const ac_complex<T2> &op2) {
  typename ac_complex<T>::template rt_T<ac_complex<T2> >::plus res( op.r() + op2.r(), op.i() + op2.i() );
  return res;
}

template<typename T, typename T2>
inline typename ac_complex<T2>::template rt_T<T>::plus operator +(const T &op, const ac_complex<T2> &op2) {
  typename ac_complex<T2>::template rt_T<T>::plus res( op + op2.r(), op2.i() );
  return res;
}

template<typename T, typename T2>
inline typename ac_complex<T>::template rt_T<T2>::plus operator +(const ac_complex<T> &op, const T2 &op2) {
  typename ac_complex<T>::template rt_T<T2>::plus res( op.r() + op2, op.i() );
  return res;
}

template<typename T, typename T2>
inline typename ac_complex<T>::template rt_T<ac_complex<T2> >::minus operator -(const ac_complex<T> &op, const ac_complex<T2> &op2) {
  typename ac_complex<T>::template rt_T<ac_complex<T2> >::minus res( op.r() - op2.r(), op.i() - op2.i() );
  return res;
}
                                                                                                                        
template<typename T, typename T2>
inline typename ac_complex<T2>::template rt_T<T>::minus2 operator -(const T &op, const ac_complex<T2> &op2) {
  typename ac_complex<T2>::template rt_T<T>::minus2 res( op - op2.r(), op2.i() );
  return res;
}
                                                                                                                        
template<typename T, typename T2>
inline typename ac_complex<T>::template rt_T<T2>::minus operator -(const ac_complex<T> &op, const T2 &op2) {
  typename ac_complex<T>::template rt_T<T2>::minus res( op.r() - op2, op.i() );
  return res;
}

template<typename T, typename T2>
inline typename ac_complex<T>::template rt_T<ac_complex<T2> >::mult operator *(const ac_complex<T> &op, const ac_complex<T2> &op2) {
  typename ac_complex<T>::template rt_T<ac_complex<T2> >::mult res( op.r()*op2.r() - op.i()*op2.i(), op.i()*op2.r() + op.r()*op2.i() ); 
  return res;
}
                                                                                                                        
template<typename T, typename T2>
inline typename ac_complex<T2>::template rt_T<T>::mult operator *(const T &op, const ac_complex<T2> &op2) {
  typename ac_complex<T2>::template rt_T<T>::mult res( op*op2.r(), op*op2.i());
  return res;
}
                                                                                                                        
template<typename T, typename T2>
inline typename ac_complex<T>::template rt_T<T2>::mult operator *(const ac_complex<T> &op, const T2 &op2) {
  typename ac_complex<T>::template rt_T<T2>::mult res( op.r()*op2, op.i()*op2 );
  return res;
}

template<typename T, typename T2>
inline typename ac_complex<T>::template rt_T<ac_complex<T2> >::div operator /(const ac_complex<T> &op, const ac_complex<T2> &op2) {
  typename ac_complex<T2>::rt_unary::mag_sqr d = op2.mag_sqr();
  typename ac_complex<T>::template rt_T<ac_complex<T2> >::div res((op.r()*op2.r() + op.i()*op2.i())/d, (op.i()*op2.r() - op.r()*op2.i())/d);
  return res;
}

template<typename T, typename T2>
inline typename ac_complex<T>::template rt_T<T2>::div operator /(const ac_complex<T> &op, const T2 &op2) {
  typename ac_complex<T>::template rt_T<T2>::div res( op.r()/op2, op.i()/op2 );
  return res;
}
                                                                                                                        
template<typename T, typename T2>
inline typename ac_complex<T2>::template rt_T<T>::div2 operator /(const T &op, const ac_complex<T2> &op2) {
  typename ac_complex<T2>::rt_unary::mag_sqr d = op2.mag_sqr();
  typename ac_complex<T2>::template rt_T<T>::div2 res(op*op2.r()/d, - op*op2.i()/d);
  return res;
}

template<typename T, typename T2>
inline bool operator == (const ac_complex<T> &op, const ac_complex<T2> &op2) {
  return op.r() == op2.r() && op.i() == op2.i();
}

template<typename T, typename T2>
inline bool operator == (const T &op, const ac_complex<T2> &op2) {
  return op == op2.r() && op2.i() == 0;
}

template<typename T, typename T2>
inline bool operator == (const ac_complex<T> &op, const T2 &op2) {
  return op.r() == op2 && op.i() == 0;
}

template<typename T, typename T2>
inline bool operator != (const ac_complex<T> &op, const ac_complex<T2> &op2) {
  return op.r() != op2.r() || op.i() != op2.i();
}

template<typename T, typename T2>
inline bool operator != (const T &op, const ac_complex<T2> &op2) {
  return op != op2.r() || op2.i() != 0;
}

template<typename T, typename T2>
inline bool operator != (const ac_complex<T> &op, const T2 &op2) {
  return op.r() != op2 || op.i() != 0;
}

// Stream --------------------------------------------------------------------
                                                                                                                     
template<typename T>
inline std::ostream& operator << (std::ostream &os, const ac_complex<T> &x) {
#ifndef __SYNTHESIS__
  os << "(" << x.r() << ", " << x.i() << ")";
#endif
  return os;
}

template<ac_special_val V, typename T>
inline ac_complex<T> value(ac_complex<T>) {
  T val = value<V>((T) 0);
  ac_complex<T> r(val, val);
  return r;
}

namespace ac {
  template<ac_special_val V, typename T>
  inline bool init_array(ac_complex<T> *a, int n) {
    ac_complex<T> t = value<V>(*a);
    for(int i=0; i < n; i++)
      a[i] = t;
    return true;
  }
}

#ifdef __AC_NAMESPACE
}
#endif

#endif // __AC_COMPLEX_H

/**************************************************************************
 *                                                                        *
 *  ALGORITHMIC C DATATYPES END-USER LICENSE AGREEMENT                    *
 *                                                                        *
 *                                                                        *
 *  IMPORTANT - USE OF SOFTWARE IS SUBJECT TO LICENSE RESTRICTIONS        *
 *  CAREFULLY READ THIS LICENSE AGREEMENT BEFORE USING THE SOFTWARE       *
 *                                                                        *
 *  YOU MAY USE AND DISTRIBUTE UNMODIFIED VERSIONS OF THIS SOFTWARE AS    *
 *  STATED BELOW, YOU MAY NOT MODIFY THE SOFTWARE This license is a       *
 *  legal Agreement between you, the end user, either individually or     *
 *  as an authorized representative of a company acquiring the license,   *
 *  and Mentor Graphics Corporation ("Mentor Graphics"). YOUR USE OF      *
 *  THE SOFTWARE INDICATES YOUR COMPLETE AND UNCONDITIONAL ACCEPTANCE     *
 *  OF THE TERMS AND CONDITIONS SET FORTH IN THIS AGREEMENT. If you do    *
 *  not agree to these terms and conditions, promptly return or, if       *
 *  received electronically, delete the Software and all accompanying     *
 *  items.                                                                *
 *                                                                        *
 *                                                                        *
 *  1. GRANT OF LICENSE. YOU MAY USE AND DISTRIBUTE THE SOFTWARE, BUT     *
 *  YOU MAY NOT MODIFY THE SOFTWARE. The Software you are installing,     *
 *  downloading, or otherwise acquired, under this Agreement, including   *
 *  source code, binary code, updates, modifications, revisions,          *
 *  copies, or documentation pertaining to Algorithmic C Datatypes        *
 *  (collectively the "Software") is a copyrighted work owned by Mentor   *
 *  Graphics. Mentor Graphics grants to you, a nontransferable,           *
 *  nonexclusive, limited copyright license to use and distribute the     *
 *  Software, but you may not modify the Software. Use of the Software    *
 *  consists solely of reproduction, performance, and display.            *
 *                                                                        *
 *  2. RESTRICTIONS; NO MODIFICATION. Modifying the Software is           *
 *  prohibited. Each copy of the Software you create must include all     *
 *  notices and legends embedded in the Software.  Modifying the          *
 *  Software means altering, enhancing, editing, deleting portions or     *
 *  creating derivative works of the Software.  You may append other      *
 *  code to the Software, so long as the Software is not otherwise        *
 *  modified. Mentor Graphics retains all rights not expressly granted    *
 *  by this Agreement. The terms of this Agreement, including without     *
 *  limitation, the licensing and assignment provisions, shall be         *
 *  binding upon your successors in interest and assigns.  The            *
 *  provisions of this section 2 shall survive termination or             *
 *  expiration of this Agreement.                                         *
 *                                                                        *
 *  3. USER COMMENT AND SUGGESTIONS.  You are not obligated to provide    *
 *  Mentor Graphics with comments or suggestions regarding the            *
 *  Software.  However, if you do provide to Mentor Graphics comments     *
 *  or suggestions for the modification, correction, improvement or       *
 *  enhancement of (a) the Software or (b) Mentor Graphics products or    *
 *  processes which may embody the Software ("Comments"), you grant to    *
 *  Mentor a non-exclusive, irrevocable, worldwide, royalty-free          *
 *  license to disclose, display, perform, copy, make, have made, use,    *
 *  sublicense, sell, and otherwise dispose of the Comments, and Mentor   *
 *  Graphics' products embodying such Comments, in any manner which       *
 *  Mentor Graphics chooses, without reference to the source.             *
 *                                                                        *
 *  4. NO WARRANTY. MENTOR GRAPHICS EXPRESSLY DISCLAIMS ALL WARRANTY      *
 *  FOR THE SOFTWARE. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE       *
 *  LAW, THE SOFTWARE AND ANY RELATED DOCUMENTATION IS PROVIDED "AS IS"   *
 *  AND WITH ALL FAULTS AND WITHOUT WARRANTIES OR CONDITIONS OF ANY       *
 *  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING, WITHOUT LIMITATION, THE   *
 *  IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR       *
 *  PURPOSE, OR NONINFRINGEMENT. THE ENTIRE RISK ARISING OUT OF USE OR    *
 *  DISTRIBUTION OF THE SOFTWARE REMAINS WITH YOU.                        *
 *                                                                        *
 *  5. LIMITATION OF LIABILITY. IN NO EVENT WILL MENTOR GRAPHICS OR ITS   *
 *  LICENSORS BE LIABLE FOR INDIRECT, SPECIAL, INCIDENTAL, OR             *
 *  CONSEQUENTIAL DAMAGES (INCLUDING LOST PROFITS OR SAVINGS) WHETHER     *
 *  BASED ON CONTRACT, TORT OR ANY OTHER LEGAL THEORY, EVEN IF MENTOR     *
 *  GRAPHICS OR ITS LICENSORS HAVE BEEN ADVISED OF THE POSSIBILITY OF     *
 *  SUCH DAMAGES.                                                         *
 *                                                                        *
 *  6.  LIFE ENDANGERING APPLICATIONS. NEITHER MENTOR GRAPHICS NOR ITS    *
 *  LICENSORS SHALL BE LIABLE FOR ANY DAMAGES RESULTING FROM OR IN        *
 *  CONNECTION WITH THE USE OR DISTRIBUTION OF SOFTWARE IN ANY            *
 *  APPLICATION WHERE THE FAILURE OR INACCURACY OF THE SOFTWARE MIGHT     *
 *  RESULT IN DEATH OR PERSONAL INJURY.  THE PROVISIONS OF THIS SECTION 6 *
 *  SHALL SURVIVE TERMINATION OR EXPIRATION OF THIS AGREEMENT.            *
 *                                                                        *
 *  7.  INDEMNIFICATION.  YOU AGREE TO INDEMNIFY AND HOLD HARMLESS        *
 *  MENTOR GRAPHICS AND ITS LICENSORS FROM ANY CLAIMS, LOSS, COST,        *
 *  DAMAGE, EXPENSE, OR LIABILITY, INCLUDING ATTORNEYS' FEES, ARISING     *
 *  OUT OF OR IN CONNECTION WITH YOUR USE OR DISTRIBUTION OF SOFTWARE.    *
 *                                                                        *
 *  8. TERM AND TERMINATION. This Agreement terminates immediately if     *
 *  you exceed the scope of the license granted or fail to comply with    *
 *  the provisions of this License Agreement.  If you institute patent    *
 *  litigation against Mentor Graphics (including a cross-claim or        *
 *  counterclaim in a lawsuit) alleging that the Software constitutes     *
 *  direct or contributory patent infringement, then any patent           *
 *  licenses granted to you under this License for that Software shall    *
 *  terminate as of the date such litigation is filed. Upon termination   *
 *  or expiration, you agree to cease all use of the Software and         *
 *  delete all copies of the Software.                                    *
 *                                                                        *
 *  9. EXPORT. Software may be subject to regulation by local laws and    *
 *  United States government agencies, which prohibit export or           *
 *  diversion of certain products, information about the products, and    *
 *  direct products of the products to certain countries and certain      *
 *  persons. You agree that you will not export any Software or direct    *
 *  product of Software in any manner without first obtaining all         *
 *  necessary approval from appropriate local and United States           *
 *  government agencies.                                                  *
 *                                                                        *
 *  10. U.S. GOVERNMENT LICENSE RIGHTS. Software was developed entirely   *
 *  at private expense. All software is commercial computer software      *
 *  within the meaning of the applicable acquisition regulations.         *
 *  Accordingly, pursuant to US FAR 48 CFR 12.212 and DFAR 48 CFR         *
 *  227.7202, use, duplication and disclosure of the Software by or for   *
 *  the U.S. Government or a U.S. Government subcontractor is subject     *
 *  solely to the terms and conditions set forth in this Agreement,       *
 *  except for provisions which are contrary to applicable mandatory      *
 *  federal laws.                                                         *
 *                                                                        *
 *  11. CONTROLLING LAW AND JURISDICTION. THIS AGREEMENT SHALL BE         *
 *  GOVERNED BY AND CONSTRUED UNDER THE LAWS OF THE STATE OF OREGON,      *
 *  USA. All disputes arising out of or in relation to this Agreement     *
 *  shall be submitted to the exclusive jurisdiction of Multnomah         *
 *  County, Oregon. This section shall not restrict Mentor Graphics'      *
 *  right to bring an action against you in the jurisdiction where your   *
 *  place of business is located.  The United Nations Convention on       *
 *  Contracts for the International Sale of Goods does not apply to       *
 *  this Agreement.                                                       *
 *                                                                        *
 *  12. SEVERABILITY. If any provision of this Agreement is held by a     *
 *  court of competent jurisdiction to be void, invalid, unenforceable    *
 *  or illegal, such provision shall be severed from this Agreement and   *
 *  the remaining provisions will remain in full force and effect.        *
 *                                                                        *
 *  13. MISCELLANEOUS.  This Agreement contains the parties' entire       *
 *  understanding relating to its subject matter and supersedes all       *
 *  prior or contemporaneous agreements. This Agreement may only be       *
 *  modified in writing by authorized representatives of the parties.     *
 *  Waiver of terms or excuse of breach must be in writing and shall      *
 *  not constitute subsequent consent, waiver or excuse. The prevailing   *
 *  party in any legal action regarding the subject matter of this        *
 *  Agreement shall be entitled to recover, in addition to other          *
 *  relief, reasonable attorneys' fees and expenses.                      *
 *                                                                        *
 *  Algorithmic C Datatypes EULA (Rev. 090507)                             *
 **************************************************************************/
