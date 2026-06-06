# UX Design Specification — LifeLog
## 발달장애인 생애전주기 기록 플랫폼 — 반응형 웹 (Responsive Web) & 모바일 앱 (Mobile App) 디자인

---

## 문서 정보 (Document Information)

| 항목 (Item) | 내용 (Content) |
|------|------|
| **문서 버전** (Document Version) | v1.0 |
| **작성일** (Date) | 2020년 |
| **Design System** | BrandBI (라이프네스트·소유드·어울) |
| **연계 문서** (Related Docs) | `PRD v1.0` · `Workflow Definition v1.0` · `BrandBI v1.0` |
| **접근성 기준** (Accessibility) | WCAG 2.1 AA 준수 |

---

## 목차 (Table of Contents)

1. 디자인 원칙 (Design Principles)
2. 브레이크포인트 및 뷰포트 전략 (Responsive Breakpoints & Viewport Strategy)
3. 글로벌 레이아웃 시스템 (Global Layout System)
4. 화면 목록 (Screen Inventory)
5. 컴포넌트 라이브러리 (Component Library)
6. 인터랙션 패턴 (Interaction Patterns)
7. 이지 모드 (Easy Mode / 당사자 모드)
8. 접근성 및 다국어 (Accessibility & Localization)
9. 브레이크포인트 × 기능 행렬 (Breakpoints × Feature Matrix)

---

## 1. 디자인 원칙 (Design Principles)

| 원칙 (Principle) | 설명 (Description) |
|------|------|
| **당사자 중심** (Person-Centered) | 당사자(장애인)가 자신의 기록 (Record)에 접근·수정할 수 있어야 함 |
| **보호자 우선** (Guardian-First) | 보호자가 이동 중 스마트폰으로 빠르게 기록 조회 및 PDF 생성 |
| **전문인력 효율** (Professional Efficiency) | 사회복지사는 PC에서 효율적으로 케이스 (Case) 관리 |
| **쉬운 모드** (Easy Mode) | 당사자용 인터페이스는 텍스트 단순화, 버튼 대형화, 설명 포함 |
| **B2G 신뢰** (B2G Trust) | 공공기관 대상 신뢰감 있는 디자인 |
| **일관성** (Consistency) | 5개 역할이 같은 플랫폼에서 동일한 디자인 시스템 사용 |

---

## 2. 브레이크포인트 및 뷰포트 전략 (Responsive Breakpoints & Viewport Strategy)

| 브레이크포인트 (Breakpoint) | 용도 (Purpose) | 대상 기기 (Target Device) |
|------|------|------|
| `S` ≤ 480px | Small Mobile | 스마트폰 (세로) |
| `M` ≤ 768px | Large Mobile / Small Tablet | 스마트폰 (가로), 작은 태블릿 |
| `T` ≤ 1024px | Tablet | iPad, Surface |
| `D` ≤ 1280px | Desktop | 일반 PC |
| `L` > 1280px | Large Desktop | 대형 모니터 |

### 주요 전략 (Key Strategies)

- **모바일 퍼스트 (Mobile First)**: S 브레이크포인트 (Breakpoint) 부터 시작, T 이상에서 레이아웃 (Layout) 확장
- **터치 타겟 (Touch Target)**: S = 48px, M = 44px, D+ = 40px (이지 모드 (Easy Mode) = 64px)
- **콘텐츠 너비 (Content Width)**: S = 100%, T = 100%, D = 1140px max

---

## 3. 글로벌 레이아웃 시스템 (Global Layout System)

### 3.1 공통 컴포넌트 (Common Components)

