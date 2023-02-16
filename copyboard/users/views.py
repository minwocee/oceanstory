from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
# Create your views here.

# 회원 가입의 경우 POST(회원 생성기능)만 있기 때문에 굳이 Viewset을 활용해 다른API 요청을 처리해줄 필요가 없다.
# 이 때문에 회원가입 기능은 generics의 CreateAPIView를 활용한다.

# 회원가입을 실행하는 뷰
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# 로그인 하는 뷰
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data    # valudate()의 리턴값인 Token을 받아옴.
        return Response({"token": token.key}, status = status.HTTP_200_OK)


