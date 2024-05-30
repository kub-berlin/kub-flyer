.PHONY: pdf
pdf: KuB-Flyer-ar.pdf KuB-Flyer-de.pdf KuB-Flyer-en.pdf KuB-Flyer-es.pdf KuB-Flyer-fa.pdf KuB-Flyer-fr.pdf KuB-Flyer-ru.pdf

.PHONY: html
html: translations/de.csv templates/content.html templates/style.css .venv
	.venv/bin/python template.py templates/content.html $< > content.html
	.venv/bin/python template.py templates/style.css $< > style.css

KuB-Flyer-%.pdf: translations/%.csv templates/content.html templates/style.css .venv template.py build.py
	.venv/bin/python template.py templates/content.html $< > content.html
	.venv/bin/python template.py templates/style.css $< > style.css
	.venv/bin/python build.py content.html $@
	@rm content.html style.css

.venv:
	python3 -m venv .venv
	.venv/bin/python -m pip install weasyprint
