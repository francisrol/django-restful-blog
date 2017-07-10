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

var list_template = '<div class="blog-post"><h2><a href="/detail/{4}/" target="_blank" >{0}</a></h2><h4>{1}</h4><div><em>关键字：{2}</em></div>{3}<a href="/detail/{4}/" target="_blank" class="btn btn-default btn-lg">Read More <i class="fa fa-angle-right"></i></a></div>';

var detail_template = '<div class="blog-post"><h2>{0}</h2><div class="clearfix"><h4 class="pull-left">{1}</h4><div class="pull-right"><em>关键字：{2}</em></div></div><blockquote >{3}</blockquote>{4}</div>';

var radio_template = '<label class="radio-inline"><input type="radio" name="category" value="{0}"> {1}</label>';

var parmas = {
        "url": "/",
        "type": "GET",
        "contentType": "application/json",
        "success": function(data){
        }
    };

function getListData(){
    /*
    首页调用：
    获取博客列表
     */
    parmas.url = '/api/blog/list/';
    parmas.type = 'GET';
    parmas.success = function (data) {
        data = JSON.parse(data);
        var html = '';
        for(var i=0;i<data.length; i++){
            var blog = data[i].fields;
            console.log(blog.title);
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
    url = location.pathname;
    parmas.url = '/api/blog' + url;
    parmas.type = 'GET';
    parmas.success = function(data){
        data = JSON.parse(data);
        var blog = data[0].fields;
        console.log(blog.title);
        var html = detail_template.format(blog.title, blog.createdTime, blog.keyWords, blog.summary, blog.content);
        $('.blog-detail').html(html);
    };
    $.ajax(parmas)
}

function getCategories(){
    /*
    获取分类信息
     */
    parmas2 = parmas;
    parmas2.url = '/api/blog/categories/';
    parmas2.type = 'GET';
    parmas2.success = function(data){
        var html = '';
        for(var i=0;i<data.length; i++){
            var category = data[i]
            var oneHtml = radio_template.format(category[1], category[1]);
            html += oneHtml;
        }
        $('#radio-category').html(html);
    }
    $.ajax(parmas);
}

function getBlogEdit(){
    /*
    博客编辑页调用
    获取某篇文章详情
     */
    url = location.pathname;
    parmas.url = '/api/blog/detail/' + url.split('/')[2] + '/';
    parmas.type = 'GET';
    console.log(url);
    parmas.success = function(data){
        data = JSON.parse(data);
        var blog = data[0].fields;
        $("#title").val(blog.title);
        $("#summary").val(blog.summary);
        $("#content").val(blog.content);
        $("#keyWords").val(blog.keyWords);
    };
    $.ajax(parmas);
}

// function deleteBlog(url, params){
//
// }

// function editBlog(url, params){
//
// }

