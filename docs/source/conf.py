# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PIC8bit Platform"
copyright = "2025, Sébastien Celles"
author = "Sébastien Celles"
release = "0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "myst_parser",  # For supporting Markdown
    "sphinx_copybutton",  # Copy button for code blocks
    "sphinx_tabs.tabs",  # Tabs
]

templates_path = ["_templates"]
exclude_patterns = []

root_doc = "index"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Furo theme configuration
html_theme = "furo"
html_title = "PIC8bit Platform"

# Furo theme options
html_theme_options = {
    "sidebar_hide_name": True,
    "light_logo": "logo-light.png",
    "dark_logo": "logo-dark.png",
    # Links to source code
    "source_repository": "https://github.com/s-celles/platform-pic8bit",
    "source_branch": "main",
    "source_directory": "docs/source",  # Changed from "docs/" to "" for correct edit link
    # Custom colors
    "light_css_variables": {
        "color-brand-primary": "#2196F3",
        "color-brand-content": "#1976D2",
        "color-admonition-background": "#fafafa",
    },
    "dark_css_variables": {
        "color-brand-primary": "#64B5F6",
        "color-brand-content": "#42A5F5",
    },
    # Navigation
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    # Footer
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/s-celles/platform-pic8bit",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

# HTML metadata
html_meta = {
    "description": "PIC8bit Platform - Support for Microchip's 8-bit PIC microcontrollers in PlatformIO",
    "keywords": "PIC, microcontroller, PlatformIO, XC8, MPLAB, embedded",
    "author": "Sébastien Celles",
}

# Static files
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["custom.js"]

# Favicon
html_favicon = "_static/favicon.ico"

# Additional HTML options
html_scaled_image_link = False
html_show_sourcelink = True
html_copy_source = False
html_show_sphinx = False

# -- Extension configuration -------------------------------------------------

# Configuration for sphinx-copybutton
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# Configuration for tabs
sphinx_tabs_disable_tab_closing = True

# Configuration for intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "platformio": ("https://docs.platformio.org/en/latest/", None),
}

# MyST parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True
