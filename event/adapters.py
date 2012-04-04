from django.conf import settings

from lablackey.djangogcal.adapter import CalendarAdapter, CalendarEventData
from lablackey.djangogcal.observer import CalendarObserver

from models import Event

class EventCalendarAdapter(CalendarAdapter):
    """
    A calendar adapter for the Showing model.
    """
    
    def get_event_data(self, instance):
        """
        Returns a CalendarEventData object filled with data from the adaptee.
        """
        return CalendarEventData(
            start=instance.start_time,
            end=instance.end_time,
            title=instance.title
        )

observer = CalendarObserver(email=settings.CALENDAR_EMAIL,
                            password=settings.CALENDAR_PASSWORD)
observer.observe(Showing, ShowingCalendarAdapter())
