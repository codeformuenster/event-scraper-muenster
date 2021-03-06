"""Controlls the active scraping."""

import model
import scraper
from time import sleep

# initialize database
model.initialize_database()

# get new event_ids
source = scraper.get_result_source()
all_event_ids = scraper.get_events_from_results(source)
model.add_event_ids_to_db(all_event_ids)

# scrape individual events
all_event_ids = model.get_event_ids()
# read events from DB
events_df = model.read_events_df()

print('new events not crawled: ' +
      str(len(all_event_ids) - len(events_df['id'].tolist())))

# crawl 3 new events
counter = 1
new_events = 300
for event_id in all_event_ids:
    if (event_id not in events_df['id'].tolist()) and (counter <= new_events):
        print("Scaping event " + str(counter) + " of " + str(new_events))
        # scrape to dictionary
        event_source = scraper.get_source_for_event(event_id)
        event_dict = scraper.event_source_to_dict(event_id, event_source)
        # add scraped dictionary to dataframe
        events_df = events_df.append(event_dict, ignore_index=True)
        # increment counter and sleep
        counter += 1
        sleep(5)

# write dataframe to db
model.write_events_df(events_df)
