var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var house_data_querying = true;   // 是否正在向后台获取数据

// 首页分类切换
$(function () {
    //调用updateNewsData()显示数据
    updateNewsData()
    // 首页分类切换
    $('.menu li').click(function () {       //新闻栏的点击事件
        var clickCid = $(this).attr('data-cid')   //获取当前用户点击的新闻类型id
        $('.menu li').each(function () {         //给每个li都加上删除active样式的函数
            $(this).removeClass('active')
        })
        $(this).addClass('active')         //给当前这个新闻类型加上active
        if (clickCid != currentCid) {          //如果这个用户点击的类型id不是默认/或者上一次点击的id
            // 记录当前分类id
            currentCid = clickCid             //更新clickCid值
            // 重置分页参数
            cur_page = 1
            total_page = 1
            updateNewsData()               //更新类型值后，在此调用该函数到后端请求数据
        }
    })

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100) {
            // TODO 判断页数，去更新新闻数据
            if (!house_data_querying){      //如果这个标志位为false

                house_data_querying = true     //置为true(正在向后台获取数据)

                if (cur_page < total_page){    //如果这个当前页小于总页数

                    updateNewsData()

                }else{

                    house_data_querying = false     //没数据的话加将标志位制为false，不请求了
                }
            }
        }
    })
})

function updateNewsData() {
    // TODO 更新新闻数据

    var params = {
        'page':cur_page,
        'per_page':10,
        'cid':currentCid
    }

    $.get('/newslist',params,function (resp) {
        //将加载标志位制为false
        house_data_querying = false

        if (resp){
            //设置totol_page
            total_page = resp.total_page   //服务器转过来的值

            //当要显示第一页时，也就是第一次访问时，清空ul中数据
            if (cur_page == 1) {
                //清空原来数据
                $(".list_con").html("")
            }
            cur_page++;   //没请求一次，当前页加一

            //显示数据
            for(var i=0;i < resp.news_list.length;i++){
                //获取单个新闻信息
                var news = resp.news_list[i]
                //拼接新闻内容
                var content = '<li>'
                content+='<a href="#" class="news_pic fl"><img src="' + news.index_image_url + '?imageView2/1/w/170/h/170"></a>'
                content+='<a href="#" class="news_title fl">'+news.title+'</a>'
                content+='<a href="#" class="news_detail fl">'+news.digest+'</a>\n'
                content+='<div class="author_info fl">\n' +
                    '                    <div class="author fl">\n' +
                    // '                        <img src="../../static/news/images/person.png" alt="author">\n' +
                    '                        <a href="#">来源：'+news.source+'</a>\n' +
                    '                    </div>\n' +
                    '                    <div class="time fl">'+news.create_time+'</div>\n' +
                    '                </div>'
                content+='</li>'
                $('.list_con').append(content)
            }
        }
    })
}
