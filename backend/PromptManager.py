class PromptManager:

    def __init__(self):

        self.prompts = {

            "generation_prompt": """
        
                You are a helpful and knowledgeable assistant. 

                Use the following context to answer the question accurately and concisely.

                Context:
                {context}

                Question:
                {question}

                Answer:



                                """,


        }

    def get_prompt(self, key: str) -> str:
        if key not in self.prompts:
            raise ValueError(f"Prompt '{key}' not found in PromptManager.")
        return self.prompts[key]

    def add_prompt(self, key: str, prompt_template: str):
        self.prompts[key] = prompt_template

