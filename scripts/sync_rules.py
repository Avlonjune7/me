"""Publish local me and global Codex rules, then verify CC Switch and GitHub."""
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
import check

ME = Path(__file__).resolve().parents[1]
GLOBAL = Path.home() / ".codex/AGENTS.md"
CC = Path(os.environ.get("CC_SWITCH_HOME", "D:/DATA/cc switch"))
STATE = Path.home() / ".agents/rules-sync-state.json"
INITIAL = {"me": "8fb15cdfe277bfc91197c0119fde79ce51f5e1cb",
           "codex-global-agent": "51bf910739606183f3ed082dccb43c04a11ce0f1"}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def normalized(data):
    return None if data is None else check.normalize(data)


def guard(old, current, wanted, label):
    for name in current.keys() | old.keys() | wanted.keys():
        actual = normalized(current.get(name))
        if actual not in (normalized(old.get(name)), normalized(wanted.get(name))):
            raise ValueError(f"Independent edit in {label}: {name}")


def apply_files(root, current, wanted):
    for name in sorted(current.keys() | wanted.keys()):
        path = root / name
        if name not in wanted:
            path.unlink()
        elif normalized(current.get(name)) != normalized(wanted[name]):
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
                tmp.write(wanted[name])
            os.replace(tmp.name, path)


def sync(work):
    baseline = json.loads(STATE.read_text()) if STATE.exists() else INITIAL
    skill = check.inventory(ME)
    description = check.metadata(skill)["description"]
    errors = check.check_links(ME, skill) + check.check_routing(skill)
    if errors:
        raise ValueError("\n".join(errors))
    rules = {"AGENTS.md": GLOBAL.read_bytes()}
    if not rules["AGENTS.md"].strip():
        raise ValueError("Empty global instructions")
    heads = {}
    old = {}
    for name, wanted in (("me", skill), ("codex-global-agent", rules)):
        repo = work / name
        git(work, "clone", "-q", "--branch", "main",
            f"https://github.com/Avlonjune7/{name}.git", str(repo))
        _, before = check.git_inventory(repo, baseline[name])
        _, current = check.git_inventory(repo, "HEAD")
        if name != "me":
            before = {"AGENTS.md": before["AGENTS.md"]}
            current = {"AGENTS.md": current["AGENTS.md"]}
        old[name] = before
        guard(before, current, wanted, name)
        apply_files(repo, current, wanted)
        git(repo, "add", "-A")
        if git(repo, "diff", "--cached", "--name-only").strip():
            git(repo, "-c", "user.name=Rules Sync", "-c", "user.email=rules-sync@localhost", "commit", "-qm", "Update personal Codex rules")
        heads[name] = git(repo, "rev-parse", "HEAD").decode().strip()

    cc_skill = CC / "skills/me"
    with sqlite3.connect((CC / "cc-switch.db").resolve().as_uri() + "?mode=rw", uri=True) as db:
        db.execute("BEGIN IMMEDIATE")
        rows = db.execute("SELECT id,content FROM prompts WHERE app_type='codex' AND enabled=1 AND name='agent'").fetchall()
        if len(rows) != 1 or not db.execute("SELECT 1 FROM skills WHERE id='local:me'").fetchone():
            raise ValueError("Expected CC Switch skill or enabled agent prompt missing")
        prompt_id, prompt = rows[0]
        guard(old["codex-global-agent"], {"AGENTS.md": prompt.encode()}, rules, "CC prompt")
        cc_files = check.inventory(cc_skill)
        guard(old["me"], cc_files, skill, "CC skill")
        apply_files(cc_skill, cc_files, skill)
        managed = check.inventory(cc_skill)
        if check.compare(skill, managed, "CC skill"):
            raise ValueError("CC skill verification failed")
        digest = check.content_hash(managed)
        db.execute("UPDATE skills SET description=?,content_hash=? WHERE id='local:me' AND (description IS NOT ? OR content_hash IS NOT ?)",
                   (description, digest, description, digest))
        content = rules["AGENTS.md"].decode("utf-8")
        if normalized(prompt.encode()) != normalized(rules["AGENTS.md"]):
            db.execute("UPDATE prompts SET content=?,updated_at=? WHERE id=?", (content, int(time.time()), prompt_id))
        if db.execute("SELECT description,content_hash FROM skills WHERE id='local:me'").fetchone() != (description, digest):
            raise ValueError("CC skill metadata verification failed")
        saved = db.execute("SELECT content FROM prompts WHERE id=?", (prompt_id,)).fetchone()[0]
        if normalized(saved.encode()) != normalized(rules["AGENTS.md"]):
            raise ValueError("CC prompt verification failed")

    for name, head in heads.items():
        repo = work / name
        if git(repo, "rev-parse", "origin/main").decode().strip() != head:
            git(repo, "push", "origin", "HEAD:refs/heads/main")
        actual = git(repo, "ls-remote", "origin", "refs/heads/main").split()[0].decode()
        if actual != head:
            raise ValueError(f"Remote changed during sync: {name}")
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(heads), encoding="utf-8")
    tmp.replace(STATE)
    print("Verified both GitHub main branches, CC Switch skill and active Codex prompt.")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
        sync(Path(directory))
