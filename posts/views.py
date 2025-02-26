from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from posts.models import Comment, Post, PostImage, PlaceComplete
from posts.forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from seoul.models import Place
from django.contrib.auth.decorators import login_required

def main(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "main.html", context)

# 댓글 작성
@require_POST 
def comment_add(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(data = request.POST)
    if form.is_valid():
        comment = form.save(commit = False)
        comment.user = request.user
        comment.post = post
        comment.save()

        return redirect("post:post_detail", post_id=comment.post.id) #url 추가 , 댓글 생성한 후 리다이렉트할 페이지 post_detail?

# 댓글 삭제    
@require_POST
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user.id == request.user.id:
        post_id=comment.post.id
        comment.delete()
        return redirect("post:post_detail", post_id=post_id) #url 추가, 댓글 삭제한 후 리다이렉트할 페이지 post_detail?
    
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")
    
# 여행 계획 상세보기

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()

    completed_places_list = (
        PlaceComplete.objects.filter(post=post, user=request.user, complete=True)
        .values_list("place_id", flat=True)
    )  

    context = {
        "post": post,
        "places": post.place.all(),  
        "comments": comments,
        "comment_form": comment_form,
        "completed_places_list": list(completed_places_list),  
    }
    return render(request, "post_detail.html", context)

# 여행 계획 작성
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()

            places = request.POST.get("places", "")  
            
            valid_places = Place.objects.filter(name__in=places)  
            print("유효한 장소:", valid_places)  
            post.place.set(valid_places)  

            # 이미지 저장
            for image_file in request.FILES.getlist("photo"):
                PostImage.objects.create(post=post, photo=image_file)

            place = request.POST.get("place")
            if place:
                place_name_list = [place_name.strip() for place_name in place.split(",")]
                for place_name in place_name_list:
                    place, _ = Post.objects.get_or_create(
                        name = place_name,
                    )
                    post.place.set(place)

            return redirect("post:main")  
        else:
            print("Form Errors:", form.errors)  

    else:
        form = PostForm()

    places = Place.objects.all()
    context = {
        "form": form, 
        "places": places,
    }
    return render(request, "make_post.html", context)
# 여행 계획 수정
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return HttpResponseForbidden("권한이 없습니다.")  # 다른 사용자가 수정 불가능

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save_m2m()

            # 여행 장소 수정
            places = request.POST.getlist("places")
            post.place.set(places)

            # 이미지 추가
            for image_file in request.FILES.getlist("images"):
                PostImage.objects.create(post=post, photo=image_file)

            return redirect("post:post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)
    places = Place.objects.all()
    context = {
        "form": form, 
        "places": places, 
        "post": post
        }

    return render(request, "make_post.html", context )

# 여행 계획 삭제

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden("권한이 없습니다.")
    post.delete()
    return redirect("post:main") #포스트 삭제하고 어디 주소로 보내야할지 정해야함

# 완료
@login_required
def place_complete(request, post_id, place_id):
    print("함수 진입")
    post = get_object_or_404(Post, id=post_id)
    place = get_object_or_404(Place, id=place_id)

    
    place_complete, created = PlaceComplete.objects.get_or_create(
        user=request.user,
        post=post,
        place=place
    )
    print(place_complete)

    if not place_complete.complete:  
        place_complete.complete = True
        place_complete.save()

    return redirect(reverse("post:post_detail", kwargs={"post_id": post.id}))

# 완료 해제
@login_required
def place_uncomplete(request, post_id, place_id):
    post = get_object_or_404(Post, id=post_id)
    place = get_object_or_404(Place, id=place_id)

    try:
        place_complete = PlaceComplete.objects.get(user=request.user, post=post, place=place)

        if place_complete.complete:  
            place_complete.complete = False
            place_complete.save()

    except PlaceComplete.DoesNotExist:
        print(f" 완료 데이터 없음: post_id={post_id}, place_id={place_id}, user={request.user}")
    
    return redirect(reverse("post:post_detail", kwargs={"post_id": post.id}))