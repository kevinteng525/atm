from django.shortcuts import render
from rest_framework import generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from TestModel.models import *
from BuildModel.models import BuildPlan, BuildDependency, BuildProject, BuildDetail
from ConfigModel.models import Project, Branch, DLFramework, Block, ConfigDetail, ConfigPlan
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class StandardPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class DLFrameworkViewSet(viewsets.ModelViewSet):
    queryset = DLFramework.objects.all()
    serializer_class = DLFrameworkSerializer

class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

class ConfigDetailViewSet(viewsets.ModelViewSet):
    queryset = ConfigDetail.objects.all()
    serializer_class = ConfigDetailSerializer

class ConfigPlanViewSet(viewsets.ModelViewSet):
    queryset = ConfigPlan.objects.all()
    serializer_class = ConfigPlanSerializer

class TestTypeViewSet(viewsets.ModelViewSet):
    queryset = TestType.objects.all()
    serializer_class = TestTypeSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# with filter, search, pagination
class TestCmdViewSet(viewsets.ModelViewSet):
    queryset = TestCmd.objects.all()
    serializer_class = TestCmdSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name','block','project','priority','tag')
    search_fields = ['name']
    pagination_class = StandardPageNumberPagination

# with filter, search and ordering
class TestCaseViewSet(viewsets.ModelViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name',)
    search_fields = ['name']
    ordering_fields = ['name']
    pagination_class = StandardPageNumberPagination

class TestPlanViewSet(viewsets.ModelViewSet):
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanUpdateSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name','project__name')
    search_fields = ['name','project__name']
    lookup_field = 'name'

    def list(self, request, *args, **kwargs):
        self.serializer_class = TestPlanSerializer
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

class TestJobViewSet(viewsets.ModelViewSet):
    queryset = TestJob.objects.all()
    serializer_class = TestJobSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name',)
    search_fields = ['name']

class BuildDetailViewSet(viewsets.ModelViewSet):
    queryset = BuildDetail.objects.all()
    serializer_class = BuildDetailSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name',)
    search_fields = ['name']

class BuildPlanViewSet(viewsets.ModelViewSet):
    queryset = BuildPlan.objects.all()
    serializer_class = BuildPlanSerializer



def parseConfigs(config, is_cmd=False):
    if config == '':
        return ''
    items = config.split('\r\n')
    dict = {}
    for item in items:
        if is_cmd:
            dict['cmd'] = item.strip()
        else:
            pair = item.split('=')
            dict[pair[0].strip()] = pair[1].strip()
    return dict

def getTestPlanJson(testplan):
    testcase_set = testplan.testcase.all()
    testplan_name = testplan.name
    project = testplan.project.name
    branch = testplan.branch.name
    dlframework = testplan.dlframework.name
    runmode = testplan.runmode.name if testplan.runmode != None else ''
    testcase_configs = testplan.config.config.all() if testplan.config != None else 0
    config_list = []
    if testcase_configs:
        for config in testcase_configs:
            config_type = config.configtype.name
            is_cmd = False
            if config_type.lower() == "cmdline":
                is_cmd = True
            config_json = parseConfigs(config.content, is_cmd)
            config_list.append({config_type: config_json})
    blocks = []
    caselist = []

    for testcase in testcase_set:
        testcase_name = testcase.name
        testcase_block = testcase.testcmd.block.name
        blocks.append(testcase_block)
        caselist.append(
            {
                'name': testcase_name,
                'block': testcase_block,
            }
        )
    blocks = list(set(blocks))
    json = {
        'name': testplan_name,
        'project': project,
        'branch': branch,
        'dlframework': dlframework,
        'runmode': runmode,
        'blocks': blocks,
        'topconfigs': config_list,
        'testcases': caselist,
    }
    return json

def getBuildPlanJson(buildplan):
    name = buildplan.name
    version = buildplan.version
    project = buildplan.project.name
    branch = buildplan.branch.name
    ostype = buildplan.ostype.name
    gcc_version = buildplan.gcc_version.name if buildplan.gcc_version != None else ''
    archived = buildplan.archived
    buildconfigs = buildplan.buildconfig.all()
    buildinfolist = []
    for buildinfo in buildconfigs:
        options = parseConfigs(buildinfo.options)
        depends = BuildDependency.objects.filter(buildproject=buildinfo.buildproject)
        dependentprojectlist = []
        dir = ''
        if depends:
            dependentprojects = depends[0].dependprojects.all()
            if dependentprojects:
                for dependproject in dependentprojects:
                    dependentprojectlist.append(dependproject.name)
            dir = depends[0].dir
        buildinfo_json = {
            'project': buildinfo.buildproject.name,
            'dir': dir,
            'depends': dependentprojectlist,
            'mode': buildinfo.buildmode.name,
            'buildtype': buildinfo.buildtype,
            'options': options
        }
        buildinfolist.append(buildinfo_json)

    json = {
        'name': name,
        'project': project,
        'branch': branch,
        'version': version,
        'os_type': ostype,
        'gcc_version': gcc_version,
        'archived': archived,
        'buildconfigs': buildinfolist
    }
    return json

def getEnvJson(env):
    if env == None:
        return {}
    else:
        image_name = env.name
        image_repo = env.repo
        image_tag = env.tag
        json = {
            'image_name': image_name,
            'image_repo': image_repo,
            'image_tag': image_tag
        }
        return json

def getTestJobJson(testjob):
    resp = ""
    jobname = testjob.name
    project = testjob.project.name if testjob.project != None else ''
    testplans = testjob.testplan.all()
    resp_testplans = []
    buildplan = testjob.buildplan
    env = testjob.env
    env_json = getEnvJson(env)
    run_mode = testjob.runMode.name if testjob.runMode != None else ''

    if len(testplans) != 0:
        for testplan in testplans:
            resp_testplan = getTestPlanJson(testplan)
            resp_testplans.append(resp_testplan)
    resp_buildplan = getBuildPlanJson(buildplan) if buildplan != None else ''
    sub_jobs = testjob.testjob_set.all()
    sub_job_list = []
    if sub_jobs.count() == 0:
        resp = {
            'name': jobname,
            'project': project,
            'env': env_json,
            'run_mode': run_mode,
            'buildplan': resp_buildplan,
            'testplans': resp_testplans
        }
    else:
        for sub_job in sub_jobs:
            resp_testjob = getTestJobJson(sub_job)
            sub_job_list.append(resp_testjob)
        resp = {
            'name': jobname,
            'project': project,
            'env': env_json,
            'run_mode': run_mode,
            'buildplan': resp_buildplan,
            'testplans': resp_testplans,
            'sub_jobs': sub_job_list
        }
    return resp

def GenTestPlan(request, plan_name):
    print(plan_name)
    try:
        testplan = TestPlan.objects.get(name=plan_name)
        data = getTestPlanJson(testplan)
        statuscode = "200"
    except TestPlan.DoesNotExist:
        data = ""
        statuscode = "404"
    resp = {
        'statuscode': statuscode,
        'data': data
    }
    return JsonResponse(resp)

def GenBuildPlan(request, plan_name):
    print(plan_name)
    try:
        testplan = BuildPlan.objects.get(name=plan_name)
        data = getBuildPlanJson(testplan)
        statuscode = "200"
    except BuildPlan.DoesNotExist:
        data = ""
        statuscode = "404"
    resp = {
        'statuscode': statuscode,
        'data': data
    }
    return JsonResponse(resp)

def GenTestJob(request, job_name):
    print(job_name)
    try:
        testjob = TestJob.objects.get(name=job_name)
        data = getTestJobJson(testjob)
        statuscode = "200"
    except TestJob.DoesNotExist:
        data = ""
        statuscode = "404"
    resp = {
        'statuscode': statuscode,
        'data': data
    }
    return JsonResponse(resp)

def GenWholeCaseList(request):
    try:
        testcases = TestCase.objects.filter(is_delete=False)
        blocks = []
        testcaselist = []
        for testcase in testcases:
            testcase_name = testcase.name
            testcase_block = testcase.testcmd.block.name
            testcase_cmd = testcase.testcmd.cmdline
            testcase_tolerance = testcase.tolerance
            testcase_timeout = testcase.timeout
            testcase_estimation = testcase.exectime
            testcase_configs = testcase.config.config.all()
            config_list = []
            if testcase_configs:
                for config in testcase_configs:
                    config_type = config.configtype.name
                    is_cmd = False
                    if config_type.lower() == "cmdline":
                        is_cmd = True
                    config_json = parseConfigs(config.content, is_cmd)
                    config_list.append({config_type : config_json})
            blocks.append(testcase_block)
            testcaselist.append(
                {
                    'name': testcase_name,
                    'block': testcase_block,
                    'cmdline': testcase_cmd,
                    'tolerance': testcase_tolerance,
                    'timeout': testcase_timeout,
                    'estimation': testcase_estimation,
                    'configs': config_list
                }
            )
        blocks = list(set(blocks))
        data = {
            'blocks': blocks,
            'caselist': testcaselist
        }
        statuscode = "200"
    except TestCase.DoesNotExist:
        data = ""
        statuscode = "404"
    resp = {
        'statuscode': statuscode,
        'data': data
    }
    return JsonResponse(resp)

#for demo purpose
def GenDemoCaseList(request):
    try:
        testcases = TestCase.objects.filter(is_delete=False, name__contains='demo')
        blocks = []
        testcaselist = []
        for testcase in testcases:
            testcase_name = testcase.name
            testcase_block = testcase.testcmd.block.name
            testcase_cmd = testcase.testcmd.cmdline
            testcase_tolerance = testcase.tolerance
            testcase_timeout = testcase.timeout
            testcase_estimation = testcase.exectime
            testcase_configs = testcase.config.config.all()
            config_list = []
            if testcase_configs:
                for config in testcase_configs:
                    config_type = config.configtype.name
                    is_cmd = False
                    if config_type.lower() == "cmdline":
                        is_cmd = True
                    config_json = parseConfigs(config.content, is_cmd)
                    config_list.append({config_type : config_json})
            blocks.append(testcase_block)
            testcaselist.append(
                {
                    'name': testcase_name,
                    'block': testcase_block,
                    'cmdline': testcase_cmd,
                    'tolerance': testcase_tolerance,
                    'timeout': testcase_timeout,
                    'estimation': testcase_estimation,
                    'configs': config_list
                }
            )
        blocks = list(set(blocks))
        data = {
            'blocks': blocks,
            'caselist': testcaselist
        }
        statuscode = "200"
    except TestCase.DoesNotExist:
        data = ""
        statuscode = "404"
    resp = {
        'statuscode': statuscode,
        'data': data
    }
    return JsonResponse(resp)
