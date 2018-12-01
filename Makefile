.PHONY: pdf
pdf: ar.pdf de.pdf en.pdf es.pdf fa.pdf fr.pdf

.PHONY: odt
odt: ar.odt de.odt en.odt es.odt fa.odt fr.odt

%.pdf: %.odt
	lowriter --convert-to pdf $<

%.odt: %.csv templates/content.xml templates/styles.xml templates/Pictures/*.svg template.py
	python template.py templates/content.xml $< > src/content.xml
	python template.py templates/styles.xml $< > src/styles.xml
	python template.py templates/Pictures/bg1.svg $< > src/Pictures/bg1.svg
	python template.py templates/Pictures/bg2.svg $< > src/Pictures/bg2.svg
	python template.py templates/Pictures/box1.svg $< > src/Pictures/box1.svg
	python template.py templates/Pictures/box2.svg $< > src/Pictures/box2.svg
	python template.py templates/Pictures/box3.svg $< > src/Pictures/box3.svg
	python template.py templates/Pictures/box4.svg $< > src/Pictures/box4.svg
	@rm -f $@
	cd src && zip -r ../$@ *
	@rm src/content.xml src/styles.xml src/Pictures/bg*.svg src/Pictures/box*.svg

.PHONY: unp
unp:
	rm -r src/*
	cp vorlage.odt src/x.zip
	cd src && unp x.zip
	rm src/x.zip
	find src -name '*.xml' | while read f; do xmlformat -i "$$f"; done
