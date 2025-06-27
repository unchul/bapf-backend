import random
import uuid

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, status
from datetime import datetime

from account.service.account_service_impl import AccountServiceImpl
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from naver_authentication.service.naver_oauth_service_impl import NaverOauthServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from account.entity.role_type import RoleType

class NaverOauthController(viewsets.ViewSet):
    naverOauthService = NaverOauthServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()
    accountProfileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestNaverOauthLink(self, request):
        url = self.naverOauthService.requestNaverOauthLink()
        return JsonResponse({"url": url}, status=status.HTTP_200_OK)

    def requestAccessToken(self, request):
        code = request.data.get('code')
        state = request.data.get('state')

        if not code:
            return JsonResponse({'error': 'Authorization code is required'}, status=400)

        try:
            tokenResponse = self.naverOauthService.requestAccessToken(code, state)
            accessToken = tokenResponse['access_token']

            with transaction.atomic():
                userInfo = self.naverOauthService.requestUserInfo(accessToken)
                response = userInfo.get('response', {})
                email = response.get('email', '')
                name = response.get('nickname', '')
                #print(name)   # AAA
                account_path = "Naver"
                role_type = RoleType.USER
                phone_num = response.get('mobile', '')
                address = ""
                gender = response.get('gender', '')
                birthyear = response.get('birthyear', '')
                birthday = response.get('birthday', '')
                payment = ""
                subscribed = False
                age = ""
                alarm_board_status = True
                alarm_comment_status = True


                birth = None
                if birthday and birthyear:
                    try:
                        birth = datetime.strptime(f"{birthyear}-{birthday}", "%Y-%m-%d").date()
                    except ValueError:
                        birth = None

                #print("asdf")      # AAA
                conflict_message = self.accountService.checkAccountPath(email, account_path)
                if conflict_message:
                    return JsonResponse({'success': False, 'error_message': conflict_message}, status=409)

                #print("asdfasdf")   # AAA
                account = self.accountService.checkEmailDuplication(email)
                account, status_message = self.accountService.checkAccountStatus(account)
                print(account, status_message)  # AAA 디버깅

                if status_message:
                    if "SUSPENDED" in status_message:
                        return JsonResponse({'success': False, 'error_message': status_message},status=414)
                    elif "BANNED" in status_message:
                        return JsonResponse({'success': False, 'error_message': status_message},status=444)

                is_new_account = False
                if account is None:
                    is_new_account = True
                    account = self.accountService.createAccount(email, account_path, role_type)
                    print(account)  # AAA
                    nickname = self.__generateUniqueNickname()
                    print(nickname)  # AAA
                    self.accountProfileService.createAccountProfile(
                        account.id, name, nickname, phone_num, address, gender, birth.strftime("%Y-%m-%d") if birth else None, payment, subscribed, alarm_board_status, alarm_comment_status
                    )
                print(account)

                self.accountService.updateLastUsed(account.id)
                print(account.id)  # AAA
                userToken = self.__createUserTokenWithAccessToken(account, accessToken)
                self.redisCacheService.storeKeyValue(userToken, account.id)
                self.redisCacheService.storeKeyValue(account.email, account.id)

                print(userToken)  # AAA

                response = JsonResponse({'message': f'login_status_ok, usertoken : {userToken}, account_id : {account.id}'}, status=status.HTTP_201_CREATED if is_new_account else status.HTTP_200_OK)
                response['usertoken'] = userToken
                response['account-id'] = account.id
                response["Access-Control-Expose-Headers"] = "usertoken,account-id"
                print(response.items())   # AAA
                return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    def requestAccessTokenForApp(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')
        if not code:
            return JsonResponse({'error': 'code is required'}, status=400)

        print(f"[NAVER] Received code: {code}, state: {state}")

        try:
            tokenResponse = self.naverOauthService.requestAccessTokenForApp(code, state)
            accessToken = tokenResponse['access_token']
            print(f"[NAVER] accessToken: {accessToken}")

            with transaction.atomic():
                userInfo = self.naverOauthService.requestUserInfo(accessToken)
                print(f"[NAVER] userInfo: {userInfo}")

                account_path = "Naver"
                role_type = RoleType.USER
                response = userInfo.get('response', {})
                email = response.get('email', '')
                nickname = response.get('nickname', '')
                name = nickname  # 네이버는 실명 정보 없음
                phone_num = ''
                address = ''
                gender = response.get('gender', '')
                birthyear = response.get('birthyear', '')
                birthday = response.get('birthday', '')
                payment = ''
                subscribed = False
                age = response.get('age', '')
                alarm_board_status = True
                alarm_comment_status = True


                birth = None
                if birthyear and birthday:
                    try:
                        birth = datetime.strptime(f"{birthyear}-{birthday}", "%Y-%m-%d").date()
                    except ValueError:
                        birth = None

                account = self.accountService.checkEmailDuplication(email)
                if account is None:
                    account = self.accountService.createAccount(email, account_path, role_type)
                    self.accountProfileService.createAccountProfile(
                    account.id, name, nickname, phone_num, address, gender,
                    birth.strftime("%Y-%m-%d") if birth else None, payment, subscribed, age, alarm_board_status, alarm_comment_status
                )

                self.accountService.updateLastUsed(account.id)
                self.redisCacheService.storeKeyValue(account.email, account.id)

                userToken = self.__createUserTokenWithAccessToken(account, accessToken)
                print(userToken)
                return HttpResponse(f"""
                    <html>
                      <body>
                        <script>
                          const userToken = '{userToken}';
                          const email = '{email}';
                          const nickname = '{nickname}';
                          window.location.href = 'flutter://naver-login-success?userToken=' + encodeURIComponent(userToken) + '&email=' + encodeURIComponent(email) + '&nickname=' + encodeURIComponent(nickname);
                        </script>
                      </body>
                    </html>
                """)

        except Exception as e:
            print(f"[NAVER] Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)



    def requestUserToken(self, request):
        access_token = request.data.get('access_token')
        email = request.data.get('email')
        name = request.data.get('nickname')
        account_path = "Naver"
        role_type = RoleType.USER
        phone_num = request.data.get('phone_num', "")
        address = request.data.get('address', "")
        gender = request.data.get('gender', "")
        birthyear = request.data.get('birthyear', "")
        birthday = request.data.get('birthday', "")
        payment = request.data.get('payment', "")
        subscribed = request.data.get('subscribed', False)
        alarm_board_status = request.data.get('alarm_board_status', True)
        alarm_comment_status = request.data.get('alarm_comment_status', True)

        birth = None
        if birthday and birthyear:
            try:
                birth = datetime.strptime(f"{birthyear}-{birthday}", "%Y-%m-%d").date()
            except ValueError:
                birth = None

        if not access_token:
            return JsonResponse({'error': 'Access token is required'}, status=400)
        if not email or not nickname:
            return JsonResponse({'error': 'Email and nickname are required'}, status=400)

        try:
            with transaction.atomic():
                conflict_message = self.accountService.checkAccountPath(email, account_path)
                if conflict_message:
                    return JsonResponse({'success': False, 'error_message': conflict_message}, status=601)

                account = self.accountService.checkEmailDuplication(email)
                is_new_account = False
                if account is None:
                    is_new_account = True
                    account = self.accountService.createAccount(email, account_path, role_type)
                    nickname = self.__generateUniqueNickname()
                    self.accountProfileService.createAccountProfile(
                        account.id, name, nickname, phone_num, address, gender, birth, payment, subscribed, alarm_board_status, alarm_comment_status
                    )

                self.accountService.updateLastUsed(account.id)
                userToken = self.__createUserTokenWithAccessToken(account, access_token)
                self.redisCacheService.storeKeyValue(account.email, account.id)

                response = JsonResponse({'message': 'login_status_ok'}, status=status.HTTP_201_CREATED if is_new_account else status.HTTP_200_OK)
                response['usertoken'] = userToken
                response['account_id'] = account.id
                return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    def __generateUniqueNickname(self):
        base = "헝글"
        for _ in range(10):
            candidate = base + str(random.randint(1000, 9999))
            from account_profile.entity.account_profile import AccountProfile
            if not AccountProfile.objects.filter(account_nickname=candidate).exists():
                return candidate
        return base + str(uuid.uuid4())[:4]

    def __createUserTokenWithAccessToken(self, account, accessToken):
        try:
            userToken = f"naver-{uuid.uuid4()}"
            self.redisCacheService.storeKeyValue(account.getId(), accessToken)
            self.redisCacheService.storeKeyValue(userToken, account.getId())
            return userToken
        except Exception as e:
            print('Redis에 토큰 저장 중 에러:', e)
            raise RuntimeError('Redis에 토큰 저장 중 에러')