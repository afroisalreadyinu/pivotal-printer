import sys, os
import pickle

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A6
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

import jinja2

from busyflow.pivotal import PivotalClient

OUT_FILENAME = 'stories'
MAX_DESC = 200
PIVOTAL_KEY_FILE = "~/.pivotal_key"
PICKLE_FILE = 'stories.pickle'

class HtmlPrinter(object):

    def __init__(self, stories, filename):
        self.stories = stories
        self.filename = filename

    def print_stories(self):
        template_path = os.path.abspath(os.path.join(__file__, "../stories.html.tmpl"))
        with open(template_path, 'r') as template_file:
            template = jinja2.Template(template_file.read())
        rendered = template.render(stories=self.stories)
        with open(self.filename, 'w') as outfile:
            outfile.write(rendered)

class PdfPrinter(object):

    def __init__(self, stories, filename):
        self.stories = stories
        self.canvas = canvas.Canvas(filename, pagesize=A6)

    def print_stories(self):
        for story in self.stories:
            self.print_story(story)
        self.canvas.save()

    def print_story(self, story):
        styleSheet = getSampleStyleSheet()
        style = styleSheet['BodyText']

        #self.canvas.setFont("Helvetica", 28)
        # draw some lines
        #a5 is 210 mm * 148 mm
        #a6 is 148 mm * 105 mm
        self.canvas.rect(0.5*cm, 0.5*cm, 9.5*cm, 13.8*cm, fill=0)
        self.canvas.rotate(90)

        style.fontSize = 12
        style.leading = 12

        story_points = "Estimate: %s points" % story['estimate']
        points = Paragraph(story_points, style)
        points.wrap(13*cm, 9*cm)
        points.drawOn(self.canvas, 1*cm, -9*cm)


        created_text = "Created on: %s" % story['created_at'].strftime("%d.%m.%Y %H:%M")
        created = Paragraph(created_text, style)
        created.wrap(13*cm, 9*cm)
        created.drawOn(self.canvas, 1*cm, -8*cm)

        status_text = "Status: %s" % story['current_state']
        status = Paragraph(status_text, style)
        status.wrap(13*cm, 9*cm)
        status.drawOn(self.canvas, 1*cm, -7*cm)

        style.fontSize = 16
        style.leading = 16
        id_text = "ID: %s" % story['id']
        id_paragraph = Paragraph(id_text, style)
        id_paragraph.wrap(13*cm, 9*cm)
        id_paragraph.drawOn(self.canvas, 1*cm, -6*cm)

        style.fontSize = 24
        style.leading = 26
        title = Paragraph(story['name'], style)
        title.wrap(13*cm, 2*cm)
        title.drawOn(self.canvas, 1*cm, -4*cm)

        self.canvas.showPage()

def process_stories(stories, print_format):
    out_file = OUT_FILENAME + "." + print_format
    if print_format == 'pdf':
        printer = PdfPrinter(stories, out_file)
        printer.print_stories()
    elif print_format == 'html':
        printer = HtmlPrinter(stories, out_file)
        printer.print_stories()
    print "Stories saved to %s" % out_file

def get_stories(api_token):
    client = PivotalClient(token=None, cache='/tmp')
    client.token = api_token
    projects = client.projects.all()['projects']
    iterations = client.iterations.current(projects[0]['id'])['iterations']
    stories = [x for x in iterations[0]['stories'] if x['current_state'] != 'accepted']
    index = 1
    for story in stories:
        story['estimate'] = story.get('estimate', 'Not estimated')
        story['index'] = index
        index += 1
    return stories

PRINT_FORMAT_ERROR = "Print format has to be one of pdf or html"

def print_stories():
    print_format = sys.argv[1] if len(sys.argv) > 1 else 'pdf'
    assert print_format in ['pdf', 'html'], PRINT_FORMAT_ERROR
    with open(os.path.expanduser(PIVOTAL_KEY_FILE)) as key_file:
        api_key = key_file.read().strip()
    stories = get_stories(api_key)
    process_stories(stories, print_format)

def save_stories():
    with open(os.path.expanduser(PIVOTAL_KEY_FILE)) as key_file:
        api_key = key_file.read().strip()
    stories = get_stories(api_key)
    with open(PICKLE_FILE, 'wb') as pickle_file:
        pickle_file.write(pickle.dumps(stories))
    print "Wrote stories to %s" % PICKLE_FILE

def print_from_file():
    print_format = sys.argv[1] if len(sys.argv) > 1 else 'pdf'
    assert print_format in ['pdf', 'html'], PRINT_FORMAT_ERROR
    with open(PICKLE_FILE, 'rb') as pickle_file:
        stories = pickle.loads(pickle_file.read())
    process_stories(stories, print_format)
