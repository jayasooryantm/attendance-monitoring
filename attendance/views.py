from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.db import connection
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test

from datetime import datetime
from io import StringIO
import os
import pandas as pd
import time

from .forms import FilterForm, RemarkForm, FileUploadForm
from .models import Record, Employee

from registry.settings import BASE_DIR


def get_data_from_device(file_path="/Users/jaya/Downloads/attenaceApp/registry/input.txt"):
    count = 2
    while count <= 2:
        if os.path.exists(file_path):
            with open(file_path, "r") as input_file:
                reader = input_file.read()
                return reader.strip()
        count += 1
        time.sleep(1)
    return None


def home(request):
    today = timezone.now().date()
    today_records = Record.objects.filter(created_at__date=today)
    return render(request, "home.html", {"records": today_records})


def all_records(request):
    form = FilterForm(request.POST)

    if request.method == "POST" and form.is_valid():

        name = form.cleaned_data["filter_name"]
        em_id = form.cleaned_data["filter_id"]
        from_date = form.cleaned_data["from_date"]
        to_date = form.cleaned_data["to_date"]

        queryset = Record.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)

        if em_id:
            queryset = queryset.filter(em_id=em_id)

        if from_date and to_date:
            date_query = Q(clocked_time__gte=from_date) & Q(
                clocked_time__lte=to_date)
            queryset = queryset.filter(date_query)

        records = queryset.all()
        if request.POST['submit_type'] == 'download':

            data = {
                'Employee ID': [record.em_id for record in records],
                'Name': [record.name for record in records],
                'Designation': [record.role for record in records],
                'Clocked Time': [record.clocked_time.replace(tzinfo=None) if record.clocked_time else None for record in records],
                'In/Out': ['Clock In' if record.clocking_type else 'Clock Out' for record in records],
                'Remarks': [record.remark for record in records]}

            df = pd.DataFrame(data)
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            response = HttpResponse(content_type='application/csv')
            response['Content-Disposition'] = f'attachment; filename=records_export{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'

            response.write(csv_buffer.getvalue().encode('utf-8'))
            return response

        return render(request, "all_record.html", {"records": records,  "form": form})
    records = Record.objects.all()
    return render(request, "all_record.html", {"records": records, "form": form})


@user_passes_test(lambda u: u.is_staff)
def load_employee_data_to_db(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            employee_database = pd.read_excel(excel_file)

            try:
                records = []
                for index, row in employee_database.iterrows():
                    records.append(
                        Employee(em_id=row["employee id"], name=row["name"], role=row["designation"]))
                result = Employee.objects.bulk_create(records)

                return HttpResponse(f"<p>Successfully added {len(result)} employee data<p> ")
            except Exception as e:
                error_message = f"Error loading employee data: {e}"
                return HttpResponse(error_message, status=500)
    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form})


def clock_in(request, employee_id=None, remark=None):

    form_data = RemarkForm(request.POST)
    if request.method == "POST" and form_data.is_valid():
        remark = form_data.cleaned_data["remark"]
        employee_id = form_data.cleaned_data['em_id']

        employee = Employee.objects.get(em_id=employee_id)
        record = Record(em_id=employee.em_id, name=employee.name,
                        role=employee.role, clocking_type=True, remark=remark)
        record.save()
        return redirect('home')

    employee_id = get_data_from_device()

    if employee_id == None:
        return HttpResponse("<p>Employee ID Not Found</p>")

    employee = Employee.objects.get(em_id=employee_id)

    form = RemarkForm(instance=employee)
    return render(request, "clock_in.html", {"header": f"Employee Clocking In", "form": form})


def clock_out(request, employee_id=None, remark=None):

    form_data = RemarkForm(request.POST)
    if request.method == "POST" and form_data.is_valid():

        remark = form_data.cleaned_data["remark"]
        employee_id = form_data.cleaned_data['em_id']

        employee = Employee.objects.get(em_id=employee_id)
        record = Record(em_id=employee.em_id, name=employee.name,
                        role=employee.role, clocking_type=False, remark=remark)
        record.save()
        return redirect('home')

    employee_id = get_data_from_device()

    if employee_id == None:
        return HttpResponse("<p>Employee ID Not Found</p>")
    employee = Employee.objects.get(em_id=employee_id)

    form = RemarkForm(instance=employee)
    return render(request, "clock_out.html", {"header": f"Employee Clocking Out", "form": form})


def employees(request):
    employees = Employee.objects.all()
    return render(request, "employees.html", {"employees": employees})
