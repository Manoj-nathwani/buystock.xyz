import os
import jinja2
import webapp2
import pusher

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
template = JINJA_ENVIRONMENT.get_template('app/index.html')

client = pusher.Pusher(
    app_id=os.environ["pusher_app_id"],
    key=os.environ["pusher_key"],
    secret=os.environ["pusher_secret"])


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(template.render())


class Push(webapp2.RequestHandler):
    def get(self):
        event = self.request.get('event')
        company = self.request.get('company')
        client.trigger(u'my_channel', event, {u'company': company})
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.write("Sent")


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/push', Push)
], debug=True)
