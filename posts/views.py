from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from posts.models import Comment, Post, PostImage, PlaceComplete
from users.models import User
from posts.forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden, JsonResponse
from seoul.models import Place
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def main(request):
    posts = Post.objects.all()
    page = request.GET.get('page', 1)
    images = PostImage.objects.all()
    
    paginator = Paginator(posts,8)

    page_obj = paginator.get_page(page)

    context = {
        "posts": posts,
        "page_obj":page_obj,
        "paginator":paginator,
        "images": images,
    }
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

        return redirect("post:post_detail", post_id=comment.post.id) 

# 댓글 삭제    
@require_POST
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user.id == request.user.id:
        post_id=comment.post.id
        comment.delete()
        return redirect("post:post_detail", post_id=post_id) 
    
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")
    
# 여행 계획 상세보기
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = User.objects.get(id=post.user_id)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()
    completed_places_list = (
        PlaceComplete.objects.filter(post=post, user=request.user, complete=True)
        .values_list("place_id", flat=True)
    )  

    context = {
        "user" : user,
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
        form = PostForm(request.POST)  
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # 이미지 저장
            for image_file in request.FILES.getlist("photo",[]):
                PostImage.objects.create(post=post, photo=image_file)

            # 장소 저장
            place = request.POST.get("place", "").strip()
            if place:
                place_name_list = [place_name.strip() for place_name in place.split(",")]
                place_name_list = [name for name in place_name_list if name]
                for place_name in place_name_list:
                    place, _ = Place.objects.get_or_create(name=place_name) 
                    post.place.add(place)  

            return redirect("post:post_detail")  
        else:
            print("Form Errors:", form.errors)  

    else:
        form = PostForm()

    places = Place.objects.all()
    context = {
        "form": form, 
        "places": places,
        "is_edit":False,
    }
    return render(request, "make_post.html", context)
# 여행 계획 수정
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return HttpResponseForbidden("권한이 없습니다.")  # 다른 사용자가 수정 불가능

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            if "photo" in request.FILES:
                for image_file in request.FILES.getlist("photo"):
                    PostImage.objects.create(post=post, photo=image_file)

            post.place.clear()
            place = request.POST.get("place", "").strip()
            if place:
                place_name_list = [place_name.strip() for place_name in place.split(",")]
                place_name_list = [name for name in place_name_list if name]
                for place_name in place_name_list:
                    place, _ = Place.objects.get_or_create(name=place_name)
                    post.place.add(place)

            return redirect("post:post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)
    existing_places = ", ".join([place.name for place in post.place.all()])
    context = {
        "form": form, 
        "places": Place.objects.all(),
        "existing_places": existing_places, 
        "post": post,
        "is_edit":True,
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
    post = get_object_or_404(Post, id=post_id)
    place = get_object_or_404(Place, id=place_id)

    
    place_complete, created = PlaceComplete.objects.get_or_create(
        user=request.user,
        post=post,
        place=place
    )

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

@login_required
@csrf_exempt
def delete_post_image(request, image_id):
    try:
        image = PostImage.objects.get(id=image_id)

        if image.post.user != request.user:
            return JsonResponse({"error": "삭제 권한이 없습니다."}, status=403)

        image.delete()
        return JsonResponse({"success": True}, status=200)
    except PostImage.DoesNotExist:
        return JsonResponse({"error": "이미지를 찾을 수 없습니다."}, status=404)