import Places
import googlemaps


key = 'AIzaSyBgZPQc5CswWQD63YSIiXO_AcS-g4wp-n4'
location = "Lajeado, RS"

pinpoints = seek_places.get_pinpoints(key, location, radius=2000)
len(pinpoints)
gmaps = googlemaps.Client(key)

places = []

for pinpoint in pinpoints:
    places.append(gmaps.places_nearby(location=pinpoint, radius=2000))


vicinities = []
for place in places:
    for details in place['results']:
        vicinities.append(details['vicinity']) if details['vicinity'].endswith('Lajeado') and not details['vicinity'].startswith("Lajeado") else None

separator = "-"
result = set()
for vicinity in vicinities:
    try:
        result.add(vicinity.split(separator, 1)[1].replace(", Lajeado", ""))
    except IndexError:
        pass

result=list(result)
for x in result:
    if "-" in x:
        result.remove(x)
result
len(result)
