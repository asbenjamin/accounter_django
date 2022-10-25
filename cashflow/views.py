from rest_framework.views import APIView
from invoice.models import Invoice
from rest_framework.response import Response

from django.db.models import Sum


class CashBalance(APIView):
    def get(self, request, format=None):
        # TODO: balance_brought_forward = cash_balance_from_previous_month
        # Inflows
        # total_funding = Funding.objects.aggregate(Sum('amount'))
        # total_equity = Equity.objects.aggregate(Sum('amount'))
        total_sales = Receipt.objects.aggregate(Sum('total_amount'))

        # Outflows
        total_operational_costs = Invoice.objects.aggregate(Sum('total_amount'))
        # total_capital_costs = ExpenseItem.objects.aggregate(Sum('total_amount'))

        gross_profit = (total_sales.get('total_amount__sum') or 0) - (total_operational_costs.get('total_amount__sum') or 0)
        if gross_profit < 0:
            total_taxes = 0
        else:
            total_taxes = 0.3*gross_profit

        cash_balance = ((total_sales.get('total_amount__sum')) or 0) - ((total_operational_costs.get('total_amount__sum') or 0) + total_taxes)

        return Response(cash_balance)
