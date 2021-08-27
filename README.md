# Chatbot Akademik AcademyBot

## Requirements

- Python
- Rasa Open Source
    You can install Rasa using `pip install rasa`
    Make sure you are using python version 3.8

## Running

1. Go to the directory `chatbot-akademik`
2. Run the command `rasa run --credentials ./credentials.yml  --enable-api --auth-token XYZ123 --model ./models --endpoints ./endpoints.yml --cors "*"`
3. You also need to run `rasa run actions`
4. Then go to the folder `src` and run `python -m rasa run --m ./models --endpoints endpoints.yml --port 5055 -vv --enable-api`
5. Open `localhost:8000/index.html` in your browser
