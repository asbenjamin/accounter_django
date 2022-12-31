import decimal

from rest_framework.views import APIView
from invoice.models import ExpenseItem
from receipt.models import SaleItem, Receipt
from invoice.models import Invoice, ExpenseItem
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
        if 'date_min' and 'date_max' in request.query_params: # since we shall be using a datepicker in vue
            date_min = int(request.query_params.get('date_min'))
            date_max = int(request.query_params.get('date_max'))

            # print (type(date_min), date_min)

            date = [month for month in range(date_min, date_max)]

            total_sales = [(Receipt.objects.filter(created_at__month=date).aggregate(Sum('net_amount'))) for date in date]
            data = {
                "date" : date,
                "total" : total_sales
            }
            # print (json.dumps(data))
            # {'date': [1, 2, 3], 'total': [{'amount__sum': 6000}, {'amount__sum': None}, {'amount__sum': 40000}]}

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


class ProfitLossStatementView(APIView):
    """View that covers all the cash flows in general - This should be the one that the frontend api should actually use"""
    def get(self, request, format=None):
        total_sales = SaleItem.objects.aggregate(Sum('net_amount'))
        total_operational_costs = ExpenseItem.objects.aggregate(Sum('net_amount'))

        gross_profit = (total_sales.get('net_amount__sum') or 0) - (total_operational_costs.get('net_amount__sum') or 0)
        if gross_profit < 0:
            total_taxes = 0
        else:
            total_taxes = decimal.Decimal(0.3)*(gross_profit)

        value_added_tax = Receipt.objects.aggregate(Sum('vat_amount'))
        cash_balance = ((total_sales.get('net_amount__sum')) or 0) - ((total_operational_costs.get('net_amount__sum') or 0) + total_taxes)

        return Response({
            "total_sales": total_sales,
            "total_operational_costs": total_operational_costs,
            "gross_profit": gross_profit,
            "sales_taxes": total_taxes,
            "value_added_tax": value_added_tax,
            "net_profit": cash_balance 
        })


class GraphicalProfitLossStement(APIView):
    """This will supply the chart api for all cashflows"""
    def get(self, request, format=None):
        # if 'date_min' and 'date_max' in request.query_params: # since we shall be using a datepicker in vue
        #     date_min = int(request.query_params.get('date_min'))
        #     date_max = int(request.query_params.get('date_max'))

            # print (type(date_min), date_min)

        date = [month for month in range(8, 14)]

        total_sales = [Receipt.objects.filter(created_at__month=date).aggregate(Sum('net_amount')) for date in date]
        data = {
            "date" : date,
            "total" : total_sales
        }
        # print (json.dumps(data))
        # {'date': [1, 2, 3], 'total': [{'amount__sum': 6000}, {'amount__sum': None}, {'amount__sum': 40000}]}

        return Response(data)


class CashFlowStatement(APIView):
    def get_month_cash_flow(date):

        # inflows (Add things like debt repayments, etc)
        total_sales =  Receipt.objects.filter(created_at__month=date).aggregate(Sum('net_amount'))
        total_inflows = total_sales

        # outflows
        total_operational_costs =  Invoice.objects.filter(created_at__month=date).aggregate(Sum('net_amount'))
        gross_profit = (total_sales.get('net_amount__sum') or 0) - (total_operational_costs.get('net_amount__sum'))
        if gross_profit < 0:
            total_taxes = 0
        else:
            total_taxes = decimal.Decimal(0.3)*(gross_profit)
        total_outflows = total_operational_costs + total_taxes

        cash_balance = total_inflows - total_outflows
        return cash_balance
    
    def balance_brought_forward(self, date):
        return self.get_month_cash_flow(date-1)

    def get(self, request, format=None):
        request_date = self.request.query_params.get('date') # could be month like 3
        starting_month = 1 # to be obtained through API when set
        starting_balance = 0 # to be obtained through API when set

        # we should enforce a starting month, I mean it has to always be there anyway
        request_cash_flow_date = \
            starting_balance + self.get_month_cash_flow(starting_month) \
            + sum([(self.get_month_cash_flow(date) + self.balance_brought_forward(date)) for date in range((starting_month+1), request_date)])

        return Response(request_cash_flow_date)
