import create_dataset
import Places

if __name__ == "__main__":

    gplaces = Places.Places("AIzaSyBgZPQc5CswWQD63YSIiXO_AcS-g4wp-n4")
    #cities = ("Londrina, PR", "Maringa, PR", "Caxias, RS", "Pelotas, RS", "Rio Grande, RS", "Santa Maria, RS")
    cities = ("Pelotas", )

    #places = ("Escritórios de contabilidade", "Escritórios administrativos", "Escritórios de arquitetura",
    #"Escritórios de advogacia", "clinicas odontológicas", "Clinicas psicológicas", "Coworking",
    #"Agências de publicidade", "Academias", "Pet shop")
    places = ("Academias", )

    places_ids = []
    for city in cities:
        vicinities = gplaces.get_vicinities(gplaces.get_pinpoints(city, radius=2000), city=city)

        for vicinity in vicinities:
            for place in places:
                places_ids.append(gplaces.get_places(place + ", " + vicinity, location=city, radius=2000)) #get the places ids. Also get the ids without specifiying a vicinity to compare.
    print(len(places_ids))
