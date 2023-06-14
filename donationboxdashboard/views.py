from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .models import VolunteerProfile
from .forms import VolunteerProfileForm

# Create your views here.
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.db import IntegrityError
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from .models import *
from datetime import date
from sklearn.cluster import KMeans
import random
from .sendSMS import sendSMS
from datetime import datetime, timedelta
# Create your views here.


def index(request):
    total_donor = Donor.objects.count()
    total_volunteer = Volunteer.objects.count()
    total_donation = Donation.objects.count()
    total_services = Gallery.objects.count()
    context = {
        'total_donor': total_donor,
        'total_volunteer': total_volunteer,
        'total_donation': total_donation,
        'total_services': total_services
    }

    return render(request, 'index.html', context)


def all_logins(request):
    return render(request, 'all_logins.html')


def donor_reg(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        em = request.POST['email']
        contact = request.POST['contact']
        pwd = request.POST['pwd']
        userpic = request.FILES['userpic']
        address = request.POST['address']

        try:
            user = User.objects.create_user(
                first_name=fn, last_name=ln, username=em, password=pwd)
            Donor.objects.create(user=user, contact=contact,
                                 userpic=userpic, address=address)

            error = "no"
        except:
            error = "yes"
    context = {
        'error': error,
    }
    return render(request, 'donor_reg.html', context)


def gallery(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery,
    }
    return render(request, 'gallery.html', context)


def donor_login(request):
    error = ""
    if request.method == "POST":
        emailid = request.POST['emailid']
        pwd = request.POST['pwd']
        user = authenticate(username=emailid, password=pwd)
        try:
            if user is not None:
                check_donor = Donor.objects.filter(user=user)
                if check_donor:
                    login(request, user)
                    error = "no"
                else:
                    error = "not_donor"
            else:
                error = "yes"
        except:
            error = "yes"
    context = {
        'error': error,
    }
    return render(request, 'donorlogin.html', context)


def volunteer_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Volunteer.objects.get(user=user)
                if user1.status != "pending":

                    login(request, user)

                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    context = {
        'error': error,
    }
    return render(request, 'volunteer_login.html', context)


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    context = {
        'error': error,
    }
    return render(request, 'admin_login.html', locals())


def donor_home(request):
    if not request.user.is_authenticated:
        return redirect('donorlogin')
    user = request.user
    donor = Donor.objects.get(user=user)
    donationcount = Donation.objects.filter(donor=donor).count()
    acceptedcount = Donation.objects.filter(
        donor=donor, status="accept").count()
    rejectedcount = Donation.objects.filter(
        donor=donor, status="reject").count()
    pendingcount = Donation.objects.filter(
        donor=donor, status="pending").count()
    deliveredcount = Donation.objects.filter(
        donor=donor, status="Donation Delivered Successfully").count()
    return render(request, 'donor_home.html', locals())


def donation_history(request):
    if not request.user.is_authenticated:
        return redirect('donorlogin')
    user = request.user
    donor = Donor.objects.get(user=user)
    donation = Donation.objects.filter(donor=donor)
    return render(request, 'donation_history.html', locals())

# def donation_request_history(request):
#     if not request.user.is_authenticated:
#         return redirect('volunteer_login')
#     user=request.user
#     volunteer=Volunteer.objects.get(user=user)
#     donation=Donation.objects.filter(volunteer=volunteer)
#     return render(request, 'donation_request_history.html',locals())


def donate_now(request):
    if not request.user.is_authenticated:
        return redirect('donorlogin')
    error = ""
    user = request.user
    donor = Donor.objects.get(user=user)
    if request.method == "POST":

        donationname = request.POST['donationname']
        donationpic = request.FILES['donationpic']
        collectionloc = request.POST['collectionloc']
        description = request.POST['description']
        try:
            Donation.objects.create(donor=donor, donationname=donationname, donationpic=donationpic,
                                    collectionloc=collectionloc, description=description, status="pending", donationdate=date.today())
            error = "no"
        except:
            error = "yes"
    return render(request, 'donate_now.html', locals())

# def donate_request(request):
#     if not request.user.is_authenticated:
#         return redirect('volunteer_login')
#     error=""
#     user=request.user
#     volunteer=Volunteer.objects.get(user=user)
#     if request.method=="POST":

#         donationname = request.POST['donationname']

#         description = request.POST['description']
#         try:
#             Donation.objects.create(volunteer=volunteer,donationname=donationname,description=description,status="pending",donationdate=date.today())
#             error = "no"
#         except:
#             error = "yes"
#     return render(request, 'donate_request.html', locals())


def Logout(request):
    logout(request)
    return redirect('index')


def changepwd_donor(request):
    if not request.user.is_authenticated:
        return redirect('donorlogin')
    error = ""
    if request.method == "POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"

    return render(request, 'changepwd_donor.html', locals())


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    totaldonations = Donation.objects.all().count()
    totaldonors = Donor.objects.all().count()
    totalvolunteers = Volunteer.objects.all().count()
    totalpendingdonations = Donation.objects.filter(status="pending").count()
    totalaccepteddonations = Donation.objects.filter(status="accept").count()
    totaldelivereddonations = Donation.objects.filter(
        status="Donation Delivered Successfully").count()
    totaldonationareas = DonationArea.objects.all().count()
    return render(request, 'admin_home.html', locals())


def pending_donation(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.filter(status='pending')
    return render(request, 'pending_donation.html', locals())


def view_donationdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        status = request.POST['status']
        adminremark = request.POST['adminremark']
        try:
            donation.adminremark = adminremark
            donation.status = status
            donation.updationdate = date.today()
            donation.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'view_donationdetail.html', locals())


def accepted_donation(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.filter(status='accept')
    return render(request, 'accepted_donation.html', locals())


def rejected_donation(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.filter(status='reject')
    return render(request, 'rejected_donation.html', locals())

# algorithm to allocate volunteer based on location using fisher yates shuffle algorithm


def assign_volunteer(collectionloc):
    volunteers = list(Volunteer.objects.filter(
        address=collectionloc, is_organization_volunteer=True))
    n = len(volunteers)
    if n == 0:
        return None
    elif n == 1:
        return volunteers[0]
    else:
        # Apply Fisher-Yates shuffle algorithm
        for i in range(n-1, 0, -1):
            j = random.randint(0, i)
            volunteers[i], volunteers[j] = volunteers[j], volunteers[i]
        return volunteers[0]


def accepted_donationdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.get(id=pid)
    donationarea = DonationArea.objects.all()
    volunteer = assign_volunteer(donation.collectionloc)
    error = ""
    if request.method == "POST":
        donationareaid = request.POST['donationareaid']
        da = DonationArea.objects.get(id=donationareaid)
        try:
            donation.donationarea = da
            donation.volunteer = volunteer
            donation.status = "Volunteer Allocated"
            donation.updationdate = date.today()
            donation.save()
            sendSMS(volunteer.user.first_name)
            error = "no"
        except:
            error = "yes"

    return render(request, 'accepted_donationdetail.html', locals())


def volunteer_reg(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        em = request.POST['email']
        contact = request.POST['contact']
        pwd = request.POST['pwd']
        userpic = request.FILES['userpic']
        idpic = request.FILES['idpic']
        address = request.POST['address']
        aboutme = request.POST['aboutme']
        is_organization_volunteer = 'is_organization_volunteer' in request.POST
        try:
            user = User.objects.create_user(
                first_name=fn, last_name=ln, username=em, password=pwd)
            Volunteer.objects.create(user=user, contact=contact, userpic=userpic,
                                     idpic=idpic, address=address, aboutme=aboutme,
                                     status='pending',
                                     is_organization_volunteer=is_organization_volunteer)
            error = "no"
        except:
            error = "yes"
    return render(request, 'volunteer_reg.html', locals())


def volunteer_home(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    totalCollectionReq = Donation.objects.filter(
        volunteer=volunteer, status="Volunteer Allocated").count()
    totalRecDonation = Donation.objects.filter(
        volunteer=volunteer, status="Donation Received").count()
    totalNotRecDonation = Donation.objects.filter(
        volunteer=volunteer, status="Donation NotReceived").count()
    totalDonationDelivered = Donation.objects.filter(
        volunteer=volunteer, status="Donation Delivered Successfully").count()
    return render(request, 'volunteer_home.html', locals())


def manage_donor(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donor = Donor.objects.all()
    return render(request, 'manage_donor.html', locals())


def view_donordetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donor = Donor.objects.get(id=pid)
    return render(request, 'view_donordetail.html', locals())


def delete_donor(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('manage_donor')


def new_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteer = Volunteer.objects.filter(status='pending')
    return render(request, 'new_volunteer.html', locals())


def view_volunteerdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteer = Volunteer.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        status = request.POST['status']
        adminremark = request.POST['adminremark']
        try:
            volunteer.adminremark = adminremark
            volunteer.status = status
            volunteer.updationdate = date.today()
            volunteer.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'view_volunteerdetail.html', locals())


def accepted_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteer = Volunteer.objects.filter(status='accept')
    return render(request, 'accepted_volunteer.html', locals())


def rejected_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteer = Volunteer.objects.filter(status='reject')
    return render(request, 'rejected_volunteer.html', locals())


def add_area(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        areaname = request.POST['areaname']
        des = request.POST['description']
        try:
            DonationArea.objects.create(areaname=areaname, description=des)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_area.html', d)


def manage_area(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    area = DonationArea.objects.all()
    return render(request, 'manage_area.html', locals())


def edit_area(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    area = DonationArea.objects.get(id=pid)

    error = ""
    if request.method == "POST":
        areaname = request.POST['areaname']
        description = request.POST['description']

        area.areaname = areaname
        area.description = description

        try:
            area.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_area.html', locals())


def delete_area(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    area = DonationArea.objects.get(id=pid)
    area.delete()
    return redirect('manage_area')


def changepwd_admin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"

    return render(request, 'changepwd_admin.html', locals())


def volunteerallocated_donation(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.filter(status='Volunteer Allocated')
    return render(request, 'volunteerallocated_donation.html', locals())


def changepwd_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"

    return render(request, 'changepwd_volunteer.html', locals())


def collection_req(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    user = request.user
    volunteer = Volunteer.objects.get(
        user=user)
    donation = Donation.objects.filter(
        volunteer=volunteer, status="Volunteer Allocated")
    return render(request, 'collection_req.html', locals())


def donationcollection_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        status = request.POST['status']
        volunteerremark = request.POST['volunteerremark']
        try:
            donation.status = status
            donation.volunteerremark = volunteerremark
            donation.updationdate = date.today()
            donation.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'donationcollection_detail.html', locals())


def donationrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    user = request.user
    volunteer = Volunteer.objects.get(
        user=user)
    donation = Donation.objects.filter(
        volunteer=volunteer, status="Donation Received")
    return render(request, 'donationrec_volunteer.html', locals())


def donationrec_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        status = request.POST['status']
        deliverypic = request.FILES['deliverypic']
        try:
            donation.status = status
            donation.updationdate = date.today()
            donation.save()
            Gallery.objects.create(donation=donation, deliverypic=deliverypic)
            error = "no"
        except:
            error = "yes"

    return render(request, 'donationrec_detail.html', locals())


def donationnotrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation = Donation.objects.filter(
        volunteer=volunteer, status="Donation NotReceived")
    return render(request, 'donationnotrec_volunteer.html', locals())


def donationdelivered_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('volunteer_login')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation = Donation.objects.filter(
        volunteer=volunteer, status="Donation Delivered Successfully")
    return render(request, 'donationdelivered_volunteer.html', locals())


def profile_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        contact = request.POST['contact']
        address = request.POST['address']
        aboutme = request.POST['aboutme']
        volunteer.user.first_name = fn
        volunteer.user.last_name = ln
        volunteer.contact = contact
        volunteer.address = address
        volunteer.aboutme = aboutme
        try:
            volunteer.save()
            volunteer.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            userpic = request.FILES['userpic']
            volunteer.userpic = userpic
            volunteer.save()
        except:
            pass

        try:
            idpic = request.FILES['idpic']
            volunteer.idpic = idpic
            volunteer.save()
        except:
            pass
    d = {'error': error, 'volunteer': volunteer}
    return render(request, 'profile_volunteer.html', d)


def donationrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.filter(status="Donation Received")
    return render(request, 'donationrec_admin.html', locals())


def donationnotrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.filter(status="Donation NotReceived")
    return render(request, 'donationnotrec_admin.html', locals())


def donationdelivered_admin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.filter(
        status="Donation Delivered Successfully")
    return render(request, 'donationdelivered_admin.html', locals())


def donationdetail_donor(request, pid):
    if not request.user.is_authenticated:
        return redirect('donorlogin')
    donation = Donation.objects.get(id=pid)

    return render(request, 'donationdetail_donor.html', locals())


def profile_donor(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    error = ""
    user = request.user
    donor = Donor.objects.get(user=user)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']

        contact = request.POST['contact']

        address = request.POST['address']

        donor.user.first_name = fn
        donor.user.last_name = ln
        donor.contact = contact
        donor.address = address

        try:
            donor.save()
            donor.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            userpic = request.FILES['userpic']
            donor.userpic = userpic
            donor.save()

        except:
            pass

    return render(request, 'profile_donor.html', locals())


def all_donations(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    donation = Donation.objects.all()
    return render(request, 'all_donations.html', locals())


def delete_donation(request, pid):
    donation = Donation.objects.get(id=pid)
    donation.delete()
    return redirect('all_donations')


def all_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    volunteer = Volunteer.objects.all()
    return render(request, 'all_volunteer.html', locals())


def delete_volunteer(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('all_volunteer')


def volunteer_profile(request):
    volunteer = get_object_or_404(Volunteer, user=request.user)
    # Check if the volunteer already has a profile

    if VolunteerProfile.objects.filter(volunteer=volunteer).exists():
        # Redirect to home if profile already exists
        return redirect('request_donation')

    if request.method == 'POST':
        form = VolunteerProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.volunteer = volunteer
            profile.save()
            return redirect('request_donation')  # Redirect to a success page
    else:
        form = VolunteerProfileForm()

    return render(request, 'volunteer_profile.html', {'form': form})


def volunteer_profile_details(request):
    volunteer = get_object_or_404(Volunteer, user=request.user)
    volunteer_profile = get_object_or_404(
        VolunteerProfile, volunteer=volunteer)
    return render(request, 'volunteer_profile_details.html', {'volunteer_profile': volunteer_profile})


def update_volunteer_profile(request):
    volunteer = get_object_or_404(Volunteer, user=request.user)
    try:
        profile = VolunteerProfile.objects.get(volunteer=volunteer)
    except VolunteerProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = VolunteerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.volunteer = volunteer
            profile.save()
            return redirect('request_donation')  # Redirect to a success page
    else:
        form = VolunteerProfileForm(instance=profile)

    return render(request, 'update_volunteer_profile.html', {'form': form})

# prioritybased scheduling algorithm


def calculate_priority(volunteer_profile):
    # This is a simple example. You can customize the logic based on your requirements.
    urgency_of_need = volunteer_profile.urgency_of_need
    time_waiting = (timezone.now() - volunteer_profile.registration_date).days
    past_donations = volunteer_profile.past_donations

    # Calculate the priority score
    priority = urgency_of_need + time_waiting - past_donations

    return priority


# assign donation to the volunteer with highest priority using priority based scheduling algorithm
def assign_donation(donation):

    # Get all the requests for this donation
    requests = Request.objects.filter(donation=donation, status='requested')

    if not requests:
        return  # No requests to assign

    # Calculate the priority score for each request
    priorities = {}
    for request in requests:

        priority = calculate_priority(request.volunteer.volunteerprofile)

        priorities[request] = priority

    # Sort the requests based on priority score in descending order
    sorted_requests = sorted(
        priorities.items(), key=lambda x: x[1], reverse=True)

    # Assign the donation to the volunteer with the highest priority
    highest_priority_request, _ = sorted_requests[0]

    highest_priority_request.status = 'assigned'
    highest_priority_request.save()

    # Update the donation status
    donation.status = 'assigned'
    donation.volunteer = highest_priority_request.volunteer

    donation.save()
    sendSMS(donation.volunteer.user.first_name)


def request_donation(request):
    if request.method == 'POST':
        # Handle the form submission
        donation_id = request.POST['donation']
        donation = Donation.objects.get(id=donation_id)
        # Assuming the user is logged in and is a volunteer
        user = request.user
        volunteer = Volunteer.objects.get(user=user)

        # Check if the volunteer has already requested this donation
        existing_request = Request.objects.filter(
            volunteer=volunteer, donation=donation).exists()
        if existing_request:
            messages.error(
                request, "You have already requested this donation.")
            return redirect('request_donation')

        new_request = Request(volunteer=volunteer,
                              donation=donation, status='requested')
        new_request.save()

        return redirect('volunteer_home')  # Redirect to a success page
    else:
        # Render the form
        # Get all donations that are accepted and not requested by the current volunteer
        user = request.user
        volunteer = Volunteer.objects.get(user=user)
        requested_donations = Request.objects.filter(
            volunteer=volunteer).values_list('donation_id', flat=True)
        donations = Donation.objects.filter(
            status='accept').exclude(id__in=requested_donations)

        return render(request, 'request_donation.html', {'donations': donations})


def review_requests(request):
    if request.method == 'POST':
        # Handle the form submission
        request_id = request.POST['request_id']
        action = request.POST['action']
        donation_request = Request.objects.get(id=request_id)
        if action == 'approve':
            donation_request.status = 'approved'
            # Assign the donation immediately when a request is approvedtion

            assign_donation(donation_request.donation)

        elif action == 'deny':
            donation_request.status = 'denied'
        donation_request.save()
        return redirect('review_requests')  # Redirect to a success page
    else:
        # Render the list of requests
        # Get all requests for accepted donations
        accepted_donations = Donation.objects.filter(status='accept')
        requests = Request.objects.filter(donation__in=accepted_donations)

        return render(request, 'review_requests.html', {'requests': requests})


def approve_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    req.status = 'approved'
    req.save()
    return redirect('review_requests')


def deny_request(request, request_id):
    # req = get_object_or_404(Request, id=request_id)
    # req.status = 'denied'
    # req.save()
    # return redirect('review_requests')
    req = get_object_or_404(Request, id=request_id)
    donation = req.donation

    # Reset the status of the donation to 'accept'
    donation.status = 'accept'
    donation.save()

    # Delete the request
    req.delete()

    return redirect('review_requests')


def my_requests(request):
    # Assuming the user is logged in and is a volunteer
    user = request.user
    volunteer = get_object_or_404(Volunteer, user=user)

    # Get all requests made by the logged in volunteer
    requests = Request.objects.filter(volunteer=volunteer)

    # Render the page with the volunteer's requests
    return render(request, 'my_requests.html', {'requests': requests})
