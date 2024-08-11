from ...models import schemas
from fastapi import Response
from ...core.database import user_collection
from ..exception import ErrorHandler
from ...utils.passhashutils import Encrypt
from ...core.database import post_collection, comments_collection
from ...utils.passhashutils import Encrypt
from ..Auth.authhandler import Validate


class UserManager:
    @staticmethod
    async def HandleNewUserCreation(request: schemas.UserDetails):
        """
        Insert a new user record.
        A unique `id` will be created and provided in the response.
        """
        duplicate_user = await Validate.verify_email(request.email)
        if not duplicate_user:
            hashed_password = Encrypt.hash_password(request.password)
            # Add the image to the server and set the url in the db
            user_data = {
                **request.model_dump(exclude={"password"}), "password": hashed_password, "isEmailVerified": False}
            # Add the img url to the user's db
            new_user = await user_collection.insert_one(user_data)
            return {"id": str(new_user.inserted_id)}
        return ErrorHandler.ALreadyExists("User already exists")

    @staticmethod
    async def HandleReadingUserRecords():
        """
        Retrieve all user records.
        """
        count = await user_collection.count_documents({})
        if count > 0:
            # this is a asynchronous cursor so we need to iterate over it using async for loop
            AsyncIOMotorCursor = user_collection.find()
            users = []
            async for user in AsyncIOMotorCursor:
                users.append(user)
            return users
        else:
            raise ErrorHandler.NotFound("No user found")

    @staticmethod
    async def HandleUserDeletion(user_email: str, password: str, res: Response):
        """
        Delete a user
        """
        # Check the password is correct
        user_details = await user_collection.find_one({"email": user_email})
        if not Encrypt.verify_password(password, user_details["password"]):
            return ErrorHandler.Unauthorized("Incorrect Password")

        # Delete the user through the email
        deleted_user = await user_collection.delete_one({"email": user_email})
        if deleted_user.deleted_count == 0:
            return ErrorHandler.NotFound("User not found")
        # Delete all the data sets associated with the user such as posts, comments, etc.
        await comments_collection.delete_many({"commented_by": user_email})
        await post_collection.delete_many({"posted_by": user_email})
        res.delete_cookie('token')
        return {"message": "User deleted successfully"}
