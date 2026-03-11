import argparse
import getpass
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create one or more SVN directories safely from the command line."
    )
    parser.add_argument(
        "urls",
        nargs="*",
        help="SVN URLs to create with svn mkdir -p",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Text file containing one SVN URL per line.",
    )
    parser.add_argument(
        "--username",
        help="SVN username",
    )
    parser.add_argument(
        "--password",
        help="SVN password. Prefer --prompt-password if possible.",
    )
    parser.add_argument(
        "--prompt-password",
        action="store_true",
        help="Prompt securely for the SVN password.",
    )
    parser.add_argument(
        "--message",
        default="Create SVN directories",
        help="Commit message for svn mkdir. Default: 'Create SVN directories'",
    )
    parser.add_argument(
        "--parents",
        action="store_true",
        default=True,
        help="Create parent directories as needed (default behavior).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned commands without executing them.",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Pass --non-interactive to svn.",
    )
    args = parser.parse_args()

    if not args.urls and not args.file:
        parser.error("provide at least one URL or use --file")

    if args.password and args.prompt_password:
        parser.error("use either --password or --prompt-password, not both")

    return args


def load_urls(args):
    urls = list(args.urls)
    if args.file:
        if not args.file.exists():
            raise FileNotFoundError(f"URL file not found: {args.file}")
        file_urls = [
            line.strip()
            for line in args.file.read_text().splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        urls.extend(file_urls)

    # Preserve order while removing duplicates.
    return list(dict.fromkeys(urls))


def validate_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https", "svn", "svn+ssh"}:
        raise ValueError(f"Unsupported SVN URL scheme in '{url}'")
    if not parsed.netloc:
        raise ValueError(f"SVN URL is missing a hostname: '{url}'")


def require_svn():
    if shutil.which("svn") is None:
        raise RuntimeError("svn command not found in PATH")


def resolve_password(args):
    if args.prompt_password:
        return getpass.getpass("SVN password: ")
    return args.password


def build_command(url, args, password):
    cmd = ["svn", "mkdir"]
    if args.parents:
        cmd.append("-p")
    cmd.extend(["-m", args.message])

    if args.username:
        cmd.extend(["--username", args.username])
    if password:
        cmd.extend(["--password", password, "--no-auth-cache"])
    if args.non_interactive or password:
        cmd.append("--non-interactive")

    cmd.append(url)
    return cmd


def create_url(url, args, password):
    cmd = build_command(url, args, password)
    if args.dry_run:
        print("DRY RUN:", " ".join(cmd))
        return True, ""

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return True, result.stdout.strip()
    return False, result.stderr.strip() or result.stdout.strip()


def main():
    args = parse_args()
    require_svn()
    password = resolve_password(args)
    urls = load_urls(args)

    for url in urls:
        validate_url(url)

    print(f"Processing {len(urls)} SVN URL(s)")
    success_count = 0
    failure_count = 0

    for url in urls:
        ok, output = create_url(url, args, password)
        if ok:
            success_count += 1
            print(f"OK: {url}")
            if output:
                print(output)
        else:
            failure_count += 1
            print(f"FAIL: {url}", file=sys.stderr)
            if output:
                print(output, file=sys.stderr)

    print(f"Summary: success={success_count} failure={failure_count}")
    return 0 if failure_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
