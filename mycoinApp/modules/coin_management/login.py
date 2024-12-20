from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from authentication.forms import *
from django.core.mail import send_mail
import random
import base64
from django.http import JsonResponse, HttpResponse
from mycoinApp.models import *
from authentication.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.db.models import Min
from urllib.parse import unquote
from django.db.models import F
import secrets
import string
from datetime import timedelta
import csv
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from collections import defaultdict, Counter

def generate_otp():
    return random.randint(100000, 999999)

def generate_token():
    characters = string.ascii_letters + string.digits
    # Generate a secure random token
    token = ''.join(secrets.choice(characters) for _ in range(25))
    return token

def send_email(email, msg, subject):
    print(email, msg)
    subject = subject
    message = msg
    email_from = 'your_email@gmail.com'  
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)



def home(request):
    coins = Coin.objects.values('denomination').annotate(min_id=Min('id')).order_by('denomination')
    data = Coin.objects.filter(id__in=[coin['min_id'] for coin in coins])
    logged_user = request.session.get('user_id', None)
    notifications = PushNotification.objects.filter(user=logged_user)

    context={
        'data':data,
        'notifications' : notifications,
        'count' : notifications.count(),
        # 'name':request.session['name']
    }
    print(data)
    return render(request, 'home.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        # decrypt(password)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print('user not exists')
            messages.error(request, "User does not exist")
            return redirect('login')

        # if check_password(password, user.password): 
        if password == user.password:
            otp = generate_otp()
            send_email(email, f'Your OTP code is {otp}.', 'Your OTP code')
            user.otp = otp
            user.save()
            request.session['otp'] = otp
            request.session['email'] = user.email
            request.session['name'] = user.first_name
            request.session['user_id'] = user.id 
            return redirect('otp-verification')
        else:
            messages.error(request, "Invalid Password")
            return redirect('login')
    return render(request, 'login.html')



# def signup(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.password = form.cleaned_data['password']  
#             user.save()
#             messages.success(request, "User register successfully")
#             return redirect('login') 
#         else:
#             print("Email allready taken ")
#             messages.error(request, "Email allready taken ")    
#             return redirect('signup') 
#     else:
#         form = UserForm()

#     return render(request, 'signup.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        age = request.POST.get('age')
        password = request.POST.get('password')
        reference = request.POST.get('reference')
        gender = request.POST.get('gender')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('signup')

        # Create user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            age=age,
            password=password,  
            reference=reference,
            gender=gender,
        )
        user.save()

        messages.success(request, "User registered successfully")
        return redirect('login')

    return render(request, 'signup.html')

def logout(request): 
    if request.session.session_key:
        request.session.flush()
    # logout(request)
    return redirect("login") 

def coins(request, id):

    logged_user = request.session.get('user_id', None)
    if not logged_user:
        messages.error(request,'Login required to access this page')
        return redirect('login')


    coin = Coin.objects.get(id=id)
    denomination = Coin.objects.filter(denomination=coin.denomination)
    notifications = PushNotification.objects.filter(user=logged_user)
    coinid = []
    for i in denomination:
        coinid.append(i.id)
    
    data = CoinStateCondition.objects.filter(coin__in=coinid)
    if request.GET.get('download') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="coin_details.csv"'

        writer = csv.writer(response)
        writer.writerow(['Denomination', 'Description', 'Metal', 'Year', 'State', 'Condition'])

        for item in data:
            writer.writerow([
                item.coin.denomination,
                item.coin.description,
                item.coin.metal,
                item.coin.year,
                item.state.name,
                item.condition.name
            ])

        return response
    context={
        'data':data,
        'current_url': request.get_full_path(),
        'notifications' : notifications,
        'count' : notifications.count(),
    }
    return render(request,'coins.html',context)


# def coins(request, id):

#     logged_user = request.session.get('user_id', None)
#     if not logged_user:
#         messages.error(request,'Login required to access this page')
#         return redirect('login')
    
#     mint = ''
#     condition = ''
#     if request.method == 'POST':
#         # Get the filter parameters from the POST request
#         mint = request.POST.get('Mint')
#         condition = request.POST.get('Condition')

#     coin = Coin.objects.get(id=id)
#     denomination = Coin.objects.filter(denomination=coin.denomination)
#     coinid = []
#     for i in denomination:
#         coinid.append(i.id)
#     if mint:
#         data = CoinStateCondition.objects.filter(coin__in=coinid, state=mint)
#     elif condition:
#         data = CoinStateCondition.objects.filter(coin__in=coinid, condition=condition)
#     else:
#         data = CoinStateCondition.objects.filter(coin__in=coinid)

