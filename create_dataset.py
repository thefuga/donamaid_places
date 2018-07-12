import os

def generate_dataset(places_list, dataset_name="dataset"):

    '''
    Generetes a CSV dataset with name, phone number and websiteself.

    :param places_list: the places found in a previous query.
    :type places_list: list of tuples.

    :param dataset_name: name to save the dataset.
    :type dataset_name: string
    '''
    dataset = open(dataset_name + ".csv", "w")
    dataset.write("nome,telefone,site\n")

    for place in places_list:
        string = place[0] + "," + place [1] + "," + place[2] + "\n"
        dataset.write(string)

    dataset.close()
