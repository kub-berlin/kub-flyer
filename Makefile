.PHONY: vorlage.odt
vorlage.odt:
	rm -f $@
	cd src && zip -r ../$@ *

%.pdf: %.odt
	lowriter --convert-to pdf $<

.PHONY: unp
unp:
	rm -r src/*
	cp vorlage.odt src/x.zip
	cd src && unp x.zip
	rm src/x.zip
	find src -name '*.xml' | while read f; do xmlformat -i "$$f"; done
