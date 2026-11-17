"""Read-only checks for this skill. Requires Python 3.10+, standard library only."""

import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
from urllib.parse import unquote, urlsplit


def inventory(root):
    if not root.is_dir():
        raise ValueError(f'Missing directory: {root}')
    result = {}
    for path in root.rglob('*'):
        parts = path.relative_to(root).parts
        if any(part.startswith('.') or part == '__pycache__' for part in parts):
            continue
        if path.is_symlink():
            raise ValueError(f'Unsupported symlink: {path}')
        if path.is_file() and path.suffix != '.pyc':
            result[path.relative_to(root).as_posix()] = path.read_bytes()
    return result


def normalize(data):
    try:
        return data.decode('utf-8').replace('\r\n', '\n').encode('utf-8')
    except UnicodeDecodeError:
        return data


def compare(expected, actual, label):
    errors = []
    for name in sorted(expected.keys() | actual.keys()):
        if name not in actual:
            errors.append(f'{label}: missing {name}')
        elif name not in expected:
            errors.append(f'{label}: extra {name}')
        elif normalize(expected[name]) != normalize(actual[name]):
            errors.append(f'{label}: differs {name}')
    return errors


def content_hash(files):
    digest = hashlib.sha256()
    for name, data in sorted(files.items()):
        digest.update(name.encode('utf-8') + b'\0' + data + b'\0')
    return digest.hexdigest()


def metadata(files):
    text = normalize(files['SKILL.md']).decode('utf-8')
    match = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        raise ValueError('SKILL.md: missing frontmatter')
    fields = {}
    for line in match[1].splitlines():
        key, separator, value = line.partition(':')
        if not separator or key not in ('name', 'description') or key in fields:
            raise ValueError('SKILL.md: unsupported or duplicate frontmatter field')
        value = value.strip()
        if value.startswith('"'):
            value = json.loads(value)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'SKILL.md: empty {key}')
        fields[key] = value
    if fields.get('name') != 'me' or not fields.get('description'):
        raise ValueError('SKILL.md: expected name me and nonempty description')
    return fields


def check_links(root, files):
    errors = []
    for name, data in files.items():
        if not name.endswith('.md'):
            continue
        text = data.decode('utf-8')
        text = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
        for target in re.findall(r'\]\(([^\s)]+)\)', text):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            resolved = (root / name).parent.joinpath(unquote(url.path)).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                errors.append(f'{name}: missing or external local target {target}')
    return errors


SKILL_BUDGET = 4000  # bytes; SKILL.md is loaded whenever me triggers


def check_routing(files):
    errors = []
    skill = files['SKILL.md'].decode('utf-8')
    for name in sorted(files):
        if name.startswith('references/') and name.endswith('.md') and f'({name})' not in skill:
            errors.append(f'SKILL.md: {name} is not routed')
    if len(files['SKILL.md']) > SKILL_BUDGET:
        errors.append(f'SKILL.md: {len(files["SKILL.md"])} bytes exceeds budget {SKILL_BUDGET}')
    return errors


def git_inventory(root, ref):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)
    commit = git('rev-parse', '--verify', '--end-of-options', ref + '^{commit}').decode().strip()
    entries = git('ls-tree', '-rz', commit).split(b'\0')
    files = {}
    for entry in filter(None, entries):
        info, name = entry.split(b'\t', 1)
        mode, kind, oid = info.split()
        if kind != b'blob' or mode == b'120000':
            raise ValueError('Git reference contains unsupported entry')
        path = name.decode('utf-8')
        if any(part.startswith('.') or part == '__pycache__' for part in path.split('/')) or path.endswith('.pyc'):
            continue
        files[path] = git('cat-file', 'blob', oid.decode())
    return commit, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--copy', type=Path, action='append', default=[])
    parser.add_argument('--cc-db', type=Path)
    parser.add_argument('--cc-skill-dir', type=Path)
    parser.add_argument('--cc-id', default='local:me')
    parser.add_argument('--git-ref')
    args = parser.parse_args()
    if bool(args.cc_db) != bool(args.cc_skill_dir):
        parser.error('--cc-db and --cc-skill-dir must be provided together')
    try:
        root = args.root.resolve()
        files = inventory(root)
        fields = metadata(files)
        errors = check_links(root, files) + check_routing(files)
        for directory in args.copy:
            errors.extend(compare(files, inventory(directory), str(directory)))
        if args.cc_db:
            managed = inventory(args.cc_skill_dir)
            errors.extend(compare(files, managed, 'CC skill'))
            with closing(sqlite3.connect(args.cc_db.resolve().as_uri() + '?mode=ro', uri=True)) as db:
                row = db.execute('SELECT description, content_hash FROM skills WHERE id=?', (args.cc_id,)).fetchone()
            if not row:
                errors.append('CC metadata: missing skill row')
            elif row != (fields['description'], content_hash(managed)):
                errors.append('CC metadata: description or content hash differs')
        if args.git_ref:
            commit, remote_files = git_inventory(root, args.git_ref)
            print(f'Git reference {commit} (local reference, no fetch)')
            errors.extend(compare(files, remote_files, 'Git reference'))
        if errors:
            print('\n'.join(errors))
            return 1
        print(f'OK: {len(files)} files, {sum(map(len, files.values()))} bytes; requested checks passed')
        return 0
    except (OSError, ValueError, KeyError, sqlite3.Error, subprocess.CalledProcessError) as error:
        print(f'ERROR: {type(error).__name__}: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
