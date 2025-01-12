from django.db import models

# # Feedback Model
# class Feedback(models.Model):
#     first_name_feed_supp = models.CharField(max_length=100)
#     last_name_feed_supp = models.CharField(max_length=100)
#     email_feed_supp = models.EmailField()
#     contact_number_feed_supp = models.CharField(max_length=15)
#     subject_line = models.CharField(max_length=255)
#     details_feed_supp = models.TextField()

#     def __str__(self):
#         return f"Feedback from {self.first_name_feed_supp} {self.last_name_feed_supp}"

# # Email Support Model
# class EmailSupport(models.Model):
#     first_name_feed_supp = models.CharField(max_length=100)
#     last_name_feed_supp = models.CharField(max_length=100)
#     email_feed_supp = models.EmailField()
#     contact_number_feed_supp = models.CharField(max_length=15)
#     subject_line = models.CharField(max_length=255)
#     details_feed_supp = models.TextField()

#     def __str__(self):
#         return f"Email Support from {self.first_name_feed_supp} {self.last_name_feed_supp}"

# class UserProfile(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     age = models.IntegerField()

#     def __str__(self):
#         return self.name


from pymongo import MongoClient
def get_db():
    """
    Establishes and returns a connection to the MongoDB database.
    """
    try:
        connection_string = "mongodb://localhost:27017/"
        client = MongoClient(connection_string)
        db = client["carainsurify"]
        return db
    except Exception as e:
        raise Exception(f"Failed to connect to MongoDB: {str(e)}")







