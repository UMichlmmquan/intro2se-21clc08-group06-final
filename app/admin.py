from django.contrib import admin
from app.models import User,Employer, Job_finder, Post, CV, Report
# Register your models here.


admin.site.register(User)
admin.site.register(Employer)
admin.site.register(Job_finder)
admin.site.register(Post)
admin.site.register(CV)
admin.site.register(Report)