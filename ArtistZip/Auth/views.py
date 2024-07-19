from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ArtistSignupForm, GeneralSignupForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from allauth.socialaccount.models import SocialAccount
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.', extra_tags='login')
    else:
        email = request.GET.get('email')
        contact_number = request.GET.get('contact_number')
        provider = request.GET.get('provider')
        
        if email or contact_number:
            return render(request, 'login.html', {'email': email, 'contact_number': contact_number, 'provider': provider})

    return render(request, 'login.html')

def link_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        provider = request.POST.get('provider')
        kakao_id = request.POST.get('kakao_id')

        try:
            existing_user = CustomUser.objects.get(email=email)
            if existing_user:
                # 소셜 계정을 기존 사용자와 연동
                social_account, created = SocialAccount.objects.get_or_create(
                    user=existing_user,
                    provider=provider,
                    uid=kakao_id
                )
                login(request, existing_user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "계정이 성공적으로 연동되었습니다.")
                
                # 연동 성공 후 세션에서 소셜 로그인 관련 데이터 제거
                if 'sociallogin' in request.session:
                    del request.session['sociallogin']
                    request.session.modified = True
                
                return redirect('index')
        except CustomUser.DoesNotExist:
            messages.error(request, "계정을 연동하는 중 오류가 발생했습니다: 존재하지 않는 사용자입니다.")
        except Exception as e:
            messages.error(request, f"계정을 연동하는 중 오류가 발생했습니다: {str(e)}")
        return redirect('login')

    email = request.session.get('sociallogin', {}).get('email')
    provider = request.session.get('sociallogin', {}).get('provider')
    kakao_id = request.session.get('sociallogin', {}).get('kakao_id')

    return render(request, 'link_account.html', {
        'email': email,
        'provider': provider,
        'kakao_id': kakao_id
    })

@csrf_exempt
def cancel_link(request):
    if request.method == 'POST':
        if 'sociallogin' in request.session:
            del request.session['sociallogin']
            request.session.modified = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})



@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if not form.cleaned_data['profile_picture']:
                form.cleaned_data['profile_picture'] = user.profile_picture
            form.save()
            return redirect('myprofile', user_id=user.id)
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'edit_profile.html', {
        'form': form
    })

def logout_view(request):
    logout(request)
    return redirect('index')

def artist_signup(request):
    if request.method == 'POST':
        form = ArtistSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_artist = True
            user.save()
            # 명시적으로 백엔드를 지정하여 로그인
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = ArtistSignupForm()
    return render(request, 'artist_signup_form.html', {'form': form})

def general_signup(request):
    if request.method == 'POST' :
        form = GeneralSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # 명시적으로 백엔드를 지정하여 로그인
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = GeneralSignupForm()
    return render(request, 'general_signup_form.html', {'form': form})

def signup(request):
    return render(request, 'login.html')
