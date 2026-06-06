# LifeLog — 데이터 정의서 (Data Definition)

> **버전**: v1.0 | **작성일**: 2026-06-06 | **기준 문서**: PRD v1.0 · UX Design Spec v1.0 · Workflow v1.0 · UI Layer Architecture v1.0
>
> **대상**: 개발팀 · 데이터베이스 · QA · 법무
>
> **플랫폼**: 발달장애인 생애전주기 기록 플랫폼 LifeLog — Phase 1 MVP

---

## 목차

1. [데이터 모델 개요](#1-데이터-모델-개요)
2. [ERD (Entity Relationship Diagram)](#2-erd-entity-relationship-diagram)
3. [테이블 명세서 (Table Specifications)](#3-테이블-명세서-table-specifications)
4. [열(컬럼) 정의 (Column Definitions)](#4-열컬럼-정의-column-definitions)
5. [Enum / 코드 정의](#5-enum--코드-정의)
6. [데이터 상태 전이도 (State Transitions)](#6-데이터-상태-전이도-state-transitions)
7. [인덱스 정의](#7-인덱스-정의)
8. [JSONB 스키마 정의](#8-jsonb-스키마-정의)
9. [데이터 보존 및 삭제 정책](#9-데이터-보존-및-삭제-정책)

---

## 1. 데이터 모델 개요

### 1.1 설계 원칙

| 원칙 | 설명 |
|------|------|
| **당사자 중심** | 모든 핵심 테이블은 `party_id`를 통해 당사자(장애인 본인)를 핵심 축으로 연결 |
| **역할별 RBAC** | 사용자-역할-속성 3층 구조. 1 사용자가 1 역할만 보유(역할 변경 시 신규 계정) |
| **생애주기 기반** | 당사자-생애주기 자동 계산. 기록·템플릿이 생애주기 × 카테고리 2차원 행렬에 매핑 |
| **JSONB 유동성** | 기록 콘텐츠는 템플릿 정의에 따라 동적 폼 생성. 구조화된 JSONB + GIN 인덱스 |
| **소프트 딜리트** | 모든 핵심 엔티티 `deleted_at` 보유. 법적 보존 의무 준수 |
| **감사 가능** | `created_at`/`updated_at`/`created_by`/`updated_by` 전 테이블 공통 |

### 1.2 핵심 엔티티 관계도 ( conceptual )

```
User (계정)
  │
  ├─── RoleAssignment (역할)
  │       │
  │       └── RoleType: GUARDIAN | PERSON | SOCIAL_WORKER | SPECIAL_TEACHER | SUPPORT_WORKER | ADMIN
  │
  ├─── PartyProfile (당사자)
  │       │
  │       ├── LifecycleStage (계산값: infant/early-childhood/adolescent/young-adult/middle-adult/older-adult)
  │       ├── Records × 1:N
  │       ├── Templates × N:M (Many-to-Many via RecordTemplate)
  │       ├── Invitations × 1:N (초대)
  │       ├── PermissionLogs × 1:N (권한 변경 이력)
  │       └── Records (기록) × 1:N
  │               │
  │               ├── Attachment × 1:N
  │               ├── RecordVersion × 1:N (수정 이력)
  │               ├── RecordTag × N:M (태그)
  │               └── RecordField × 1:N (동적 필드 값)
  │
  └─── Institution (기관)
          │
          ├── Users (해당 기관 소속 전문가)
          ├── ServiceLinkage × 1:N
          └── PermissionLog × 1:N
```

---

## 2. ERD (Entity Relationship Diagram)

```
┌──────────────────┐    ┌──────────────────────┐    ┌──────────────────────────┐
│      User        │    │   RoleAssignment     │    │       Institution        │
├──────────────────┤    ├──────────────────────┤    ├──────────────────────────┤
│ id (PK)          │───<│ user_id (FK → User)  │    │ id (PK)                  │
│ email            │    │ role_type (Enum)     │    │ name                     │
│ password_hash    │    │ institution_id (FK)  │    │ code (UNIQUE)            │
│ email_verified   │    │ assigned_at          │    │ type                     │
│ refresh_token    │    │ expires_at           │    │ status                   │
│ status           │    │ granted_by           │    │ created_at             │
│ created_at       │    └──────────────────────┘    └───────────┬──────────────┘
│ updated_at       │                                          │
└────────┬─────────┘                                          │
         │                                                    │
         ▼                                                    │
┌──────────────────┐    ┌──────────────────────┐    ┌───────────┴──────────────┐
│  PartyProfile    │    │   Invitation         │    │     ServiceLinkage       │
├──────────────────┤    ├──────────────────────┤    ├──────────────────────────┤
│ id (PK)          │    │ id (PK)              │    │ id (PK)                  │
│ party_id (FK)    │    │ sender_id (FK)       │    │ party_id (FK)            │
│ guardian_id(FK)  │    │ recipient_email      │    │ service_name             │
│ name             │    │ role_type (Enum)     │    │ provider_name            │
│ birth_date       │    │ invitation_type      │    │ start_date               │
│ gender (Enum)    │    │ token (UUID)         │    │ status (Enum)            │
│ disability_type  │    │ status (Enum)        │    │ end_date                 │
│ disability_grade │    │ accepted_at          │    │ notes (JSONB)            │
│ avatar_url       │    │ expires_at           │    └──────────────────────────┘
│ lifecycle_stage  │    │ created_at           │
│ created_at       │    └──────────────────────┘
│ updated_at       │
└────────┬─────────┘    ┌──────────────────────┐
         │               │  PermissionLog       │
         │               ├──────────────────────┤
         │               │ id (PK)              │
         │               │ party_id (FK)        │
         │               │ actor_id (FK → User) │
         │               │ action (Enum)        │
         │               │ target_type          │
         │               │ target_id            │
         │               │ details (JSONB)      │
         │               │ created_at           │
         │               └──────────────────────┘
         │
         ▼
┌──────────────────┐    ┌──────────────────────┐    ┌──────────────────────────┐
│      Record      │    │   Attachment         │    │      RecordTag           │
├──────────────────┤    ├──────────────────────┤    ├──────────────────────────┤
│ id (PK)          │    │ id (PK)              │    │ id (PK)                  │
│ party_id (FK)    │    │ record_id (FK)       │    │ record_id (FK → Record)  │
│ template_id (FK) │    │ file_name            │    │ tag_name (UNIQUE)        │
│ template_field   │    │ storage_path         │    │ record_tag_id (FK)       │
│ category (Enum)  │    │ file_size            │    └──────────────────────────┘
│ life_stage (Enum)│    │ mime_type            │
│ content_type     │    │ thumbnail_path       │
│ status (Enum)    │    │ exif_removed (bool)  │
│ author_id (FK)   │    │ created_at           │
│ visibility (Enum)│    └──────────────────────┘
│ parent_id (FK)   │    ┌──────────────────────┐
│ created_at       │    │  RecordVersion       │
│ updated_at       │    ├──────────────────────┤
│ archived_at      │    │ id (PK)              │
│ deleted_at       │    │ record_id (FK)       │
└──────────────────┘    │ version (int)        │
                        │ content_snapshot     │
                        │ changes (JSONB)      │
                        │ author_id (FK)       │
                        │ created_at           │
                        └──────────────────────┘
```

---

## 3. 테이블 명세서 (Table Specifications)

### TABLE: `users` — 계정 정보

| 용도 | 플랫폼 전체 계정 관리. 이메일/비밀번호 로그인, JWT 토큰, 상태 관리 |
|------|------|
| **PK** | `id` (UUID) |
| **FK 없음** | 독립 계정, 역할은 `role_assignments` 테이블에서 분리 |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | 고유 ID |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | 로그인 식별자 |
| `password_hash` | VARCHAR(255) | NOT NULL | bcrypt hash (cost 12) |
| `email_verified` | BOOLEAN | DEFAULT false | 이메일 인증 여부 |
| `email_verified_at` | TIMESTAMPTZ | NULL | 이메일 인증 시각 |
| `refresh_token` | TEXT | NULL | JWT refresh token |
| `refresh_token_expires_at` | TIMESTAMPTZ | NULL | refresh token 만료 시각 |
| `status` | VARCHAR(20) | DEFAULT 'pending' | `pending` / `active` / `suspended` / `deleted` |
| `locale` | VARCHAR(10) | DEFAULT 'ko-KR' | 언어 설정 |
| `theme` | VARCHAR(20) | DEFAULT 'light' | `light` / `dark` |
| `easy_mode_enabled` | BOOLEAN | DEFAULT false | 당사자 Easy Mode 활성화 |
| `last_login_at` | TIMESTAMPTZ | NULL | 마지막 로그인 시각 |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |
| `updated_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 수정 시각 |
| `deleted_at` | TIMESTAMPTZ | NULL | 소프트 딜리트 |

---

### TABLE: `role_assignments` — 역할 할당

| 용도 | User → 역할 1:1 매핑. RBAC의 기반 테이블 |
|------|------|
| **PK** | `id` (UUID) |
| **FK** | `user_id` → `users.id`, `institution_id` → `institutions.id` |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `user_id` | UUID | FK → `users.id`, UNIQUE, NOT NULL | 1 사용자 = 1 역할 |
| `role_type` | VARCHAR(30) | NOT NULL | `GUARDIAN` / `PERSON` / `SOCIAL_WORKER` / `SPECIAL_TEACHER` / `SUPPORT_WORKER` / `ADMIN` |
| `institution_id` | UUID | FK → `institutions.id`, NULL | 전문가 역할 소속 기관 |
| `assigned_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 할당 시각 |
| `expires_at` | TIMESTAMPTZ | NULL | 만료 시각 (기간제 기록자) |
| `granted_by` | UUID | FK → `users.id` | 승인자 |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |

---

### TABLE: `institutions` — 기관 정보

| 용도 | 복지관·특수학교·자립지원센터 등 지원 기관 관리 |
|------|------|
| **PK** | `id` (UUID) |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `name` | VARCHAR(200) | NOT NULL | 기관명 |
| `code` | VARCHAR(50) | UNIQUE, NOT NULL | 기관 인증 코드 |
| `type` | VARCHAR(50) | NOT NULL | `welfare_center` / `special_school` / `自立_center` / `job_rehab` / `other` |
| `phone` | VARCHAR(30) | NULL | 연락처 |
| `address` | VARCHAR(500) | NULL | 주소 |
| `status` | VARCHAR(20) | DEFAULT 'active' | `active` / `inactive` / `suspended` |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |
| `updated_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 수정 시각 |
| `deleted_at` | TIMESTAMPTZ | NULL | 소프트 딜리트 |

---

### TABLE: `party_profiles` — 당사자 프로파일

| 용도 | 발달장애인 당사자의 생애전주기 핵심 정보. 생애주기 자동 계산의 기반 |
|------|------|
| **PK** | `id` (UUID) |
| **FK** | `guardian_id` → `users.id` |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `guardian_id` | UUID | FK → `users.id`, NOT NULL | 보호자 계정 |
| `name` | VARCHAR(100) | NOT NULL | 당사자 이름 |
| `birth_date` | DATE | NOT NULL | 생년월일 (생애주기 계산 기준) |
| `gender` | VARCHAR(10) | NULL | `male` / `female` / `other` |
| `disability_type` | VARCHAR(100) | NULL | 장애 유형 (지체/뇌병변/정신/자폐/발달/청각/시각/지적 등) |
| `disability_grade` | VARCHAR(10) | NULL | 장애 등급 (1~4급) |
| `needs_support_level` | VARCHAR(20) | NULL | 지원필요등급 |
| `avatar_url` | TEXT | NULL | 아바타 이미지存储 경로 |
| `notes` | TEXT | NULL | 메모 |
| `status` | VARCHAR(20) | DEFAULT 'active' | `active` / `transition_planned` / `transition_in_progress` / `transition_complete` / `inactive` |
| `lifecycle_stage` | VARCHAR(30) | NOT NULL | **calc**: `infant` / `early_childhood` / `adolescent` / `young_adult` / `middle_adult` / `older_adult` |
| `transition_state` | VARCHAR(30) | DEFAULT 'NEW_BORN' | 권한 이양 상태 Machine ( §6.1 ) |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |
| `updated_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 수정 시각 |
| `deleted_at` | TIMESTAMPTZ | NULL | 소프트 딜리트 |

---

### TABLE: `invitations` — 기록자 초대

| 용도 | 이메일 기반 기록자 초대. 역할·카테고리·기간·유효기간 지정 |
|------|------|
| **PK** | `id` (UUID) |
| **FK** | `sender_id` → `users.id`, `recipient_user_id` → `users.id` |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `sender_id` | UUID | FK → `users.id`, NOT NULL | 초대자 |
| `party_id` | UUID | FK → `party_profiles.id`, NOT NULL | 초대 대상 당사자 |
| `recipient_email` | VARCHAR(255) | NOT NULL | 초대Recipient 이메일 |
| `role_type` | VARCHAR(30) | NOT NULL | `SOCIAL_WORKER` / `SPECIAL_TEACHER` / `SUPPORT_WORKER` |
| `invitation_type` | VARCHAR(30) | NOT NULL | `collaborator` / `reviewer` / `viewer` |
| `category_filter` | VARCHAR(100)[] | NULL | 접근 허용 카테고리 배열 (NULL=all) |
| `period_start` | DATE | NULL | 기간 시작 |
| `period_end` | DATE | NULL | 기간 종료 |
| `token` | UUID | UNIQUE, NOT NULL | 초대 토큰 (7일 유효) |
| `status` | VARCHAR(20) | DEFAULT 'pending' | `pending` / `accepted` / `expired` / `revoked` |
| `accepted_at` | TIMESTAMPTZ | NULL | 수락 시각 |
| `expires_at` | TIMESTAMPTZ | NOT NULL | 만료 시각 (생성 + 7일) |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |

---

### TABLE: `templates` — 기록 템플릿 정의

| 용도 | 생애주기 × 카테고리 기반 템플릿 구조 정의. 동적 폼 렌더링의 schema |
|------|------|
| **PK** | `id` (UUID) |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `name` | VARCHAR(200) | NOT NULL | 템플릿명 (예: "IEP 목표설정", "건강검진") |
| `description` | TEXT | NULL | 템플릿 설명 |
| `category` | VARCHAR(30) | NOT NULL | `health` / `education` / `daily_life` / `service_linkage` / `self_expression` |
| `life_stage` | VARCHAR(30) | NOT NULL | `infant` / `early_childhood` / `adolescent` / `young_adult` / `middle_adult` / `older_adult` |
| `field_schema` | JSONB | NOT NULL | 폼 필드 정의 ( §8 참조 ) |
| `editable_roles` | VARCHAR(30)[] | NOT NULL | 작성 가능 역할 배열 |
| `visible_roles` | VARCHAR(30)[] | NOT NULL | 열람 가능 역할 배열 |
| `estimated_time_min` | INT | DEFAULT 10 | 예상 입력 시간 (분) |
| `active` | BOOLEAN | DEFAULT true | 활성화 여부 |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |
| `updated_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 수정 시각 |

**template field_schema 구조 예시:**
```json
{
  "fields": [
    {"key": "name", "type": "text", "label": "환자명", "required": true, "visible_to": ["SOCIAL_WORKER","GUARDIAN"]},
    {"key": "date", "type": "date", "label": "진료일자", "required": true},
    {"key": "diagnosis", "type": "select", "label": "진단", "options": ["感冒","발진","중이염"], "required": false},
    {"key": "notes", "type": "textarea", "label": "의사 소견", "required": false, "max_length": 500},
    {"key": "attachments", "type": "file", "label": "첨부파일", "max_count": 10, "allowed_types": ["pdf","jpg","png"]},
    {"key": "pain_level", "type": "scale", "label": "통증 정도", "min": 0, "max": 10, "unit": "점"}
  ]
}
```

---

### TABLE: `records` — 기록본문

| 용도 | 플랫폼 핵심 데이터. 템플릿 기반 동적 형태로 작성된 모든 기록 |
|------|------|
| **PK** | `id` (UUID) |
| **FK** | `party_id` → `party_profiles.id`, `template_id` → `templates.id`, `author_id` → `users.id`, `parent_id` → `records.id` (수정 계보) |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `party_id` | UUID | FK → `party_profiles.id`, NOT NULL | 기록 대상 당사자 |
| `template_id` | UUID | FK → `templates.id`, NOT NULL | 사용 템플릿 |
| `category` | VARCHAR(30) | NOT NULL | 카테고리 (template과 동일) |
| `life_stage` | VARCHAR(30) | NOT NULL | 생애주기 (template과 동일) |
| `content_type` | VARCHAR(30) | NOT NULL | `standard` / `daily_log` / `iep` / `health` / `self_entry` |
| `status` | VARCHAR(20) | DEFAULT 'DRAFT' | `DRAFT` / `SUBMITTED` / `REVISED` / `ARCHIVED` / `SOFT_DELETE` / `PERMANENT_DELETE` |
| `author_id` | UUID | FK → `users.id`, NOT NULL | 작성자 |
| `visibility` | VARCHAR(20) | DEFAULT 'private' | `private` / `restricted` / `shared` |
| `parent_id` | UUID | FK → `records.id`, NULL = 최초버전 | 수정 계보 (parent가 있으면 수정본) |
| `title` | VARCHAR(500) | NULL | 기록 제목 |
| `content_data` | JSONB | NOT NULL | 템플릿 필드별 값 ( §8 참조 ) |
| `metadata` | JSONB | DEFAULT '{}' | 추가 메타데이터 |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |
| `updated_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 수정 시각 |
| `archived_at` | TIMESTAMPTZ | NULL | 아카이브 시각 |
| `deleted_at` | TIMESTAMPTZ | NULL | 소프트 딜리트 |

**content_data 구조 예시:**
```json
{
  "name": "김사랑",
  "date": "2026-03-15",
  "diagnosis": "발진",
  "notes": "손과 얼굴에 발진 관찰",
  "pain_level": 3,
  "attachments": ["/uploads/abc123.pdf"],
  "mood": "happy",
  "activities": ["밥 먹기", "친구 만나기"]
}
```

---

### TABLE: `attachments` — 파일 첨부

| 용도 | 기록에 첨부된 PDF·이미지·DOCX 파일 정보 |
|------|------|
| **PK** | `id` (UUID) |
| **FK** | `record_id` → `records.id` |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `record_id` | UUID | FK → `records.id`, NOT NULL | 소속 기록 |
| `file_name` | VARCHAR(500) | NOT NULL | 원본 파일명 |
| `storage_path` | TEXT | NOT NULL | 물리 저장 경로 (S3 등) |
| `file_size` | BIGINT | NOT NULL | 바이트 단위 크기 (max 20MB) |
| `mime_type` | VARCHAR(100) | NOT NULL | MIME 타입 |
| `thumbnail_path` | TEXT | NULL | 썸네일 경로 |
| `exif_removed` | BOOLEAN | DEFAULT true | EXIF 제거 여부 |
| `virus_scanned` | BOOLEAN | DEFAULT false | ClamAV 검사 여부 |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |

---

### TABLE: `record_versions` — 기록 수정 이력

| 용도 | 법적 분쟁 대비 기록 수정 전후 추적 (auditing) |
|------|------|
| **PK** | `id` (UUID) |
| **FK** | `record_id` → `records.id`, `author_id` → `users.id` |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `record_id` | UUID | FK → `records.id`, NOT NULL | 대상 기록 |
| `version` | INT | NOT NULL | 버전 번호 (1부터 증분) |
| `content_snapshot` | JSONB | NOT NULL | 해당 버전의 content_data 전체 스냅샷 |
| `changes` | JSONB | NOT NULL | `{field: {old: X, new: Y}}` 형태 변경 사항 |
| `reason` | TEXT | NULL | 수정 사유 |
| `author_id` | UUID | FK → `users.id`, NOT NULL | 수정자 |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |

---

### TABLE: `record_tags` — 기록 태그

| 용도 | 기록의 비정형 분류 (P1 기능) |
|------|------|
| **PK** | `id` (UUID) |
| **FK** | `record_id` → `records.id` |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `record_id` | UUID | FK → `records.id`, NOT NULL | 소속 기록 |
| `tag_name` | VARCHAR(100) | NOT NULL | 태그명 |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |

---

### TABLE: `service_linkages` — 서비스 연계 정보

| 용도 | 당사자가 이용하는 복지 서비스 기록 (직업재활·활동지원·요양 등) |
|------|------|
| **PK** | `id` (UUID) |
| **FK** | `party_id` → `party_profiles.id` |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `party_id` | UUID | FK → `party_profiles.id`, NOT NULL | 당사자 |
| `service_name` | VARCHAR(200) | NOT NULL | 서비스명 |
| `provider_name` | VARCHAR(200) | NOT NULL | 제공 기관명 |
| `provider_id` | UUID | FK → `institutions.id`, NULL | 제공 기관 |
| `start_date` | DATE | NOT NULL | 시작일 |
| `end_date` | DATE | NULL | 종료일 |
| `notes` | JSONB | DEFAULT '{}' | 서비스 상세 메모 (field key-value) |
| `status` | VARCHAR(20) | DEFAULT 'active' | `active` / `completed` / `suspended` / `cancelled` |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |
| `updated_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 수정 시각 |

---

### TABLE: `permission_logs` — 권한 변경 로그

| 용도 | 모든 권한 변경 이벤트 영구 보존. 법적 감사 요구 대응 |
|------|------|
| **PK** | `id` (UUID) |

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| `id` | UUID | PK | 고유 ID |
| `party_id` | UUID | FK → `party_profiles.id`, NOT NULL | 영향 받은 당사자 |
| `actor_id` | UUID | FK → `users.id`, NOT NULL | 권한 변경 수행자 |
| `action` | VARCHAR(50) | NOT NULL | `INVITE` / `ACCEPT` / `REVOKE` / `MODIFY` / `TRANSFER_START` / `TRANSFER_COMPLETE` / `TRANSFER_REJECTED` / `LOGIN` / `PDF_VIEW` / `PDF_DOWNLOAD` |
| `target_type` | VARCHAR(30) | NOT NULL | `invitation` / `permission` / `record` / `profile` |
| `target_id` | UUID | NOT NULL | 영향 대상 ID |
| `details` | JSONB | DEFAULT '{}' | 변경 전후 상세 |
| `ip_address` | INET | NULL | 로그인이거나 권한 변경 시 기록 |
| `user_agent` | TEXT | NULL | User-Agent |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | 생성 시각 |

---

## 4. 열(컬럼) 정의

### 4.1 공통 컬럼 convention

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `id` | UUID (PG UUID extension) | 모든 테이블의 PK. `gen_random_uuid()` 기본값 |
| `created_at` | TIMESTAMPTZ | 레코드 생성 시각. `DEFAULT now()` |
| `updated_at` | TIMESTAMPTZ | 레코드 수정 시각. `DEFAULT now()` + UPDATE trigger |
| `deleted_at` | TIMESTAMPTZ | 소프트 딜리트. NULL = 활성 |

### 4.2 역할 Enum 전체 목록

| Enum 값 | Korean | 설명 |
|---------|--------|------|
| `GUARDIAN` | 보호자 | 당사자의 법정 보호자 (부모 등) |
| `PERSON` | 당사자 | 발달장애인 본인 (만 18세 이상) |
| `SOCIAL_WORKER` | 사회복지사 | 사례 관리자 |
| `SPECIAL_TEACHER` | 특수교사 | 특수교육 기관 교사 |
| `SUPPORT_WORKER` | 활동지원사 | 일상 생활 지원 종사자 |
| `ADMIN` | 관리자 | 시스템 관리자 |

### 4.3 카테고리 Enum 전체 목록

| Enum 값 | Korean | 설명 |
|---------|--------|------|
| `health` | 건강·의료 | 건강검진, 병원기록, 발달검진 |
| `education` | 교육·발달 | IEP, 학업성취, 행동관찰 |
| `daily_life` | 일상생활 | 식사, 수면, 개인위생, 취미 |
| `service_linkage` | 서비스 연계 | 복지연계, 직업재활, 서비스계획 |
| `self_expression` | 자기표현 | 당사자 직접 기록, 선호·관심사 |

### 4.4 생애주기 Enum 전체 목록

| Enum 값 | Age | Korean | 주요 기록 |
|---------|-----|--------|---------|
| `infant` | 0–5 세 | 영유아 | 건강검진, 발달검진, 조기교육 |
| `early_childhood` | 6–11 세 | 유아·초등 | IEP, 생활기록, 학업성취 |
| `adolescent` | 12–17 세 | 청소년 | 진로상담, 사회적기술, 자립준비 |
| `young_adult` | 18–29 세 | 청년 | 직업훈련, 자립지원, 사회참여 |
| `middle_adult` | 30–59 세 | 성인 | 직업재활, 지역사회활동, 가정치료 |
| `older_adult` | 60세+ | 노년 | 건강관리, 돌봄서비스, 여가·문화 |

### 4.5 기록 상태 Enum

| Enum 값 | Korean | 설명 | 전이 가능 상태 |
|---------|--------|------|-------------|
| `DRAFT` | 임시저장 | 작성 중, 미 확정 | `SUBMITTED` |
| `SUBMITTED` | 확정저장 | 확정된 기록 | `REVISED`, `ARCHIVED` |
| `REVISED` | 수정됨 | 수정된 기록 (이력 생성) | `ARCHIVED` |
| `ARCHIVED` | 보관 | 삭제 불가 보관 상태 | `SOFT_DELETE` |
| `SOFT_DELETE` | 삭제됨 | 30일 내 복구 가능 | `PERMANENT_DELETE` |
| `PERMANENT_DELETE` | 영구삭제 | 되돌릴 수 없음 | — |

### 4.6 공개범위 Enum

| Enum 값 | Korean | 설명 |
|---------|--------|------|
| `private` | 나만보기 | 작성자·보호자만 열람 |
| `restricted` | 제한공개 | 초대 받은 기록자만 열람 |
| `shared` | 공유 | 모든 기록자와 당사자 열람 |

### 4.7 이양 상태 Enum (Permission Transfer)

| Enum 값 | 설명 | 전이 |
|---------|------|------|
| `NEW_BORN` | 등록 완료 | `TRANSITION_PLANNED` (D-90) |
| `TRANSITION_PLANNED` | 이양 준비 | `TRANSITION_REMINDER` (D-30) |
| `TRANSITION_REMINDER` | 재알림 | `TRANSITION_NOTIFIED` (D-7) |
| `TRANSITION_NOTIFIED` | 알림 완료 | `TRANSITION_IN_PROGRESS` (당사자 시작 버튼) |
| `TRANSITION_IN_PROGRESS` | 이양 진행 중 | `TRANSITION_VERIFIED` (전자서명) |
| `TRANSITION_VERIFIED` | 서명 완료 | `TRANSITION_AUTHENTICATED` (PASS 인증) |
| `TRANSITION_AUTHENTICATED` | 인증 완료 | `TRANSITION_COMPLETE` |
| `TRANSITION_COMPLETE` | 이양 완료 | — |
| `TRANSITION_REJECTED` | 이양 거부 | — |
| `GUARDIAN_OVERRIDE` | 법정후견 | — |

---

## 5. Enum / 코드 정의

### 5.1 PostgreSQL ENUM 타입 정의

```sql
-- 역할 Enum
DO $$ BEGIN
    CREATE TYPE role_type AS ENUM (
        'GUARDIAN', 'PERSON', 'SOCIAL_WORKER', 
        'SPECIAL_TEACHER', 'SUPPORT_WORKER', 'ADMIN'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- 카테고리 Enum
DO $$ BEGIN
    CREATE TYPE record_category AS ENUM (
        'health', 'education', 'daily_life', 
        'service_linkage', 'self_expression'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- 생애주기 Enum
DO $$ BEGIN
    CREATE TYPE lifecycle_stage AS ENUM (
        'infant', 'early_childhood', 'adolescent', 
        'young_adult', 'middle_adult', 'older_adult'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- 기록 상태 Enum
DO $$ BEGIN
    CREATE TYPE record_status AS ENUM (
        'DRAFT', 'SUBMITTED', 'REVISED', 
        'ARCHIVED', 'SOFT_DELETE', 'PERMANENT_DELETE'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- 공개범위 Enum
DO $$ BEGIN
    CREATE TYPE record_visibility AS ENUM (
        'private', 'restricted', 'shared'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- 이양 상태 Enum
DO $$ BEGIN
    CREATE TYPE transition_state AS ENUM (
        'NEW_BORN', 'TRANSITION_PLANNED', 'TRANSITION_REMINDER',
        'TRANSITION_NOTIFIED', 'TRANSITION_IN_PROGRESS',
        'TRANSITION_VERIFIED', 'TRANSITION_AUTHENTICATED',
        'TRANSITION_COMPLETE', 'TRANSITION_REJECTED', 'GUARDIAN_OVERRIDE'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- 초대 상태 Enum
DO $$ BEGIN
    CREATE TYPE invitation_status AS ENUM (
        'pending', 'accepted', 'expired', 'revoked'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;
```

---

## 6. 데이터 상태 전이도 (State Transitions)

### 6.1 기록 상태 전이도

```
  ┌───────┐   SUBMIT   ┌───────────┐   REVISE   ┌─────────┐   ARCHIVE   ┌──────────┐
  │ DRAFT ─────────────▶│ SUBMITTED ─────────────▶│ REVISED ─────────────▶│ ARCHIVED │
  └───────┘            └───────────┘            └─────────┘             └──────────┘
                                                  │                         │
                                                  ▼                         ▼
                                             ┌──────────┐          ┌───────────────┐
                                             │SOFT_DELETE│◀─────────│PERMANENT_DEL│
                                             └──────────┘   30일후   └───────────────┘
```

### 6.2 당사자 이양 상태 전이도

```
[NEW_BORN]
   │
   ▼ (D-90)
[TRANSITION_PLANNED]
   │
   ▼ (D-30)
[TRANSITION_REMINDER]
   │
   ▼ (D-7)
[TRANSITION_NOTIFIED]
   │
   ▼ (당사자 시작 버튼)
[TRANSITION_IN_PROGRESS]
   │
   ▼ (전자서명 완료)
[TRANSITION_VERIFIED]
   │
   ▼ (PASS 본인인증)
[TRANSITION_AUTHENTICATED]
   │
   ▼ (권한 적용)
[TRANSITION_COMPLETE] ── 보호자: 쓰기→열람전원, 당사자: 모든권한 부여
```

**예외 경로:**
- `TRANSITION_NOTIFIED` → `TRANSITION_REJECTED` (당사자 거부 시)
- `NEW_BORN` → `GUARDIAN_OVERRIDE` (법정후견인 등록 시)
- 모든 상태 → `TRANSITION_REJECTED` (보호자 거부 시)

---

## 7. 인덱스 정의

### 7.1 테이블별 인덱스

```sql
-- users
CREATE UNIQUE INDEX idx_users_email         ON users (email)        WHERE deleted_at IS NULL;
CREATE INDEX  idx_users_status              ON users (status)       WHERE deleted_at IS NULL;
CREATE INDEX  idx_users_last_login          ON users (last_login_at) DESC;

-- role_assignments
CREATE INDEX  idx_role_user                 ON role_assignments (user_id);
CREATE INDEX  idx_role_institution          ON role_assignments (institution_id);
CREATE INDEX  idx_role_role_type            ON role_assignments (role_type);
CREATE INDEX  idx_role_expires              ON role_assignments (expires_at) WHERE expires_at IS NOT NULL;

-- party_profiles
CREATE INDEX  idx_party_guardian            ON party_profiles (guardian_id);
CREATE INDEX  idx_party_birth_date          ON party_profiles (birth_date);
CREATE INDEX  idx_party_lifecycle_stage     ON party_profiles (lifecycle_stage);
CREATE INDEX  idx_party_status              ON party_profiles (status);
CREATE INDEX  idx_party_transition          ON party_profiles (transition_state) WHERE transition_state != 'NEW_BORN';

-- templates
CREATE INDEX  idx_template_category         ON templates (category);
CREATE INDEX  idx_template_life_stage       ON templates (life_stage);
CREATE INDEX  idx_template_active           ON templates (active) WHERE active = true;
CREATE INDEX  idx_template_category_stage   ON templates (category, life_stage);

-- records
CREATE INDEX  idx_record_party              ON records (party_id);
CREATE INDEX  idx_record_template           ON records (template_id);
CREATE INDEX  idx_record_category           ON records (category);
CREATE INDEX  idx_record_life_stage         ON records (life_stage);
CREATE INDEX  idx_record_status             ON records (status);
CREATE INDEX  idx_record_author             ON records (author_id);
CREATE INDEX  idx_record_visibility         ON records (visibility);
CREATE INDEX  idx_record_parent             ON records (parent_id) WHERE parent_id IS NOT NULL;
-- JSONB 검색 지원 (PRD §8.1)
CREATE INDEX  idx_record_content_gin        ON records USING GIN (content_data);
CREATE INDEX  idx_record_created            ON records (created_at) DESC;

-- attachments
CREATE INDEX  idx_attachment_record         ON attachments (record_id);
CREATE INDEX  idx_attachment_mime           ON attachments (mime_type);

-- record_versions
CREATE INDEX  idx_version_record            ON record_versions (record_id);
CREATE INDEX  idx_version_record_ver        ON record_versions (record_id, version DESC);

-- invitations
CREATE INDEX  idx_invitation_sender         ON invitations (sender_id);
CREATE INDEX  idx_invitation_party          ON invitations (party_id);
CREATE INDEX  idx_invitation_token          ON invitations (token);
CREATE INDEX  idx_invitation_status         ON invitations (status) WHERE status = 'pending';
CREATE INDEX  idx_invitation_expires        ON invitations (expires_at);

-- service_linkages
CREATE INDEX  idx_service_party             ON service_linkages (party_id);
CREATE INDEX  idx_service_status            ON service_linkages (status);
CREATE INDEX  idx_service_provider          ON service_linkages (provider_id);

-- permission_logs (대용량 로그 테이블 — 분할 고려)
CREATE INDEX  idx_permlog_party             ON permission_logs (party_id);
CREATE INDEX  idx_permlog_actor             ON permission_logs (actor_id);
CREATE INDEX  idx_permlog_action            ON permission_logs (action);
CREATE INDEX  idx_permlog_created           ON permission_logs (created_at) DESC;
```

---

## 8. JSONB 스키마 정의

### 8.1 `records.content_data` — 기록 필드값

템플릿의 `field_schema`에 따라 동적으로 구조화됨. 공통 필드:

```json
{
  "meta": {
    "template_id": "uuid",
    "template_name": "istring",
    "version": "integer",
    "filled_at": "ISO8601 timestamp"
  },
  "fields": {
    "<field_key>": "<field_value>",
    "...": "..."
  }
}
```

**field_type 별 value 형식:**

| type | value 형식 | 예시 |
|------|-----------|------|
| `text` | string | `"김사랑"` |
| `textarea` | string | `"집에서 조용히 지냄"` |
| `date` | `YYYY-MM-DD` | `"2026-06-01"` |
| `date_range` | `{"start":"YYYY-MM-DD", "end":"YYYY-MM-DD"}` | `{"start":"2026-01-01", "end":"2026-03-31"}` |
| `select` | string (options 중 1개) | `"발진"` |
| `multiselect` | string[] (options 중 복수) | `["밥 먹기", "친구 만나기"]` |
| `scale` | number (min~max) | `5` |
| `file` | string[] (storage_path 배열) | `["/uploads/abc.pdf"]` |
| `checkbox` | boolean | `true` |
| `table` | `{ headers: string[], rows: string[][] }` | `{"headers":[" 항목","결과"], "rows":[["체중","45kg"],["시력","0.8"]]}` |

### 8.2 `records.metadata` — 기록 메타

```json
{
  "is_public": boolean,
  "tags": string[],
  "pinned": boolean,
  "custom_fields": object
}
```

### 8.3 `invitations.category_filter` — 카테고리 제한 배열

```json
["health", "education", "self_expression"]  // null = 전체 허용
```

### 8.4 `service_linkages.notes` — 서비스 메모

```json
{
  "service_hours_per_week": 12,
  "special_notes": "주말 서비스 추가 요청 가능",
  "progress_notes": "3개월째 연속 이용 중"
}
```

---

## 9. 데이터 보존 및 삭제 정책

### 9.1 보존 기간

| 엔티티 | 보존 기간 | 삭제 정책 | 법적 근거 |
|--------|---------|---------|---------|
| `party_profiles` | 계정 탈퇴 후 **익명화** | `deleted_at` → 필드 익명화 (이름·생일 마스킹) | 개인정보보호법 |
| `records` | 명시적 삭제까지 **영구 보존** | `SOFT_DELETE` → 30일 후 `PERMANENT_DELETE` | 장애인권리보장법 |
| `record_versions` | 기록과 **동일 기간** | 영구 유지 (법적 분쟁 대비) | — |
| `attachments` | 기록과 **동일 기간** | 기록 삭제 시 함께 삭제 | — |
| `invitations` | 만료일에서 **30일 후** 삭제 | 자동 삭제 또는 수동 정리 | — |
| `permission_logs` | **무기한** 보존 | 변경 불가, 읽기 전용 | 감사 요구 대응 |
| `users` | 탈퇴 후 **30일** | 30일간 `deleted_at` 설정 후 실제 삭제 | 개인정보보호법 |

### 9.2 익명화 프로세스

```
party_profile 삭제 요청
  │
  ├── name → '익명'
  ├── birth_date → 'YYYY-XX-XX' (월·일 마스킹)
  ├── disability_type → NULL
  ├── disability_grade → NULL
  ├── avatar_url → NULL
  │
  └── records는 보존 (party_id는 익명화됨)
```

### 9.3 백업 전략 (PRD §8.2)

| 전략 | 빈도 | 보관 기간 | 목적 |
|------|------|---------|------|
| 전체 백업 | 일 1회 | 30일 | 기본 복구 |
| WAL 아카이브 | 시간당 | 7일 | Poin-in-Time 복구 |
| 스냅샷 | 마이그레이션 전 | — | 안전한 롤백 |

---

> **본 문서는 PRD v1.0, UX Design Spec v1.0, Workflow v1.0, UI Layer Architecture v1.0을 기준으로 작성되었습니다.**
> 
> **관리자**: 개발팀 · **검토 주기**: 매 Sprint 종료 시
