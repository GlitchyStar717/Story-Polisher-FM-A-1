from typing import List
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import re
from ollama import chat
'''Running the models locally using ollama. With VRam limitation of 8Gb, choosing the quantized version of the models. You could replace the models with Gemini or OpenAPI and use your API key instead of this though.'''
MODELS = ['llama3:8b-instruct-q4_0', 'mistral:7b-instruct-q4_0']
MODEL = MODELS[0]

'''Creating the class that performs the serving of FastAPI requests'''
app = FastAPI()

'''Defining the structure of the objects we are passing between the elements. Using this with Gemini works really well as it can use this for providing the output just as described in this form.'''
class StoryInput(BaseModel):
    text_to_summarize: str
class AIResponse(BaseModel):
    questions_asked: List[str]

def generate_questions(story: str) -> List[str]:
    """
    Generates questions about loopholes and potential improvements for a given story using the chat API.

    Args:
        story: The input story text.

    Returns:
        A list of strings, where each string is a question.
    """
    # Prompt to extract meaningful critique questions
    prompt = f"""
    You are an expert in story critique and creative writing.

    Analyze the following story and identify potential weaknesses, inconsistencies, and areas for improvement. 
    Your task is to generate insightful, specific, and constructive QUESTIONS that a writer or editor should ask 
    to improve the story.

    The story is:

    \"\"\"{story}\"\"\"

    Respond with a list of questions only — no explanations, no summaries, no introductions.

    Format each question like this:
    1. Why does the character choose to...?
    2. Is there enough context for...?
    3. Could the plot benefit from...?

    Keep the questions concise and thought-provoking.
    """

    response = chat(model=MODEL, messages=[{'role': 'user', 'content': prompt}])
    parsed = response['message']['content']

    # Prompt to extract only the list in JSON-compatible format
    prompt2 = f"""
    You are a formatter bot.

    Convert the following list of questions into valid JSON according to this Pydantic model:

    ```python
    from pydantic import BaseModel
    from typing import List

    class AIResponse(BaseModel):
        questions_asked: List[str]
    ```

    The input is:

    \"\"\"{parsed}\"\"\"

    Format the output so that it looks like:
    {{
        "questions_asked": [
            "Question 1",
            "Question 2",
            ...
        ]
    }}

    Do not include any explanation or preamble — only output the JSON object.
    """

    response2 = chat(model=MODEL, messages=[{'role': 'user', 'content': prompt2}])
    parsed2 = response2['message']['content']
    print("Ollama Response 2:", parsed2)

    # Improved regex pattern (now handles multiple types of formatting reliably)
    question_pattern = r'"(.*?)"'
    questions = re.findall(question_pattern, parsed2)

    print("Extracted Questions:", questions)
    return questions

@app.get("/")
async def read_root():
    """
    Handles GET requests to the root path ("/").

    Returns:
        A JSON response with the message "Home".
    """
    return {"page": "Home"}

@app.post("/polish")
async def summarize(story_input: StoryInput):
    """
    Handles POST requests to the "/polish" path.  This function is intended to 
    summarize a story, but in the current implementation, the story is hardcoded.

    Args:
        story_input:  An instance of the StoryInput Pydantic model.  
                      Even though the parameter is named story_input, the function does not use the value passed by the user.

    Returns:
        A JSON response with a status code and the generated questions.  
        Returns status 696 if an error occurs, 717 on success.
    """
    # Hardcoded story.  The actual story provided by the user via the story_input parameter is ignored.
    story_input = "There was a boy named Ram. He was a handsome guy. He studied Social Science. He gets married some day. He lives happily ever after."
    try:
        # Call the generate_questions function to get the list of questions.
        response = generate_questions(story_input)
    except Exception as e:
        # Handle exceptions during question generation.  Prints an error message and returns a 696 status.
        print(f"Error occurred: {e}")
        return {'status': 696}
    # Return a 717 status and the generated questions.
    return {'status': 717, 'response': response}

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application using Uvicorn.
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)