import app 
from flask_mail import Message
from flask import render_template, Markup

def sendEmail(title, body, target):
  # ref: https://pythonhosted.org/Flask-Mail/
  # msg = Message(title,
  #               sender="noreply@kompetisi.id",
  #               recipients=target)
  # msg.html = render_template('email/index.html', body=Markup(body))
  # return app.mail.send(msg)
  return True
