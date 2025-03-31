class PromptBuilder:
    def __init__(self, task, doc_type, use_case):
        self.task = task
        self.doc_type = doc_type
        self.use_case = use_case

    def generate(self, user_input):
        if self.task == "summarize":
            return self._build_summary_prompt(user_input)
        elif self.task == "qa":
            return self._build_qa_prompt(user_input)
        else:
            return user_input

    def _build_summary_prompt(self, doc_text):
        return (
            f"You are an expert assistant. The user uploaded a {self.doc_type}.\n"
            f"They want a summary for the purpose of: {self.use_case}.\n\n"
            f"Please provide a helpful summary below:\n\n"
            f"{doc_text.strip()}"
        )

    def _build_qa_prompt(self, question_and_doc):
        question, doc_text = question_and_doc
        return (
            f"You are reading a {self.doc_type}. The user has a question about it.\n"
            f"The context is for: {self.use_case}.\n\n"
            f"Document:\n{doc_text.strip()}\n\n"
            f"Question: {question}\n\n"
            f"Answer clearly based on the document."
        )
