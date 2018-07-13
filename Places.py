import googlemaps
from datetime import datetime
from googlemaps import convert
import time
import math


class Places(object):

    def __init__(self, key):
        self.__gmaps = googlemaps.Client(key)

    def get_places(self, query_string, location, radius=None):
        '''
        Querys for a list of places from a given string query.

        :param query_string: string to request for the api.
        :type query_string: string, dict, list, or tuple

        :param location: The city to query information from.
        :type location: string, dict, list, or tuple

        :param radius: Distance in meters within which to bias results.
        :type radius: int

        :rtype: List of IDs found.
        '''

        #Gets the limits of the city
        #pinpoints = get_pinpoints(location, radius)

        #Chaneges the location from a string to the coordinates
        location = self.__gmaps.geocode(location)
        location = location[0]['geometry']['location']

        #query for a list of places
        places = self.__gmaps.places(query_string, location, radius)

        #list of places
        places_found = []

        #create a tuple for each place found
        while True:
            for place in places['results']:
                places_found.append(place['place_id'])

            if 'next_page_token' not in places:
                break

            time.sleep(5) #this is needed because Google dennies consecutive requests
            places = self.__gmaps.places(query_string, location, radius, page_token=None if 'next_page_token' not in places else places['next_page_token'])

        return places_found


    def get_pinpoints(self, location, radius=1000):

        location = self.__gmaps.geocode(location)

        #km_degree = 111.32
        #m_degree = km_degree  * 1000
        #radius_per_degree = m_degree/2

        #degree_per_meter = 0.0000089??
        #pin_distance = degree_per_meter * radius

        pace = (radius*2)/111320

        #longitude = convert.normalize_lat_lng(location[0]['geometry']['bounds']['southwest'])[1]
        latitude_limit = convert.normalize_lat_lng(location[0]['geometry']['bounds']['northeast'])[0]
        longitude_limit = convert.normalize_lat_lng(location[0]['geometry']['bounds']['northeast'])[1]

        pinpoints = []

        latitude = convert.normalize_lat_lng(location[0]['geometry']['bounds']['southwest'])[0]
        while abs(latitude) >= abs(latitude_limit):
            longitude = convert.normalize_lat_lng(location[0]['geometry']['bounds']['southwest'])[1]
            while abs(longitude) >= abs(longitude_limit):
                pinpoints.append((latitude,longitude))
                longitude += pace / math.cos(latitude * 0.018) #check
            latitude += pace

        #pinpoints = [location[0]['geometry']['location'],
        #location[0]['geometry']['bounds']['northeast'],
        #location[0]['geometry']['bounds']['southwest']]

        return pinpoints


    def get_place_info(self, ids_list):
        '''
        Querys for details on places based on their IDs.

        :param key: API key from Google Maps API
        :type key: string

        :param ids_list: List of IDs to query.
        :type ids_list: any iterable of strings.

        :rtype: Tuples with name, phone number and website of the places found.
        '''

        places_details = []

        for id in ids_list:
            place_result = self.__gmaps.place(id)['result']
            name = "NA" if 'name' not in place_result else place_result['name']
            phone_number = "NA" if 'formatted_phone_number' not in place_result else place_result['formatted_phone_number']
            website = "NA" if 'website' not in place_result else place_result['website']
            places_details.append((name, phone_number, website))

        return places_details


    def get_vicinities(self, pinpoints, city=None, radius=1000):
        '''
        Tries to find a list of vicinities in a given set of pinpoints.
        :param pinpoints: list of pinpoint.
        :type pinpoints: googlemaps location.

        :param city: City to find the pinpoints. Will actually only remove the
        token 'city' from the formatted address returned by google nearby
        search.

        :param radius: radius of each pinpoint.
        :type radius: int.

        :rtype: list of strings.

        '''
        places = []

        if ", " in city:
            city = city.split(", ")[0]

        for pinpoint in pinpoints:
            places.append(self.__gmaps.places_nearby(pinpoint, radius))

        vicinities = set()
        for place in places:
            for details in place['results']:
                vicinities.add(details['vicinity'])

        result = set()
        for vicinity in vicinities:
            try:
                token = vicinity
                if city not in token:
                    continue

                if " - " not in token:
                    continue

                while " - " in token:
                    token = token.split(" - ")
                    token = token[len(token)-1]

                if(city):
                    if token.endswith(", " + city):
                        token = token.replace(", " + city, "")

                result.add(token)

            except IndexError:
                pass

        return list(result)
