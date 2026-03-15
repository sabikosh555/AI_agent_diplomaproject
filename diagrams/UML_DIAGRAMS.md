# UML диаграммалары — Университеттің қызметі бойынша AI агент

![UML диаграмма](uml.png)

---

## Сипаттама

Жоғарыда көрсетілген UML диаграмма жобаның деректер модельін (ER — Entity-Relationship) және жүйе құрылымын көрсетеді.

### Атрибуттары

| Модель | Сипаттама | Атрибуттары |
|---------|-----------|-----------------|
| **Пайдаланушы** (User) | Django аутентификация модельі. Студенттер мен қызметкерлер. | id, username, email, first_name, last_name, is_staff |
| **Студент профилі** (StudentProfile) | Студенттің қосымша мәліметтері. User-мен 1:1 байланыс. | student_id, course, faculty, specialty |
| **Құжат** (Document) | Құжат сұрауы. User-ге тәуелді. | doc_type, status, created_at |
| **Баға** (Grade) | Пән бойынша баға. User-ге тәуелді. | subject, score, exam_status, status |
| **Кесте** (Schedule) | Сабақ кестесі. Курс бойынша сұрыпталады. | day, time_start, time_end, subject, course |
| **Хабарлама** (Notification) | Студентке хабарлама. User-ге тәуелді. | title, message, created_at, is_read |

### Байланыстар

| Байланыс | Кардиналдық | Сипаттама |
|----------|-------------|-----------|
| User ↔ StudentProfile | 1:1 | Бір пайдаланушының бір профилі |
| User → Document | 1:N | Бір пайдаланушы көп құжат сұрауын жасай алады |
| User → Grade | 1:N | Бір пайдаланушыға көп баға |
| User → Notification | 1:N | Бір пайдаланушыға көп хабарлама |
| StudentProfile ⋯ Schedule | логикалық | Профильдегі course өрісі кесте course-ымен сәйкес |

### Жүйе компоненттері

| Компонент | Сипаттама |
|-----------|-----------|
| **main** | Бас бет (index) |
| **cabinet** | Аутентификация, жеке кабинет, AI көмекші, Chat API, қызметкер панелі |
| **AI қызметі** | OpenAI интеграциясы, локальді кілт сөздер |
| **Дерекқор** | User, StudentProfile, Document, Grade, Schedule, Notification |
