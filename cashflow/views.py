import decimal

from rest_framework.views import APIView
from invoice.models import ExpenseItem
from receipt.models import SaleItem, Receipt
from rest_framework.response import Response

from django.db.models import Sum


class SalesView(APIView):
    def get(self, request, format=None):
        total_sales = SaleItem.objects.aggregate(Sum('net_amount'))

        return Response(total_sales)


class CostsView(APIView):
    def get(self, request, format=None):
        total_operational_costs = ExpenseItem.objects.aggregate(Sum('net_amount'))

        return Response(total_operational_costs)


class SalesTaxesView(APIView):
    def get(self, request, format=None):
        total_sales = SaleItem.objects.aggregate(Sum('net_amount'))

        total_operational_costs = ExpenseItem.objects.aggregate(Sum('net_amount'))

        gross_profit = (total_sales.get('net_amount__sum') or 0) - (total_operational_costs.get('net_amount__sum') or 0)
        if gross_profit < 0:
            total_taxes = 0
        else:
            total_taxes = decimal.Decimal(0.3)*(gross_profit)

        return Response(total_taxes)


class VATView(APIView):
    def get(self, request, format=None):
        value_added_tax = Receipt.objects.aggregate(Sum('vat_amount'))

        return Response(value_added_tax)


class GrossProfitView(APIView):
    def get(self, request, format=None):
        total_sales = SaleItem.objects.aggregate(Sum('net_amount'))

        total_operational_costs = ExpenseItem.objects.aggregate(Sum('net_amount'))

        gross_profit = (total_sales.get('net_amount__sum') or 0) - (total_operational_costs.get('net_amount__sum') or 0)

        return Response(gross_profit)


class NetCashBalance(APIView):
    def get(self, request, format=None):
        # TODO: balance_brought_forward = cash_balance_from_previous_month
        # Inflows
        # total_funding = Funding.objects.aggregate(Sum('amount'))
        # total_equity = Equity.objects.aggregate(Sum('amount'))
        total_sales = SaleItem.objects.aggregate(Sum('net_amount'))

        # Outflows
        total_operational_costs = ExpenseItem.objects.aggregate(Sum('net_amount'))
        # total_capital_costs = ExpenseItem.objects.aggregate(Sum('total_amount'))

        gross_profit = (total_sales.get('net_amount__sum') or 0) - (total_operational_costs.get('net_amount__sum') or 0)
        if gross_profit < 0:
            total_taxes = 0
        else:
            total_taxes = decimal.Decimal(0.3)*(gross_profit)

        cash_balance = ((total_sales.get('net_amount__sum')) or 0) - ((total_operational_costs.get('net_amount__sum') or 0) + total_taxes)

        return Response(cash_balance)
