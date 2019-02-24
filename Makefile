build:
	ELM_HOME=all-elm-pkg-sources time elm-offline || true
	python3 -u ./build-all.py

clobber:
	rm -r all-elm-pkg-sources/
