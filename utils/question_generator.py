import os
import random
import re
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from utils.pdf_processor import PDFProcessor

class QuestionGenerator:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.question_templates = {
            "Multiple Choice": [
                "Which of the following best describes {}?",
                "What is the main characteristic of {}?",
                "In the context of {}, which statement is correct?",
                "The primary function of {} is:",
                "Which of these is associated with {}?"
            ],
            "Short Answer": [
                "Define {} and explain its importance.",
                "What are the key features of {}?",
                "Explain the concept of {} in your own words.",
                "List three important points about {}.",
                "How does {} work? Explain briefly."
            ],
            "Long Answer": [
                "Discuss the significance of {} with examples.",
                "Explain the process of {} in detail.",
                "Write a detailed note on {}.",
                "Analyze the role of {} and its applications.",
                "Describe {} and its impact with suitable examples."
            ],
            "Fill in the Blanks": [
                "The main component of {} is _______.",
                "In {}, the process involves _______.",
                "{} is important because _______.",
                "The result of {} leads to _______.",
                "When studying {}, we observe _______."
            ]
        }
    
    def get_available_subjects_and_chapters(self, class_level):
        """
        Get list of available subjects and chapters from uploaded textbooks for a class
        
        Args:
            class_level (str): Class level (e.g., "7", "8", "9")
            
        Returns:
            dict: Dictionary with subject -> {chapters, class_info} mapping
        """
        try:
            textbook_path = f"data/grades/grade_{class_level}/textbooks"
            metadata_path = os.path.join(textbook_path, "metadata")
            
            subjects_data = {}
            
            if not os.path.exists(metadata_path):
                return subjects_data
            
            # Read all metadata files
            for metadata_file in os.listdir(metadata_path):
                if metadata_file.endswith('_metadata.json'):
                    filepath = os.path.join(metadata_path, metadata_file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        
                        # Get detected subject and class from metadata
                        detected_subject = metadata.get('detected_subject', 'General Studies')
                        detected_class = metadata.get('detected_class', f'Class {class_level}')
                        
                        chapters = metadata.get('chapters', [])
                        if chapters:
                            if detected_subject not in subjects_data:
                                subjects_data[detected_subject] = {
                                    'chapters': [],
                                    'class_info': detected_class,
                                    'source_files': []
                                }
                            
                            # Add chapters with enhanced info
                            for chapter in chapters:
                                chapter_info = {
                                    'number': chapter.get('number', 'N/A'),
                                    'title': chapter.get('title', 'Unknown'),
                                    'start_page': chapter.get('start_page', 'N/A'),
                                    'content': chapter.get('content', ''),
                                    'source_file': metadata.get('source_file', '')
                                }
                                subjects_data[detected_subject]['chapters'].append(chapter_info)
                            
                            # Track source files
                            source_file = metadata.get('source_file', '')
                            if source_file not in subjects_data[detected_subject]['source_files']:
                                subjects_data[detected_subject]['source_files'].append(source_file)
                    
                    except Exception as e:
                        print(f"Error reading metadata file {metadata_file}: {e}")
                        continue
            
            return subjects_data
            
        except Exception as e:
            print(f"Error getting available subjects and chapters: {str(e)}")
            return {}
    
    def extract_facts_and_concepts(self, text_content):
        """
        Extract actual facts, definitions, and concepts from textbook content
        
        Args:
            text_content (str): Text content from textbook
            
        Returns:
            dict: Dictionary containing facts, definitions, and concepts
        """
        try:
            sentences = re.split(r'[.!?]+', text_content)
            
            facts = []
            definitions = []
            processes = []
            examples = []
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) < 15:
                    continue
                
                # Extract definitions (sentences with "is", "are", "refers to", "means")
                if any(pattern in sentence.lower() for pattern in [' is ', ' are ', ' refers to ', ' means ', ' defined as ']):
                    definitions.append(sentence)
                
                # Extract processes (sentences with process indicators)
                elif any(pattern in sentence.lower() for pattern in ['process', 'steps', 'procedure', 'method']):
                    processes.append(sentence)
                
                # Extract examples
                elif any(pattern in sentence.lower() for pattern in ['example', 'for instance', 'such as', 'like']):
                    examples.append(sentence)
                
                # General facts (other informative sentences)
                elif len(sentence) > 30 and not sentence.startswith('Chapter'):
                    facts.append(sentence)
            
            return {
                'definitions': definitions[:10],
                'processes': processes[:5],
                'examples': examples[:8],
                'facts': facts[:15]
            }
            
        except Exception as e:
            print(f"Error extracting facts and concepts: {str(e)}")
            return {'definitions': [], 'processes': [], 'examples': [], 'facts': []}
    
    def generate_question_from_content(self, question_type, content_data, marks):
        """
        Generate a question based on actual textbook content
        
        Args:
            question_type (str): Type of question
            content_data (dict): Extracted facts, definitions, processes, examples
            marks (int): Marks for the question
            
        Returns:
            dict: Generated question with actual content
        """
        try:
            question = {
                'type': question_type,
                'marks': marks,
                'question': '',
                'source_content': ''
            }
            
            if question_type == "Multiple Choice":
                # Use definitions for MCQ
                if content_data['definitions']:
                    definition = random.choice(content_data['definitions'])
                    # Extract the concept being defined
                    concept_match = re.search(r'^(.+?)\s+(?:is|are|refers to|means)', definition, re.IGNORECASE)
                    if concept_match:
                        concept = concept_match.group(1).strip()
                        # Extract the definition part
                        definition_part = definition.replace(concept, '').strip()
                        definition_part = re.sub(r'^(?:is|are|refers to|means)\s*', '', definition_part, flags=re.IGNORECASE)
                        
                        question['question'] = f"What is {concept}?"
                        question['correct_answer'] = definition_part
                        question['options'] = self._generate_mcq_options(definition_part, concept)
                        question['source_content'] = definition
                    else:
                        return None
                else:
                    return None
            
            elif question_type == "Short Answer":
                # Use processes or facts
                if content_data['processes']:
                    process = random.choice(content_data['processes'])
                    question['question'] = f"Explain the process mentioned in: '{process[:50]}...'"
                    question['source_content'] = process
                elif content_data['facts']:
                    fact = random.choice(content_data['facts'])
                    # Create question from fact
                    question['question'] = f"Explain: {fact[:60]}..."
                    question['source_content'] = fact
                else:
                    return None
            
            elif question_type == "Long Answer":
                # Use comprehensive content
                if content_data['definitions'] and content_data['facts']:
                    definition = random.choice(content_data['definitions'])
                    concept_match = re.search(r'^(.+?)\s+(?:is|are|refers to|means)', definition, re.IGNORECASE)
                    if concept_match:
                        concept = concept_match.group(1).strip()
                        question['question'] = f"Write a detailed note on {concept}. Include its definition, characteristics, and examples."
                        question['source_content'] = definition
                    else:
                        return None
                else:
                    return None
            
            elif question_type == "Fill in the Blanks":
                # Create fill-in-the-blank from facts
                if content_data['facts']:
                    fact = random.choice(content_data['facts'])
                    # Find key terms to blank out
                    words = fact.split()
                    if len(words) > 10:
                        # Blank out important words (nouns, adjectives)
                        important_words = [w for w in words if len(w) > 4 and w[0].isupper()]
                        if important_words:
                            word_to_blank = random.choice(important_words)
                            blanked_sentence = fact.replace(word_to_blank, '_______', 1)
                            question['question'] = blanked_sentence
                            question['answer'] = word_to_blank
                            question['source_content'] = fact
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
            
            return question if question['question'] else None
            
        except Exception as e:
            print(f"Error generating question from content: {str(e)}")
            return None
    
    def _generate_mcq_options(self, correct_answer, concept):
        """Generate plausible multiple choice options"""
        try:
            # Create variations of the correct answer for distractors
            options = [correct_answer]  # Correct answer
            
            # Generate plausible wrong answers
            base_terms = ["process", "method", "system", "structure", "property", "characteristic"]
            
            for i in range(3):  # 3 wrong options
                if i == 0:
                    # Slightly modify the correct answer
                    wrong = correct_answer.replace("temporary", "permanent").replace("permanent", "temporary")
                    wrong = wrong.replace("physical", "chemical").replace("chemical", "physical")
                    options.append(wrong if wrong != correct_answer else f"A different type of {random.choice(base_terms)}")
                elif i == 1:
                    # Create opposite or contrasting answer
                    options.append(f"The opposite of what {concept.lower()} represents")
                else:
                    # Generic plausible option
                    options.append(f"A {random.choice(base_terms)} related to {concept.lower()}")
            
            # Shuffle and assign letters
            random.shuffle(options)
            lettered_options = []
            for idx, option in enumerate(options):
                letter = chr(ord('a') + idx)
                lettered_options.append(f"{letter}) {option}")
            
            return lettered_options
            
        except Exception as e:
            print(f"Error generating MCQ options: {str(e)}")
            return [
                "a) Option A",
                "b) Option B", 
                "c) Option C",
                "d) Option D"
            ]
    
    def generate_paper(self, class_level, total_marks, subject, duration=2, question_types=None, selected_chapters=None):
        """
        Generate a complete question paper using actual textbook content
        
        Args:
            class_level (str): Class level (e.g., "7", "8", "9")
            total_marks (int): Total marks for the paper
            subject (str): Subject name
            duration (int): Exam duration in hours
            question_types (list): Types of questions to include
            selected_chapters (list): Specific chapters to use (optional)
            
        Returns:
            str: Generated question paper content
        """
        try:
            if question_types is None:
                question_types = ["Multiple Choice", "Short Answer", "Long Answer"]
            
            # Get available subjects and chapters
            subjects_data = self.get_available_subjects_and_chapters(class_level)
            
            if subject not in subjects_data:
                print(f"No textbook found for subject: {subject}")
                return None
            
            subject_info = subjects_data[subject]
            available_chapters = subject_info['chapters']
            class_info = subject_info['class_info']
            
            # Filter chapters if specific ones are selected
            if selected_chapters and "All Chapters" not in selected_chapters:
                filtered_chapters = []
                for chapter in available_chapters:
                    chapter_name = f"Chapter {chapter['number']}: {chapter['title']}"
                    if chapter_name in selected_chapters:
                        filtered_chapters.append(chapter)
                chapters_to_use = filtered_chapters
            else:
                chapters_to_use = available_chapters
            
            if not chapters_to_use:
                print("No chapters available for question generation")
                return None
            
            # Extract content and analyze from selected chapters
            combined_content = ""
            
            for chapter in chapters_to_use:
                chapter_content = chapter.get('content', '')
                combined_content += chapter_content + "\n"
            
            # Extract actual facts, definitions, and concepts from textbook content
            if combined_content.strip():
                content_data = self.extract_facts_and_concepts(combined_content)
            else:
                print("No textbook content found for question generation")
                return None
            
            # Check if we have enough content for question generation
            total_content_items = (len(content_data['definitions']) + 
                                 len(content_data['facts']) + 
                                 len(content_data['processes']) + 
                                 len(content_data['examples']))
            
            if total_content_items < 5:
                print("Insufficient textbook content for quality question generation")
                return None
            
            # Distribute marks among question types
            mark_distribution = self._distribute_marks(total_marks, question_types)
            
            # Generate questions using actual textbook content
            questions = []
            question_number = 1
            
            for question_type, allocated_marks in mark_distribution.items():
                if question_type in question_types:
                    questions_for_type = self._calculate_questions_needed(question_type, allocated_marks)
                    marks_per_question = allocated_marks // questions_for_type
                    
                    for _ in range(questions_for_type):
                        question = self.generate_question_from_content(question_type, content_data, marks_per_question)
                        if question:
                            question['number'] = question_number
                            questions.append(question)
                            question_number += 1
            
            # Format the question paper with actual class info
            paper_content = self._format_question_paper(
                questions, subject, class_info, total_marks, duration, chapters_to_use
            )
            
            return paper_content
            
        except Exception as e:
            print(f"Error generating paper: {str(e)}")
            return None
    
    def _get_default_topics(self, subject):
        """Get default topics for a subject if no textbook content is available"""
        default_topics = {
            "Science": ["Matter", "Energy", "Force", "Motion", "Light", "Sound", "Heat", "Plants", "Animals"],
            "Mathematics": ["Numbers", "Algebra", "Geometry", "Statistics", "Probability", "Fractions", "Decimals"],
            "English": ["Grammar", "Vocabulary", "Reading", "Writing", "Literature", "Poetry", "Prose"],
            "Social Studies (SST)": ["History", "Geography", "Civics", "Culture", "Society", "Government"]
        }
        
        return default_topics.get(subject, [subject, "General Knowledge", "Concepts", "Principles", "Applications"])
    
    def _format_question_paper(self, questions, subject, class_info, total_marks, duration, chapters_used):
        """Format questions into a proper question paper with chapter information"""
        try:
            # Create chapter info string
            if len(chapters_used) > 3:
                chapter_info = f"Chapters: {chapters_used[0]['number']}-{chapters_used[-1]['number']}"
            else:
                chapter_names = [f"Ch{ch['number']}" for ch in chapters_used[:3]]
                chapter_info = f"Chapters: {', '.join(chapter_names)}"
                if len(chapters_used) > 3:
                    chapter_info += f" and {len(chapters_used)-3} more"
            
            paper = f"""
{subject.upper()}
{class_info}
Time: {duration} hours                                                     Maximum Marks: {total_marks}

SYLLABUS: {chapter_info}

INSTRUCTIONS:
1. All questions are compulsory.
2. Read all questions carefully before answering.
3. Write your answers clearly and legibly.
4. Use black or blue pen for writing.

---

"""
            
            # Group questions by type
            question_groups = {}
            for question in questions:
                q_type = question['type']
                if q_type not in question_groups:
                    question_groups[q_type] = []
                question_groups[q_type].append(question)
            
            # Add questions to paper
            section_number = 1
            for question_type, type_questions in question_groups.items():
                paper += f"SECTION {section_number}: {question_type.upper()}\n\n"
                
                for question in type_questions:
                    paper += f"Q{question['number']}. {question['question']} ({question['marks']} marks)\n"
                    
                    if question_type == "Multiple Choice" and 'options' in question:
                        for option in question['options']:
                            paper += f"    {option}\n"
                    
                    if question_type == "Fill in the Blanks" and 'answer' in question:
                        # For internal reference, don't show answer in question paper
                        pass
                    
                    paper += "\n"
                
                paper += "\n"
                section_number += 1
            
            return paper
            
        except Exception as e:
            print(f"Error formatting paper: {str(e)}")
            return "Error generating question paper format"
    
    def _distribute_marks(self, total_marks, question_types):
        """Distribute total marks among different question types"""
        distribution = {}
        
        if "Multiple Choice" in question_types:
            distribution["Multiple Choice"] = int(total_marks * 0.3)
        if "Short Answer" in question_types:
            distribution["Short Answer"] = int(total_marks * 0.3)
        if "Long Answer" in question_types:
            distribution["Long Answer"] = int(total_marks * 0.4)
        if "Fill in the Blanks" in question_types:
            distribution["Fill in the Blanks"] = int(total_marks * 0.2)
        
        # Adjust to match total marks exactly
        current_total = sum(distribution.values())
        if current_total < total_marks:
            # Add remaining marks to the first question type
            first_type = list(distribution.keys())[0]
            distribution[first_type] += (total_marks - current_total)
        
        return distribution
    
    def _calculate_questions_needed(self, question_type, allocated_marks):
        """Calculate number of questions needed for a question type"""
        marks_per_question = {
            "Multiple Choice": 1,
            "Fill in the Blanks": 1,
            "Short Answer": 3,
            "Long Answer": 5
        }
        
        default_marks = marks_per_question.get(question_type, 2)
        return max(1, allocated_marks // default_marks)
    
    def create_pdf(self, question_paper_content, subject, class_level, total_marks):
        """Create PDF version of the question paper"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{subject}_Class{class_level}_{total_marks}marks_{timestamp}.pdf"
            filepath = os.path.join("data/question_papers", filename)
            
            # Ensure directory exists
            os.makedirs("data/question_papers", exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Split content into lines and convert to paragraphs
            lines = question_paper_content.split('\n')
            for line in lines:
                if line.strip():
                    # Determine style based on content
                    if line.isupper() and len(line) < 50:
                        # Headers
                        p = Paragraph(line, styles['Title'])
                    elif line.startswith('SECTION'):
                        p = Paragraph(line, styles['Heading2'])
                    elif line.startswith('Q'):
                        p = Paragraph(line, styles['Normal'])
                    else:
                        p = Paragraph(line, styles['Normal'])
                    story.append(p)
                else:
                    story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            return filepath
            
        except Exception as e:
            print(f"Error creating PDF: {str(e)}")
            return None