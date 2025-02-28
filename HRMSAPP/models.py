from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# >> we use a custom userr model to store user data in the database

# HR Model (Custom User Model)
class HR(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)# ✅ Ensure it's True
    company = models.CharField(max_length=255, blank=True, null=True)
    
    
    USERNAME_FIELD = "email"  # ✅ FIXED: Email ko primary bana diya
    REQUIRED_FIELDS = ["username"]  # ✅ Username ko optional rakha
    
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="hr_users",  # ✅ related_name change kiya
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="hr_specific_permissions",  # ✅ related_name change kiya
        blank=True
    )
    
    def __str__(self):
        return self.email

# THis is  Candidate Model we store only canditate data in database
class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    resume = models.FileField(upload_to="resumes/")
    experience = models.FloatField(blank=True, null=True)
    skills = models.TextField()
    date_of_birth = models.DateField()
    father_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    domain_of_interest = models.CharField(max_length=255)
    tech_area = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    # pincode = models.CharField(max_length=6)
    # country = models.CharField(max_length=255)
    # photo = models.ImageField(upload_to="photos/")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    any_gap = models.BooleanField(default=False)
    # gap_reason = models.TextField(blank=True, null=True)
    # year_of_passing = models.IntegerField()
    last_company = models.CharField(max_length=255)
    # last_designation = models.CharField(max_length=255)
    # last_salary = models.FloatField()
    # notice_period = models.IntegerField()
    # current_ctc = models.FloatField() 
    # expected_ctc = models.FloatField()
    work_experience = models.TextField(blank = True, null = True)
    exp_years = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    