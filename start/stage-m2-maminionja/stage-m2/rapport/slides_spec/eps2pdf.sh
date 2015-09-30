for epsfile in $(ls images/*.eps)
	do
	epstopdf $epsfile	
	done
