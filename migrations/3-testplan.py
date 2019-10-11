import os
import django
import csv
import collections

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdj.settings")
django.setup()

def main():
    from TestModel.models import TestPlan
    from TestModel.models import TestCase
    from ConfigModel.models import ConfigPlan
    from ConfigModel.models import ConfigDetail
    from ConfigModel.models import Project
    from ConfigModel.models import DLFramework
    from ConfigModel.models import Branch
    from TestModel.models import TestType

    TestPlanTuple = collections.namedtuple('testplan_name', ['project', 'dl_framework', 'branch', 'top_config', 'case_filter'])
    testplan_list = [
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='tf_fixdata',
                      case_filter='daily_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='tf_random_comp',
                      case_filter='daily_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='tf_random_nocomp',
                      case_filter='daily_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='tf_fixdata',
                      case_filter='checkin_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='tf_random_comp',
                      case_filter='checkin_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='tf_random_nocomp',
                      case_filter='checkin_test'),
        TestPlanTuple(project='v1', dl_framework='mxnet', branch='graph_opt', top_config='mxnet_fixdata',
                      case_filter='daily_test'),
        TestPlanTuple(project='v1', dl_framework='mxnet', branch='graph_opt', top_config='mxnet_random_comp',
                      case_filter='daily_test'),
        TestPlanTuple(project='v1', dl_framework='mxnet', branch='graph_opt', top_config='mxnet_random_nocomp',
                      case_filter='daily_test'),
        TestPlanTuple(project='v1', dl_framework='mxnet', branch='graph_opt', top_config='mxnet_fixdata',
                      case_filter='checkin_test'),
        TestPlanTuple(project='v1', dl_framework='mxnet', branch='graph_opt', top_config='mxnet_random_comp',
                      case_filter='checkin_test'),
        TestPlanTuple(project='v1', dl_framework='mxnet', branch='graph_opt', top_config='mxnet_random_nocomp',
                      case_filter='checkin_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='legacy_fixdata',
                      case_filter='daily_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='legacy_random_comp',
                      case_filter='daily_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='legacy_random_nocomp',
                      case_filter='daily_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='legacy_fixdata',
                      case_filter='checkin_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='legacy_random_comp',
                      case_filter='checkin_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='legacy_random_nocomp',
                      case_filter='checkin_test'),
        TestPlanTuple(project='v1', dl_framework='tensorflow', branch='graph_opt', top_config='dump_mode_tf',
                      case_filter='daily_test'),
        ]

    for testplan in testplan_list:
        project = testplan.project
        dl_framwork = testplan.dl_framework
        branch = testplan.branch
        top_config = testplan.top_config
        case_filter = testplan.case_filter
        testplan_name = "{0}_{1}_{2}_{3}".format(project, case_filter, top_config, branch)
        desc = "Project: {0}; Test Purpose: {1}; Framework: {2}; Branch: {3}; Config: {4}".format(project, case_filter, dl_framwork, branch, top_config)
        projectObject = Project.objects.get(name=project)
        dlframeworkObject = DLFramework.objects.get(name=dl_framwork)
        branchObject = Branch.objects.get(name=branch)
        configObject = ConfigPlan.objects.get(name=top_config)

        testPlans = TestPlan.objects.filter(name=testplan_name)
        if (len(testPlans) == 0):
            testPlan = TestPlan(name=testplan_name, desc=desc, project=projectObject, branch=branchObject, dlframework=dlframeworkObject,
                                config=configObject)
            testPlan.save()
        else:
            testPlan = testPlans[0]


        if case_filter == 'daily_test':
            testCaseList = TestCase.objects.filter()
        elif case_filter == 'checkin_test':
            testCaseList = TestCase.objects.filter(priority='0')
        else:
            testCaseList = TestCase.objects.all()
        for testCase in testCaseList:
            testcase_name = testCase.name
            if dl_framwork == 'tensorflow':
                if 'mxnet' in testcase_name:
                    pass
                    # testPlan.testcase.remove(testCase)
                else:
                    testPlan.testcase.add(testCase)
            elif dl_framwork == 'mxnet':
                if 'tf' in testcase_name:
                    pass
                    # testPlan.testcase.remove(testCase)
                else:
                    testPlan.testcase.add(testCase)
            else:
                pass

        testPlan.save()



if __name__ == "__main__":
    main()
    print('Done!')