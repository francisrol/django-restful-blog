/**
 * Created by whiteHouse on 17/7/8.
 */

<!-- lang: js -->
/**
 * 替换所有匹配exp的字符串为指定字符串
 * @param exp 被替换部分的正则
 * @param newStr 替换成的字符串
 */
String.prototype.replaceAll = function (exp, newStr) {
    return this.replace(new RegExp(exp, "gm"), newStr);
};

/**
 * 原型：字符串格式化
 * @param args 格式化参数值
 */
String.prototype.format = function(args) {
    var result = this;
    if (arguments.length < 1) {
        return result;
    }

    var data = arguments; // 如果模板参数是数组
    if (arguments.length == 1 && typeof (args) == "object") {
        // 如果模板参数是对象
        data = args;
    }
    for ( var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replaceAll("\\{" + key + "\\}", value);
        }
    }
    return result;
}

var list_template = '<div class="blog-post"><h2><a href="/detail/{4}/" target="_blank" >{0}</a></h2><h4>{1}</h4><div><em>关键字：{2}</em></div>{3}<a href="/detail/{4}/" target="_blank" class="btn btn-default">Read More <i class="fa fa-angle-right"></i></a></div>';

var detail_template = '<div class="blog-post"><h2>{0}</h2><div class="clearfix"><h4 class="pull-left">{1}</h4><div class="pull-right"><em>关键字：{2}</em></div></div><blockquote >{3}</blockquote>{4}</div>';

var option_template = '<option>{0}</option>';

var page_template = '<li><a href="{0}">{1}</a></li>';

var active_page_template = '<li class="active"><a>{0}</a></li>';

var category_template = '<li class="list-group-item btn btn-default"><a href="/category/{0}/" class="list-group-item">{1}</a></li>';

var family_template = '<li><a href="/family/{0}/">{1}</a></li>';

var edit_template = '<a href="{0}" class="btn btn-default btn-xs" id="{1}"><i class="fa fa-{2} fa-1x"></i></a>'

var parmas = {
        "url": "/",
        "type": "GET",
        "contentType": "application/json",
        "success": function(data){
        }
    };


function sendBlogData(sendData, url, method, redirectUrl){
    /*
    发送数据到服务器保存
     */
    parmas.url = '/api/blog' + url;
    parmas.type = method;
    parmas.data = sendData;
    parmas.success = function (data) {
        location.assign(redirectUrl);
    }
    $.ajax(parmas);
}

function clickSubmit(url, method, redirectUrl){
    /*
    点击保存按钮
     */
    $('#blog-form').submit(function () {
        var title = $("#title").val();
        var summary = $("#summary").val();
        var content = $("#content").val();
        var keyWords = $("#keyWords").val();
        var category = $('#category').val();
        var data = {
            "title" : title,
            "summary" : summary,
            "content" : content,
            "keyWords" : keyWords,
            "category" : category
        }
        data = JSON.stringify(data);
        sendBlogData(data, url, method, redirectUrl);
        return false;
    })
}

function searchStringToObj() {
    // 获取URL中?及其之后的字符
    var str = location.search;
     var obj = new Object();
    if (str == ""){
        return obj
    }
    str = str.substring(1,str.length); // 去掉？

    // 以&分隔字符串，获得类似name=xiaoli这样的元素数组
    var arr = str.split("&");

    // 将每一个数组元素以=分隔并赋给obj对象
    for(var i = 0; i < arr.length; i++) {
        var tmp_arr = arr[i].split("=");
        obj[decodeURIComponent(tmp_arr[0])] = decodeURIComponent(tmp_arr[1]);
    }
    return obj
}

function searchObjToString(obj){
    /*
    查询对象转字符串
     */
    var str = '';
    for(var key in obj){
        str += key+'=';
        str += obj[key].toString();
        str += "&";
    }
    return str.slice(0,-1);
}

function createPageHtml(pageObj){
    /*
    生成分页的HTML
     */
    var pageHtml = '';
    var path_url = location.pathname;
    var searchObj = searchStringToObj();
    // 判断是否有上一页
    if (pageObj.has_previous){
        searchObj.page = parseInt(pageObj.page_index)-1;
        $('.page_previous a').prop('href', path_url + '?' + searchObjToString(searchObj));
    }else{
        $('.page_previous').addClass("disabled");
        $(".page_previous a").removeAttr("href");
    }
    // 判断是否有下一页
    if (pageObj.has_next){
        searchObj.page = parseInt(pageObj.page_index)+1;
        $('.page_next a').prop('href', path_url + '?' + searchObjToString(searchObj));
    }else{
        $('.page_next').addClass("disabled");
        $(".page_next a").removeAttr("href");
    }
    for(var i=0;i<parseInt(pageObj.page_numbers); i++){
        searchObj.page = i+1;
        var html = '';
        if (i+1==parseInt(pageObj.page_index)){
            html = active_page_template.format(i+1);
        }else {
            html = page_template.format(path_url + '?' + searchObjToString(searchObj), i + 1);
        }
        pageHtml += html;
    }
    $(".pagination li").eq(0).after(pageHtml);  // 将生成的html加载到页面

}