| 컴포넌트 (Component) | S (Mobile) | T (Tablet) | D+ (Desktop) |
|------|------|------|------|
| **헤더 (Header)** | 스크롤 시 고정 top-bar (앱바) | 고정 top-bar | 고정 top-bar + 세로 내비게이션 (Navigation) |
| **내비게이션 (Navigation)** | 바텀 바 (Bottom Bar) 5개 | 바텀 바 (Bottom Bar) / 상단 헤더 (Header) | 사이드 메뉴 (세로 280px) |
| **크럼 (Bread Crumb)** | 숨김 (탭 (Tab)바로 대체) | 숨김 | 상단에 표시 |
| **푸터 (Footer)** | 고정 하단 | 고정 하단 | 사이드 메뉴 하단에 통합 |
| **드로어 (Drawer)** | 바텀 시트 (Bottom Sheet) | 사이드 시트 | 고정 사이드 메뉴 |
| **토스트 (Toast)** | 하단 고정 (Full width) | 하단 우측 | 상단 우측 |
| **모달 (Modal)** | Full screen overlay | Center (60%의 너비) | Center (40%의 너비, max 600px) |
| **다이얼로그 (Dialog)** | 바텀 시트 (Bottom Sheet) | Center 모달 (Modal) | Center 다이얼로그 (Dialog) |
| **테이블 (Table)** | 카드 (Card) 뷰 (각 행 = 카드 (Card)) | 4열 이상 | 풀 테이블 (Table) |
| **폼 (Form)** | Single column, full width | Single column | Multi-column (2~3열) |

### 3.2 헤더 (Header) / 내비게이션 (Navigation)

| 브레이크포인트 (Breakpoint) | 헤더 (Header) | 내비게이션 (Navigation) |
|------|------|------|
| **Desktop** | 상단 헤더 (Header): 로고 좌측, 검색 중앙, 프로필 우측 + 역할 (Role) 정보 | 왼쪽 사이드바 (280px, scrollable) 내비게이션 (Navigation) |
| **Tablet** | 상단 헤더 (Header) + 역할 (Role) 뱃지 (Badge) | 상단 탭 (Tab)바 또는 햄버거 메뉴 |
| **Mobile** | 상단 헤더 (Header) + 역할 (Role) 뱃지 (Badge) + 햄버거 메뉴 | 하단 탭 (Tab)바 (5개 기본 탭 (Tab)) |

### 3.3 역할 (Role) 뱃지 (Badge)

| 역할 (Role) | S | T | D+ |
|------|------|------|------|
| **보호자 (Guardian)** | 🔒 보호자 (Guardian) | 🔒 보호자 (Guardian) | 🔒 보호자 (Guardian) — 전체 사이드바 |
| **당사자 (Person)** | 👤 당사자 (Person) | 👤 당사자 (Person) | 👤 당사자 (Person) — 이지 모드 (Easy Mode) 버튼 포함 |
| **사회복지사 (Social Worker)** | 📋 사회복지사 (Social Worker) | 📋 사회복지사 (Social Worker) | Full 사이드바 |
| **특수교사 (Special Teacher)** | 📚 특수교사 (Special Teacher) | 📚 특수교사 (Special Teacher) | Full 사이드바 |
| **활동지원사 (Support Worker)** | 🔁 활동지원사 (Support Worker) | 🔁 활동지원사 (Support Worker) | Full 사이드바 |

---

## 4. 화면 목록 (Screen Inventory)

### 4.1 공통 (Common) — 모든 역할 (Role)

#### 공통 화면 (Common Screen)

