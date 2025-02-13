from typing import Any

from swarms.models.base_llm import AbstractLLM
from swarms.tools.format_tools import Jsonformer


class ToolAgent(AbstractLLM):
    """
    Represents a tool agent that performs a specific task using a model and tokenizer.

    Args:
        name (str): The name of the tool agent.
        description (str): A description of the tool agent.
        model (Any): The model used by the tool agent.
        tokenizer (Any): The tokenizer used by the tool agent.
        json_schema (Any): The JSON schema used by the tool agent.
        *args: Variable length arguments.
        **kwargs: Keyword arguments.

    Attributes:
        name (str): The name of the tool agent.
        description (str): A description of the tool agent.
        model (Any): The model used by the tool agent.
        tokenizer (Any): The tokenizer used by the tool agent.
        json_schema (Any): The JSON schema used by the tool agent.

    Methods:
        run: Runs the tool agent for a specific task.

    Raises:
        Exception: If an error occurs while running the tool agent.


    Example:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from swarms import ToolAgent


        model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v2-12b")
        tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-12b")

        json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"},
                "is_student": {"type": "boolean"},
                "courses": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }

        task = "Generate a person's information based on the following schema:"
        agent = ToolAgent(model=model, tokenizer=tokenizer, json_schema=json_schema)
        generated_data = agent.run(task)

        print(generated_data)
    """

    def __init__(
        self,
        name: str = "Function Calling Agent",
        description: str = "Generates a function based on the input json schema and the task",
        model: Any = None,
        tokenizer: Any = None,
        json_schema: Any = None,
        max_number_tokens: int = 500,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.name = name
        self.description = description
        self.model = model
        self.tokenizer = tokenizer
        self.json_schema = json_schema
        self.max_number_tokens = max_number_tokens

    def run(self, task: str, *args, **kwargs):
        """
        Run the tool agent for the specified task.

        Args:
            task (str): The task to be performed by the tool agent.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The output of the tool agent.

        Raises:
            Exception: If an error occurs during the execution of the tool agent.
        """
        try:
            self.toolagent = Jsonformer(
                model=self.model,
                tokenizer=self.tokenizer,
                json_schema=self.json_schema,
                prompt=task,
                max_number_tokens=self.max_number_tokens,
                *args,
                **kwargs,
            )

            out = self.toolagent()
            return out
        except Exception as error:
            print(f"[Error] [ToolAgent] {error}")
            raise error

    def __call__(self, task: str, *args, **kwargs):
        """Call self as a function.

        Args:
            task (str): _description_

        Returns:
            _type_: _description_
        """
        return self.run(task, *args, **kwargs)
