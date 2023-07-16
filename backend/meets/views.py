from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import csv
from .models import Lifter, Meet, Result

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f, meet):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    with open('some/file/name.txt', 'r') as file:
        data = csv.reader(file)
        headers = next(data, None) # Skips the headers
        for row in data:
            name, team, div, bwt_kg, ipf_wt_cls, dob, lot, squat1, squat2, squat3, bench1, bench2, bench3, deadlift1, deadlift2, deadlift3, event, state, member_id, drug_test = row
            
            # Creates a new lifter if not already in database
            lifter, created = Lifter.objects.get_or_create(
                member_id=member_id,
                defaults={'name': name},
            )

            # Creates new result
            Result.objects.create(
                lifter=lifter,
                meet=meet,
                team=team,
                div=div,
                bwt_kg=bwt_kg,
                ipf_wt_cls=ipf_wt_cls,
                dob=dob,
                lot=lot,
                squat1=squat1,
                squat2=squat2,
                squat3=squat3,
                bench1=bench1,
                bench2=bench2,
                bench3=bench3,
                deadlift1=deadlift1,
                deadlift2=deadlift2,
                deadlift3=deadlift3,
                event=event,
                state=state,
                drug_test=drug_test,
            )
