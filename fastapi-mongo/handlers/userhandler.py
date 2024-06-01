from models import schemas
from fastapi import Request, Depends, Response
from core.database import user_collection
from handlers.exception import ErrorHandler
from pymongo import ReturnDocument
from config.dependencies import verify_token

# from utils.passhashutils import Encryptor


class Validate:
    @staticmethod
    def verify_email(email: str):
        check_email = user_collection.find_one({"email": email})
        if check_email:
            return email
        raise ErrorHandler.NotFound("Email not found")


class UserManager:
    @staticmethod
    def create(request: schemas.User):
        """
        Insert a new user record.
        A unique `id` will be created and provided in the response.
        """
        duplicate_user = user_collection.find_one({"email": request.email})
        if not duplicate_user:
            # Import Encryptor only when it's needed
            from utils.passhashutils import Encryptor
            hashed_password = Encryptor.hash_password(request.password)
            new_user = user_collection.insert_one(
                {**request.model_dump(exclude={"password"}), "password": hashed_password})
            return {"id": str(new_user.inserted_id)}
        return ErrorHandler.ALreadyExists("User already exists")

    @staticmethod
    def read():
        """
        Retrieve all user records.
        """
        count = user_collection.count_documents({})
        if count > 0:
            users = user_collection.find()
            return users
        else:
            raise ErrorHandler.NotFound("No user found")

    @staticmethod
    async def update(old_email: str, request: Request, new_email: schemas.UpdateUserEmail):
        """"""
        # Get the user email from the cookie
        logged_in_user_email = await verify_token(request)
        print(logged_in_user_email)
        print(old_email)
        # Check email from the cookie and the email to be updated are same
        if old_email != logged_in_user_email:
            raise ErrorHandler.Forbidden(
                "You are not authotrized to perform this action")
            # check if the new email entered is available or not
        is_available = user_collection.find_one({"email": new_email.email})
        if not is_available:
            user = user_collection.find_one_and_update(
                {"email": logged_in_user_email},
                {"$set": {"email": new_email.email}},
                return_document=ReturnDocument.AFTER
            )
            if user is None:
                raise ErrorHandler.NotFound("User not found")
            return user
        else:
            return ErrorHandler.Error("Bad request")

    @staticmethod
    async def delete(request: Request, res: Response):
        """
        Delete a user
        """
        # Get the user email from the cookie
        user_email = await verify_token(request)
        # Delete the user through the email
        deleted_user = user_collection.delete_one({"email": user_email})
        res.delete_cookie('token')
        if deleted_user.deleted_count == 0:
            raise ErrorHandler.NotFound("User not found")
        return {"message": "User deleted successfully"}
