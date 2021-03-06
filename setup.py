from setuptools import setup, find_packages

setup(
    name = "pivotal-printer",
    version = "0.01",
    author = "Ulas Tuerkmen ",
    install_requires = ["reportlab==2.6", "busyflow.pivotal==0.3.4", "httplib2", 'jinja2'],
    packages=find_packages(),
    zip_safe=False,
    entry_points = {'console_scripts': ['print-stories = pivotal_printer:print_stories',
                                        'save-stories =  pivotal_printer:save_stories',
                                        'print-from-file =  pivotal_printer:print_from_file']}
)
