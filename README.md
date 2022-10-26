# company_mgmt
----------
## 개발기간
#### 2022-10-24 ~ 2022-10-26

## 프로젝트 설명
 - 다국어를 지원하는 회사 정보 관리 서비스 개발
 - docker에서 db 실행
 - Todo: docker에서 app실행
 
 
## 사용된 기술
 - Python, FastAPI, Postgresql, sqlalchemy, docker
 
## ERD
<img width="196" alt="erd" src="https://user-images.githubusercontent.com/57758265/197950353-1dc895ad-434a-4229-9fcb-2afb8ae059ef.png">

## API_DOCS

### 회사명 자동 완성
- 회사명의 일부만 들어가도 검색이 가능
- header의 x-wanted-language 언어값에 따라 해당 언어로 출력

API URL

GET /search?query=

#### Request_header
|헤더명|형식|비고|
|:------:|:------:|:------:|
|x-wanted-language|str|"ko","en","ja"|

#### Response_body
|명칭|변수명|형식|비고|
|:------:|:------:|:------:|:------:|
|회사명 리스트||dictionary[]||
|회사명|company_name|str||


#### HTTP status code
| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | - | 정상종료 |
| 500 | Internal Server Error | | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    [
        {"company_name": "주식회사 링크드코리아"},
        {"company_name": "스피링크"},
    ]
}
```

2) 500

```json
{
    "Message": "Exception 내용"
}
```
### 회사 이름으로 회사 검색
- header의 x-wanted-language 언어값에 따라 해당 언어로 출력
- 검색된 회사가 없는 경우, 404를 리턴
API URL

GET companies/{str:company_name}

#### Request_header
|헤더명|형식|비고|
|:------:|:------:|:------:|
|x-wanted-language|str|"ko","en","ja"|

#### Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
|회사명|company_name|str||
|태그| tags | list |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | - | 정상 |
| 404 | - | - | 해당 회사 없음 |
| 500 | Internal Server Error |  | API 내부 에러 발생 |

Response Example

1) 200

```json
{
        "company_name": "원티드랩",
        "tags": [
            "태그_4",
            "태그_20",
            "태그_16",
        ],
    }
```

2) 500

```json
{
    "message": "Exception 내용"
}
```


### 새로운 회사 추가
- 새로운 언어(tw)도 같이 추가 가능
- 저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력

API URL

POST /companies

Request Body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| 회사명 | company_name | dict |  |
| 언어별 회사명 | "ko","en","tw" | str | |
| 태그 리스트 | tags | list | |
| 태그명 | tag_name | dict | |
| 언어별 태그명 | "ko","en","tw" | str | |

Request Example

```json
{
            "company_name": {
                "ko": "라인 프레쉬",
                "tw": "LINE FRESH",
                "en": "LINE FRESH",
            },
            "tags": [
                {
                    "tag_name": {
                        "ko": "태그_1",
                        "tw": "tag_1",
                        "en": "tag_1",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_8",
                        "tw": "tag_8",
                        "en": "tag_8",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_15",
                        "tw": "tag_15",
                        "en": "tag_15",
                    }
                },
            ],
        }
```

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| 회사명 | company_name | str | header에 따라 언어 변경 |
| 태그리스트 | tags | list | header에 따라 언어 변경 |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | | 정상종료 |
| 400 | Request Error | | 파라미터 형식 틀림 |
| 422 | Request Error | | 필수 파라미터 없음 |
| 500 | Internal Server Error | "exception 내용" | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "message": "success"
}
```

2) 400

```json
{
    "message": "company_name is not dict"
}
```

3) 500

```json
{
    "message": "Exception 내용"
}
```


### 태그명으로 회사 검색
- header의 x-wanted-language 언어값에 따라 해당 언어로 출력
- 태그로 검색 관련된 회사가 검색
- 다국어로 검색이 가능
- ko언어가 없을경우 노출가능한 언어로 출력합니다.
- 동일한 회사는 한번만 노출이 되어야합니다.

API URL

GET tags?query=

#### Request_header
|헤더명|형식|비고|
|:------:|:------:|:------:|
|x-wanted-language|str|"ko","en","ja"|

#### Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
|회사명|company_name|str||
|태그| tags | list |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | - | 정상 |
| 500 | Internal Server Error |  | API 내부 에러 발생 |

Response Example

1) 200

```json
[{
        "company_name": "원티드랩",
        "tags": [
            "태그_4",
            "태그_20",
            "태그_16",
        ],
    },
    {
        "company_name": "원티드랩",
        "tags": [
            "태그_4",
            "태그_20",
            "태그_16",
        ],
    }
    ]
```

2) 500

```json
{
    "message": "Exception 내용"
}
```


### 회사 태그 정보 추가
- 저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력

API URL

PUT companies/<str:company_name>/tags

#### Request_header
|헤더명|형식|비고|
|:------:|:------:|:------:|
|x-wanted-language|str|"ko","en","ja"|

Request Body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| 태그명 | tag_name | dict |  |
| 언어별 태그명 | "ko","tw","en" | str ||

Request Example

```json
[
                {
                    "tag_name": {
                        "ko": "태그_50",
                        "ja": "タグ_50",
                        "en": "tag_50",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_4",
                        "tw": "tag_4",
                        "en": "tag_4",
                    }
                },
            ]
```

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
|회사명|company_name|str||
|태그| tags | list |  |
HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | | | 정상종료 |
| 400 | Request Error |  | 파라미터 형식 틀림 |
| 422 | Request Error | | 파라미터 없음 |
| 500 | Internal Server Error | "Exception 내용.” | API 내부 에러 발생 |

Response Example

1) 200

```json
{
        "company_name": "Wantedlab",
        "tags": [
            "tag_4",
            "tag_16",
            "tag_20",
            "tag_50",
        ],
    }
```

2) 500

```json
{
    "message": "Exception 내용."
}
```

### 회사 태그 정보 삭제
- header의 x-wanted-language 언어값에 따라 해당 언어로 출력.

API URL

Delete companies/<str:company_name>/tags/<str:tag_name>

#### Request_header
|헤더명|형식|비고|
|:------:|:------:|:------:|
|x-wanted-language|str|"ko","en","ja"|

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
|회사명|company_name|str||
|태그| tags | list |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - |  | 정상종료 |
| 500 | Internal Server Error | "Exception내용.” | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "message": "게시물이 삭제되었습니다."
}
```

2) 500

```json
{
    "message": "서버 에러가 발생하였습니다."
}
```
## Unit test
- 주어진 유닛테스트 실행
<img width="324" alt="test_list" src="https://user-images.githubusercontent.com/57758265/197957551-398cfb61-4a30-4b59-a851-fd5e989a1904.png">



