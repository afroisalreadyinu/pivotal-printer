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

4. Run `print-stories "API-KEY"`. You can find your API-KEY in the
Profile section of Pivotal Tracker.

Your stories should now be saved in `stories.pdf` in the same
directory, ready for printing.

TODO
----

* Add Ticket ID, status, assigned to, created on.

* Cut description if it's too long.

* Improve formatting

* Read from `.pivotal_key` file if no key is provided.

* Orientation is wrong