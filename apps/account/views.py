from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from apps.account import filter_params
from apps.account.models import CustomUser, ChangedPhone
from django.shortcuts import get_object_or_404


class LoginWithPhone(APIView):
    """Registration with phone"""
    @swagger_auto_schema(manual_parameters=filter_params.get_phone_number())
    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None) or request.query_params.get("phone", None)
        action = self.request.query_params.get("type")
        user_type = CustomUser.CLIENT if action else CustomUser.COMPANY
        if phone:
            try:
                user = CustomUser.objects.get(phone_number=phone)
                user.verification_code = 1111
                user.verification_code_creted_at = datetime.now()
                user.user_type = user_type
                user.save()
            except:
                user = CustomUser.objects.create(phone_number=phone, verification_code=1111,
                                                 verification_code_created_at=datetime.now(),
                                                 user_type=user_type)
            return Response({"success": "User found"}, status=status.HTTP_200_OK)


class VerifyPhoneMain(APIView):
    """Verification user phone number"""

    @swagger_auto_schema(manual_parameters=filter_params.get_user_phone_and_code())
    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None) or request.query_params.get("phone", None)
        code = request.data.get("code", None) or request.query_params.get("code", None)
        if phone and code:
            try:
                user = CustomUser.objects.get(phone_number=phone)
                if user:
                    if user.verification_code is not None:
                        if int(code) == user.verification_code:
                            difference = datetime.now() - user.verification_code_created_at.replace(tzinfo=None)
                            difference = float(difference.seconds)
                            if difference > float(120.0):
                                return Response({"error": "verification code expired"},
                                                 status=status.HTTP_400_BAD_REQUEST)
                            user.is_active = True
                            user.save()
                            refresh = TokenObtainPairSerializer().get_token(user)
                            data = {"refresh": str(refresh), "access": str(refresh.access_token), "user_id": user.id}
                            data['status'] = "registered" if user.registered else "not_registered"
                            return Response(data=data, status=status.HTTP_201_CREATED)
                        return Response(
                            {"error": "wrong code"}, status=status.HTTP_403_FORBIDDEN
                        )
                    return Response(
                        {"error": "Verification code is not sent or expired."},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except:
                return Response(
                    {"error": f"User with {phone} is not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {"error": "Phone number or code not provided."},
            status=status.HTTP_400_BAD_REQUEST
        )


class PhoneNumberChangeView(APIView):
    """Change phone number"""

    def post(self, request):
        user = self.request.user
        phone_number = self.request.data.get('phone_number')
        if user.is_authenticated:
            if phone_number:
                if user.phone_number == phone_number:
                    return Response({"success": "phone success changed"}, status=status.HTTP_200_OK)
                try:
                    CustomUser.objects.get(phone_number=phone_number)
                    return Response({"error": "user with this number exists"}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    number, _ = ChangedPhone.objects.get_or_create(user=user)
                    number.number = phone_number
                    number.verification_code = 2222
                    number.created_at = datetime.now()
                    number.save()
                    return Response({"success": "verification code sent"}, status=status.HTTP_200_OK)
            return Response({"error": "phone_number is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "user isn't authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyChangedPhoneNumber(APIView):
    """Verification changed phone number"""

    def post(self, request):
        user = self.request.user
        code = self.request.data.get("code")
        if user.is_authenticated:
            if code:
                changed_number = ChangedPhone.objects.get(user=user)
                if code == changed_number.verification_code:
                    difference = datetime.now() - changed_number.created_at.replace(tzinfo=None)
                    difference = float(difference.seconds)
                    if difference > float(120.0):
                        return Response({"error": "verification code expired"}, status=status.HTTP_400_BAD_REQUEST)
                    phone_number = CustomUser.objects.get(id=user.id)
                    phone_number.phone_number = changed_number.number
                    phone_number.save()
                    return Response({"success": "phone success changed"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "verification code incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "code is required"})
        return Response({"error": "user isn't authenticated"})


class ResendVerifyCodeView(APIView):
    """Resend expired code"""

    def post(self, request):
        user = self.request.user
        action = request.query_params.get("action", None)
        if action == "changephone":
            if user.is_authenticated:
                try:
                    number = ChangedPhone.objects.get(user=user)
                    number.created_at = datetime.now()
                    number.verification_code = 5555
                    number.save()
                    return Response({"success": "verification code sent"}, status=status.HTTP_200_OK)
                except:
                    return Response({"error": "an error occurred while sending the verification code"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "user isn't authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        if action == "login":
            phone = self.request.data.get("phone")
            user = get_object_or_404(CustomUser, phone_number=phone)
            user.verification_code = 1111
            user.verification_code_created_at = datetime.now()
            user.save()
            return Response({"success": "verification code sent"}, status=status.HTTP_200_OK)
