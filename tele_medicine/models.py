from django.db import models

class CustomUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=255)  # Store hashed passwords only!
    
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'telehealth_users'


class MedicalCenter(models.Model):
    # Map Django field names to actual database column names
    unique_id = models.IntegerField(primary_key=True, db_column='unique_id')
    name = models.CharField(max_length=255, db_column='center_name')
    center_type = models.CharField(max_length=50, db_column='center_type')
    latitude = models.FloatField(db_column='latitude')
    longitude = models.FloatField(db_column='longitude')
    #address = models.TextField(db_column='address', null=True, blank=True)

    class Meta:
        db_table = 'medical_centers'
        managed = False  # Tell Django this table already exists

    def __str__(self):
        return self.name
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"