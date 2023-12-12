from os import environ as env


class DataAccessConfig:
    class MongoDB:
        CONNECTION_STRING = env.get("MONGO_CONNECTION_STRING", "mongodb://mongodb:27017")
        DB_NAME = env.get("MONGO_DB_NAME", "glassdollar")

    class GlassDollar:
        URI = env.get('GLASSDOLLAR_URI', "https://ranking.glassdollar.com/graphql")

