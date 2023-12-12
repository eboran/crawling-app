from os import environ as env


class AppConfig:
    NAME = env.get("APP_NAME", "Crawling App")
    LOG_LEVEL = env.get("LOG_LEVEL", "info").upper()
    BROKER_URL = env.get("BROKER_URL", "pyamqp://guest:guest@rabbitmq:5672//")

