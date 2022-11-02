from django.urls import re_path
from . import views


urlpatterns = [
    # re_path(r'^fundings/$', views.FundingList.as_view(), name=views.FundingList.name),
    # re_path(r'^fundings/(?P<pk>[0-9]+)$',views.FundingDetail.as_view(), name=views.FundingDetail.name),

    # re_path(r'^equities/$', views.EquityList.as_view(), name=views.EquityList.name),
    # re_path(r'^equities/(?P<pk>[0-9]+)$',views.EquityDetail.as_view(), name=views.EquityDetail.name),
    # re_path(r'^fundings/total', views.FundingTotal.as_view(), name='total'),
    # re_path(r'^equities/total', views.EquityTotal.as_view(), name='total'),
    re_path(r'^sales/', views.SalesView.as_view(), name='sales'),
    re_path(r'^costs/', views.CostsView.as_view(), name='costs'),
    re_path(r'^taxes/', views.SalesTaxesView.as_view(), name='taxes'),
    re_path(r'^gross-profit/', views.GrossProfitView.as_view(), name='gross-profit'),
    re_path(r'^net-cash/', views.NetCashBalance.as_view(), name='net-cash'),
    re_path(r'^vat/', views.VATView.as_view(), name='vat'),
    # re_path(r'^cumm-cash-balance/', views.CummCashBalance.as_view(), name='cumm_cash_balance')
]
