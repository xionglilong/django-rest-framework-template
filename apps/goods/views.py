from datetime import datetime
from django.shortcuts import render
from utils.alipay_api import AlipayAPI
from .models import OrderInfoModel
from rest_framework.response import Response

# Create your views here.

from rest_framework.views import APIView


class AlipayView(APIView):
    """支付"""
    def get(self, request):
        param_dict = {key: value for key, value in request.GET.items()}
        result = self.update_order_status(param_dict)
        if result:
            return Response('success')  # 告诉支付宝已经收到，不然支付宝会多次发请求

    def post(self, request):
        param_dict = {key: value for key, value in request.POST.items()}
        result = self.update_order_status(param_dict)
        if result:
            return Response('success')  # 告诉支付宝已经收到，不然支付宝会多次发请求

    # 更新订单状态
    @staticmethod
    def update_order_status(param_dict) -> bool:
        verify_result = AlipayAPI().verify_from_dict(param_dict)
        if verify_result is True:  # 如果验签成功
            order_sn = param_dict.get('out_trade_no', None)  # 订单号
            trade_no = param_dict.get('trade_no', None)  # 支付宝交易号
            trade_status = param_dict.get('trade_status', None)  # 交易状态

            # 修改数据库中订单状态
            order_queryset = OrderInfoModel.objects.filter(order_sn=order_sn)  # 通过订单号查询订单
            for order in order_queryset:
                order.pay_status = trade_status
                order.trade_no = trade_no
                order.pay_time = datetime.now()
                order.save()
            return True

