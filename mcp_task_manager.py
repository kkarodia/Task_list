#!/usr/bin/env python3
"""
Simple Task Manager using MCP (Model Context Protocol)

This application demonstrates how to build a Python client that uses MCP servers
to accomplish real tasks. In this case, we'll create a task manager that can
interact with a filesystem MCP server.
"""

import asyncio
import json
from typing import Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class TaskManager:
    """A simple task manager that uses MCP servers to store tasks."""
    
    def __init__(self):
        self.session: ClientSession | None = None
        self.tasks_file = "tasks.json"
    
    async def connect_to_server(self):
        """Connect to the filesystem MCP server."""
        # In a real scenario, you'd connect to an actual MCP server
        # For this demo, we'll show the connection pattern
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
            env=None
        )
        
        # This creates a connection to the MCP server
        stdio_transport = await stdio_client(server_params)
        self.read, self.write = stdio_transport
        self.session = ClientSession(self.read, self.write)
        
        await self.session.initialize()
        print("✅ Connected to MCP filesystem server")
        
        # List available tools
        tools = await self.session.list_tools()
        print(f"\n📦 Available tools from MCP server:")
        for tool in tools.tools:
            print(f"  - {tool.name}: {tool.description}")
    
    async def add_task(self, task_description: str, priority: str = "medium"):
        """Add a new task using the MCP server."""
        if not self.session:
            print("❌ Not connected to MCP server")
            return
        
        # Read existing tasks
        tasks = await self._read_tasks()
        
        # Add new task
        new_task = {
            "id": len(tasks) + 1,
            "description": task_description,
            "priority": priority,
            "completed": False
        }
        tasks.append(new_task)
        
        # Write back using MCP server's write_file tool
        await self._write_tasks(tasks)
        print(f"✅ Task added: {task_description} (Priority: {priority})")
    
    async def list_tasks(self):
        """List all tasks using the MCP server."""
        if not self.session:
            print("❌ Not connected to MCP server")
            return
        
        tasks = await self._read_tasks()
        
        if not tasks:
            print("📝 No tasks found!")
            return
        
        print("\n📋 Your Tasks:")
        print("-" * 60)
        for task in tasks:
            status = "✅" if task["completed"] else "⬜"
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                task["priority"], "⚪"
            )
            print(f"{status} [{task['id']}] {priority_emoji} {task['description']}")
        print("-" * 60)
    
    async def complete_task(self, task_id: int):
        """Mark a task as complete using the MCP server."""
        if not self.session:
            print("❌ Not connected to MCP server")
            return
        
        tasks = await self._read_tasks()
        
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                await self._write_tasks(tasks)
                print(f"✅ Task {task_id} marked as complete!")
                return
        
        print(f"❌ Task {task_id} not found")
    
    async def _read_tasks(self) -> list[dict[str, Any]]:
        """Read tasks from file using MCP server."""
        try:
            # Use MCP server's read_file tool
            result = await self.session.call_tool(
                "read_file",
                arguments={"path": f"/tmp/{self.tasks_file}"}
            )
            
            # Parse the content from MCP response
            content = result.content[0].text if result.content else "[]"
            return json.loads(content)
        except Exception:
            # File doesn't exist yet, return empty list
            return []
    
    async def _write_tasks(self, tasks: list[dict[str, Any]]):
        """Write tasks to file using MCP server."""
        # Use MCP server's write_file tool
        await self.session.call_tool(
            "write_file",
            arguments={
                "path": f"/tmp/{self.tasks_file}",
                "content": json.dumps(tasks, indent=2)
            }
        )
    
    async def close(self):
        """Close the connection to the MCP server."""
        if self.session:
            await self.session.close()
            print("\n👋 Disconnected from MCP server")


async def main():
    """Main function demonstrating the task manager."""
    print("=" * 60)
    print("🚀 MCP Task Manager Demo")
    print("=" * 60)
    
    manager = TaskManager()
    
    try:
        # Connect to MCP server
        await manager.connect_to_server()
        
        # Demo: Add some tasks
        print("\n📝 Adding tasks...")
        await manager.add_task("Write documentation for MCP demo", "high")
        await manager.add_task("Review pull requests", "medium")
        await manager.add_task("Update dependencies", "low")
        
        # List tasks
        await manager.list_tasks()
        
        # Complete a task
        print("\n✅ Completing task 1...")
        await manager.complete_task(1)
        
        # List tasks again
        await manager.list_tasks()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Note: This demo requires an MCP filesystem server to be available.")
        print("   Install it with: npm install -g @modelcontextprotocol/server-filesystem")
    
    finally:
        await manager.close()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
