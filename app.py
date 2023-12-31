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
    session['question_number'] = 0
    session['survey_complete'] = False

    return redirect('/questions/0')

@app.get('/questions/<int:question_number>')
def show_question(question_number):
    '''show question for survey, input question number to show'''

    if session['survey_complete']:
        return redirect('/thank-you')

    if question_number != session['question_number']:
        flash("Please answer the questions in order")
        return redirect(f"/questions/{session['question_number']}")

    question = survey.questions[question_number]

    return render_template(
        'question.html',
        question=question,
        question_number=question_number
    )

@app.post('/answer/<int:question_number>')
def handle_answer(question_number):
    '''appends user answer to response list'''

    responses = session["responses"]
    responses.append(request.form["choice"])
    session["responses"] = responses

    next_question = question_number + 1
    session['question_number'] += 1

    if next_question < len(survey.questions):
        return redirect(f'/questions/{next_question}')

    else:
        return redirect('/thank-you')

@app.get('/thank-you')
def survey_completion():
    '''showing thank-you screen with thank you results'''

    session['survey_complete'] = True

    return render_template(
        "completion.html",
        questions=survey.questions,
        responses=session["responses"]
    )




