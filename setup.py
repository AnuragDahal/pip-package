from setuptools import setup, find_packages

setup(
    name='fastapi-mongo',
    version='0.1.1',
    long_description='This is a simple package that helps you to create a FastAPI project with MongoDB it comes with default crud operations and database setup just configure your environment variables and you are good to go.',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    data_files=[
        ('config',
         ['fastapi-mongo/config/dependencies.py', 'fastapi-mongo/config/__init__.py']),
        ('core', ['fastapi-mongo/core/database.py',
         'fastapi-mongo/core/__init__.py']),
        ('handlers', ['fastapi-mongo/handlers/authhandler.py', 'fastapi-mongo/handlers/exception.py',
         'fastapi-mongo/handlers/__init__.py', 'fastapi-mongo/handlers/userhandler.py']),
        ('', ['fastapi-mongo/main.py', "fastapi-mongo/.env.sample",
         'fastapi-mongo/Readme.md', 'fastapi-mongo/requirements.txt']),
        ('models', ['fastapi-mongo/models/__init__.py',
         'fastapi-mongo/models/models.py', 'fastapi-mongo/models/schemas.py']),
        ('routers',
         ['fastapi-mongo/routers/auth.py', 'fastapi-mongo/routers/user.py']),
        ('utils', ['fastapi-mongo/utils/envutils.py',
         'fastapi-mongo/utils/jwtutil.py', 'fastapi-mongo/utils/passhashutils.py', 'fastapi-mongo/utils/__init__.py'])

    ],
    include_package_data=True,
    install_requires=["fastapi", "pymongo",
                      "python-dotenv", "uvicorn", "passlib", "python-jose", "python-multipart"]
)
