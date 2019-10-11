from rest_framework import serializers
from TestModel import models as testmodels
from BuildModel import models as buildmodels
from ConfigModel import models as configmodels
from EnvModel import models as envmodels


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = configmodels.Project

class ProjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = configmodels.Branch

class DLFrameworkSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = configmodels.DLFramework

class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = configmodels.Block

class OSTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = configmodels.OSType

class ConfigTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = configmodels.ConfigType

class ConfigDetailSerializer(serializers.ModelSerializer):
    configtype = serializers.ReadOnlyField(source='configtype.name')

    class Meta:
        fields = '__all__'
        model = configmodels.ConfigDetail

class ConfigPlanSerializer(serializers.ModelSerializer):
    config = ConfigDetailSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = configmodels.ConfigPlan

class TestTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = testmodels.TestType

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = testmodels.Tag

class DockerImageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = envmodels.DockerImage

class TestCmdSerializer(serializers.ModelSerializer):
    # project = serializers.CharField(source='project.name', read_only=True)
    # project = serializers.PrimaryKeyRelatedField(many=False, queryset=testmodels.Project.objects.all())
    # testplan = serializers.PrimaryKeyRelatedField(many=True, queryset=testmodels.TestCase.testplan_set)
    block = serializers.ReadOnlyField(source='block.name')
    project = serializers.ReadOnlyField(source='project.name')
    testtype = serializers.ReadOnlyField(source='testtype.name')
    tag = TagSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = testmodels.TestCmd

class TestCaseSerializer(serializers.ModelSerializer):
    # project = serializers.CharField(source='project.name', read_only=True)
    # testcmd = serializers.PrimaryKeyRelatedField(many=False, queryset=testmodels.TestCmd.objects.all())
    # testplan = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    testcmd = serializers.ReadOnlyField(source='testcmd.cmdline')
    block = serializers.ReadOnlyField(source='testcmd.block.name')
    config = ConfigPlanSerializer()

    class Meta:
        # fields = ('id','name', 'testcmd','testplan',)
        fields = '__all__'
        model = testmodels.TestCase

class TestPlanSerializer(serializers.ModelSerializer):
    # project = serializers.CharField(source='project.name', read_only=True)
    # project = ProjectSerializer()
    project = serializers.ReadOnlyField(source='project.name')
    branch = serializers.ReadOnlyField(source='branch.name')
    dlframework = serializers.ReadOnlyField(source='dlframework.name')
    testcase = TestCaseSerializer(many=True)
    config = ConfigPlanSerializer()

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'project', 'testcase',)
        model = testmodels.TestPlan

class TestPlanUpdateSerializer(serializers.ModelSerializer):
    # project = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'project', 'testcase',)
        model = testmodels.TestPlan

class BuildProjectSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'project', 'testcase',)
        model = buildmodels.BuildProject

class BuildModeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'project', 'testcase',)
        model = buildmodels.BuildMode

class RunModeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'project', 'testcase',)
        model = buildmodels.RunMode

class BuildDetailSerializer(serializers.ModelSerializer):
    buildproject = serializers.ReadOnlyField(source='buildproject.name')
    buildmode = serializers.ReadOnlyField(source='buildmode.name')
    runmode = serializers.ReadOnlyField(source='runmode.name')

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'project', 'testcase',)
        model = buildmodels.BuildDetail

class BuildPlanSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.name')
    branch = serializers.ReadOnlyField(source='branch.name')
    ostype = serializers.ReadOnlyField(source='ostype.name')
    buildconfig = BuildDetailSerializer(many=True)

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'project', 'testcase',)
        model = buildmodels.BuildPlan

class TestJobSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.name')
    buildplan = BuildPlanSerializer()
    testplan = TestPlanSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = testmodels.TestJob




