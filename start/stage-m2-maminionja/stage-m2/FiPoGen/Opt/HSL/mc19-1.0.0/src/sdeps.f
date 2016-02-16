* COPYRIGHT (c) 1967 AEA Technology
*######DATE 26 Oct 1992
C       New version with S in names.
C  EAT 21/6/93 EXTERNAL statement put in for block data on VAXs.
C  15/10/02 SNGL removed
C
      REAL FUNCTION FA01A(I)
C     .. Scalar Arguments ..
      INTEGER I
C     ..
C     .. Local Scalars ..
      DOUBLE PRECISION R,S
C     ..
C     .. Intrinsic Functions ..
      INTRINSIC DINT,MOD
C     ..
C     .. Common blocks ..
      COMMON /FA01E/GL,GR
      DOUBLE PRECISION GL,GR
C     ..
C     .. Save statement ..
      SAVE /FA01E/
C     ..
C     .. Data block external statement
      EXTERNAL FA01F
C     ..
C     .. Executable Statements ..
      R = GR*9228907D0/65536D0
      S = DINT(R)
      GL = MOD(S+GL*9228907D0,65536D0)
      GR = R - S
      IF (I.GE.0) FA01A = (GL+GR)/65536D0
      IF (I.LT.0) FA01A = (GL+GR)/32768D0-1.D0
      GR = GR*65536D0
      RETURN

      END
      SUBROUTINE FA01B(MAX,NRAND)
C     .. Scalar Arguments ..
      INTEGER MAX,NRAND
C     ..
C     .. External Functions ..
      REAL FA01A
      EXTERNAL FA01A
C     ..
C     .. Intrinsic Functions ..
      INTRINSIC FLOAT,INT
C     ..
C     .. Executable Statements ..
      NRAND = INT(FA01A(1)*FLOAT(MAX)) + 1
      RETURN

      END
      SUBROUTINE FA01C(IL,IR)
C     .. Scalar Arguments ..
      INTEGER IL,IR
C     ..
C     .. Common blocks ..
      COMMON /FA01E/GL,GR
      DOUBLE PRECISION GL,GR
C     ..
C     .. Save statement ..
      SAVE /FA01E/
C     ..
C     .. Executable Statements ..
      IL = GL
      IR = GR
      RETURN

      END
      SUBROUTINE FA01D(IL,IR)
C     .. Scalar Arguments ..
      INTEGER IL,IR
C     ..
C     .. Common blocks ..
      COMMON /FA01E/GL,GR
      DOUBLE PRECISION GL,GR
C     ..
C     .. Save statement ..
      SAVE /FA01E/
C     ..
C     .. Executable Statements ..
      GL = IL
      GR = IR
      RETURN

      END
      BLOCK DATA FA01F
C     .. Common blocks ..
      COMMON /FA01E/GL,GR
      DOUBLE PRECISION GL,GR
C     ..
C     .. Save statement ..
      SAVE /FA01E/
C     ..
C     .. Data statements ..
      DATA GL/21845D0/
      DATA GR/21845D0/
C     ..
C     .. Executable Statements ..
      END
