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

    testCases = TestCase.objects.all()
    for testCase in testCases:
        if '[' in testCase.name:
            testCase.name = testCase.name.replace('[', '_')
            testCase.name = testCase.name.replace(']', '')
            testCase.save()



if __name__ == "__main__":
    main()
    print('Done!')