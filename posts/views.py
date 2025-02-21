from django.shortcuts import render,redirect, get_object_or_404
from posts.models import Comment, Post, PostImage
from posts.forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

def main(request):
    return render(request, "main.html")

# 댓글 작성
@require_POST 
def comment_add(request):
    form = CommentForm(data = request.POST)
    if form.is_valid():
        comment = form.save(commit = False)
        comment.user = request.user
        comment.save()

        return redirect("pass") #url 추가 , 댓글 생성한 후 리다이렉트할 페이지 post_detail?

# 댓글 삭제    
@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id = comment_id)
    comment.delete()

    if comment.user == request.user:
        comment.delete()
        return redirect("pass") #url 추가, 댓글 삭제한 후 리다이렉트할 페이지 post_detail?
    
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")

# 글 작성
def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit = False)
            post.user = request.user
            post.save()

            # 이 아래 주석 내용은 pystagram의 포스트안에 사진 여러개 보여주기 기능
            # for image_file in request.FILES.getlist("images"):
            #     PostImage.objects.create(
            #         post = post,
            #         photo = image_file,
            #     )
            # postimage, post 생성 완료하면 어디로 이동할지 정해야함
            # 아래에 되있는건 리다이렉트할 url과 스크롤의 위치
           # url = f"/posts/feeds/#post-{post.id}" 넣어야함
            return redirect(url)
    else:
        form = PostForm()

    context = {"form": form}
    return render(request,"pass", context) # 요청 전달할 템플릿,post_add.html

# 완료한 여행 계획 목록 (완료된 것만 공개) # 일단 만들엇는데 어디에 넣어야할지 모름
def post_list(request):
    posts = Post.objects.filter(is_complete=True).order_by("-created_at")
    context = {
        "posts": posts
    }
    return render(request, "pass", context) # 요청 전달할 템플릿,post_detail.html


# 여행 계획 상세보기
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm()
    if not post.complete and post.user != request.user:
        return redirect("post_list")  # 본인만 초안 상태 글을 볼 수 있음
    context = {
        "post": post,
        "comment_form": comment_form,
    }
    return render(request, "pass", context)# 요청 전달할 템플릿,post_detail.html

# 여행 계획 수정
def post_edit(request, post_id):
    posts = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=posts)
        if form.is_valid():
            form.save()
            return redirect("pass", id=post_id)# 요청 전달할 템플릿,post_detail.html
    else:
        form = PostForm(instance=posts)
    context ={
        "posts": form
    }
    return render(request, "pass", context)# 요청 전달할 템플릿 ??edit.html?

# 여행 계획 삭제
def post_delete(request, post_id):
    posts = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        posts.delete()
        return redirect("post_list")
    context ={
        "posts": posts
    }
    return render(request, "pass", context) # 요청 전달할 템플릿 ??delete.html?

# 여행 계획 완료 (Complete 버튼 누르면 공개)
def post_complete(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.complete = True
    post.save()
    return redirect("pass", id=post_id) # 요청 전달할 템플릿,post_detail.html

