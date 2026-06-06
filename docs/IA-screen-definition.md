# LifeLog — IA 및 화면정의서 (Information Architecture & Screen Definition)

> **버전**: v1.0 | **작성일**: 2026-06-06 | **기준 문서**: PRD v1.0 · UX Design Spec v1.0 · Workflow v1.0 · UI Layer Architecture v1.0 · BrandBI v1.0
>
> **대상**: 기획팀 · UX/UI 디자이너 · 프론트엔드 개발팀
>
> **플랫폼**: 발달장애인 생애전주기 기록 플랫폼 LifeLog — Phase 1 MVP
>
> **디자인 시스템**: BrandBI (라이프네스트 · 소유드 · 어울 통합) · WCAG 2.1 AA 준수

---

## 목차

1. [서비스 구조 개요](#1-서비스-구조-개요)
2. [전체 메뉴 구조 IA (Information Architecture)](#2-전체 메뉴-구조-ia-information-architecture)
3. [역할별 내비게이션 매핑](#3-역할별-내비게이션-매핑)
4. [화면 정의 (Screen Definition)](#4-화면-정의-screen-definition)
5. [모든 화면 상세 정의](#5-모든-화면-상세-정의)
6. [글로벌 레이아웃 시스템](#6-글로벌-레이아웃-시스템)
7. [모바일 ↔ 데스크탑 반응형 매핑](#7-모바일--데스크탑-반응형-매핑)
8. [이지 모드 (Easy Mode) 정의](#8-이지- 모드-easy-mode-정의)
9. [화면 간 이동 경로 (Screen Flow)](#9-화면-간-이동-경로-screen-flow)
10. [접근성 요구사항](#10-접근성-요구사항)

---

## 1. 서비스 구조 개요

### 1.1 서비스 레이어 (Service Layers)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LifeLog Platform (Responsive Web)                  │
├─────────────────────────────────────────────────────────────────────┤
│  Layer (UI)  │ Pages / Components / Views / Screens                  │
├─────────────────────────────────────────────────────────────────────┤
│ ViewModel    │ ScreenVM / FormState / Validation / FieldMapping      │
├─────────────────────────────────────────────────────────────────────┤
│ Feature      │ UseCase / Interactor / DTO Mapper                     │
├─────────────────────────────────────────────────────────────────────┤
│ Domain       │ Entity / ValueObject / RepositoryContract / Service   │
├─────────────────────────────────────────────────────────────────────┤
│ Infra        │ API.Adapter / PDF.Adapter / Storage.Adapter           │
├─────────────────────────────────────────────────────────────────────┤
│ Data         │ HTTP Client / Cache.Store / LocalDB / WebSocket       │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 서비스 모듈 (Service Modules)

| 모듈 ID | 모듈명 | 역할 | 주요 기능 |
|---------|--------|------|---------|
| **SRV-AUTH** | 인증/계정 | 회원가입, 로그인, 인증 | 이메일/비밀번호, Passport OTP, Social Login, RBAC |
| **SRV-DASHBOARD** | 대시보드 | 역할별 홈 화면 | 요약 카드, 오늘 할일, 빠른 액션 |
| **SRV-FAMILY** | 가족 관리 | 당사자 프로파일 관리 | 프로파일 CRUD, 생애주기 전환, 타임라인 |
| **SRV-RECORD** | 기록 | 기록 CRUD | 생성, 열람, 수정, 삭제, 검색 |
| **SRV-TEMPLATE** | 템플릿 | 템플릿 기반 폼 | 템플릿 선택, 동적 폼 렌더링 |
| **SRV-WORK** | 협업 | 초대, 협업, 케이스 관리 | 기록자 초대, 권한 관리, 케이스 관리 |
| **SRV-SHARE** | 공유/인출 | PDF 출력, 기록 공유 | PDF 생성, 다운로드, 공유 링크 |
| **SRV-NOTIFY** | 알림 | 알림 센터 | 앱 내 알림, 이메일 알림, 푸시 알림 |
| **SRV-PROFILE** | 프로필 | 당사자/전문가 프로필 | 자기기록,เป้าหมาย, Easy Mode, 선호리스트 |
| **SRV-ACCOUNT** | 계정설정 | 계정 관리 | 프로필 수정, 비밀번호, 알림설정, 탈퇴 |
| **SRV-ADMIN** | 관리자 | 시스템 관리 | 기관/사용자/권한 관리 |

### 1.3 사용자 역할 (User Roles)

| 역할 | RoleType | 설명 | 주요 사용 기기 |
|------|----------|------|--------------|
| **보호자** | GUARDIAN | 당사자의 법정 보호자 (부모) | 모바일 + 데스크탑 |
| **당사자** | PERSON | 발달장애인 본인 (만 18세 이상) | 모바일 (Easy Mode) |
| **사회복지사** | SOCIAL_WORKER | 사례 관리자 | 데스크탑 + 모바일 |
| **특수교사** | SPECIAL_TEACHER | 특수교육 기관 교사 | 데스크탑 |
| **활동지원사** | SUPPORT_WORKER | 일상 생활 지원 종사자 | 모바일 |
| **시스템 관리자** | ADMIN | 플랫폼 관리자 | 데스크탑 |

---

## 2. 전체 메뉴 구조 IA (Information Architecture)

```
LifeLog Platform
│
├── [공통] 인증 (SRV-AUTH)
│   ├── 스플래시 / 온보딩              (C-001)
│   ├── 로그인 / 이메일 OTP             (C-002)
│   ├── 역할 온보딩                     (C-003)
│   ├── 비밀번호 찾기                    (C-013)
│
├── [공통] 대시보드 (SRV-DASHBOARD)
│   ├── 공통 대시보드                   (C-004)
│   │
│   ├── ── 보호자 전용 ──
│   ├── 보호자 대시보드                 (G-001)
│   │
│   ├── ── 당사자 전용 ──
│   ├── 당사자 대시보드                 (P-001)
│   │
│   ├── ── 사회복지사 전용 ──
│   ├── 케이스 관리 대시보드            (S-001)
│   │
│   ├── ── 특수교사 전용 ──
│   ├── IEP 대시보드                    (T-001)
│   │
│   ├── ── 활동지원사 전용 ──
│   ├── 일일 기록 대시보드              (A-001)
│   │
│   └── ── 관리자 전용 ──
│   └── 관리자 대시보드                 (ADM-001)
│
├── [공통] 기록 (SRV-RECORD)
│   ├── 기록 상세                       (C-005)
│   ├── 기록 생성/수정                  (C-006)
│   ├── 검색/필터                       (C-007)
│   │
│   ├── ── 보호자 전용 ──
│   ├── 타임라인 뷰                     (G-003)
│   ├── 카테고리 필터                   (G-004)
│   │
│   ├── ── 당사자 전용 ──
│   ├── 당사자 기록 열람                (P-002)
│   ├── 당사자 자기 기록 작성           (P-003)
│   │
│   ├── ── 사회복지사 전용 ──
│   ├── 케이스 상세 페이지              (S-002)
│   ├── 기록 생성/수정                  (S-003)
│   ├── 기록 목록 뷰                    (S-005)
│   │
│   ├── ── 특수교사 전용 ──
│   ├── IEP 생성/수정                   (T-002)
│   ├── 학생 목록                       (T-004)
│   │
│   ├── ── 활동지원사 전용 ──
│   ├── 일일 기록                       (A-002)
│   │
│   └── ── 관리자 전용 ──
│   └── 법정 이관                       (ADM-002)
│
├── [공통] 가족 (SRV-FAMILY)
│   ├── 가족 구성원 목록                (G-002)
│   │
│   ├── ── 당사자 전용 ──
│   ├── 당사자 프로필 & 목표            (P-004)
│   ├── 이지 모드 토글                  (P-006)
│   │
│   └── ── 활동지원사 전용 ──
│   └── 선호 리스트                     (A-004)
│
├── [공통] 협업 (SRV-WORK)
│   ├── 협업자 초대                     (S-004)
│   ├── 팀 협업 뷰                      (S-006)
│   ├── IEP 보호자 공유                 (T-003)
│   └── 주간 요약                       (A-003)
│
├── [공통] 공유/인출 (SRV-SHARE)
│   └── PDF 출력                       (C-008)
│   └── 공유/내보내기                   (G-005)
│
├── [공통] 알림 (SRV-NOTIFY)
│   ├── 알림 센터                       (C-009)
│   │
│   └── ── 당사자 전용 ──
│   └── 당사자 알림                     (P-005)
│
└── [공통] 계정설정 (SRV-ACCOUNT)
    ├── 역할 등록                       (C-011)
    ├── 이메일 인증                     (C-012)
    └── 계정 설정                       (C-014)
```

---

## 3. 역할별 내비게이션 매핑

### 3.1 데스크탑 (D+ ≥ 768px) — 사이드바 내비게이션

```
┌────────────────────────────────────────────────────────────┐
│                    LifeLog                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Logo  │  ┌─────────────┐                               │ │
│  │       │  │ 🏠 대시보드  │ ← C-004 (역할별 커스텀)      │ │
│  │       │  │ 📋 기록       │ ← C-005 ~ C-007 (역할별)    │ │
│  │       │  │ 👨‍👩‍👧 가족      │ ← G-001 ~ G-004 (보호자)   │ │
│  │       │  │ 🤝 협업       │ ← S-004 ~ S-006 (전문인력)  │ │
│  │       │  │ 📤 공유/인출  │ ← C-008 / G-005            │ │
│  │       │  │ 🔔 알림       │ ← C-009 / P-005            │ │
│  │       │  │ 👤 프로필     │ ← P-004 / C-014            │ │
│  │       │  │ ⚙️ 설정       │ ← C-014                    │ │
│  │       │  └─────────────┘                               │ │
│  │    280px 고정                                    [User]│ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

### 3.2 모바일 (S/T ≤ 768px) — 바텀바 내비게이션

```
┌──────────────────────────────────────┐
│           상단 헤더 (TopBar)          │
│  Logo            🔔  👤              │
├──────────────────────────────────────┤
│                                      │
│           메인 콘텐츠                 │
│                                      │
│                                      │
├──────────────────────────────────────┤
│  🏠    📋    🔔    👤    ⚙️          │
│ 대시보 기록  알림 프로필  설정         │
│ 드기                                     │
└──────────────────────────────────────┘
```

### 3.3 역할별 내비게이션 항목 매핑

| 화면 ID | 화면명 | 보호자 | 당사자 |社工 | 특수교사 | 지원사 | 관리자 |
|---------|--------|:------:|:------:|:----:|:-------:|:-----:|:-----:|
| C-004 | 대시보드 | O | O | O | O | O | O |
| C-005 | 기록 상세 | O | O | O | O | O | O |
| C-006 | 기록 생성/수정 | O | O | O | O | O | O |
| C-007 | 검색/필터 | O | O | O | O | O | O |
| C-008 | PDF 출력 | O | O | O | O | O | O |
| G-001 | 보호자 대시보드 | O | — | — | — | — | — |
| G-002 | 가족 구성원 목록 | O | — | — | — | — | — |
| G-003 | 타임라인 뷰 | O | — | — | — | — | — |
| G-004 | 카테고리 필터 | O | — | — | — | — | — |
| G-005 | 공유/내보내기 | O | — | — | — | — | — |
| P-001 | 당사자 대시보드 | — | O | — | — | — | — |
| P-002 | 당사자 기록 열람 | — | O | — | — | — | — |
| P-003 | 당사자 자기 기록 | — | O | — | — | — | — |
| P-004 | 당사자 프로필 & 목표 | — | O | — | — | — | — |
| P-005 | 당사자 알림 | — | O | — | — | — | — |
| P-006 | 이지 모드 토글 | — | O | — | — | — | — |
| S-001 | 케이스 관리 대시보드 | — | — | O | — | — | — |
| S-002 | 케이스 상세 페이지 | — | — | O | — | — | — |
| S-003 | 기록 생성/수정 (社工) | — | — | O | — | — | — |
| S-004 | 협업자 초대 | — | — | O | — | — | — |
| S-005 | 기록 목록 뷰 | — | — | O | — | — | — |
| S-006 | 팀 협업 뷰 | — | — | O | — | — | — |
| T-001 | IEP 대시보드 | — | — | — | O | — | — |
| T-002 | IEP 생성/수정 | — | — | — | O | — | — |
| T-003 | IEP 보호자 공유 | — | — | — | O | — | — |
| T-004 | 학생 목록 | — | — | — | O | — | — |
| A-001 | 일일 기록 대시보드 | — | — | — | — | O | — |
| A-002 | 일일 기록 | — | — | — | — | O | — |
| A-003 | 주간 요약 | — | — | — | — | O | — |
| A-004 | 선호 리스트 | — | — | — | — | O | — |
| ADM-001 | 관리자 대시보드 | — | — | — | — | — | O |
| ADM-002 | 법정 이관 | — | — | — | — | — | O |
| C-009 | 알림 센터 | O | O | O | O | O | O |
| C-014 | 계정 설정 | O | O | O | O | O | O |

---

## 4. 화면 정의 (Screen Definition)

### 4.1 화면 ID 체계

| 접두사 | 의미 | 대상 역할 |
|--------|------|---------|
| **C-** | Common (공통) | 여러 역할 공유 |
| **G-** | Guardian (보호자) | 보호자 전용 |
| **P-** | Person (당사자) | 당사자 전용 |
| **S-** | Social Worker (社工) | 사회복지사 전용 |
| **T-** | Teacher (특수교사) | 특수교사 전용 |
| **A-** | Assistant (지원사) | 활동지원사 전용 |
| **ADM-** | Admin (관리자) | 관리전용 |

### 4.2 화면 레이아웃 타입

| 레이아웃 타입 | 설명 | 적용 브레이크포인트 |
|-------------|------|-----------------|
| **Full page** | 전체 페이지 단일 레이아웃 | S, T |
| **Full layout** | 전체 화면 활용 레이아웃 | S, T, D+ |
| **Split pane** | 좌우 분할 (템플릿 / 폼) | D+ |
| **Multi-column** | 다컬럼 그리드 | D+ |
| **Centered** | 중앙 집중형 | S, T, D+ |
| **Centered-card** | 카드중앙 집중 | S, T, D+ |
| **Timeline view** | 타임라인형 | S, D+ |
| **Card list** | 카드 목록 | S, T |
| **Card grid** | 카드 그리드 | T |
| **3-column** | 3컬럼 | D+ |
| **2-column** | 2컬럼 | T, D+ |
| **Half-screen** | 반화면 | T |
| **Scroll form** | 스크롤 폼 | S, T |
| **Bottom sheet** | 바텀 시트 | S |
| **Slide drawer** | 사이드 드로어 | T |
| **Modal** | 중앙 모달 | D+ |

---

## 5. 모든 화면 상세 정의

---

### [COMMON] C-001 — 스플래시 / 온보딩

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-AUTH |
| **역할** | All (미로그인) |
| **레이아웃** | Centered (D+ 40% width) / Full page (S) |
| **브레이크 포인트** | S = Full, D+ = Centered Card |
| **이동 경로** | C-001 → C-002 / C-003 → C-004 |
| **접근 제어** | 비로그인 전용 |
| **화면 구성** | `Layout → Shell → BrandLogo → Title → WelcomeText → StartButton` |
| **핵심 인터랙션** | 스플래시 2초 자동 → 온보딩화면 → 로그인/가입 이동 |
| **디자인 포인트** | BrandBI 컬러 그라데이션 배경, 로고, "당신의 생애를 기록하는 플랫폼" |

---

### [COMMON] C-002 — 로그인 / 이메일 OTP

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-AUTH |
| **역할** | All (미로그인) |
| **레이아웃** | Centered Card (D+) / Full Screen (S) |
| **브레이크 포인트** | S = 100% width, D+ = 40% max |
| **이동 경로** | C-002 → C-003 → C-004 |
| **접근 제어** | 비로그인 전용 |
| **화면 구성** | `Form → EmailInput → PasswordInput → LoginButton → Divider → SocialButtons → ForgotPasswordLink` |
| **핵심 인터랙션** | 이메일+비밀번호 → JWT Access(1h)+Refresh(7d) → 역할 온보딩 또는 대시보드 |
| **비고** | P1: PASS 간편인증, 카카오 소셜 로그인 |

---

### [COMMON] C-003 — 역할 온보딩

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-AUTH |
| **역할** | All (신규 계정) |
| **레이아웃** | Centered Card |
| **이동 경로** | C-003 → C-004 |
| **접근 제어** | 신규 계정 전용 (1회성) |
| **화면 구성** | `RoleSelector → RoleCards(Guardian/Person/Professional) → Form(역할별 다름) → Submit` |
| **핵심 인터랙션** | 역할 선택 → 역할별 필드 입력 → RoleAssignment 테이블 DB INSERT |

---

### [COMMON] C-004 — 공통 대시보드 (Role-specific)

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-DASHBOARD |
| **역할** | All (역할별 커스텀) |
| **레이아웃** | Global Layout (Sidebar D+ / BottomBar S) |
| **브레이크 포인트** | S/T = BottomBar + Full page, D+ = Sidebar + 1140px |
| **이동 경로** | C-004 → 각 역할별 서브 화면으로 분기 |
| **접근 제어** | 로그인 필요 |
| **화면 구성** | `TopBar → RoleSwitcher → SummaryCards → RoleSpecificMainContent` |
| **핵심 인터랙션** | 역할에 따라 4~5개 SummaryCard 표시 (기록수, 승인대기, 마감임박, 총케이스) |
| **Role별 Main Content** | 보호자: FamilyCard + RecentRecord + QuickPDF / 당사자: RecentRecord + NextAppointment /社工: CaseSummary + TodayTasks / 특수교사: IEP Goal + ProgressRate / 지원사: Today's Schedule / 관리자: InstitutionStats |

---

### [COMMON] C-005 — 기록 상세

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD |
| **역할** | All (권한 있는 역할) |
| **레이아웃** | Global Layout |
| **이동 경로** | C-005 → C-006(수정가권 있을 시) |
| **접근 제어** | 기록 조회 권한 필요 |
| **화면 구성** | `Layout → Shell → Breadcrumb → RecordActions(Edit/Download/Share/History) → RecordMetaCard → RecordFormView(Readonly) → RecordHistoryTimeline` |
| **핵심 인터랙션** | 템플릿 필드별 값 표시, 첨부파일 목록, 역사 타임라인 |
| **Metadata 표시** | 카테고리, 생애주기, 작성일자, 작성자, 공개범위 |

---

### [COMMON] C-006 — 기록 생성/수정

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD + SRV-TEMPLATE |
| **역할** | All (작성 권한 있는 역할) |
| **레이아웃** | Split Pane (D+) / Scroll Form (S, T) |
| **이동 경로** | C-006 → C-005 → (PDF) C-008 |
| **접근 제어** | 템플릿 작성 권한 필요 |
| **화면 구성 (D+ Split)** | `Left: TemplateSelector(카테고리 → 생애주기 → 템플릿) | Right: Form(동적 필드)` |
| **핵심 인터랙션** | ① 카테고리 선택 → ② 생애주기+역할에 맞는 템플릿 필터 → ③ 동적 폼 렌더링(10종 필드) → ④ 자동 임시저장(5분) → ⑤ 저장/확정 |
| **동적 폼 필드 타입** | text, textarea, select, multiselect, date, date_range, scale, table, file, checkbox |
| **비고** | 모바일에서 카메라 직접 촬영 또는 앨범 선택으로 첨부 가능 |

---

### [COMMON] C-007 — 검색/필터

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD |
| **역할** | All |
| **레이아웃** | Global Layout |
| **이동 경로** | C-007 → (결과 선택) → C-005 |
| **접근 제어** | 로그인 필요 |
| **화면 구성** | `SearchBar(FilterPanel) → CategoryTabs(전체/건강/교육/일상/서비스/자기) → DateRangePicker → KeywordInput → SearchResults(Cards/Datatable)` |
| **핵심 인터랙션** | 키워드(JSONB GIN 인덱스) + 카테고리 + 날짜 범위 필터링 |
| **결과 표시** | 카테고리 아이콘, 날짜, 작성자, 첨부파일 수, 공개범위 표시 |

---

### [COMMON] C-008 — PDF 출력

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-SHARE |
| **역할** | All |
| **레이아웃** | Centered Modal |
| **이동 경로** | C-008 → (생성 대기) → C-008(완료) → (다운로드) |
| **접근 제어** | 기록 열람 권한 필요 |
| **화면 구성** | `Modal → Single/RecordSelection → RangePicker → GenerateButton → Progress(비동기) → DownloadLink(15분 유효)` |
| **핵심 인터랙션** | 백그라운드 작업큐로 PDF 생성 (<30초) → 완료 시 알림 → 15분 유효 다운로드 링크 제공 |
| **비고** | PDF 생성 이벤트는 `permission_logs`에 기록 |

---

### [COMMON] C-009 — 알림 센터

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-NOTIFY |
| **역할** | All |
| **레이아웃** | Global Layout |
| **이동 경로** | C-009 → (알림 선택) → 해당 화면으로 이동 |
| **접근 제어** | 로그인 필요 |
| **화면 구성** | `BellNotificationCenter → NotificationList(유형별 탭) → MarkAllRead → NotificationSettings` |
| **핵심 인터랙션** | 실시간 알림(WebSocket), 유형별 필터링(이양/초대/기록변경/일정), 읽음표시 |

---

### [COMMON] C-010 — 설정/프로필 *(C-014와 통합)*

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-ACCOUNT |
| **역할** | All |
| **레이아웃** | Global Layout |
| **화면 구성** | `UserProfileCard(프로필수정) → SettingsGroup(계정/알림/기타)` |
| **설정 그룹** | 계정: 이메일변경, 비밀번호변경, 역할변경요청 / 알림: 이메일, 푸시, SMS 토글 / 기타: 언어, 테마, 계정탈퇴 |

---

### [COMMON] C-011 — 역할 등록

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-AUTH |
| **역할** | All (역할 변경 요청) |
| **레이아웃** | Centered Card |
| **화면 구성** | `RoleSelector → RoleCards → RequestForm → Submit → AdminReview` |

---

### [COMMON] C-012 — 이메일 인증

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-ACCOUNT |
| **역할** | All |
| **레이아웃** | Centered Card |
| **화면 구성** | `EmailInput → VerificationCodeInput(6자리) → VerifyButton → ResendTimer(60초)` |

---

### [COMMON] C-013 — 비밀번호 찾기

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-AUTH |
| **역할** | All (비로그인) |
| **레이아웃** | Centered Card |
| **화면 구성** | `EmailInput → SendResetEmail → LinkExpire(1시간) → NewPasswordInput → ConfirmPassword → Submit` \|
| **핵심 인터랙션** | 이메일 발송 → 링크 클릭 → 새 비밀번호 설정 |

---

### [COMMON] C-014 — 계정 설정

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-ACCOUNT |
| **역할** | All |
| **레이아웃** | Global Layout |
| **화면 구성** | `Layout → UserProfileCard → SettingsGroup(계정/알림/기타)` |

---

### [GUARDIAN] G-001 — 보호자 대시보드

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-DASHBOARD + SRV-FAMILY |
| **역할** | Guardian |
| **레이아웃** | Multi-column (D+), Full page (S) |
| **이동 경로** | G-001 → G-002(가족목록) / G-003(타임라인) / C-005(기록) |
| **화면 구성** | `SummaryCard(TotalCases / ActiveParties / PendingPDF / UpcomingDeadlines) → FamilyCardList ← QuickAction(CreateRecord/QuickPDF/Invite) → RecentRecords → UpcomingReminders` |
| **핵심 인터랙션** | FamilyCard: 당사자별 요약(프로필사진, 생애주기, 기록수, 마지막활동). FamilyCard 클릭 시 상세 타임라인(G-003) 이동 |

---

### [GUARDIAN] G-002 — 가족 구성원 목록

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-FAMILY |
| **역할** | Guardian |
| **레이아웃** | Card List (S) / Data Table (D+) |
| **이동 경로** | G-002 → G-003(타임라인/기록) / P-004(프로필수정) |
| **화면 구성** | `PartyProfileList(Cards/Table) → AddPartyButton(신규당사자) → Click→PartyDetail(Timeline/Records) → EditButton` |
| **핵심 인터랙션** | 1 보호자 × 다수 당사자 관리. 당사자 추가: 프로필생성 → 생애주기 자동계산 |

---

### [GUARDIAN] G-003 — 타임라인 뷰

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD + SRV-FAMILY |
| **역할** | Guardian |
| **레이아웃** | Timeline View (D+) / Card List (S) |
| **이동 경로** | G-003 → C-005(기록상세) / C-008(PDF) |
| **화면 구성** | `TimelineView(生애주기구간별 세그먼트) → CategoryFilter(전체/5종) → DateRangeSearch → KeywordSearch → RecordCards(아이콘/날짜/작성자/첨부수/공개범위) → Click→RecordDetail` |
| **핵심 인터랙션** | 무한스크롤(Cursor 기반). 6개 생애주기 구간으로 시각적 구분. 카테고리별 색상 코딩 |

---

### [GUARDIAN] G-004 — 카테고리 필터

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-FAMILY |
| **역할** | Guardian |
| **레이아웃** | Bottom Sheet (S) / Slide Drawer (T) / Side Panel (D+) |
| **화면 구성** | `ToggleButton → FilterPanel(Toggle5개 카테고리) → ApplyButton → FilterCountBadge` |
| **핵심 인터랙션** | 5개 카테고리 토글: 건강·의료 / 교육·발달 / 일상생활 / 서비스연계 / 자기표현 |

---

### [GUARDIAN] G-005 — 공유/내보내기

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-SHARE |
| **역할** | Guardian |
| **레이아웃** | Modal (D+) / Bottom Sheet (S) |
| **화면 구성** | `RangeSelection → PDFPreview → DownloadButton → ShareLink(Create15minExpiredLink)` |

---

### [PERSON] P-001 — 당사자 대시보드 (Easy Mode)

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-DASHBOARD |
| **역할** | Person |
| **레이아웃** | Centered (D+) / Full page (S), Easy Mode 적용 |
| **이동 경로** | P-001 → P-002(기록) / P-003(자기기록) / P-004(프로필) / P-005(알림) |
| **화면 구성** | `EasyModeTopBar(BrandLogo / EasyToggle / LargeUserAvatar) → WelcomeText(H1 EasyFont) → RecentRecordCard → NextAppointmentCard → EasyModeBottomBar(홈/기록/목표/프로필)` |
| **핵심 인터랙션** | 2개의 카드만 표시. Easy Mode: Large Text/Font(18px+), Large Button(64px), Simple Icon |
| **Easy Mode** | 터치타겟 64px, 명도비 7:1, 라인height 1.8 |

---

### [PERSON] P-002 — 당사자 기록 열람

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD |
| **역할** | Person |
| **레이아웃** | Card List (S, T) / DataTable(D+) |
| **화면 구성** | `RecordCardList(Cards:카테고리아이콘/제목/일자/작성자) → AuthorFilter(기록자별필터) → Click→P-002Detail(RecordFormViewReadonly)` |
| **핵심 인터랙션** | 권한 범위 내 기록만 열람. Easy Mode: Large Text, Large Button |

---

### [PERSON] P-003 — 당사자 자기 기록 작성

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD |
| **역할** | Person |
| **레이아웃** | Centered Card (D+) / Full page (S) |
| **화면 구성** | `LargeRecordButton(최소56px) → MoodSelector(😊😐😢😡😴) → TextInput(텍스트) → PhotoUpload → QuickActions(밥먹기/친구만나기/운동하기) → SaveButton → Feedback("잘저장됐어요! 👍")` |
| **핵심 인터랙션** | 이모지 기분선택, 미리정의된 선택지 체크. Easy Mode Font 18px+ |

---

### [PERSON] P-004 — 당사자 프로필 & 목표

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-PROFILE |
| **역할** | Person |
| **레이아웃** | Full page |
| **화면 구성** | `UserProfileCard(Avatar/Name/BirthDate/Profile) → GoalList(현재목표/성과) → EditGoalButton → LifespanTimeline(생애주기시각화) → ServiceHistory` |
| **핵심 인터랙션** | 목표설정·추적. 생애타임라인 확인. 자기소개서 관리 |

---

### [PERSON] P-005 — 당사자 알림

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-NOTIFY |
| **역할** | Person |
| **레이아웃** | Full page / Centered (D+) |
| **화면 구성** | `NotificationList → NewRecordAdded / UpcomingSchedule / InvitationAccepted` |

---

### [PERSON] P-006 — 이지 모드 토글

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-PROFILE |
| **역할** | Person |
| **레이아웃** | Profile Settings |
| **화면 구성** | `EasyModeToggle → FontSizeSlider(16~24px) → TouchTargetSize(Standard/Large/Largest) → ThemeToggle(Light/Dark) → Preview(P-001)` |
| **핵심 인터랙션** | 당사자 모드 활성화/비활성화. 인앱 글자 사이즈 조절 |

---

### [SOCIAL WORKER] S-001 — 케이스 관리 대시보드

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-DASHBOARD |
| **역할** | Social Worker |
| **레이아웃** | Multi-column (D+) |
| **이동 경로** | S-001 → S-002(케이스상세) / S-003(기록작성) / S-004(초대) |
| **화면 구성** | `TopBar(Dashboard) → RoleSwitcher → SummaryCards(TotalCases/Active/Overdue/PendingApproval) → TaskList(TodayFolowUp/Approval/Reminder) → CaseTable(D+FullTable / S/T CardList) → FAB(CreateRecord)` |
| **핵심 인터랙션** | Cases: Case명, 생애주기, 기록수, 마지막활동. 요약카드: 총케이스수, 활성, 리마인더, 승인대기 |

---

### [SOCIAL WORKER] S-002 — 케이스 상세 페이지

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD |
| **역할** | Social Worker |
| **레이아웃** | 3-column (D+) / 1 column (S) / 2 column (T) |
| **이동 경로** | S-002 → C-005(기록상세) / S-003(기록작성) |
| **화면 구성** | `CaseInfo(프로필/생애주기/기록수/서비스연계) → RecordList → CollaboratorList → QuickActions(CreateRecord/Invite/ServiceLinkage)` |

---

### [SOCIAL WORKER] S-003 — 기록 생성/수정

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD + SRV-TEMPLATE |
| **역할** | Social Worker |
| **레이아웃** | Split Pane (D+) / Scroll (S, T) |
| **이동 경로** | S-002 → S-003 → C-005 |
| **화면 구성** | `C-006의 템플릿 선택 +社工특화 필드(서비스연계/케이스관리/목표설정)` |
| **핵심 인터블** | IEP 템플릿, 건강검진 템플릿, 서비스연계 템플릿 |

---

### [SOCIAL WORKER] S-004 — 협업자 초대

| 항목 | 세부 |
|------|------|
| **서비스** : SRV-WORK |
| **역할** | Social Worker |
| **레이아웃** | Bottom Sheet (S) / Slide Drawer (T) / Modal (D+) |
| **화면 구성** | `EmailInput → RoleSelector(社工/특수교사/지원사) → CategoryFilter(접근범위) → PeriodPicker(기간) → SendButton` |
| **핵심 인터랙션** | 이메일 → 역할·카테고리·기간指定 → 7일유효 토큰발급 → `invitations`테이블 INSERT |

---

### [SOCIAL WORKER] S-005 — 기록 목록 뷰

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD |
| **역할** | Social Worker |
| **레이아웃** | Full Data Table (D+) / Card List (S, T) |
| **화면 구성** | `SearchBar → Sort(Picker → Pagination → RecCard` |
| **핵심 인터랙션** | 검색+정렬+페이지네이션 |

---

### [SOCIAL WORKER] S-006 — 팀 협업 뷰

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-SHARE |
| **역할** | Social Worker |
| **레이아웃** | 3-column (D+) / (S) |
| **화면 구성** | `RecordersList → PermissionStatus → InvitationStatus → CollaboratorActions(수정/회수)` |

---

### [SPECIAL TEACHER] T-001 — IEP 대시보드

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-DASHBOARD |
| **역할** | Special Teacher |
| **레이아웃** | Multi-column (D+) |
| **이동 경로** | T-001 → T-002(IEP작성) / T-003(보호자공유) / T-004(학생목록) |
| **화면 구성** | `IEPGoals(장기/단기) → ProgressRate(수행도/개선사항) → RecordList → StudentOverview(Cards)` |
| **핵심 인터** | IEP 목표 달성율, 기록 건수, 보호자 공유 상태 |

---

### [SPECIAL TEACHER] T-002 — IEP 생성/수정

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD + SRV-TEMPLATE |
| **역할** | Special Teacher |
| **레이아웃** | Split Pane (D+) / Half-screen (T) / Scroll (S) |

| 화면 구성 | `Left: IEP Template 선택 → Right: IEP Form(장기목표/단기목표/평가기준/실행내용)` |
| 핵심 인터 | IEP 템플릿 선택 → 생애주기별 템플릿 → 목표설정 → 평가작성 → 보호자/社工과 공유 |

---

### [SPECIAL TEACHER] T-003 — IEP 보호자 공유

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-SHARE |
| **역할** | Special Teacher |
| **레이아웃** | Bottom Sheet (S) / Slide Drawer (T) / Modal (D+) |

| 화면 구성 | `Guardian/社工 Selector → ShareConfirm → ShareButton` |
| 핵심 인터 | 보호자 및社工에게 IEP 공유. 공유 이력 `permission_logs`에 기록 |

---

### [SPECIAL TEACHER] T-004 — 학생 목록

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-WORK |
| **역할** | Special Teacher |
| **레이아웃** | Card Grid (T) / Table (D+) |
| **화면 구성** | `StudentCards(Card:이름/생애주기/상태(재학/졸업)) → StatusFilter → Click→CaseDetail(S-002)` |

---

### [SUPPORT WORKER] A-001 — 일일 기록 대시보드

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-DASHBOARD |
| **역할** | Support Worker |
| **레이아웃** | Timeline View (S, T) / Timeline + Table (D+) |
| **이동 경로** | A-001 → A-002(일일기록) / A-003(주간요약) |
| **화면 구성** | `TodayDateHeader → TimelineView(오늘날짜기준지원일지) → QuickActions(SupportJournal/PhotoUpload/WeekReport)` |
| **핵심 인터** | 오늘의 지원일지, 사진 첨부(지원활동증거) |

---

### [SUPPORT WORKER] A-002 — 일일 기록

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD |
| **역할** | Support Worker |
| **레이아웃** | Scroll Form (S, T) / Split (D+) |

| 화면 구성 | `SupportTargetSelector → SupportContent(이동/식사/개인위생/취미) → SpecialNotes(사고/긴급상황) → PhotoUpload → SaveButton` |
| 핵심 인터 | 지원내용: 이동 / 식사 / 개인위생 / 취미 / 특이사항 / 사진첨부 |

---

### [SUPPORT WORKER] A-003 — 주간 요약

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-WORK |
| **역할** | Support Worker |
| **레이아웃** | Full page |

| 화면 구성 | `WeekSelector → WeeklySummary(TotalDays/SupportHours/SpecialEvents/RatingTrends) → ExportButton` |
| 핵심 인터 | 작성된 일지 자동 집계 → 주간 요약 확인 |

---

### [SUPPORT WORKER] A-004 — 선호 리스트

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-PROFILE |
| **역할** | Support Worker |
| **레이아웃** | Multi-column (D+) / Full (S, T) |
| **화면 구성** | `PreferenceList(선호사항/취미/활동) → AddButton → EditButton → DeleteButton` |

---

### [ADMIN] ADM-001 — 관리자 대시보드

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-DASHBOARD |
| **역할** | Admin |
| **레이아웃** | Full page |
| **화면 구성** | `SystemStats(InstitutionCount/UserCount/RecordCount) → PermissionOverview → ServiceStatus → QuickActions(ManageInstitutions/ManageUsers/BulkNotifications)` |

---

### [ADMIN] ADM-002 — 법정 이관

| 항목 | 세부 |
|------|------|
| **서비스** | SRV-RECORD |
| **역할** | Admin |
| **레이아웃** | Full page |

| 화면 구성 | `GuardianList → OverrideSelection → PostGuardianAssignment → ConfirmButton → LogToPermissonLogs` |
| 핵심 인터 | 후견등록/해제. 법정후견 범위 내에서만 후견인이 권한 |

---

## 6. 글로벌 레이아웃 시스템

### 6.1 헤더 (Header)

| 브레이크 포인트 | 레이아웃 |
|----------------|---------|
| **S** (≤480px) | Scroll 시 고정 TopBar (App Bar). Back button + Page Title |
| **T** (≤1024px) | 고정 Top Bar. Back + Page Title + Right Actions |
| **D+** (≥768px) | 고정 Top Bar + Left fixed Sidebar (280px) |
| **D+** (≥1280px) | 고정 Top Bar + Left fixed Sidebar (280px) + 1140px max content |

### 6.2 내비게이션 (Navigation)

| 브레이크 포인트 | 형태 | 내용 |
|----------------|------|------|
| **S / M** (≤768px) | **BottomBar** (5개 icon bar, 고정 하단) | 대시보드 / 기록 / 알림 / 프로필 / 설정 |
| **T** (≤1024px) | **BottomBar OR Sidebar** (선택) | 모바일/데스크탑 전환 |
| **D+** (≥768px) | **Sidebar** (fixed 280px, 좌측 고정) | 전체 메뉴, 계층적 구조 |

### 6.3 크럼 (Bread Crumb)

| 브레이크 포인트 | 표시 |
|----------------|------|
| **S / T** | 숨김 (탭바로 대체) |
| **D+** | 상단에 표시: `기록 > 카테고리 > 상세` |

### 6.4 푸터 (Footer)

| 브레이크 포인트 | 위치 |
|----------------|------|
| **S / T** | 고정 하단 |
| **D+** | 사이드바 하단에 통합 |

### 6.5 모달 (Modal)

| 브레이크 포인트 | 형태 |
|----------------|------|
| **S** | Full-screen overlay |
| **T** | Center 60% |
| **D+** | Center 40-60% width |

### 6.6 토스트 (Toast)

| 브레이크 포인트 | 위치 |
|----------------|------|
| **S / T** | Full-width 하단 고정 |
| **D+** | 상단 우측 |

---

## 7. 모바일 ↔ 데스크탑 반응형 매핑

### 7.1 Breakpoint 전략

| Breakpoint | 용도 | 대상 기기 |
|------------|------|---------|
| **S** (≤480px) | Small Mobile | 스마트폰 (세로) |
| **M** (≤768px) | Large Mobile / Small Tablet | 스마트폰 (가로), 작은 태블릿 |
| **T** (≤1024px) | Tablet | iPad, Surface |
| **D** (≤1280px) | Desktop | 일반 PC |
| **L** (>1280px) | Large Desktop | 대형 모니터 |

### 7.2 컴포넌트 브레이크포인트 매핑

| 컴포넌트 | S (≤480px) | M (≤768px) | T (≤1024px) | D (≤1280px) | L (>1280px) |
|---------|-----------|-----------|------------|-------------|-------------|
| Touch Target | 48px | 44px | 44px | 40px | 40px |
| Content Width | 100% | 100% | 100% | 1140px max | 1140px max |
| Navigation | BottomBar | BottomBar | BottomBar/Sidebar | Sidebar(280px fixed) | Sidebar(280px fixed) |
| Modal | Full-screen | Full-screen | Center 60% | Center 40-60% | Center 40-60% |
| Form | Scroll form | Scroll form | Scroll form | Split Pane | Split Pane |
| Breadcrumb | Hidden | Hidden | Hidden | Visible | Visible |
| Footer | Fixed bottom | Fixed bottom | Fixed bottom | Sidebar bottom | Sidebar bottom |
| Border Radius | 8px | 8px | 8px | 10px | 10px |

### 7.3 Breakpoint × 레이아웃 타입 행렬

| Breakpoint | Layout Type | Touch Target | Navigation | Modal Type | Form Type |
|------------|------------|--------------|------------|------------|-----------|
| **S** (≤480px) | Full page | 48px | BottomBar | Full-screen | Scroll |
| **M** (≤768px) | Full page | 44px | BottomBar | Full-screen | Scroll |
| **T** (≤1024px) | Full page | 44px | BottomBar/Sidebar | Center | Scroll |
| **D** (≤1280px) | 1140px max | 40px | Sidebar | Center | Split pane |
| **L** (>1280px) | 1140px max | 40px | Sidebar | Center | Split pane |

---

## 8. 이즈 모드 (Easy Mode) 정의

### 8.1 Easy Mode 활성화 조건

| 조건 | 설명 |
|------|------|
| **기본** | 사용자 설정에서 수동 활성화 (Q-011 미결정 시, 당사자 가입 시 자동 활성화 권장) |
| **적용 위치** | 당사자(P-) 모든 화면 |
| **전역 상태** | `users.easy_mode_enabled` Boolean |

### 8.2 Easy Mode 오버라이트 스펙

| 파라미터 | Standard | Easy Mode |
|---------|----------|----------|
| Base Font Size | 16px | **20px** |
| Button Height | 48px | **64px** |
| Line Height | 1.5 | **1.8** |
| Contrast Ratio | 4.5:1 | **7:1+** |
| Touch Target | Min 48px | **Min 64px** |
| Form Layout | Multi-field per screen | **Single-field-per-screen (P-003 특화)** |
| Icon | Standard size | **Large + Label** |
| Feedback | Standard toasts | **Enhanced (larger toasts, visual cues)** |

### 8.3 Easy Mode CSS Custom Properties

```css
--base-font-size: 20px
--touch-target-min: 64px
--line-height: 1.8
--contrast-ratio-min: 7:1
```

### 8.4 Easy Mode 화면 예시 (P-001 당사자 대시보드)

```
EasyModeTopBar
├── BrandLogo (small)
├── EasyModeToggle (on/off)
└── UserProfileAvatar (64px touch target)

Section: Welcome
├── "안녕, {{name}}씨!" (H1 EasyFont, 24px+)

Section: Recents
└── RecentRecordCard (single, large)

Section: Next Event
└── AppointmentCard (single, large)

EasyModeBottomBar
├── 홈 (home) ← selected
├── 기록 (records)
├── 목표 (goals)
└── 내 프로필 (profile)
```

---

## 9. 화면 간 이동 경로 (Screen Flow)

### 9.1 핵심 사용자 스토리별 화면 흐름

#### F-001: 보호자 — 당사자 추가 → 기록 작성 → PDF 출력

```
C-002 (로그인) → C-003 (역할온보딩) → G-001 (보호자대시보드)
  ├── G-002 (가족목록) → 당사자신규등록
  └── G-003 (타임라인) → G-003
        └── G-003 (카테고리필터)
              └── G-003 (키워드검색)
                    └── C-005 (기록상세)
                          ├── C-006 (기록수정)
                          └── C-008 (PDF출력) → 다운로드
```

#### F-002: 특수교사 — IEP 수립 → 보호자 공유

```
C-002 (로그인) → C-003 (역할온보딩) → T-001 (IEP 대시보드)
  └── T-002 (IEP 생성/수정) → IEP 저장 → T-001
        └── T-003 (IEP 보호자 공유) → 공유완료 → T-001
```

#### F-003: 사회복지사 — 케이스관리 → 협업초대

```
C-002 (로그인) → S-001 (케이스관리대시보드)
  ├── S-002 (케이스상세) → S-003 (기록작성) → S-002
  └── S-004 (협업자초대) → S-006 (팀협업뷰)
```

#### F-004: 당사자 — Easy Mode 기록작성

```
C-002 (로그인) → P-001 (당사자대시보드 EasyMode)
  ├── P-003 (자기기록작성) → C-005 (기록상세)
  ├── P-002 (기록열람) → C-005
  ├── P-004 (프로필&목표)
  └── P-005 (알림)
```

---

### 9.2 권한 이양 화면 흐름

```
시스템 ( 매일 09:00 Cron )
  │
  ├── D-90: 알림 → 보호자 + 당사자 (email + app)
  │         └── G-001 (보호자대시보드에 이양안내 배지 표시)
  │
  ├── D-30: 재알림 → 보호자 + 당사자
  │
  ├── D-7: 최종알림 → 보호자 + 당사자
  │
  ├── 당사자 이양시작버튼클릭 → TRANSITION_IN_PROGRESS
  │
  ├── 전자서명 → TRANSITION_VERIFIED
  │
  ├── PASS 본인인증 → TRANSITION_AUTHENTICATED
  │
  ├── 권한적용: 보호자(쓰기→열람전원) / 당사자(모든권한부여) → TRANSITION_COMPLETE
  │
  └── ADM-002 (법정이관) — 예외: 법정후견인 등록
```

---

### 9.3 기관 간 기록 이전 흐름 (Phase 2, 현재는 PDF로 대체)

```
[현재] 종이 PDF
기관 A → PDF인쇄 → 종이전달 → 기관 B 수동재입력 → 중복/누락 발생

[향후] API 기반
기관 A → LifeLog 접근권한요청 → 기관 B 승인 → 기록자동동기화 → 새기록추가
```

---

## 10. 접근성 요구사항

### 10.1 WCAG 2.1 AA 준수사항

| 항목 | 요구 수준 |
|------|---------|
| 명도 대비 (文本) | 4.5:1 이상 (당사자 모드: 7:1) |
| 터치 타겟 | 최소 44×44px (당사자 모드: 64×64px) |
| 키보드 내비게이션 | 전 기능 Tab 키 접근 가능 |
| 스크린리더 | VoiceOver (iOS) + TalkBack (Android) + NVDA+Chrome |
| 폰트 크기 | 브라우저 확대 200% 시 레이아웃 정상 |

### 10.2 접근성 설계 원칙

| 원칙 | 구현 |
|------|------|
| 모든 이미 ALT 텍스트 | 아이콘 버튼 → `aria-label` 필수 |
| color ≠ 유일한 정보 전달 | 상태 표시 → 아이콘+텍스트+color 동시사용 |
| 폼 검증 필드 | `aria-invalid`, `aria-describedby` 사용 |
| 모달 포커스 | 모달 열릴 때 첫 포커스 가능한 요소로 자동 이동 |
| 스크롤 가능 영역 | 스크롤 시 `overflow: auto` + 키보드 이동 가능 |
| 자동 재생 미디어 | 모든 자동 재생 중지 버튼 제공 |

---

> **본 문서는 PRD v1.0, UX Design Spec v1.0, Workflow v1.0, UI Layer Architecture v1.0, BrandBI v1.0을 기준으로 작성되었습니다.**
>
> **관리자**: 기획팀 · **검토 주기**: 매 Sprint 종료 시