| ID | 화면 (Screen) | S | T | D+ | 설명 (Description) |
|------|------|------|------|------|------|
| C-001 | **스플래시 (Splash) / 온보딩 (Onboarding)** | 100% | 100% | 40% 너비 | 브랜드 소개, 주요 3개 기능 소개 |
| C-002 | **로그인 (Login) / 이메일 OTP** | 100% | 60% | 40% center | 이메일+비밀번호. OTP 토큰으로 로그인 |
| C-003 | **역할 (Role) 온보딩 (Onboarding)** | 100% | 60% | 40% center | 역할 (Role) 선택: 보호자 / 당사자 / 전문인력 |
| C-004 | **대시보드 (Dashboard) (Main)** | 100% | 100% | 100% | 역할 (Role)별 대시보드 (Dashboard) — 상단 요약, 기록 (Record) 리스트 |
| C-005 | **기록 상세 (Record Detail)** | 100% | 100% | 100% | 기록 (Record) 상세: 필드값, 첨부파일, 이력 |
| C-006 | **기록 생성/수정 (Create/Edit Record)** | 100% | 60% | 40% center | 템플릿 (Template) 기반 폼 (Form): 10가지 필드 타입 |
| C-007 | **검색 (Search) / 필터 (Filter)** | 100% | 60% | 40% center | 생애주기+카테고리+날짜+키워드 |
| C-008 | **PDF 출력 (PDF Output)** | 100% | 60% | 40% center | PDF 생성: 선택 기록 (Record) → 생성 |
| C-009 | **알림 센터 (Notification Center)** | 100% | 100% | 40% center | 읽지 않은 알림, 읽음 처리 |
| C-010 | **설정 (Settings) / 프로필 (Profile)** | 100% | 60% | 40% center | 비밀번호 변경, 이메일 변경, 역할 (Role) 변경 요청 |

#### 인증 (Auth) & 프로필 (Profile) 화면

| ID | 화면 (Screen) | S | T | D+ | 설명 (Description) |
|------|------|------|------|------|------|
| C-011 | **역할 (Role) 등록 (Register with Role)** | 100% | 60% | 40% center | 역할 (Role) 선택 + 이메일 + 비밀번호 |
| C-012 | **이메일 인증 (E-Mail Verification)** | 100% | 60% | 40% center | 인증 링크 발송 및 수신 확인 |
| C-013 | **비밀번호 찾기 (Password Lost)** | 100% | 60% | 40% center | 이메일 OTP 기반 임시 비밀번호 |
| C-014 | **계정 설정 (Account Settings)** | 100% | 60% | 40% center | 프로필 (Profile), 알림 설정, 탈퇴 |

### 4.2 보호자 (Guardian)

| ID | 화면 (Screen) | S | T | D+ | 설명 (Description) |
|------|------|------|------|------|------|
| G-001 | **보호자 대시보드 (Guardian Dashboard)** | 하단 탭 (Tab): 대시보드 (Dashboard) | 하단 탭 (Tab): 대시보드 (Dashboard) | 사이드바+메인 | 가족 목록(상단), 최근 기록 (Record)(본문), PDF 출력 바로가기 |
| G-002 | **가족 구성원 목록 (Family Member List)** | Full list | Grid 2열 | Table+Tree | 각 당사자 카드 (Card) + 권한 (Permission) 상태 + 버튼 |
| G-003 | **타임라인 뷰 (Timeline View)** | Vertical scroll | Vertical scroll | Horizontal timeline | 생애주기별 이벤트 흐름 |
| G-004 | **카테고리 필터 (Category Filter)** | Bottom sheet | Slide drawer | Fixed header | 생애주기 / 카테고리 / 날짜 / 상태 (State) |
| G-005 | **공유 / 내보내기 (Share / Export)** | Bottom sheet | Slide drawer | Center 모달 (Modal) | PDF 생성, 링크 공유, CSV 출력 |

### 4.3 당사자 (Person)

| ID | 화면 (Screen) | S | T | D+ | 설명 (Description) |
|------|------|------|------|------|------|
| P-001 | **당사자 대시보드 (Person Dashboard)** | Full layout | 80% 너비 (이지 모드 (Easy Mode)) | Center (이지 모드 (Easy Mode)) | 간단한 카드 (Card) 2개: 최근 기록 (Record), 다음 예약 |
| P-002 | **당사자 기록 열람 (Person Record Read)** | Full layout | 100% | 60% | 읽기 전용. Large text, icon-heavy |
| P-003 | **당사자 자기 기록 작성 (Self Recording)** | 1면 1필드 | Half-screen | Single-field-per-screen | 1면 1필드. 예: "오늘 기분이 어때요?" (이모티콘) |
| P-004 | **당사자 프로필 (Profile) & 목표 (Goals)** | Full layout | 80% 너비 | Center (Simple) | 간단한 프로필 (Profile), 목표 진행도 |
| P-005 | **당사자 알림 (Notification)** | Full layout | Full layout | Center 모달 (Modal) | 알림 (간단 텍스트+이모티콘) |
| P-006 | **당사자 이지 모드 (Easy Mode) 토글** | Top toolbar | Top toolbar | Top toolbar | 이지 모드 (Easy Mode) ↔ Normal Mode 토글 |

