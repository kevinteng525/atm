from django.urls import path

from . import views

urlpatterns = [
    path('project/', views.ProjectList.as_view()),
    path('project/<int:pk>/', views.ProjectDetail.as_view()),
    path('testcmd/', views.TestCmdList.as_view()),
    path('testcmd/<int:pk>/', views.TestCmdDetail.as_view()),
    path('testcase/', views.TestCaseList.as_view()),
    path('testcase/<int:pk>/', views.TestCaseDetail.as_view()),
    path('testplan/', views.TestPlanList.as_view()),
    path('testplan/<int:pk>/', views.TestPlanDetail.as_view()),
]