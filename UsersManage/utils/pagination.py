import copy
from django.http.request import QueryDict
from django.utils.safestring import mark_safe

"""
自定义的分页组件，以后如果想要使用这个分页组件，你需要做如下几件事：

在视图函数中：
    def pretty_list(request):

        # 1.根据自己的情况去筛选自己的数据
        queryset = models.PrettyNum.objects.all()

        # 2.实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html()       # 生成页码
        }
        return render(request, 'pretty_list.html', context)

在HTML页面中

    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>

"""


class Pagination(object):

    def __init__(self, request, queryset, per_page=10, page_param='page', step=3):
        """
        :param request: 请求对象
        :param queryset: 要分页数据
        :param per_page: 每页显示的数量
        :param page_param: 在url中传递的参数名称：/list/?page=12
        :param step: 显示当前页的前几页
        """

        query_dict = copy.deepcopy(request.GET)  # 拷贝一份GET请求参数
        query_dict._mutable = True  # 允许请求参数被修改
        self.query_dict = query_dict

        self.per_page = per_page
        self.page_param = page_param
        self.step = step

        # 计算当前页数
        page = request.GET.get(page_param, "1")  # 获取当前页数，默认为1
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page

        # 计算总页数
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, self.per_page)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

        # 计算当前页码的前step页，后step页
        self.start_page = self.page - self.step
        if self.start_page < 1:
            self.start_page = 1
        self.end_page = self.page + self.step
        if self.end_page > self.total_page_count:
            self.end_page = self.total_page_count
        # print(self.start_page, self.end_page)

        # 计算要展示数据的index
        self.start = (self.page - 1) * self.per_page
        self.end = self.page * self.per_page
        # print(self.start, self.end)

        # 截取当前页要显示的数据
        self.page_queryset = queryset[self.start:self.end]

    def html(self):
        page_str_list = []
        # page_str_list = """
        #     <li><a href="#">1</a></li>
        #     <li><a href="#">2</a></li>
        #     <li><a href="#">3</a></li>
        #     <li><a href="#">4</a></li>
        #     <li><a href="#">5</a></li>"""

        # 首页
        if self.total_page_count > 1:
            self.query_dict.setlist(self.page_param, [1])
            page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 显示前一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])  # 前一页
            page_str_list.append("""
                <li>
                  <a href="?{}" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                  </a>
                </li>""".format(self.query_dict.urlencode()))

        # 所有页码
        for i in range(self.start_page, self.end_page + 1):
            self.query_dict.setlist(self.page_param, [i])  # 将参数变成字典
            if i == self.page:
                page_str_list.append('<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i))
                continue
            page_str_list.append('<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i))
            # print(self.query_dict.urlencode())  # q=1&page=1

        # 显示后一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])  # 后一页
            page_str_list.append("""
                <li>
                  <a href="?{}" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                  </a>
                </li>""".format(self.query_dict.urlencode()))

        # 尾页
        if self.total_page_count > 1:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        page_string = mark_safe("".join(page_str_list))
        return page_string