#     context={
#         'data':data,
#         'current_url': request.get_full_path()
#     }
#     return render(request,'coins.html',context)

def my_coin(request):
    logged_user = request.session.get('user_id', None)
    if not logged_user:
        messages.error(request,'Login required to access this page')
        return redirect('login')
    data = UserCoinOwnership.objects.filter(user=logged_user)
    notifications = PushNotification.objects.filter(user=logged_user)
    context={
        'data':data,
        'notifications' : notifications,
        'count' : notifications.count(),
    }    
    return render(request, 'my_coin.html',context)

def contact(request):
    return render(request, 'contact.html')

@csrf_exempt
def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get('email')
        user = User.objects.get(email=email)
        
        if user.otp == entered_otp:  
            return redirect('home')  
        else:
            messages.error(request, "Invalid OTP")
            return redirect('login')
    return render(request, 'otp_verification.html')    

def coinDetail(request, id):
    logged_user = request.session.get('user_id', None)
    if not logged_user:
        messages.error(request,'Login required to access this page')
        return redirect('login')
    data = CoinStateCondition.objects.get(id=id)
    notifications = PushNotification.objects.filter(user=logged_user)
    try:
        coin_count = UserCoinOwnership.objects.get(user=logged_user,coin_state_condition=data.id )
        count = coin_count.count
    except:
        count = 0
    
    context={
        'data': data,
        'count' : count,
        'notifications' : notifications,
    }
    return render(request, 'coin_detail.html', context)

def submitCount(request):
    if request.method == 'POST':
        # try:
        quantity = int(request.POST.get('count'))
        coinid = int(request.POST.get('coin-id'))
        user_id = int(request.session.get('user_id'))
        
        coin_state_condition = get_object_or_404(CoinStateCondition, id=coinid)
        user = get_object_or_404(User, id=user_id)

        ownership, created = UserCoinOwnership.objects.get_or_create(user=user, coin_state_condition=coin_state_condition, defaults={'count': quantity})
        if not created:
            ownership.count = quantity
            ownership.save()

        required_coins = [
            {
                'coin_state_condition_id': entry['id'],
                'state_id': entry['state_id'],
                'condition_id': entry['condition_id'],
                'coin_id': entry['coin_id']
            }
            for entry in CoinStateCondition.objects.filter(
                inclusion_status='Y', coin_id=coin_state_condition.coin_id
            ).values('id', 'state_id', 'condition_id', 'coin_id')
        ]
    
        # Fetch user ownerships
        user_ownerships = [
            {
                'coin_state_condition_id': entry['coin_state_condition_id'],
                'state_id': entry['coin_state_condition__state_id'],
                'condition_id': entry['coin_state_condition__condition_id'],
                'coin_id': entry['coin_state_condition__coin_id'],
                'count' : entry['count']
            }
            for entry in UserCoinOwnership.objects.filter(
                user=user_id, coin_state_condition__inclusion_status='Y', count__gt=0
            ).select_related(
                'coin_state_condition__coin',
                'coin_state_condition__state',
                'coin_state_condition__condition',
                'count'
            ).values(
                'coin_state_condition_id', 'coin_state_condition__state_id',
                'coin_state_condition__condition_id', 'coin_state_condition__coin_id', 'count'
            )
        ]

        print(user_ownerships, "user ownerships")
        print(required_coins, "required_coins")
    
        if check_coin_state_ownership(user_ownerships, required_coins):
            grouped_data = defaultdict(list)
            for entry in user_ownerships:
                grouped_data[entry['coin_id']].append(entry)

            # Step 2: Process each group separately
            for coin_id, coin_entries in grouped_data.items():
                # Create a unique set of (condition_id, state_id) tuples to fetch data from CoinStateCondition
                unique_conditions = {(entry['condition_id'], entry['state_id']) for entry in coin_entries}
                
                # Extract condition_ids and state_ids separately
                condition_ids = [condition_id for condition_id, _ in unique_conditions]
                state_ids = [state_id for _, state_id in unique_conditions]

                # Step 3: Get the mapping of (condition_id, state_id) to condition_name and state_name
                condition_mapping = {
                    (condition.condition.id, condition.state.id): {
                        "condition_name": condition.condition.name,
                        "state_name": condition.state.name
                    }
                    for condition in CoinStateCondition.objects.filter(
                        condition_id__in=condition_ids, state_id__in=state_ids
                    ).select_related('condition', 'state')
                }

                # Get the parent coin to retrieve its year
                parent_coin = Coin.objects.get(id=coin_id)
                
                # Step 4: Prepare the JSON-compatible list of dictionaries
                coin_state_condition_data = [
                    {
                        "condition_name": condition_mapping.get((entry['condition_id'], entry['state_id']), {}).get("condition_name", "Unknown"),
                        "state_name": condition_mapping.get((entry['condition_id'], entry['state_id']), {}).get("state_name", "Unknown"),
                        "state_id": entry['state_id'],
                        "count": entry['count'],  # Directly use the count from user_ownerships
                        "year": parent_coin.year
                    }
                    for entry in coin_entries
                ]
                
                # Step 4: Save to the UserSetOfCoins model for the current coin_id
                
                UserSetOfCoin.objects.update_or_create(
                    user=user,  # Match the user
                    coin=parent_coin,  # Match the coin
                    defaults={
                        "set_counts": coin_state_condition_data,  # Update this field
                    },
                    set_name="Set 1"
                )
            # Fetch user's set of coins and link to a set name if available
            user_set_coins = UserSetOfCoin.objects.filter(user=user_id)
            is_make_set = [i.coin_id for i in user_set_coins]
    
            try:
                make_set = SetNameCoins.objects.get(coin_list=is_make_set)
            except SetNameCoins.DoesNotExist:
                make_set = None
    
            if make_set:
                for k in user_set_coins:
                    UniverseCoinSet.objects.update_or_create(
                        user=user, coin_set=k, set_name=make_set, defaults={}
                    )
        return JsonResponse({'message': f"{user.first_name} requested {quantity} coins {coin_state_condition}", 'status': 'success'})        
        # except Exception as e:
        #     return JsonResponse({'message': str(e), 'status': 'error'})
    return JsonResponse({'message': 'Invalid request', 'status': 'error'}, status=400)


