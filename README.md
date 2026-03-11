# bulk-svn-directory-helper

Small command-line helper for creating one or more SVN directory URLs safely and consistently.

This repository is meant for people who still operate Subversion repositories and want a cleaner way to create multiple remote directories without repeating `svn mkdir` commands manually.

## Why this can be useful

This helper is useful when you need to:

- create several SVN paths in one run
- standardize `svn mkdir` usage across repeated operations
- avoid unsafe shell-based command construction
- validate planned changes before running them
- create repository paths from a text file during release or migration work

## Real operational use cases

This is practical in situations like:

- creating `branches`, `tags`, or release folders across multiple SVN repositories
- preparing a standard directory structure for a new project
- creating several remote paths during deployment or migration prep
- reducing human error when the same SVN path creation task is repeated often

## What this helper does

The script:

- accepts SVN URLs directly from the command line
- can also read SVN URLs from a file
- validates URLs before execution
- uses `svn mkdir -p` safely without `shell=True`
- supports username/password or secure password prompt
- supports `--dry-run`
- prints per-URL results and a final summary

## Why this is better than a raw shell snippet

This version adds practical value:

- safer subprocess usage
- no command injection via shell interpolation
- reusable CLI options
- support for bulk URL creation from a file
- clearer failure output
- easier repeatability in real operations

## Requirements

- Python 3
- Subversion CLI (`svn`) installed and available in `PATH`

## Usage

Create a single SVN path:

```bash
python3 create_svn_url.py \
  --username myuser \
  --prompt-password \
  --message "Create release directory" \
  https://svn.example.com/project/releases/2026
```

Create multiple SVN paths in one command:

```bash
python3 create_svn_url.py \
  --username myuser \
  --prompt-password \
  --message "Create standard project layout" \
  https://svn.example.com/project/trunk/releases/2026 \
  https://svn.example.com/project/branches/hotfix-01 \
  https://svn.example.com/project/tags/v1.0.0
```

Dry-run:

```bash
python3 create_svn_url.py \
  --username myuser \
  --dry-run \
  https://svn.example.com/project/releases/2026
```

Read URLs from a file:

```bash
python3 create_svn_url.py \
  --username myuser \
  --prompt-password \
  --message "Create standard SVN layout" \
  --file urls.txt
```

Example `urls.txt`:

```text
https://svn.example.com/project/trunk/releases/2026
https://svn.example.com/project/branches/hotfix-01
https://svn.example.com/project/tags/v1.0.0
```

## Supported options

- `urls...`
- `--file`
- `--username`
- `--password`
- `--prompt-password`
- `--message`
- `--dry-run`
- `--non-interactive`

## Notes

- `--prompt-password` is safer than passing a password directly on the command line
- `--dry-run` is useful before batch operations
- the helper validates scheme and hostname, but it does not validate repository permissions in advance
- the actual directory creation is still performed by the local `svn` client

## Suggested positioning

This repository makes the most sense as:

- an SVN directory creation helper
- a bulk SVN path creation utility
- a small operations tool for teams still maintaining Subversion repositories

---

## Author

Built by **Mert Can Girgin**

**MSc | DevOps Engineer | Linux Administrator**

Guardian of the Linux realms. No outage shall pass.
