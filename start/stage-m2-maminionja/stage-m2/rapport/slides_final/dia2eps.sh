for diafile in $(ls images/*.dia)
	do
	file=$(basename $diafile .dia)
	echo $file
	dia --nosplash --export=images/$file.eps $diafile
	done
