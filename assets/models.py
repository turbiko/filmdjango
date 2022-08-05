# python modules
import datetime
import uuid

# Django modules
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.db.models.deletion import CASCADE

# project modules
from users.models import Profile
from . import settings


def warranty_end_date(warranty_years=settings.ASSET_ITEM_WARRANTY_YEARS,
                      warranty_months=settings.ASSET_ITEM_WARRANTY_MONTHS,
                      warranty_days=settings.ASSET_ITEM_WARRANTY_DAYS):

    warranty_start_date = datetime.date.today()
    start_warranty = [
        warranty_start_date.year,
        warranty_start_date.month,
        warranty_start_date.day
    ]
    end_warranty = datetime.date(
        start_warranty[0]+int(warranty_years),
        start_warranty[1]+int(warranty_months),
        start_warranty[2]+int(warranty_days)
    )
    return end_warranty
class Asset(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    warranty_to = models.DateField(default=warranty_end_date())
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL, default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

    @property
    def imageURL(self) -> str:
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset


class Review(models.Model):

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="asset_review_owner")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'asset']]

    # def __str__(self):
    #     return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
