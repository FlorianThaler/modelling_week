PROJECT_NAME = "data_scientist_kern-partner "

MAIN_DOCUMENT_BASE_NAME = main
MAIN_DOCUMENT_FILE_NAME = ${MAIN_DOCUMENT_BASE_NAME}.tex

PDFLATEX_CMD = pdflatex
BIBTEX_CMD = bibtex

.PHONY: pdf
pdf:
	${PDFLATEX_CMD} ${MAIN_DOCUMENT_FILE_NAME}
	${PDFLATEX_CMD} ${MAIN_DOCUMENT_FILE_NAME}

.PHONY: clean
clean:
	-rm -r *.aux *.toc *.log *.nav *.out *.snm *.fls *.fdb_latexmk *.synctex.gz -f
