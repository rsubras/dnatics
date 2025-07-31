"""
Rapid Fire Question Generator for different subjects
Generates timed quiz questions for Mathematics, English, and Science
"""

import random
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class RapidFireGenerator:
    def __init__(self):
        self.math_operations = {
            'multiplication_tables': self._generate_multiplication_table,
            'two_digit_multiplication': self._generate_two_digit_multiplication,
            'fractions': self._generate_fraction_questions,
            'basic_arithmetic': self._generate_basic_arithmetic
        }
        
        self.english_grammar = {
            'parts_of_speech': self._generate_parts_of_speech,
            'verb_forms': self._generate_verb_forms,
            'sentence_correction': self._generate_sentence_correction,
            'synonyms_antonyms': self._generate_synonyms_antonyms
        }
        
        self.science_basics = {
            'general_science': self._generate_general_science,
            'biology_basics': self._generate_biology_basics,
            'physics_basics': self._generate_physics_basics,
            'chemistry_basics': self._generate_chemistry_basics
        }
        
    def generate_rapid_fire_questions(self, subject: str, num_questions: int) -> List[Dict]:
        """Generate rapid fire questions for the specified subject"""
        questions = []
        
        if subject.lower() == 'mathematics':
            questions = self._generate_math_questions(num_questions)
        elif subject.lower() == 'english':
            questions = self._generate_english_questions(num_questions)
        elif subject.lower() == 'science':
            questions = self._generate_science_questions(num_questions)
        
        return questions
    
    def _generate_math_questions(self, num_questions: int) -> List[Dict]:
        """Generate mathematics questions with no repeats"""
        questions = []
        operation_types = list(self.math_operations.keys())
        
        # Create a pool of unique questions
        all_questions_pool = []
        for operation in operation_types:
            try:
                # Generate multiple questions from each operation type
                for _ in range(30):  # Generate 30 from each type
                    question_data = self.math_operations[operation]()
                    if question_data:
                        question_data['subject'] = 'Mathematics'
                        question_data['category'] = operation
                        all_questions_pool.append(question_data)
            except:
                continue
        
        # Remove duplicates based on question text
        unique_questions = []
        seen_questions = set()
        for q in all_questions_pool:
            if q['question'] not in seen_questions:
                unique_questions.append(q)
                seen_questions.add(q['question'])
        
        # Randomly sample from unique questions
        if len(unique_questions) >= num_questions:
            selected_questions = random.sample(unique_questions, num_questions)
        else:
            # If not enough unique questions, add some duplicates
            selected_questions = unique_questions.copy()
            while len(selected_questions) < num_questions:
                selected_questions.append(random.choice(unique_questions))
        
        # Add question numbers
        for i, question_data in enumerate(selected_questions):
            question_data['question_number'] = i + 1
            questions.append(question_data)
        
        return questions
    
    def _generate_english_questions(self, num_questions: int) -> List[Dict]:
        """Generate English grammar questions with no repeats"""
        questions = []
        grammar_types = list(self.english_grammar.keys())
        
        # Create a pool of unique questions
        all_questions_pool = []
        for grammar_type in grammar_types:
            try:
                # Generate multiple questions from each grammar type
                for _ in range(25):  # Generate 25 from each type
                    question_data = self.english_grammar[grammar_type]()
                    if question_data:
                        question_data['subject'] = 'English'
                        question_data['category'] = grammar_type
                        all_questions_pool.append(question_data)
            except:
                continue
        
        # Remove duplicates based on question text
        unique_questions = []
        seen_questions = set()
        for q in all_questions_pool:
            if q['question'] not in seen_questions:
                unique_questions.append(q)
                seen_questions.add(q['question'])
        
        # Randomly sample from unique questions
        if len(unique_questions) >= num_questions:
            selected_questions = random.sample(unique_questions, num_questions)
        else:
            # If not enough unique questions, add some duplicates
            selected_questions = unique_questions.copy()
            while len(selected_questions) < num_questions:
                selected_questions.append(random.choice(unique_questions))
        
        # Add question numbers
        for i, question_data in enumerate(selected_questions):
            question_data['question_number'] = i + 1
            questions.append(question_data)
        
        return questions
    
    def _generate_science_questions(self, num_questions: int) -> List[Dict]:
        """Generate basic science questions with no repeats"""
        questions = []
        science_types = list(self.science_basics.keys())
        
        # Create a pool of all possible questions
        all_questions_pool = []
        for science_type in science_types:
            try:
                # Generate multiple questions from each type
                for _ in range(20):  # Generate 20 from each type
                    question_data = self.science_basics[science_type]()
                    if question_data:
                        question_data['subject'] = 'Science'
                        question_data['category'] = science_type
                        all_questions_pool.append(question_data)
            except:
                continue
        
        # Remove duplicates based on question text
        unique_questions = []
        seen_questions = set()
        for q in all_questions_pool:
            if q['question'] not in seen_questions:
                unique_questions.append(q)
                seen_questions.add(q['question'])
        
        # Randomly sample from unique questions
        if len(unique_questions) >= num_questions:
            selected_questions = random.sample(unique_questions, num_questions)
        else:
            # If not enough unique questions, add some duplicates
            selected_questions = unique_questions.copy()
            while len(selected_questions) < num_questions:
                selected_questions.append(random.choice(unique_questions))
        
        # Add question numbers
        for i, question_data in enumerate(selected_questions):
            question_data['question_number'] = i + 1
            questions.append(question_data)
        
        return questions
    
    # Mathematics Question Generators
    def _generate_multiplication_table(self) -> Dict:
        """Generate multiplication table questions"""
        num1 = random.randint(2, 12)
        num2 = random.randint(2, 12)
        answer = num1 * num2
        
        # Generate wrong options
        options = [answer]
        while len(options) < 4:
            wrong_answer = answer + random.randint(-10, 10)
            if wrong_answer > 0 and wrong_answer not in options:
                options.append(wrong_answer)
        
        random.shuffle(options)
        correct_option = chr(ord('a') + options.index(answer))
        
        return {
            'question': f"What is {num1} × {num2}?",
            'options': [f"{chr(ord('a') + i)}) {opt}" for i, opt in enumerate(options)],
            'correct_answer': correct_option,
            'answer_value': answer,
            'type': 'MCQ'
        }
    
    def _generate_two_digit_multiplication(self) -> Dict:
        """Generate two-digit multiplication questions"""
        num1 = random.randint(11, 99)
        num2 = random.randint(11, 99)
        answer = num1 * num2
        
        return {
            'question': f"Calculate: {num1} × {num2}",
            'correct_answer': str(answer),
            'answer_value': answer,
            'type': 'Short Answer'
        }
    
    def _generate_fraction_questions(self) -> Dict:
        """Generate fraction questions"""
        questions_types = [
            'addition', 'subtraction', 'simplification', 'comparison'
        ]
        question_type = random.choice(questions_types)
        
        if question_type == 'addition':
            # Simple fraction addition with same denominator
            denom = random.choice([2, 3, 4, 5, 6, 8, 10])
            num1 = random.randint(1, denom-1)
            num2 = random.randint(1, denom-1)
            if num1 + num2 >= denom:
                num2 = denom - num1 - 1
            
            answer_num = num1 + num2
            
            return {
                'question': f"What is {num1}/{denom} + {num2}/{denom}?",
                'correct_answer': f"{answer_num}/{denom}",
                'answer_value': f"{answer_num}/{denom}",
                'type': 'Short Answer'
            }
        
        elif question_type == 'simplification':
            # Generate a fraction that can be simplified
            common_factor = random.choice([2, 3, 4, 5])
            simple_num = random.randint(1, 10)
            simple_denom = random.randint(simple_num + 1, 15)
            
            num = simple_num * common_factor
            denom = simple_denom * common_factor
            
            return {
                'question': f"Simplify the fraction {num}/{denom}",
                'correct_answer': f"{simple_num}/{simple_denom}",
                'answer_value': f"{simple_num}/{simple_denom}",
                'type': 'Short Answer'
            }
    
    def _generate_basic_arithmetic(self) -> Dict:
        """Generate basic arithmetic questions"""
        operations = ['+', '-', '*', '÷']
        operation = random.choice(operations)
        
        if operation == '+':
            num1 = random.randint(10, 999)
            num2 = random.randint(10, 999)
            answer = num1 + num2
            question = f"{num1} + {num2}"
        elif operation == '-':
            num1 = random.randint(50, 999)
            num2 = random.randint(10, num1 - 1)
            answer = num1 - num2
            question = f"{num1} - {num2}"
        elif operation == '*':
            num1 = random.randint(2, 50)
            num2 = random.randint(2, 20)
            answer = num1 * num2
            question = f"{num1} × {num2}"
        else:  # division
            answer = random.randint(2, 50)
            num2 = random.randint(2, 20)
            num1 = answer * num2
            question = f"{num1} ÷ {num2}"
        
        return {
            'question': f"Calculate: {question}",
            'correct_answer': str(answer),
            'answer_value': answer,
            'type': 'Short Answer'
        }
    
    # English Question Generators
    def _generate_parts_of_speech(self) -> Dict:
        """Generate parts of speech questions"""
        words_data = [
            ('run', 'verb'), ('beautiful', 'adjective'), ('quickly', 'adverb'),
            ('book', 'noun'), ('and', 'conjunction'), ('in', 'preposition'),
            ('happy', 'adjective'), ('cat', 'noun'), ('jump', 'verb'),
            ('slowly', 'adverb'), ('but', 'conjunction'), ('under', 'preposition')
        ]
        
        word, correct_pos = random.choice(words_data)
        
        # Generate options
        all_pos = ['noun', 'verb', 'adjective', 'adverb', 'conjunction', 'preposition']
        options = [correct_pos]
        while len(options) < 4:
            wrong_pos = random.choice(all_pos)
            if wrong_pos not in options:
                options.append(wrong_pos)
        
        random.shuffle(options)
        correct_option = chr(ord('a') + options.index(correct_pos))
        
        return {
            'question': f"What part of speech is the word '{word}'?",
            'options': [f"{chr(ord('a') + i)}) {opt}" for i, opt in enumerate(options)],
            'correct_answer': correct_option,
            'answer_value': correct_pos,
            'type': 'MCQ'
        }
    
    def _generate_verb_forms(self) -> Dict:
        """Generate verb form questions"""
        verbs_data = [
            ('go', 'went', 'gone'), ('eat', 'ate', 'eaten'), ('see', 'saw', 'seen'),
            ('take', 'took', 'taken'), ('give', 'gave', 'given'), ('write', 'wrote', 'written'),
            ('sing', 'sang', 'sung'), ('ring', 'rang', 'rung'), ('swim', 'swam', 'swum')
        ]
        
        present, past, past_participle = random.choice(verbs_data)
        
        question_types = [
            (f"What is the past tense of '{present}'?", past),
            (f"What is the past participle of '{present}'?", past_participle),
            (f"What is the present tense of '{past}'?", present)
        ]
        
        question, answer = random.choice(question_types)
        
        return {
            'question': question,
            'correct_answer': answer,
            'answer_value': answer,
            'type': 'Short Answer'
        }
    
    def _generate_sentence_correction(self) -> Dict:
        """Generate sentence correction questions"""
        incorrect_sentences = [
            ("She don't like apples", "She doesn't like apples"),
            ("I has finished my work", "I have finished my work"),
            ("They was playing football", "They were playing football"),
            ("He go to school daily", "He goes to school daily"),
            ("We doesn't understand this", "We don't understand this")
        ]
        
        incorrect, correct = random.choice(incorrect_sentences)
        
        return {
            'question': f"Correct this sentence: '{incorrect}'",
            'correct_answer': correct,
            'answer_value': correct,
            'type': 'Short Answer'
        }
    
    def _generate_synonyms_antonyms(self) -> Dict:
        """Generate synonyms and antonyms questions"""
        words_data = [
            ('happy', 'joyful', 'sad'),
            ('big', 'large', 'small'),
            ('fast', 'quick', 'slow'),
            ('bright', 'shiny', 'dark'),
            ('hot', 'warm', 'cold'),
            ('easy', 'simple', 'difficult')
        ]
        
        word, synonym, antonym = random.choice(words_data)
        
        question_types = [
            (f"What is a synonym for '{word}'?", synonym),
            (f"What is an antonym for '{word}'?", antonym)
        ]
        
        question, answer = random.choice(question_types)
        
        return {
            'question': question,
            'correct_answer': answer,
            'answer_value': answer,
            'type': 'Short Answer'
        }
    
    # Science Question Generators
    def _generate_general_science(self) -> Dict:
        """Generate general science questions"""
        questions_data = [
            ("How many bones are there in an adult human body?", "206", ["206", "204", "208", "210"]),
            ("What is the hardest natural substance?", "Diamond", ["Diamond", "Gold", "Iron", "Steel"]),
            ("Which planet is closest to the Sun?", "Mercury", ["Mercury", "Venus", "Earth", "Mars"]),
            ("What gas do plants absorb from the atmosphere?", "Carbon dioxide", ["Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"]),
            ("How many chambers does a human heart have?", "4", ["4", "3", "2", "5"]),
            ("What is the chemical symbol for water?", "H2O", ["H2O", "CO2", "O2", "NaCl"])
        ]
        
        question, answer, options = random.choice(questions_data)
        random.shuffle(options)
        correct_option = chr(ord('a') + options.index(answer))
        
        return {
            'question': question,
            'options': [f"{chr(ord('a') + i)}) {opt}" for i, opt in enumerate(options)],
            'correct_answer': correct_option,
            'answer_value': answer,
            'type': 'MCQ'
        }
    
    def _generate_biology_basics(self) -> Dict:
        """Generate basic biology questions"""
        questions_data = [
            ("What is the basic unit of life?", "Cell", ["Cell", "Tissue", "Organ", "Atom"]),
            ("Which part of the plant conducts photosynthesis?", "Leaves", ["Leaves", "Roots", "Stem", "Flowers"]),
            ("What do we call animals that eat only plants?", "Herbivores", ["Herbivores", "Carnivores", "Omnivores", "Decomposers"]),
            ("Which organ in the human body produces insulin?", "Pancreas", ["Pancreas", "Liver", "Kidney", "Heart"]),
            ("What is the largest organ of the human body?", "Skin", ["Skin", "Liver", "Brain", "Lungs"])
        ]
        
        question, answer, options = random.choice(questions_data)
        random.shuffle(options)
        correct_option = chr(ord('a') + options.index(answer))
        
        return {
            'question': question,
            'options': [f"{chr(ord('a') + i)}) {opt}" for i, opt in enumerate(options)],
            'correct_answer': correct_option,
            'answer_value': answer,
            'type': 'MCQ'
        }
    
    def _generate_physics_basics(self) -> Dict:
        """Generate basic physics questions"""
        questions_data = [
            ("What is the speed of light in vacuum?", "300,000 km/s", ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"]),
            ("What force pulls objects toward Earth?", "Gravity", ["Gravity", "Magnetism", "Friction", "Tension"]),
            ("What is the unit of electric current?", "Ampere", ["Ampere", "Volt", "Watt", "Ohm"]),
            ("Which color has the longest wavelength?", "Red", ["Red", "Blue", "Green", "Violet"]),
            ("What happens to the volume of a gas when heated?", "Increases", ["Increases", "Decreases", "Remains same", "Becomes zero"])
        ]
        
        question, answer, options = random.choice(questions_data)
        random.shuffle(options)
        correct_option = chr(ord('a') + options.index(answer))
        
        return {
            'question': question,
            'options': [f"{chr(ord('a') + i)}) {opt}" for i, opt in enumerate(options)],
            'correct_answer': correct_option,
            'answer_value': answer,
            'type': 'MCQ'
        }
    
    def _generate_chemistry_basics(self) -> Dict:
        """Generate basic chemistry questions"""
        questions_data = [
            ("What is the chemical symbol for gold?", "Au", ["Au", "Ag", "Go", "Gd"]),
            ("How many elements are in the periodic table?", "118", ["118", "108", "128", "98"]),
            ("What is the most abundant gas in Earth's atmosphere?", "Nitrogen", ["Nitrogen", "Oxygen", "Carbon dioxide", "Argon"]),
            ("What is the pH of pure water?", "7", ["7", "6", "8", "0"]),
            ("Which gas is produced when metals react with acids?", "Hydrogen", ["Hydrogen", "Oxygen", "Nitrogen", "Carbon dioxide"])
        ]
        
        question, answer, options = random.choice(questions_data)
        random.shuffle(options)
        correct_option = chr(ord('a') + options.index(answer))
        
        return {
            'question': question,
            'options': [f"{chr(ord('a') + i)}) {opt}" for i, opt in enumerate(options)],
            'correct_answer': correct_option,
            'answer_value': answer,
            'type': 'MCQ'
        }

    def get_timer_duration(self, num_questions: int) -> int:
        """Get timer duration in seconds based on number of questions"""
        timer_mapping = {
            25: 5 * 60,   # 5 minutes
            50: 10 * 60,  # 10 minutes 
            75: 15 * 60,  # 15 minutes
            100: 20 * 60  # 20 minutes
        }
        return timer_mapping.get(num_questions, 5 * 60)  # Default 5 minutes
    
    def calculate_score(self, user_answers: Dict, correct_answers: List[Dict]) -> Dict:
        """Calculate the score for rapid fire test with detailed feedback"""
        total_questions = len(correct_answers)
        correct_count = 0
        wrong_answers_details = []
        
        for i, question in enumerate(correct_answers):
            user_answer = user_answers.get(f'q_{i}', '').strip().lower()
            
            if question['type'] == 'MCQ':
                correct_answer = question['correct_answer'].lower()
                is_correct = user_answer == correct_answer
                if is_correct:
                    correct_count += 1
                else:
                    # Find the correct option text
                    correct_option_text = question.get('answer_value', 'Unknown')
                    if 'options' in question:
                        for option in question['options']:
                            if option.startswith(question['correct_answer'].upper() + ')'):
                                correct_option_text = option.split(') ', 1)[1] if ') ' in option else option
                                break
                    
                    # Fallback if still empty
                    if not correct_option_text:
                        correct_option_text = question.get('answer_value', 'Answer not found')
                    
                    # Find user's selected option text
                    user_option_text = ""
                    if user_answer and 'options' in question:
                        for option in question['options']:
                            if option.startswith(user_answer.upper() + ')'):
                                user_option_text = option.split(') ', 1)[1]
                                break
                    
                    wrong_answers_details.append({
                        'question_number': i + 1,
                        'question': question['question'],
                        'user_answer': user_option_text or user_answer,
                        'correct_answer': correct_option_text,
                        'type': 'MCQ'
                    })
            else:  # Short Answer
                correct_answer = str(question['answer_value']).strip().lower()
                is_correct = user_answer == correct_answer
                if is_correct:
                    correct_count += 1
                else:
                    wrong_answers_details.append({
                        'question_number': i + 1,
                        'question': question['question'],
                        'user_answer': user_answer,
                        'correct_answer': str(question['answer_value']),
                        'type': 'Short Answer'
                    })
        
        percentage = (correct_count / total_questions) * 100
        
        # Determine grade
        if percentage >= 90:
            grade = 'A+'
        elif percentage >= 80:
            grade = 'A'
        elif percentage >= 70:
            grade = 'B+'
        elif percentage >= 60:
            grade = 'B'
        elif percentage >= 50:
            grade = 'C'
        else:
            grade = 'F'
        
        return {
            'total_questions': total_questions,
            'correct_answers': correct_count,
            'wrong_answers': total_questions - correct_count,
            'percentage': round(percentage, 2),
            'grade': grade,
            'wrong_answers_details': wrong_answers_details,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_rapid_fire_result(self, student_name: str, subject: str, result: Dict) -> str:
        """Save rapid fire test result to file"""
        try:
            # Create reports directory structure
            reports_dir = "data/reports/rapid_fire"
            os.makedirs(reports_dir, exist_ok=True)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{student_name}_{subject}_rapidfire_{timestamp}.json"
            filepath = os.path.join(reports_dir, filename)
            
            # Add metadata
            result['student_name'] = student_name
            result['subject'] = subject
            result['test_type'] = 'Rapid Fire'
            result['date'] = datetime.now().isoformat()
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            return filepath
            
        except Exception as e:
            print(f"Error saving rapid fire result: {str(e)}")
            return None
    
    def _generate_basic_arithmetic(self):
        """Fallback method for basic arithmetic"""
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        operation = random.choice(['+', '-', '×'])
        
        if operation == '+':
            answer = num1 + num2
            question = f"Calculate: {num1} + {num2}"
        elif operation == '-':
            answer = num1 - num2 if num1 >= num2 else num2 - num1
            question = f"Calculate: {max(num1, num2)} - {min(num1, num2)}"
        else:  # multiplication
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)
            answer = num1 * num2
            question = f"Calculate: {num1} × {num2}"
        
        return {
            'question': question,
            'correct_answer': str(answer),
            'answer_value': answer,
            'type': 'Short Answer'
        }
    
    def _generate_parts_of_speech(self):
        """Fallback method for parts of speech"""
        words_pos = [
            ("run", "Verb"), ("beautiful", "Adjective"), ("quickly", "Adverb"),
            ("dog", "Noun"), ("and", "Conjunction"), ("in", "Preposition"),
            ("happy", "Adjective"), ("sing", "Verb"), ("table", "Noun"),
            ("very", "Adverb"), ("blue", "Adjective"), ("jump", "Verb")
        ]
        
        word, correct_pos = random.choice(words_pos)
        
        # Create wrong options
        all_pos = ["Noun", "Verb", "Adjective", "Adverb", "Preposition", "Conjunction"]
        wrong_options = [pos for pos in all_pos if pos != correct_pos]
        options = [correct_pos] + random.sample(wrong_options, 3)
        random.shuffle(options)
        
        return {
            'question': f'What part of speech is the word "{word}"?',
            'options': [f"{chr(65+i)}) {opt}" for i, opt in enumerate(options)],
            'correct_answer': chr(65 + options.index(correct_pos)),
            'type': 'MCQ'
        }
    
    def _generate_general_science(self):
        """Fallback method for general science"""
        science_facts = [
            ("Water boils at what temperature?", "100°C", ["50°C", "100°C", "150°C", "200°C"]),
            ("How many legs does a spider have?", "8", ["6", "8", "10", "12"]),
            ("What gas do plants release during photosynthesis?", "Oxygen", ["Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"]),
            ("The Earth has how many moons?", "1", ["0", "1", "2", "3"]),
            ("What is the hardest natural substance?", "Diamond", ["Gold", "Iron", "Diamond", "Silver"])
        ]
        
        question, correct, all_options = random.choice(science_facts)
        random.shuffle(all_options)
        
        return {
            'question': question,
            'options': [f"{chr(65+i)}) {opt}" for i, opt in enumerate(all_options)],
            'correct_answer': chr(65 + all_options.index(correct)),
            'type': 'MCQ'
        }