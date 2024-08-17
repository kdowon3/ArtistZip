from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artwork, Portfolio, Special_Portfolio
from .forms import ArtworkForm, PortfolioForm, SpecialPortfolioForm
from Auth.models import CustomUser, Subscription
from Chat.models import ChatRoom, Message
from django.contrib.auth import get_user_model
import random
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.urls import reverse, resolve, NoReverseMatch
from django.http import Http404
import requests
from django.http import HttpResponse
User = get_user_model()

def index(request):
    return render(request, 'MyApp/index.html')

def az(request):
    return render(request, 'MyApp/az.html')

@login_required
def artists(request):
    search_query = request.GET.get('search', '')
    if search_query:
        artists_queryset = CustomUser.objects.filter(
            Q(username__icontains=search_query) & Q(is_artist=True)
        )
    else:
        artists_queryset = CustomUser.objects.filter(is_artist=True)
    
    artists = list(artists_queryset)  # QuerySet을 리스트로 변환
    random.shuffle(artists)
    
    context = {
        'artists': artists,
        'search_query': search_query,
    }
    return render(request, 'MyApp/artists.html', context)

@login_required
def gallery(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        artworks = list(Artwork.objects.filter(
            Q(user__username__icontains=search_query) |
            Q(artwork_title__icontains=search_query)
        ))
    else:
        artworks = list(Artwork.objects.all())
    
    random.shuffle(artworks)
    
    paginator = Paginator(artworks, 20)  # Show 20 artworks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'MyApp/gallery.html', context)

@login_required
def contact(request):
    chatrooms = ChatRoom.objects.filter(participants=request.user)
    for chatroom in chatrooms:
        chatroom.last_message = chatroom.messages.last()
        chatroom.last_message_time = chatroom.last_message.timestamp if chatroom.last_message else None
        chatroom.unread = chatroom.messages.filter(is_read=False).exclude(user=request.user).exists()

    active_chatroom = None
    messages = None
    other_user = None
    chatroom_id = request.GET.get('chatroom_id')
    if chatroom_id:
        active_chatroom = get_object_or_404(ChatRoom, id=chatroom_id, participants=request.user)
        messages = Message.objects.filter(chat_room=active_chatroom).order_by('timestamp')
        # Update the 'is_read' field for messages not sent by the current user
        Message.objects.filter(chat_room=active_chatroom).filter(~Q(user=request.user)).update(is_read=True)
        other_user = active_chatroom.get_other_user(request.user)

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat_room=active_chatroom, user=request.user, content=content)
            return redirect(f'/contact/?chatroom_id={chatroom_id}')

    return render(request, 'MyApp/contact.html', {
        'chatrooms': chatrooms,
        'active_chatroom': active_chatroom,
        'messages': messages,
        'other_user': other_user
    })

def signup(request):
    return render(request, 'MyApp/signup.html')

def login(request):
    return render(request, 'MyApp/login.html')

@login_required
def profile(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)
    artworks = Artwork.objects.filter(user=profile_user)
    portfolios = Portfolio.objects.filter(user=profile_user)
    is_subscribed = Subscription.objects.filter(subscriber=request.user, subscribed_to=profile_user).exists()
    
    # 기존에 이 두 사용자 간의 채팅방이 있는지 확인
    chatroom = ChatRoom.objects.filter(participants__id=profile_user.id).filter(participants__id=request.user.id).first()
    if not chatroom:
        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(request.user, profile_user)
        
    return render(request, 'MyApp/profile.html', {
        'profile_user': profile_user,
        'artworks': artworks,
        'portfolios': portfolios,
        'is_subscribed': is_subscribed,
        'chatroom_id': chatroom.id
    })

@login_required
def myprofile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    artworks = Artwork.objects.filter(user=user)
    portfolios = Portfolio.objects.filter(user=user)
    subscriptions = Subscription.objects.filter(subscriber=user)
    
    if user.is_artist:
        is_subscribed = Subscription.objects.filter(subscriber=request.user, subscribed_to=user).exists()
    else:
        is_subscribed = None
    
    return render(request, 'MyApp/myprofile.html', {
        'user': user,
        'artworks': artworks,
        'portfolios': portfolios,
        'subscriptions': subscriptions,
        'is_subscribed': is_subscribed
    })

