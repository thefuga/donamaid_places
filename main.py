import create_dataset
import Places


if __name__ == "__main__":
    
    gplaces = Places.Places("AIzaSyBgZPQc5CswWQD63YSIiXO_AcS-g4wp-n4")
    #cities = ("Londrina, PR", "Maringa, PR", "Caxias, RS", "Pelotas, RS", "Rio Grande, RS", "Santa Maria, RS")
    cities = ("Maringá, PR", )
    ddds = {"Londrina, PR": "(43)",
            "Maringá, PR": "(44)",
            "Caxias, RS": "(54)",
            "Pelotas, RS": "(53)",
            "Rio Grande, RS": "(53)",
            "Santa Maria, RS": "(55)"}
    
    places = ("Escritorios de contabilidade", "Escritorios administrativos", "Escritorios de arquitetura",
    "Escritorios de advogacia", "clinicas odontologicas", "Clinicas psicologicas", "Coworking",
    "Agencias de publicidade", "Academias", "Pet shop")
    #places = ("Academias", )

    for city in cities:
        print("Looking for places in " + city + "...")
        vicinities = gplaces.get_vicinities(gplaces.get_pinpoints(city, radius=2000), location=city)

        for place in places:
            print("...Looking for " + place + "...")
            places_full = []
            for vicinity in vicinities:
                print("...In " + vicinity)
                places_full += [x for x in gplaces.get_places(place + ", " + vicinity, location=city, radius=2000)]

            places_full = set(places_full)
            infos = gplaces.get_place_info(places_full)

            outsiders = []
            print("...Refining results...")
            for info in infos:
                if ddds[city] not in info[1]:
                    outsiders.append(info)

            places_full = [x for x in infos if x not in outsiders]
            create_dataset.generate_dataset(places_full, place + " em " + city)
            print("All done for this place!")
        print("All done for this city!")
    print("All done!")