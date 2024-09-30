from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import math

# Create your models here.
class User(AbstractUser):
    is_job_finder = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
CITY_CHOICES = (
        ('An Giang', 'An Giang'),
        ('Ba Ria-Vung Tau', 'Ba Ria-Vung Tau'),
        ('Bac Lieu', 'Bac Lieu'),
        ('Bac Kan', 'Bac Kan'),
        ('Bac Giang', 'Bac Giang'),
        ('Bac Ninh', 'Bac Ninh'),
        ('Ben Tre', 'Ben Tre'),
        ('Binh Duong', 'Binh Duong'),
        ('Binh Dinh', 'Binh Dinh'),
        ('Binh Phuoc', 'Binh Phuoc'),
        ('Binh Thuan', 'Binh Thuan'),
        ('Ca Mau', 'Ca Mau'),
        ('Cao Bang', 'Cao Bang'),
        ('Can Tho', 'Can Tho'),
        ('Da Nang', 'Da Nang'),
        ('Dak Lak', 'Dak Lak'),
        ('Dak Nong', 'Dak Nong'),
        ('Dien Bien', 'Dien Bien'),
        ('Dong Nai', 'Dong Nai'),
        ('Dong Thap', 'Dong Thap'),
        ('Gia Lai', 'Gia Lai'),
        ('Ha Giang', 'Ha Giang'),
        ('Ha Nam', 'Ha Nam'),
        ('Ha Noi', 'Ha Noi'),
        ('Ha Tinh', 'Ha Tinh'),
        ('Hai Duong', 'Hai Duong'),
        ('Hai Phong', 'Hai Phong'),
        ('Hoa Binh', 'Hoa Binh'),
        ('Ho Chi Minh City', 'Ho Chi Minh City'),
        ('Hau Giang', 'Hau Giang'),
        ('Hung Yen', 'Hung Yen'),
        ('Khanh Hoa', 'Khanh Hoa'),
        ('Kien Giang', 'Kien Giang'),
        ('Kon Tum', 'Kon Tum'),
        ('Lai Chau', 'Lai Chau'),
        ('Lao Cai', 'Lao Cai'),
        ('Lang Son', 'Lang Son'),
        ('Lam Dong', 'Lam Dong'),
        ('Long An', 'Long An'),
        ('Nam Dinh', 'Nam Dinh'),
        ('Nghe An', 'Nghe An'),
        ('Ninh Binh', 'Ninh Binh'),
        ('Ninh Thuan', 'Ninh Thuan'),
        ('Phu Tho', 'Phu Tho'),
        ('Phu Yen', 'Phu Yen'),
        ('Quang Binh', 'Quang Binh'),
        ('Quang Nam', 'Quang Nam'),
        ('Quang Ngai', 'Quang Ngai'),
        ('Quang Ninh', 'Quang Ninh'),
        ('Quang Tri', 'Quang Tri'),
        ('Soc Trang', 'Soc Trang'),
        ('Son La', 'Son La'),
        ('Tay Ninh', 'Tay Ninh'),
        ('Thai Binh', 'Thai Binh'),
        ('Thai Nguyen', 'Thai Nguyen'),
        ('Thanh Hoa', 'Thanh Hoa'),
        ('Thua Thien-Hue', 'Thua Thien-Hue'),
        ('Tien Giang', 'Tien Giang'),
        ('Tra Vinh', 'Tra Vinh'),
        ('Tuyen Quang', 'Tuyen Quang'),
        ('Vinh Long', 'Vinh Long'),
        ('Vinh Phuc', 'Vinh Phuc'),
        ('Yen Bai', 'Yen Bai'),
    )
class Job_finder(models.Model):
    full_name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    gender=models.CharField(max_length=100)
    address=models.TextField()
    city = models.CharField(max_length=255, choices=CITY_CHOICES)
    date_of_birth=models.TextField()
    introduction=models.TextField()

class Employer(models.Model):
    company_name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    address=models.TextField()
    city = models.CharField(max_length=255, choices=CITY_CHOICES)
    introduction=models.TextField()

class Post(models.Model):
    pic_url = models.ImageField()
    company_name=models.CharField(default="",max_length=100)
    contact = models.CharField(max_length=100, blank=True, null=True)
    introduction = models.TextField(default="")
    city=models.TextField(default="")
    caption = models.CharField(max_length=255)
    address = models.TextField()
    fields = ( ('Medicine', 'Medicine'),
            ('Law', 'Law'),
            ('Information Technology', 'Information Technology'),
            ('Finance and Banking', 'Finance and Banking'),
            ('Business Management', 'Business Management'),
            ('Education', 'Education'),
            ('Insurance Business', 'Insurance Business'),
            ('Real Estate', 'Real Estate'),
            ('Tourism', 'Tourism'),
            ('Electronics/Electricity', 'Electronics/Electricity'),
            ('Architecture', 'Architecture'),
            ('Hotel and Restaurant', 'Hotel and Restaurant'),
            ('Construction/Building', 'Construction/Building'),
            ('Finacial Investment', 'Finacial Investment'),
        )
    field = models.CharField(choices=fields)
    job = models.CharField()
    description = models.TextField()
    hour = models.CharField(max_length=255)
    salaries = ( ('Below 100$','Below 100$'),
               ('100$ - 200$','100$ - 200$'),
               ('200$ - 400$','200$ - 400$'),
               ('400$ - 600$','400$ - 600$'),
               ('600$ - 800$','600$ - 800$'),
               ('800$ - 1000$','800$ - 1000$'),
               ('Above 1000$','Above 1000$'),
               )
    salary = models.CharField(choices=salaries)

    deny = models.TextField()
    approve = models.TextField()

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Hide function uses here
    is_hidden = models.BooleanField(default=False)
    # Additional fields
    likes = models.ManyToManyField(User, related_name='liked_posts')
    dislikes = models.ManyToManyField(User, related_name='disliked_posts')
    
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    # Time posted function
    def __str__(self):
        return self.caption


    def time_posted(self):
        now = timezone.now()
        
        diff = now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_comments', blank=True)

class CV(models.Model):
    finder = models.ForeignKey(Job_finder, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    address = models.TextField()
    date_of_birth = models.TextField()
    introduction = models.TextField()
    experience = models.TextField()
    education = models.TextField()
    interest = models.TextField()
    languages = models.TextField()
    skill = models.TextField()
    mail = models.EmailField()
    phone = models.CharField()

class Dashboard(models.Model):
    #E
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    STATUS_CHOICES_E = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DENIED', 'Denied'),
        ('HIDE', 'Hide'),
        ('HIGHTLIGHT', 'Hightlight')
    ]
    status_E = models.CharField(max_length=10, choices=STATUS_CHOICES_E, default='PENDING')
    #JF
    job_finder = models.ForeignKey(Job_finder, on_delete=models.CASCADE,default="")
    company_name = models.CharField(max_length=200,default="")
    job_applied = models.CharField(max_length=200,default="")
    STATUS_CHOICES_JF = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DENIED', 'Denied'),
    ]
    status_JF = models.CharField(max_length=10, choices=STATUS_CHOICES_JF, default='PENDING')

    #BOTH
    applied_time = models.DateTimeField(auto_now_add=True)
    highlight = models.BooleanField(default=False)
    deny = models.TextField()
    approve = models.TextField()

class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    content = models.TextField(default="")
    is_user = models.BooleanField(default=False)
    is_post = models.BooleanField(default=False)
    reported_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='reported',null=True, blank=True)
    reported_post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True, blank=True,)