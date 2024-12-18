# script to populate database Products, Properties and ProductImages tables 
# using (modified) Cereal.csv dataset and folder /Cereal Pictures, found in folder /script_input

# NOTE: should be ran on a fresh database, otherwise there might arise issues with auto-incrementing IDs

import os
import csv

from database import Database

cereal_path = os.path.join("script_input", "Cereal.csv")
images_path = os.path.join("script_input", "Cereal Pictures")

# hardcoded copy of the headers cus this is already a specific script and I can't be bothered to make it reusable
header = ['ID', 'Type', 'Name', 'Price', 'Currency', 'Stock', 'Calories', 'Protein', 'Fat', 'Sodium', 'Fiber', 'Carbs', 'Sugars', 'Potassium', 'Vitamins', 'UnitWeight']
header_split = 6
products_header = header[1:header_split] # leave ID out
cereal_header = header[header_split:]


def main():
    # get connection to db
    db = Database()

    ##### load cereal dataset
    with open(cereal_path, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=";")

        # pack items into dicts and pass to connection
        for row in reader:
            id = row[0]
            product_dict = dict(zip(products_header, row[1:header_split])) # leave ID out
            cereal_dict = dict(zip(cereal_header, row[header_split:]))

            db.create("Products", product_dict)

            for key, value in cereal_dict.items():
                data = {
                    "ProductID": id,
                    "Name":      key,
                    "Value":     value
                }
                db.create("Properties", data)
            
    ##### load image paths from folder
    img_files = [f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))]

    for f in img_files:
        # pack into dicts: get id of product that matches image filename
        f_no_extension = f[:-4]
        product = db.find_by_params("Products", {"Name": f_no_extension})

        if not product: # skip if we couldnt find the id (shouldnt happen since ive corrected cereal.csv and the picture filenames)
            f"couldnt find id for {f}"
            continue

        product_id = product[0][0]

        # send to connection
        data = {
            "ProductID": str(product_id),
            "Path": f
        }
        db.create("ProductImages", data)

    ##### add some random users
    data = [
        {"FirstName": "Cereza", "LastName": "Morpheus"},
        {"FirstName": "Jeanne", "LastName": "Orpheus"},
        {"FirstName": "Cheshire", "LastName": "Walrus"}
    ]

    for guy in data:
        db.create("Customers", guy)

    return


if __name__ == "__main__":
    main()