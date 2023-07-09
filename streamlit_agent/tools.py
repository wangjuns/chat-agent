from langchain.tools import BingSearchRun
from langchain.utilities import BingSearchAPIWrapper, PythonREPL
from langchain.agents.tools import Tool

python_repl = PythonREPL()
repl_tool = Tool(
    name="Python",
    description="A Python shell. Use this to execute python commands. "
    "Python command MUST NOT enclosed with '```python```'."
    "Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)
tool_map = {
    "Search": BingSearchRun(name="Search", api_wrapper=BingSearchAPIWrapper(k=3)),
    "Python": repl_tool,
}
