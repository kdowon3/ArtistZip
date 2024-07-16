from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import redirect
from django.contrib.auth import login
from .models import CustomUser

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        email = user.email
        
        if email:
            try:
                existing_user = CustomUser.objects.filter(email=email).first()
                if existing_user:
                    # 연동된 소셜 계정이 있는지 확인
                    social_account = SocialAccount.objects.filter(user=existing_user, provider=sociallogin.account.provider).first()
                    if social_account:
                        # 이미 연동된 계정이 존재할 경우 로그인 처리
                        login(request, existing_user, backend='django.contrib.auth.backends.ModelBackend')
                        raise ImmediateHttpResponse(redirect('index'))
                    else:
                        # 기존 사용자가 있을 경우 계정 연동 데이터를 세션에 저장하고 모달 띄우기
                        request.session['sociallogin'] = {
                            'email': email,
                            'provider': sociallogin.account.provider,
                            'kakao_id': sociallogin.account.extra_data.get('id')
                        }
                        request.session.modified = True
                        raise ImmediateHttpResponse(redirect('/auth/link-account'))
            except CustomUser.DoesNotExist:
                pass
        else:
            user.username = sociallogin.account.extra_data.get('nickname', user.username)
            user.save()

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        extra_data = sociallogin.account.extra_data

        if sociallogin.account.provider == 'kakao':
            user.user_id = extra_data.get('id', user.user_id)
            user.username = extra_data.get('properties', {}).get('nickname', user.username)

        super().save_user(request, sociallogin, form=form)
        SocialAccount.objects.get_or_create(
            user=user,
            provider=sociallogin.account.provider,
            uid=sociallogin.account.extra_data.get('id')
        )
