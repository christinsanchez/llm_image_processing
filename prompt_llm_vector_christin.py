from openai import OpenAI
import os
 




dev_key = ""
client = OpenAI(api_key = dev_key )


assistant = client.beta.assistants.create(
  name="Nursing Video Image Identifier",
  instructions="You are an expert nurse. Use your knowledge to critique images from Nursing Training Videos.",
  model="gpt-4o",
  tools=[{"type": "file_search"}],
)


# # Create a vector store
# vector_store = client.beta.vector_stores.create(name="Nursing Training Videos")
 
# # Ready the files for upload to OpenAI

# # Specify the directory containing the text files
# directory = "./base64_grid_image_shrunken/"

# # Get all text files in the directory
# file_paths = [os.path.join(directory, filename) 
#               for filename in os.listdir(directory) 
#               if filename.endswith(".txt")]

# # Open each file in binary mode and store streams in a list
# file_streams = [open(path, "rb") for path in file_paths]

# # Example usage: print the file paths (optional)
# print("Files to upload:", file_paths)

# # Don't forget to close the files after processing to avoid memory leaks
# # for stream in file_streams:
# #     # Perform your OpenAI API upload or processing logic here
# #     stream.close()

    
# print("uploading files and adding them to vector store")
# # Use the upload and poll SDK helper to upload the files, add them to the vector store,
# # and poll the status of the file batch for completion.
# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#   vector_store_id=vector_store.id, files=file_streams
# )
 
# # You can print the status and the file counts of the batch to see the result of this operation.
# print(file_batch.status)
# print(file_batch.file_counts)


# print("updating assistant to use new Vector Store")

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": ['vs_iXat8Guc4qhuWwHeYkNwOZ9z']}},
)

from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
 

thread = client.beta.threads.create() 


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))


# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.



with client.beta.threads.runs.stream(
    model="gpt-4o-mini",
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="""The file in the vector store consist of a base64 encoding of an image. 
    Decode the base64 encodings.  
    The images consist of frames from a video. 
    There are 4 images per row and 4 row. 
    They are ordered from left to right. 
    And then the rows are ordered in descending order. 
    describe what you see in the frames""",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()