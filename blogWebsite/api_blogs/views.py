# encoding=utf-8
import json

from django.http import HttpResponse
from django.core import serializers
from django.conf import settings
from django.core.paginator import Paginator
from api_blogs.models import BlogModel
from api_blogs.serializers import PageOrQuerySetSerializer
from api_blogs.permissions import permission
import markdown

# 将中文转换为拼音，并用-链接在一起
# 用作url匹配
from uuslug import slugify

# Create your views here.
# 博客的增删改查
@permission.allowedMethod(["GET"])
def blogList(request, category=None, family=None):
    '''
    客户端使用的应当是GET请求
    返回博客列表
    :param request:django自动传入
    :return: HttpResponse对象
    '''
    # # 判断方法是不是GET方法，如果不是，那么返回405（请求行中指定的请求方法不能被用于请求相应的资源）
    # if request.method != 'GET':
    #     # json.dumps方法把python的数据类型转换为json格式数据
    #     data = json.dumps({"message": "only allowed GET method"})
    #     return HttpResponse(data, status=405)

    allBlogObj = BlogModel.objects.all().order_by('-createdTime')

    # ----分类----
    allBlogObj = allBlogObj.filter(category=category) if category else allBlogObj
    # ----分类----

    # ----系列----
    allBlogObj = allBlogObj.filter(family=family) if family else allBlogObj
    # ----系列----

    # ----排序----
    orderBy = request.GET.get('orderby', '')
    allBlogObj = allBlogObj.order_by(orderBy) if orderBy else allBlogObj
    # ----排序----

    # ----分页----
    allPages = Paginator(allBlogObj, 2)
    page = request.GET.get("page", 1)    # 从查询字符串获取page属性
    try:
        page = int(page)
        page = allPages.num_pages if page>allPages.num_pages else page
        page = page if page>0 else 1
    except Exception:
        page = 1
    pageData = allPages.page(page)
    # ----分页----

    # 因为allBlogObj是django的QuerySet对象
    # 所以需要使用from django.core import serializers
    # 把对象序列化为json格式数据
    # 在python中json格式的数据表现形式就是一个字符串
    # pageData = serializers.serialize('json', pageData)
    pageData = PageOrQuerySetSerializer().serialize(pageData)
    pageData = json.dumps(pageData)
    return HttpResponse(pageData)

@permission.allowedMethod(["GET"])
def blogDetail(request, slug):
    '''
    客户端使用的应当是GET请求
    返回单篇博客文章
    :param request:django自动传入
    :param slug: 用于匹配url
    :return:HttpResponse对象
    '''
    # # 判断方法是不是GET方法，如果不是，那么返回405（请求行中指定的请求方法不能被用于请求相应的资源）
    # if request.method != 'GET':
    #     # json.dumps方法把python的数据类型转换为json格式数据
    #     data = json.dumps({"message": "only allowed GET method"})
    #     return HttpResponse(data, status=405)
    oneBlogObj = BlogModel.objects.filter(slug=slugify(slug))
    # 把QuerySet对象对象序列化为json格式数据
    # oneBlogObj = serializers.serialize('json', oneBlogObj)
    oneBlogObj = json.dumps(PageOrQuerySetSerializer().serialize(oneBlogObj))
    if not oneBlogObj:
        # 如果不存在，那么返回404
        data = json.dumps({"message":"'您访问的内容不存在'"})
        return HttpResponse(data, status=404)

    return HttpResponse(oneBlogObj)


@permission.allowedMethod(["POST"])
@permission.hasEditPermission
def createBlog(request):
    '''
    客户端使用的应当是POST请求，携带请求数据
    创建博客
    :param request: django自动传入
    :return: HttpResponse对象
    '''
    # # 判断方法是不是POST方法，如果不是，那么返回405（请求行中指定的请求方法不能被用于请求相应的资源）
    # if request.method != 'POST':
    #     # json.dumps方法把python的数据类型转换为json格式数据
    #     data = json.dumps({"message": "only allowed POST method"})
    #     return HttpResponse(data, status=405)

    # 获取来自客户端POST提交的数据
    # 如果以表单形式提交的数据django会帮我们放在request.POST里
    # postData = request.POST

    # 如果非表单提交的数据，比如json
    # 只能通过request.body取出http请求中的原始数据
    # 因为我们规定客户端发出的数据形式应当是json
    postData = request.body
    print(postData)
    # 所以我们拿到json数据后
    # 在python中json就是一串字符串
    # 所以需要使用json.loads方法，把它转换成python的内置数据结构，比如列表、字典
    # 如果数据是'[{"key": "value"}]'  ==>  那么将转出列表[{'key':'value'}]
    # 如果数据是'{"key": "value"}'  ==>  那么将转出字典{'key':'value'}
    postData = json.loads(postData)

    # 获取属性
    title = postData.get('title', None)
    summary = postData.get('summary', None)
    content = postData.get('content', None)
    keyWords = postData.get('keyWords', '')
    category = postData.get('category', '')

    # 过滤数据，判断数据是否为空
    if not title or not summary or not content:
        # 如果任何一项为空，那么我们返回400状态码
        # 表明请求参数有问题，服务器不接受
        return HttpResponse(status=400)
    # 如果数据都不为空，那么创建新对象，保存数据
    newblog = BlogModel()
    newblog.title = title
    newblog.summary = markdown.markdown(summary, ["codehilite"])
    newblog.content = markdown.markdown(content, ["codehilite"])
    if keyWords:
        newblog.keyWords = keyWords
    if category:
        newblog.category = category
    newblog.save()
    # 把QuerySet对象序列化为json格式数据
    retblog = serializers.serialize('json', [newblog])
    # 201状态码，表明请求创建的资源已经成功创建
    return HttpResponse(retblog, status=201)

