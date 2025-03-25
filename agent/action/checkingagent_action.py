from .base_action import Action
from typing import Optional
import re, json5
from .utils import remove_quote


class SendAPI(Action):
    
    argument: dict = {}
    action_name: str = "Send_api"
    
    @classmethod
    def get_action_description(cls) -> str:
        return """
# Send api Action
* Signature: {
    "action_name": "Send_api",
    "argument": [{
        "api_name": api's name, which should be the same as the tool,
        "docstring": The concise usage instruction of an API, including functional description, input parameters, and output description,
        "note": A brief description of the specific scenario or problem this API is intended to address.
        "demo": usage example of api,
    }]
}
* Description: The Send_api Action is used to submit finalized APIs or tools to the SolvingAgent. The api_name corresponds to the name of the API or tool generated by the ToolAgent, `docstring` provides detailed usage information, `note` includes a brief description of the specific scenario or problem this API is intended to address, and `demo` includes a practical usage example. This action requires sending the data in JSON format, and if multiple APIs need to be sent, they should be packaged in a list format.
Please note that this action should only be used after you've checked all the tools and selected the appropriate APIs and tools. It signifies the completion of the tool creation task.

* Examples:
{
    "action_name": "Send_api",
    "argument": [
        {
            "api_name": "linear_equation_solver",
            "docstring": "linear_equation_solver(a, b, c) solves the linear equation ax + b = c.\nParameters:\n- a (float): The coefficient of the variable x.\n- b (float): The constant term added to the product of a and x.\n- c (float): The constant term on the right-hand side of the equation.\nReturns:\n- The solution (float) to the equation ax + b = c."
            "note": "The API must accurately solve for x in a linear equation ax + b = c, where a \neq 0, and return the solution as a numeric value.",
            "demo": "Query: Solve 2x + 3 = 7; \nExample: linear_equation_solver(2, 3, 7)\nExplanation: This example solves the linear equation 2x + 3 = 7 by isolating x to find its value."
        }
    ]
}
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        pattern = re.compile(r'\{.*\}', re.DOTALL)
        match = pattern.search(text)
        
        if match:
            json_string = match.group(0)
            json_string = json_string.replace('\n', ' ')
            try:
                # Parse the JSON string
                action_json = json5.loads(json_string)
            except Exception as e:
                return None
        else:
            return None

        action_name = action_json.get("action_name", None)
        if not action_name:
            return None
        elif action_name.lower() != "send_api":
            return None
        argument = action_json.get("argument", None)
        if not argument:
            return None
        
        argument = argument if isinstance(argument, list) else [argument]
        
        return cls(argument=argument)
        
    def print_action(self):
        return f"""
{{
  "action_name": "Send_api",
  "argument": {self.argument}
}}
"""

class Feedback_outdated(Action):
    argument: dict = {}
    action_name: str = "Feedback"
    
    @classmethod
    def get_action_description(cls) -> str:
        return """
## Feedback Action
* Signature: Feedback(the message you want to feedback to ToolAgent)
* Description: The Feedback Action allows you to send feedback on a tool or other request to the ToolAgent. Feedback must be specific and constructive. Whenever you complete a stage of the review, you need to provide your feedback to the ToolAgent, and your feedback must be thorough and critical.
* Example:
  - Example1: Feedback("The tool quadratic_equation_solver returned a ZeroDivisionError: division by zero, likely because the coefficient  a = 0 , making the equation linear rather than quadratic. To prevent this, add a check at the start of quadratic_equation_solver to ensure a \neq 0")
  - Example2: Feedback("The tool calculate_average failed with a KeyError because the specified column ‘scores’ was not found in the dataset. Add a check to verify the column exists before proceeding with the calculation.")
  - Example3: Feedback("The tool linear_regression failed with a ValueError because the input dataset contained missing values. To handle this, consider adding a preprocessing step to either remove rows with missing values or impute them before performing regression.")
"""
        
    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        pattern = r'Feedback(.*)'
        matches = re.findall(pattern, text, flags=re.DOTALL)
        if matches:
            message = matches[0].strip()
            if message.startswith('(') and message.endswith(')'):
                message = message[1:-1]
            return cls(argument={"message": remove_quote(message)})
        return None
        

    def print_action(self):
        return f"""
Feedback("{self.argument.get("Feedback")}")
```
"""


class Feedback(Action):
    argument: dict = {}
    action_name: str = "Feedback"
    
    @classmethod
    def get_action_description(cls) -> str:
        return """
# Feedback Action
* Signature: {
    "action_name": "Feedback",
    "argument": {
        "feedback": ...
        "passed": true/false
    }
}
* Description: The Feedback Action is used to provide feedback to the ToolAgent or SolvingAgent. The feedback field contains detailed comments or suggestions, while pass indicates whether the submitted API or tool meets the requirements (true for approval, false for rejection). This action is essential for evaluating and improving the quality of the generated APIs or tools. Feedback should be concise, constructive, and relevant, ensuring the tool aligns with the intended use case.
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        pattern = re.compile(r'\{.*\}', re.DOTALL)
        match = pattern.search(text)
        
        if match:
            json_string = match.group(0)
            json_string = json_string.replace('\n', ' ')
            json_string = json_string.replace('\t', '')
            try:
                action_json = json5.loads(json_string)
            except Exception as e:
                return None
        else:
            return None

        action_name = action_json.get("action_name", None)
        if not action_name:
            return None
        elif action_name.lower() != "feedback":
            return None
        argument = action_json.get("argument", None)
        if not argument:
            return None
        elif "feedback" not in argument.keys() or "passed" not in argument.keys():
            return None
        
        return cls(argument=argument)
    
    def print_action(self) -> str:
        return f"""
{{
  "action_name": "Feedback",
  "argument": {self.argument}
}} 
"""