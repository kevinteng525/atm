import os
import django
import csv
import collections
from django.db.models import Q

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

        if dl_framwork == "tensorflow":
            csv_file = 'TF_CASE_GEN_TABLE.csv'
        else:
            csv_file = 'MXNET_CASE_GEN_TABLE.csv'

        data = csv.reader(open(csv_file, 'r'))
        rm_count = 0
        for line in data:
            cmdline_name = line[4]
            case_name = line[1]
            unsupported = line[16]
            case_failure = line[17]
            source = line[19]
            coremask = line[20]
            timeout = line[22]
            lmcopy = line[25]
            compression = line[26]
            comment = line[27]
            parameters = line[28]

            # if tolerance == 'N/A':
            #     tolerance = 0
            # elif tolerance == 'inf':
            #     tolerance = 65536
            # elif tolerance == '1.98E+37' or tolerance == '9.63E+27':
            #     tolerance = 65536
            # elif tolerance == '2.0f':
            #     tolerance = 2
            # else:
            #     tolerance = int(tolerance)
            branch = line[18]
            if branch == 'master':
                continue

            if coremask == 'N/A' or coremask == '1':
                coremask = 'N/A-1'

            # remove unsupported test cases from test plan
            if unsupported == "1" or case_failure == "1" or parameters == "101":
                # print(case_name)
                testCases = TestCase.objects.filter(Q(name=case_name) | Q(name=case_name + "_image_default") | Q(name=case_name + "_image_vops"))
                for testCase in testCases:
                    # print(testCase.name)
                    rm_count = rm_count + 1
                    testPlan.testcase.remove(testCase)
        print(rm_count)
        testPlan.save()


if __name__ == "__main__":
    main()
    print('Done!')