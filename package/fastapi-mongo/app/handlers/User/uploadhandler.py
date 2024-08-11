from ...config.cloudinary_config import uploadImage
from ...core.database import user_collection
from pymongo import ReturnDocument
from ..Auth.authhandler import Validate
from ..exception import ErrorHandler
from fastapi import UploadFile


class UploadManager:
    @staticmethod
    async def HandleUploadProfilePic(user_email: str, img: UploadFile):
        """
        Upload the user profile picture.
        """
        # Check the user in db
        try:
            isUser = await Validate.verify_email(user_email)
            if not isUser:
                return ErrorHandler.NotFound("User not found")
            filename = img.filename.split(".")[0][:10]
            img_bytes = await img.read()
            # Upload the image and get its URL
            img_url = uploadImage(filename, img_bytes)
            # Save the image URL in the database
            user = await user_collection.find_one_and_update(
                {"email": user_email},
                {"$set": {"profile_picture": img_url}},
                # this will return the updated document
                return_document=ReturnDocument.AFTER
            )
            return {"profile_pic": user["profile_picture"]}
        except Exception as e:
            return ErrorHandler.Error(e)
