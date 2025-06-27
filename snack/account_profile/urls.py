from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account_profile.controller.account_profile_controller import AccountProfileController

router = DefaultRouter()
router.register(r"account/profile", AccountProfileController, basename='account-profile')

urlpatterns = [
    path("", include(router.urls)),
    path("create", AccountProfileController.as_view({"post": "createProfile"}), name="create-profile"),
    path("get", AccountProfileController.as_view({"get": "getProfile"}), name="get-profile"),
    path("update", AccountProfileController.as_view({"patch": "updateProfile"}), name="update-profile"),
    path("check-nickname-duplication", AccountProfileController.as_view({"post": "checkNicknameDuplication"}), name="check-nickname-duplication"),
    # path('update-board-alarm', AccountProfileController.as_view({'put': 'userUpdateBoardAlarm'}), name='update-board-alarm'),
    # path('update-comment-alarm', AccountProfileController.as_view({'put': 'userUpdateCommentAlarm'}), name='update-comment-alarm'),
]