# LifeLog UI Layer Architecture — Screen-Level Definition

> **Version:** v1.0 · **Date:** 2026-06-05 · **Based on:** UX Design Specification v1.0, PRD v1.0, BrandBI v1.0

---

## 목차

1. [아키텍처 개요 — 6 계층 구조](#1-아키텍처-개요--6-계층-구조)
2. [서비스별 화면 레이어 매핑](#2-서비스별-화면-레이어-매핑)
3. [화면별 컴포넌트 트리구조 (Component Tree)](#3-화면별-컴포넌트-트리구조-component-tree)
4. [상태 관리 아키텍처](#4-상태-관리-아키텍처)
5. [데이터 흐름 (Data Flow)](#5-데이터-흐름-data-flow)
6. [레이어별 의존성 방향](#6-레이어별-의존성-방향)
7. [모바일 ↔ 데스크탑 반응형 계층 매핑](#7-모바일--데스크탑-반응형-계층-매핑)

---

## 1. 아키텍처 개요 — 6 계층 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│ L6  Presentation Layer (UI Rendering)                               │
│  Pages → Layout → ScreenShell → View → Component                    │
├─────────────────────────────────────────────────────────────────────┤
│ L5  View Module / ViewModel (UI-Specific Logic)                     │
│  ScreenVM → FormState → Validation → FieldMapping                   │
├─────────────────────────────────────────────────────────────────────┤
│ L4  Feature / UseCase (User Goal Operations)                        │
│  UseCase → Interactor → DTO Mapper                                  │
├─────────────────────────────────────────────────────────────────────┤
│ L3  Domain Layer (Business Logic)                                   │
│  Entity → ValueObject → RepositoryContract → DomainService          │
├─────────────────────────────────────────────────────────────────────┤
│ L2  Infrastructure Layer (External Adaptation)                      │
│  API.Adapter → PDF.Adapter → Storage.Adapter → Notification.Adapter │
├─────────────────────────────────────────────────────────────────────┤
│ L1  Data Layer (Persistence & Transport)                            │
│  HTTP Client → Cache.Store → LocalDB → WebSocket                    │
└─────────────────────────────────────────────────────────────────────┘
```

### 계층별 책임 (Layer Responsibilities)

| 계층 | 명칭 | 책임 | 출력물 |
|------|------|------|--------|
| **L6** | Presentation | 화면 렌더링, 레이아웃 전이, 제스처 처리, 반응형 분기 | `<Page>`, `<Layout>`, `<View>`, `<Component>` |
| **L5** | View Module | 화면별 상태, 폼 검증, 필드 매핑, UI 비즈니스 규칙 | `useScreenVM()`, `FormSchema`, `ValidationRules` |
| **L4** | Feature | 유저 목표 기반 UseCase (레코드 생성, 공유, 검색) | `UseCase.execute()` |
| **L3** | Domain | 도메인 엔티티, 값 객체, Repository 계약, 도메인 서비스 | `Record`, `Template`, `Permission` |
| **L2** | Infrastructure | 외부 API Adapter, PDF 생성, 파일 저장소, 푸시 알림 | `ApiClient`, `PdfGenerator`, `FileStorage` |
| **L1** | Data | HTTP 요청, 캐시, 로컬 DB, WebSocket 연결 | `HttpClient`, `CacheManager`, `LocalDb` |

### 의존성 방향 (Dependency Direction)

```
L6 → L5 → L4 → L3 ← L2 ← L1

화살표 방향: L6는 L5에 의존
역화살표: L3은 L2, L1의 인터페이스(계약)를 정의 → L2/L1가 구현

⚠️  하위 계층(L3~L1)은 상위 계층(L4~L6)을 참조할 수 없음 (Clean Architecture 준수)
```

---

## 2. 서비스별 화면 레이어 매핑

### 2.1 서비스 분류

LifeLog의 46개 화면을 8개 서비스 영역으로 분류한다.

| Service ID | 서비스명 | 화면 수 | 포함 화면 |
|------------|---------|---------|-----------|
| **SRV-AUTH** | 인증/온보딩 | 5 | C-001, C-002, C-003, C-011, C-013 |
| **SRV-ACCOUNT** | 계정/프로필 | 3 | C-010, C-012, C-014 |
| **SRV-DASHBOARD** | 대시보드 | 7 | C-004, G-001, P-001, S-001, T-001, A-001, ADM-001 |
| **SRV-RECORD** | 기록 관리 | 13 | C-005, C-006, C-007, G-003, P-002, P-003, S-002, S-003, S-005, T-002, A-002, ADM-002 |
| **SRV-TEMPLATE** | 템플릿 | 3 | C-006, S-003, T-002 |
| **SRV-SHARE** | 공유/내보내기 | 4 | C-008, G-005, S-006, T-003 |
| **SRV-NOTIFY** | 알림 | 3 | C-009, P-005, ADM-002 |
| **SRV-PROFILE** | 당사자 프로필/목표 | 3 | P-004, P-006, A-004 |
| **SRV-FAMILY** | 가족 관리 | 2 | G-002, G-004 |
| **SRV-WORK** | 업무 협업 | 4 | S-004, S-005, T-004, A-003 |

> **참고**: C-006(기록 생성/수정), S-003(기록 생성/수정), T-002(IEP 생성/수정)은 SRV-RECORD + SRV-TEMPLATE의 중복 포함

### 2.2 서비스별 레이어 매핑矩阵

각 서비스의 화면이 L3~L6에서 어떻게 계층화되는지 정의한다.

```
SRV-AUTH (인증/온보딩)
├── L6: SplashPage, LoginPage, RoleOnboardingPage, AccountRegisterPage, ForgotPasswordPage
├── L5: AuthVM, EmailVerificationVM, RoleSelectionVM
├── L4: AuthService, OtpService, RegistrationUseCase
├── L3: User Entity, Role Enum, Permission Enum
└── L2: AuthApiAdapter, EmailServiceAdapter

SRV-DASHBOARD (대시버스)
├── L6: DashboardPage (role-specific variants)
├── L5: DashboardVM (role-specific: GuardianDashboardVM, PersonDashboardVM, etc.)
├── L4: GetDashboardSummaryUseCase, GetRecentRecordsUseCase
├── L3: DashboardSummary, Record Summary, User Context
└── L2: DashboardApiAdapter, CacheStore (dashbaord summary 60s TTL)

SRV-RECORD (기록 관리)
├── L6: RecordListView, RecordDetailView, RecordCreatePage, RecordEditPage
├── L5: RecordListVM, RecordDetailVM, RecordFormVM, RecordTemplateVM
├── L4: CreateRecordUseCase, UpdateRecordUseCase, DeleteRecordUseCase, GetRecordsUseCase
├── L3: Record Entity, Template Entity, RecordCategory, LifespanStage
└── L2: RecordApiAdapter, TemplateApiAdapter, FileStorageAdapter

SRV-SHARE (공유/내보내기)
├── L6: ShareSheet, P dfExportPage, CsvExportModal
├── L5: ShareVM, PdfExportVM
├── L4: ExportPdfUseCase, ShareLinkUseCase, ExportCsvUseCase
├── L3: ShareLink, ExportConfig, PermissionScope
└── L2: PdfGenerator, LinkServiceAdapter, CsvGenerator

SRV-NOTIFY (알림)
├── L6: NotificationCenterPage, NotificationListItem
├── L5: NotificationVM
├── L4: ReadNotificationUseCase, GetNotificationsUseCase, SubscribePushUseCase
├── L3: Notification Entity, NotificationType Enum
└── L2: NotificationApiAdapter, PushServiceAdapter (WebSocket/Firebase)
```

---

## 3. 화면별 컴포넌트 트리구조 (Component Tree)

각 화면의 L6 (Presentation) 컴포넌트 트리구조를 정의한다.

** notation convention: **
- `<Page>` — 최상위 페이지 레이아웃
- `<Layout>` — 글로벌 레이아웃 영역 (Header, Navigation, Main, Footer/Drawer)
- `<Shell>` — 화면별 컨테이너 레이아웃
- `<Section>` — 섹션 단위 (card list, chart, form group 등)
- `<View>` — 복합 UI 블록 (데이터 표시 + 인터랙션)
- `<Component>` — 재사용 가능한 단일 UI 요소 (Button, Input, Card)

### 3.1 SRV-AUTH (인증)

#### C-001: Splash / Onboarding

```
<SplashPage>
  <Layout type="full-screen-overlay">
    <Section region="brand-intro">
      <BrandLogo />               <!-- /docs/brand-bi-ould.html: Logo asset -->
      <Typography variant="H1">lifeNest</Typography>
      <Typography variant="Body">당신의 생애, 하나의 기록</Typography>
    </Section>
    <Section region="feature-list">
      <FeatureCard variant="lifespan-record" />
      <FeatureCard variant="multi-recorder" />
      <FeatureCard variant="auto-permission-transfer" />
    </Section>
    <Section region="cta">
      <Button variant="primary" size="full" />
    </Section>
  </Layout>
</SplashPage>
```

#### C-002: Login / Email OTP

```
<LoginPage>
  <Layout type="centered-card" width="40% (D+)" />
    <Shell>
      <Section region="header">
        <BrandLogo />
        <Typography variant="H2">로그인</Typography>
      </Section>
      <Section region="form">
        <Form state="loginForm">
          <Field variant="text-input" name="email" />     <!-- Full width, 40px (D+) -->
          <Field variant="password-input" name="password" />
          <Field variant="otp-input" name="otp" count="6" />
        </Form>
      </Section>
      <Section region="actions">
        <Link href="/forgot-password">비밀번호 찾기</Link>
        <Link href="/register">회원가입</Link>
      </Section>
      <Section region="submit">
        <Button variant="primary" size="full" />
      </Section>
    </Shell>
  </Layout>
</LoginPage>
```

#### C-003 / C-011: Role Onboarding / Register

```
<RoleOnboardingPage>
  <Layout type="centered-card" width="40% (D+)" />
    <Shell>
      <Section region="role-selection">
        <RoleSelector>
          <RoleCard role="guardian" label="보호자" />
          <RoleCard role="person" label="당사자" />
          <RoleCard role="professional" label="전문인력" />
        </RoleSelector>
      </Section>
      <Section region="form">
        <Form state="registrationForm">
          <Field variant="text-input" name="email" />
          <Field variant="password-input" name="password" />
          <Field variant="select" name="role" options="guardian|person|professional" />
        </Form>
      </Section>
      <Section region="submit">
        <Button variant="primary" size="full" />
      </Section>
    </Shell>
  </Layout>
</RoleOnboardingPage>
```

### 3.2 SRV-DASHBOARD (대시보드)

#### C-004: Common Dashboard (Role-specific)

```
<DashbaordPage>
  <Layout type="global" nav="bottom-bar (S/T) | sidebar (D+)" width="1140px (D+ max)">
    <Shell>
      <!-- Shared Header -->
      <Section region="header">
        <TopBar>
          <BrandLogo small />
          <Typography variant="H1">대시보드</Typography>
          <NotificationCenterBadge />
          <UserProfileAvatar />
        </TopBar>
        <RoleSwitcher />
      </Section>

      <!-- Role-specific Summary Cards -->
      <Section region="summary">
        <SummaryCard variant="record-count" />
        <SummaryCard variant="pending-approval" />
        <SummaryCard variant="upcoming-deadline" />
        <SummaryCard variant="total-users" />
      </Section>

      <!-- Role-specific Main Content -->
      <Section region="main">
        <!-- Role: Guardian -->
        <!-- FamilyCard list (G-001) + RecentRecord list + QuickPDF -->

        <!-- Role: Person -->
        <!-- Simple 2 Cards: RecentRecord + NextAppointment -->

        <!-- Role: Social Worker -->
        <!-- CaseSummary table + TodayTasks + Reminders -->

        <!-- Role: Special Teacher -->
        <!-- IEP Goal + ProgressRate + RecordList -->

        <!-- Role: Support Worker -->
        <!-- Timeline view: Today's schedule -->

        <!-- Role: Admin -->
        <!-- Institution stats + User stats + Permission overview -->
      </Section>

      <!-- Bottom Navigation (S/T only) -->
      <Section region="bottom-nav" visible="(S/T)">
        <BottomBar>
          <BottomNavItem icon="dashboard" label="대시보드" />
          <BottomNavItem icon="records" label="기록" />
          <BottomNavItem icon="notifications" label="알림" />
          <BottomNavItem icon="calendar" label="일정" />
          <BottomNavItem icon="profile" label="프로필" />
        </BottomBar>
      </Section>

      <!-- Fixed Footer (S/T only) -->
      <Section region="footer" visible="(S/T)">
        <FooterBrand />
      </Section>
    </Shell>
  </Layout>
</DashboardPage>
```

### 3.3 SRV-RECORD (기록 관리)

#### C-005: Record Detail

```
<RecordDetailPage>
  <Layout type="full-page" nav="global">
    <Shell>
      <Section region="header">
        <Breadcrumb>
          <BreadcrumbItem label="기록" href="/records" />
          <BreadcrumbItem label="{{title}}" current />
        </Breadcrumb>
        <RecordActions>
          <Button variant="ghost" icon="edit" />
          <Button variant="ghost" icon="download" />
          <Button variant="ghost" icon="share" />
          <Button variant="ghost" icon="history" />
        </RecordActions>
      </Section>

      <Section region="metadata">
        <RecordMetaCard>
          <MetaField label="카테고리" value="{{category}}" />
          <MetaField label="생애주기" value="{{lifespanStage}}" />
          <MetaField label="작성일자" value="{{createdDate}}" />
          <MetaField label="작성자" value="{{author}}" />
          <MetaField label="공개범위" value="{{visibility}}" />
        </RecordMetaCard>
      </Section>

      <Section region="content">
        <RecordFormView readonly>
          <Field variant="text-display" name="title" value="{{title}}" />
          <Field variant="text-display" name="description" value="{{description}}" />
          <Field variant="display" name="date" value="{{date}}" />
          <Field variant="display" name="select" value="{{type}}" />
          <Field variant="file-display" name="attachment" />
          <!-- Supports 10+ field types per UX Spec §5.4 -->
        </RecordFormView>
      </Section>

      <Section region="history">
        <RecordHistoryTimeline>
          <HistoryItem date="{{timestamp}}" user="{{name}}" action="{{action}}" />
        </RecordHistoryTimeline>
      </Section>
    </Shell>
  </Layout>
</RecordDetailPage>
```

#### C-006: Record Create / Edit

```
<RecordCreatePage>
  <Layout type="split-pane (D+)" nav="global">
    <Shell>
      <!-- Side: Template Selector (D+) -->
      <Section region="template-panel" visible="(D+)">
        <TemplateSelector>
          <TemplateGroup label="영유아기">
            <TemplateCard template="{{birth_record}}" />
            <TemplateCard template="{{health_check}}" />
          </TemplateGroup>
          <TemplateGroup label="학령기">
            <TemplateCard template="{{iep}}" />
            <TemplateCard template="{{behavior_record}}" />
          </TemplateGroup>
          <TemplateGroup label="Adult">
            <TemplateCard template="{{self_introduction}}" />
            <TemplateCard template="{{satisfaction_survey}}" />
          </TemplateGroup>
        </TemplateSelector>
      </Section>

      <!-- Main: Form -->
      <Section region="form">
        <Form state="recordForm" template="{{selectedTemplate}}">
          <Field variant="text-input" field="title" />
          <Field variant="textarea" field="description" maxLength="1000" />
          <Field variant="select" field="category" chips />
          <Field variant="date-picker" field="date" />
          <Field variant="file-upload" field="attachment" maxSize="10MB" />
          <!-- Dynamic fields based on template schema -->
        </Form>
        <FormValidation state="recordForm" mode="real-time" />
      </Section>

      <Section region="actions">
        <Button variant="secondary" label="임시저장" />
        <Button variant="primary" label="작성완료" />
      </Section>
    </Shell>
  </Layout>
</RecordCreatePage>
```

#### S-001: Social Worker Case Management Dashboard

```
<CaseManagementDashboard>
  <Layout type="multi-column (D+)" nav="global">
    <Shell>
      <Section region="header">
        <TopBar>
          <Typography variant="H1">케이스 관리</Typography>
          <!-- Role indicator: 사회복지사 -->
        </TopBar>
      </Section>

      <!-- Summary Row -->
      <Section region="summary">
        <SummaryCard variant="total-cases" label="총 케이스" />
        <SummaryCard variant="active-cases" label="활성" />
        <SummaryCard variant="overdue-cases" label="리마인더" />
        <SummaryCard variant="pending-approval" label="승인대기" />
      </Section>

      <!-- Main: Today's Tasks -->
      <Section region="tasks">
        <TaskList title="오늘 할일">
          <TaskItem type="follow-up" label="{{caseName}} — 후속 미팅" deadline="{{dueDate}}" />
          <TaskItem type="approval" label="{{recordTitle}} 검토" action="approve/reject" />
          <TaskItem type="reminder" label="{{name}} — 기록 작성 만료" />
        </TaskList>
      </Section>

      <!-- Main: Cases Table (D+) / Card List (S) -->
      <Section region="cases">
        <CaseTable>
          <!-- D+: Full data table with columns -->
          <!-- S/T: Card list with key info -->
        </CaseTable>
      </Section>

      <!-- FAB (S/T only) -->
      <Section region="fab" visible="(S/T)">
        <FloatingActionButton variant="primary" label="새 기록" />
      </Section>
    </Shell>
  </Layout>
</CaseManagementDashboard>
```

### 3.4 SRV-PROFILE (당사자)

#### P-001: Person Dashboard (Easy Mode)

```
<PersonDashboard>
  <Layout type="centered (D+)" nav="bottom-bar">
    <Shell variant="easy-mode">
      <Section region="header">
        <EasyModeTopBar>
          <BrandLogo small />
          <EasyModeToggle />                  <!-- P-006 토글 -->
          <UserProfileAvatar large />         <!-- 64px touch target in Easy Mode -->
        </EasyModeTopBar>
      </Section>

      <Section region="welcome">
        <Typography variant="H1" size="easy">안녕, {{name}}씨!</Typography>
      </Section>

      <!-- Only 2 cards as per UX Spec §4.3 -->
      <Section region="recents">
        <RecordCard variant="recent" />         <!-- 최근 기록 카드 -->
      </Section>

      <Section region="next-event">
        <AppointmentCard variant="next" />     <!-- 다음 예약 카드 -->
      </Section>

      <!-- Bottom Navigation (S/T & Easy Mode) -->
      <Section region="bottom-nav">
        <EasyModeBottomBar>
          <EasyNavItem icon="home" label="홈" selected />
          <EasyNavItem icon="records" label="기록" />
          <EasyNavItem icon="goals" label="목표" />
          <EasyNavItem icon="profile" label="내 프로필" />
        </EasyModeBottomBar>
      </Section>
    </Shell>
  </Layout>
</PersonDashboard>
```

#### P-003: Self Recording (Easy Mode — 1면 1필드)

```
<SelfRecordingPage>
  <Layout type="single-field (Easy Mode)" nav="minimal">
    <Shell variant="easy-mode">
      <Section region="question">
        <EasyModeQuestionCard>
          <Typography variant="H2" size="easy">오늘 기분이 어때요?</Typography>
          <EmojiSelector>
            <EmojiButton value="happy"   label="😊 좋았어요" size="64px" />
            <EmojiButton value="ok"      label="🙂 그냥 그래" size="64px" />
            <EmojiButton value="sad"     label="😢 슬펐어요" size="64px" />
            <EmojiButton value="angry"   label="😠 화났어요"  size="64px" />
            <EmojiButton value="tired"   label="😫 피곤해요"  size="64px" />
          </EmojiSelector>
        </EasyModeQuestionCard>
      </Section>

      <Section region="progress">
        <ProgressIndicator variant="number-only" label="1 / 5" />
      </Section>
    </Shell>
  </Layout>
</SelfRecordingPage>
```

### 3.5 SRV-SHARE (공유/내보내기)

#### C-008 / G-005: PDF Export / Share

```
<ShareExportPage>
  <Layout type="modal (D+) | bottom-sheet (S/T)" nav="modal-overlay">
    <Shell>
      <Section region="selections">
        <RecordSelectionList>
          <!-- Single / Multiple selection -->
          <SelectionItem variant="record-card" selected />
        </RecordSelectionList>
      </Section>

      <Section region="export-options">
        <ExportOptionCard variant="pdf" label="PDF 출력" icon="document" />
        <ExportOptionCard variant="csv" label="CSV 출력" icon="table" />
        <ExportOptionCard variant="link-share" label="링크 공유" icon="link" />
      </Section>

      <Section region="status">
        <PdfExportStatus>
          <StatusMessage variant="pending"> PDF 생성 대기 중...</StatusMessage>
          <ProgressBar variant="linear" indeterminate />
        </PdfExportStatus>
        <PdfExportStatus>
          <StatusMessage variant="complete"> 생성 완료!</StatusMessage>
          <Button variant="primary" label="다운로드" />
          <Button variant="secondary" label="공유" />
        </PdfExportStatus>
      </Section>
    </Shell>
  </Layout>
</ShareExportPage>
```

### 3.6 SRV-NOTIFY (알림)

#### C-009: Notification Center

```
<NotificationCenterPage>
  <Layout type="drawer (D+) | full-page (S/T)" nav="global">
    <Shell>
      <Section region="header">
        <TopBar>
          <Typography variant="H2">알림</Typography>
          <Button variant="ghost" label="모두 읽음" icon="check-all" />
        </TopBar>
      </Section>

      <Section region="notifications">
        <NotificationList>
          <NotificationItem variant="unread">
            <NotificationIcon type="record-added" />
            <NotificationContent>
              <NotificationTitle>{{recorderName}}님이 {{recordTitle}} 작성</NotificationTitle>
              <NotificationTimestamp>{{relativeTime}}</NotificationTimestamp>
            </NotificationContent>
            <NotificationAction type="mark-read" />
          </NotificationItem>
          <!-- Template-based item rendering -->
          <!-- Types: record-added, approval-request, invitation, system -->
        </NotificationList>
      </Section>
    </Shell>
  </Layout>
</NotificationCenterPage>
```

### 3.7 SRV-FAMILY (가족 관리) — Guardian

#### G-002: Family Member List

```
<FamilyMemberListPage>
  <Layout type="global" nav="bottom-bar (S/T) | sidebar (D+)">
    <Shell>
      <Section region="header">
        <TopBar>
          <Typography variant="H2">가족 구성원</Typography>
          <Button variant="primary" label="당사자 추가" icon="plus" />
        </TopBar>
      </Section>

      <Section region="member-list">
        <!-- S: Full list, T: Grid 2col, D+: Table + Tree -->
        <MemberCard>
          <MemberAvatar />
          <MemberInfo>
            <MemberName>{{name}}</MemberName>
            <MemberMeta>장애등급: {{grade}} · 생애주기: {{stage}}</MemberMeta>
          </MemberInfo>
          <MemberActions>
            <Button variant="ghost" label="권한 관리" />
            <Button variant="ghost" label="기록 열람" />
          </MemberActions>
        </MemberCard>
      </Section>
    </Shell>
  </Layout>
</FamilyMemberListPage>
```

### 3.8 SRV-WORK (업무 협업)

#### S-004: Invite Collaborator

```
<InviteCollaboratorPage>
  <Layout type="modal (D+) | bottom-sheet (S/T)" nav="global">
    <Shell>
      <Section region="header">
        <Typography variant="H3">협업자 초대</Typography>
      </Section>

      <Section region="form">
        <InviteForm>
          <Field variant="text-input" name="email" placeholder="초대할 이메일" />
          <Field variant="select" name="role" options="social-worker|special-teacher|support-worker" />
          <Field variant="text-input" name="access-scope" placeholder="접근 범위" />
          <Field variant="date-range" name="period" />
        </InviteForm>
      </Section>

      <Section region="actions">
        <Button variant="primary" label="초대 보내기" />
        <Button variant="secondary" label="취소" />
      </Section>

      <!-- Invitation Tracking (if any existing) -->
      <Section region="invitations">
        <InvitationStatusList>
          <InvitationStatusItem status="pending" label="초대 대기중" />
          <InvitationStatusItem status="accepted" label="수락 완료" />
          <InvitationStatusItem status="expired" label="만료" />
        </InvitationStatusList>
      </Section>
    </Shell>
  </Layout>
</InviteCollaboratorPage>
```

### 3.9 SRV-TEMPLATE (템플릿)

#### C-006 / S-003 / T-002: Template-based Form

```
<TemplateFormView>
  <Layout type="split-pane (D+) | scroll-form (S/T)" nav="global">
    <Shell>
      <!-- Template Panel (D+ only) -->
      <Section region="template-panel">
        <TemplateGroup label="영유아기">
          <TemplateCard>출생기록</TemplateCard>
          <TemplateCard>건강체크</TemplateCard>
          <TemplateCard>발달평가</TemplateCard>
        </TemplateGroup>
        <TemplateGroup label="학령기">
          <TemplateCard>IEP</TemplateCard>
          <TemplateCard>행동기록</TemplateCard>
          <TemplateCard>학급일지</TemplateCard>
        </TemplateGroup>
        <TemplateGroup label="성인기">
          <TemplateCard>자기소개서</TemplateCard>
          <TemplateCard>만족도조사</TemplateCard>
          <TemplateCard>자립계획</TemplateCard>
        </TemplateGroup>
        <TemplateGroup label="노년기">
          <TemplateCard>건강관리일지</TemplateCard>
          <TemplateCard>돌봄평가</TemplateCard>
        </TemplateGroup>
      </Section>

      <!-- Form (all breakpoints) -->
      <Section region="form">
        <Form state="templateForm" template="{{selected}}">
          <!-- Fields rendered from template schema -->
          <!-- Supports 10 field types: text, textarea, select, date, file,
               checkbox, radio, emoji, rating, signature -->
        </Form>
        <FormValidation mode="real-time" />
      </Section>
    </Shell>
  </Layout>
</TemplateFormView>
```

### 3.10 SRV-ACCOUNT (계정)

#### C-010 / C-014: Settings & Profile

```
<SettingsPage>
  <Layout type="centered-card (D+)" nav="global">
    <Shell>
      <Section region="profile">
        <ProfileCard>
          <ProfileAvatar />
          <ProfileInfo>
            <ProfileName>{{name}}</ProfileName>
            <ProfileRole>{{role}}</ProfileRole>
          </ProfileInfo>
          <Button variant="ghost" label="프로필 수정" />
        </ProfileCard>
      </Section>

      <Section region="settings">
        <SettingsGroup title="계정">
          <SettingsItem type="change-email" />
          <SettingsItem type="change-password" />
          <SettingsItem type="role-change-request" />
        </SettingsGroup>
        <SettingsGroup title="알림">
          <SettingsToggle type="notification-email" />
          <SettingsToggle type="notification-push" />
          <SettingsToggle type="notification-sms" />
        </SettingsGroup>
        <SettingsGroup title="기타">
          <SettingsItem type="language" />
          <SettingsItem type="theme" />
          <SettingsItem type="delete-account" variant="danger" />
        </SettingsGroup>
      </Section>
    </Shell>
  </Layout>
</SettingsPage>
```

---

## 4. 상태 관리 아키텍처

### 4.1 상태 계층

```
┌─────────────────────────────────────────────────────────────┐
│ L5: View Module State                                        │
│  ├── useScreenVM()    — 화면별 상태 (local to screen)        │
│  ├── useFormState()   — 폼 상태 (controlled, validated)      │
│  └── useFieldState()  — 필드별 상태 (per-field validation)   │
├─────────────────────────────────────────────────────────────┤
│ L4: Feature State                                            │
│  ├── useUseCase()      — UseCase 실행 상태                   │
│  ├── useFeatureStore() — 화면간 공유 상태 (session-scoped)    │
│  └── useNavigationState() — 라우팅/내비게이션 상태           │
├─────────────────────────────────────────────────────────────┤
│ L2/L1: Infrastructure State                                  │
│  ├── QueryClient      — 서버 상태 캐시 (React Query style)   │
│  ├── WebSocketStore   — 실시간 알림 상태                    │
│  └── LocalStorage     — 로컬 프리퍼런스 / OAuth token        │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 상태 소유권 규칙

| 상태 유형 | 소유 계층 | 공유 범위 | 지속 기간 |
|-----------|----------|----------|----------|
| **UI 상태** (모달 열림, 탭 선택, 스크롤 위치) | L5 (View Module) | 화면 내 | 세션 |
| **폼 상태** (입력값, 검증 에러, touched) | L5 (View Module) | 화면 내 | 포맷 생명주기 |
| **비즈니스 상태** (로딩, 성공, 에러) | L4 (Feature Store) | 도메인 단위 | 세션 |
| **서버 상태** (원천 진실) | L2 (Query Client) | 전역 | 캐시 + 재생成的 |
| **실시간 상태** (알림 도착) | L1 (WebSocket) | 전역 | 연결 생명주기 |
| **퍼퍼런스** (이지 모드, 테마, 언어) | L2 (Session Store) | 전역 | 지속 저장 |

### 4.3 상태 플로우 예시: 기록 생성

```
L6: RecordCreatePage.render()
  │
  ├── L5: RecordFormVM.useState()
  │     ├─ title: "" (local)
  │     ├─ template: null (local)
  │     └─ isSubmitting: false (local)
  │
  ├── L4: CreateRecordUseCase.submit(formValues)
  │     ├─ isSubmitting → true (feature state)
  │     └─ calls L2: RecordApiAdapter.create()
  │           └── L1: HTTP POST /api/v1/records
  │
  ├── Success → L4 state → L5 state → L6 rerender → Navigate to Detail
  └── Error → L4 state.error → L5 validation UI → Toast notification
```

---

## 5. 데이터 흐름 (Data Flow)

### 5.1 CRUD 흐름

```
CREATE:
  L6 (RecordCreatePage)
    → L5 (FormState.setValues())
      → L4 (CreateRecordUseCase.execute(dto))
        → L2 (RecordApiAdapter.create(data))
          → L1 (HTTP POST /records)
            → Response → L2.parse() → L4.mapDomain()
              → L5 (SuccessState) → L6 (navigate)

READ:
  L6 (RecordListView)
    → L4 (GetRecordsUseCase.execute(filters))
      → L2 (RecordApiAdapter.list(params))
        → L1 (HTTP GET /records?...)
          → Response → L2.parse() → Cache store
            → L3 Domain entities → L4 (return list)
              → L5 (listState = data) → L6 (render cards)

UPDATE:
  L6 (RecordEditPage)
    → L5 (FormState.load(entity))
      → L4 (UpdateRecordUseCase.execute(id, dto))
        → L2 (RecordApiAdapter.update(id, data))
          → L1 (HTTP PATCH /records/:id)

DELETE:
  L6 (RecordDetailPage → confirm dialog)
    → L4 (DeleteRecordUseCase.execute(id))
      → L2 (RecordApiAdapter.delete(id))
        → L1 (HTTP DELETE /records/:id)
```

### 5.2 실시간 알림 흐름 (WebSocket)

```
L1: WebSocket.connect('/ws/notifications')
   → authenticated by L1 token

L2: NotificationAdapter.onMessage(message)
   → parse message → map to L3 Notification entity

L4: NotificationFeature.pushNotification(notification)
   → UpdateFeatureStore

L5: NotificationVM.state.receivedNotifications
   → subscribe via useSyncExternalStore

L6: NotificationCenter render new badge count
   → push notification (browser API)
```

---

## 6. 레이어별 의존성 방향

### 6.1 참조 규칙

```
──────────────────────────────────────────────────────
│          의존성 화살표:  → 는 "참조/사용" 의미       │
──────────────────────────────────────────────────────

L6 (Presentation)
  ├── 참조 → L5 (View Module)          ✅ 허용
  ├── 참조 → L4 (Feature/UseCase)       ✅ 허용 (UI event → UseCase 호출)
  └── 참조 → L3 (Domain Entities)      ❌ 금지 — DTO 사용
       L2 (Infrastructure)              ❌ 금지 — Adapter interface 사용
       L1 (Infrastructure)              ❌ 금지

L5 (View Module)
  ├── 참조 → L4 (Feature/UseCase)       ✅ 허용
  ├── 참조 → L3 (Domain Entities)       ✅ 허용 (ValueObject 활용)
  └── 참조 → L2/L1                       ❌ 금지

L4 (Feature)
  ├── 참조 → L3 (Domain Entities)        ✅ 허용 (핵심)
  └── 참조 → L2 (Infrastructure)         ✅ 허용 (Repository interface)

L3 (Domain)
  ├── 참조 → L2 (Infrastructure)         ✅ 허용 (interface 정의만)
  ├── 참조 → L1 (Infrastructure)         ✅ 허용 (interface 정의만)
  └── 참조 → 상위 계층                   ❌ 절대 금지

L2 (Infrastructure)
  ├── 참조 → L3 (Domain)                 ✅ 허용 (interface 구현)
  ├── 참조 → L1 (Infrastructure)         ✅ 허용
  └── 참조 → 상위 계층                   ❌ 금지

L1 (Data)
  ├── 참조 → L2 (Infrastructure)         ✅ 허용 (adapter 구현)
  └── 참조 → 상위 계층                   ❌ 금지
```

### 6.2 L3 → L2 의존성 역전 예시

```typescript
// L3 Domain: Repository Interface (계약 정의)
interface RecordRepository {
  findAll(filters: RecordFilters): Promise<Record[]>;
  findById(id: string): Promise<Record | null>;
  create(record: Record): Promise<Record>;
  update(id: string, record: Record): Promise<Record>;
  delete(id: string): Promise<void>;
}

// L2 Infrastructure: HTTP Adapter (계약 구현)
class HttpRecordRepository implements RecordRepository {
  constructor(private apiClient: HttpClient, private cache: CacheStore) {}

  async findAll(filters: RecordFilters): Promise<Record[]> {
    const cached = this.cache.get('records', filters);
    if (cached) return cached;

    const { data } = await this.apiClient.get('/records', { params: filters });
    this.cache.set('records', filters, data);
    return data.map(Record.parse);
  }
  // ...other methods
}
```

---

## 7. 모바일 ↔ 데스크탑 반응형 계층 매핑

### 7.1 반응형 분기 전략

```
Layout 컴포넌트에서 breakpoint별 분기
┌──────────────────────────────────────────────────┐
│ L6 Layout Layer에서 S/M/T/D/L breakpoint 확인     │
│  └── CSS custom props 또는 hook을 통해 레이아웃 전환│
└──────────────────────────────────────────────────┘

Navigation:
  S/T (≤768px):  BottomBar (5-item icon bar)
  D+ (>768px):   Sidebar (280px fixed, per BrandBI)

Modal:
  S: Full-screen overlay
  T: Center 60%
  D+: Center modal 40-60% width

Form:
  S/T: Scroll form (vertical stack)
  D+: Split pane (template left / form right)
```

### 7.2 Breakpoint별 컴포넌트 매핑

| Breakpoint | Layout Type | Touch Target | Navigation | Modal Type | Form Type |
|------------|------------|--------------|------------|------------|-----------|
| **S** (≤480px) | Full page | 48px | BottomBar | Full-screen | Scroll |
| **M** (≤768px) | Full page | 44px | BottomBar | Full-screen | Scroll |
| **T** (≤1024px) | Full page | 44px | BottomBar/Sidebar | Center | Scroll |
| **D** (≤1280px) | 1140px max | 40px | Sidebar | Center | Split pane |
| **L** (>1280px) | 1140px max | 40px | Sidebar | Center | Split pane |

### 7.3 이지 모드 (Easy Mode) 레이어 오버라이트

```
Easy Mode 활성화 시 L6 컴포넌트 오버라이트:

L6 컴포넌트
  ├── Typography:  16px → 20px base
  ├── Button:      48px → 64px touch target
  ├── Line height: 1.5 → 1.8
  ├── Form:        multi-field → single-field-per-screen (P-003)
  ├── Icon:        standard → large + label
  ├── Color:       standard palette → high contrast (7:1+)
  └── Feedback:    standard → enhanced (larger toasts, visual cues)

오버라이트는 CSS custom properties 또는 EasyModeContext를 통해 적용:
  --base-font-size: 20px
  --touch-target-min: 64px
  --line-height: 1.8
  --contrast-ratio-min: 7:1
```

---

## 부록 A: 화면 ID — 서비스/역할 매핑

| 화면 ID | 화면명 | 서비스 | 역할 |
|---------|--------|--------|------|
| C-001 | 스플래시 / 온보딩 | SRV-AUTH | All |
| C-002 | 로그인 / 이메일 OTP | SRV-AUTH | All |
| C-003 | 역할 온보딩 | SRV-AUTH | All |
| C-004 | 대시보드 | SRV-DASHBOARD | All |
| C-005 | 기록 상세 | SRV-RECORD | All |
| C-006 | 기록 생성/수정 | SRV-RECORD + SRV-TEMPLATE | All |
| C-007 | 검색/필터 | SRV-RECORD | All |
| C-008 | PDF 출력 | SRV-SHARE | All |
| C-009 | 알림 센터 | SRV-NOTIFY | All |
| C-010 | 설정/프로필 | SRV-ACCOUNT | All |
| C-011 | 역할 등록 | SRV-AUTH | All |
| C-012 | 이메일 인증 | SRV-ACCOUNT | All |
| C-013 | 비밀번호 찾기 | SRV-AUTH | All |
| C-014 | 계정 설정 | SRV-ACCOUNT | All |
| G-001 | 보호자 대시보드 | SRV-DASHBOARD | Guardian |
| G-002 | 가족 구성원 목록 | SRV-FAMILY | Guardian |
| G-003 | 타임라인 뷰 | SRV-RECORD | Guardian |
| G-004 | 카테고리 필터 | SRV-FAMILY | Guardian |
| G-005 | 공유/내보내기 | SRV-SHARE | Guardian |
| P-001 | 당사자 대시보드 | SRV-DASHBOARD | Person |
| P-002 | 당사자 기록 열람 | SRV-RECORD | Person |
| P-003 | 당사자 자기 기록 작성 | SRV-RECORD | Person |
| P-004 | 당사자 프로필 & 목표 | SRV-PROFILE | Person |
| P-005 | 당사자 알림 | SRV-NOTIFY | Person |
| P-006 | 이지 모드 토글 | SRV-PROFILE | Person |
| S-001 | 케이스 관리 대시보드 | SRV-DASHBOARD | Social Worker |
| S-002 | 케이스 상세 페이지 | SRV-RECORD | Social Worker |
| S-003 | 기록 생성/수정 | SRV-RECORD + SRV-TEMPLATE | Social Worker |
| S-004 | 협업자 초대 | SRV-WORK | Social Worker |
| S-005 | 기록 목록 뷰 | SRV-RECORD | Social Worker |
| S-006 | 팀 협업 뷰 | SRV-SHARE | Social Worker |
| T-001 | IEP 대시보드 | SRV-DASHBOARD | Special Teacher |
| T-002 | IEP 생성/수정 | SRV-RECORD + SRV-TEMPLATE | Special Teacher |
| T-003 | IEP 보호자 공유 | SRV-SHARE | Special Teacher |
| T-004 | 학생 목록 | SRV-WORK | Special Teacher |
| A-001 | 일일 기록 대시보드 | SRV-DASHBOARD | Support Worker |
| A-002 | 일일 기록 | SRV-RECORD | Support Worker |
| A-003 | 주간 요약 | SRV-WORK | Support Worker |
| A-004 | 선호 리스트 | SRV-PROFILE | Support Worker |
| ADM-001 | 관리자 대시보드 | SRV-DASHBOARD | Admin |
| ADM-002 | 법정 이관 | SRV-RECORD | Admin |

---

## 부록 B: 용어 정의

| 용어 | 정의 |
|------|------|
| **Page** | L6 최상위 컴포넌트. 단일 라우트 대응 |
| **Layout** | 전역 레이아웃. Header/Nav/Main/Footer 구조 |
| **Shell** | 화면별 컨테이너. Page 내 영역 구분 |
| **Section** | 레이아웃 영역. Region 기반 배치 |
| **Component** | 재사용 가능한 최소 UI 단위 |
| **View** | 복합 UI 블록. 데이터 표시 + 인터랙션 |
| **Form** | 입력 필드 집합. State + Validation |
| **VM** | View Module. 화면별 상태 + UI 로직 |
| **UseCase** | L4 기능 단위. 유저Goal 기반 |
