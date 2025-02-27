from django.shortcuts import render, redirect, get_object_or_404
from users.forms import LoginForm, SignupForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from users.models import User
from posts.models import Post, PlaceComplete
from seoul.models import Place
# from django.http import HttpResponse

# Create your views here.
# 로그인 처리
def login_view(request):
    # print('request.user : ', request.user)
    # 로그인 user 유효성 검증하는 부분
    if request.user.is_authenticated:
        return redirect("/user/profile/")
    
    # LoginForm 에서 로그인 버튼을 누르면 처리하는 부분 
    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # username, password에 해당하는 사용자가 있는지 검사
            # 해당 정보가 있는지 여부 확인, 정보가 없으면 None 반환
            user = authenticate(username=username, password=password)

            # 해당 사용자가 존재하면
            if user:
                # 로그인 처리 후, 게시글 첫 화면으로 redirect
                login(request, user)
                return redirect("/user/profile/")
            
            # 사용자가 없다면 form에서 에러 추가
            else:
                auth_after_error = "입력한 자격증명에 해당하는 사용자가 없습니다."
                # form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다.")

        # 어떤 경우든지 실패한 경우 다시 LoginForm을 사용한 로그인 페이지 렌더링
        context = {"form" : form, "message" : auth_after_error}
        return render(request, "login.html", context)    

    else:
        # LoginForm 빈 인스턴스를 생성
        form = LoginForm()

        context = {
            "form" : form
        }

        return render(request, "login.html", context)

# 로그아웃 처리
def logout_view(request):
    # logout 함수 호출에 request를 전달
    logout(request)

    # logout 처리한 후 로드인 페이지로 이동
    return redirect("/user/login/")         

# 회원 가입 처리
def signup(request):
    if request.method == "POST":
        form = SignupForm(data = request.POST, files = request.FILES)

        # Form에 에러가 없다면 form의 save() 메서드로 사용자를 생성
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            return redirect("/post/")

    # GET 요청에서는 빈 form을 보여줌
    else:
        # SignupForm 인스턴스를 생성, Template에 전달
        form = SignupForm()

    context = {"form":form}
    return render(request, "signup.html", context) 

# 프로필 정보 보여주기
def profile(request):
    # 로그인 user 유효성 검증이후 로그인한 사람의 username으로 
    # 사용자 프로필 정보를 조회한다.
    # print("request.user.username : ", request.user.username)
    user = get_object_or_404(User, username = request.user.username)
    # print("user : ", user)
    # 조회하여 정보가 있으면 프로필 정보 화면으로 데이터를 넘겨준다.

    # 명소 답사하여 complete를 체크한 건수
    complete_cnt = PlaceComplete.objects.filter(complete=True)
    if complete_cnt:
        complete_cnt 
    else:
         complete_cnt = 0

    # 명소 전체 건수 조회
    place_cnt = Place.objects.all()

    if place_cnt:
        place_cnt
    else:
        place_cnt = 0

    # 진척률
    progress_per = len(complete_cnt) * 100 / len(place_cnt)
    print("progress_per : ", round(progress_per))        

    context = {"user": user, "complete_cnt" : len(complete_cnt), "place_cnt" : len(place_cnt), "progress_per" : round(progress_per)}
    # return HttpResponse("ok")
    return render(request, "profile.html", context) 

# 프로필 정보 수정
def profile_edit(request, user_id):
    # 프로필 정보 화면에서 사용자 id를 가지고서 사용자 정보를 조회한다.
    profile = get_object_or_404(User, pk = user_id)
    # 프로필 정보 중 수정된 항목 데이터를 가지고서 작성완료버튼을 누른다.
    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance = profile)

        # 수정된 데이터 항목이 유효한지 검증한다.
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect("/user/profile/")
        else:
            print("form_error :", form.errors)
        
    # GET 방식으로, 넘겨진 프로필 정보를 화면에 보여준다.
    else:
        form = ProfileForm(instance = profile)        
    context = {
        "profile" : profile,
        "form" : form,
    }
    return render(request, "profile_edit.html", context)
    # return HttpResponse("ok")

# 프로필 정보 삭제(사용자 삭제)
def profile_delete(request, user_id):
    profile = get_object_or_404(User, pk = user_id)
    profile.delete()

    return redirect("/user/login/")
    
