import openai
import time
import re

class Assistant:
    def __init__(self, api_key, assistant_id):
        self.client = openai.OpenAI(api_key=api_key)
        self.assistant_id = assistant_id

    def interact_with_assistant(self, user_query, thread_id=None):
        try:
            # Create or use existing thread
            if thread_id is None:
                thread = self.client.beta.threads.create()
                thread_id = thread.id

            # Add a message to the thread
            self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=user_query,
            )

            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
            )

            # Wait for the run to complete
            while run.status != "completed":
                time.sleep(1)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run.id
                )

            # Retrieve messages
            if run.status == "completed":
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread_id, order="asc"
                ).data

                # Extract assistant responses
                responses = []
                for msg in messages:
                    if msg.role == "assistant" and msg.content:
                        response_text = msg.content[0].text.value
                        cleaned_response = re.sub(r"\u3010.*?\u3011", "", response_text).strip()
                        responses.append(cleaned_response)

                return responses

        except Exception as e:
            return [f"Error: {str(e)}"]
