from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail, mail_admins
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import get_template, TemplateDoesNotExist
from django.template import Context, RequestContext
from cStringIO import StringIO

import sys, traceback, markdown

def render_template(name,context):
  html = None
  for ext in ['html','md']:
    try:
      html = get_template("%s.%s"%(name,ext)).render(context)
      break
    except TemplateDoesNotExist:
      pass
  if html and ext == 'md':
    html = markdown.markdown(html,safe=True)
  text = None
  try:
    text = get_template("%s.%s"%(name,ext)).render(context)
  except TemplateDoesNotExist:
    pass
  return html,text

def send_template_email(template_name, recipients, request=None,
                        from_email=settings.DEFAULT_FROM_EMAIL, context={}):
  if type(recipients) in [unicode,str]:
    recipients = [recipients]
  if not 'settings' in context:
    context['settings'] = {a: getattr(settings,a,None) for a in getattr(settings,"PUBLIC_SETTINGS",['DEBUG'])}
  preface = ''
  bcc = []
  html,text = render_template(template_name,context)
  send_mail(
    get_template('%s.subject'%template_name).render(context).strip(), # dat trailing linebreak
    text,
    from_email,
    recipients,
    html_message=html
  )
  return html,text

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

def mail_on_fail(target):
  def wrapper(*args,**kwargs):
    try:
      return target(*args,**kwargs)
    except Exception, err:
      lines = [
        "An unknown erro has occurred when executing the following function:",
        "name: %s"%target.__name__,
        "args: %s"%args,
        "kwargs: %s"%kwargs,
        "",
        "traceback:\n%s"%traceback.format_exc(),
        ]
      mail_admins("Error occurred via 'mail_on_fail'",'\n'.join(lines))
  return wrapper

def filter_emails(emails):
  if settings.DEBUG:
    #only email certain people from dev server!
    return [e for e in emails if e in getattr(settings,'ALLOWED_EMAILS',[])]

class DebugBackend(EmailBackend):
  def send_messages(self,email_messages):
    if not settings.DEBUG:
      return super(DebugBackend,self).send_messages(email_messages)
    for message in email_messages:
      if not settings.EMAIL_SUBJECT_PREFIX in message.subject:
        message.subject = "%s%s"%(settings.EMAIL_SUBJECT_PREFIX,message.subject)
      message.to = filter_emails(message.to) or [getattr(settings,'ALLOWED_EMAILS',[])[0]]
      message.cc = filter_emails(message.cc)
      message.bcc = filter_emails(message.bcc)
    return super(DebugBackend,self).send_messages(email_messages)