@login_required
def template(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.user = user
            artwork.save()
            messages.success(request, '작품이 성공적으로 저장되었습니다.')
            return redirect('myprofile', user_id=user.id)
        else:
            messages.error(request, '저장 중 오류가 발생했습니다.')
    else:
        form = ArtworkForm()
    context = {
        'form': form,
    }
    return render(request, 'MyApp/template.html', context)

@login_required
def edit_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect('myprofile', user_id=artwork.user.id)
    else:
        form = ArtworkForm(instance=artwork)
    
    context = {
        'form': form
    }
    return render(request, 'MyApp/template.html', context)

def delete_artwork(request):
    if request.method == 'GET' and 'id' in request.GET:
        artwork_id = request.GET['id']
        artwork = get_object_or_404(Artwork, id=artwork_id)
        user_id = artwork.user.id
        artwork.delete()
        return redirect('myprofile', user_id=user_id)
    return redirect('myprofile')



def create_portfolio1(request, user_id):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user_id = user_id  # user_id를 할당
            portfolio.template_number = 1
            portfolio.save()
            # 저장된 포트폴리오의 ID를 사용하여 리디렉션
            return redirect('portfolio_detail1', user_id=user_id, portfolio_id=portfolio.id)
        else:
            print(form.errors)  # 폼 에러 출력
    else:
        form = PortfolioForm()

    return render(request, 'MyApp/portfolio1.html', {'form': form})

def create_portfolio2(request, user_id):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user_id = user_id  # user_id를 할당
            portfolio.template_number = 2
            portfolio.save()
            # 저장된 포트폴리오의 ID를 사용하여 리디렉션
            return redirect('portfolio_detail2', user_id=user_id, portfolio_id=portfolio.id)
        else:
            print(form.errors)  # 폼 에러 출력
    else:
        form = PortfolioForm()

    return render(request, 'MyApp/portfolio2.html', {'form': form})

def create_portfolio3(request, user_id):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user_id = user_id  # user_id를 할당
            portfolio.template_number = 3
            portfolio.save()
            # 저장된 포트폴리오의 ID를 사용하여 리디렉션
            return redirect('portfolio_detail3', user_id=user_id, portfolio_id=portfolio.id)
        else:
            print(form.errors)  # 폼 에러 출력
    else:
        form = PortfolioForm()

    return render(request, 'MyApp/portfolio3.html', {'form': form})

def create_portfolio4(request, user_id):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user_id = user_id  # user_id를 할당
            portfolio.template_number = 4
            portfolio.save()
            # 저장된 포트폴리오의 ID를 사용하여 리디렉션
            return redirect('portfolio_detail4', user_id=user_id, portfolio_id=portfolio.id)
        else:
            print(form.errors)  # 폼 에러 출력
    else:
        form = PortfolioForm()

    return render(request, 'MyApp/portfolio4.html', {'form': form})
def create_portfolio5(request, user_id):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user_id = user_id  # user_id를 할당
            portfolio.template_number = 5
            portfolio.save()
            # 저장된 포트폴리오의 ID를 사용하여 리디렉션
            return redirect('portfolio_detail5', user_id=user_id, portfolio_id=portfolio.id)
        else:
            print(form.errors)  # 폼 에러 출력
    else:
        form = PortfolioForm()

    return render(request, 'MyApp/portfolio5.html', {'form': form})

def create_portfolio6(request, user_id):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user_id = user_id  # user_id를 할당
            portfolio.template_number = 6
            portfolio.save()
            # 저장된 포트폴리오의 ID를 사용하여 리디렉션
            return redirect('portfolio_detail6', user_id=user_id, portfolio_id=portfolio.id)
        else:
            print(form.errors)  # 폼 에러 출력
    else:
        form = PortfolioForm()

    return render(request, 'MyApp/portfolio6.html', {'form': form})


def portfolio_detail1(request, user_id, portfolio_id):
    portfolio = get_object_or_404(Portfolio, user_id=user_id, id=portfolio_id)
    return render(request, 'MyApp/portfolio_detail1.html', {'portfolio': portfolio})

def portfolio_detail2(request, user_id, portfolio_id):
    portfolio = get_object_or_404(Portfolio, user_id=user_id, id=portfolio_id)
    return render(request, 'MyApp/portfolio_detail2.html', {'portfolio': portfolio})

def portfolio_detail3(request, user_id, portfolio_id):
    portfolio = get_object_or_404(Portfolio, user_id=user_id, id=portfolio_id)
    return render(request, 'MyApp/portfolio_detail3.html', {'portfolio': portfolio})

def portfolio_detail4(request, user_id, portfolio_id):
    portfolio = get_object_or_404(Portfolio, user_id=user_id, id=portfolio_id)
    return render(request, 'MyApp/portfolio_detail4.html', {'portfolio': portfolio})

def portfolio_detail5(request, user_id, portfolio_id):
    portfolio = get_object_or_404(Portfolio, user_id=user_id, id=portfolio_id)
    return render(request, 'MyApp/portfolio_detail5.html', {'portfolio': portfolio})

def portfolio_detail6(request, user_id, portfolio_id):
    portfolio = get_object_or_404(Portfolio, user_id=user_id, id=portfolio_id)
    return render(request, 'MyApp/portfolio_detail6.html', {'portfolio': portfolio})


@login_required
@csrf_exempt
def handle_portfolio(request, user_id, template_name):
    portfolio, created = Portfolio.objects.get_or_create(user_id=user_id)
    
    if request.method == 'POST':
        portfolio_form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        artwork_formset = ArtworkFormSet(request.POST, request.FILES, instance=portfolio)
        
        if portfolio_form.is_valid() and artwork_formset.is_valid():
            portfolio = portfolio_form.save(commit=False)
            portfolio.user_id = user_id
            portfolio.save()

            # Handle Artwork uploads
            for i in range(1, 7):
                image_file = request.FILES.get(f'image{i}')
                if image_file:
                    artwork = Artwork(
                        user=request.user,
                        artwork_image=image_file,
                        artwork_title=f'Artwork {i}',  # Placeholder title
                        artwork_description=f'Description for artwork {i}'  # Placeholder description
                    )
                    artwork.save()

            return redirect('myprofile', user_id=user_id)
    else:
        form = PortfolioForm(instance=portfolio)

    artworks = Artwork.objects.filter(user=request.user)

    context = {
        'form': form,
        'artworks': artworks,
    }
    return render(request, template_name, context)

@login_required
def portfolio_view(request, user_id):
    portfolio = get_object_or_404(Portfolio, user__id=user_id)
    return render(request, 'MyApp/portfolio_view.html', {'portfolio': portfolio})

@login_required
def portfolio1(request, user_id):
    return handle_portfolio(request, user_id, template_name='MyApp/portfolio1.html')

@login_required
def portfolio2(request, user_id):
    return handle_portfolio(request, user_id, template_name='MyApp/portfolio2.html')

@login_required
def portfolio3(request, user_id):
    return handle_portfolio(request, user_id, template_name='MyApp/portfolio3.html')

@login_required
def portfolio4(request, user_id):
    return handle_portfolio(request, user_id, template_name='MyApp/portfolio4.html')

@login_required
def portfolio5(request, user_id):
    return handle_portfolio(request, user_id, template_name='MyApp/portfolio5.html')

def portfolio_upload(request, user_id):
    if request.method == 'POST':
        form = SpecialPortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            special_portfolio = form.save(commit=False)
            special_portfolio.user_id = user_id
            special_portfolio.save()
            return redirect('portfolio_list', user_id=user_id)
    else:
        form = SpecialPortfolioForm()

    return render(request, 'MyApp/create_portfolio.html', {'form': form})

def portfolio_list(request, user_id):
    portfolios = Special_Portfolio.objects.filter(user_id=user_id)
    return render(request, 'MyApp/portfolio_list.html', {'portfolios': portfolios})

def view_my_portfolio(request, user_id):
    portfolio = Portfolio.objects.filter(user_id=user_id).first()
    
    if not portfolio:
        return HttpResponse("포트폴리오가 없습니다.", status=404)

    if portfolio.template_number:
        return redirect(f'portfolio_detail{portfolio.template_number}', user_id=user_id, portfolio_id=portfolio.id)

    return HttpResponse("포트폴리오를 찾을 수 없습니다.", status=404)

def popup(request):
    return render(request, 'MyApp/popup.html')