function getListData(){
    /*
    首页调用：
    获取博客列表
     */
    var search_parmas = searchStringToObj();
    parmas.url = '/api/blog/list' + decodeURIComponent(location.pathname);
    parmas.data = search_parmas;
    parmas.type = 'GET';
    parmas.success = function (data) {
        data = JSON.parse(data);
        createPageHtml(data);
        var object_list = data.object_list;
        var html = '';
        for(var i=0;i<object_list.length; i++){
            var blog = object_list[i];
            var blogHtml = list_template.format(blog.title, blog.createdTime, blog.keyWords, blog.summary, blog.slug);
            html += blogHtml;
        };
        $('.blog-list').html(html);
    };
    $.ajax(parmas)
}

function getBlogDetail(){
    /*
    博客详情页调用
    获取某篇文章详情
     */
    var url = location.pathname;
    parmas.url = '/api/blog' + url;
    parmas.type = 'GET';
    parmas.success = function(data){
        data = JSON.parse(data);
        var blog = data[0];
        var html = detail_template.format(blog.title, blog.createdTime, blog.keyWords, blog.summary, blog.content);
        $('.blog-detail').html(html);
        $('pre code').each(function(i, block) {
            hljs.highlightBlock(block);
          });
        var editBtn = edit_template.format('/edit/'+blog.slug+'/', 'edit', 'edit');
        var deleteBtn = edit_template.format('/delete/'+blog.slug+'/', 'remove', 'remove');
        $("#add").after(editBtn+deleteBtn);
    };
    $.ajax(parmas)
}

function getBlogEdit(){
    /*
    博客编辑页调用
    获取某篇文章详情
     */
    var url = location.pathname;
    parmas.url = '/api/blog/detail/' + url.split('/')[2] + '/';
    parmas.type = 'GET';
    parmas.success = function(data){
        data = JSON.parse(data);
        var blog = data[0];
        $("#title").val(blog.title);
        $("#summary").val(blog.summary);
        $("#content").val(blog.content);
        $("#keyWords").val(blog.keyWords);
        $('#category').val(blog.category);
        $('#family').val(blog.family);
        clickSubmit(url, 'PUT', url);
    };
    $.ajax(parmas);
}

function getCreateBlog(){
    /*
    创建博客
     */
    var url = location.pathname;
    var method = 'POST';
    var redirectUrl = '/';
    clickSubmit(url, method, redirectUrl);
}

function showCategory(){
    /*
    请求博客分类，并显示到页面
     */
    $.ajax({
        "url": "/api/blog/categories/",
        "type" : 'GET',
        "success" : function(data){
            data = JSON.parse(data);
            var categoryHtml = '';
            for(var i=0;i<data.length; i++){
                var html = category_template.format(data[i][1], data[i][1]);
                categoryHtml += html;
            }
            $(".list-group li").after(categoryHtml);
            if (location.pathname.slice(0,5) == '/edit' | location.pathname.slice(0,8) == '/create/'){
                var html = '';
                for(var i=0;i<data.length; i++){
                    var category = data[i];
                    var oneHtml = option_template.format(category[1]);
                    html += oneHtml;
                }
                $('#category').html(html);
            }
        }
    });
}

function showFamily(){
    /*
    请求博客分类，并显示到页面
     */
    $.ajax({
        "url": "/api/blog/allFamily/",
        "type" : 'GET',
        "success" : function(data){
            data = JSON.parse(data);
            var beforeHtml = '';
            for(var i=0;i<data.length-1; i++){
                var html = family_template.format(data[i][1],data[i][1]);
                beforeHtml += html;
            }
            var afterHtml = family_template.format(data[data.length-1][1], data[data.length-1][1]);
            $(".divider").before(beforeHtml);
            $(".divider").after(afterHtml);
            if (location.pathname.slice(0,5) == '/edit' | location.pathname.slice(0,8) == '/create/'){
                var html = '';
                for(var i=0;i<data.length; i++){
                    var family = data[i];
                    var oneHtml = option_template.format(family[1]);
                    html += oneHtml;
                }
                console.log(html);
                $('#family').html(html);
            }
        }
    });
}
