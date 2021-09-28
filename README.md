# DjangoProject

Python Django Pybo 게시판 프로젝트

## 소개

- Do it! 점프 투 장고 교재의 Pybo 실습 프로젝트 기반
- 실습한 프로젝트 기반으로 기능 확장

## 추가된 기능

1. 개인정보 / 비밀번호 수정 기능 추가

2. 게시글 검색 기능 추가

3. 게시글 내 채택 기능 추가
    - 채택 기능 구현을 위한 게시글 필드 추가(accepted)

4. 프로필 추가
    - 본인이 작성한 게시글, 답변을 남긴 게시글 조회 가능
    - 각각 조회 시 페이지네이션 적용

5. 게시글 작성 시 에디터 추가
    - TextArea -> Summernote 에디터 사용
    - Summernote 에디터 사용 시 html 형식으로 게시글 / 답변이 저장 된다. 
        - 이 과정에서 <, >등은 이스케이프 처리 되는걸 확인함. 
        - 따로 XSS 처리할 필요는 없어 보임.
    - html 형식을 그대로 불러오기 위해 Django의 safe 필터를 사용

6. 메인 화면에 조회수 top3, 최근에 답변이 남겨진 게시글 표시
    - 조회수 표시 부분은 문제가 없었으나, 
    - 최근에 답변이 남겨진 게시글 조회 파트 구현할 때 중복이 발견되어 distinct('속성명')을 사용하고 싶었으나 동작하지 않아서 직접 구현함
        - 이유는 MySQL과 SQLite에서는 distinct('속성명')을 지원하지 않고 PostgreSQL에서 사용 가능하다고 함.
    - set을 통해 중복이 아닌 게시글 지정한 개수만큼(3개) 가져오도록 처리
    ``` python
    def index(request):
        page = request.GET.get('page', '1')
        query = request.GET.get('query', '')
        question_list = Question.objects.filter(subject__contains=query).order_by('-create_date')
        paginator = Paginator(question_list, 10)
        page_obj = paginator.get_page(page)

        # 최다 조회수
        greatest_hits_list = Question.objects.order_by('-hits')[:3]

        # 최근에 답변이 달린 게시글
        temp = Answer.objects.order_by('-create_date').values('question')
        recently_answered_list = []
        duplicated = set()

        # 하나의 게시글에 여러개의 답변이 달릴 수 있으므로 중복 제거
        for answered_question in temp:
            if answered_question['question'] not in duplicated:
                duplicated.add(answered_question['question'])
                recently_answered_list.append(answered_question['question'])
                if len(recently_answered_list) == 3:
                    break

        recently_answered_list = Question.objects.filter(id__in=recently_answered_list)

        context = {
            'question_list': page_obj,
            'greatest_hits_list': greatest_hits_list, 
            'recently_answered_list': recently_answered_list,
            'query': query,
        }

        return render(request, 'pybo/question_list.html', context)
    ```

7. 게시판 추가 
    - 자유게시판, 자바게시판, 파이썬 게시판
    - 메인 페이지에서는 전체 게시판의 게시글들을 보여주고, 각 게시판 페이지에서는 해당 게시판의 게시글만 보여지도록 함

8. DataBase 수정 ( SQLite -> MySQL )
    - 기본적으로 Django에서는 SQLite를 제공 
    - SQLite도 충분히 프로젝트에 적용 가능하지만 다른 데이터베이스로 확장하는 실습을 해보고 싶어 이동해 봄.
    ``` python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS':  {
                    'read_default_file': os.path.join(BASE_DIR, 'djangoproj.cnf'),
                }
        }
    }
    ```
    - djangoproj.cnf
    ```
    [client]
    database = djangoproject
    user = root
    password = root
    default-character-set = utf8
    host = 127.0.0.1
    port = 3306
    ```

9. 댓글 / 답변 시 게시글/답변 주인에게 알림 가는 기능 구현
    - API가 아닌 페이지 로딩 시 알림을 로드하게 되면 페이지 로딩하는 모든 뷰에 알림 로드 부분을 추가해야 하는 문제가 있음..
    - 따라서, API를 만든 후, Navbar 불러올 때 API 호출하여 알림을 불러오는 기능 추가
    - API 구현은 DjangoRestFramework를 사용하여 쉽게 구현
    - API 호출 시 로그인 여부 확인하여 로그인 되어있지 않으면 PermissionDenied 반환

    ``` python
    class NotificationViewSet(viewsets.ModelViewSet):
        queryset = Notification.objects.all()
        serializer_class = NotificationSerializer
        MAX_NOTIFICATION_COUNT = 15

        @action(detail=False, methods=['get'])
        def get_notification_information(self, request):
            if request.user.is_authenticated:
                notification = Notification.objects.filter(user=request.user, isread=False)[:self.MAX_NOTIFICATION_COUNT]
                serializer = self.get_serializer(notification, many=True)
                return Response(serializer.data)
            else:
                return PermissionDenied()

        @action(detail=True, methods=['get'])
        def change_notification_status(self, request, pk=None):
            if request.user.is_authenticated:
                notification = self.get_object()
                #serializer = NotificationSerializer(request.data)
                #if serializer.is_valid():
                if notification != None:
                    notification.isread = True
                    notification.save()
                    return Response({'status':'save successfully'})
                else:
                    return Response({'status':'save failed'})
            else:
                return PermissionDenied()
    ```

# 실행 화면

- 회원 정보 수정이나 비밀번호 수정 화면은 포함하지 않음.

<hr>

## 메인 화면

![image](https://user-images.githubusercontent.com/76891875/135045697-40e2e295-074a-4049-86dc-bdbe57c808f5.png)

## 상세 페이지

![image](https://user-images.githubusercontent.com/76891875/135045891-ebd59900-de98-4e23-a259-e0203c77a575.png)

## 개별 게시판

![image](https://user-images.githubusercontent.com/76891875/135046313-b6fead73-1af8-4d64-a48f-465303cd3d2e.png)

## 게시글 작성

![image](https://user-images.githubusercontent.com/76891875/135045994-9bb21275-d757-457f-8a46-2cc8b113e673.png)

## 프로필

![image](https://user-images.githubusercontent.com/76891875/135046139-aba653bc-2dbc-4d2c-be18-ae2383a134d3.png)

## 알림

![image](https://user-images.githubusercontent.com/76891875/135046548-5a970b0b-5b33-4cb4-86f8-82abf1ca708d.png)




