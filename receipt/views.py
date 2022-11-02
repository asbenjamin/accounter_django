import pdfkit

from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from rest_framework import viewsets 
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .serializers import ReceiptSerializer, ItemSerializer
from .models import Receipt, SaleItem

from team.models import Team

class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer
    queryset = Receipt.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        team = self.request.user.teams.first()
        receipt_number = team.first_receipt_number
        team.first_receipt_number = receipt_number + 1
        team.save()

        serializer.save(created_by=self.request.user, team=team, modified_by=self.request.user, receipt_number=receipt_number, bankaccount=team.bankaccount)
    
    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')
    
        serializer.save()

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    template_name = 'receipt/pdf.html'

    if receipt.is_credit_for:
        template_name = 'receipt/pdf_creditnote.html'

    template = get_template(template_name)
    html = template.render({'receipt': receipt, 'team': team})
    pdf = pdfkit.from_string(html, False, options={})

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    return response

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_reminder(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    subject = 'Unpaid receipt'
    from_email = team.email
    to = [receipt.client.email]
    text_content = 'You have an unpaid receipt. Receipt number: #' + str(receipt.receipt_number)
    html_content = 'You have an unpaid receipt. Receipt number: #' + str(receipt.receipt_number)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    template = get_template('receipt/pdf.html')
    html = template.render({'receipt': receipt, 'team': team})
    pdf = pdfkit.from_string(html, False, options={})

    if pdf:
        name = 'receipt_%s.pdf' % receipt.receipt_number
        msg.attach(name, pdf, 'application/pdf')

    msg.send()

    return Response()
