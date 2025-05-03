import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSendingService:
    @staticmethod
    def send_email(subject, body, to_email):
        from_email = "..."  # TODO
        from_password = "..."  # TODO

        # Create the email headers
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'html'))

        try:
            # Connect to the Gmail SMTP server and send the email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.close()

            print(f"Email to '{to_email}' successfully sent!")
        except Exception as e:
            print(f"Failed to send email: {e}")


# body = f"""
#                 <!DOCTYPE html>
#             <html>
#             <head>
#                 <meta charset="UTF-8">
#                 <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             </head>
#
#             <body style="font-family: Arial, sans-serif; background-color: #ffffff ; margin: 0; padding: 0;">
#                 <div style="width: 100%; min-width: 320px; max-width: 500px; margin: 0 auto; background-color: #060606; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
#                     <div style="text-align: center; padding: 10px 0;">
#                         <img src="https://pubsfiles.s3.amazonaws.com/logo+GOLDnSIP.jpg" alt="Company Logo" style="width: 70px;">
#                     </div>
#                     <div style="padding: 20px;">
#                         <h2 style="color: #E45600; font-size: 24px;">Ողջույն Samvel 🧡</h2>
#                         <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Շնորհավորում եմ Քեզ Իմ Ոսկե 50-ից 1-ը լինելու կապակցությամբ 😊</p>
#                         <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Այժմ Դու ունես այն բացառիկ հնարավորությունը, որով կարող ես օգտվել մեր համակարգից Անվճար 😋</p>
#                         <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Քեզ միայն անհրաժեշտ է վերիֆիկացնել Քո հաշիվը, եթե դեռ չես արել այն և վայելել երեկոներդ Անվճար 😌։</p>
#                         <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Ստուգիր Քո Email հաշիվը կամ Spam-ը , ես քեզ ուղարկել եմ այն Քո գրանցվելուց հետո😄</p>
#                         <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Հրավիրիր ընկերներիդ նույնպես, միասին վայելեք, քանի որ Դուք Արժանի եք🙃</p>
#
#                         <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px">Սիրով , Քո Ոսկե Ընկեր GoldnSip🧡</p>
#                     </div>
#                     <div style="text-align: center; padding: 20px 0 10px; font-size: 10px; color: #999999;">
#                     </div>
#                 </div>
#             </body>
#             </html>
#                 """
# <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px">Best regards ,<span style="color: #E45600;"> GoldnSip </span></p>
#  27 | Vard         | dashtoyan92@gmail.com
# 28 | Artur_000    | arturunique27@gmail.com
# body = """
# <!DOCTYPE html>
# <html>
#
#   <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
#     <div style="width: 100%; background-color: #f4f4f4; padding: 20px 0;">
#       <div style="min-width: 300px; max-width: 500px; margin: 0 auto; background-color: #000000; border-radius: 10px; padding: 20px;">
#         <!-- Logo -->
#         <div style="text-align: center; padding-bottom: 20px;">
#           <img src="https://pubsfiles.s3.amazonaws.com/logo+GOLDnSIP.jpg" alt="Logo" style="width: 70px; height: 70px;">
#         </div>
#         <!-- Header -->
#         <div style="color: #FF6600; padding: 20px;  font-size: 24px; font-weight: bold; padding-bottom: 10px;">
#           Hello, [Username]!
#         </div>
#         <!-- Body -->
#         <div style="padding: 10px 20px; color: #ffffff; font-size: 16px; line-height: 1.8;">
#           <p>
#             Ողջույն Ոսկե Օգտատեր😊🧡 <br>
#             Հիշում ես ,որ Դու այն Ոսկե 50-ից մեկն էիր?😌 <br>
#             Այժմ կարող ես օգտագործել Քո այդ առանձնահատկությունը  օգտվելով GoldnSip-ից զեղչով ,
#             Գնելով մեր առաջին փաթեթը 6000-ի փոխարեն ընդամենը 3900 դրամով🧡։ Զեղչից օգտվելու համար անհրաժեշտ է օգտագործել "goldnsip" պրոմո կոդը կայքում և Դու կստանաս հնարավորություն 31 օր շարունակ, ԱՄԵՆ ՕՐ, վայելելու երեկոներդ Անվճար։
#             Հրավիրիր ընկերներիդ, նրանք նույնպես կարող են օգտվել Քո պրոմո կոդից , քանի որ Դու բացառիկ Ոսկե 50-ից մեկն ես😊։ <br>
#             Ու հիշիր Դու արժանի ես 🧡
#           </p>
#
#           <p>
#            <span style="color: #FF6600;">Հ․Գ․</span>՝ Քանի որ Դուք օգտվել եք կայքի թեստային տարբերակից, մուտք գործելու համար խնդրում ենք նորից գրանցվել։
#           </p>
#
#           <p>Հարգանքներով , <a href="https://www.goldnsip.am" target="_blank"  style="text-decoration:none ; color:#FF6600;">GoldnSip</a></p>
#         </div>
#         <!-- Footer -->
#         <div style="text-align: center; font-size: 12px; color: #777777; padding-top: 20px;">
#           © 2024 GoldnSip. All rights reserved.
#         </div>
#       </div>
#     </div>
#   </body>
# </html>
# """



