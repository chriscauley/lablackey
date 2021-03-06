from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from .utils import make_ics,ics2response
from .models import Event, EventOccurrence, RSVP, CheckIn, EventRepeat
from lablackey.geo.models import Room, Location
from lablackey.loader import load_class

import datetime, json, arrow, calendar

@staff_member_required
def owner_ajax(request,action,event_id):
  if action == 'own':
    Event.objects.get(id=event_id).eventowner_set.get_or_create(user=request.user)
  elif action == 'disown':
    Event.objects.get(id=event_id).eventowner_set.filter(user=request.user).delete()
  return JsonResponse({'owner_ids': Event.objects.get(id=event_id).owner_ids })

def index(request,daystring=None):
  start = datetime.date.today()
  if daystring:
    start = datetime.datetime.strptime(daystring,'%Y-%m-%d').date()
    dt = start - datetime.date.today()
    if dt.days < -770 or dt.days > 365:
      print "DDoS: %s || %s"%(request.META['HTTP_USER_AGENT'],request.META['REMOTE_ADDR'])
      raise Http404("You have selected a date too far in the future or past.")
  end = start+datetime.timedelta(7)
  year = start.year
  month = start.month
  first = datetime.date(year,month,1)
  weeks = []
  week = []
  if first.isoweekday() != 7:
    week = [('',[])]*first.isoweekday()
  day = 0
  while True:
    day += 1
    try:
      date = datetime.date(year,month,day)
    except ValueError:
      if week:
        weeks.append(week)
      break
    kwargs = dict(start__gte=date,start__lte=datetime.timedelta(1)+date)
    events = EventOccurrence.objects.filter(event__hidden=False,**kwargs).select_related("event")
    if len(week) == 7:
      weeks.append(week)
      week = []
  values = {
    'weeks': weeks,
    'current_date': start,
    'next': datetime.date(year if month!=12 else year+1,month+1 if month!=12 else 1,1),
    'previous': datetime.date(year if month!=1 else year-1,month-1 if month!=1 else 12,1),
  }
  return TemplateResponse(request,'event/index.html',values)

#! TODO DEPRACATED 3/2017
def occurrence_detail(request,occurrence_id,slug=None):
  # NOTE: the above slug does nothing, it is only for prettier urls
  occurrence = get_object_or_404(EventOccurrence,pk=occurrence_id)
  values = {
    'occurrence': occurrence,
  }
  return TemplateResponse(request,'event/occurrence_detail.html',values)

def detail(request,event_id,slug=None):
  # NOTE: ze slug does notzing!
  event = get_object_or_404(Event,id=event_id)
  user_rsvps = None
  if request.user.is_authenticated():
    user_rsvps = event.get_user_rsvps(request.user)
  values = {
    'event': event,
    'rsvps_json': json.dumps(user_rsvps)
  }
  return TemplateResponse(request,'event/detail.html',values)

@cache_page(12*60*60)
def ics(request,module,model_str,pk,fname):
  """Returns an ics file for any `Event` like or `EventOccurrence` like model.
     An `Event` model will add an entry for `Event.all_occurrences()`."""
  model = apps.get_model(module,model_str)
  event = get_object_or_404(model,pk=pk)
  try:
    occurrences = event.all_occurrences
  except AttributeError: # single occurrence
    occurrences = [event]

  calendar_object = make_ics(occurrences,title=event.name)
  return ics2response(calendar_object,fname=fname)

@cache_page(12*60*60)
def all_ics(request,fname):
  occurrences = EventOccurrence.objects.filter(event__hidden=False)
  calendar_object = make_ics(occurrences,title="%s Events"%settings.SITE_NAME)
  return ics2response(calendar_object,fname=fname)

