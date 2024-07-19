import smtplib
from fastapi import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ...utils.envutils import Environment
import random
from jose import jwt, JWTError
from ...core.database import otp_collection, user_collection
from ...handlers.exception import ErrorHandler
from datetime import datetime, timezone
env = Environment()

'''
The @staticmethod decorator is used to declare a method as a static method, which means it belongs to the class and not the instance of the class. It can be called on the class itself, rather than on an instance of the class.'''


class EmailHandler:
    '''
    This class is responsible for handling the email verification process.'''
    @staticmethod
    def generate_email_verification_otp():
        # Generate a random 6-digit number
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_email_to(recipient: str, htmlContent: str, subject: str):
        # Define your Gmail username and password
        gmail_user = env.GMAIL_USER
        gmail_password = env.APP_SPECIFIC_PASS

        # Create a MIMEMultipart object
        msg = MIMEMultipart('alternative')
        html = f'''{htmlContent}'''
        # Add the HTML content to the MIMEMultipart object
        msg.attach(MIMEText(html, 'html'))
        msg['Subject'] = subject
        msg['From'] = "mailer@connectify.com"
        msg['To'] = recipient

        # Connect to the Gmail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to your Gmail account
        server.login(gmail_user, gmail_password)

        # Send the email
        try:
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def VerifyOtp(otp, user_otp):
        if otp == user_otp:
            return True
        return False

    @staticmethod
    async def HandleEmailVerification(recipient: str, user_email: str, flag: str):
        try:
            if recipient != user_email:
                return ErrorHandler.Unauthorized("Invalid Email Address")
            otp = EmailHandler.generate_email_verification_otp()
            htmlContent = f"""
                    <html>
                    <body>
                        <p>Dear User,</p>

                        <p>We recently received a request for a new login or signup associated with this email address. If you initiated this request, please enter the following verification code to confirm your identity:</p>

                        <p><b>Verification Code: {otp}</b></p>

                        <p>If you did not initiate this request, please disregard this email and no changes will be made to your account.</p>

                        <p>Thank you,<br>
                        The Connectify Team</p>
                    </body>
                    </html>
                    """
            sub = "Email Verification"
            isEmailSent = EmailHandler.send_email_to(
                recipient, htmlContent, sub)
            # Add the otp to the database
            await otp_collection.insert_one(
                {"email": recipient, "otp": otp, f"{flag}": True, "expires_on": datetime.now(timezone.utc)})
            if isEmailSent:
                return "Email sent Successfully"
            else:
                return ErrorHandler.Error("Invalid Email Address or Email not sent successfully")
        except Exception as e:
            return str(e)

    @staticmethod
    async def HandleOtpVerification(user_otp: str, user_email: str, flag: str):
        # Attempt to retrieve the OTP document for the user
        email_doc = await otp_collection.find_one({"email": user_email})
        if email_doc is None:
            return ErrorHandler.Error("Invalid Email or OTP not found in the database")
        # Verify the OTP and the flag
        otp_in_db = email_doc["otp"]
        isOtpVerified = EmailHandler.VerifyOtp(user_otp, otp_in_db)
        if not isOtpVerified or not email_doc.get(flag, False):
            return ErrorHandler.Unauthorized("Email Verification Failed, incorrect OTP")

        # Ensure the user exists
        isUser = await user_collection.find_one({"email": user_email})
        if not isUser:
            return ErrorHandler.NotFound("User not found in the database")

        # Update the user's email verification status and delete the OTP
        await user_collection.update_one({"email": user_email}, {"$set": {"isEmailVerified": True}})
        await otp_collection.find_one_and_delete({"email": user_email})
        return "Email Verified Successfully"
