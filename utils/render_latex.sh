#!/bin/bash
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
bibtex main
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
pandoc main.tex --bibliography=refs.bib -o main.docx

pdflatex -synctex=1 -interaction=nonstopmode -file-line-error supplements.tex
bibtex supplements
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error supplements.tex
pandoc supplements.tex --bibliography=refs.bib -o supplements.docx
