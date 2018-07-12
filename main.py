import create_dataset
import seek_places

if __name__ == "__main__":
    key = "AIzaSyBgZPQc5CswWQD63YSIiXO_AcS-g4wp-n4"

    cities = ("Londrina, PR", "Maringa, PR", "Caxias, RS", "Pelotas, RS", "Rio Grande, RS", "Santa Maria, RS")

    places = ("Escritórios de contabilidade", "Escritórios administrativos", "Escritórios de arquitetura",
    "Escritórios de advogacia", "clinicas odontológicas", "Clinicas psicológicas", "Coworking",
    "Agências de publicidade", "Academias", "Pet shop")

    for city in cities:
        for place in places:
            create_dataset.generate_dataset(seek_places.get_place_info(key, seek_places.get_places(key, place, location=city, radius=20000)), place + " em " + city)
