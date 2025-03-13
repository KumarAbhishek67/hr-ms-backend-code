from django.contrib import admin
from .models import HR, Candidate, TechArea, Qualification, CandidateTechArea, DomainInterest
from django.utils.html import format_html

# we make in logic to show in data basee format
class HrAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_active', 'is_staff')
    list_display_links = ('id', 'email')
    
    # now we add search filter in data base
    search_fields = ('name', 'email')
    list_filter = ['is_active']
    list_per_page = 20
    
    # now make a funtion
    def clickable_email(self, obj):
        return format_html(f'<a href="mailto:{obj.email}">{obj.email}</a>')
    
    clickable_email.short_description = 'Email'

# now asits we make for a candidate table 
class candidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'mobile', 'exp_years', 'resume', 'gender', 'city', 'state', 'address')    
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email')
    list_filter = ['name']
    list_per_page = 20
    
    # main logic for show the resume in admin panel
    def clickable_name(self, obj):
        return format_html(f'<a href="{obj.name.url}" target="_blank">{obj.name}</a>')
    
    clickable_name.short_description = 'name'
    
# now we make TEchArea 
class TechAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'tech_specification', 'is_deleted')
    list_display_links = ('id', 'tech_specification')
    search_fields = ('tech_specification',)
    list_filter = ['tech_specification']
    list_per_page = 20
    
    def clickable_tech_specification(self, obj):
        return format_html(f'<a href="{obj.tech_specification.url}" target="_blank">{obj.tech_specification}</a>')

#now we make Qualification Admin
class qualificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'qualification_name', 'is_deleted')
    list_display_links = ('id', 'qualification_name')
    search_fields = ('qualification_name',)
    list_filter = ('is_deleted',)
    list_per_page = 20
    
    def clickable_qualification_name(self, obj):
        return format_html(f'<a href="{obj.qualification_name.url}" target="_blank">{obj.qualification_name}</a>')

# now we make CandidateTechArea Admin
class CandidateTechAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'candidate', 'tech_area', 'is_deleted')
    list_display_links = ('id', 'candidate')
    search_fields = ('candidate', 'tech_area')
    list_filter = ['candidate', 'tech_area']
    list_per_page = 20
    
    def clickable_candidate(self, obj):
        return format_html(f'<a href="{obj.candidate.url}" target="_blank">{obj.candidate}</a>')            

#   DomainInterest Admin
class DomainInterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain_name', 'is_deleted')
    list_display_links = ('id', 'domain_name')
    search_fields = ('domain_name','is_deleted')
    list_filter = ('is_deleted',)
    list_per_page = 20
    
    def clickable_domain_name(self, obj):
        return format_html(f'<a href="{obj.domain_name.url}" target="_blank">{obj.domain_name}</a>')
# Register your models here.
admin.site.register(HR,HrAdmin)
admin.site.register(Candidate, candidateAdmin)
admin.site.register(TechArea, TechAreaAdmin)
admin.site.register(Qualification, qualificationAdmin) 
admin.site.register(CandidateTechArea, CandidateTechAreaAdmin)
admin.site.register(DomainInterest, DomainInterestAdmin)
