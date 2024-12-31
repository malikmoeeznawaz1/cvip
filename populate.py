import os
import json
import django
from django.conf import settings

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InvoiceProject.settings')  # Replace 'your_project' with your project name
django.setup()

# Import models after initializing Django
from App.models import Image, Category, Annotation  # Replace 'App' with the actual app name

# Function to populate the database
def populate_database():
    folder_path = "C:/Users/MalikMoeezNawaz/Desktop/output"
    files = sorted(os.listdir(folder_path))[:20]  # Only process the first 20 files

    for file in files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as f:
            data = json.load(f)

             

            # Save Categories with modified name from JSON file
            for cat in data.get("categories", []):
                # Extract the base name of the JSON file (excluding extension) and add .png
                base_name = os.path.splitext(file)[0] 
                Category.objects.get_or_create(
                    id=cat["id"], 
                    defaults={"name": base_name}  # Use the modified file name
                )

            # Save Annotations
            for ann in data.get("annotations", []):
                Annotation.objects.create(
                    image_id=ann["image_id"],
                    category_id=ann["category_id"],
                    bbox=ann["bbox"],
                    area=ann["area"],
                    iscrowd=ann["iscrowd"]
                )

    print("Processed and saved data from 20 files.")

if __name__ == "__main__":
    populate_database()







# import django
# import os
# from django.conf import settings

# # Initialize Django settings
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InvoiceProject.settings')  # Replace 'InvoiceProject' with your project name
# django.setup()

# # Import models after initializing Django
# from App.models import Category  # Replace 'App' with the actual app name

# # List of categories
# categories = [
#     "Date_label", "Date_val", "Business_Name_label", "Business_Name_Val", 
#     "Seller_Name_Label", "Seller_Name_val", "Seller_Address_Label", "Seller_Address_val", 
#     "Seller_S.T.Reg_no_label", "Seller_S.T.Reg_no_val", "Seller_NTN_label", "Seller_NTN_val", 
#     "Buyer_Name_Label", "Buyer_Name_val", "Buyer_Address_Label", "Buyer_Address_val", 
#     "Buyer_S.T.Reg_no_label", "Buyer_S.T.Reg_no_val", "Buyer_NTN_label", "Buyer_NTN_val", 
#     "Product_Names_label", "Product_1name_val", "Product_2name_val", "Product_3name_val", "Product_4name_val", 
#     "Prod_Quantity_label", "Quantity_prod1_val", "Quantity_prod2_val", "Quantity_prod3_val", "Quantity_prod4_val", 
#     "Prod_Rate_label", "Rate_prod1_val", "Rate_prod2_val", "Rate_prod3_val", "Rate_prod4_val", 
#     "Prod_Amount_EXCL_label", "prod1_amount_excl_val", "prod2_amount_excl_val", "prod3_amount_excl_val", "prod4_amount_excl_val", 
#     "Prod_Amount_INCL_label", "prod1_amount_INC_val", "prod2_amount_INC_val", "prod3_amount_INC_val", "prod4_amount_INC_val", 
#     "prod_total_label", "prod_total_EXC_val", "prod_total_INC_val"
# ]

# # Function to populate the Category table
# def populate_categories():
#     for category_name in categories:
#         # Save each category to the Category table
#         Category.objects.get_or_create(name=category_name)

#     print(f"Processed and saved {len(categories)} category entries.")

# # Call the function to populate the database
# if __name__ == "__main__":
#     populate_categories()
