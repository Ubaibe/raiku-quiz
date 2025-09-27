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
    else:
    # No more questions - transition to end screen
        st.session_state.stage = "end"
        st.rerun()

# End screen
elif st.session_state.stage == "end":
    final_score = st.session_state.quiz.score
    total_questions = st.session_state.quiz.question_number
    username = st.session_state.username_obj.get_username()
    st.session_state.leaderboard.update_score(username, final_score)
    st.title("Quiz Completed!")
    st.markdown("---")

    # Leaderboard
    st.subheader("📊 Your Final Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Score", f"{final_score}/{total_questions}")
    with col2:
        accuracy = (final_score / total_questions) * 100 if total_questions > 0 else 0
        st.metric("Accuracy", f"{accuracy:.1f}%")
    with col3:
        # Calculate user's rank with error handling
        if hasattr(st.session_state, 'leaderboard') and st.session_state.leaderboard:
            user_rank = st.session_state.leaderboard.get_user_rank(username)
        else:
            user_rank = 1
        st.metric("Your Rank", f"#{user_rank}")

    st.markdown("---")

    # Enhanced Leaderboard Display
    st.subheader("🏆 Global Leaderboard")

    # Get scores with error handling
    if hasattr(st.session_state, 'leaderboard') and st.session_state.leaderboard:
        scores = st.session_state.leaderboard.get_sorted_scores()
    else:
        scores = []
    if not scores:
        st.info("🎯 Be the first to set a score and claim the top spot!")
    else:
        # Create top 3 podium
        st.markdown("### 🥇🥈🥉 Top Champions")

        # Top 3 with special styling
        top_3 = scores[:3]
        for i, (name, user_scores) in enumerate(top_3, 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}[i]
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 15px;
                        border-radius: 10px;
                        margin: 10px 0;
                        color: white;
                        text-align: center;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <h3 style='margin: 0;'>{medal} {name}</h3>
                <p style='margin: 5px 0;'>Best Score: <strong>{user_scores['high_score']}</strong> |
                Total Points: <strong>{user_scores['cumulative_score']}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        # Rest of leaderboard
        if len(scores) > 3:
            st.markdown("### 📋 Complete Rankings")
            remaining_scores = scores[3:]

            # Create columns for better display
            col1, col2, col3, col4 = st.columns([1, 2, 1, 1])

            with col1:
                st.markdown("**Rank**")
            with col2:
                st.markdown("**Player**")
            with col3:
                st.markdown("**Best Score**")
            with col4:
                st.markdown("**Total Points**")

            # Display remaining players
            for i, (name, user_scores) in enumerate(remaining_scores, 4):
                col1, col2, col3, col4 = st.columns([1, 2, 1, 1])

                with col1:
                    st.markdown(f"**#{i}**")
                with col2:
                    # Highlight current user
                    if name == username:
                        st.markdown(f"👤 **{name}** ⭐")
                    else:
                        st.markdown(name)
                with col3:
                    st.markdown(f"{user_scores['high_score']}")
                with col4:
                    st.markdown(f"{user_scores['cumulative_score']}")

        # Leaderboard Statistics
        st.markdown("---")
        st.subheader("📈 Leaderboard Statistics")

        # Get leaderboard stats directly from the leaderboard instance
        if hasattr(st.session_state, 'leaderboard') and st.session_state.leaderboard:
            stats = st.session_state.leaderboard.get_leaderboard_stats()
        else:
            # Fallback if leaderboard not properly initialized
            stats = {"total_players": 0, "total_games": 0, "avg_high_score": 0, "max_high_score": 0, "total_points": 0}

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Players", stats["total_players"])
        with col2:
            st.metric("Total Games Played", stats["total_games"])
        with col3:
            st.metric("Average Best Score", f"{stats['avg_high_score']:.1f}")

        # Show additional stats if there are players
        if stats["total_players"] > 0:
            st.metric("Highest Score", stats["max_high_score"])
            st.metric("Total Points Earned", stats["total_points"])

        # Current user's detailed stats
        if hasattr(st.session_state, 'leaderboard') and st.session_state.leaderboard:
            user_stats = st.session_state.leaderboard.get_user_stats(username)
            if user_stats:
                st.markdown("---")
                st.subheader(f"🎯 {username}'s Statistics")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Your Best Score", user_stats['high_score'])
                with col2:
                    st.metric("Total Points Earned", user_stats['cumulative_score'])

    st.markdown("---")

    # Replay and motivation section
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again", type="primary", use_container_width=True):
            st.session_state.stage = "quiz"
            init_quiz()
            st.rerun()

    with col2:
        st.markdown("### 💡 Keep Learning!")
        st.markdown("""
        - 📚 Read the explanations carefully
        - 🎯 Practice makes perfect
        - 🏆 Challenge yourself to beat your high score
        - 🌟 Help grow the leaderboard!
        """)

    # Fun fact or motivational message based on performance
    if total_questions > 0:
        if final_score == total_questions:
            st.success("🎊 PERFECT SCORE! You're a true f(x) Protocol expert!")
        elif final_score >= total_questions * 0.8:
            st.success("🌟 Excellent work! You're mastering the concepts!")
        elif final_score >= total_questions * 0.6:
            st.info("👍 Good job! Keep learning and improving!")
        else:
            st.info("📖 Great effort! Every wrong answer is a learning opportunity!")
    # scores = st.session_state.leaderboard.get_sorted_scores()
    # if not scores:
    #     st.write("No scores yet!")
    # else:
    #     for i, (name, scores) in enumerate(scores, 1):
    #         st.write(f"{i}. {name}: High={scores['high_score']}, Total={scores['cumulative_score']}")

    # # Replay button
    # if st.button("Replay"):
    #     st.session_state.stage = "quiz"
    #     init_quiz()

    #     st.rerun()