### 4.4 사회복지사 (Social Worker)

| ID | 화면 (Screen) | S | T | D+ | 설명 (Description) |
|------|------|------|------|------|------|
| S-001 | **케이스 (Case) 관리 대시보드 (Dashboard)** | Full layout | Full layout | Multi-column | 담당 케이스 (Case) 요약, 오늘 할일, 리마인더 |
| S-002 | **케이스 (Case) 상세 페이지 (Detail Page)** | Full layout | 1 column | 3-column | 케이스 (Case) 정보, 기록 (Record) 리스트, 협업자 리스트 |
| S-003 | **기록 생성/수정 (Create/Edit Record)** | Scroll form | Scroll form | Split pane | 좌=템플릿 (Template) 선택, 우=폼 (Form) |
| S-004 | **협업자 초대 (Invite Collaborator)** | Bottom sheet | Slide drawer | Center 모달 (Modal) | 이메일 입력 + 역할 (Role) / 접근 권한 (Permission) / 기간 |
| S-005 | **기록 목록 뷰 (Record List View)** | Card list | Card list | Full data table | 검색 (Search) + 정렬 + 페이지네이션 |
| S-006 | **팀 협업 뷰 (Team Collaboration View)** | Full layout | 2-column | 3-column | 기록자 리스트, 권한 (Permission) 현황, 초대 현황 |

### 4.5 특수교사 (Special Teacher)

| ID | 화면 (Screen) | S | T | D+ | 설명 (Description) |
|------|------|------|------|------|------|
| T-001 | **IEP 대시보드 (Dashboard)** | Full list | 2-column | Multi-column | IEP 목표, 진도율, 기록 (Record) |
| T-002 | **IEP 생성/수정 (Create / Edit)** | Scroll form | Half-screen | Split pane | 좌=IEP 템플릿 (Template), 우=폼 (Form) |
| T-003 | **IEP 보호자 공유 (Share)** | Bottom sheet | Slide drawer | Center 모달 (Modal) | 보호자 / 사회복지사 선택하여 공유 |
| T-004 | **학생 목록 (Student List)** | Card grid | Grid 2열 | Table view | 졸업 / 재학 상태 필터 |

### 4.6 활동지원사 (Support Worker)

| ID | 화면 (Screen) | S | T | D+ | 설명 (Description) |
|------|------|------|------|------|------|
| A-001 | **일일 기록 대시보드 (Daily Log Dashboard)** | Timeline view | Timeline view | Timeline + table | 오늘 날짜 기준 지원 일지 |
| A-002 | **일일 기록 (Record Daily)** | Scroll form | Half-screen | Split pane | 1면 3~5개 필드. 간소화 |
| A-003 | **주간 요약 (Weekly Summary)** | Full layout | Full layout | Full page | 주간 리포트 |
| A-004 | **선호 리스트 (Preference List)** | Full layout | Split view | Multi-column | 이용자 선호 사항 리스트 |

### 4.7 시스템 관리자 (System Admin)

| ID | 화면 (Screen) | S | T | D+ | 설명 (Description) |
|------|------|------|------|------|------|
| ADM-001 | **관리자 대시보드 (Admin Dashboard)** | Full layout | Full layout | Full | 기관, 사용자, 권한 (Permission) 통계 |
| ADM-002 | **법정 이관 (Legal Override)** | Full layout | Full layout | Full | 후견 등록 / 해제 |

