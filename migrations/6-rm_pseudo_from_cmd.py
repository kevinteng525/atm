import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdj.settings")
django.setup()


def main():
    from TestModel.models import TestCmd, TestCase
    from ConfigModel.models import ConfigPlan
    from ConfigModel.models import Project
    from TestModel.models import TestType

    testCMDs = TestCmd.objects.all()
    for testCMD in testCMDs:
        cmdline = testCMD.cmdline
        print(cmdline)
        if "-r pseudo" in cmdline:
            new_cmdline = cmdline.replace(" -r pseudo", "")
            testCMD.cmdline = new_cmdline
            testCMD.save()



if __name__ == "__main__":
    main()
    print('Done!')