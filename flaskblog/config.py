import json


with open("/etc/flask_config.json") as config_file:
    config = json.load(config_file)


class Config:
    SECRET_KEY = config["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = config["SQLALCHEMY_DATABASE_URI"]
    # MONGO_URI = config["MONGO_URI"]
    MAIL_SERVER = config["EMAIL_SERVER"]
    MAIL_PORT = config["EMAIL_PORT"]
    MAIL_USE_TLS = config["EMAIL_USE_TLS"]
    MAIL_USERNAME = config["EMAIL_USER"]  # os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = config["EMAIL_PASS"]
