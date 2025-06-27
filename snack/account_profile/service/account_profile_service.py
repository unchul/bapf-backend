from abc import ABC, abstractmethod
from account_profile.entity.account_profile import AccountProfile

class AccountProfileService(ABC):
    @abstractmethod
    def createAccountProfile(
        self, account_id: int, account_name: str, account_nickname: str, phone_num: str,
        account_add: str, account_sex: str, account_birth: str, account_pay: dict, account_sub: bool, alarm_board_status: bool, alarm_comment_status: bool
    ) -> AccountProfile:
        """새로운 AccountProfile을 생성한다."""
        pass

    @abstractmethod
    def getProfileByAccountId(self, account_id: int) -> dict:
        """Account ID로 프로필을 찾는다."""
        pass

    @abstractmethod
    def updateProfile(self, account_id: int, update_data: dict) -> AccountProfile:
        pass

    @abstractmethod
    def isNicknameAvailable(self, account_nickname: str) -> bool:
        """닉네임 중복 확인"""
        pass

    @abstractmethod
    def updateBoardAlarmStatus(self, account_id: int, alarm_board_status: bool):
        pass

    @abstractmethod
    def updateCommentAlarmStatus(self, account_id: int, alarm_comment_status: bool):
        pass