import os
from django.views.generic import View
from tools.decorator import allow_origin
from django.utils.decorators import method_decorator
from tools.pygal_process import create_wordcloud, create_pie, create_bar, jieba_top10_bar
# 导入分页模块
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
# 导入表
from .models import Computer
from tools.orm2json import object_to_json
# 导入haystack搜索框架SearchView
from haystack.views import SearchView
from django.http import JsonResponse

from tools.searchresult2json import sea_result2json

class ComputerView(View):
    @method_decorator(allow_origin)
    def get(self, request):
        # ?&brand=huawei&page=1&page_size=5
        # 1、获取请请求参数
        brand = request.GET.get('brand', 'huawei')
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 5)
        results = Computer.objects.filter(brand=brand).order_by('-good_rate')
        # isdigit()：判断page、page_size是否纯数字组成
        page = int(page) if page.isdigit() else 1
        page_size = int(page_size) if page_size.isdigit() else 5
        # print(page_size)
        # 2、开始分页
        paginator = Paginator(results, page_size)
        error = 0
        try:
            # 获取当前页对象
            current_page = paginator.page(page)
            print(current_page.object_list)
        except (EmptyPage, InvalidPage, PageNotAnInteger) as e:
            error = '请求参数异常，默认已返回最后一页'
            current_page = paginator.page(paginator.num_pages)
            # 同时将page改为最后一页
            page = paginator.num_pages
        # 3、上一页、下一页链接以及总页数
        # next_url = f'http://127.0.0.1:8000/phone/?brand={brand}&page={page+1}&page_size={page_size}' if current_page.has_next() else ""
        # pre_url = f'http://127.0.0.1:8000/phone/?brand={brand}&page={page-1}&page_size={page_size}' if current_page.has_previous() else ""
        total_page = paginator.num_pages
        # 4、计算页码
        page_numbers = []
        if total_page <= 5:
            page_numbers = [x for x in range(1, total_page+1)]
        else:
            # 移动
            if 3 < page < total_page-3:
                page_numbers = [x for x in range(page-2, page+3)]
            # 不移动
            elif page <= 3:
                page_numbers = [x for x in range(1, 6)]
            # 不移动
            elif page >= total_page-3:
                page_numbers = [x for x in range(page-5, total_page+1)]
        data = {
            'status': 1,
            'error': error,
            'if_has_pre_page': current_page.has_previous(),
            'if_has_next_page': current_page.has_next(),
            'page_numbers': page_numbers,
            'current_page_data': object_to_json(current_page.object_list)
        }
        # response = JsonResponse(data)
        # response['Access-Control-Allow-Origin'] = '*'
        return data


class DetailView(View):
    @method_decorator(allow_origin)
    def get(self, request):
        computer_id = request.GET.get('computer_id', '')
        computer = 0
        status = 1
        wordcloud_path = 0
        pie_path = 0
        bar_path = 0
        top10_bar_path = 0
        try:
            computer_obj = Computer.objects.filter(computer_id=computer_id)
            computer = object_to_json(computer_obj)[0]
            # 词云图
            if not os.path.exists(f'static\wordcloud\{computer_id}.png'):
                if_success = create_wordcloud(computer_id)
                if if_success:
                    wordcloud_path = f'..\computer_analysis\static\wordcloud\{computer_id}.png'
            else:
                wordcloud_path = f'..\computer_analysis\static\wordcloud\{computer_id}.png'
            # 饼状图
            if not os.path.exists(f'..\static\pie\{computer_id}.svg'):
                if_success = create_pie(computer_id)
                if if_success:
                    pie_path = f'..\computer_analysis\static\pie\{computer_id}.svg'
            else:
                pie_path = f'..\computer_analysis\static\pie\{computer_id}.svg'
            # 柱状图
            if not os.path.exists(f'..\static\\bar\{computer_id}.svg'):
                if_success = create_bar(computer_id)
                if if_success:
                    bar_path = f'..\computer_analysis\static\\bar\{computer_id}.svg'
            else:
                bar_path = f'..\computer_analysis\static\\bar\{computer_id}.svg'
            # jieba_top10_bar柱图
            if not os.path.exists(f'..\static\jieba_top10_bar\{computer_id}.svg'):
                if_success = jieba_top10_bar(computer_id)
                if if_success:
                    top10_bar_path = f'..\computer_analysis\static\jieba_top10_bar\{computer_id}.svg'
            else:
                bar_path = f'..\computer_analysis\static\jieba_top10_bar\{computer_id}.svg'
        except Exception as e:
            print(e)
            status = 0
        data = {
            'status': status,
            'computer': computer,
            'wordcloud': wordcloud_path,
            'pie': pie_path,
            'bar': bar_path,
            'top10_bar': top10_bar_path
        }
        # response = JsonResponse(data)
        # response['Access-Control-Allow-Origin'] = '*'
        return data



class ComputerSearchView(SearchView):

    def extra_context(self):
        context = super(ComputerSearchView, self).extra_context()
        key = self.request.GET.get('q')
        context['q'] = key
        return context

    def build_page(self):
        data = {
            'status': 1,
            'error': 0,
            'if_has_pre_page': 0,
            'if_has_next_page': 0,
            'page_numbers': 0,
            'current_page_data': 0
        }
        try:
            page = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            data['error'] = '页码值非法！'
            page = 0
            data['status'] = 0
        if page < 1:
            data['error'] = '页码值非法！'
            data['status'] = 0
        # start_offset = (page - 1) * self.results_per_page
        if data['status']:
            self.results[:]
            self.results = self.results.order_by('-good_rate')
            paginator = Paginator(self.results, self.results_per_page)
            # self.results[start_offset: start_offset + self.results_per_page]
            # self.results在经过上面的切片代码self.results[start_offset:start_offset + self.results_per_page]之后，才有值。在此之前是没有值的，所有排序的order_by必须设置在这句代码的后面
            # haystack对搜索结果的分页，并不是将所有的搜索结果全部分页。
            # paginator = Paginator(self.results, self.results_per_page)
            try:
                # 获取当前页对象
                current_page = paginator.page(page)
                data['current_page_data'] = sea_result2json(current_page.object_list)
                data['if_has_next_page'] = current_page.has_next()
                data['if_has_pre_page'] = current_page.has_previous()
            except (EmptyPage, InvalidPage, PageNotAnInteger) as e:
                data['error'] = '请求页码超出范围，默认返回最后一页'
                data['current_page_data'] = sea_result2json(paginator.page(paginator.num_pages).object_list)
                # 同时将page改为最后一页
                page = paginator.num_pages
                data['if_has_pre_page'] = True
            total_page = paginator.num_pages
            # 计算页码
            page_numbers = []
            if total_page <= 5:
                page_numbers = [x for x in range(1, total_page + 1)]
            else:
                # 移动
                if 3 < page < total_page - 3:
                    page_numbers = [x for x in range(page - 2, page + 3)]
                # 不移动
                elif page <= 3:
                    page_numbers = [x for x in range(1, 6)]
                # 不移动
                elif page >= total_page - 3:
                    page_numbers = [x for x in range(page - 5, total_page + 1)]
            data['page_numbers'] = page_numbers
            return data
        return data

    def get_context(self):
        data = self.build_page()
        response = JsonResponse(data)
        # 解决跨域
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def create_response(self):
        response = self.get_context()
        return response




