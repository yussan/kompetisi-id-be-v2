import app 
from flask_mail import Message
from flask import render_template

def sendEmail(title, body, target):
  # ref: https://pythonhosted.org/Flask-Mail/
  msg = Message(title,
                sender="noreply@kompetisi.id",
                recipients=target)
  msg.html = render_template('email/test.html')
  return app.mail.send(msg)
