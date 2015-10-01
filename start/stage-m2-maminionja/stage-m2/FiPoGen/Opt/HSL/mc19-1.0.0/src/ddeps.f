* COPYRIGHT (c) 1967 AEA Technology
*######DATE 4 Oct 1992
C       Toolpack tool decs employed.
C       SAVE statement for COMMON FA01ED added.
C  EAT 21/6/93 EXTERNAL statement put in for block data on VAXs.
C
C
      DOUBLE PRECISION FUNCTION FA01AD(I)
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
      COMMON /FA01ED/GL,GR
      DOUBLE PRECISION GL,GR
C     ..
C     .. Data block external statement
      EXTERNAL FA01FD
C     ..
C     .. Save statement ..
      SAVE /FA01ED/
C     ..
C     .. Executable Statements ..
      R = GR*9228907D0/65536D0
      S = DINT(R)
      GL = MOD(S+GL*9228907D0,65536D0)
      GR = R - S
      IF (I.GE.0) FA01AD = (GL+GR)/65536D0
      IF (I.LT.0) FA01AD = (GL+GR)/32768D0 - 1.D0
      GR = GR*65536D0
      RETURN

      END
      SUBROUTINE FA01BD(MAX,NRAND)
C     .. Scalar Arguments ..
      INTEGER MAX,NRAND
C     ..
C     .. External Functions ..
      DOUBLE PRECISION FA01AD
      EXTERNAL FA01AD
C     ..
C     .. Intrinsic Functions ..
      INTRINSIC DBLE,INT
C     ..
C     .. Executable Statements ..
      NRAND = INT(FA01AD(1)*DBLE(MAX)) + 1
      RETURN

      END
      SUBROUTINE FA01CD(IL,IR)
C     .. Scalar Arguments ..
      INTEGER IL,IR
C     ..
C     .. Common blocks ..
      COMMON /FA01ED/GL,GR
      DOUBLE PRECISION GL,GR
C     ..
C     .. Save statement ..
      SAVE /FA01ED/
C     ..
C     .. Executable Statements ..
      IL = GL
      IR = GR
      RETURN

      END
      SUBROUTINE FA01DD(IL,IR)
C     .. Scalar Arguments ..
      INTEGER IL,IR
C     ..
C     .. Common blocks ..
      COMMON /FA01ED/GL,GR
      DOUBLE PRECISION GL,GR
C     ..
C     .. Save statement ..
      SAVE /FA01ED/
C     ..
C     .. Executable Statements ..
      GL = IL
      GR = IR
      RETURN

      END
      BLOCK DATA FA01FD
C     .. Common blocks ..
      COMMON /FA01ED/GL,GR
      DOUBLE PRECISION GL,GR
C     ..
C     .. Save statement ..
      SAVE /FA01ED/
C     ..
C     .. Data statements ..
      DATA GL/21845D0/
      DATA GR/21845D0/
C     ..
C     .. Executable Statements ..
      END
