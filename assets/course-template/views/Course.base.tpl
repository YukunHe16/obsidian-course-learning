filters:
  and:
    - 'file.ext == "md"'
    - 'note.course == "{{COURSE_ID}}"'
    - not:
        - 'file.inFolder("templates")'
properties:
  mastery:
    displayName: 掌握度
  review_stage:
    displayName: 复习阶段
  next_review:
    displayName: 下次复习
  lecture_no:
    displayName: 讲次
  date:
    displayName: 日期
  status:
    displayName: 状态
views:
  - type: table
    name: 今日到期
    filters:
      and:
        - 'note.type == "concept"'
        - 'note.status == "active"'
        - 'note.next_review.isType("date")'
        - 'note.next_review <= today()'
    order:
      - file.name
      - note.mastery
      - note.review_stage
      - note.next_review
    sort:
      - property: note.next_review
        direction: ASC
      - property: note.mastery
        direction: ASC
  - type: table
    name: 薄弱概念
    filters:
      and:
        - 'note.type == "concept"'
        - 'note.status == "active"'
        - 'note.mastery <= 2'
    order:
      - file.name
      - note.mastery
      - note.next_review
    sort:
      - property: note.mastery
        direction: ASC
      - property: note.next_review
        direction: ASC
  - type: table
    name: 待审核
    filters:
      or:
        - 'note.status == "draft"'
        - 'file.inFolder("wiki/pending")'
    order:
      - file.name
      - note.type
      - note.lecture_no
      - note.status
    sort:
      - property: file.mtime
        direction: DESC
  - type: table
    name: 最近学习
    filters:
      and:
        - 'note.type == "study-session"'
        - 'note.date.isType("date")'
        - 'note.date >= today() - "14d"'
    order:
      - file.name
      - note.date
      - note.mode
      - note.score
    sort:
      - property: note.date
        direction: DESC
