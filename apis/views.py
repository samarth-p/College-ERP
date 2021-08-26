from django.shortcuts import render
from info.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from itertools import chain
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from django.db.models.signals import post_save
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from django.db.models import Sum, Count
from django.conf import settings
import apis.serializers as api_ser


class DetailView(APIView):
    """
    Returns user's info.
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            # fetching token sent in request header by the user.
            us = Token.objects.filter(user=request.user)
            if(us):          # checking for authentication using token authentication.

                # getting user from in-built user model class.
                user = User.objects.filter(auth_token=us[0]).first()
                # getting student from student model by filtering based on user that we got.
                details = Student.objects.get(user=user)
                serializer = api_ser.DetailSerializer(
                    details, context={'request': request})       # Serializing the data into Json format.
                return Response({'data': serializer.data, }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class AttendanceView(APIView):
    """
    This view is used to return user's attendance 
    that is to check user's attendance.
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            token = Token.objects.filter(user=request.user).first()
            if(token):  # checking for authentication using token authentication.
                # getting user from in-built user model class.
                user = User.objects.get(auth_token=token)
                # getting student from student model by filtering based on user that we got.
                stud = Student.objects.get(user=user)
                # using ass_list and att_list we get the classes assigned to that user
                ass_list = Assign.objects.filter(class_id_id=stud.class_id)
                # and respectively their attendance
                att_list = []
                for ass in ass_list:
                    try:
                        a = AttendanceTotal.objects.get(
                            student=stud, course=ass.course)
                    except AttendanceTotal.DoesNotExist:
                        a = AttendanceTotal(student=stud, course=ass.course)
                        a.save()
                    att_list.append(a)
                serializer = api_ser.AttendanceSerializer(
                    att_list, many=True, context={'request': request})     # Serializing the data into Json format.
                return Response({'user_attendance': serializer.data, }, status=status.HTTP_200_OK)
            else:
                # returning not authenticated message when user isn't authenticated with status code 400.
                return Response({'message': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MarksView(APIView):
    """
    This view is used to return user's marks 
    that is to check user's marks in different subjects as given by the teacher.
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            token = Token.objects.filter(user=request.user).first()
            if(token):  # checking for authentication using token authentication.
                user = User.objects.get(auth_token=token)
                stud = Student.objects.get(user=user)

                # using ass_list and sc_list we retrieve all the subjects assigned
                ass_list = Assign.objects.filter(class_id_id=stud.class_id)
                # and then their respective marks. Store them in a dictionary and return it to the user.
                sc_list = []
                for ass in ass_list:
                    sc = StudentCourse.objects.get(
                        student=stud, course=ass.course)
                    sc_list.append(sc)
                sc_total = {}
                for sc in sc_list:
                    for m in sc.marks_set.all():
                        sc_total[m.studentcourse.course.name] = m.marks1
                return Response({'user_marks': sc_total, }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TimetableView(APIView):
    """
    This view is used to check user's class timetable
    It returns the respective class' timetable to which the user is assigned.
    """

    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            token = Token.objects.filter(user=request.user).first()
            if(token):  # checking for authentication using token authentication.
                user = User.objects.get(auth_token=token)
                stud = Student.objects.get(user=user)
                asst = AssignTime.objects.filter(
                    assign__class_id=stud.class_id)
                serializer = api_ser.TimeTableSerializer(
                    asst, many=True, context={'request': request})     # Serializing the data into Json format.
                return Response({'user_marks': serializer.data, }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
