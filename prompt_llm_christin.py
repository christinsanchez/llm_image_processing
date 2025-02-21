import json
import os
from openai import OpenAI 
import time 


# API Key 

def initialize_openai_client(api_key = dev_key):
    return OpenAI(api_key) 


def submit_message(assistant_id, thread, user_message, client):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )

    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )


def wait_on_run(run, thread, client):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.1)
    return run


def get_response(thread, client):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")


# read base64 content from a text file
def read_base64_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()


def submit_base64_images_for_description(folder_path, client, output_file="image_descriptions.txt"):
    """Iterate through a folder of base64-encoded images and get descriptions from the LLM."""
    descriptions = [] 


    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            print("it starts constructing the path ")
            # constructing full path and read the base64 encoding
            file_path = os.path.join(folder_path, file_name)
            base64_image = read_base64_from_file(file_path)

            prompt = """ 
                    This image consists of smaller images which are frames from a 
                        video. They are ordered left to right in the rows. Then 
                        the rows are stacked in order from top to bottom. 
                        There are 4 images per row. 
                        The video is a nursing training video. 
                        Describe the communication and actions between the nurse and patient in each frame, noting non-verbal cues, equipment handling, and any steps that involve close contact or procedural focus.
                        {
                            File Name: 
                            General Description: 
                            Number of People: 
                            Actions of People: 
                            General Setting: 
                            Picture Quality: 
                            Trouble/Problems while Reading Image: 
                        }     
            """

            print(f"Processing {file_name}: {base64_image[:30]}...")

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                {
                    "role": "user",
                    "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                        "url":  f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                    ],
                }
                ],
            )

            print(response.choices[0].message.content)

            # Extracting the response content
            description = str(response.choices[0].message.content) 
            
            response_content = response.choices[0].message.content
            # Print the response to confirm its format
            print("Original response content:", repr(response_content))

            # Remove triple backticks if present
            cleaned_response = response_content.replace("```json", "").replace("```", "").strip()

            try:
                # Attempt to parse the cleaned response
                description_data = json.loads(cleaned_response)
                description_data['File Name'] = file_name  # Add file name to the JSON data
                description_data['Prompt'] = prompt
                descriptions.append(description_data)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error for file {file_name}: {e}")
                print("Cleaned response content:", cleaned_response)
                continue  # Skip to the next file or handle as needed

    # Write descriptions to the output file
    with open(output_file, "w") as file:
        json.dump(descriptions, file, indent=4)

    print(f"Descriptions have been written to {output_file}")


from openai import OpenAI

if __name__ == "__main__":
    client = OpenAI(api_key = dev_key)

    submit_base64_images_for_description("./1280px/1280px_pics/4x4_grid", client, "./different_prompts/behavior_interaction.txt")
