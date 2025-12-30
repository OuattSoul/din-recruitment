from django.db import models

class JobOffer(models.Model):
    image = models.ImageField(upload_to='job_images/', blank=True, null=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contract_type = models.CharField(
        max_length=50,
        choices=[
            ('cdi','CDI'),
            ('cdd','CDD'),
            ('stage','Stage'),
            ('alternance','Alternance'),
            ('interim','Intérim'),
            ('freelance','Freelance'),
            ('temps_partiel','Temps partiel'),
        ]
    )
    salary = models.CharField(max_length=50, blank=True, null=True)
    deadline = models.DateField()
    description = models.TextField()
    skills = models.JSONField()  # ou ArrayField si PostgreSQL

    def __str__(self):
        return self.title
