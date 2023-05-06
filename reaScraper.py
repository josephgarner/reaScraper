import json
from dataclasses import asdict
from realestate_com_au import RealestateComAu
from datetime import datetime
from dateutil import parser

from pymongo_get_database import get_database

api = RealestateComAu()

dbname = get_database()
buyListingsCollection = dbname["buy_listings_test"]
soldListingsCollection = dbname["sold_listings_test"]


def saveListings(listings, collection):
	for listing in listings:
		dictListing = asdict(listing)

		dictListing.pop('images', None)
		dictListing.pop('images_floorplans', None)
		dictListing.pop('listers', None)
		dictListing.pop('inspections', None)
		dictListing.pop('description', None)
		dictListing.pop('listing_company_id', None)
		dictListing.pop('listing_company_name', None)
		dictListing.pop('listing_company_phone', None)

		dictListing['scraped_date'] = datetime.now()

		newdata = [{ "$set": {
    	"badge" : dictListing['badge'],
    	"url" : dictListing['url'],
    	"suburb" : dictListing['suburb'],
    	"state" : dictListing['state'],
    	"postcode" : dictListing['postcode'],
    	"short_address" : dictListing['short_address'],
    	"full_address" : dictListing['full_address'],
    	"property_type" : dictListing['property_type'],
    	"price" : dictListing['price'],
    	"price_text" : dictListing['price_text'].replace("$",""),
    	"bedrooms" : dictListing['bedrooms'],
    	"bathrooms" : dictListing['bathrooms'],
    	"parking_spaces" : dictListing['parking_spaces'],
    	"building_size" : dictListing['building_size'],
    	"building_size_unit" : dictListing['building_size_unit'],
    	"land_size" : dictListing['land_size'],
    	"land_size_unit" : dictListing['land_size_unit'],
    	"auction_date" : dictListing['auction_date'],
    	"available_date" : dictListing['available_date'],
    	"sold_date" : dictListing['sold_date'],
    	"starred" : { "$eq": [ "$starred", True ] },
    	"scraped_date" : dictListing['scraped_date']
		} }]

		print(dictListing['id'])
		print(dictListing['price_text'])

		print(newdata)

		collection.update_one({"id": dictListing["id"]}, newdata, True)

def main():

	print('Pulling down BUY listings')

	buyListings = api.search(
	    locations=["Altona Meadows"], # search term
	    channel="buy", # listing type
	    sort_type="new-desc", # sort method
	    limit=10 # number of articles to collect
	)

	print('Pulling down SOLD listings')

	# soldListings = api.search(
	#     locations=["suburbs"], # search term
	#     channel="sold", # listing type
	#     sort_type="new-desc", # sort method
	#     limit=100 # number of articles to collect
	# )

	print('Saving scrape')

	saveListings(buyListings, buyListingsCollection)
	# saveListings(soldListings, soldListingsCollection)

	print('Scrape complete')


main()