def check_coin_state_ownership(user_coin_ownership, required_coins):
    # Step 1: Extract unique (coin_id, state_id) pairs from required_coins
    required_pairs = {(entry['coin_id'], entry['state_id']) for entry in required_coins}
    
    # Step 2: Extract unique (coin_id, state_id) pairs from user_coin_ownership
    user_pairs = {(entry['coin_id'], entry['state_id']) for entry in user_coin_ownership}
    
    # Step 3: Check if all required pairs exist in user pairs
    missing_pairs = required_pairs - user_pairs
    
    # If there are missing pairs, return False; otherwise, return True
    if missing_pairs:
        print(f"Missing pairs: {missing_pairs}")  # Show missing (coin_id, state_id) pairs for debugging
        return False
    return True



# def submitCount(request):
#     if request.method == 'POST':
#         # try:
#         quantity = int(request.POST.get('count'))
#         coinid = int(request.POST.get('coin-id'))
#         user_id = int(request.session.get('user_id'))
        
#         coin_state_condition = get_object_or_404(CoinStateCondition, id=coinid)
#         user = get_object_or_404(User, id=user_id)

#         ownership, created = UserCoinOwnership.objects.get_or_create(user=user, coin_state_condition=coin_state_condition, defaults={'count': quantity})
#         if not created:
#             ownership.count = quantity
#             ownership.save()

#         # dict = {coin_state_condition_id : state_id}
#         required_coins = [{
#         'coin_state_condition_id': entry['id'],
#         'state_id': entry['state_id'],
#         'condition_id': entry['condition_id'],
#         'coin_id' : entry['coin_id']
#         } for entry in CoinStateCondition.objects.filter(inclusion_status='Y', coin_id=coin_state_condition.coin_id).values('id', 'state_id', 'condition_id', 'coin_id')]
       
#         user_ownerships = [{
#         'coin_state_condition_id': entry['coin_state_condition_id'],
#         'state_id': entry['coin_state_condition__state_id'],
#         'condition_id': entry['coin_state_condition__condition_id'],
#         'coin_id' : entry['coin_state_condition__coin_id']
#         } for entry in UserCoinOwnership.objects.filter(user=user_id,coin_state_condition__inclusion_status='Y', count__gt=0).select_related('coin_state_condition__coin', 'coin_state_condition__state', 'coin_state_condition__condition', 'coin_state_condition__coin').values('coin_state_condition_id', 'coin_state_condition__state_id', 'coin_state_condition__condition_id', 'coin_state_condition__coin_id')]
#         print(user_ownerships, "user ownerships")
#         print(required_coins, "required_coins")
        
