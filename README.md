# GitHub MCP Server

**A custom Model Context Protocol (MCP) server that connects AI applications with GitHub operations through executable tools.**

Built with Python, FastMCP, and the GitHub REST API.

## Overview

Managing GitHub repositories involves repetitive operations such as checking repositories, tracking issues, creating new issues, and assigning labels.

This project provides an MCP-based interface that exposes these GitHub operations as tools, allowing compatible AI clients to interact with GitHub through the Model Context Protocol.

Instead of manually performing every operation through the GitHub interface, an MCP-compatible client can invoke the available tools.

## What It Does

The server implements four GitHub tools:

| Tool                    | Functionality                                                         |
| ----------------------- | --------------------------------------------------------------------- |
| `list_repositories`     | Fetches repositories accessible to the authenticated GitHub user.     |
| `get_repository_issues` | Retrieves repository issues filtered by state (open, closed, or all). |
| `create_issue`          | Creates a new issue with a title and description.                     |
| `add_labels`            | Adds one or more labels to an existing GitHub issue.                  |

## Key Features

- **MCP Integration:** Exposes GitHub operations through the Model Context Protocol.
- **GitHub REST API:** Communicates directly with GitHub's API.
- **Authentication:** Uses a GitHub Personal Access Token for authenticated requests.
- **Asynchronous API Requests:** Uses HTTPX AsyncClient for API communication.
- **Modular Tool Design:** Implements individual tools for specific GitHub operations.
- **Tool Testing:** Verified tool execution and server communication using MCP Inspector.

## Tech Stack

- **Language:** Python
- **MCP Framework:** FastMCP
- **API Integration:** GitHub REST API
- **HTTP Client:** HTTPX
- **Environment Management:** python-dotenv
- **Testing:** MCP Inspector
- **Transport:** STDIO

## Architecture

```text
       MCP-Compatible Client
                 |
                 | STDIO
                 |
          GitHub MCP Server
                 |
            FastMCP
                 |
       +---------+---------+
       |         |         |
   List Repos  Get Issues  Create Issue
                 |
             Add Labels
                 |
           HTTPX Client
                 |
          GitHub REST API
                 |
          GitHub Repository
<img width="341" height="452" alt="image" src="https://github.com/user-attachments/assets/f92cd3c5-6e0a-48ab-9352-d8981546927d" />

```

## Project Structure

```text
github-mcp-server/
│
├── .venv/             # Virtual environment (not committed)
├── .env               # GitHub token (not committed)
├── .gitignore
├── requirements.txt
└── server.py          # MCP server and GitHub tools
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/github-mcp-server.git

cd github-mcp-server
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure GitHub Authentication

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_personal_access_token
```

Generate a GitHub Personal Access Token with the necessary repository access and permissions.

For this project, the token needs permission to read repositories and issues and to create issues and manage issue labels.

**Security:** Never commit your `.env` file or expose your personal access token.

### 5. Run the MCP Server

```bash
python server.py
```

The server uses STDIO transport and waits for requests from an MCP client.

## Testing with MCP Inspector

To test the server interactively, run:

```bash
npx -y @modelcontextprotocol/inspector python server.py
```

Open the localhost URL displayed in the terminal.

Navigate to the Tools section and test the four available tools.

### Testing Results

All four tools were successfully tested using MCP Inspector.

<img width="753" height="255" alt="image" src="https://github.com/user-attachments/assets/ed305657-d02f-4ce2-a2be-13c5bf854a39" />

<img width="1486" height="501" alt="image" src="https://github.com/user-attachments/assets/f60c9daa-0ef3-4642-b32b-6ee1efc31eb5" />
<img width="1525" height="382" alt="image" src="https://github.com/user-attachments/assets/06edc006-7c07-431d-a3ee-4c418eb54b81" />
<img width="1488" height="360" alt="image" src="https://github.com/user-attachments/assets/5b9a2f7a-157f-4a29-a888-08bb8c818be0" />

## Problem Solved

The project demonstrates how GitHub operations can be exposed through a standardized tool interface rather than requiring every AI application to implement its own GitHub integration.

It provides a foundation for connecting GitHub functionality to MCP-compatible AI applications and agent workflows.

## What I Learned

- Implementing an MCP server using FastMCP.
- Understanding how MCP tools expose functionality to AI clients.
- Integrating third-party REST APIs using Python.
- Handling GitHub authentication with environment variables.
- Building asynchronous API requests using HTTPX.
- Testing MCP tools using MCP Inspector.

## Future Improvements

- Integrate with Claude Desktop and other compatible MCP clients.
- Add tools for searching repositories and retrieving file contents.
- Implement better API error handling and validation.
- Add automated tests using pytest.
- Introduce pagination and support for larger repository datasets.

---

**Built as a hands-on project to explore Model Context Protocol, AI tool integration, and GitHub API automation.**
