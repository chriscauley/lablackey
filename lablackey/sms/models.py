from django.conf import settings
from django.db import models
from django.utils import timezone

from lablackey.db.models import UserModel

from twilio.rest import TwilioRestClient
import random, datetime

class Message(object):
  body = to = from_  = None

_digits = getattr(settings,"TWILIO_VERIFICATION_DIGITS",4)
_days = getattr(settings,"TWILIO_EXPIRATION_SECONDS",20*60)

def random_code():
  return random.randint(10**(_digits-1),10**_digits)
def expiry():
  return timezone.now()+datetime.timedelta(0,_days)

class SMSNumber(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL,null=True,blank=True)
  number = models.CharField(max_length=16,unique=True)
  verified = models.DateTimeField(null=True,blank=True)
  code = models.IntegerField(default=random_code)
  expire = models.DateTimeField(default=expiry)
  def send_verification(self):
    self.code = random_code()
    self.expire = expiry()
    self.save()
    self.send("Code: %s for %s"%(self.code,settings.SITE_NAME))
  __unicode__ = lambda self: "%s - %s"%(self.number,self.user)
  def send(self,body,from_=settings.TWILIO_NUMBER):
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(to=self.number,from_=from_,body=body)
  def call(self,url,from_=settings.TWILIO_NUMBER):
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    client.calls.create(to=self.number,from_=from_,url=url)
    
if getattr(settings,'TESTING',None):
  from lablackey import sms
  sms.outbox = []
  def _send(self,body,from_=settings.TWILIO_NUMBER):
    m = Message()
    m.body = body
    m.to = self.number
    m.from_ = from_
    sms.outbox.append(m)
    print "SMS to %s: %s"%(self.number,body)
  SMSNumber.send = _send
