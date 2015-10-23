from django.conf import settings
from django.core import mail

def check_subjects(subjects,outbox=None):
  if not outbox:
    outbox = mail.outbox
  outbox_subjects = [m.subject.replace(settings.EMAIL_SUBJECT_PREFIX,'') for m in outbox]
  success = sorted(subjects) == sorted(outbox_subjects)
  if not success:
    print "desired subjects: ",sorted(subjects)
    print "outbox subjects:  ",sorted(outbox_subjects)
  return success
