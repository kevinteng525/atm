from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from . import views
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register('project', views.ProjectViewSet, base_name='projects')
router.register('branch', views.BranchViewSet, base_name='branches')
router.register('dlframework', views.DLFrameworkViewSet, base_name='dlframeworks')
router.register('block', views.BlockViewSet, base_name='blocks')
router.register('configdetail', views.ConfigDetailViewSet, base_name='configdetails')
router.register('configplan', views.ConfigPlanViewSet, base_name='configplans')
router.register('testtype', views.TestTypeViewSet, base_name='testtypes')
router.register('tag', views.TagViewSet, base_name='tags')
router.register('testcmd', views.TestCmdViewSet, base_name='testcmds')
router.register('testcase', views.TestCaseViewSet, base_name='testcases')
router.register('testplan', views.TestPlanViewSet, base_name='testplans')
router.register('testjob', views.TestJobViewSet, base_name='testjobs')
router.register('builddetail', views.BuildDetailViewSet, base_name='builddetails')
router.register('buildplan', views.BuildPlanViewSet, base_name='buildplans')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title="Alinpu Test Management", description="API design for Alinpu Test Management", authentication_classes=[], permission_classes=[])),
    path('open/testplan/<str:plan_name>/', views.GenTestPlan),
    path('open/testjob/<str:job_name>/', views.GenTestJob),
    path('open/buildplan/<str:plan_name>/', views.GenBuildPlan),
    path('open/wholecaselist/', views.GenWholeCaseList),
    path('open/democaselist/', views.GenDemoCaseList)
]
# urlpatterns.append(
#     path('open/testplan/<str:plan_name>/', views.GenTestPlan)
# )
# urlpatterns.append(
#     path('open/testjob/<str:job_name>/', views.GenTestJob)
# )
# urlpatterns.append(
#     path('open/buildplan/<str:plan_name>/', views.GenBuildPlan)
# )
# urlpatterns.append(
#     path('open/wholecaselist/', views.GenWholeCaseList)
# )
#
# urlpatterns = [
#     path('project/', views.ProjectList.as_view()),
#     path('project/<int:pk>/', views.ProjectDetail.as_view()),
#     path('teststep/', views.TestStepList.as_view()),
#     path('teststep/<int:pk>/', views.TestStepDetail.as_view()),
#     path('testcase/', views.TestCaseList.as_view()),
#     path('testcase/<int:pk>/', views.TestCaseDetail.as_view()),
#     path('testplan/', views.TestPlanList.as_view()),
#     path('testplan/<int:pk>/', views.TestPlanDetail.as_view()),
# ]