import json
from dataclasses import asdict
from realestate_com_au import RealestateComAu
from datetime import datetime
from dateutil import parser

from pymongo_get_database import get_database

api = RealestateComAu()

dbname = get_database()
buyListingsCollection = dbname["buy_listings"]
soldListingsCollection = dbname["sold_listings"]


def saveListings(listings, collection):
	for listing in listings:
		dictListing = asdict(listing)

		dictListing.pop('images', None)
		dictListing.pop('images_floorplans', None)
		dictListing.pop('listers', None)
		dictListing.pop('inspections', None)
		dictListing.pop('description', None)
		dictListing.pop('shot_address', None)
		dictListing.pop('listing_company_id', None)
		dictListing.pop('listing_company_name', None)
		dictListing.pop('listing_company_phone', None)

		dictListing['scraped_date'] = datetime.now()

		collection.insert_one(dictListing)

def main():

	print('Pulling down BUY listings')

	buyListings = api.search(
	    locations=["place"], # search term
	    channel="buy", # listing type
	    sort_type="new-desc", # sort method
	    limit=200 # number of articles to collect
	)

	print('Pulling down SOLD listings')

	soldListings = api.search(
	    locations=["place"], # search term
	    channel="sold", # listing type
	    sort_type="new-desc", # sort method
	    limit=200 # number of articles to collect
	)

	print('Saving scrape')

	saveListings(buyListings, buyListingsCollection)
	saveListings(soldListings, soldListingsCollection)

	print('Scrape complete')


main()