import sys, os

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

from busyflow.pivotal import PivotalClient

OUT_FILENAME = 'stories.pdf'

def generate_pdf(story, existing_canvas=None):
    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']

    c = existing_canvas or canvas.Canvas(OUT_FILENAME, pagesize=A5)
    #c.setFont("Helvetica", 28)
    # draw some lines
    #a5 is 210 mm * 148 mm
    c.rect(1*cm, 1*cm, 12.8*cm, 19*cm, fill=0)

    c.rotate(90)
    style.fontSize = 24
    style.leading = 24
    story_points = ("%s points" % story['estimate']
                    if ('estimate' in story and story['estimate'])
                    else 'Not estimated')
    title = Paragraph("%s [%s]" % (story['name'],story_points), style)

    title.wrap(17*cm, 4*cm)
    title.drawOn(c, 2*cm, -3.5*cm)

    # c.drawString(2*cm, -3*cm, "%s [%d points]" % (story['Subject'],
    #                                               int(float(story['Story points']))))

    style.fontSize = 14
    style.leading = 16
    description = Paragraph(story['description'], style)
    description.wrap(14*cm, 15*cm)
    description.drawOn(c, 2*cm, -8*cm)
    c.showPage()
    return c

def process_stories(stories):
    canvas = None
    for story in stories:
        canvas = generate_pdf(story, canvas)
    canvas.save()
    print "Stories saved to %s" % OUT_FILENAME

def print_stories():
    if len(sys.argv) != 2:
        print "Usage: print-stories API-KEY"
        return
    client = PivotalClient(token=None, cache='path/to/cache')
    client.token = sys.argv[1]
    projects = client.projects.all()['projects']
    iterations = client.iterations.current(projects[0]['id'])['iterations']
    stories = iterations[0]['stories']
    stories = [x for x in stories if x['current_state'] != 'accepted']
    process_stories(stories)
