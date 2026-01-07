


# MCP Task Manager Demo 

A simple Python application demonstrating how to use **Model Context Protocol (MCP)** servers to build powerful applications that can interact with external services.

##  What is MCP?

**MCP (Model Context Protocol)** is a standardized way for applications (like this one) to communicate with external services and data sources. Think of it like USB for AI - one standard interface that works with many different tools and services.

### Key Concepts

- **MCP Server**: A service that exposes tools and data (e.g., filesystem, GitHub, Slack)
- **MCP Client**: An application (like this one) that uses those tools
- **Tools**: Functions the server provides (e.g., `read_file`, `write_file`, `create_issue`)

##  What This Demo Does

This project includes two versions:

1. **`mcp_demo_simple.py`** - Simulated version (runs immediately, no setup needed)
2. **`mcp_task_manager.py`** - Real version (requires MCP server installation)

Both demonstrate a task manager that:
-  Adds tasks with priorities
-  Lists all tasks
-  Marks tasks as complete
-  Deletes tasks
-  Stores everything through MCP (not direct file access!)

##  Quick Start

### Option 1: Run the Simple Demo (Recommended First)

No installation needed - just run:

```bash
python mcp_demo_simple.py
```

This shows exactly how MCP works without requiring any external services.

### Option 2: Run with Real MCP Server

1. **Install the MCP filesystem server:**
   ```bash
   npm install -g @modelcontextprotocol/server-filesystem
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the real version:**
   ```bash
   python mcp_task_manager.py
   ```

##  How It Works

### The Magic of MCP

Instead of this:
```python
# Direct file access
with open('tasks.json', 'r') as f:
    tasks = json.load(f)
```

We do this:
```python
# Through MCP server
result = await session.call_tool(
    "read_file",
    arguments={"path": "tasks.json"}
)
```

### Why This Matters

The same code pattern works with ANY MCP server:

- **Filesystem MCP** → Read/write files
- **GitHub MCP** → Create issues, PR's
- **Slack MCP** → Send messages, read channels  
- **Database MCP** → Query data, run transactions
- **Gmail MCP** → Read emails, send messages

Your application doesn't need to know the implementation details - it just calls MCP tools!

##  Project Structure

```
.
├── mcp_demo_simple.py      # Simulated demo (start here!)
├── mcp_task_manager.py     # Real MCP implementation
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

##  Code Walkthrough

### Key Components

1. **Connecting to MCP Server**
   ```python
   server_params = StdioServerParameters(
       command="npx",
       args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
   )
   ```

2. **Listing Available Tools**
   ```python
   tools = await session.list_tools()
   # Returns: read_file, write_file, list_directory, etc.
   ```

3. **Calling Tools**
   ```python
   result = await session.call_tool(
       "read_file",
       arguments={"path": "/tmp/tasks.json"}
   )
   ```

4. **Processing Results**
   ```python
   content = result.content[0].text
   tasks = json.loads(content)
   ```

##  Example Output

```
==================================================================
 MCP TASK MANAGER DEMO
==================================================================

Connected to MCP filesystem server

 Available tools from MCP server:
  - read_file: Read contents of a file
  - write_file: Write contents to a file
  - list_directory: List files in a directory

 Adding tasks...
 Task added: Build a Python MCP client (Priority: high)
 Task added: Write documentation (Priority: medium)

 Your Tasks:
------------------------------------------------------------
 [1]  Build a Python MCP client
 [2]  Write documentation
------------------------------------------------------------
```

##  Next Steps

### Try Other MCP Servers

1. **GitHub MCP Server**
   ```bash
   npm install -g @modelcontextprotocol/server-github
   ```
   Then modify the code to create issues, list repos, etc.

2. **Google Drive MCP Server**
   Connect to your Google Drive and manage documents

3. **Build Your Own**
   Create custom MCP servers for your specific needs!

### Extend This Demo

Ideas to build on this:
- Add due dates and reminders
- Integrate with a calendar MCP server
- Connect to Slack to post completed tasks
- Use GitHub MCP to create issues from tasks
- Add task categories and tags

##  Resources

- **MCP Specification**: https://modelcontextprotocol.io/
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Available Servers**: https://github.com/modelcontextprotocol/servers
- **Build Your Own**: See the MCP documentation for creating custom servers

##  Key Takeaways

1. **Standardization**: One protocol works with many services
2. **Flexibility**: Swap out MCP servers without changing client code
3. **Simplicity**: No need to learn each API individually
4. **Power**: Combine multiple MCP servers for complex workflows

##  Contributing

Have ideas to improve this demo? Feel free to experiment and extend it!

##  License

This demo is free to use for learning and experimentation.

---

**Happy coding with MCP! 🎉**
