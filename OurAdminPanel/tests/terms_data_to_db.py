"""
TODO Terms of Use [8 - 11] in English not in Russian
"8. TERMINATION :-> qrmenuarmenia.site has the right to terminate or suspend your account (if applicable) and access to the platform at our discretion, without prior notice and for any reason, including violation of these Terms of Use. Upon termination, your right to use qrmenuarmenia.site will be immediately revoked.",
"9. LIMITATION OF LIABILITY :-> qrmenuarmenia.site shall not be liable for any indirect, incidental, special, consequential, or punitive damages, or any loss of profits or revenues, whether incurred directly or indirectly, or any loss of data, use, goodwill, or other intangible losses, resulting from (i) your use or inability to use the platform; (ii) any unauthorized access to or use of our servers and/or any personal information stored therein.",
"10. CHANGES TO TERMS :-> qrmenuarmenia.site reserves the right to modify these Terms of Use at any time. We will notify you of any changes by posting the new Terms of Use on the platform. You are advised to review these Terms of Use periodically for any changes. Changes to these Terms of Use are effective when they are posted on this page.",
"11. CONTACT US :-> If you have any questions about these Terms of Use, please contact us at by email itcompany.ys@gmail.com."

TODO in Armenian section Terms of Use not in [6 - 11] sections, has presection, but English and Russian not have that

TODO ԳՐԱՆՑՈՒՄ ԵՒ ՀԱՇԻՎՆԵՐ in Russian translation writen РЕГИСТРАЦИЯ И УЧЕТНЫЕ ЗАПИСИ (Հաշիվներ ֊ УЧЕТНЫЕ ЗАПИСИ ? Wrong)
"""


import json
import requests


terms_list = []

# Read JSON file
with open('terms_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# print(data.get("privacy_policy_en"))
# print(data.get("privacy_policy_ru"))
# print(data.get("privacy_policy_am"))

for term in data:
    terms_list.append(data[term])


# API endpoint
url = "http://127.0.0.1:8888/api/termsCRUD/add-term"

# Your Bearer token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDg1OTU1NzIsImFkbWluIjp7ImlkIjoxLCJuYW1lIjoiU2FtdmVsIiwiZW1haWwiOiJzYW12ZWwuYXJha2VseWFuMDBAZ21haWwuY29tIn19.-_y9Z5yJCsBF4HXZ3Y4sJuoOJsf6aNlPCqVWgl6xU3k"

# Headers with authorization
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send POST request

for term in terms_list:
    response = requests.post(url, headers=headers, json=term)

    # Print the response
    print("Status Code:", response.status_code)