#         user_ownerships_states = {state['state_id'] for state in user_ownerships}
#         required_states = {state['state_id'] for state in required_coins}
#         if user_ownerships_states.issubset(required_states):
#             required_coin_map = {}
#             for entry in user_ownerships:
#                 state = entry['state_id']
#                 condition = entry['condition_id']
#                 if state not in required_coin_map:
#                     required_coin_map[state] = set()
#                 required_coin_map[state].add(condition)   
#             print(required_coin_map)
#             common_conditions = set.intersection(*required_coin_map.values())
#             complete_set = [entry for entry in user_ownerships if entry['condition_id'] in common_conditions]
#             uncomplete_set = [entry for entry in user_ownerships if entry['condition_id'] not in common_conditions]
#             print("complete set", complete_set, "Uncomplete set", uncomplete_set)
#             all_sets = complete_set + uncomplete_set

#             # Count occurrences of each condition_id
#             condition_counts = Counter(entry['condition_id'] for entry in all_sets)

#             condition_ids = list(condition_counts.keys())
#             condition_mapping = {
#                 condition.condition.id: condition.condition.name
#                 for condition in CoinStateCondition.objects.filter(condition_id__in=condition_ids).select_related('condition')
#             }

#             # Prepare the JSON-compatible list of dictionaries with condition names
#             coin_state_condition_data = [
#                 {
#                     "condition_name": condition_mapping.get(condition_id, "Unknown"),
#                     "count": count
#                 }
#                 for condition_id, count in condition_counts.items()
#             ]

#             # Save to the UserSetOfCoins model
#             parent_coin = Coin.objects.get(id=coin_state_condition.coin_id)
#             UserSetOfCoin.objects.update_or_create(
#                 user=user,  # Match the user
#                 coin=parent_coin,  # Match the coin
#                 defaults={
#                     "set_counts": coin_state_condition_data,  # Update this field
#                 },
#                 set_name = "Set 1"
#             )
#             user_set_coins = UserSetOfCoin.objects.filter(user = user)
#             is_make_set = [i.coin_id for i in user_set_coins]
#             # make_set = SetNameCoins.objects.get(coin_list = is_make_set)
#             # Get the related set name for the list of coins
#             try:
#                 make_set = SetNameCoins.objects.get(coin_list=is_make_set)
#             except SetNameCoins.DoesNotExist:
#                 make_set = None
                
#             if make_set:
#                 # set_details = [i.id for i in user_set_coins]
#                 for k in user_set_coins:
#                     UniverseCoinSet.objects.update_or_create(user = user, coin_set = k, set_name = make_set, defaults={})

#             print(f"The number of pairs of condition_ids that are the same across different states is {common_conditions} and length is {len(common_conditions)}.")

#         return JsonResponse({'message': f"{user.first_name} requested {quantity} coins  {coin_state_condition}", 'status': 'success'})
        
#         # except Exception as e:
#         #     return JsonResponse({'message': str(e), 'status': 'error'})
#     return JsonResponse({'message': 'Invalid request', 'status': 'error'}, status=400)





# def requestCoin(request):
#     if request.method == 'POST':
#         # try:
#         quantity = int(request.POST.get('count'))
#         coinid = int(request.POST.get('coin-id'))
#         per_coin_price = int(request.POST.get('per_coin_price'))
#         user_id = int(request.session.get('user_id'))

#         coin_state_condition = get_object_or_404(CoinStateCondition, id=coinid)
#         user = get_object_or_404(User, id=user_id)
#         message = f"{user.first_name} requested {quantity} coins  {coin_state_condition} at {per_coin_price} Rs per coin"
#         users_with_coins = UserCoinOwnership.objects.filter(coin_state_condition=coin_state_condition, count__gt=0).exclude(user=user)
#         ownership, created = UserCoinOwnership.objects.get_or_create(user=user, coin_state_condition=coin_state_condition, defaults={'request': quantity})
#         if not created:
#             ownership.request = quantity
#             ownership.save()

