from datetime import timedelta, datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import path

from .models import Dept, Class, Student, Attendance, Course, Teacher, Assign, AssignTime, AttendanceClass
from .models import StudentCourse, Marks, User, AttendanceRange

# Register your models here.

days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class ClassInline(admin.TabularInline):
    model = Class
    extra = 0


class DeptAdmin(admin.ModelAdmin):
    inlines = [ClassInline]
    list_display = ('name', 'id')
    search_fields = ('name', 'id')
    ordering = ['name']


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'dept', 'sem', 'section')
    search_fields = ('id', 'dept__name', 'sem', 'section')
    ordering = ['dept__name', 'sem', 'section']
    inlines = [StudentInline]


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dept')
    search_fields = ('id', 'name', 'dept__name')
    ordering = ['dept', 'id']


class AssignTimeInline(admin.TabularInline):
    model = AssignTime
    extra = 0


class AssignAdmin(admin.ModelAdmin):
    inlines = [AssignTimeInline]
    list_display = ('class_id', 'course', 'teacher')
    search_fields = ('class_id__dept__name', 'class_id__id', 'course__name', 'teacher__name', 'course__shortname')
    ordering = ['class_id__dept__name', 'class_id__id', 'course__id']
    raw_id_fields = ['class_id', 'course', 'teacher']


class MarksInline(admin.TabularInline):
    model = Marks
    extra = 0


class StudentCourseAdmin(admin.ModelAdmin):
    inlines = [MarksInline]
    list_display = ('student', 'course',)
    search_fields = ('student__name', 'course__name', 'student__class_id__id', 'student__class_id__dept__name')
    ordering = ('student__class_id__dept__name', 'student__class_id__id', 'student__USN')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('USN', 'name', 'class_id')
    search_fields = ('USN', 'name', 'class_id__id', 'class_id__dept__name')
    ordering = ['class_id__dept__name', 'class_id__id', 'USN']


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'dept')
    search_fields = ('name', 'dept__name')
    ordering = ['dept__name', 'name']


class AttendanceClassAdmin(admin.ModelAdmin):
    list_display = ('assign', 'date', 'status')
    ordering = ['assign', 'date']
    change_list_template = 'admin/attendance/attendance_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('reset_attd/', self.reset_attd, name='reset_attd'),
        ]
        return my_urls + urls

    def reset_attd(self, request):

        start_date = datetime.strptime(request.POST['startdate'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['enddate'], '%Y-%m-%d').date()

        try:
            a = AttendanceRange.objects.all()[:1].get()
            a.start_date = start_date
            a.end_date = end_date
            a.save()
        except AttendanceRange.DoesNotExist:
            a = AttendanceRange(start_date=start_date, end_date=end_date)
            a.save()

        Attendance.objects.all().delete()
        AttendanceClass.objects.all().delete()
        for asst in AssignTime.objects.all():
            for single_date in daterange(start_date, end_date):
                if single_date.isoweekday() == days[asst.day]:
                    try:
                        AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign=asst.assign)
                    except AttendanceClass.DoesNotExist:
                        a = AttendanceClass(date=single_date.strftime("%Y-%m-%d"), assign=asst.assign)
                        a.save()

        self.message_user(request, "Attendance Dates reset successfully!")
        return HttpResponseRedirect("../")


admin.site.register(User, UserAdmin)
admin.site.register(Dept, DeptAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Assign, AssignAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
admin.site.register(AttendanceClass, AttendanceClassAdmin)
