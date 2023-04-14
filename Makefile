.PHONY: pdf
pdf: KuB-Flyer-ar.pdf KuB-Flyer-de.pdf KuB-Flyer-en.pdf KuB-Flyer-es.pdf KuB-Flyer-fa.pdf KuB-Flyer-fr.pdf

.PHONY: odt
odt: KuB-Flyer-ar.odt KuB-Flyer-de.odt KuB-Flyer-en.odt KuB-Flyer-es.odt KuB-Flyer-fa.odt KuB-Flyer-fr.odt

%.pdf: %.odt
	lowriter --convert-to pdf $<

KuB-Flyer-%.odt: %.csv templates/content.xml templates/styles.xml templates/Pictures/*.svg template.py
	python template.py templates/content.xml $< > src/content.xml
	python template.py templates/styles.xml $< > src/styles.xml
	python template.py templates/Pictures/box1.svg $< > src/Pictures/box1.svg
	python template.py templates/Pictures/box2.svg $< > src/Pictures/box2.svg
	python template.py templates/Pictures/box3.svg $< > src/Pictures/box3.svg
	python template.py templates/Pictures/box4.svg $< > src/Pictures/box4.svg
	@rm -f $@
	cd src && zip -r ../$@ *
	@rm src/content.xml src/styles.xml src/Pictures/box*.svg

.PHONY: unp
unp:
	rm -r src/*
	cp vorlage.odt src/x.zip
	cd src && unp x.zip
	rm src/x.zip
	find src -name '*.xml' | while read f; do xmlformat -i "$$f"; done
