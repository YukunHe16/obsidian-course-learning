filters:
  and:
    - 'file.ext == "md"'
    - 'note.course == "{{COURSE_ID}}"'
    - not:
        - 'file.inFolder("templates")'
properties:
  lecture_no:
    displayName: 讲次
  date:
    displayName: 日期
  deadline_kind:
    displayName: 截止类型
  due_date:
    displayName: 截止日期
  date_window:
    displayName: 日期窗口
  due_time:
    displayName: 时间
  due_time_text:
    displayName: 来源时间原文
  timezone:
    displayName: 时区
  verification_status:
    displayName: 核验状态
  submission_platform:
    displayName: 提交平台
  status:
    displayName: 状态
views:
  - type: table
    name: 今日截止
    filters:
      and:
        - 'note.type == "deadline"'
        - 'note.status == "pending"'
        - 'note.due_date.isType("date")'
        - 'note.due_date == today()'
    order:
      - file.name
      - note.deadline_kind
      - note.due_date
      - note.date_window
      - note.due_time
      - note.due_time_text
      - note.timezone
      - note.submission_platform
      - note.verification_status
    sort:
      - property: note.due_time
        direction: ASC
  - type: table
    name: 未来 14 天截止日期
    filters:
      and:
        - 'note.type == "deadline"'
        - 'note.status == "pending"'
        - 'note.due_date.isType("date")'
        - 'note.due_date >= today()'
        - 'note.due_date <= today() + "14d"'
    order:
      - file.name
      - note.deadline_kind
      - note.due_date
      - note.date_window
      - note.due_time
      - note.due_time_text
      - note.timezone
      - note.submission_platform
      - note.verification_status
    sort:
      - property: note.due_date
        direction: ASC
      - property: note.due_time
        direction: ASC
  - type: table
    name: 待核验截止日期
    filters:
      and:
        - 'note.type == "deadline"'
        - 'note.status == "pending"'
        - or:
            - 'note.verification_status != "verified"'
            - 'note.date_status != "exact"'
    order:
      - file.name
      - note.deadline_kind
      - note.date_status
      - note.due_date
      - note.date_window
      - note.due_time
      - note.due_time_text
      - note.verification_status
      - note.source_locator
    sort:
      - property: note.due_date
        direction: ASC
  - type: table
    name: 已逾期
    filters:
      and:
        - 'note.type == "deadline"'
        - 'note.status == "pending"'
        - 'note.due_date.isType("date")'
        - 'note.due_date < today()'
    order:
      - file.name
      - note.deadline_kind
      - note.due_date
      - note.date_window
      - note.due_time
      - note.due_time_text
      - note.submission_platform
      - note.verification_status
    sort:
      - property: note.due_date
        direction: ASC
  - type: table
    name: 全部截止日期
    filters:
      and:
        - 'note.type == "deadline"'
    order:
      - file.name
      - note.deadline_kind
      - note.date_status
      - note.due_date
      - note.date_window
      - note.due_time
      - note.due_time_text
      - note.timezone
      - note.status
      - note.verification_status
      - note.submission_platform
      - note.source_locator
    sort:
      - property: note.due_date
        direction: ASC
      - property: file.name
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
