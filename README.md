edit in config.py 


import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-development-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@127.0.0.1:3306/mingalaraid"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")


on line 12,

change password to your own password that you use for MySql Workbench

create database using data in schema.sql  in mysql,

the program should run successfully

normally this is not a problem since people usually use root for password in mysql but I use something else :)
