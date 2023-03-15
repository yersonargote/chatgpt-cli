# Python CLI to use chatGPT api

## API KEY

Create a file named `.env` and place inside the API KEY

```bash
# .env file
OPENAI_API_KEY=YOUR_API_KEY
```

## Install dependencies

```bash
pipenv install
```

## Run app

***Option 1***

```bash
pipenv shell
python3 main.py "filename" "message" "system"
```

***Option 2***

```bash
pipenv run python3 main.py "filename" "message" "system"
```

## Use

```bash
python3 main.py solid "What are the SOLID principles?"
```

```bash
python3 main.py solid "What are the SOLID principles?" programming
```

## Arguments

1. **Filename**

- The conversation is saved in `./chat/{filename}.json`

2. **Message**

- Is the input message of the user

3. **System**

- The system message helps set the behavior of the assistant

***System options***: `default` and `programming`
