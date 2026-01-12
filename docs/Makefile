.PHONY: help clean html html-zh all livehtml

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean      to remove built files"
	@echo "  html       to make standalone HTML files (English)"
	@echo "  html-zh    to make standalone HTML files (Chinese)"
	@echo "  all        to make both English and Chinese HTML"
	@echo "  livehtml   to serve docs with live reloading (requires sphinx-autobuild)"

clean:
	rm -rf _build
	@echo "Cleaned build files."

html:
	uv run sphinx-build -b html . _build/en
	@echo ""
	@echo "Build finished. The HTML pages are in _build/en."

html-zh:
	mkdir -p _build/zh
	cp conf_zh.py _build/zh/conf.py
	uv run sphinx-build -b html -c _build/zh . _build/zh
	@echo ""
	@echo "Build finished. The Chinese HTML pages are in _build/zh."

all: html html-zh
	@echo ""
	@echo "All documentation built successfully."
	@echo "Open _build/en/index.html for English"
	@echo "Open _build/zh/index.html for Chinese"

livehtml:
	uv run sphinx-autobuild . _build/html --ignore "*~" --ignore "*.swp"
