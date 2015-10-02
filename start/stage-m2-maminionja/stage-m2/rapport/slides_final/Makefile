TEX=RAVOSON_presentation_FxPS
FIGREP=images

all: eps pdf $(TEX).pdf view

# generate main PDF ___________
$(TEX).pdf: $(TEX).tex 
	pdflatex $(TEX)
	pdflatex $(TEX)

# view PDF _____________
view:
	evince $(TEX).pdf &


# convert images to pdf _________________________________________________________
# rule : dia to eps
eps:
	./dia2eps.sh
	 
# rule : eps to pdf
pdf:
	./eps2pdf.sh	


# clean generated files __________________________________________________________
clean:
	rm -f *.aux $(TEX).toc $(TEX).nav $(TEX).out $(TEX).pdf $(TEX).snm *.log 
	rm -f $(FIGREP)/*.eps $(FIGREP)/*.pdf $(TEX).synctex.gz
