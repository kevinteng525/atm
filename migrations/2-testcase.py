import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdj.settings")
django.setup()

def handleParameters(parameters):
    if '15' in parameters:
        return '15'
    elif parameters == '0,1':
        return '0-1'
    elif '0+101,1+101' in parameters:
        return '0-1'
    else:
        return '0'

def main():
    from TestModel.models import TestCmd, TestCase
    from ConfigModel.models import ConfigPlan
    from ConfigModel.models import Project
    from TestModel.models import TestType

    case_config_mapping = {}
    mappings = csv.reader(open('case_config_mapping.csv', 'r', encoding="utf-8-sig"))
    for mapping in mappings:
        source = mapping[0]
        coremask = mapping[1]
        lmcopy = mapping[2]
        compression = mapping[3]
        parameters = mapping[4]
        configplan = mapping[5]
        key = "{0}_{1}_{2}_{3}_{4}".format(source, coremask.replace(' ', '-'), lmcopy, compression, parameters.replace(' ', '-'))
        case_config_mapping[key] = configplan.replace(' ', '-')

    CaseList = []
    namelist = []
    data = csv.reader(open('TF_CASE_GEN_TABLE.csv', 'r'))

    for line in data:
        cmdline_name = line[4]
        case_name = line[1]
        source = line[19]
        coremask = line[20]
        tolerance = line[21]
        timeout = line[22]
        lmcopy = line[25]
        compression = line[26]
        comment = line[27]
        parameters = line[28]

        if tolerance == 'N/A':
            tolerance = 0
        elif tolerance == 'inf':
            tolerance = 65536
        elif tolerance == '1.98E+37' or tolerance == '9.63E+27':
            tolerance = 65536
        elif tolerance == '2.0f':
            tolerance = 2
        else:
            tolerance = int(tolerance)
        branch = line[18]
        if branch == 'master':
            continue

        if coremask == 'N/A' or coremask == '1':
            coremask = 'N/A-1'

        parameters = handleParameters(parameters)

        key = "{0}_{1}_{2}_{3}_{4}".format(source, coremask, lmcopy, compression, parameters)
        configplans = case_config_mapping[key].split('-')

        for configplan in configplans:
            print("name: {0}  config_plan: {1}  testcmd: {2}".format(case_name.ljust(70), configplan.ljust(30), cmdline_name))
            testCmd = TestCmd.objects.get(name=cmdline_name)

            configPlan = ConfigPlan.objects.get(name=configplan)
            priority = testCmd.priority
            new_case_name = case_name
            if len(configplans) > 1:
                new_case_name = "{0}[{1}]".format(case_name, configplan)

            testCase = TestCase.objects.filter(name=new_case_name)
            if len(testCase) == 0:
                testCase = TestCase(name=new_case_name, desc=comment, testcmd=testCmd, config=configPlan, priority=priority, tolerance=tolerance, timeout=int(timeout), exectime=5)
                testCase.save()
        #
        # print("name: {0}    cmdline: {1}    block: {2}     branch: {3}     priority: {4}".format(name, cmdline, block.name, branch, priority))
        # CmdList.append(TestCmd(name=name, cmdline=cmdline, block=block, project=project, testtype=testtype, priority=priority, comment=comment))


    # TestCmd.objects.bulk_create(CmdList)


if __name__ == "__main__":
    main()
    print('Done!')