@login_required
def rsvp(request):
  occurrence = get_object_or_404(EventOccurrence,id=request.GET['occurrence_id'])
  event = occurrence.event
  if event.access.icon == "members-only" and request.user.level_id == settings.DEFAULT_MEMBERSHIP_LEVEL:
    return JsonResponse({'error': "Only member's are allowed to RSVP for this event"})
  if event.get_user_rsvps(request.user,status="completed"):
    return JsonResponse({'error': "You have been approved by the TXRX tech to work unattended in this area. There is no need to RSVP. You may come in and work during your regular membership times."})
  kwargs = {
    'content_type_id': EventOccurrence._cid,
    'user': request.user,
    'object_id': request.GET['occurrence_id'],
  }
  if request.GET['quantity'] == '0':
    RSVP.objects.filter(**kwargs).delete()
  else:
    rsvp,new = RSVP.objects.get_or_create(**kwargs)
    rsvp.quantity = request.GET['quantity']
    rsvp.save()
  return JsonResponse(occurrence.event.get_user_rsvps(request.user),safe=False)

def detail_json(request,event_pk):
  event = get_object_or_404(Event,pk=event_pk)
  fields = ['id','name','description','hidden','allow_rsvp','owner_ids']
  out = {key:getattr(event,key) for key in fields}
  fields = ['id','name','total_rsvp','start','end','rsvp_cutoff','past']
  if request.user.is_superuser:
    fields.append("total_rsvp")
  os = event.upcoming_occurrences[:10]
  out['upcoming_occurrences'] = [{key: getattr(o,key) for key in fields} for o in os]
  return JsonResponse(out)

@csrf_exempt
def checkin(request):
  User = get_user_model()
  try:
    user = User.objects.get(rfid__number=request.POST['rfid'])
  except User.DoesNotExist:
    response = HttpResponse("Unable to find that user. Try again or contact the staff.")
    response.status_code=401
    return response
  kwargs = {
    'object_id': request.POST.get('object_id',None),
    'checkinpoint_id': request.POST.get('checkinpoint_id',None),
    'content_type_id': request.POST.get('content_type_id',None),
    'user': user,
  }
  # ignore checkins for the same thing with in 10 minutes of each other
  ten_ago = arrow.now().replace(minutes=-10).datetime
  if not CheckIn.objects.filter(datetime__gte=ten_ago,**kwargs):
    CheckIn.objects.create(**kwargs)
  return HttpResponse(json.dumps("%s has been checked in."%user))

@staff_member_required
def bulk_ajax(request):
  eventrepeat = get_object_or_404(EventRepeat,id=request.GET['eventrepeat_id'])
  if 'day_string' in request.POST:
    st = eventrepeat.start_time
    start = timezone.datetime(*([int(s) for s in request.POST['day_string'].split('-')]+[st.hour,st.minute]))
    if request.POST['action'] == 'remove':
      eventrepeat.month_occurrences.filter(start=start).delete()
    else:
      eventrepeat.eventoccurrence_set.get_or_create(
        start=start,
        end_time=eventrepeat.end_time,
        event=eventrepeat.event
      )
  occurrences = [arrow.get(eo.start).format("YYYY-M-D") for eo in eventrepeat.month_occurrences]
  months = []
  for month in range(5):
    start = arrow.now().replace(day=1,months=month)
    calendar.setfirstweekday(calendar.SUNDAY)
    months.append({
      'name': start.format("MMMM YYYY"),
      'weeks': calendar.monthcalendar(start.year, start.month),
      'number': "%s-%s"%(start.year,start.month)
    })
  return JsonResponse({
    'months': months,
    'occurrences': occurrences,
    'eventrepeat': eventrepeat.as_json,
  })

def conference_json(request):
  events = Event.objects.filter(hidden=False)
  event_owners = events.values_list('eventowner__user_id',flat=True)
  out = {
    'events': [e.as_json for e in events],
    'eventoccurrences': [o.as_json for o in EventOccurrence.objects.filter(event__in=events)],
    'rooms': [r.as_json for r in Room.objects.all()],
    'locations': [l.as_json for l in Location.objects.all()],
    'MAPS_API_KEY': getattr(settings,'MAPS_API_KEY',None),
  }
  if hasattr(settings,'CONFERENCE_JSON_EXTRA'):
    out.update(load_class(settings.CONFERENCE_JSON_EXTRA)())
  return JsonResponse(out)
