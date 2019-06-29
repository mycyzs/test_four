# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^get_app_info$', 'test'),
    (r'^search_sys_info$', 'search_sys_info'),
    (r'^add_sys$', 'add_sys'),
    (r'^modify_sys$', 'modify_sys'),
    (r'^delete_sys$', 'delete_sys'),
    (r'^search_init$', 'search_app_host'),
    (r'^get_count_obj$', 'get_count_obj'),  # 圆饼图
    (r'^get_count$', 'get_count'),   # 折线图
    (r'^get_count_zhu$', 'get_count_zhu'),  # 柱状图
    (r'^search_biz$', 'search_buseness'),  # 柱状图
    (r'^search_user$', 'get_all_user'),  # 柱状图
    (r'^search_detail$', 'search_detail'),  # 柱状图
    (r'^search_kao_info$', 'search_kao_info'),  # 柱状图
    (r'^up_cvs$', 'up_cvs'),  # 柱状图
    (r'^down_load$', 'down_cvs'),  # 柱状图

)
