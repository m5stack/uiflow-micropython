# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in the docs/ directory.

## Documentation System

This directory contains Sphinx-based documentation for UIFlow2 MicroPython. The documentation is built with reStructuredText (.rst) and published to Read the Docs.

## Building Documentation

```bash
# Build HTML documentation (English)
make html

# Build English version explicitly
make en

# Build Chinese version
make zh

# Clean build artifacts
make clean
```

Built documentation appears in:
- `build/html/en/` - English version
- `build/html/zh_CN/` - Chinese version

## Documentation Structure

```
docs/
├── source/              # Source files
│   ├── index.rst       # Main entry point
│   ├── conf.py         # Sphinx configuration
│   ├── controllers/    # Controller documentation
│   ├── hardware/       # Hardware API docs
│   ├── unit/           # Unit accessories
│   ├── hat/            # HAT accessories
│   ├── base/           # Base modules
│   ├── module/         # Modules
│   ├── chain/          # Chain accessories
│   ├── cap/            # Cap accessories
│   ├── m5ui/           # UI widgets
│   ├── widgets/        # Widget library
│   ├── software/       # Software APIs
│   ├── system/         # System APIs
│   ├── advanced/       # Advanced features
│   ├── quick-reference/# Quick reference
│   └── contribute/     # Contribution guide
├── locales/            # Translation files (Chinese)
├── _static/            # Static assets (CSS, images)
└── requirements.txt    # Python dependencies
```

## Documentation Template

**CRITICAL**: All API documentation must follow the strict template in `source/contribute/template.rst`.

### Required Structure

1. **Title** (with overline/underline `***`)
2. **Overview** - Brief description
3. **Product Support** - List compatible devices
4. **Compatibility Table** (if needed)
5. **UiFlow2 Example** section
   - Example subsections with:
     - Description
     - UiFlow2 block image
     - Example output
6. **MicroPython Example** section
   - Example subsections with:
     - Description
     - Code block (literalinclude or code-block)
     - Example output
7. **API** section
   - Functions
   - Classes with methods/properties/attributes

### reStructuredText Syntax

**Headers**:
```rst
Title (Level 1)
***************

Section (Level 2)
=================

Subsection (Level 3)
--------------------

Subsubsection (Level 4)
^^^^^^^^^^^^^^^^^^^^^^^
```

**Code blocks**:
```rst
.. code-block:: python

    import unit

.. literalinclude:: ../../examples/unit/example.py
    :language: python
    :linenos:
```

**API directives**:
```rst
.. function:: func_name(arg1: int, arg2: str) -> bool

    Function description.

    :param int arg1: Parameter description
    :param str arg2: Parameter description
    :return: Return value description
    :rtype: bool

.. class:: ClassName(arg1: int)

    Class description.

    :param int arg1: Parameter description

    .. method:: ClassName.method_name(arg: int) -> None

        Method description.

        :param int arg: Parameter description
        :return: None

    .. property:: ClassName.property_name
        :type: int

        Property description.

    .. attribute:: ClassName.attr_name
       :type: str

        Attribute description.

    .. data:: ClassName.CONSTANT
       :type: int

        Constant description (uppercase naming).
```

**Notes and warnings**:
```rst
.. note::

    This is a note.

.. warning::

    This is a warning.
```

**Tables**:
```rst
.. table::
    :widths: auto

    +-----------------+-------------------+
    |Controller       | Support           |
    +=================+===================+
    | AtomS3          | |S|               |
    +-----------------+-------------------+

.. |S| unicode:: U+2705
```

**Images**:
```rst
.. image:: /_static/image.png
    :width: 400px
```

**Links**:
```rst
`Link text <https://example.com>`_
```

## Adding New Documentation

1. **Create .rst file** in appropriate directory:
   - `source/unit/` for Unit accessories
   - `source/hat/` for HAT accessories
   - `source/hardware/` for hardware APIs
   - etc.

2. **Follow the template** strictly (`source/contribute/template.rst`)

3. **Add to index** in the parent directory's `index.rst`:
   ```rst
   .. toctree::
       :maxdepth: 2

       new_doc
   ```

4. **Include examples**:
   - UiFlow2 block images in `_static/`
   - MicroPython code in `../../examples/`

5. **Build and verify**:
   ```bash
   make html
   # Check build/html/en/index.html
   ```

## Sphinx Configuration

Key settings in `source/conf.py`:

- **autodoc_mock_imports**: Mock MicroPython modules (micropython, machine, M5, etc.)
- **sys.path**: Points to `../../m5stack/libs/` for autodoc
- **Extensions**: autodoc, napoleon, intersphinx, copybutton
- **Language**: English (default), Chinese (zh_CN)

## Translation Workflow

Chinese translations use `sphinx-intl`:

1. **Extract translatable strings**:
   ```bash
   make gettext
   ```

2. **Update translation files**:
   ```bash
   sphinx-intl update -p build/gettext -l zh_CN -d locales
   ```

3. **Edit** `.po` files in `locales/zh_CN/LC_MESSAGES/`

4. **Build Chinese docs**:
   ```bash
   make zh
   ```

## Documentation Guidelines

### Content

- **Be precise**: Document actual API behavior, not assumptions
- **Include types**: Always specify parameter and return types
- **Show examples**: Every API should have working code examples
- **Test examples**: Verify all code examples actually work
- **Use autodoc**: For Python modules, use `.. autoclass::` and `.. autofunction::`

### Style

- **Consistent naming**: Use exact API names (case-sensitive)
- **Clear descriptions**: Explain what, why, and how
- **Inline code**: Use double backticks for code: `` `variable` ``
- **Cross-references**: Link to related APIs with `:class:`, `:func:`, `:meth:`

### UiFlow2 Integration

- **Block images**: Include screenshots of UiFlow2 blocks
- **Image naming**: Use descriptive names (e.g., `unit_env_init.png`)
- **Image location**: Store in `_static/` or subdirectories
- **Image macros**: Define reusable image references:
  ```rst
  .. |example.m5f2| replace:: example
  ```

## Common Issues

1. **Build warnings**: Treat warnings as errors (`-W` flag in Makefile)
2. **Missing references**: Check that all `:class:`, `:func:` references exist
3. **Autodoc failures**: Ensure modules are in `sys.path` and mocked properly
4. **Encoding errors**: Use UTF-8 encoding for all .rst files
5. **Broken links**: Verify all external links are accessible

## Testing Documentation

Before committing:

1. **Build without warnings**:
   ```bash
   make html
   # Should complete with no warnings
   ```

2. **Check output**: Open `build/html/en/index.html` in browser

3. **Verify links**: Click through navigation and cross-references

4. **Test examples**: Run code examples on actual hardware if possible

## Read the Docs

Documentation is automatically built and published to Read the Docs:

- Configuration: `../.readthedocs.yaml`
- URL: https://uiflow-micropython.readthedocs.io/
- Builds on every commit to main branch

## Related Files

- `../tools/knowledge-base/` - Documentation source for knowledge base
- `../.github/prompts/docs.prompt.md` - Documentation generation prompt
- `../examples/` - Example code referenced in docs
- `../m5stack/libs/` - Python modules documented here

## Documentation Prompt

Use the docs generation prompt (`.github/prompts/docs.prompt.md`) for AI-assisted documentation writing. It enforces the template structure and formatting rules.
