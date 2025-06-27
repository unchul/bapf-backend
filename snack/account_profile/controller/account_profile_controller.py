from django.http import JsonResponse
from rest_framework import viewsets, status

from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class AccountProfileController(viewsets.ViewSet):
    __profileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def createProfile(self, request):
        """AccountProfile을 생성하는 엔드포인트"""
        postRequest = request.data
        email = postRequest.get("email")

        # Redis에서 account_id 가져오기
        account_id = self.redisCacheService.getValueByKey(email)

        if not account_id:
            return JsonResponse({"error": "해당 이메일에 대한 계정 정보를 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        profile = self.__profileService.createAccountProfile(
            account_id=account_id,
            account_name=postRequest.get("account_name"),
            account_nickname=postRequest.get("account_nickname"),
            phone_num=postRequest.get("phone_num"),
            account_add=postRequest.get("account_add"),
            account_sex=postRequest.get("account_sex"),
            account_birth=postRequest.get("account_birth"),
            account_pay=postRequest.get("account_pay"),
            account_sub=postRequest.get("account_sub"),
            alarm_board_status=postRequest.get("alarm_board_status", True),
            alarm_comment_status=postRequest.get("alarm_comment_status", True)
        )
        return JsonResponse({"success": True, "profile_id": profile.account.id}, status=status.HTTP_201_CREATED)

    def getProfile(self, request):
        account_id = request.headers.get("account-id")
        user_token = request.headers.get("usertoken")

        print(f"account_id: {account_id}")   # AAA
        print(f"user_token: {user_token}")   # AAA

        if not user_token or not account_id:
            return JsonResponse({"error": "userToken과 account_id가 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        print(123)  # AAA

        redis_account_id = self.redisCacheService.getValueByKey(user_token)
        if str(redis_account_id) != str(account_id):
            return JsonResponse({"error": "토큰 인증 실패", "success": False}, status=status.HTTP_403_FORBIDDEN)

        profile = self.__profileService.getProfileByAccountId(account_id)

        if not profile:
            return JsonResponse({"error": "프로필을 찾을 수 없습니다", "success": False}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({
            "account_id": profile["account_id"],
            "account_name": profile["account_name"],
            "account_nickname": profile["account_nickname"],
            "phone_num": profile["phone_num"],
            "account_add": profile["account_add"],
            "account_sex": profile["account_sex"],
            "account_birth": profile["account_birth"],
            "account_pay": profile["account_pay"],
            "account_sub": profile["account_sub"],
            "account_age": profile["account_age"],
            "alarm_board_status": profile["alarm_board_status"],
            "alarm_comment_status": profile["alarm_comment_status"],
            "success": True
        }, status=status.HTTP_200_OK)
    
    def updateProfile(self, request):
        account_id = request.headers.get("account-id")
        user_token = request.headers.get("usertoken")

        if not account_id:  # user_token도 체크하지 않음
            return JsonResponse({"error": "Account-Id가 필요합니다.", "success": False}, status=400)

        if not account_id or not user_token:
            return JsonResponse({"error": "Account-Id와 userToken이 필요합니다.", "success": False}, status=400)

        redis_account_id = self.redisCacheService.getValueByKey(user_token)
        if str(redis_account_id) != str(account_id):
            return JsonResponse({"error": "토큰 인증 실패", "success": False}, status=403)

        post_data = request.data
        updated_profile = self.__profileService.updateProfile(account_id, post_data)

        return JsonResponse({"success": True, "account_id": updated_profile.account.id}, status=200)

    def checkNicknameDuplication(self, request):
        account_nickname = request.data.get("account_nickname")
        if not account_nickname:
            return JsonResponse({"error": "닉네임이 필요합니다.", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        is_available = self.__profileService.isNicknameAvailable(account_nickname)

        if is_available:
            return JsonResponse({"success": True, "available": True}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"success": False, "available": False, "error": "이미 사용 중인 닉네임입니다."}, status=status.HTTP_409_CONFLICT)

    # def userUpdateBoardAlarm(self, request):
    #     user_token = request.headers.get("usertoken")
    #     if not user_token:
    #         return JsonResponse({"error": "userToken이 필요합니다.", "success": False}, status=400)
    #
    #     account_id = request.headers.get("account-id")
    #     if not account_id:
    #         return JsonResponse({"error": "account_id가 필요합니다.", "success": False}, status=401)
    #
    #     postRequest = request.data
    #     alarm_board_status = postRequest.get("alarm_board_status")
    #
    #     if alarm_board_status is None:
    #         return JsonResponse({"error": "alarm_board_status 값이 필요합니다.", "success": False}, status=400)
    #
    #     updated = self.__profileService.updateBoardAlarmStatus(account_id, alarm_board_status)
    #     if updated:
    #         return JsonResponse({"success": True, "message": "댓글 알림 설정이 업데이트되었습니다."}, status=200)
    #     else:
    #         return JsonResponse({"success": False, "message": "댓글 알림 설정 업데이트에 실패했습니다."}, status=500)
    #
    # def userUpdateCommentAlarm(self, request):
    #     user_token = request.headers.get("usertoken")
    #     if not user_token:
    #         return JsonResponse({"error": "userToken이 필요합니다.", "success": False}, status=400)
    #
    #     account_id = request.headers.get("account-id")
    #     if not account_id:
    #         return JsonResponse({"error": "account_id가 필요합니다.", "success": False}, status=401)
    #
    #     postRequest = request.data
    #     alarm_comment_status = postRequest.get("alarm_comment_status")
    #
    #     if alarm_comment_status is None:
    #         return JsonResponse({"error": "alarm_comment_status 값이 필요합니다.", "success": False}, status=400)
    #
    #     updated = self.__profileService.updateCommentAlarmStatus(account_id, alarm_comment_status)
    #     if updated:
    #         return JsonResponse({"success": True, "message": "대댓글 알림 설정이 업데이트되었습니다."}, status=200)
    #     else:
    #         return JsonResponse({"success": False, "message": "대댓글 알림 설정 업데이트에 실패했습니다."}, status=500)