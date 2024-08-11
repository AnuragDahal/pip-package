from ...models import schemas
from ...core.database import user_collection
from ..exception import ErrorHandler
from ...utils.passhashutils import Encrypt
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
        