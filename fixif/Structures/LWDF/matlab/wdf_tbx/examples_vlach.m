warning('off','MATLAB:dispatcher:InexactMatch')
close all
fprintf( 'A 5th order vlach lowpass, 0.5 dB passband ripple, ....\n' );
fprintf( '>> Hs = Hs_Vlach(5,0.5,1,[3 4],0,0);\n\n' );
Hs = Hs_Vlach(5,0.5,1,[3 4],0,0);
plotHs(Hs,1,1,[],[],10000)
pause

fprintf( 'Same parameters as before, but now cut-off frequency normalized at -3 dB level\n' );
fprintf( '>> Hs = Hs_Vlach(5,0.5,1,[3 4],0,1);\n\n' );
Hs3 = Hs_Vlach(5,0.5,1,[3 4],0,1);   
plotHs([Hs Hs3],1,1,[],[],10000)
pause

fprintf( 'Now for a cut-off frequency at 2 instead of at 1 rad/s\n' ); 
fprintf( '>> Hs = Hs_Vlach(5,0.5,2,[3 4],0,0);\n\n' );
Hs = Hs_Vlach(5,0.5,2,[3 4],0,0);
plotHs(Hs,1,1,[],[],10000)
pause
fprintf( '... and with -3 dB cut-off frequency normalization\n' );
fprintf( '>> Hs = Hs_Vlach(5,0.5,2,[3 4],0,1);\n\n' );
Hs3 = Hs_Vlach(5,0.5,2,[3 4],0,1);   
plotHs([Hs Hs3],1,1,[],[],10000)
pause

fprintf( 'Just for fun: Also possible for passband ripples larger than -3 dB\n' );
fprintf( '>> Hs = Hs_Vlach(5,6,2,[3 4],0,1);\n\n' );
Hs = Hs_Vlach(5,6,2,[3 4],0,1);     
plotHs(Hs,1,1,[],[],10000)
pause
fprintf( '... and for cut-off frequency smaller than 1 rad/s,\n' );
fprintf( 'also one stopband zero smaller than 1\n' );
fprintf( '>> Hs = Hs_Vlach(5,6,0.5,[0.7 4],0,1);\n\n' );
Hs2 = Hs_Vlach(5,6,0.5,[0.7 4],0,1); 
plotHs([Hs Hs2],1,1,[],[],10000)
pause


fprintf( 'A 5th order low-pass filter with 10 additional unit elements\n' );
fprintf( '>> Hs = Hs_Vlach(5,1,1.5,[2.5 3],10,0);\n\n' ); 
Hs = Hs_Vlach(5,1,1.5,[2.5 3],10,0);  
plotHs(Hs,1,1,[],[],10000)
pause

fprintf( 'Now only the 10 unit elements, cut-off frequency at 1.5 rad/s\n' );
fprintf( '>> Hs = Hs_Vlach(0,1,1.5,[],10,0);\n\n' );
Hs = Hs_Vlach(0,1,1.5,[],10,0);	   
plotHs(Hs,1,1,[],[],10000)
pause
fprintf( '... and with -3 dB cut-off frequency normalization\n' );
fprintf( '>> Hs3 = Hs_Vlach(0,1,1.5,[],10,1);\n\n' );
Hs3 = Hs_Vlach(0,1,1.5,[],10,1);	   
plotHs([Hs Hs3],1,1,[],[],10000)
pause

fprintf( 'If not specified, default values for number of unit elements (0)\n' );
fprintf( 'and normalization method (0) are used:\n' );
fprintf( '>> Hs = Hs_Vlach(7,1,2,[2.5 3]);\n\n' );
Hs = Hs_Vlach(7,1,2,[2.5 3]);		   
plotHs(Hs,1,1,[],[],10000)
pause

fprintf( 'Nine (9) unit elements constructing a ladder filter\n' );
fprintf( '>> NlpLadder = nlp_ladder(''vlach'',0,1,[],[], [ 1 1 1 1 1 1 1 1 1  ] );\n\n' );
NlpLadder = nlp_ladder('vlach',0,1,[],[], [ 1 1 1 1 1 1 1 1 1  ] );
pause

fprintf( '\nFinally, a lumped element ladder filter (3rd order) with 2 unit elements\n' );
fprintf( 'that do contribute to the transfer function:\n' );
fprintf( '>> NlpLadder = nlp_ladder(''vlach'',3,1,1.5,[1], [ 0 1 1 ] );\n' );
NlpLadder = nlp_ladder('vlach',3,1,1.5,[1], [ 0 1 1 ] )
pause

fprintf( '\nIf constructed with transmission lines, this would become the transfer function ...\n' );
Hs = Hs_Vlach(3,1,1,1.5,2);
Hz = Hs2Hz(Hs);
plotHz(Hz,1,3);
xy = get(figure(2),'Position');		   
set(figure(3),'Position', [ 1.07 0.95 1 1].*xy );
