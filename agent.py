from langchain_community.llms import OpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.prompts import PromptTemplate
from langchain_experimental.utilities import PythonREPL
import asteval
import sympy as sp
import re


class SafeCalculator:
    def __init__(self):
        self.a_eval = asteval.Interpreter(use_numpy=True)
        self.repl = PythonREPL()

    def evaluate(self, expression: str) -> str:
        try:
            expression = re.sub(r'\s+', '', expression)
            if not re.match(r'^[0-9+\-*/().^sqrtlogsin costan]+$', expression):
                return "Invalid expression. Please use numbers and operators (+, -, *, /, ^, sqrt, log, sin, cos, tan)."

            try:
                expr = expression.replace('^', '**')
                expr = expr.replace('sqrt', 'sp.sqrt')
                expr = re.sub(r'\blog\(', 'sp.log10(', expr)
                result = sp.sympify(expr).evalf(10)
                return str(float(result))
            except Exception:
                result = self.a_eval(expression)
                if isinstance(result, (int, float)):
                    return str(result)
                raise ValueError("Evaluation failed.")

        except Exception:
            try:
                return self.repl.run(f"print({expression})")
            except Exception:
                return f"Error: Unable to evaluate '{expression}'. Please check the expression."


class MathAgent:
    def __init__(self, temperature: float = 0.2):
        self.llm = OpenAI(temperature=temperature)
        self.calculator = SafeCalculator()
        self.tool = self._create_tool()
        self.prompt_template = self._create_prompt_template()
        self.agent = self._initialize_agent()

    def _create_tool(self):
        return Tool(
            name="Calculator",
            func=self.calculator.evaluate,
            description="Evaluates mathematical expressions with high precision. Supports +, -, *, /, ^, sqrt, log (base 10), sin, cos, tan."
        )

    def _create_prompt_template(self):
        return PromptTemplate(
            input_variables=["input"],
            template=(
                "You are a precise mathematical assistant. "
                "For any numerical or algebraic expression, use the Calculator tool to compute the result accurately. "
                "If the input is not a clear mathematical expression, clarify with the user. Input: {input}"
            )
        )

    def _initialize_agent(self):
        return initialize_agent(
            tools=[self.tool],
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            agent_kwargs={
                "prefix": self.prompt_template.template,
                "input_variables": ["input"]
            }
        )

    def run(self, query: str):
        return self.agent.run(query)


