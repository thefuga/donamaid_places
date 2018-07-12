import googlemaps
from datetime import datetime
from googlemaps import convert
import time
import math


def get_places(key, query_string, location, radius=None):
    '''
    Querys for a list of places from a given string query.

    :param key: API key from Google Maps API
    :type key: string

    :param query_string: string to request for the api.
    :type query_string: string, dict, list, or tuple

    :param location: The city to query information from.
    :type location: string, dict, list, or tuple

    :param radius: Distance in meters within which to bias results.
    :type radius: int

    :rtype: List of IDs found.
    '''

    #Connects my key with the API
    gmaps = googlemaps.Client(key)

    #Gets the limits of the city
    pinpoints = get_pinpoints(key, location, radius)

    #Chaneges the location from a string to the coordinates
    location = gmaps.geocode(location)
    location = location[0]['geometry']['location']

    #query for a list of places
    places = gmaps.places(query_string, location, radius)

    #list of places
    places_found = []

    #create a tuple for each place found
    while True:
        for pinpoint in pinpoints:
            for place in places['results']:
                places_found.append(place['place_id'])

            if 'next_page_token' not in places:
                break

            time.sleep(5) #this is needed because Google refuses consecutive requests
            places = gmaps.places(query_string, pinpoint, radius, page_token=None if 'next_page_token' not in places else places['next_page_token'])

    return places_found


def get_pinpoints(key, location, radius=1000):

    gmaps = googlemaps.Client(key)
    location = gmaps.geocode(location)

    #km_degree = 111.32
    #m_degree = km_degree  * 1000
    #radius_per_degree = m_degree/2

    #degree_per_meter = 0.0000089??
    #pin_distance = degree_per_meter * radius

    pace = (radius/2)/111320

    #longitude = convert.normalize_lat_lng(location[0]['geometry']['bounds']['southwest'])[1]
    latitude_limit = convert.normalize_lat_lng(location[0]['geometry']['bounds']['northeast'])[0]
    longitude_limit = convert.normalize_lat_lng(location[0]['geometry']['bounds']['northeast'])[1]

    pinpoints = []

    latitude = convert.normalize_lat_lng(location[0]['geometry']['bounds']['southwest'])[0]
    while abs(latitude) >= abs(latitude_limit):
        longitude = convert.normalize_lat_lng(location[0]['geometry']['bounds']['southwest'])[1]
        while abs(longitude) >= abs(longitude_limit):
            pinpoints.append((latitude,longitude))
            longitude += pace / math.cos(latitude * 0.018)
        latitude += pace

    #pinpoints = [location[0]['geometry']['location'],
    #location[0]['geometry']['bounds']['northeast'],
    #location[0]['geometry']['bounds']['southwest']]

    return pinpoints

key = 'AIzaSyBgZPQc5CswWQD63YSIiXO_AcS-g4wp-n4'
location = "Pelotas, RS"

gmaps = googlemaps.Client(key)



points = get_pinpoints(key, location, 100000)
len(points)

places = get_places(key, "academia", location, radius=100000)



def get_place_info(key, ids_list):
    '''
    Querys for details on places based on their IDs.

    :param key: API key from Google Maps API
    :type key: string

    :param ids_list: List of IDs to query.
    :type ids_list: any iterable of strings.

    :rtype: Tuples with name, phone number and website of the places found.
    '''
    gmaps = googlemaps.Client(key)
    places_details = []

    for id in ids_list:
        place_result = gmaps.place(id)['result']
        name = "NA" if 'name' not in place_result else place_result['name']
        phone_number = "NA" if 'formatted_phone_number' not in place_result else place_result['formatted_phone_number']
        website = "NA" if 'website' not in place_result else place_result['website']
        places_details.append((name, phone_number, website))

    return places_details
