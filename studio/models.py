from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import *
from django.db import models
import ast

class ListField(models.TextField):
    #metaclass = models.SubfieldBase
    description = "Stores a python list"

    def init(self, args, **kwargs):
        super(ListField, self).init(args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


# Create your models here.


def image_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'event_images/{0}/{1}'.format(instance.studio_img.id, filename)

def genre_image_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'event_images/{0}/{1}'.format(instance.name, filename)

def category_image_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'event_images/{0}/{1}'.format(instance.name, filename)


class Generics(models.Model):
    name = models.CharField(max_length=255, null=True,
                            blank=True)
    uploaded = models.DateTimeField(auto_now_add=True, null=True,  blank=True)
    image = models.ImageField(upload_to=genre_image_upload, null=True,  blank=True)


    def __str__(self):
        return str(self.name)


class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    service_provider = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to=category_image_upload, null=True, blank=True)
    status = models.BooleanField(default=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class SubCategory(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, null=True,blank=True, related_name='subcategory',
                               on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

status = (
        ('Report', 'Report'),
        ('Blocked', 'Blocked'),
        ('Approved','Approved'),
    )

class Studio(models.Model): 
    first_name = models.CharField(max_length=255,verbose_name=_('First Name'), blank=True,
                                 null=True)
    last_name = models.CharField(max_length=255,verbose_name=_('Last Name'), blank=True,
                                  null=True)
    studio_name = models.CharField(max_length=255,verbose_name=_('Name'), blank=True,
                                  null=True)
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('Description')
                                   )
    #email = models.EmailField(max_length=255, null=True,blank=True)
    latitude = models.FloatField(verbose_name=_('Latitude'), blank=True,
                                 null=True)
    longitude = models.FloatField(verbose_name=_('Longitude'), blank=True, null=True)



    generic = models.ManyToManyField(Generics,null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name='category',
        null=True, blank=True)
    #category = models.ForeignKey('Category',
    #                                null=True, blank=True,
    #                                on_delete=models.SET_NULL)
    subcategory = models.ManyToManyField(SubCategory, verbose_name='subcategory',
        null=True, blank=True)
    
    price = models.FloatField(verbose_name=_('Price Per Session'), max_length=6,null=True,
                             blank=True,default='0')
    instagram = models.URLField(max_length=255, null=True,
                                blank=True,
                                verbose_name=_('Instagram')
                                )
    twitter = models.URLField(max_length=255, null=True,
                              blank=True, verbose_name=_('Twitter'))
    facebook = models.URLField(max_length=255, null=True,
                               blank=True, verbose_name=_('Facebook'))
    created_by=models.ForeignKey('user.User',
                                 on_delete=models.CASCADE,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255,verbose_name=_('Location'), blank=True,
                                 null=True)
    remote_service_status = models.BooleanField(default=False)
    cover_photo = models.FileField(upload_to="cover_photo", blank=True)

    # comment = models.TextField(null=True, blank=True)
    temp_services = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    #studio_distance = models.FloatField(verbose_name=_('Distance'), blank=True, null=True)


    # is_profile_setup=models.BooleanField(default=False)
    #services=ListField(null=True,blank=True)



class StudioImage(models.Model):
    studio_img = models.ForeignKey(Studio, related_name='studio_img',
                                   on_delete=models.CASCADE)
    image = models.FileField(upload_to=image_upload, null=True, blank=True)
    is_active = models.BooleanField(default=True)


day = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'))


class StudioAvailability(models.Model):
    studio = models.ForeignKey(Studio, related_name='studio_avail',
                               on_delete=models.CASCADE)
    days = models.CharField(max_length=255, choices=day)
    start_time = models.CharField(max_length=25, null=True, blank=True)
    end_time = models.CharField(max_length=25, null=True, blank=True)
    # start_time = models.TimeField(max_length=25, null=True, blank=True)
    # end_time = models.TimeField(max_length=25, null=True, blank=True)

    def __str__(self):
        return str(self.studio.id)



class Services(models.Model):
    ServiceId = models.ForeignKey(Studio, related_name='service_id',
                                   on_delete=models.CASCADE)
    ServiceName = models.CharField(max_length=255,verbose_name=_('Service Name'), blank=True,
                                 null=True)
    ServicePrice = models.IntegerField(verbose_name=_('Service Price'), max_length=6,null=True,
                             blank=True)
    IsActive = models.BooleanField(default=True)
    service_remote_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ServiceId)
#multipleselect fields


class Rating(models.Model):
    rating_for = models.ForeignKey(Studio, related_name='rating_for_studio',
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Rating To')
    rating_from = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
        null=True, verbose_name='Rating From')
    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    created_time = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.rating)

    class Meta:
        verbose_name = 'Studio Ratings'
        verbose_name_plural = 'Studio Ratings'
        db_table = 'Rating&Reviews'


class Favourite(models.Model):
    studio = models.ForeignKey(Studio, related_name='fav_studio',
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Studio')
    musician_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_favourite = models.BooleanField(default=False)

    class Meta:
        db_table = 'Favourite User Category'


class RaiseDispute(models.Model):
    musician = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Service Provider",)
    comment = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'raise_dispute'


class StudioBlock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='event_report_user')
    studio_status = models.CharField(max_length=15, choices=status,
                                     default='Approved', verbose_name='Status')
    studio = models.ForeignKey(Studio,on_delete=models.CASCADE,null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

