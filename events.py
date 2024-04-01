from enum import Enum
from bs4 import BeautifulSoup
import re
import cloudscraper
import json


class EventType(Enum):
    MAJOR = 1
    INTERNATIONAL_LAN = 2
    REGIONAL_LAN = 3
    ONLINE = 4
    LOCAL_LAN = 5

class Event:
    def __init__(self, event_id, name):
        self.event_id = event_id
        self.name = name

def get_events(event_type):
    scraper = cloudscraper.create_scraper()

    html = scraper.get('https://www.hltv.org/events?eventType={}#tab-TODAY'.format(EventType(event_type).name))
    bs = BeautifulSoup(html.content, 'html.parser')
    current_events_section = bs.find(id='TODAY')

    result = []

    current_events = current_events_section.find_all('a')

    pattern = r'\d+'

    for event in current_events:
        event_name = event.find('td', class_='event-name-col').find('div', class_='text-ellipsis').text
        event_id = re.findall(pattern, event['href'])[0]
        result.append({"event_id": event_id, "event_name": event_name})

    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return json_result


print(get_events(4))


