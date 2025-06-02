# GitHub MCP Server

A Model Context Protocol (MCP) server that provides GitHub repository management functionality.

## Features

- **Create Repository**: Create new GitHub repositories with customizable settings

## Prerequisites

- Python 3.8 or higher
- GitHub Personal Access Token with repository creation permissions

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Joseph19820124/joseph-github-mcp-server.git
cd joseph-github-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your GitHub token:
```bash
export GITHUB_TOKEN="your_github_personal_access_token"
```

## Usage

### Running the MCP Server

```bash
python main.py
```

The server will start and listen for MCP requests via stdin/stdout.

### Available Tools

#### create_repository

Creates a new GitHub repository.

**Parameters:**
- `name` (required): Repository name
- `description` (optional): Repository description
- `private` (optional): Whether the repository should be private (default: false)

**Example Request:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "create_repository",
    "arguments": {
      "name": "my-new-repo",
      "description": "A sample repository",
      "private": false
    }
  },
  "id": "1"
}
```

**Example Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\n  \"success\": true,\n  \"repository\": {\n    \"id\": 123456789,\n    \"name\": \"my-new-repo\",\n    \"full_name\": \"username/my-new-repo\",\n    \"html_url\": \"https://github.com/username/my-new-repo\",\n    \"clone_url\": \"https://github.com/username/my-new-repo.git\",\n    \"ssh_url\": \"git@github.com:username/my-new-repo.git\",\n    \"private\": false,\n    \"description\": \"A sample repository\"\n  }\n}"
    }
  ],
  "id": "1"
}
```

## GitHub Token Setup

To use this MCP server, you need a GitHub Personal Access Token with the following permissions:

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with the following scopes:
   - `repo` (for repository access)
   - `user` (for user information)

3. Set the token as an environment variable:
```bash
export GITHUB_TOKEN="your_token_here"
```

## Development

### Project Structure

```
joseph-github-mcp-server/
├── main.py              # Main MCP server implementation
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── pyproject.toml      # Project configuration
```

### Testing

You can test the server by sending JSON-RPC requests:

1. Start the server:
```bash
python main.py
```

2. Send a test request:
```bash
echo '{"method": "tools/list", "id": "1"}' | python main.py
```

## MCP (Model Context Protocol)

This server implements the Model Context Protocol, which is an open standard for connecting AI applications with external data sources and tools. The protocol uses JSON-RPC 2.0 over stdio for communication.

### Supported MCP Methods

- `tools/list`: List available tools
- `tools/call`: Execute a specific tool

### Tool Schema

The `create_repository` tool follows the MCP tool schema:

```json
{
  "name": "create_repository",
  "description": "Create a new GitHub repository",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "Repository name"
      },
      "description": {
        "type": "string",
        "description": "Repository description",
        "default": ""
      },
      "private": {
        "type": "boolean",
        "description": "Whether the repository should be private",
        "default": false
      }
    },
    "required": ["name"]
  }
}
```

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
