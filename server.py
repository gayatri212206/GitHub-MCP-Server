import os
import json
import httpx
from dotenv import load_dotenv
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv(Path(__file__).with_name(".env"))

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Create MCP server
mcp = FastMCP("GitHub MCP Server")

GITHUB_API = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}


def check_token():
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN missing. Check your .env file.")


# Tool 1: List GitHub repositories
@mcp.tool()
async def list_repositories() -> str:
    """List repositories accessible to the authenticated GitHub user."""

    check_token()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/user/repos",
            headers=HEADERS,
            params={"per_page": 30, "sort": "updated"}
        )

    response.raise_for_status()
    repos = response.json()

    result = [
        {
            "name": repo["name"],
            "full_name": repo["full_name"],
            "private": repo["private"],
            "url": repo["html_url"]
        }
        for repo in repos
    ]

    return json.dumps(result, indent=2)


# Tool 2: Get repository issues
@mcp.tool()
async def get_repository_issues(
    owner: str,
    repo: str,
    state: str = "open"
) -> str:
    """Get issues from a GitHub repository. State can be open, closed or all."""

    check_token()

    if state not in ["open", "closed", "all"]:
        raise ValueError("State must be open, closed or all.")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=HEADERS,
            params={"state": state, "per_page": 30}
        )

    response.raise_for_status()

    issues = response.json()

    result = [
        {
            "number": issue["number"],
            "title": issue["title"],
            "state": issue["state"],
            "url": issue["html_url"]
        }
        for issue in issues
        if "pull_request" not in issue
    ]

    return json.dumps(result, indent=2)


# Tool 3: Create a GitHub issue
@mcp.tool()
async def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: str
) -> str:
    """Create a new issue in a GitHub repository."""

    check_token()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=HEADERS,
            json={"title": title, "body": body}
        )

    response.raise_for_status()
    issue = response.json()

    return json.dumps({
        "message": "Issue created successfully!",
        "number": issue["number"],
        "title": issue["title"],
        "url": issue["html_url"]
    }, indent=2)


# Tool 4: Add labels to a GitHub issue
@mcp.tool()
async def add_labels(
    owner: str,
    repo: str,
    issue_number: int,
    labels: list[str]
) -> str:
    """Add labels to an existing GitHub issue."""

    check_token()

    if not labels:
        raise ValueError("At least one label is required.")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues/{issue_number}/labels",
            headers=HEADERS,
            json={"labels": labels}
        )

    response.raise_for_status()

    return json.dumps({
        "message": "Labels added successfully!",
        "labels": [label["name"] for label in response.json()]
    }, indent=2)


# Start MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
