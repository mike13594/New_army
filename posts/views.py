from django.shortcuts import render,redirect, get_object_or_404
from posts.models import Comment, Post, PostImage, PlaceComplete
from posts.forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from seoul.models import Place

def main(request):
    return render(request, "main.html")

# 댓글 작성
@require_POST 
def comment_add(request, post_id):
    form = CommentForm(data = request.POST)
    if form.is_valid():
        comment = form.save(commit = False)
        comment.user = request.user
        comment.save()

        return redirect("post_detail", post_id=comment.post.id) #url 추가 , 댓글 생성한 후 리다이렉트할 페이지 post_detail?

# 댓글 삭제    
@require_POST
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()

    if comment.user == request.user:
        comment.delete()
        return redirect("post_detail") #url 추가, 댓글 삭제한 후 리다이렉트할 페이지 post_detail?
    
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")
    
# 여행 계획 상세보기
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm()
    if not post.complete and post.user != request.user:
        return redirect("main")  
    context = {
        "post": post,
        "comment_form": comment_form,
    }
    return render(request, "post_detail.html", context)# 요청 전달할 템플릿,post_detail.html

# 여행 계획 작성
def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit = False)
            post.user = request.user
            post.save()
            for image_file in request.FILES.getlist("images"):
                PostImage.objects.create(
                    post = post,
                    photo = image_file,
                )
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm()

    context = {"form": form}
    return render(request,"post_detail", context) # 요청 전달할 템플릿,post_add.html

# 여행 계획 수정
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden("권한이 없습니다.")
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)

    context ={
        "form": form
    }
    return render(request, "post_detail.html", context)# 요청 전달할 템플릿 ??edit.html?

# 여행 계획 삭제

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden("권한이 없습니다.")
    post.delete()
    return redirect("main") #포스트 삭제하고 어디 주소로 보내야할지 정해야함

# 여행 계획 완료 (Complete 버튼 누르면 공개)
def place_complete(request, post_id, place_id):
    place_complete = PlaceComplete.objects.get_or_create(
        post_id=post_id,
        place_id=place_id,
        user=request.user
    )
    place_complete.complete = not place_complete.complete
    place_complete.save()

    return redirect("post_detail",post_id=post_id)

# # 완료한 여행 계획 목록 (완료된 것만 공개) # 일단 만들엇는데 어디에 넣어야할지 모름
# def post_list(request):
#     posts = Post.objects.filter(is_complete=True).order_by("-created_at")
#     context = {
#         "posts": posts
#     }
#     return render(request, "pass", context) # 요청 전달할 템플릿,post_detail.html