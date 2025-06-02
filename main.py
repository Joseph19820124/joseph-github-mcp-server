#!/usr/bin/env python3
"""
GitHub MCP Server

A Model Context Protocol server that provides GitHub repository management functionality.
Currently supports creating repositories.
"""

import json
import logging
import sys
from typing import Any, Dict, List, Optional
import asyncio
import aiohttp
import os
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubMCPServer:
    """
    GitHub MCP Server implementation
    """
    
    def __init__(self, github_token: str):
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-MCP-Server/1.0"
        }
    
    async def create_repository(self, name: str, description: str = "", private: bool = False) -> Dict[str, Any]:
        """
        Create a new GitHub repository
        
        Args:
            name: Repository name
            description: Repository description
            private: Whether the repository should be private
            
        Returns:
            Dictionary containing repository information
        """
        url = urljoin(self.base_url, "/user/repos")
        
        payload = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": True  # Initialize with README
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                if response.status == 201:
                    repo_data = await response.json()
                    return {
                        "success": True,
                        "repository": {
                            "id": repo_data["id"],
                            "name": repo_data["name"],
                            "full_name": repo_data["full_name"],
                            "html_url": repo_data["html_url"],
                            "clone_url": repo_data["clone_url"],
                            "ssh_url": repo_data["ssh_url"],
                            "private": repo_data["private"],
                            "description": repo_data["description"]
                        }
                    }
                else:
                    error_data = await response.json()
                    return {
                        "success": False,
                        "error": f"Failed to create repository: {error_data.get('message', 'Unknown error')}",
                        "status_code": response.status
                    }

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle MCP request
        
        Args:
            request: MCP request dictionary
            
        Returns:
            MCP response dictionary
        """
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "tools/list":
                return {
                    "tools": [
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
                                        "default": False
                                    }
                                },
                                "required": ["name"]
                            }
                        }
                    ]
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name == "create_repository":
                    result = await self.create_repository(
                        name=arguments.get("name"),
                        description=arguments.get("description", ""),
                        private=arguments.get("private", False)
                    )
                    
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                else:
                    return {
                        "error": {
                            "code": -32601,
                            "message": f"Unknown tool: {tool_name}"
                        }
                    }
            
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Unknown method: {method}"
                    }
                }
                
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

    async def run_stdio(self):
        """
        Run the MCP server using stdio transport
        """
        logger.info("Starting GitHub MCP Server...")
        
        try:
            while True:
                # Read JSON-RPC request from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                
                if not line:
                    break
                
                try:
                    request = json.loads(line.strip())
                    response = await self.handle_request(request)
                    
                    # Add request ID to response if present
                    if "id" in request:
                        response["id"] = request["id"]
                    
                    # Write JSON-RPC response to stdout
                    print(json.dumps(response), flush=True)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {e}")
                    error_response = {
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")

def main():
    """
    Main entry point
    """
    # Get GitHub token from environment variable
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is required")
        sys.exit(1)
    
    # Create and run server
    server = GitHubMCPServer(github_token)
    asyncio.run(server.run_stdio())

if __name__ == "__main__":
    main()
