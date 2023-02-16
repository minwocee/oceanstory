from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    # 회원가입 뷰 연결 완료
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
]
