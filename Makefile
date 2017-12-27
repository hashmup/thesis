INPUT=thesis.tex

OUTPUT=thesis

VIEWER=open -a /Applications/Skim.app

all:
	latexmk -jobname=$(OUTPUT) $(INPUT)

clean:
	latexmk -CA -jobname=$(OUTPUT) $(INPUT)
	find . -name *.aux -delete
	find . -name *.log -delete
	rm -rf *.bbl

view:
	latexmk -pv -jobname=$(OUTPUT) $(INPUT)

watch:
	latexmk -pvc -jobname=$(OUTPUT) $(INPUT)

push: all
	git add -A && git commit && git push origin master
