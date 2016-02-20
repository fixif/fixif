close all
fprintf( 'Design of a lumped low-pass ladder filter, cauer type: \n' );
fprintf( '>> Ladder = nlp_ladder(''cauer'',5,1,45,''a'',1);\n\n' );
Ladder = nlp_ladder('cauer',5,1,45,'a',1);
fprintf( '\npaused: hit any key to continue ...\n' );
pause

fprintf( '\nThis low-pass ladder translated to a symmetric all 3-port WDF ... \n' );
fprintf( '>> WDF = ladder2WDF(Ladder,''3p_sym'');\n\n' );
WDF = ladder2WDF(Ladder,'3p_sym');
fprintf( 'paused: hit any key to continue ...\n' );
pause

fprintf( '\nTransformation to a band-pass ladder: \n' );
fprintf( '>> BpLadder = nladder2bp(Ladder,fz2fs(0.15),0.1);\n\n' );
BpLadder = nladder2bp(Ladder,fz2fs(0.15),0.1);
showLadder(BpLadder);
fprintf( '\npaused: hit any key to continue ...\n' );
pause

fprintf( '\nThis band-pass ladder translated to an all 3-port WDF ... \n' );
fprintf( '>> WDF1 = ladder2WDF(BpLadder,''3p'',2048);\n\n' );
WDF1 = ladder2WDF(BpLadder,'3p',2048);
fprintf( 'paused: hit any key to continue ...\n' );
pause

fprintf( '\n... or to a WDF with 2-port translations of resonator circuits: \n' );
fprintf( '>> WDF1 = WDF1 = ladder2WDF(BpLadder,''2p'',2048);\n\n' );
WDF2 = ladder2WDF(BpLadder,'2p',2048);
fprintf( 'paused: hit any key to continue ...\n' );
pause

close all
fprintf( '\nFinally an LWDF realization of the same transfer function: \n' );
fprintf( '>> Hs = nlpf(''cauer'',5,1,45,''a'',1);\n' );
fprintf( '>> HsBp = nlp2bp(Hs,fz2fs(0.15),0.1);\n' );
fprintf( '>> [LWDF,Hz] = Hs2LWDF(HsBp);\n\n' );
Hs = nlpf('cauer',5,1,45,'a',1);
HsBp = nlp2bp(Hs,fz2fs(0.15),0.1);
[LWDF,Hz] = Hs2LWDF(HsBp);
plotHz(Hz,1,2);