@permission.allowedMethod(["PUT"])
@permission.hasEditPermission
def editBlog(request, slug):
    '''
    客户端使用的应当是PUT请求
    更新博客
    :param request: django自动传入
    :param slug: 用于匹配url
    :return:HttpResponse对象
    '''
    # # 判断方法是不是PUT方法，如果不是，那么返回405（请求行中指定的请求方法不能被用于请求相应的资源）
    # if request.method != 'PUT':
    #     # json.dumps方法把python的数据类型转换为json格式数据
    #     data = json.dumps({"message": "only allowed PUT method"})
    #     return HttpResponse(data, status=405)

    # 从数据库取出主键为pk的博客，如果不存在，filter返回的[]
    blog = BlogModel.objects.filter(slug=slugify(slug))

    # 判断主键为pk的博客是否存在
    if not blog:
        # 如果不存在，那么返回404
        data = json.dumps({"message":"'您访问的内容不存在'"})
        return HttpResponse(data, status=404)
    # 如果存在，那么开始接受PUT提交的json数据：
    # 获取来自客户端PUT提交的数据,body里存储的是http请求的body部分的实体内容
    # 是原始的json格式数据，因此需要使用json.loads方法转换成python的dict
    putData = request.body
    putData= json.loads(putData)

    title = putData.get('title', None)
    summary = putData.get('summary', None)
    content = putData.get('content', None)
    keyWords = putData.get('keyWords', '')
    category = putData.get('category', '')

    # 过滤数据，判断数据是否为空，如果为空就不更新数据
    # 因为使用的filter方法，返回的是列表，所以需要取出下标0的元素才是BlogModel对象
    blog = blog[0]
    if title:
        blog.title = title
    if summary:
        blog.summary = summary
    if content:
        blog.content = content
    if keyWords:
        blog.keyWords = keyWords
    if category:
        blog.category = category
    blog.save()
    # 把QuerySet对象序列化为json格式数据
    retblog = serializers.serialize('json', [blog])
    return HttpResponse(retblog, status=200)

@permission.allowedMethod(["DELETE"])
@permission.hasEditPermission
def deleteBlog(request, slug):
    '''
    客户端使用的应当是DELETE方法
    删除博客
    :param request: django自动传入
    :param slug: 用于匹配url
    :return:HttpResponse对象
    '''
    # # 判断方法是不是DELETE方法，如果不是，那么返回405（请求行中指定的请求方法不能被用于请求相应的资源）
    # if request.method != 'DELETE':
    #     # json.dumps方法把python的数据类型转换为json格式数据
    #     data = json.dumps({"message": "only allowed DELETE method"})
    #     return HttpResponse(data, status=405)

    # 从数据库取出主键为pk的博客，如果不存在，filter返回的[]
    blog = BlogModel.objects.filter(slug=slugify(slug))
    # 判断主键为pk的博客是否存在
    if not blog:
        # 如果不存在，那么返回404
        data = json.dumps({"message":"'您访问的内容不存在'"})
        return HttpResponse(data, status=404)
    # 如果存在那么执行删除操作
    blog[0].delete()
    return HttpResponse('删除成功', status=200)

@permission.allowedMethod(["GET"])
def getCategories(request):
    '''
    获取分类信息
    :param request:
    :return:
    '''
    categories = settings.CATEGORIES
    retData = json.dumps(categories)
    return HttpResponse(retData)

@permission.allowedMethod(["GET"])
def getBlogFamily(request):
    '''
    获取系列信息
    :param request:
    :return:
    '''
    family = settings.BLOGFAMILY
    retData = json.dumps(family)
    return HttpResponse(retData)

@permission.allowedMethod(["POST"])
def getPermission(request, ):
    '''
    设置权限
    保存到session中
    过期时间在settings文件中设置
    :param request:
    :return:
    '''
    if request.method == 'POST':
        loginName = request.POST.get('loginName', '')
        loginPasswd = request.POST.get('loginPasswd', '')
        if permission.getPermissionCode(loginName, loginPasswd):
            # 设置一定时间的权限，保存到sessions
            request.session['permissionCodeName'] = loginName
            request.session['permissionCodePasswd'] = loginPasswd
            return HttpResponse(status=204)
        return HttpResponse(status=403)
    else:
        return HttpResponse(status=405)