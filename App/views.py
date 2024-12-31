from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from ultralytics import YOLO
import pytesseract
import cv2
import os

# Label mapping for tensor values
label_mapping = {
    0: "Date_label",
    1: "Date_val",
    2: "Business_Name_label",
    3: "Business_Name_Val",
    4: "Seller_Name_Label",
    5: "Seller_Name_val",
    6: "Seller_Address_Label",
    7: "Seller_Address_val",
    8: "Seller_S.T.Reg_no_label",
    9: "Seller_S.T.Reg_no_val",
    10: "Seller_NTN_label",
    11: "Seller_NTN_val",
    12: "Buyer_Name_Label",
    13: "Buyer_Name_val",
    14: "Buyer_Address_Label",
    15: "Buyer_Address_val",
    16: "Buyer_S.T.Reg_no_label",
    17: "Buyer_S.T.Reg_no_val",
    18: "Buyer_NTN_label",
    19: "Buyer_NTN_val",
    20: "Product_Names_label",
    21: "Product_1name_val",
    22: "Product_2name_val",
    23: "Product_3name_val",
    24: "Product_4name_val",
    25: "Prod_Quantity_label",
    26: "Quantity_prod1_val",
    27: "Quantity_prod2_val",
    28: "Quantity_prod3_val",
    29: "Quantity_prod4_val",
    30: "Prod_Rate_label",
    31: "Rate_prod1_val",
    32: "Rate_prod2_val",
    33: "Rate_prod3_val",
    34: "Rate_prod4_val",
    35: "Prod_Amount_EXCL_label",
    36: "prod1_amount_excl_val",
    37: "prod2_amount_excl_val",
    38: "prod3_amount_excl_val",
    39: "prod4_amount_excl_val",
    40: "Prod_Amount_INCL_label",
    41: "prod1_amount_INC_val",
    42: "prod2_amount_INC_val",
    43: "prod3_amount_INC_val",
    44: "prod4_amount_INC_val",
    45: "prod_total_label",
    46: "prod_total_EXC_val",
    47: "prod_total_INC_val"
}


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
model = YOLO(r'C:\Users\MalikMoeezNawaz\Downloads\yolov8_best_model\yolov8_best_model.pt')  # Replace with your trained YOLO model path


def home(request):
    return render(request, 'firstApp/home.html')


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('image')
        if uploaded_file:
            # Save the uploaded file temporarily
            temp_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(temp_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            try:
                # Process the image
                image = cv2.imread(temp_path)
                results = model.predict(temp_path, conf=0.26)
                extracted_data = []

                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cropped_region = image[y1:y2, x1:x2]
                        text = pytesseract.image_to_string(cropped_region).strip()
                        label = int(box.cls.item())  # Convert the tensor value to an integer
                        
                        # Add the corresponding label name using the label_mapping dictionary
                        label_name = label_mapping.get(label, "Unknown")
                        
                        extracted_data.append({
                            'label': label_name,
                            'text': text,
                            'coords': (x1, y1, x2, y2),
                        })
                        # Annotate image
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Sort extracted data by label
                extracted_data.sort(key=lambda x: label_mapping.get(x['label'], ''))

                # Save the annotated image
                annotated_image_path = os.path.join(settings.MEDIA_ROOT, 'annotated_' + uploaded_file.name)
                cv2.imwrite(annotated_image_path, image)

                # Construct annotated image URL
                annotated_image_url = settings.MEDIA_URL + 'annotated_' + uploaded_file.name
                # Render the response
                return render(request, 'firstApp/upload.html', {
                    'data': extracted_data,
                    'annotated_image_url': annotated_image_url,
                })
            finally:
                # Remove the temporary file if it exists
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    return render(request, 'firstApp/upload.html')




from django.shortcuts import render
from .models import Image, Category, Annotation

def show_data(request):
    # Retrieve all records from the database
    images = Image.objects.all()
    categories = Category.objects.all()
    annotations = Annotation.objects.all()

    # Pass data to template
    return render(request, 'firstApp/show_data.html', {
        'images': images,
        'categories': categories,
        'annotations': annotations
    })
