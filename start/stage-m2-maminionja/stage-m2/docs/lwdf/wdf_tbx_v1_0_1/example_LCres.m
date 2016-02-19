fprintf( 'Design of an LWDF implementation of a simple LC-resonator ...\n\n' );
fprintf( '>> HsNLP = nlpf(''butter'',1);\n' );
fprintf( '>> HsBP  = nlp2bp(HsNLP,fz2fs(0.25),fz2fs(0.020508));\n' );
fprintf( '>> LWDF  = Hs2LWDF(HsBP,1,1,''1,2'');\n\n' );
HsNLP = nlpf('butter',1);
HsBP  = nlp2bp(HsNLP,fz2fs(0.25),fz2fs(0.020508));
LWDF  = Hs2LWDF(HsBP,1,1,'1,2');