body = """
<!DOCTYPE html>
<html lang="hy">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GoldnSip Offer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 100%;
            max-width: 500px;
            margin: 0 auto;
            background-color: #060606;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            color: #f6f6f6;
        }
        .logo {
            text-align: center;
            padding: 10px 0;
        }
        .logo img {
            width: 70px;
        }
        .header {
            text-align: center;
            color: #E45600;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .content {
            font-size: 14px;
            line-height: 1.6;
        }
        .footer {
            text-align: center;
            font-size: 10px;
            color: #999999;
            margin-top: 20px;
        }
        .cta {
            text-align: center;
            margin: 20px 0;
        }
        .cta a {
            display: inline-block;
            padding: 10px 20px;
            color: #ffffff;
            background-color: #E45600;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
        .cta a:hover {
            background-color: #cc4500;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="https://pubsfiles.s3.amazonaws.com/logo+GOLDnSIP.jpg" alt="GoldnSip Logo">
        </div>
        <div class="header">
            Ողջույն 🧡
        </div>
        <div class="content">
            <p>Սիրով ցանկանում ենք տեղեկացնել, որ GoldnSip-ի հատուկ առաջարկը դեռ հասանելի է 😊🧡</p>
            <p>Ամենամսյա բաժանորդագրությունը **1900 դրամ** է՝ բացառիկ առաջարկ մինչև դեկտեմբերի 31-ը ներառյալ 🥳</p>
            <p>Բաց մի թողեք այս բացառիկ հնարավորությունը օգտվելու GoldnSip-ի առաջին փաթեթից</p>
            <p>Նվիրեք ինքներդ Ձեզ և Ձեր ընկերներին անմոռանալի երեկոներ:</p>
        </div>
        <div class="cta">
            <a href="https://www.goldnsip.am/log" target="_blank">Միացե՛ք հիմա</a>
        </div>
        <div class="footer">
            GoldnSip-ը գնահատում է Ձեր վստահությունը 🧡
        </div>
    </div>
</body>
</html>
"""

# subject = "Քո Ոսկե Ընկերը🧡"
# to_emails = ['samvel.arakelyan00@gmail.com', 'samvel.arakelyan00@gmail.com', 'samvel.arakelyan00@gmail.com']
# to_emails = 'samvel.arakelyan00@gmail.com'
# to_emails = "vahesmbatyan5@gmail.com"
#
def send_mails_to_user(subject_, body_, email_):
    try:
        MailSendingService.send_email(subject_, body_, email_)
    except Exception as err:
        print(err)
    time.sleep(1)

#
# send_mails_to_user(subject, body, to_emails)
# send_mails_to_all_users(subject=subject, body=body, emails_list=to_emails)
