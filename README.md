# LOCAL THEATER

- 기능
    - 시나리오
    - 검색 시퀀스(서울 내) 
        - 1 : 위치  
            - 1-1 : 원하는 위치를 검색하면 지점을(branch) checkbutton or radiobutton으로 선택 할 수 있게 해 줌
            - 1-2 : 선택하면 해당 상세 정보 보여줌(crwaling 여석)
            - 1-3 : 필터를 통해 세부 조건 추가 가능(crwaling 여석)
            - 1-4 : 여석 갱신 버튼 클릭시 crwaling 
        - 2 : 제목 
            - 2-1 : 제목 and 관종류 검색(but 관종류는 null 가능)
            - 2-2 : 검색 조건에 맞는 지점을(branch) checkbutton or radiobutton으로 선택 할 수 있게 해 줌
            - 2-3 : 선택하면 해당 상세 정보 보여줌(crwaling 여석)
            - 2-4 : 필터를 통해 세부 조건 추가 가능(crwaling 여석)
            - 2-5 : 여석 갱신 버튼 클릭시 crwaling
    - 리뷰 
        - 1 : 입력창에 필터로 본인이 관람한 브랜드, 지점, 관 정해서 후기 입력 후 등록
        - 2 : 입력창 밑으로 원하는 후기를 볼 수 있게 필터를 두고 설정하지 않을시 모든 후기 보여주기

- 표기
    - 파이썬 변수 : 싱글카멜
    - html : - 케이스
    

- table
    - remain_seat은 사용자가 클릭시 
    - **theater**
        | 이름 | 형식 | 비고 |
        |:---:|:---:|:---:|
        | `id` | NUM | `pk` |
        | `company` | CharField(max_length=30) | 브랜드 |
        | `branch` | CharField(max_length=50) | 지점명 |
        | `num` | CharField(max_length=20) | ex.1관, 2관 |
        | `category` | CharField(max_length=20) | ex.일반관,특별관 ... |
        | `created_at` | DateTimeField(auto_now_add=True) | ex.일반관,특별관 ... |
        | `updated_at` | DateTimeField(auto_now=True) | ex.일반관,특별관 ... |
        | `lat` | DecimalField(max_digits=9, decimal_places=6) | 위도 |
        | `lon` | DecimalField(max_digits=9, decimal_places=6) | 경도 |
    - **movie** 
        | 이름 | 형식 | 비고 |
        |:---:|:---:|:---:|
        | `id` | NUM | `pk` |
        | `theater_id` | ForeignKey(Theater, on_delete=models.CASCADE) | `fk` |
        | `movie_name` | CharField(max_length=100) |  |
        | `showtime` | DateTimeField() | 상영 시작 시간 |
        | `created_at` | DateTimeField(auto_now_add=True) | ex.일반관,특별관 ... |
        | `updated_at` | DateTimeField(auto_now=True) | ex.일반관,특별관 ... |
        
    - **review**
        | 이름 | 형식 | 비고 |
        |:---:|:---:|:---:|
        | `id` | NUM | `pk` |
        | `theater_id` | ForeignKey(Theater, on_delete=models.CASCADE) | `fk` |
        | `user_id` | ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) | `fk` |
        | `contents` | TextField() | 후기 내용 |
        | `created_at` | DateTimeField(auto_now_add=True) | ex.일반관,특별관 ... |
        | `updated_at` | DateTimeField(auto_now=True) | ex.일반관,특별관 ... |
    - **user** -> django user 이용        