#         for i in users_with_coins:
#             notification = i.user
#             notification.notifi_count += 1
#             PushNotification.objects.create(user=notification, message=message, request_user=user)
#             notification.save()

#         return JsonResponse({'message': f"{user.first_name} requested {quantity} coins  {coin_state_condition} at {per_coin_price} Rs per coin", 'status': 'success'})
        
#         # except Exception as e:
#         #     return JsonResponse({'message': str(e), 'status': 'error'})
#     return JsonResponse({'message': 'Invalid request', 'status': 'error'}, status=400)



def requestCoin(request):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('count'))
            coinid = int(request.POST.get('coin-id'))
            per_coin_price = int(request.POST.get('per_coin_price'))
            user_id = int(request.session.get('user_id'))

            coin_state_condition = get_object_or_404(CoinStateCondition, id=coinid)
            user = get_object_or_404(User, id=user_id)
            message = f"{user.first_name} requested {quantity} coins {coin_state_condition} at {per_coin_price} Rs per coin"
            users_with_coins = UserCoinOwnership.objects.filter(coin_state_condition=coin_state_condition, count__gt=0).exclude(user=user)
            ownership, created = UserCoinOwnership.objects.get_or_create(user=user, coin_state_condition=coin_state_condition, defaults={'request': quantity})
            
            if not created:
                ownership.request = quantity
                ownership.save()

            for i in users_with_coins:
                notification = i.user
                notification.notifi_count += 1
                PushNotification.objects.create(user=notification, message=message, request_user=user)
                notification.save()

            messages.success(request, f"{user.first_name} requested {quantity} coins {coin_state_condition} at {per_coin_price} Rs per coin")
            return redirect('home')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('home')
    
    messages.error(request, 'Invalid request')
    return redirect('home')

def ContactRequest(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        msg = request.POST.get('msg')
        contactrequest = Contact.objects.create(name=name, email=email,  mobile_number=contact, message=msg)
        contactrequest.save()
        send_email(email, f'{name} {email} {contact} {msg}.', 'Contact Request')
        return JsonResponse({'success': True})

    else:
        return render(request, 'contact.html')


def ForgotPassword(request):
    email = request.GET.get('email', '')
    user = get_object_or_404(User, email=email)
    token = generate_token()
    print(token)
    reset_link = f"http://127.0.0.1:8000/reset_password/{token}/"
    send_email(email, f"You can reset your Password by click on this link {reset_link}", 'Reset Password Link')
    PasswordResetToken.objects.create(
        user=user,
        token=token,
        expires_at=timezone.now() + timedelta(hours=1)  # Token valid for 1 hour
    )
    return render(request, 'forgot_password.html')


def ResetPassword(request, token):
    
    token_obj = get_object_or_404(PasswordResetToken, token=token)
    user = get_object_or_404(User, id=token_obj.user.id)

    if token_obj.is_expired():
        return HttpResponse("This link has expired.", status=400)
    
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        print(new_password, confirm_password)
        if new_password == confirm_password:
            user.password = new_password
            user.save()
            token_obj.delete()  # Token used, delete it
            return HttpResponse("Password has been reset successfully.")
        else:
            return HttpResponse("Passwords do not match.", status=400)
        
    return render(request, 'reset_password.html', {'token': token})




def SetOfCoins(request):
    logged_user = request.session.get('user_id', None)
    if not logged_user:
        messages.error(request,'Login required to access this page')
        return redirect('login')
    data = UniverseCoinSet.objects.filter(user=logged_user)
    notifications = PushNotification.objects.filter(user=logged_user)
    combined_data = {}
    for i in data:
        set_id = i.set_name.id
        if set_id not in combined_data:
            combined_data[set_id] = {
                "set_name": i.set_name.set_name,
                "set_counts": i.coin_set.set_counts if i.coin_set else [],  # If i.coin_set exists
                "price": i.set_name.price,
                "number_of_sets": None
            }
        else:
            combined_data[set_id]["set_counts"] += i.coin_set.set_counts  # Merge lists
        min_count = min(item['count'] for item in i.coin_set.set_counts) if i.coin_set.set_counts else None
        combined_data[set_id]["number_of_sets"] = min_count
    # If you want to convert the combined_data dict to a list of dictionaries
    combined_data_list = list(combined_data.values())
    print(combined_data_list)
    context={
        'data': combined_data_list,
        'notifications' : notifications,
    }
    return render(request, 'setsOfCoins.html', context)
    