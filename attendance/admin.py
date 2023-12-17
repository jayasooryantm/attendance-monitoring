from django.contrib import admin
from .models import Record, Employee

admin.site.register(Record)
admin.site.register(Employee)

admin.site.site_header = 'Database System Dashboard'
admin.site.site_title = 'The New Filipino Private School'
admin.site.index_title = 'The New Filipino Private School'
