class DataAccessConstants:
    class MongoDB:
        class CollectionNames:
            JOB = "job"
            CORPORATES = "corporates"

    class GlassDollar:
        EXCLUDED_FIELDS = ["id", "_id", "created_at", "job_id"]
