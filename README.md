pivotal-printer
===============

Python package to create PDFs from Pivotal Tracker stories through the
API. There was a Ruby version, but the f*#!&# gem would not install.

Installation and Usage
----------------------

1. Install virtualenv

2. Create a virtualenv and activate it

3. Run `python setup.py develop`. This should install the
dependencies.

4. Get your Pivotal Tracker API key. You can find it in the Profile
section. Save it in `~/.pivotal_key`.

5. Run `print-stories FMT`. The argument `FMT` can be one of `pdf` or
`html`; if ommitted, the default is `pdf`.

Your stories should now be saved in `stories.pdf` or `stories.html` in
the same directory, ready for printing.

If the `FMT` argument is used, `reportlab` is used for pdf
generation. If it's `html`, simple string templating is used for
generating a HTML page. The template used for tis purpose is
`stories.html.tmpl`; you can change it to suit your needs.

TODO
----

* Add Ticket ID, assigned to.

* Improve formatting

* Orientation is wrong