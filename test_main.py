#Since the application returns html file, we require beautifulsoup for testing the output.
from fastapi.testclient import TestClient
from main import app
from bs4 import BeautifulSoup

#Create a TestClient to test the app
client = TestClient(app)

#Testing polish function
def test_polish_endpoint():
    #Test against a hard coded story.
    story = "There was a boy named Ram. He was a handsome guy. He studied Social Science. He gets married someday. He lives happily ever after."

    #Generate the response
    response = client.post("/polish", data={"story_input": story})

    #Test if the response gives errors
    assert response.status_code == 200

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    #Check the no. of items displayed in the returned HTML document. IF the no. of questions gave as a feedback > 0, then it passes the test. 
    question_items = soup.find_all("li")
    assert len(question_items) > 0, "No questions found in response HTML."
    #Also, print the questions generated.
    for item in question_items:
        print("Question:", item.text)
