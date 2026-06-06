#!/usr/bin/env python3
"""
WBS → GitLab 연동 스크립트
wbs.json을 읽어 GitLab 프로젝트에 마일스톤과 이슈를 자동 생성합니다.

사용법:
  export GITLAB_URL=https://gitlab.com
  export GITLAB_TOKEN=your_personal_access_token
  export GITLAB_PROJECT_ID=123
  python scripts/create_gitlab_wbs.py --dry-run
  python scripts/create_gitlab_wbs.py
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

WBS_FILE = Path(__file__).resolve().parent.parent / "wbs.json"
GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID", "")


def get_headers():
    return {"PRIVATE-TOKEN": GITLAB_TOKEN, "Content-Type": "application/json"}


def api_get(path: str):
    url = f"{GITLAB_URL}/api/v4/{path}"
    resp = requests.get(url, headers=get_headers(), timeout=30)
    if resp.status_code not in (200, 201):
        print(f"  ✗ GET {path} → {resp.status_code}: {resp.text[:200]}")
    return resp


def api_post(path: str, data: dict):
    url = f"{GITLAB_URL}/api/v4/{path}"
    resp = requests.post(url, headers=get_headers(), json=data, timeout=30)
    if resp.status_code not in (200, 201):
        print(f"  ✗ POST {path} → {resp.status_code}: {resp.text[:200]}")
    return resp


def resolve_labels(label_names: list) -> list:
    if not label_names:
        return []
    resp = api_get(f"projects/{GITLAB_PROJECT_ID}/labels")
    if resp.status_code != 200:
        return label_names
    all_labels = resp.json()
    label_map = {l["name"]: l["id"] for l in all_labels}
    resolved = []
    for name in label_names:
        if name in label_map:
            resolved.append(label_map[name])
        else:
            label_data = {"name": name, "description": f"Auto-created from WBS: {name}", "priority": 5}
            create_resp = api_post(f"projects/{GITLAB_PROJECT_ID}/labels", label_data)
            if create_resp.status_code == 201:
                new_label = create_resp.json()
                resolved.append(new_label["id"])
                print(f"  ✓ Created label '{name}' (ID: {new_label['id']})")
            else:
                resolved.append(name)
    return resolved


def ensure_existing_milestone(milestone_id: str, title: str):
    resp = api_get(f"projects/{GITLAB_PROJECT_ID}/milestones?search={title}")
    if resp.status_code == 200:
        for m in resp.json():
            if m["title"] == title:
                print(f"  ✓ Found existing milestone: {title} (ID: {m['id']})")
                return m["id"]
    return None


def load_wbs() -> dict:
    if not WBS_FILE.exists():
        print(f"ERROR: WBS file not found: {WBS_FILE}")
        sys.exit(1)
    with open(WBS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_date(d: str) -> str:
    if not d:
        return None
    d = d.strip().replace("/", "-")
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(d, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return d


def main():
    parser = argparse.ArgumentParser(description="WBS JSON → GitLab Milestones & Issues 연동")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-milestones", action="store_true")
    parser.add_argument("--skip-issues-only", action="store_true")
    parser.add_argument("--milestone", type=str, default=None)
    parser.add_argument("--wbs", type=str, default=None)
    parser.add_argument("--batch-size", type=int, default=1)
    args = parser.parse_args()

    if args.wbs:
        global WBS_FILE
        WBS_FILE = Path(args.wbs).resolve()

    if not GITLAB_TOKEN:
        print("ERROR: GITLAB_TOKEN 환경변수가 설정되지 않았습니다.")
        sys.exit(1)
    if not GITLAB_PROJECT_ID:
        print("ERROR: GITLAB_PROJECT_ID 환경변수가 설정되지 않았습니다.")
        sys.exit(1)
    if not GITLAB_URL:
        print("ERROR: GITLAB_URL 환경변수가 설정되지 않았습니다.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  LifeLog WBS → GitLab 연동 스크립트")
    print(f"{'='*60}")
    print(f"  GitLab URL     : {GITLAB_URL}")
    print(f"  Project ID     : {GITLAB_PROJECT_ID}")
    print(f"  WBS File       : {WBS_FILE}")
    print(f"  Dry Run        : {'Yes ✓' if args.dry_run else 'No ✗'}")
    print(f"{'='*60}\n")

    wbs_data = load_wbs()
    milestones = wbs_data.get("milestones", [])
    wbs_levels = wbs_data.get("wbs_levels", {})

    if args.milestone:
        milestones = [m for m in milestones if m["id"] == args.milestone]

    milestone_map = {}

    if not args.skip_milestones and not args.skip_issues_only:
        print("📌 Step 1: 마일스톤 생성")
        print("-" * 40)
        for m in milestones:
            m_id = m["id"]
            m_title = m["gitlab_title"]
            m_start = parse_date(m["start_date"])
            m_due = parse_date(m["due_date"])
            m_desc = m.get("description", "")
            print(f"\n마일스톤 [{m_id}]: {m_title} ({m_start} ~ {m_due})")

            existing = ensure_existing_milestone(m_id, m_title)
            if existing:
                milestone_map[m_id] = existing
                continue

            if args.dry_run:
                print(f"  [DRY RUN] 마일스톤 생성 예정: {m_title}")
                milestone_map[m_id] = f"dry-run-{m_id}"
                continue

            m_data = {
                "title": m_title,
                "description": m_desc,
                "due_date": m_due,
                "start_date": m_start
            }
            resp = api_post(f"projects/{GITLAB_PROJECT_ID}/milestones", m_data)
            if resp.status_code in (200, 201):
                new_m = resp.json()
                milestone_map[m_id] = new_m["id"]
                print(f"  ✓ Created milestone (ID: {new_m['id']})")
            else:
                print(f"  ✗ Failed to create milestone")
            time.sleep(args.batch_size)
        print(f"\n  → {len(milestone_map)} 개 마일스톤 처리 완료\n")
    else:
        print("📌 Step 1: 기존 마일스톤 검색")
        print("-" * 40)
        for m in milestones:
            m_id = m["id"]
            existing = ensure_existing_milestone(m_id, m["gitlab_title"])
            if existing:
                milestone_map[m_id] = existing
        print(f"  → {len(milestone_map)} 개 기존 마일스톤 연결\n")

    all_wbs_labels = set()
    for item in wbs_levels.values():
        for label in item.get("labels", []):
            all_wbs_labels.add(label)
    print(f"🏷️ Step 2: 라벨 확인 ({len(all_wbs_labels)}개)")
    resolve_labels(sorted(all_wbs_labels))

    print("\n📋 Step 3: 이슈 생성")
    print("-" * 40)

    issue_map = {}
    items_by_level = {}
    for wbs_id, item in wbs_levels.items():
        level = item.get("level", 0)
        if level not in items_by_level:
            items_by_level[level] = []
        items_by_level[level].append((wbs_id, item))

    for level in sorted(items_by_level.keys()):
        items = items_by_level[level]
        print(f"\n  Level {level}: {len(items)} items")
        for wbs_id, item in items:
            if wbs_id == "WP0":
                print(f"  ⏭  [SKIP] {wbs_id} (project container)")
                continue

            milestone_id = item.get("milestone")
            milestone_gitlab_id = milestone_map.get(milestone_id) if milestone_id else None
            parent_wbs_id = item.get("parent_id")
            parent_issue_iid = issue_map.get(parent_wbs_id) if parent_wbs_id else None

            title = item.get("name", wbs_id)
            desc = item.get("desc", "")
            desc_full = desc
            if item.get("estimated_weeks"):
                desc_full += f"\n\n**추정 기간**: {item['estimated_weeks']}주"
            if item.get("deliverable"):
                desc_full += f"\n\n**산출물**: {item['deliverable']}"
            if item.get("start_date") and item.get("end_date"):
                desc_full += f"\n\n**기간**: {item['start_date']} ~ {item['end_date']}"
            if item.get("assignees"):
                desc_full += f"\n\n**담당자**: {', '.join(item['assignees'])}"
            if item.get("ref_docs"):
                desc_full += f"\n\n**연계 문서**: {', '.join(item['ref_docs'])}"
            desc_full += f"\n\n---\n_WBS ID: {wbs_id}_"

            priority = item.get("priority", "normal")
            weight_map = {"critical": 8, "high": 5, "low": 1}

            phase_labels = {"requirement", "design", "dev-env", "development", "testing", "poc", "improvement"}
            role_labels = [l for l in item.get("labels", []) if l not in phase_labels]
            type_label = "subtask" if "subtask" in str(item.get("labels", [])) else "task"
            all_label_names = role_labels + [type_label]

            due_date = item.get("end_date")
            print(f"\n  [{wbs_id}] {title}")
            print(f"    Milestone: {milestone_id} | Parent: {parent_wbs_id} | Priority: {priority}")

            if args.dry_run:
                print(f"    [DRY RUN] 이슈 생성 예정")
                issue_map[wbs_id] = f"dry-run-{wbs_id}"
                continue

            issue_data = {
                "title": title,
                "description": desc_full,
                "label_names": all_label_names,
                "due_date": due_date,
            }
            if milestone_gitlab_id:
                issue_data["milestone_id"] = milestone_gitlab_id
            if parent_issue_iid:
                issue_data["parent_issue_iid"] = parent_issue_iid
            if priority in weight_map:
                issue_data["weight"] = weight_map[priority]

            resp = api_post(f"projects/{GITLAB_PROJECT_ID}/issues", issue_data)
            if resp.status_code in (200, 201):
                new_issue = resp.json()
                issue_map[wbs_id] = new_issue["iid"]
                print(f"  ✓ Created issue (IID: {new_issue['iid']})")
                if new_issue.get("web_url"):
                    print(f"    URL: {new_issue['web_url']}")
            else:
                print(f"  ✗ Failed to create issue: {resp.text[:200]}")
             time.sleep(args.batch_size)

    print(f"\n{'='*60}")
    print(f"  완료 요약")
    print(f"{'='*60}")
    print(f"  마일스톤: {len(milestone_map)} 개 처리")
    print(f"  이슈: {len(issue_map)} 개 처리")
    print(f"{'='*60}")

    if args.dry_run:
        print(f"\n⚠  Dry Run — 실제 생성되지 않았습니다.")
        print(f"  실제 생성하려면 --dry-run 없이 실행하세요.")
        print(f"\n  생성 예정 이슈:")
        for wbs_id, issue_id in issue_map.items():
            if issue_id.startswith("dry-run"):
                item = wbs_levels.get(wbs_id, {})
                print(f"    {wbs_id}: {item.get('name', 'Unknown')}")
    else:
        print(f"\n✅ GitLab에 마일스톤과 이슈가 생성되었습니다.")

    print(f"\n{'WBS ID':<12} {'Parent':<12} {'Milestone':<12} {'Issue IID':<12} {'Title'}")
    print("-" * 80)
    for wbs_id, item in wbs_levels.items():
        if wbs_id == "WP0":
            continue
        parent = item.get("parent_id", "")
        milestone = item.get("milestone", "")
        issue_iid = issue_map.get(wbs_id, "")
        title = item.get("name", "Unknown")[:40]
        print(f"  {wbs_id:<10} {parent:<10} {milestone:<10} {str(issue_iid):<10} {title}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

