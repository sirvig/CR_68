from django.shortcuts import render

import datetime, random, string

from models import *
from forms import *

def percentage(part, whole):
  return 100 * float(part)/float(whole)

def showTable(request):
    dReturn = {}
    centername = "Living Waters Children's Ranch"
    
    dDonationMax = {
        '25': 11,
        '50': 10,
        '75':  9,
        '100': 8,
        '250': 7,
        '500': 6,
        '750': 5,
        '1000': 4,
        '2500': 3,
        '5000': 2,
        '10000': 1,
        }
    
    # Gather information for page display
    oDonations = Donation.objects.all()
    
    for key,entry in dDonationMax.iteritems():
        donate_count = 0
        donate_more = 0
        donate_percent = 0
        
        donate_count = oDonations.filter(amount = key + ".00").count()
        donate_more = entry - donate_count
        donate_percent = int(percentage(donate_count, entry))
        
        dReturn['donate' + key + '_count'] = donate_count
        dReturn['donate' + key + '_more'] = donate_more
        dReturn['donate' + key + '_percent'] = donate_percent
        
    
    # Handle donations and present form
    if request.method == 'POST':
        # check response
        form = DonationForm(request.POST)
        if form.is_valid():
            # The form is valid
            cd = form.cleaned_data
            amount = str(cd['amount']) + ".00"
            
            # Lookup center
            try:
                center = Center.objects.get(name=centername)
            except:
                request.flash['error'] = "The feeding center specified is not configured for this site."
                return render_to_response("error.html", dReturn, context_instance=RequestContext(request))
                
            # Lookup donor
            try:
                donor = Donor.objects.get(email=cd['emailaddress'])
            except:
                # Doesnt exist - need to create a new one
                donor = Donor(name=cd['name'],
                              email=cd['emailaddress'])
                          
                donor.save()
            
            # Generate random key
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
            
            # Save transaction to transaction table
            rightnow = datetime.datetime.now()
            transaction = Donation (key=key,
                                    donor=donor,
                                    center=center,
                                    amount=amount,
                                    anon=cd['anon'],
                                    frequency=cd['frequency'],
                                    dt_donated=rightnow,
                                    confirmed=False)
            
            transaction.save()
            
            # Now create the paypal form and submit
            dPaypal = {}
            dPaypal['centername'] = center.name
            dPaypal['reference'] = center.reference
            dPaypal['amount'] = amount
            dPaypal['return'] = key
            dPaypal['center'] = center
            if cd['frequency'] == "2":
                dPaypal['monthly'] = True
            
            return render(request, "paypal.html", dPaypal)
    
        else:
            dReturn['form'] = form
    else:
        form = DonationForm(initial={
            'centername': centername,
            'frequency': '1',
            })
        dReturn['form'] = form
        
    return render(request, "fundraiser.html", dReturn)
