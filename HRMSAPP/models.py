from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# >> we use a custom userr model to store user data in the database

# HR Model (Custom User Model)
class HR(AbstractUser):
    GENDER = [
        ('Male', 'Male'),
        ('Female','Female'),
    ]
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=50, choices=GENDER, default='Female', null=True, blank='True' )
    
    
    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ["username"] 
    
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="hr_users",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="hr_specific_permissions",  #related_name change kiya
        blank=True
    )
    
    def __str__(self):
        return self.email

# THis is  Candidate Model we store only canditate data in database
class Candidate(models.Model):
    EXPERIENCE_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]
    GENDER = [
        ('Male','Male'),
        ('Female','Female'),
    ]
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER, default='Female', null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    is_experienced = models.BooleanField(choices=EXPERIENCE_CHOICES, default = False, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True) 
    father_name = models.CharField(max_length=255, null=True, blank=True)
    domain_of_interest = models.ForeignKey('DomainInterest', on_delete=models.SET_NULL, null=True, blank=True)
    highest_Qualification = models.ForeignKey('Qualification', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    any_gap = models.BooleanField(default=False, null=True, blank=True)
    last_company = models.CharField(max_length=255, blank=True, null=True)
    work_experience = models.TextField(blank = True, null = True)
    exp_years = models.FloatField(default=0, blank=True, null=True)  
    modified_by = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name='modified_candidates')
    modified_date = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name='deleted_candidates')
    deleted_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return self.name


# TechArea Model
class TechArea(models.Model):
    tech_specification = models.CharField(max_length=255, null=True, blank=True)
    modified_by = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, blank= True, related_name='modified_tech_areas')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_by = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_tech_areas')
    deleted_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.tech_specification 

# Qualification Model
class Qualification(models.Model):
    qualification_name = models.CharField(max_length=255, null=True, blank=True)
    qualification_desc = models.TextField(null=True, blank=True)
    modified_by = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_qualifications')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_by = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name='deleted_qualifications')
    deleted_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.qualification_name

# CandidateTechArea Model (Junction Table)
class CandidateTechArea(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    tech_area = models.ForeignKey(TechArea, on_delete=models.CASCADE, null=True, blank=True)
    modified_by = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_candidate_tech_areas')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_by = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_candidate_tech_areas')
    deleted_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.candidate.name} - {self.tech_area.tech_specification}"        

# DomainInterest Model
class DomainInterest(models.Model):
    domain_name = models.CharField(max_length=255, unique = True, null=True, blank=True)
    modified_by = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name='modified_domain_interests')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_by = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True, related_name='deleted_domain_interests')
    deleted_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)

    def delete(self, deleted_by=None, *args, **kwargs):
        """Soft delete instead of hard delete"""
        self.is_deleted = True
        self.deleted_by = deleted_by
        self.deleted_date = now()
        self.save()

    def restore(self):
        """Restore the deleted record"""
        self.is_deleted = False
        self.deleted_by = None  # Reset deleted_by
        self.deleted_date = None  # Reset deleted_date
        self.save()

    def __str__(self):
        return self.domain_name if self.domain_name else "unnamed Domain" 