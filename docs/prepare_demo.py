"""Initialize a fresh LOCAL database for the README walkthrough.

Run from univProject: python manage.py shell < ../docs/prepare_demo.py
Existing records are never overwritten. Catalog data comes from backup.json;
lessons, materials and posts below are explicitly authored demonstration data.
"""
import json
from pathlib import Path
from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.db import transaction
from accounts.models import UserProfile
from search.models import Major, Question, ScoreRecord
from curriculums.models import Stage, Lesson, LessonScreen, LessonQuestion, LessonProgress, LessonReflection
from materials.models import Material
from posts.models import Post

if not settings.DEBUG:
    raise RuntimeError('This script is for local development with DEBUG=True only.')
if User.objects.exists() or Major.objects.exists() or Stage.objects.exists():
    raise RuntimeError('Use a fresh database. Existing data has been left unchanged.')

with transaction.atomic():
    # The committed backup uses CP949 and is missing its closing array bracket.
    source = (settings.BASE_DIR / 'backup.json').read_text(encoding='cp949').strip()
    try:
        records = json.loads(source)
    except json.JSONDecodeError:
        records = json.loads(source + ']')
    allowed = {'search.major', 'search.question', 'search.choice', 'search.choicescore', 'search.experience', 'search.experiencequestion'}
    catalog = [record for record in records if record['model'] in allowed]
    for obj in serializers.deserialize('json', json.dumps(catalog, ensure_ascii=False)):
        obj.save()

    major = Major.objects.get(pk=3)
    stages = [
        ('M03-S1', '콘텐츠 감각 찾기', '내 경험에서 전달의 강점을 발견하고, 콘텐츠의 대상과 메시지를 살펴봐요.', '나의 콘텐츠 경험 카드'),
        ('M03-S2', '콘텐츠 기획하기', '누구에게 어떤 이야기를 전할지 정하고, 한 편의 콘텐츠를 기획해봐요.', '콘텐츠 기획안'),
        ('M03-S3', '채널 운영해보기', '콘텐츠의 반응을 살펴보고, 다음 시도를 위한 개선점을 찾아봐요.', '채널 운영 기록'),
    ]
    lesson_titles = [
        ['나의 전달 경험 돌아보기', '콘텐츠의 대상과 메시지 찾기', '반응을 살피는 연습'],
        ['콘텐츠를 읽을 사람 정하기', '핵심 메시지 만들기', '첫 번째 콘텐츠 기획하기'],
        ['채널과 콘텐츠 연결하기', '반응을 기록하고 비교하기', '다음 콘텐츠 개선하기'],
    ]
    all_lessons = []
    previous = None
    for index, (stage_id, title, summary, deliverable) in enumerate(stages, 1):
        stage = Stage.objects.create(stage_id=stage_id, major=major, order=index, title=title,
            summary=summary, lesson_count=3, estimated_minutes=30, deliverable_name=deliverable,
            unlock_rule='전공 선택 완료' if index == 1 else '이전 단계 완료')
        for order, lesson_title in enumerate(lesson_titles[index-1], 1):
            lesson = Lesson.objects.create(lesson_id=f'{stage_id}-L{order}', stage=stage, order=order,
                title=lesson_title, card_summary='일상에서 해온 경험을 작은 배움으로 연결해요.',
                detail_intro='누군가에게 정보를 전했던 경험을 떠올리고, 나만의 강점을 정리해보세요.',
                core_activity='경험을 떠올리고 나만의 메시지 정리하기', duration_minutes=10,
                deliverable_name=deliverable, previous_lesson=previous)
            LessonScreen.objects.create(lesson=lesson, page_title=lesson_title, lesson_badge=f'{order}차시',
                lesson_intro=lesson.detail_intro, deliverable_label=deliverable, usage_label='나의 경험 정리',
                detail_cta='수업 완료하기', autosave_text='작성한 내용은 수업 완료 시 저장돼요.',
                complete_title='오늘의 배움을 완성했어요!', complete_subtitle='작은 시도가 새로운 시작이 됩니다.',
                result_section_title='나의 결과물', insight_title='발견한 나의 강점',
                insight_body='익숙한 경험에도 새로운 배움의 가능성이 있어요.', reflection_title='한 줄 소감',
                reflection_help='오늘 발견한 점을 남겨주세요.', reflection_placeholder='오늘의 배움은 어땠나요?',
                next_cta='다음 수업으로')
            for q_order, (label, question) in enumerate([('상황','어떤 상황이었나요?'),('나의 행동','어떻게 전달했나요?'),('결과','어떤 반응이 있었나요?')],1):
                LessonQuestion.objects.create(question_id=f'{lesson.lesson_id}-Q{q_order}',lesson=lesson,
                    order=q_order,result_label=label,question_text=question,help_text='내 경험을 편하게 적어주세요.',
                    placeholder='기억에 남는 경험을 적어주세요.',max_length=200)
            previous = lesson
            all_lessons.append(lesson)
    for lesson, following in zip(all_lessons, all_lessons[1:]):
        screen=lesson.screen; screen.next_lesson=following; screen.save()

    materials = [
        ('콘텐츠의 대상과 메시지 살펴보기', 'article', '관심 있는 게시물에서 핵심 메시지를 찾는 연습 자료입니다.', 'thumb_m03_s1_kocca_content.png'),
        ('나의 콘텐츠 경험 정리하기', 'practice', '일상에서 정보를 전했던 경험을 기록하는 실습 자료입니다.', 'thumb_m03_s2_kmooc_marketing.png'),
        ('처음 시작하는 콘텐츠 기획', 'lecture', '대상과 목적을 정하고 콘텐츠를 구상하는 학습 자료입니다.', 'thumb_m03_s2_kmooc_marketing.png'),
    ]
    # Reuse an existing thumbnail only; these entries do not claim to be real courses.
    library=settings.BASE_DIR / 'materials/static/assets/library'
    fallback=next(iter(sorted(library.glob('thumb_m03*.png')))).name
    for order,(title,kind,summary,thumbnail) in enumerate(materials,1):
        if not (library/thumbnail).exists(): thumbnail=fallback
        material=Material.objects.create(material_id=f'DEMO-M03-{order}',title=title,material_type=kind,
            provider='잇대 시연 자료',summary=summary,duration_text='10분',price_type='free',difficulty='입문',
            thumbnail_asset_key=thumbnail,source_url='',display_order=order,
            recommendation_reason='콘텐츠·채널 마케팅 전공을 처음 시작하는 분께 추천해요.')
        material.majors.add(major); material.stages.add(Stage.objects.get(stage_id='M03-S1'))
        material.lessons.add(all_lessons[0])

    demo_users=[]
    for username,nickname in [('readme_demo','새봄'),('readme_peer1','하루'),('readme_peer2','다온')]:
        user=User.objects.create_user(username=username,password='itdae-local-demo-2026')
        UserProfile.objects.create(user=user,nickname=nickname,selectedMajor=major,explorationStatus='selected')
        for lesson in all_lessons:
            LessonProgress.objects.create(user=user,lesson=lesson,status='in_progress' if lesson==all_lessons[0] else 'locked')
        demo_users.append(user)
    for user in demo_users[1:]:
        LessonReflection.objects.create(user=user,lesson=all_lessons[0],reflection_text='익숙한 경험에서 새로운 가능성을 발견했어요.')
    for user,title,content,category in [
        (demo_users[1],'우리의 첫 수업, 함께 시작해요!','처음이라 낯설지만 오늘의 작은 배움을 함께 나눠요.','info'),
        (demo_users[2],'일상에서 발견한 콘텐츠 아이디어','누군가에게 정보를 전했던 경험을 적어보니 새로운 아이디어가 떠올랐어요.','info'),
        (demo_users[1],'콘텐츠의 대상을 어떻게 정하나요?','첫 기획을 시작할 때 어떤 질문부터 해보면 좋을까요?','question'),
    ]:
        Post.objects.create(author=user,major=major,title=title,content=content,category=category)
    # These scores make recommendation screenshots reproducible without pretending
    # that the seeded account has completed a real survey.
    for major_id,score in [(3,10),(4,7)]:
        ScoreRecord.objects.create(user=demo_users[0],major_id=major_id,score=score)

print('Local demo data ready: readme_demo / itdae-local-demo-2026')
print('Search catalog: original repository. Lessons, materials and posts: demo examples.')
