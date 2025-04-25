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
        
    def _preprocess_natural_language(self, query: str) -> str:
        """Convert natural language math questions into symbolic expressions."""
        # Normalize spacing
        query = query.lower().strip()
        
        # Remove common question prefixes
        prefixes = [
            "what is ", "what's ", "calculate ", "compute ", "find ", "what would be ",
            "can you tell me ", "tell me ", "solve ", "evaluate "
        ]
        for prefix in prefixes:
            if query.startswith(prefix):
                query = query[len(prefix):]
                break
        
        # Handle "the square root of X" patterns
        sqrt_pattern = r"(?:the\s+)?square\s+root\s+of\s+(.+?)(?:\?|$|\s+[a-zA-Z])"
        sqrt_match = re.search(sqrt_pattern, query)
        if sqrt_match:
            inner_expr = sqrt_match.group(1).strip()
            # If the inner expression contains operations, parse it first
            if any(op in inner_expr for op in ["+", "-", "*", "/", "^"]):
                query = query.replace(sqrt_match.group(0), f"sqrt({inner_expr})")
            else:
                query = query.replace(sqrt_match.group(0), f"sqrt({inner_expr})")
        
        # Handle other function patterns (similar logic can be extended)
        # For example: "log of X", "sine of X", etc.
        
        # Replace verbal operators with symbols
        replacements = [
            (r"\bplus\b", "+"),
            (r"\bminus\b", "-"),
            (r"\btimes\b", "*"),
            (r"\bdivided\s+by\b", "/"),
            (r"\bto\s+the\s+power\s+of\b", "^"),
            (r"\bto\s+the\b", "^"),
            (r"\bsquared\b", "^2"),
            (r"\bcubed\b", "^3")
        ]
        
        for pattern, replacement in replacements:
            query = re.sub(pattern, replacement, query)
        
        # Extract just the math expression by removing trailing punctuation and text
        query = re.sub(r"[?!]", "", query)
        
        # Final cleanup - remove any remaining non-math related words
        expression_chars = set("0123456789+-*/()^.sqrtlogsincostan ")
        cleaned_expr = ''.join(c for c in query if c in expression_chars)
        
        return cleaned_expr.strip()
    
    def evaluate(self, expression: str) -> str:
        """Evaluates mathematical expressions, including natural language inputs."""
        try:
            # First, try to parse natural language
            if not expression.strip().replace('.', '').isdigit() and any(c.isalpha() for c in expression):
                cleaned_expr = self._preprocess_natural_language(expression)
            else:
                cleaned_expr = expression
                
            # Remove spaces for symbolic processing
            cleaned_expr = re.sub(r'\s+', '', cleaned_expr)
            
            # Validate the cleaned expression
            if not re.match(r'^[0-9+\-*/().^sqrtlogsincostan]+$', cleaned_expr):
                return f"Invalid expression: '{cleaned_expr}'. Please use numbers and operators (+, -, *, /, ^, sqrt, log, sin, cos, tan)."
            
            try:
                # Try with sympy first - best for mathematical accuracy
                expr = cleaned_expr.replace('^', '**')
                expr = expr.replace('sqrt(', 'sp.sqrt(')
                expr = re.sub(r'\blog\(', 'sp.log10(', expr)
                expr = re.sub(r'\bsin\(', 'sp.sin(', expr)
                expr = re.sub(r'\bcos\(', 'sp.cos(', expr)
                expr = re.sub(r'\btan\(', 'sp.tan(', expr)
                
                result = sp.sympify(expr).evalf(10)
                return str(float(result))
            except Exception as e:
                # Fallback to asteval
                try:
                    result = self.a_eval(cleaned_expr)
                    if isinstance(result, (int, float)):
                        return str(result)
                    raise ValueError(f"Evaluation failed: {e}")
                except Exception:
                    # Last resort - try Python's eval with safety wrapper
                    return self.repl.run(f"print({cleaned_expr})")
                
        except Exception as e:
            return f"Error: Unable to evaluate '{expression}'. Please check the expression. Details: {str(e)}"


class MathAgent:
    def __init__(self, temperature: float = 0.1):  # Lower temperature for more consistent responses
        self.llm = OpenAI(temperature=temperature)
        self.calculator = SafeCalculator()
        self.tool = self._create_tool()
        self.prompt_template = self._create_prompt_template()
        self.agent = self._initialize_agent()

    def _create_tool(self):
        return Tool(
            name="Calculator",
            func=self.calculator.evaluate,
            description="Evaluates mathematical expressions including natural language queries. Supports +, -, *, /, ^, sqrt, log (base 10), sin, cos, tan."
        )

    def _create_prompt_template(self):
        return PromptTemplate(
            input_variables=["input"],
            template=(
                "You are a precise mathematical assistant specialized in interpreting and solving math problems. "
                "When faced with a mathematical query, first analyze whether it's a direct calculation or needs interpretation. "
                "For expressions like 'square root of 144 + 5', determine if it means sqrt(144) + 5 or sqrt(144+5) based on context. "
                "Always use the Calculator tool to compute numerical results accurately. Break complex problems into steps. "
                "If the input is ambiguous, explain the possible interpretations and solve each one. "
                "If the input is not a mathematical expression, clarify with the user what calculation they need. "
                "Input: {input}"
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
        try:
            # First try to run through the agent
            return self.agent.run(query)
        except Exception as e:
            # Fallback to direct calculator if agent fails
            try:
                result = self.calculator.evaluate(query)
                return f"Result: {result}"
            except Exception as inner_e:
                return f"I encountered an error processing your math query. Please try rephrasing it. Error: {str(e)}"