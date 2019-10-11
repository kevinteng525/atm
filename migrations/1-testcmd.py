import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdj.settings")
django.setup()

def main():
    from TestModel.models import TestCmd
    from ConfigModel.models import Block
    from ConfigModel.models import Project
    from TestModel.models import TestType

    blocks = {
        'run_block_chub_test': 'chub',
        'run_block_matmul_test': 'matmul',
        'run_block_vop_test': 'vop',
        'run_block_convEw_test': 'convew',
        'run_block_cp_test': 'cp',
        'run_block_interp_test': 'interp',
        'run_block_lm_test': 'lm',
        'run_block_pbu_test': 'pbu',
        'run_block_random_test': 'cdu',
        'run_block_rbu_test': 'rbu',
        'run_block_roi_test': 'roi',
        'run_block_se_test': 'se',
        'run_top_npu_test': 'top',
        'run_infer_checkin_test': 'infer_checkin',
        'run_kaleido_network_checkin_test': 'kaleido_network',
        'run_kaleido_v2_checkin_test': 'kaleido_v2',
        'run_on_demand_test': 'on_demand',
        'run_ratelnn_checkin_test': 'ratelnn_checkin'
    }

    CmdList = []
    namelist = []
    data = csv.reader(open('TF_CASE_GEN_TABLE.csv', 'r'))

    for line in data:
        parts = line
        name = parts[4]
        cmdline = parts[8]
        block_name = blocks[parts[5]]
        branch = parts[18]
        if branch == 'master':
            continue
        if name in namelist:
            continue
        namelist.append(name)
        block = Block.objects.get(name = block_name)
        project = Project.objects.get(id=1)
        testtype = TestType.objects.get(id=1)
        # change priority from P1, P2, P3 to 1, 2, 3, and if N/A, then set to 2
        priority = parts[7] if parts[7]!='N/A' else 2
        if priority != 2:
            priority = int(priority[1:])
        # if is_checkin, then set priority to 1
        is_checkin = parts[15]
        if is_checkin == "1":
            priority = 0

        comment = parts[28]
        testCMD = TestCmd.objects.filter(name=name)
        if len(testCMD) == 0:
            print("name: {0}    cmdline: {1}    block: {2}     branch: {3}     priority: {4}".format(name, cmdline, block.name, branch, priority))
            CmdList.append(TestCmd(name=name, cmdline=cmdline, block=block, project=project, testtype=testtype, priority=priority, comment=comment))


    TestCmd.objects.bulk_create(CmdList)


if __name__ == "__main__":
    main()
    print('Done!')