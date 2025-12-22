import secrets
from datetime import timedelta

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import LicenseKey


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def license_status(request):
    """Return whether the current user has a valid license and any pending requests."""
    user = request.user
    has_license = bool(user.License)

    pending_request = LicenseKey.objects.filter(email=user.email, redeemed_by__isnull=True).first()

    data = {
        "has_license": has_license,
        "pending_request": pending_request is not None,
        "pending_code": pending_request.code if pending_request else None,
    }

    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def request_license(request):
    """Generate a license key, email it to the user, and persist the pending key."""
    user = request.user

    if user.License:
        return Response(
            {"detail": "You already have a license."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    pending = LicenseKey.objects.filter(email=user.email, redeemed_by__isnull=True).first()
    if pending:
        code = pending.code
    else:
        code = secrets.token_urlsafe(12).replace("-", "").upper()
        pending = LicenseKey.objects.create(
            code=code,
            email=user.email,
            issued_to=user,
        )

    subject = "Your Condingo License Key"
    message = (
        f"Hi {user.user_name},\n\n"
        f"Here is your Condingo license code:\n\n"
        f"{code}\n\n"
        f"This code expires in 1 hour. Paste it into the app to unlock exports.\n\n"
        f"- Condingo Team"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except BadHeaderError:
        return Response(
            {"detail": "Invalid email header. License not sent."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exc:
        return Response(
            {"detail": f"Unable to send license email: {exc}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response({"detail": "License sent to your email."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def redeem_license(request):
    """Redeem a license code for the current user."""
    code = request.data.get("code")
    if not code:
        return Response(
            {"detail": "License code is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        license_key = LicenseKey.objects.get(code=code)
    except LicenseKey.DoesNotExist:
        return Response(
            {"detail": "License not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if license_key.redeemed_by:
        return Response(
            {"detail": "License has already been redeemed."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if license_key.email.lower() != request.user.email.lower():
        return Response(
            {"detail": "This license was issued to a different email."},
            status=status.HTTP_403_FORBIDDEN,
        )

    license_key.redeemed_by = request.user
    license_key.redeemed_at = timezone.now()
    license_key.save(update_fields=["redeemed_by", "redeemed_at"])

    request.user.License = license_key.code
    request.user.save(update_fields=["License"])

    return Response({"detail": "License redeemed successfully.", "license_code": license_key.code})
