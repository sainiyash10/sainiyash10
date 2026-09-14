"""
Fetches real GitHub stats for a user via the GitHub GraphQL API and regenerates
stats.svg and contribution.svg using the existing hand-built SVG designs (make_stats.py /
make_contribution.py) — no third-party rendering service involved.

Run in CI with GH_TOKEN (or GITHUB_TOKEN) set to a token with public read access.
Locally: GH_TOKEN=ghp_xxx GH_USERNAME=sainiyash10 python3 scripts/fetch_github_stats.py
"""
import os
import sys
import json
import datetime
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import make_stats
import make_contribution

API_URL = "https://api.github.com/graphql"
USERNAME = os.environ.get("GH_USERNAME", "sainiyash10")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

STATS_OUT = os.environ.get("STATS_OUT", "stats.svg")
CONTRIBUTION_OUT = os.environ.get("CONTRIBUTION_OUT", "contribution.svg")


def gql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(API_URL, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "profile-readme-stats-script")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
      totalCount
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes { stargazerCount }
    }
  }
}
"""

YEAR_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch_profile():
    data = gql(PROFILE_QUERY, {"login": USERNAME})
    return data["user"]


def fetch_all_time_contributions(created_at_iso):
    """GraphQL contributionsCollection is capped at 1 year per call, so we
    walk year-by-year from account creation to now and sum the totals, and
    collect the full daily contribution calendar for streak calculations."""
    created = datetime.datetime.fromisoformat(created_at_iso.replace("Z", "+00:00"))
    now = datetime.datetime.now(datetime.timezone.utc)
    commits = prs = issues = 0
    daily_counts = {}
    start = created
    while start < now:
        end = min(start + datetime.timedelta(days=365), now)
        data = gql(YEAR_QUERY, {
            "login": USERNAME,
            "from": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "to": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
        cc = data["user"]["contributionsCollection"]
        commits += cc["totalCommitContributions"]
        prs += cc["totalPullRequestContributions"]
        issues += cc["totalIssueContributions"]
        for week in cc["contributionCalendar"]["weeks"]:
            for day in week["contributionDays"]:
                daily_counts[day["date"]] = daily_counts.get(day["date"], 0) + day["contributionCount"]
        start = end
    return commits, prs, issues, daily_counts


def compute_streaks(daily_counts):
    """daily_counts: {'YYYY-MM-DD': count}. Returns
    (total_contributions, current_streak, current_range, longest_streak, longest_range)."""
    if not daily_counts:
        return 0, 0, "\u2013", 0, "\u2013"

    days = sorted(daily_counts.keys())
    total = sum(daily_counts.values())

    def fmt(d1, d2):
        a = datetime.date.fromisoformat(d1).strftime("%b %-d, %Y" if d1[:4] != d2[:4] else "%b %-d")
        b = datetime.date.fromisoformat(d2).strftime("%b %-d, %Y")
        return f"{a} \u2013 {b}"

    # longest streak: scan chronologically
    longest = 0
    longest_start = longest_end = days[0]
    run_start = None
    run_len = 0
    for d in days:
        if daily_counts[d] > 0:
            if run_len == 0:
                run_start = d
            run_len += 1
            if run_len > longest:
                longest = run_len
                longest_start, longest_end = run_start, d
        else:
            run_len = 0

    # current streak: scan backward from most recent day; allow "today" to be
    # 0 (day not over yet) without breaking the streak.
    idx = len(days) - 1
    if daily_counts[days[idx]] == 0:
        idx -= 1
    current = 0
    cur_end = days[idx] if idx >= 0 else days[-1]
    cur_start = cur_end
    while idx >= 0 and daily_counts[days[idx]] > 0:
        cur_start = days[idx]
        current += 1
        idx -= 1

    longest_range = fmt(longest_start, longest_end) if longest else "\u2013"
    current_range = fmt(cur_start, cur_end) if current else "\u2013"
    return total, current, current_range, longest, longest_range


def rank_letter(score):
    # Simple heuristic tiering (not an exact replica of any specific service's
    # algorithm) so the rank ring reacts to your real activity level.
    if score >= 900: return "S+"
    if score >= 700: return "S"
    if score >= 500: return "A+"
    if score >= 350: return "A"
    if score >= 200: return "B+"
    if score >= 100: return "B"
    if score >= 40: return "C+"
    return "C"


def tier_pct(score, cap=900):
    return max(8, min(97, round(score / cap * 100)))


def main():
    if not TOKEN:
        print("ERROR: set GH_TOKEN (or GITHUB_TOKEN) in the environment.", file=sys.stderr)
        sys.exit(1)

    profile = fetch_profile()
    followers = profile["followers"]["totalCount"]
    contributed_to = profile["repositoriesContributedTo"]["totalCount"]
    repos = profile["repositories"]["totalCount"]
    stars = sum(r["stargazerCount"] for r in profile["repositories"]["nodes"])

    commits, prs, issues, daily_counts = fetch_all_time_contributions(profile["createdAt"])
    total_contrib, cur_streak, cur_range, longest_streak, longest_range = compute_streaks(daily_counts)
    joined = datetime.date.fromisoformat(profile["createdAt"][:10]).strftime("%b %-d, %Y")

    print(f"stars={stars} commits={commits} prs={prs} issues={issues} "
          f"repos={repos} followers={followers} contributed_to={contributed_to} "
          f"total_contrib={total_contrib} current_streak={cur_streak} longest_streak={longest_streak}")

    # ---- stats.svg ----
    overall_score = commits * 1 + prs * 3 + issues * 2 + stars * 4 + repos * 2 + followers * 3
    rank = rank_letter(overall_score)
    pct = tier_pct(overall_score)
    make_stats.build(stars=stars, commits=commits, repos=repos, followers=followers,
                      rank=rank, rank_pct=pct, out_path=STATS_OUT)

    # ---- contribution.svg (contribution streak card) ----
    make_contribution.build(
        total_contributions=total_contrib, total_range=f"{joined} \u2013 Present",
        current_streak=cur_streak, current_range=cur_range,
        longest_streak=longest_streak, longest_range=longest_range,
        out_path=CONTRIBUTION_OUT,
    )


if __name__ == "__main__":
    main()
