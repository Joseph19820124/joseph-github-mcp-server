#!/usr/bin/env python3
"""
Test script for GitHub MCP Server

This script demonstrates how to test the GitHub MCP server by sending MCP requests.
"""

import json
import subprocess
import sys
import os

def test_tools_list():
    """Test the tools/list method"""
    print("Testing tools/list...")
    request = {
        "method": "tools/list",
        "id": "1"
    }
    
    return send_request(request)

def test_create_repository(name, description="Test repository", private=False):
    """Test the create_repository tool"""
    print(f"Testing create_repository with name: {name}...")
    request = {
        "method": "tools/call",
        "params": {
            "name": "create_repository",
            "arguments": {
                "name": name,
                "description": description,
                "private": private
            }
        },
        "id": "2"
    }
    
    return send_request(request)

def send_request(request):
    """Send a request to the MCP server"""
    try:
        # Start the MCP server process
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the request
        stdout, stderr = process.communicate(input=json.dumps(request) + "\n", timeout=30)
        
        if stderr:
            print(f"Error: {stderr}")
            return None
        
        try:
            response = json.loads(stdout.strip())
            print(f"Response: {json.dumps(response, indent=2)}")
            return response
        except json.JSONDecodeError:
            print(f"Invalid JSON response: {stdout}")
            return None
            
    except subprocess.TimeoutExpired:
        print("Request timed out")
        process.kill()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Main test function"""
    # Check if GITHUB_TOKEN is set
    if not os.getenv("GITHUB_TOKEN"):
        print("Error: GITHUB_TOKEN environment variable is required")
        print("Please set it with: export GITHUB_TOKEN='your_token_here'")
        sys.exit(1)
    
    print("GitHub MCP Server Test")
    print("=" * 30)
    
    # Test tools list
    response = test_tools_list()
    if not response:
        print("Failed to list tools")
        return
    
    print("\n" + "=" * 30)
    
    # Test repository creation (uncomment to actually create a repo)
    # WARNING: This will create a real repository!
    # repo_name = f"test-repo-{int(time.time())}"
    # response = test_create_repository(repo_name)
    # if not response:
    #     print("Failed to create repository")
    #     return
    
    print("Tests completed!")

if __name__ == "__main__":
    main()
