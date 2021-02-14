import caldav

class CalDav():

    client = None

    def __init__(self, url:str, username:str, password:str):
        self.client = caldav.DAVClient(url=url, username=username, password=password)

    def fetch_calendar(self, name=None, calid=None):
        principal = self.client.principal()
        return principal.calendar(name, calid)

    def add_event(self, event, calendar):
        event = self._clean_event(event)
        c = calendar.save_event(event)
        if c:
            return True
        return False

    def _clean_event(self, event):
        event = event.replace("METHOD:PUBLISH", "")
        event = event.replace("SUMMARY:", "SUMMARY:Permanence ")
        return event