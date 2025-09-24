FROM python:3.13
ADD clairdicebot.py .
ADD path_buttons.py .
RUN pip install telebot
CMD ["python3", "./clairdicebot.py"] 