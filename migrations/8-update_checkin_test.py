import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdj.settings")
django.setup()

def main():
    from TestModel.models import TestCmd
    from ConfigModel.models import ConfigPlan
    from ConfigModel.models import ConfigDetail
    from TestModel.models import TestType
    from TestModel.models import TestCase
    from TestModel.models import TestPlan

    CheckinFailureList = []
    namelist = []
    tf_checkin_test_plans = ["v1_checkin_test_tf_fixdata_graph_opt", "v1_checkin_test_tf_random_comp_graph_opt", "v1_checkin_test_tf_random_nocomp_graph_opt"]
    mxnet_checkin_test_plans = ["v1_checkin_test_mxnet_fixdata_graph_opt", "v1_checkin_test_mxnet_random_comp_graph_opt", "v1_checkin_test_mxnet_random_nocomp_graph_opt"]

    data = csv.reader(open('checkin_fail.csv', 'r', encoding="utf-8-sig"))

    for line in data:
        parts = line
        name = parts[0]
        if "_tensorflow" in name:
            case_name = name[:-11]
            testCases = TestCase.objects.filter(name=case_name)
            if(len(testCases)>0):
                for testplan_name in tf_checkin_test_plans:
                    testPlans = TestPlan.objects.filter(name=testplan_name)
                    testCases[0].testplan_set.remove(testPlans[0])
                    print("remove testplan {0} from case: {1}".format(testplan_name, case_name))
                testCases[0].save()
        elif "_mxnet" in name:
            case_name = name[:-6]
            testCases = TestCase.objects.filter(name=case_name)
            if (len(testCases) > 0):
                for testplan_name in mxnet_checkin_test_plans:
                    testPlans = TestPlan.objects.filter(name=testplan_name)
                    testCases[0].testplan_set.remove(testPlans[0])
                    print("remove testplan {0} from case: {1}".format(testplan_name, case_name))
                testCases[0].save()
        else:
            pass



if __name__ == "__main__":
    main()
    print('Done!')