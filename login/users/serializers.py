# json 문서를 변환하는 DB와 외부와의 번역기 역할이라고 생각하면 좋다.
# 회원가입 과정에 대한 기능의 대부분을 시리얼라이저에서 구현하였기 때문에 조금 복잡하다.

from django.contrib.auth.models import User   #user모델을 불러온다.(기본 장고 패키지)
from django.contrib.auth.password_validation import validate_password    # 장고의 기본 패스워드 검증 도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token    # 토큰 모델(로그인창 만들때)
from rest_framework.validators import UniqueValidator   # 이메일 중복 방지를 위한 검증 도구
# from rest_framework.authtoken.serializers import TokenSerializer

# 회원 가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators = [UniqueValidator(queryset=User.objects.all())],    # 이메일에 대한 중복 검증
    )
    
    password = serializers.CharField(
        write_only=True,    #복사 붙여넣기를 금지한다.
        required=True,
        validators=[validate_password],    # 비밀번호에 대한 검증을 실행한다.
    )
    
    password2 = serializers.CharField(write_only=True, required=True)    # 비밀번호 재확인을 위한 필드
    
    
    
    
    class Meta:
        model = User
        fields =('username','password', 'password2', 'email')
        
        
        
        
    # 추가적으로 비밀번호 일치 여부를 확인
    def validate(self, data):
        
        # 만약 사용자가 입력한 비밀번호가, 다시한번 입력한 비밀번호와 일치하지 않으면 실행됨
        if data['password'] != data['password2']:    
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}     # 비밀번호가 일치하지 않습니다 라는 메시지 출력됨
            )
        return data
    
    
    # 회원 정보를 생성하는 시리얼라이저
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user
    
    
    
from django.contrib.auth import authenticate    # 장고의 기본 authenticate 함수 ,우리가 성정한 DefaultAuthBackend인 TokenAuth 방식으로 유저를 인증한다. 
# 로그인 하는 기능을 구현 (ID, PW만 적어주면 이를 확인해서 그에 해당하는 토큰을 응답하기만 하면 끝이기 때문), Modelserializer 사용할 필요 없음

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    # write_only 옵션을 통해 클라이언트 -> 서버 방향의 역 직렬화는 가능, 서버->클라이언트 방향의 직렬화는 불가능하게 함
    
    def validate(self, data):
        user = authenticate(**data)
        if user:
            token= Token.objects.get(user=user)    # 사용자의 아이디와 입력한 아이디가 일치하면 로그인 실행
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )