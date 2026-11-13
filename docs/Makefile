# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
PYTHON        ?= python3
SPHINX_PARALLEL ?= 8
SOURCEDIR     = source
BUILDDIR      = build/$(SOURCEDIR)

ifneq ($(strip $(SPHINX_PARALLEL)),)
SPHINX_PARALLEL_FLAG = -j $(SPHINX_PARALLEL)
endif

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

doxygen:
	doxygen

.PHONY: help Makefile en zh check-literalincludes check-python-examples #doxygen

check-literalincludes:
	@$(PYTHON) tools/check_literalincludes.py "$(SOURCEDIR)"

check-python-examples:
	@$(PYTHON) tools/check_python_examples.py

en: check-literalincludes check-python-examples
	@$(SPHINXBUILD) -W $(SPHINX_PARALLEL_FLAG) -b html -D language=en "$(SOURCEDIR)" build/html/en $(SPHINXOPTS) $(O)

zh: check-literalincludes check-python-examples
	@$(SPHINXBUILD) -W $(SPHINX_PARALLEL_FLAG) -b gettext "$(SOURCEDIR)" build/gettext $(SPHINXOPTS) $(O)
	@sphinx-intl update -p build/gettext -l zh_CN -d locales
	@$(SPHINXBUILD) -W $(SPHINX_PARALLEL_FLAG) -b html -D language=zh_CN "$(SOURCEDIR)" build/html/zh_CN $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile #doxygen
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
