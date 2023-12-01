from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
# from surveys import personality_quiz as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# responses = []

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

    session["responses"] = []

    return redirect('/question')

@app.get('/question')
def show_question():
    '''show question for survey, input question number to show'''

    if len(session["responses"]) == len(survey.questions):
        return redirect('/thank-you')

    next_question = len(session["responses"])

    question = survey.questions[next_question]

    return render_template(
        'question.html',
        question=question,
        question_number=next_question
    )

@app.post('/answer')
def handle_answer():
    '''appends user answer to response list'''

    responses = session["responses"]
    responses.append(request.form["choice"])
    session["responses"] = responses

    next_question = len(session["responses"])

    if next_question < len(survey.questions):
        return redirect('/question')

    else:
        return redirect('/thank-you')

@app.get('/thank-you')
def survey_completion():
    '''showing thank-you screen with thank you results'''

    return render_template(
        "completion.html",
        questions=survey.questions,
        responses=session["responses"]
    )
