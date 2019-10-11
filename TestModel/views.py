from django.shortcuts import render
from rest_framework import generics

from .models import Project, TestCmd, TestCase, TestPlan
from .serializers import ProjectSerializer, TestStepSerializer, TestCaseSerializer, TestPlanSerializer

# Create your views here.

class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TestCmdList(generics.ListAPIView):
    queryset = TestCmd.objects.all()
    serializer_class = TestStepSerializer

class TestCmdDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestCmd.objects.all()
    serializer_class = TestStepSerializer


class TestCaseList(generics.ListAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

class TestCaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

class TestPlanList(generics.ListAPIView):
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer

class TestPlanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer