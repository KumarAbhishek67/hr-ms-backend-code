from django.db import models
from django.contrib.auth.models import AbstractUser

class HR(AbstractUser):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    email = models.CharField(max_length=200, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    username=None
    # username = models.CharField(max_length=255, unique=True)
    
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, default='Female', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    IsDeleted = models.BooleanField(default=False)
   
    def __str__(self):
        return self.email
    
class DomainInterest(models.Model):
    domain_name = models.CharField(max_length=255, unique=True)
    ModifiedByUserid = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name="modified_domains")
    ModifyDateTime = models.DateTimeField(auto_now=True)
    DeletedByUserid = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name="deleted_domains", blank=True)
    DeletedDateTime = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.domain_name
    
class Qualification(models.Model):
    qualification_name = models.CharField(max_length=255, unique=True)
    qualification_desc = models.TextField(blank=True, null=True)
    ModifiedByUserid = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name="modified_qualification")
    ModifyDateTime = models.DateTimeField(auto_now=True)
    DeletedByUserid = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name="deleted_qualification", blank=True)
    DeletedDateTime = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.qualification_name

    
class Candidate(models.Model):
    EXPERIENCE_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13)
    cv = models.FileField(upload_to="cv/")
    is_experienced = models.BooleanField(choices=EXPERIENCE_CHOICES, default=False)
    date_of_birth = models.DateField()
    father_name = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    gap = models.IntegerField(default=0, null=True, blank=True)
    last_company = models.CharField(max_length=255)
    exp_years = models.IntegerField(default=0, null=True, blank=True)
    domain_of_interest = models.ManyToManyField(DomainInterest, related_name='candidates', blank=True )
    qualification = models.ManyToManyField(Qualification, related_name='candidates', blank=True )
    ModifiedByUserid = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, blank=True, related_name='modifier')
    ModifyDateTime = models.DateTimeField(null=True, blank=True)
    DeletedByUserid = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, blank=True, related_name='delete_record')
    DeletedDateTime = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TechArea(models.Model):
    tech_specification = models.CharField(max_length=255, unique=True)
    ModifiedByUserid = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name="modified_tech")
    ModifyDateTime = models.DateTimeField(auto_now=True)
    DeletedByUserid = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name="deleted_tech", blank=True)
    DeletedDateTime = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.tech_specification



class CandidateTechArea(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    tech_area = models.ForeignKey(TechArea, on_delete=models.CASCADE)
    ModifiedByUserid = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name="modified_candidate_tech")
    ModifyDateTime = models.DateTimeField(auto_now=True)
    DeletedByUserid = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name="deleted_candidate_tech", blank=True)
    DeletedDateTime = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.candidate.name} - {self.tech_area.tech_specification}"