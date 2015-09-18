from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template, TemplateDoesNotExist
from django.template import Context

def send_template_email(template_name, recipients, from_email=settings.DEFAULT_FROM_EMAIL, context={}):
  if type(recipients) in [unicode,str]:
    recipients = [recipients]
  d = Context(context)
  msg = EmailMultiAlternatives(
    get_template('%s.subject'%template_name).render(d).strip(), # dat trailing linebreak
    get_template('%s.txt'%template_name).render(d),
    from_email,
    recipients)
  try:
    msg.attach_alternative(get_template('%s.html'%template_name).render(d), "text/html")
  except TemplateDoesNotExist:
    pass
  msg.send()

def print_to_mail(subject='Unnamed message',to=[settings.ADMINS[0][1]],notify_empty=lambda:True):
  def wrap(target):
    def wrapper(*args,**kwargs):
      old_stdout = sys.stdout
      sys.stdout = mystdout = StringIO()
      mail_on_fail(target)(*args,**kwargs)

      sys.stdout = old_stdout
      output = mystdout.getvalue()
      if output:
        send_mail(subject,output,settings.DEFAULT_FROM_EMAIL,to)
      elif notify_empty():
        send_mail(subject,"Output was empty",settings.DEFAULT_FROM_EMAIL,to)

    return wrapper
  return wrap
