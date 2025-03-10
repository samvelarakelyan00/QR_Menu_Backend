import os
import time

import requests

from menudata import datalist


def add_menu_new(url: str, form_data: dict, file_path: str = "", token: str=""):
    # Open the image file
    with open(file_path, "rb") as image_file:
        files = {"image": image_file}

        # Set headers with Bearer token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Send POST request
        response = requests.post(url, data=form_data, files=files, headers=headers)

        # Handle response
        if response.status_code == 200:
            print("Menu item added:", response.json())
        else:
            print(f"Error: {response.status_code} - {response.text}")


# localhost url
url = "http://127.0.0.1:8080/api/menuCRUD/add-menu-new"

# localhost token
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDE2ODg3MjgsImNhZmVfYWRtaW4iOnsiaWQiOjEsIm5hbWUiOiJ0bWJsIEFybWVuIiwiZW1haWwiOiJ0bWJsQGdtYWlsLmNvbSIsImhvcmVrYWNsaWVudF9pZCI6MX19.5gpBnEZ876lw4p4DZ3dC-BUlxkqghyXTG-ZAicaFk88"

# aws test ec2 url
# url = "http://23.20.175.90/api/cafeadmin/api/menuCRUD/add-menu-new"
# aws test ec2 token
# auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDE2OTA2OTIsImNhZmVfYWRtaW4iOnsiaWQiOjEsIm5hbWUiOiJtZWxvZHlfYWRtaW4iLCJlbWFpbCI6Im1lbG9keUBnbWFpbC5jb20iLCJob3Jla2FjbGllbnRfaWQiOjF9fQ.OUxhvrgyU1Evfy0AoMM0C52hrMbqIXPN2B-0iHQEMeg"

image_directory = "../../../../images/"

for form_data in datalist:
    # Construct full image file path
    image_path = os.path.join(image_directory, form_data["image"])

    if not os.path.exists(image_path):
        print(f"Warning: Image file not found for {form_data['name']} at {image_path}")
        continue  # Skip if image does not exist

    add_menu_new(url, form_data, image_path, auth_token)
    time.sleep(1)  # Avoid overwhelming the server
