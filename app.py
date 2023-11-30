from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get('/')
def show_survey_start():
    '''show initial instructions and button to start survey'''

    return render_template(
        "survey_start.html",
        title=survey.title,
        instructions=survey.instructions
        )

@app.post('/begin')
def begin_survey():
    '''post for when user clicks on button to start'''

    return redirect('/questions/0')

@app.get('/questions/<int:question_number>')
def show_question(question_number):
    '''show question for survey, input question number to show'''

    question = survey.questions[question_number]

    return render_template(
        'question.html',
        question=question
    )



