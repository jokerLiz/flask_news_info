#视图
from flask import render_template, current_app, session, request, jsonify

from . import index_blue      #导入__init__.py下的蓝图对象index_blue

#网页标签logo
from ... import constants
from ...models import User, News, Category  # 用户表
from ...utils.response_code import RET


@index_blue.route('/favicon.ico')
def get_web_logo():
    return current_app.send_static_file('news/favicon.ico')

#首页
@index_blue.route('/')
def index():
    '''首页显示'''

    #通过session获取当前的用户id
    user_id = session.get('user_id')

    user = None
    #通过id查询用户的信息
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)


    '''新闻右侧排行'''
    news_list = []
    try:
        #根据点击数进行排序，并取前6个
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    #如果该列表存在，执行前边的语句，否则执行后边的语句
    for news in news_list if news_list else []:
        click_news_list.append(news.to_basic_dict())   #将每个news对象，转化为字典后，加到另一个列表中

    '''选则栏'''
    category = Category.query.all()        #查询所有的选项


    #传给前台的数据
    data = {
        "user_info": user.to_dict() if user else None,     #to_dict():将对象中的信息转换为字典类型
        "click_news_list":click_news_list,
        'category':category,
    }

    return render_template('news/index.html',data=data)


#新闻列表
@index_blue.route('/newslist')
def get_news_list():
    # 1.获取参数
    arg_list = request.args
    page = arg_list.get('page',1)       #page参数：第几页，默认为1
    per_page = arg_list.get('per_page',constants.HOME_PAGE_MAX_NEWS)  #一页多少数据

    # cid:新闻类别的编号
    category_id = arg_list.get('cid',1)


    # 2.校验参数
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.PARAMERR,errmsg = '参数错误')

    # 3.查询数据
    filters = []
    if category_id != "1":                     #id为1时，显示的时所有数据，即filter=[]
        filters.append(News.category_id == category_id)

    try:
        # 查询所有的数据并分页，返回一个paginate对象
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,per_page,False)
        # 通过paginate对象获取查询的数据
        items = paginate.items
        # 获取总页数
        total_page = paginate.pages
        # 当前页
        current_page = paginate.page
    except Exception as e:

        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='数据查询失败')
    news_list = []
    for news in items:
        news_list.append(news.to_basic_dict())

    return jsonify(errno=RET.OK, errmsg='OK',
                   #数据
                   total_page=total_page,      #总页数
                   current_page=current_page,    #当前页
                   news_list=news_list,         #新闻列表
                   cid = category_id        #新闻类型id
                   )


