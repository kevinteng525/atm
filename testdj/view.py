from django.http import HttpResponse
from django.shortcuts import render
from ConfigModel.models import Project
from django.shortcuts import render_to_response
from django.views.decorators import csrf

def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)

def search_post(request):
    ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['q']
    return render(request, "post.html", ctx)

def search_form(request):
    return render_to_response('search_form.html')


# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    if 'q' in request.GET:
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)

def testdb(request):
    test1 = Project(name='runoob')
    test1.save()
    return HttpResponse("<p>数据库添加成功！</p>")

def readdb(request):
    response = ""
    response1 = ""

    list = Project.objects.all()

    response2 = Project.objects.filter(id=1)
    response3 = Project.objects.get(id=1)

    list = Project.objects.order_by('name')
    list = list[0:2]

    #Test.objects.order_by('id')

    #Test.objects.filter(name="runoob").order_by("id")

    for var in list:
        response1 += str(var.id) + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")


def updatedb(request):
    # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
    test1 = Project.objects.get(id=1)
    test1.name = 'Google'
    test1.save()

    # 另外一种方式
    # Test.objects.filter(id=1).update(name='Google')

    # 修改所有的列
    # Test.objects.all().update(name='Google')

    return HttpResponse("<p>修改成功</p>")

def deletedb(request):
    # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
    test1 = Project.objects.get(id=3)
    test1.delete()

    # 另外一种方式
    # Test.objects.filter(id=1).update(name='Google')

    # 修改所有的列
    # Test.objects.all().update(name='Google')

    return HttpResponse("<p>删除成功</p>")