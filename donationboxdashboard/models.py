from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Donor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    userpic = models.ImageField(null=True)
    regdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    userpic = models.ImageField(null=True)
    idpic = models.ImageField(null=True)
    aboutme = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=20, null=True)
    regdate = models.DateTimeField(auto_now_add=True)
    adminremark = models.CharField(max_length=300, null=True)
    updationdate = models.DateField(null=True)
    is_organization_volunteer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class DonationArea(models.Model):
    areaname = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.areaname


class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donationname = models.CharField(max_length=100, null=True)
    donationpic = models.ImageField(null=True)
    collectionloc = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=30, null=True)
    donationdate = models.DateField(null=True)
    adminremark = models.CharField(max_length=200, null=True)
    volunteer = models.ForeignKey(
        Volunteer, on_delete=models.CASCADE, null=True)
    donationarea = models.ForeignKey(
        DonationArea, on_delete=models.CASCADE, null=True)
    volunteerremark = models.CharField(max_length=200, null=True)
    updationdate = models.DateField(null=True)

    def __str__(self):
        return self.donationname


class Gallery(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    deliverypic = models.ImageField(null=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class Request(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    # could be 'pending', 'approved', 'denied', etc.
    status = models.CharField(max_length=30)

    # class Meta:
    #     unique_together = ('volunteer', 'donation')


class VolunteerProfile(models.Model):
    volunteer = models.OneToOneField(Volunteer, on_delete=models.CASCADE)
    urgency_of_need = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)])
    past_donations = models.IntegerField(default=0)
    registration_date = models.DateTimeField(auto_now_add=True)
