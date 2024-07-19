from setuptools import setup, find_packages

setup(
    name='fastapi-mongo',
    version='0.0.6',
    long_description='This is a simple package that helps you to create a FastAPI project with MongoDB it comes with default crud operations and database setup just configure your environment variables and you are good to go.',
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
        ('', ['package/folder_structure.json']),
    ],
    include_package_data=True,
    install_requires=["fastapi", "pymongo", "python-dotenv",
                      "uvicorn", "passlib", "python-jose", "python-multipart", 'setuptools',],
    entry_points={
        'console_scripts': [
            'build=package.build_structure:create_files_and_dirs_from_json',
        ],
    },
)
