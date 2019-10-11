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

    ConfigPlanList = []
    namelist = []
    data = csv.reader(open('config_plan.csv', 'r', encoding="utf-8-sig"))

    for line in data:
        parts = line
        name = parts[0]
        desc = parts[2]
        configPlans = ConfigPlan.objects.filter(name=name)
        if len(configPlans) == 0:
            configPlan = ConfigPlan.objects.create(name=name, desc=desc, is_delete=False)
        else:
            configPlan = configPlans[0]
        config_options = parts[1]
        config_options_list = config_options.split(' ')
        for config_option in config_options_list:
            configOptions = ConfigDetail.objects.filter(name=config_option)
            if len(configOptions) != 0:
                configPlan.config.add(configOptions[0])
            configPlan.save()

        print("name: {0}    config_options: {1}".format(name, config_options))



if __name__ == "__main__":
    main()
    print('Done!')