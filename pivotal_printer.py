import sys, os
import pickle

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A6
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

from busyflow.pivotal import PivotalClient

OUT_FILENAME = 'stories.pdf'
MAX_DESC = 200
PIVOTAL_KEY_FILE = "~/.pivotal_key"
PICKLE_FILE = 'stories.pickle'
def generate_pdf(story, existing_canvas=None):
    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']

    c = existing_canvas or canvas.Canvas(OUT_FILENAME, pagesize=A6)
    #c.setFont("Helvetica", 28)
    # draw some lines
    #a5 is 210 mm * 148 mm
    #a6 is 148 mm * 105 mm
    c.rect(0.5*cm, 0.5*cm, 9.5*cm, 13.8*cm, fill=0)
    c.rotate(90)

    style.fontSize = 12
    style.leading = 12

    story_points = ("Estimate: %s points" % story['estimate']
                    if ('estimate' in story and story['estimate'])
                    else 'Not estimated')
    points = Paragraph(story_points, style)
    points.wrap(13*cm, 9*cm)
    points.drawOn(c, 1*cm, -9*cm)


    created_text = "Created on: %s" % story['created_at'].strftime("%d.%m.%Y %H:%M")
    created = Paragraph(created_text, style)
    created.wrap(13*cm, 9*cm)
    created.drawOn(c, 1*cm, -8*cm)

    status_text = "Status: %s" % story['current_state']
    status = Paragraph(status_text, style)
    status.wrap(13*cm, 9*cm)
    status.drawOn(c, 1*cm, -7*cm)

    style.fontSize = 16
    style.leading = 16
    id_text = "ID: %s" % story['id']
    id_paragraph = Paragraph(id_text, style)
    id_paragraph.wrap(13*cm, 9*cm)
    id_paragraph.drawOn(c, 1*cm, -6*cm)

    style.fontSize = 24
    style.leading = 26
    title = Paragraph(story['name'], style)
    title.wrap(13*cm, 2*cm)
    title.drawOn(c, 1*cm, -4*cm)

    c.showPage()
    return c

def process_stories(stories):
    canvas = None
    for story in stories:
        canvas = generate_pdf(story, canvas)
    canvas.save()
    print "Stories saved to %s" % OUT_FILENAME

def get_stories(api_token):
    client = PivotalClient(token=None, cache='/tmp')
    client.token = api_token
    projects = client.projects.all()['projects']
    iterations = client.iterations.current(projects[0]['id'])['iterations']
    stories = iterations[0]['stories']
    return [x for x in stories if x['current_state'] != 'accepted']

def print_stories():
    with open(os.path.expanduser(PIVOTAL_KEY_FILE)) as key_file:
        api_key = key_file.read().strip()
    stories = get_stories(api_key)
    process_stories(stories)

def save_stories():
    with open(os.path.expanduser(PIVOTAL_KEY_FILE)) as key_file:
        api_key = key_file.read().strip()
    stories = get_stories(api_key)
    with open(PICKLE_FILE, 'wb') as pickle_file:
        pickle_file.write(pickle.dumps(stories))
    print "Wrote stories to %s" % PICKLE_FILE

def print_from_file():
    with open(PICKLE_FILE, 'rb') as pickle_file:
        stories = pickle.loads(pickle_file.read())
    process_stories(stories)
