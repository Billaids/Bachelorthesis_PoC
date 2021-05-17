import time
import uuid

import pymongo
import yaml
from loguru import logger

from poc.helpers.helpers import Helpers
from poc.models.auth import UserModel

helpers = Helpers()
config = yaml.load(open("config.yaml"), Loader=yaml.FullLoader)

logger.info("PoC CLI-TOOL ")
logger.info("Bitte wählen Sie aus:")
logger.info("1 - Admin hinzufügen")
logger.info("2 - Nutzer hinzufügen")
logger.info("3 - Alle Nutzer anzeigen")
action = int(input("Action: "))

pym = pymongo.MongoClient(config["core"]["mongodb_url"])
db = pym[config["core"]["mongodb_db"]]

if action == 1:
    name = input("Name: ")
    email = input("E-Mail: ")
    password = helpers.hash_password(input("Passwort: "))
    token = uuid.uuid4().hex
    reg_time = time.time()
    user = UserModel(
        name=name,
        email=email,
        password=password,
        level=3,
        token=token,
        reg_time=reg_time,
    )

    db.users.insert_one(user.dict())
    logger.info(f"Dein Token lautet: {token}")
    logger.info("Fertig.")

elif action == 2:
    name = input("Name: ")
    email = input("E-Mail: ")
    password = helpers.hash_password(input("Passwort: "))
    token = uuid.uuid4().hex
    reg_time = time.time()
    user = UserModel(
        name=name,
        email=email,
        password=password,
        level=2,
        token=token,
        reg_time=reg_time,
    )

    db.users.insert_one(user.dict())
    logger.info(f"Dein Token lautet: {token}")
    logger.info("Fertig.")

elif action == 3:
    users = db.users.find()

    for user in users:
        user = helpers.load_model(UserModel, user)
        logger.info(" --- Name: " + user.name)
        logger.info(" - Email: " + user.email)
        logger.info(" - level: " + str(user.level))
        logger.info(" - Registrationsdatum: " + str(user.reg_time))
        logger.info(" - token: " + user.token)
