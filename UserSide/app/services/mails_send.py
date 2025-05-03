import os

import jinja2
from fastapi.templating import Jinja2Templates

from services.mail_service.mail_send import MailSendingService, send_mails_to_user


class MailSend:
    @staticmethod
    def send_mails_to_50_for_buy_discount(to_email, username):
        body = f"""
        <!DOCTYPE html>
        <html>

          <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <div style="width: 100%; background-color: #f4f4f4; padding: 20px 0;">
              <div style="min-width: 300px; max-width: 500px; margin: 0 auto; background-color: #000000; border-radius: 10px; padding: 20px;">
                <!-- Logo -->
                <div style="text-align: center; padding-bottom: 20px;">
                  <img src="https://pubsfiles.s3.amazonaws.com/logo+GOLDnSIP.jpg" alt="Logo" style="width: 70px; height: 70px;">
                </div>
                <!-- Header -->
                <div style="color: #FF6600; padding: 20px;  font-size: 24px; font-weight: bold; padding-bottom: 10px;">
                  Hello, {username}!
                </div>
                <!-- Body -->
                <div style="padding: 10px 20px; color: #ffffff; font-size: 16px; line-height: 1.8;">
                  <p>
                    Ողջույն Ոսկե Օգտատեր😊🧡 <br>
                    Հիշում ես ,որ Դու այն Ոսկե 50-ից մեկն էիր?😌 <br>
                    Այժմ կարող ես օգտագործել Քո այդ առանձնահատկությունը  օգտվելով GoldnSip-ից զեղչով , 
                    Գնելով մեր առաջին փաթեթը 6000-ի փոխարեն ընդամենը 3900 դրամով🧡։ Զեղչից օգտվելու համար անհրաժեշտ է օգտագործել "goldnsip" պրոմո կոդը կայքում և Դու կստանաս հնարավորություն 31 օր շարունակ, ԱՄԵՆ ՕՐ, վայելելու երեկոներդ Անվճար։
                    Հրավիրիր ընկերներիդ, նրանք նույնպես կարող են օգտվել Քո պրոմո կոդից , քանի որ Դու բացառիկ Ոսկե 50-ից մեկն ես😊։ <br>
                    Ու հիշիր Դու արժանի ես 🧡
                  </p>

                  <p>
                   <span style="color: #FF6600;">Հ․Գ․</span>՝ Քանի որ Դուք օգտվել եք կայքի թեստային տարբերակից, մուտք գործելու համար խնդրում ենք նորից գրանցվել։ 
                  </p>

                  <p>Հարգանքներով , <a href="https://www.goldnsip.am" target="_blank"  style="text-decoration:none ; color:#FF6600;">GoldnSip</a></p>
                </div>
                <!-- Footer -->
                <div style="text-align: center; font-size: 12px; color: #777777; padding-top: 20px;">
                  © 2024 GoldnSip. All rights reserved.
                </div>
              </div>
            </div>
          </body>
        </html>
        """
        subject = "Քո Ոսկե Ընկերը🧡"

        MailSendingService.send_email(subject, body, to_email)

    @staticmethod
    def send_user_email_verify(to_email, username: str):
        verify_url = f"https://www.goldnsip.am/api/auth/verify-user/{to_email}"

        body = f"""
        <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>

    <body style="font-family: Arial, sans-serif; background-color: #ffffff ; margin: 0; padding: 0;">
        <div style="width: 100%; min-width: 320px; max-width: 500px; margin: 0 auto; background-color: #060606; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <div style="text-align: center; padding: 10px 0;">
                <img src="https://pubsfiles.s3.amazonaws.com/logo+GOLDnSIP.jpg" alt="Company Logo" style="width: 70px;">
            </div>
            <div style="padding: 20px;">
                <h2 style="color: #E45600; font-size: 24px;">Hello, {username}!</h2>
                <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Thank you for signing up for our service. We are excited to have you on our board. To get started, please verify your email address by clicking the button below.</p>
                <a href="{verify_url}" style="display: inline-block; padding: 10px 20px; margin: 5px 0 15px; font-family: revert; font-weight: 600; color: #060606; background-color: #E45600; text-decoration: none; border-radius: 5px;">Verify Email</a>
                <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px">If you did not sign up for this account, please ignore this email or contact support if you have any questions.</p>
                <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px">Best regards ,<span style="color: #E45600;"> GoldnSip </span></p>
            </div>
            <div style="text-align: center; padding: 20px 0 10px; font-size: 10px; color: #999999;">
                <p style="margin-bottom: 0;">&copy; 2024 GoldnSip. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
        """

        subject = "Confirm Registration"
        MailSendingService.send_email(subject, body, to_email)

    @staticmethod
    def send_forgot_password_code_email(to_email: str, code: int):
        body = f"""
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GoldnSip - Forgot Password</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #060606; margin: 0; padding: 0;">
    <div style="background-color: #060606; padding: 20px; margin:0 auto;  border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); min-width:320px; max-width: 420px; width: 100%; max-height: 500px;">
        <div style="text-align: center; padding: 10px 0;">
                <img src="https://pubsfiles.s3.amazonaws.com/logo+GOLDnSIP.jpg" alt="Company Logo" style="width: 70px;">
        </div>
            
        <h1 style="font-size:24px; color: #E45600;">Hi!</h1>
        <h3 style="font-size:14px; color: #f6f6f6;">You requested to reset your GoldnSip password. Use the code below to complete the process:</h3>
        <h2 style="font-size:18px; margin: 40px 0; color: #f6f6f6;">Your Reset Code: {code}</h2>
        <h3 style="font-size:14px; color: #f6f6f6;">Please enter this code on the password reset page of our website to set a new password.</h3>
        <h3 style="font-size:14px; color: #f6f6f6;">If you didn't request this, please ignore this email.</h3>
        <h4 style="font-size:14px; color: #f6f6f6;">Best regards, The GoldnSip Team &#129505;</h4>

        <span style="font-size:10px; text-align: center; color: #ccc; display: block; margin-top: 20px;">&#169; 2024  GoldnSip  All rights reserved.</span>
    </div>
</body>
</html>
        """
        subject = "Confirm Email"

        MailSendingService.send_email(subject, body, to_email)

    @staticmethod
    def send_mails_to_user50free(email: str, username: str):
        subject = "Քո Ոսկե Ընկերը🧡"
        body = f"""
                        <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    </head>

                    <body style="font-family: Arial, sans-serif; background-color: #ffffff ; margin: 0; padding: 0;">
                        <div style="width: 100%; min-width: 320px; max-width: 500px; margin: 0 auto; background-color: #060606; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                            <div style="text-align: center; padding: 10px 0;">
                                <img src="https://pubsfiles.s3.amazonaws.com/logo+GOLDnSIP.jpg" alt="Company Logo" style="width: 70px;">
                            </div>
                            <div style="padding: 20px;">
                                <h2 style="color: #E45600; font-size: 24px;">Ողջույն {username} 🧡</h2>
                                <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Շնորհավորում եմ Քեզ Իմ Ոսկե 50-ից 1-ը լինելու կապակցությամբ 😊</p>
                                <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Այժմ Դու ունես այն բացառիկ հնարավորությունը, որով կարող ես օգտվել մեր համակարգից Անվճար 😋</p>
                                <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Քեզ միայն անհրաժեշտ է վերիֆիկացնել Քո հաշիվը, եթե դեռ չես արել այն և վայելել երեկոներդ Անվճար 😌։</p>
                                <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Ստուգիր Քո Email հաշիվը կամ Spam-ը , ես քեզ ուղարկել եմ այն Քո գրանցվելուց հետո😄</p>
                                <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px;">Հրավիրիր ընկերներիդ նույնպես, միասին վայելեք, քանի որ Դուք Արժանի եք🙃</p>

                                <p style="color: #f6f6f6; line-height: 1.6; font-size: 14px">Սիրով , Քո Ոսկե Ընկեր GoldnSip🧡</p>
                            </div>
                            <div style="text-align: center; padding: 20px 0 10px; font-size: 10px; color: #999999;">
                            </div>
                        </div>
                    </body>
                    </html>
                        """
        send_mails_to_user(subject, body, email)

    @staticmethod
    def send_mail_to_all_signup_users(email):
        subject = "Քո Ոսկե Ընկերը🧡"
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
            <p>Ամեն օր ստացեք 1 անվճար ըմպելիք, 31 օր շարունակ, ընդամենը՝ 1900 դրամով 😊🧡</p>
            <p>GoldnSip-ի հատուկ առաջարկը դեռ հասանելի է մինչև դեկտեմբերի 31-ը ներառյալ 🥳</p>
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
        send_mails_to_user(subject, body, email)
