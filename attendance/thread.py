import time
import threading
from .models import Record, Employee
import os
from django.shortcuts import render, redirect
from registry.settings import BASE_DIR
from django.utils import timezone


class ClockThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def get_data_from_device(self, file_path):
        with open(file_path, "r") as input_file:
            reader = input_file.read()
            return reader.strip()

    def instant_clocking(self, employee_id):
        employee = Employee.objects.get(em_id=employee_id)

        today = timezone.now().date()
        first_record = Record.objects.filter(
            em_id=employee_id, clocked_time__date=today)

        if first_record == None or first_record.count() % 2 == 0:
            record = Record(em_id=employee.em_id, name=employee.name,
                            role=employee.role, clocking_type=True)
            record.save()
        else:
            record = Record(em_id=employee.em_id, name=employee.name,
                            role=employee.role, clocking_type=False)
            record.save()

    def run(self):
        try:
            file_name = "attendance/clockin_file/input.txt"
            file_path = os.path.join(BASE_DIR, file_name)

            while True:
                if os.path.exists(file_path):
                    employee_id = self.get_data_from_device(file_path)
                    self.instant_clocking(employee_id)
                    os.remove(file_path)
                    redirect('home')
                else:
                    print("scanning...")
                time.sleep(0.5)

        except Exception as e:
            print(e)


ClockThread().start()
