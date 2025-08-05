from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import re
import requests


@api_view(["GET"])
@permission_classes([AllowAny])
def company_lookup(request, company_number):
    # Validate format (alphanumeric only)
    if not re.match(r'^[A-Za-z0-9]+$', company_number):
        return Response({"detail": "Invalid company number format"}, status=status.HTTP_400_BAD_REQUEST)

    url = f"https://api.company-information.service.gov.uk/company/{company_number}"
    response = requests.get(url, auth=(settings.COMPANIES_HOUSE_API_KEY, ""))

    if response.status_code == 200:
        data = response.json()
        address = ", ".join(filter(None, [
            data.get("registered_office_address", {}).get("address_line_1"),
            data.get("registered_office_address", {}).get("address_line_2"),
            data.get("registered_office_address", {}).get("locality"),
            data.get("registered_office_address", {}).get("postal_code")
        ]))
        return Response({
            "company_name": data.get("company_name") or None,
            "registered_office_address": address or None
        }, status=status.HTTP_200_OK)

    return Response({"detail": "Company not found"}, status=status.HTTP_404_NOT_FOUND)