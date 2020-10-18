import mongoengine

class Jobs(mongoengine.Document):
    term = mongoengine.StringField()
    jobTitle = mongoengine.StringField()
    jobCompany = mongoengine.StringField()
    jobLocation = mongoengine.StringField()
    jobDesc = mongoengine.StringField()


class UniqueJobs(mongoengine.Document):
    term = mongoengine.StringField()
    jobTitle = mongoengine.StringField()
    jobCompany = mongoengine.StringField()
    jobLocation = mongoengine.StringField()
    jobDesc = mongoengine.StringField(unique=True)
