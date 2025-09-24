import html

class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None
        self.answered = False

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        if self.still_has_questions():
            self.current_question = self.question_list[self.question_number]
            self.question_number += 1
            self.answered = False
            q_text = html.unescape(self.current_question.text)
            # explanation = html.unescape(self.current_question.explanation)
            return f"Q.{self.question_number}: {q_text}"
        return None # Return none if no questions remain
        # user_answer = input(f"Q.{self.question_number}: {q_text} (True/False): ")
        # self.check_answer(user_answer)

    def check_answer(self, user_answer):
        if not self.current_question or self.answered:
            return False
        self.answered = True
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        return False




