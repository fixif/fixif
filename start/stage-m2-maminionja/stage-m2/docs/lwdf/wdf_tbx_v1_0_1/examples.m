format compact
format short

fprintf( 'Design of a 3rd order normalized Butterworth lowpass filter\n' );
fprintf( '>> Hs = nlpf(''butter'',3);\n' );
Hs = nlpf('butter',3);
fprintf( 'f(s) and g(s) for decrementing powers of s:\n' );
fs = Hs.poly_fs
gs = Hs.poly_gs

fprintf( 'Figure(1) shows a very simple plot ...\n' );
fprintf( '>> plotHs(Hs);\n' );clf
plotHs(Hs)
figure(1)
fprintf( '\npaused: hit any key to continue ...\n' );
pause

fprintf( '\nNicer plots are shown now ...\n' );
fprintf( '>> plotHs(Hs,2,1,[],2,2000,''Butterworth lowpass'',''3rd order'' );\n' );clf
plotHs(Hs,2,1,[],2,2000,'Butterworth lowpass','3rd order' );
figure(1)
fprintf( '\npaused: hit any key to continue ...\n' );
pause

fprintf( '\nTranformation to the z-domain, normalized cut-off frequency at 0.2\n' );
fprintf( '>> Hs = nlp2lp(Hs,fz2fs(0.2));\n' );
fprintf( '>> Hz = Hs2Hz(Hs);\n' );
Hs = nlp2lp(Hs,fz2fs(0.2));  %gs = butter_gs(3,fz2fs(0.2));
Hz = Hs2Hz(Hs);              %Hz = Hs2Hz( {1;gs} );
fprintf( 'The resulting f(z) and g(z) for decrementing powers of z:\n' );
fz = Hz.poly_fz
gz = Hz.poly_gz
clf
fprintf( 'z-domain plot with a magnitude scaled in dB''s\n' );
fprintf( '>> plotHz(Hz,1);\n' );
plotHz(Hz,1)
figure(1)
fprintf( '\npaused: hit any key to continue ...\n' );
pause

fprintf( '\n\nDesign of a 7th order normalized Inverse Chebyshev lowpass filter\n' );
fprintf( 'Stopband ripple 40 dB, normalized for wn=1 at -3 dB\n' );
fprintf( '>> Hs = nlpf(''invcheby'',7,40,1);\n' );
Hs = nlpf('invcheby',7,40,1);
fprintf( 'f(s) and g(s) for decrementing powers of s:\n' );
fs = Hs.poly_fs
gs = Hs.poly_gs
clf
plotHs(Hs,1)
figure(1)
pause

fprintf( '\nNicer plots are shown now ...\n' );
fprintf( '>> plotHs(Hs,2,1,[0.1 100],2,10000,''Inverse Chebyshev'',''7th order'' );\n' );
plotHs(Hs,2,1,[0.1 100],2,10000,'Inverse Chebyshev','7th order' );
figure(1)
pause

fprintf( '\nTransformation to the z-domain, normalized cutoff frequency at 0.2\n' );
fprintf( '>> Hs = Hs_invcheby(7,40,fz2fs(0.2),1);\n' );
fprintf( '>> Hz = Hs2Hz(Hs);\n' );
Hs = Hs_invcheby(7,40,fz2fs(0.2),1);
Hz = Hs2Hz(Hs);
fprintf( 'The resulting f(z) and g(z) for decrementing powers of z:\n' );
fz = Hz.poly_fz
gz = Hz.poly_gz
clf
fprintf( 'z-domain plot with a magnitude scaled in dB''s\n' );
plotHz(Hz,1,1,[],5000)
figure(1)
pause

fprintf( '\n\n6th order Vlach filter with added stopband zeros and 2 Unit Elements\n' );
fprintf( 'Passband ripple 1 dB, normalized for wn=1 at -3 dB\n' );
fprintf( 'Since we want to design a z-domain filter with a cutoff at 0.15*sampleFrequency,\n')
fprintf( 'and stopband zeros at 0.21 and 0.25, we ''prewarp'' the s-domain\n' );
fprintf( 'stopband zeros to become tan(pi*[0.2 0.25])\n' );
fprintf( '>> Hs = Hs_Vlach(6,1,fz2fs(0.15),fz2fs([0.2 0.25]),2,1);\n' );
Hs = Hs_Vlach(6,1,fz2fs(0.15),fz2fs([0.2 0.25]),2,1);
fprintf( 'f(s) and g(s) for decrementing powers of s:\n' );
fs = Hs.poly_fs{1}
nUEs = Hs.poly_fs{2}
gs = Hs.poly_gs
clf
plotHs(Hs,1)
figure(1)
pause

fprintf( '\nTransformation to the z-domain, ' );
fprintf( 'normalized cutoff frequency will translate to 0.15*sampleFrequency\n' );
fprintf( '>> Hz = Hs2Hz(Hs);\n' );
Hz = Hs2Hz(Hs);
fprintf( 'The resulting f(z) and g(z) for decrementing powers of z:\n' );
fz = Hz.poly_fz{1}
nUEs = Hz.poly_fz{2}
gz = Hz.poly_gz
clf
fprintf( 'z-domain plot with a magnitude scaled in dB''s\n\n' );
plotHz(Hz,1,1,[],5000)
figure(1)