---

## 5. 컴포넌트 라이브러리 (Component Library)

### 5.1 기반 컴포넌트 (Foundation)

| 토큰 (Token) | S | T | D+ | 설명 (Description) |
|------|------|------|------|------|
| **여백 (Spacing)** | 8px base | 8px base | 8px base | 4, 8, 12, 16, 20, 24, 32, 40, 48, 64 |
| **테두리 둥글기 (Border Radius)** | 8px | 8px | 10px | 카드 (Card), 버튼 (Button), 입력 (Input) |
| **그림자 (Shadow)** | 0 1px 3px | 0 2px 8px | 0 4px 16px | 카드 (Card), 모달 (Modal), 드롭다운 (Dropdown) |
| **Z-index 레이어** | Fixed scale | Fixed scale | Fixed scale | 모달 (Modal): 1000, 드罗어 (Drawer): 900, 툴팁 (Tooltip): 800 |

### 5.2 버튼 (Button) 컴포넌트 (Button Component)

| 유형 (Type) | S | T | D+ | 색상 (Color) |
|------|------|------|------|------|
| Primary 버튼 (Button) | 48 × Full | 44 × auto | 40 × auto | Terracotta (#D97B54) |
| Secondary 버튼 (Button) | 48 × Full | 44 × auto | 40 × auto | Outline (Primary) |
| Danger 버튼 (Button) | 48 × Full | 44 × auto | 40 × auto | Coral (#E8645A) |
| Ghost 버튼 (Button) | 48 × 48 | 40 × 40 | 36 × 36 | Gray text |
| FAB (Mobile) | 56 × 56 | 48 × 48 | — | Primary |

### 5.3 카드 (Card) 컴포넌트 (Card Component)

| 타입 (Type) | S | T | D+ | 설명 (Description) |
|------|------|------|------|------|
| 기록 (Record) 카드 (Card) | 100% 너비, 16px padding | 100% 너비, 20px padding | Full, 20px padding | 최근 기록 (Record) |
| 타임라인 (Timeline) 카드 (Card) | 100% full | 100% full | 100% full | 생애주기별 사건 이벤트 |

### 5.4 폼 (Form) 필드 컴포넌트 (Form Field Component)

| 필드 타입 (Field Type) | S | T | D+ | 검증 (Validation) |
|------|------|------|------|------|
| 텍스트 입력 (Text Input) | Full, 64px (이지 모드 (Easy Mode)) | Full, 48px | Full, 40px | 실시간 (Real-time) |
| 텍스트 영역 (Textarea) | Full, 120px | Full, 80px | Full, 60px | 문자 수 (Character count) |
| 셀렉트 (Select) | Full, 64px | Full, 48px | Full, 40px | 칩 (Chip) 스타일 |
| 날짜 선택기 (Date Picker) | Full, 64px | Full, 48px | Dropdown or Inline | — |
| 파일 업로드 (File Upload) | Full, 80px area | 50% 너비, 80px | 50% 너비, 80px | 드래그 & 드롭, 10MB |
| 체크박스 (Checkbox) | 64 × 64 (이지 모드 (Easy Mode)) | 40 × 40 | 20 × 20 | 접근성 (Accessibility) 보장 |
| 라디오 (Radio) | 64 × 64 (이지 모드 (Easy Mode)) | 40 × 40 | 20 × 20 | 접근성 (Accessibility) 보장 |

### 5.5 타이포그래피 스케일 (Typography Scale)

| 스타일 (Style) | S | T | D+ | 가중치 (Weight) |
|------|------|------|------|------|
| H1 | 28px | 32px | 48px | 700 |
| H2 | 22px | 22px | 32px | 700 |
| H3 | 18px | 20px | 24px | 700 |
| 본문 (Body) | 16px | 16px | 16px | 400 |
| 캡션 (Caption) | 13px | 13px | 13px | 400 |
| 버튼 (Button) | 15px | 15px | 14px | 500 |

---

## 6. 인터랙션 패턴 (Interaction Patterns)

### 6.1 손제스처 (Swipe Gesture) — 모바일 (Mobile) 전용

| 제스처 (Gesture) | 대상 (Target) | 액션 (Action) |
|------|------|------|
| Swipe Left | 기록 (Record) 카드 (Card) | 삭제 확인 (Delete Confirmation) |
| Swipe Right | 기록 (Record) 카드 (Card) | 빠른 수정 (Quick Edit) |
| Swipe Down | 바텀 바 (Bottom Bar) | 닫기 / 최소화 |
| Long Press | 카드 (Card) | 컨텍스트 메뉴 (Context Menu: Edit, Share, Delete) |
| Swipe Up | 바텀 시트 (Bottom Sheet) | 풀 화면 (Full Screen) 확장 |

### 6.2 당기기 새로고침 (Pull to Refresh)

| 화면 (Screen) | S | T | D+ |
|------|------|------|------|
| 대시보드 (Dashboard) | ✅ | ✅ | ✅ (mouse drag) |
| 기록 (Record) 리스트 | ✅ | ✅ | ✅ |
| 캘린더 (Calendar) 뷰 (View) | ✅ | ✅ | ✅ |

### 6.3 로딩 상태 (Loading States)

| 타입 (Type) | S | T | D+ |
|------|------|------|------|
| 스킨레톤 (Skeleton) | 카드 (Card) 레벨 | 페이지 레벨 | 섹션 (Section) 레벨 |
| 스피너 (Spinner) | Centered full-screen | Centered 48px | Centered 32px |
| 진행 바 (Progress Bar) | Linear (full) | Linear (page) | Linear (section) |

### 6.4 토스트 (Toast) / 알림 (Notification)

| 우선순위 (Priority) | 유형 (Type) | 표시 위치 (Display Location) | 지속 시간 (Duration) |
|------|------|------|------|
| 높음 (High) | 모달 다이얼로그 (Modal Dialog) | Full-screen overlay | 사용자 닫을 때까지 (User dismiss) |
| 중간 (Medium) | 모달 (Modal) | Center, 60% | 사용자 닫을 때까지 (User dismiss) |
| 낮음 (Low) | 토스트 (Toast) | 하단 (S) / 상단 우측 (D+) | 3초 (Seconds) |

---

## 7. 이지 모드 (Easy Mode / 당사자 모드)

### 7.1 활성화 조건 (Activation Condition)

| 조건 (Condition) | 결과 (Result) |
|------|------|
| 당사자 역할 (Role) P2 | 자동 활성화 (Auto-active) |
| 당사자 미성년 (P6) | 보호자 설정으로 켤 수 있음 |
| 이지 모드 (Easy Mode) 설정 | 수동으로 끌 수 있음 |

### 7.2 이지 모드 (Easy Mode) 디자인 규칙 (Design Rules)

| 요소 (Element) | 일반 (Normal) | 이지 모드 (Easy Mode) |
|------|------|------|
| **폰트 (Font) 크기 (Size)** | 16px base | 20px base |
| **터치 타겟 (Touch Target)** | 48px | 64px+ |
| **줄 간격 (Line Height)** | 1.5 | 1.8 |
| **색상 (Color)** | 표준 팔레트 (Standard Palette) | 고대비 (High Contrast, 7:1+), 흰 배경 (White background) |
| **아이콘 (Icon)** | 표준 아이콘 (Standard Icons) | 대형 아이콘 (Large Icons) + 텍스트 레이블 (Label) |
| **텍스트 (Text)** | 전체 설명 (Full description) | 간결 텍스트 (Simple text only) |
| **폼 (Form)** | 복잡한 폼 (Complex Form) | 1 질문 per 화면 (Question per screen) |
| **진행도 (Progress)** | Linear progress | 숫자만 (Number only) |
| **피드백 (Feedback)** | 표준 토스트 (Standard Toast) | 오디오 + 시각 (Audio + Visual) |

---

## 8. 접근성 및 다국어 (Accessibility & Localization)

### 8.1 WCAG 2.1 AA 체크리스트 (Checklist)

| 기준 (Criteria) | 상태 (Status) | 설명 (Notes) |
|------|------|------|
| **1.1.1** 대체 텍스트 | ✅ | 모든 SVG에 `alt`, `title`, `aria-label` |
| **1.4.3** 대비 (Contrast, Minimum) | ✅ | 4.5:1 이상 (테마: 7:1+) |
| **1.4.4** 텍스트 리사이즈 (Resize) | ✅ | 200% 확대 시 레이아웃 (Layout) 무너지지 않음 |
| **1.4.11** 비텍스트 대비 (Non-text) | ✅ | UI 컴포넌트 3:1 이상 |
| **2.1.1** 키보드 (Keyboard) | ✅ | 전체 기능 Tab키 접근 가능 |
| **2.4.6** 헤딩 (Heading) | ✅ | H1-H3 계층 structure |
| **2.4.7** 포커스 (Focus) | ✅ | 2px outline |
| **2.5.1** 제스처 (Pointer Gestures) | ✅ | 단일 제스처 (Single gesture)로 대체 |
| **2.5.3** 레이블 (Label in Name) | ✅ | button text contains icon title |
| **3.3.2** 레이블 (Labels) | ✅ | 필드 레이블 (Label) 항상 표시 |
| **4.1.2** 이름 (Name), 역할 (Role), 값 (Value) | ✅ | 모든 컴포넌트 `aria-*` |

### 8.2 다국어 (i18n, Phase 2)

- 언어 전환 (Language Toggle)은 헤더 (Header) 상단에 위치
- RTL 레이아웃 (Layout) 준비 (Phase 1에서는 미구현)
- 한국어 (Korean) 텍스트 전용 (Text-only) Phase 1

---

## 9. 브레이크포인트 × 기능 행렬 (Breakpoints × Feature Matrix)

| 기능 (Feature) | S | M | T | D+ |
|------|------|------|------|------|
| 대시보드 (Dashboard) | 카드 (Card) 뷰 (View) | 카드 (Card) | 그리드 (Grid) | Multi-column |
| Records 리스트 | 카드 (Card) 리스트 (List) | 카드 (Card) 리스트 (List) | 데이터 테이블 (Data Table) | 데이터 테이블 (Data Table) |
| Record 생성/수정 폼 (Form) | 스크롤 폼 (Scroll Form) | 하프 스크린 (Half-screen) | 풀 폼 (Full Form) | 스플릿 페인 (Split Pane) |
| 검색 (Search) & 필터 (Filter) | 바텀 시트 (Bottom Sheet) | 슬라이드 드로어 (Slide Drawer) | 필터 헤더 (Filter Header) | 분리형 사이드바 (Collapsible Sidebar) |
| PDF (PDF) 출력 | 바텀 시트 (Bottom Sheet) | Center 모달 (Modal) | Center 모달 (Modal) | Center 다이얼로그 (Dialog) |
| 기록자 협업 (Collaborator) | 바텀 시트 (Bottom Sheet) | 슬라이드 드로어 (Slide Drawer) | 모달 (Modal) | 모달 (Modal) |
| 타임라인 (Timeline) | 수직 스크롤 (Vertical Scroll) | 수직 스크롤 (Vertical Scroll) | 수평 (Horizontal) | 수평 (Horizontal) |
| 알림 (Notification) | Full 리스트 (List) | Full 리스트 (List) | Center 모달 (Modal) | Center 모달 (Modal) |
| 설정 (Settings) | Full 리스트 (List) | Full 리스트 (List) | Center 모달 (Modal) | Center 다이얼로그 (Dialog) |
