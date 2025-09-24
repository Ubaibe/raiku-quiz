# app.py
import streamlit as st
import random
from question_model import Question
from data import get_decoded_question_data
from quiz_brain import QuizBrain
from username import Username
from leaderboard import Leaderboard
import html

# Initialize session state
def init_session_state():
    defaults = {
        "stage": "username",
        "username_obj": Username(),
        "quiz": None,
        "leaderboard": Leaderboard(),
        "current_question": None,
        "answered": False,
        "feedback": None,
        "explanation": None,
        "question_key": 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Initialize quiz
def init_quiz():
    question_data = get_decoded_question_data()
    question_bank = []
    selected_questions = random.sample(question_data, k=min(10, len(question_data)))
    for question in selected_questions:
        question_text = question["question"]
        question_answer = question["correct_answer"]
        explanation = question.get("explanation", "No explanation provided.")
        new_question = Question(question_text, question_answer, explanation)
        question_bank.append(new_question)
    random.shuffle(question_bank)
    st.session_state.quiz = QuizBrain(question_bank)
    st.session_state.current_question = None
    st.session_state.answered = False
    st.session_state.feedback = None
    st.session_state.explanation = None
    st.session_state.question_key += 1

# Username screen
if st.session_state.stage == "username":
    st.title("Quiz Game")
    st.write("Enter your username to start the quiz:")
    username_input = st.text_input("Username", key="username_input")
    if st.button("Start Game"):
        if st.session_state.username_obj.set_username(username_input):
            init_quiz()
            st.session_state.stage = "quiz"
            st.rerun()
        else:
            st.error("Please enter a username!")

# Quiz screen
elif st.session_state.stage == "quiz":
    if not st.session_state.quiz:
        init_quiz()

    if st.session_state.quiz.still_has_questions():
        # Load next question if needed (only if not answered)
        if not st.session_state.current_question:
            question_text = st.session_state.quiz.next_question()
            if question_text:
                st.session_state.current_question = question_text
                st.session_state.answered = False
                st.session_state.feedback = None
                st.session_state.explanation = None
                st.session_state.question_key += 1
            else:
                # No more questions
                st.session_state.stage = "end"
                st.rerun()

        # Display player and score
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**Player: {st.session_state.username_obj.get_username()}**")
        with col2:
            st.markdown(f"**Score: {st.session_state.quiz.score}**")

        # Display question
        if st.session_state.current_question:
            st.markdown(f"**{st.session_state.current_question}**")
        else:
            # No more questions, end the quiz
            st.session_state.stage = "end"
            st.rerun()

        # True/False buttons
        col_true, col_false = st.columns(2)
        with col_true:
            if st.button("True", key=f"true_{st.session_state.question_key}", disabled=st.session_state.answered):
                # Get explanation before marking as answered
                current_explanation = html.unescape(st.session_state.quiz.current_question.explanation)
                is_right = st.session_state.quiz.check_answer("True")
                st.session_state.feedback = "Correct!" if is_right else "Incorrect!"
                st.session_state.explanation = current_explanation
                st.session_state.answered = True
        with col_false:
            if st.button("False", key=f"false_{st.session_state.question_key}", disabled=st.session_state.answered):
                # Get explanation before marking as answered
                current_explanation = html.unescape(st.session_state.quiz.current_question.explanation)
                is_right = st.session_state.quiz.check_answer("False")
                st.session_state.feedback = "Correct!" if is_right else "Incorrect!"
                st.session_state.explanation = current_explanation
                st.session_state.answered = True

        # Feedback and explanation
        if st.session_state.feedback:
            # Show feedback
            st.markdown(
                f"<div style='background-color: {'green' if 'Correct' in st.session_state.feedback else 'red'}; padding: 10px; color: white; text-align: center;'>"
                f"{st.session_state.feedback}</div>",
                unsafe_allow_html=True
            )

            # Show explanation
            if st.session_state.explanation:
                st.markdown("---")  # Add a separator line
                st.markdown(f"**📖 Explanation:** {st.session_state.explanation}")
                st.markdown("---")  # Add another separator line
            else:
                st.markdown("*No explanation available*")

            # Next button
            if st.button("Next Question", key=f"next_{st.session_state.question_key}"):
                st.session_state.feedback = None
                st.session_state.explanation = None
                st.session_state.current_question = None
                st.session_state.answered = False
                st.session_state.question_key += 1
                st.rerun()

# End screen
elif st.session_state.stage == "end":
    final_score = st.session_state.quiz.score
    total_questions = st.session_state.quiz.question_number
    st.session_state.leaderboard.update_score(st.session_state.username_obj.get_username(), final_score)
    st.title("Quiz Completed!")
    st.markdown(f"**Final Score: {final_score}/{total_questions}**")

    # Leaderboard
    st.subheader("Leaderboard")
    scores = st.session_state.leaderboard.get_sorted_scores()
    if not scores:
        st.write("No scores yet!")
    else:
        for i, (name, scores) in enumerate(scores, 1):
            st.write(f"{i}. {name}: High={scores['high_score']}, Total={scores['cumulative_score']}")

    # Replay button
    if st.button("Replay"):
        st.session_state.stage = "quiz"
        init_quiz()
        st.rerun()