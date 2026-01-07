#!/usr/bin/env python3
"""
Simple MCP Demo - Simulated Version

This is a simplified demonstration that shows how MCP works conceptually
without requiring an actual MCP server to be running. Perfect for learning!
"""

import json
from typing import Any


class SimulatedMCPServer:
    """Simulates an MCP filesystem server for demonstration purposes."""
    
    def __init__(self):
        self.filesystem = {}  # In-memory file system
        self.tools = {
            "read_file": "Read contents of a file",
            "write_file": "Write contents to a file",
            "list_directory": "List files in a directory"
        }
    
    def list_tools(self):
        """List available tools."""
        return self.tools
    
    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute a tool with given arguments."""
        if tool_name == "read_file":
            path = arguments["path"]
            if path in self.filesystem:
                return {"content": self.filesystem[path]}
            else:
                return {"content": "[]"}  # Empty file
        
        elif tool_name == "write_file":
            path = arguments["path"]
            content = arguments["content"]
            self.filesystem[path] = content
            return {"success": True}
        
        elif tool_name == "list_directory":
            return {"files": list(self.filesystem.keys())}
        
        else:
            return {"error": f"Unknown tool: {tool_name}"}


class SimpleTaskManager:
    """Task manager using simulated MCP server."""
    
    def __init__(self):
        self.mcp_server = SimulatedMCPServer()
        self.tasks_file = "tasks.json"
        print("🚀 Task Manager initialized with simulated MCP server")
    
    def show_available_tools(self):
        """Display available MCP tools."""
        print("\n📦 Available MCP Tools:")
        tools = self.mcp_server.list_tools()
        for tool_name, description in tools.items():
            print(f"  • {tool_name}: {description}")
    
    def add_task(self, description: str, priority: str = "medium"):
        """Add a new task using MCP server."""
        # Read existing tasks via MCP
        tasks = self._read_tasks()
        
        # Create new task
        new_task = {
            "id": len(tasks) + 1,
            "description": description,
            "priority": priority,
            "completed": False
        }
        tasks.append(new_task)
        
        # Write back via MCP
        self._write_tasks(tasks)
        print(f"✅ Task added: {description} [Priority: {priority}]")
    
    def list_tasks(self):
        """List all tasks."""
        tasks = self._read_tasks()
        
        if not tasks:
            print("\n📝 No tasks yet!")
            return
        
        print("\n" + "=" * 70)
        print("📋 YOUR TASKS")
        print("=" * 70)
        
        for task in tasks:
            status = "✅" if task["completed"] else "⬜"
            priority_emoji = {
                "high": "🔴",
                "medium": "🟡", 
                "low": "🟢"
            }.get(task["priority"], "⚪")
            
            print(f"{status} [{task['id']}] {priority_emoji} {task['description']}")
        
        print("=" * 70)
    
    def complete_task(self, task_id: int):
        """Mark task as complete."""
        tasks = self._read_tasks()
        
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self._write_tasks(tasks)
                print(f"✅ Task {task_id} completed!")
                return
        
        print(f"❌ Task {task_id} not found")
    
    def delete_task(self, task_id: int):
        """Delete a task."""
        tasks = self._read_tasks()
        tasks = [t for t in tasks if t["id"] != task_id]
        self._write_tasks(tasks)
        print(f"🗑️  Task {task_id} deleted!")
    
    def _read_tasks(self) -> list[dict[str, Any]]:
        """Read tasks using MCP server's read_file tool."""
        result = self.mcp_server.call_tool(
            "read_file",
            {"path": self.tasks_file}
        )
        
        content = result.get("content", "[]")
        return json.loads(content)
    
    def _write_tasks(self, tasks: list[dict[str, Any]]):
        """Write tasks using MCP server's write_file tool."""
        self.mcp_server.call_tool(
            "write_file",
            {
                "path": self.tasks_file,
                "content": json.dumps(tasks, indent=2)
            }
        )


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}")


def main():
    """Run the demo."""
    print_header("🎯 MCP TASK MANAGER DEMO")
    
    print("\n💡 This demo shows how a Python app uses MCP servers to:")
    print("   • Read data through MCP tools (read_file)")
    print("   • Write data through MCP tools (write_file)")
    print("   • Accomplish real tasks without direct file access")
    
    # Create task manager
    manager = SimpleTaskManager()
    
    # Show available tools
    manager.show_available_tools()
    
    # Demo workflow
    print_header("📝 ADDING TASKS")
    manager.add_task("Build a Python MCP client", "high")
    manager.add_task("Write documentation", "medium")
    manager.add_task("Create demo application", "high")
    manager.add_task("Test with real MCP server", "low")
    
    # List tasks
    print_header("📋 CURRENT TASKS")
    manager.list_tasks()
    
    # Complete some tasks
    print_header("✅ COMPLETING TASKS")
    manager.complete_task(1)
    manager.complete_task(3)
    
    # Show updated list
    manager.list_tasks()
    
    # Delete a task
    print_header("🗑️  DELETING A TASK")
    manager.delete_task(2)
    
    # Final list
    manager.list_tasks()
    
    print_header("✨ DEMO COMPLETE")
    print("\n🎓 Key Takeaways:")
    print("   1. The app never directly accesses files")
    print("   2. All operations go through MCP server tools")
    print("   3. MCP provides a standard interface to external services")
    print("   4. The same code pattern works with ANY MCP server")
    print("\n💡 Next Steps:")
    print("   • Install real MCP servers: npm install -g @modelcontextprotocol/server-filesystem")
    print("   • Try mcp_task_manager.py with a real MCP server")
    print("   • Explore other MCP servers: GitHub, Slack, databases, etc.")
    print()


if __name__ == "__main__":
    main()
