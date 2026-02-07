# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build/$(SOURCEDIR)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

doxygen:
	doxygen

.PHONY: help Makefile en zh #doxygen

en:
	@$(SPHINXBUILD) -W -b html -D language=en "$(SOURCEDIR)" build/html/en $(SPHINXOPTS) $(O)

zh:
	@$(SPHINXBUILD) -W -b gettext "$(SOURCEDIR)" build/gettext $(SPHINXOPTS) $(O)
	@sphinx-intl update -p build/gettext -l zh_CN -d locales
	@$(SPHINXBUILD) -W -b html -D language=zh_CN "$(SOURCEDIR)" build/html/zh_CN $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile #doxygen
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
