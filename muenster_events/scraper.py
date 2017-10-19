"""Scrape muenster.de for events."""

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
import re
import requests


def get_result_source():
    """Get source of events results page."""
    link = "http://www.stadt-muenster.de/de/tourismus/veranstaltungen/" \
           "veranstaltungskalender.html"
    # run browser headless
    display = Display(visible=0, size=(800, 600))
    display.start()
    # get search result
    driver = webdriver.Firefox()
    driver.get(link)
    elem = driver.find_element_by_name("submit")
    elem.click()
    return driver.page_source


def get_events_from_results(source):
    """Get list of event IDs from source of events results page."""
    soup = BeautifulSoup(source, 'html.parser')
    p = re.compile("veranstaltung.php\?id=([0-9]+)&")
    events = p.findall(str(soup))
    return events


def get_source_for_event(event):
    """Get html source for event_id."""
    resp = requests.get("https://www.muenster.de/veranstaltungskalender/scr" +
                        "ipts/frontend/mm2/veranstaltung.php?id=" + event)
    content = resp.content
    return content


def event_source_to_dict(event_source):
    """Extract event properties from source and store in dictionary."""
    soup = BeautifulSoup(event_source, 'html.parser')
    event_dict = {}
    event_dict['title'] = soup.find("div", class_="titel")
    event_dict['subtitle'] = soup.find("div", class_="untertitel")
    event_dict['time'] = soup.find("div", class_="datum-uhrzeit")
    event_dict['address'] = soup.find("div", class_="location-adresse")
    event_dict['details'] = soup.find("div", class_="detailbeschreibung")
    event_dict['link'] = soup.find('a', class_='extern')
    # get stripped content from html tag
    for key in event_dict.keys():
        if event_dict[key] is not None:
            event_dict[key] = event_dict[key].contents[0].strip()
        else:
            event_dict[key] = ""
    return event_dict


source = get_result_source()
events = get_events_from_results(source)
event_source = get_source_for_event(events[1])
event_dict = event_source_to_dict(event_source)
event_dict
