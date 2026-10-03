# README 이미지와 로컬 시연

## 실제 화면 캡처

- 기준 코드: `2026-HERETHON/2026-herethon-16`, `main`의 `604e397`.
- 환경: Python 3.12.14, Django 6.0.6, SQLite, 모바일 뷰포트 393 × 852.
- 실행: `python manage.py runserver 127.0.0.1:8765`.
- 원본 앱의 템플릿, CSS, JavaScript, view 코드를 변경하지 않고 브라우저에서 캡처했습니다.
- 캡처 시점의 화면을 그대로 저장했으며 주요 기능 이미지는 AI 생성 이미지가 아닙니다.

| 파일 | 로컬 화면 | 캡처 상태 |
| --- | --- | --- |
| `readme_images/screenshots/exploration.jpg` | `/search/select1/` | 원본 설문, 선택지 1개 선택 |
| `readme_images/screenshots/my-major.jpg` | `/curriculums/my-major/` | 콘텐츠·채널 마케팅 전공의 첫 수업 |
| `readme_images/screenshots/materials.jpg` | `/materials/?scope=all` | 전체 전공 자료 탭 |
| `readme_images/screenshots/community.jpg` | `/posts/` | 우리 전공 탭, 동료 소감과 게시글 |

## 데이터 범위

저장소의 `backup.json`은 CP949로 인코딩되어 있고 배열의 닫는 대괄호가 누락되어 있습니다. `docs/prepare_demo.py`는 메모리에서만 이를 보완해 전공·설문·선택지·전공별 점수·체험 수업 카탈로그를 읽습니다. 원본 파일은 수정하지 않습니다.

이 백업에는 학습 단계, 정규 수업, 학습 자료, 게시글 데이터가 없어 로컬 시연용 예시를 새로 구성했습니다. 화면의 수업 제목·진도·자료·게시글·동료 수는 이 예시 데이터이며 실제 사용자 활동이나 서비스 운영 실적을 뜻하지 않습니다. 자료 제목은 가상의 연습 자료이고 외부 강의의 존재나 제공자를 주장하지 않습니다.

기존 백업의 사용자, 비밀번호 해시, 세션, 관리자 로그는 가져오지 않습니다. 시연 스크립트는 DEBUG 환경의 빈 데이터베이스에서만 실행되고 이미 데이터가 있으면 덮어쓰지 않고 중단합니다.

## 디자인 자산

- `readme-banner.png`: 앞서 확정한 시안에서 내장 ImageGen으로 제작한 민트색 배너. 서비스 화면이 아닌 README 장식용 이미지입니다.
- `journey.svg`, `service-flow.svg`: README를 위한 단계별 안내 그림.
- `badges/*.svg`: 외부 이미지 서비스에 의존하지 않는 기술 이름 배지.
- 팀원 이미지: 저장소의 `readme_images/이름.png` 원본을 그대로 사용했습니다.

배너 제작 프롬프트: “확정된 README 시안의 상단 민트색 배너만 독립된 가로 이미지로 제작. 잇대 로고와 연결 곡선, 책·학사모·길 일러스트를 유지하고 ‘2026 HE:REthon · TEAM 16’, ‘다시 시작하는 당신에게, 두 번째 대학을 잇다’, ‘전공 탐색부터 학습, 동료와의 연결까지’를 정확히 표기. 다른 README 영역과 브라우저 테두리는 제외.”
