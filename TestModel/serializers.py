from rest_framework import serializers
from . import models


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','name', 'desc', 'is_delete',)
        model = models.Project

class ProjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

class TestStepSerializer(serializers.ModelSerializer):
    # project = serializers.CharField(source='project.name', read_only=True)
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all())
    # testplan = serializers.PrimaryKeyRelatedField(many=True, queryset=models.TestCase.testplan_set)

    class Meta:
        fields = ('id','name', 'cmdline', 'block', 'project', 'testtype',)
        model = models.TestCmd

class TestPlanSerializer(serializers.ModelSerializer):
    # project = serializers.CharField(source='project.name', read_only=True)
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all())
    testcase = serializers.PrimaryKeyRelatedField(many=True, queryset=models.TestCase.objects.all())

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'project', 'testcase',)
        model = models.TestPlan

class TestCaseSerializer(serializers.ModelSerializer):
    # project = serializers.CharField(source='project.name', read_only=True)
    testcmd = serializers.PrimaryKeyRelatedField(many=False, queryset=models.TestCmd.objects.all())
    # testplan = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        # fields = ('id','name', 'testcmd','testplan',)
        fields = '__all__'
        model = models.TestCase

