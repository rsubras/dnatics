import streamlit as st
import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

# Create necessary directories
def setup_directories():
    directories = [
        "data/grades/grade_7/textbooks",
        "data/grades/grade_7/question_papers", 
        "data/grades/grade_7/sample_answers",
        "data/grades/grade_8/textbooks",
        "data/grades/grade_8/question_papers",
        "data/grades/grade_8/sample_answers",
        "data/grades/grade_9/textbooks",
        "data/grades/grade_9/question_papers",
        "data/grades/grade_9/sample_answers",
        "data/question_papers",
        "data/evaluated_sheets"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

# Initialize session state
def initialize_session_state():
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}

def main():
    setup_directories()
    initialize_session_state()
    
    st.set_page_config(
        page_title="SmartEduQuest",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main title
    st.title("📚 SmartEduQuest - Educational Portal")
    st.markdown("### Question Generation and Answer Evaluation System")
    
    # Role selection
    if st.session_state.user_role is None:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👨‍🏫 Teacher Login", use_container_width=True, type="primary"):
                st.session_state.user_role = "teacher"
                st.rerun()
                
        with col2:
            if st.button("👨‍🎓 Student Login", use_container_width=True):
                st.session_state.user_role = "student"
                st.rerun()
    else:
        # Display current role and logout option
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"Logged in as: **{st.session_state.user_role.title()}**")
        with col2:
            if st.button("Logout"):
                st.session_state.user_role = None
                st.rerun()
        
        st.markdown("---")
        
        # Role-specific content
        if st.session_state.user_role == "teacher":
            show_teacher_interface()
        elif st.session_state.user_role == "student":
            show_student_interface()

def show_teacher_interface():
    st.header("👨‍🏫 Teacher Dashboard")
    
    tabs = st.tabs(["📤 Upload Materials", "📝 Generate Question Paper", "📊 Manage Files"])
    
    with tabs[0]:
        show_upload_interface()
    
    with tabs[1]:
        show_question_generation()
        
    with tabs[2]:
        show_file_management()

def show_student_interface():
    st.header("👨‍🎓 Student Dashboard")
    
    tabs = st.tabs(["📥 Download Question Papers", "📤 Submit Answer Sheet", "⚡ Rapid Fire Quiz", "📋 View Results"])
    
    with tabs[0]:
        show_question_download()
    
    with tabs[1]:
        show_answer_submission()
        
    with tabs[2]:
        show_rapid_fire_quiz()
        
    with tabs[3]:
        show_results()

def show_upload_interface():
    st.subheader("Upload Academic Materials")
    
    # Information about supported document types
    st.info("📋 **Supported Document Types:**\n"
           "• **Textbooks**: Use filename format Class7_Science.pdf for automatic metadata extraction\n"
           "• **Question Papers**: Text or image-based PDFs for reference\n"
           "• **Sample Answer Sheets**: Handwritten/scanned documents for evaluation training")
    
    # Class selection
    class_level = st.selectbox("Select Class", ["Class 7", "Class 8", "Class 9"])
    class_num = class_level.split()[-1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📚 Textbooks (PDF)")
        textbooks = st.file_uploader(
            "Upload textbook PDFs", 
            type=['pdf'], 
            accept_multiple_files=True,
            key="textbooks"
        )
        
        if textbooks:
            from utils.pdf_processor import PDFProcessor
            processor = PDFProcessor()
            
            for book in textbooks:
                # Save textbook
                save_path = f"data/grades/grade_{class_num}/textbooks/{book.name}"
                with open(save_path, "wb") as f:
                    f.write(book.read())
                
                # Process with metadata extraction
                with st.spinner(f"Processing {book.name}..."):
                    result = processor.extract_content_with_chapters(save_path)
                    if result:
                        st.success(f"✅ Processed: {book.name}")
                        st.write(f"📖 Found {len(result.get('chapters', []))} chapters")
                        
                        # Save metadata
                        metadata_dir = f"data/grades/grade_{class_num}/textbooks/metadata"
                        processor.save_textbook_metadata(save_path, result, metadata_dir)
                    else:
                        st.success(f"✅ Saved: {book.name}")
    
    with col2:
        st.markdown("##### 📄 Past Question Papers (PDF)")
        question_papers = st.file_uploader(
            "Upload past question papers", 
            type=['pdf'], 
            accept_multiple_files=True,
            key="past_papers"
        )
        
        if question_papers:
            for paper in question_papers:
                # Save question paper
                save_path = f"data/grades/grade_{class_num}/question_papers/{paper.name}"
                with open(save_path, "wb") as f:
                    f.write(paper.read())
                st.success(f"✅ Saved: {paper.name}")
    
    st.markdown("##### 📝 Sample Answer Sheets (PDF/Images)")
    sample_answers = st.file_uploader(
        "Upload 10-15 evaluated answer sheets", 
        type=['pdf', 'jpg', 'jpeg', 'png'], 
        accept_multiple_files=True,
        key="sample_answers"
    )
    
    if sample_answers:
        for answer in sample_answers:
            # Save sample answer
            save_path = f"data/grades/grade_{class_num}/sample_answers/{answer.name}"
            with open(save_path, "wb") as f:
                f.write(answer.read())
            st.success(f"✅ Saved: {answer.name}")

def show_question_generation():
    from utils.question_generator import QuestionGenerator
    import json
    
    st.subheader("📝 Generate Question Paper")
    
    generator = QuestionGenerator()
    
    col1, col2 = st.columns(2)
    
    with col1:
        class_level = st.selectbox("Select Class", ["Class 7", "Class 8", "Class 9"], key="gen_class")
        class_num = class_level.split()[-1]
        
        # Get available subjects from uploaded textbooks
        subjects_data = generator.get_available_subjects_and_chapters(class_num)
        available_subjects = list(subjects_data.keys()) if subjects_data else ["No textbooks uploaded"]
        
        if available_subjects and "No textbooks uploaded" not in available_subjects:
            subject = st.selectbox(
                "Select Subject", 
                available_subjects,
                key="subject_select"
            )
        else:
            st.warning(f"⚠️ No textbooks found for {class_level}. Please upload textbooks first.")
            subject = "No Subject"
            
        total_marks = st.selectbox("Total Marks", [25, 50, 100])
    
    with col2:
        question_types = st.multiselect(
            "Question Types",
            ["Multiple Choice", "Short Answer", "Long Answer", "Fill in the Blanks"],
            default=["Multiple Choice", "Short Answer", "Long Answer"]
        )
        
        # Chapter selection for available subject
        if subject != "No Subject" and subject in subjects_data:
            chapters = subjects_data[subject]['chapters']
            
            # Chapter selection multiselect
            chapter_options = ["All Chapters"] + [f"Chapter {ch['number']}: {ch['title']}" for ch in chapters]
            selected_chapters = st.multiselect(
                f"Select Chapters ({len(chapters)} available)",
                chapter_options,
                default=["All Chapters"],
                key="chapter_select"
            )
            
            # Show chapter info
            if chapters and "All Chapters" not in selected_chapters:
                st.info(f"📚 Selected {len(selected_chapters)} chapter(s)")
        else:
            selected_chapters = ["All Chapters"]
    
    if st.button("🔄 Generate Question Paper", type="primary"):
        if subject == "No Subject":
            st.error("⚠️ No textbooks found for this class. Please upload textbooks first.")
            return
        
        with st.spinner("Generating question paper from actual textbook content..."):
            question_paper = generator.generate_paper(
                class_level=class_num,
                total_marks=total_marks,
                question_types=question_types,
                subject=subject,
                selected_chapters=selected_chapters
            )
            
            if question_paper:
                st.success("✅ Question paper generated successfully!")
                
                # Show selected chapters info
                if subjects_data and subject in subjects_data:
                    if "All Chapters" not in selected_chapters:
                        st.info(f"📖 Questions generated from: {', '.join(selected_chapters)}")
                    else:
                        st.info(f"📚 Questions generated from all {len(subjects_data[subject]['chapters'])} chapters")
                
                # Display preview
                st.markdown("### 📋 Question Paper Preview")
                st.text_area("Preview", question_paper, height=300)
                
                # Ensure directory exists
                os.makedirs("data/question_papers", exist_ok=True)
                
                # Generate PDF
                pdf_path = generator.create_pdf(question_paper, subject, class_num, total_marks)
                
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download Question Paper (PDF)",
                            data=pdf_file.read(),
                            file_name=f"{subject}_Class{class_num}_{total_marks}marks.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.error("❌ Failed to generate PDF file.")
            else:
                st.error("❌ Failed to generate question paper. Please check if textbooks are uploaded.")

def show_file_management():
    st.subheader("📊 File Management")
    
    class_level = st.selectbox("Select Class to View", ["Class 7", "Class 8", "Class 9"], key="manage_class")
    class_num = class_level.split()[-1]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### 📚 Textbooks")
        textbook_path = f"data/grades/grade_{class_num}/textbooks"
        if os.path.exists(textbook_path):
            files = os.listdir(textbook_path)
            if files:
                for file in files:
                    if file.endswith('.pdf'):
                        st.text(f"📄 {file}")
            else:
                st.info("No textbooks uploaded")
        else:
            st.info("No textbooks uploaded")
    
    with col2:
        st.markdown("##### 📄 Question Papers")
        papers_path = f"data/grades/grade_{class_num}/question_papers"
        if os.path.exists(papers_path):
            files = os.listdir(papers_path)
            if files:
                for file in files:
                    st.text(f"📄 {file}")
            else:
                st.info("No question papers generated")
        else:
            st.info("No question papers generated")
    
    with col3:
        st.markdown("##### 📝 Sample Answers")
        answers_path = f"data/grades/grade_{class_num}/sample_answers"
        if os.path.exists(answers_path):
            files = os.listdir(answers_path)
            if files:
                for file in files:
                    st.text(f"📄 {file}")
            else:
                st.info("No sample answers uploaded")
        else:
            st.info("No sample answers uploaded")

def show_question_download():
    st.subheader("📥 Download Question Papers")
    
    class_level = st.selectbox("Select Class", ["Class 7", "Class 8", "Class 9"], key="download_class")
    class_num = class_level.split()[-1]
    
    # Check for available question papers
    papers_path = f"data/grades/grade_{class_num}/question_papers"
    global_papers_path = "data/question_papers"
    
    available_papers = []
    
    if os.path.exists(papers_path):
        for file in os.listdir(papers_path):
            if file.endswith('.pdf'):
                available_papers.append((file, papers_path))
    
    if os.path.exists(global_papers_path):
        for file in os.listdir(global_papers_path):
            if file.endswith('.pdf') and f"Class{class_num}" in file:
                available_papers.append((file, global_papers_path))
    
    if available_papers:
        st.markdown("### Available Question Papers")
        for paper_name, paper_path in available_papers:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(f"📄 {paper_name}")
            with col2:
                full_path = os.path.join(paper_path, paper_name)
                if os.path.exists(full_path):
                    with open(full_path, "rb") as file:
                        st.download_button(
                            label="Download",
                            data=file.read(),
                            file_name=paper_name,
                            mime="application/pdf",
                            key=f"download_{paper_name}"
                        )
    else:
        st.info(f"No question papers available for {class_level}")

def show_answer_submission():
    st.subheader("📤 Submit Answer Sheet")
    
    class_level = st.selectbox("Select Class", ["Class 7", "Class 8", "Class 9"], key="submit_class")
    subject = st.selectbox("Select Subject", ["Science", "Mathematics", "English", "Social Studies"])
    
    st.markdown("##### Upload Your Answer Sheet")
    answer_sheet = st.file_uploader(
        "Upload scanned/photographed answer sheet",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        key="answer_submission"
    )
    
    if answer_sheet:
        if st.button("🔍 Evaluate Answer Sheet", type="primary"):
            with st.spinner("Evaluating your answers..."):
                # Here you would integrate with answer evaluation logic
                st.success("✅ Answer sheet submitted for evaluation!")
                st.info("📊 Results will be available in the 'View Results' tab")

def show_rapid_fire_quiz():
    st.subheader("⚡ Rapid Fire Quiz")
    
    # Initialize session state for rapid fire
    if 'rf_questions' not in st.session_state:
        st.session_state.rf_questions = []
    if 'rf_current_question' not in st.session_state:
        st.session_state.rf_current_question = 0
    if 'rf_user_answers' not in st.session_state:
        st.session_state.rf_user_answers = {}
    if 'rf_test_started' not in st.session_state:
        st.session_state.rf_test_started = False
    if 'rf_test_completed' not in st.session_state:
        st.session_state.rf_test_completed = False
    if 'rf_start_time' not in st.session_state:
        st.session_state.rf_start_time = None
    if 'rf_timer_duration' not in st.session_state:
        st.session_state.rf_timer_duration = 0
    
    # Quiz setup section
    if not st.session_state.rf_test_started:
        st.markdown("### Configure Your Rapid Fire Quiz")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox(
                "Select Subject",
                ["Mathematics", "English", "Science"],
                key="rf_subject"
            )
        
        with col2:
            num_questions = st.selectbox(
                "Number of Questions",
                [25, 50, 75, 100],
                key="rf_num_questions"
            )
        
        # Show timer information
        timer_info = {
            25: "5 minutes",
            50: "10 minutes", 
            75: "15 minutes",
            100: "20 minutes"
        }
        
        st.info(f"⏱️ **Timer**: {timer_info[num_questions]} for {num_questions} questions")
        
        # Subject-specific information
        subject_info = {
            "Mathematics": "• Multiplication tables\n• Two-digit calculations\n• Fractions\n• Basic arithmetic",
            "English": "• Parts of speech\n• Verb forms\n• Sentence correction\n• Synonyms & antonyms",
            "Science": "• General science facts\n• Biology basics\n• Physics concepts\n• Chemistry fundamentals"
        }
        
        st.markdown(f"**Topics covered:**\n{subject_info[subject]}")
        
        # Student name input
        student_name = st.text_input("Enter Your Name", key="rf_student_name")
        
        if st.button("🚀 Start Rapid Fire Quiz", type="primary", key="start_quiz_with_name") and student_name:
            from utils.rapid_fire_generator import RapidFireGenerator
            
            generator = RapidFireGenerator()
            
            with st.spinner("Generating quiz questions..."):
                questions = generator.generate_rapid_fire_questions(subject, num_questions)
                
                if questions:
                    st.session_state.rf_questions = questions
                    st.session_state.rf_current_question = 0
                    st.session_state.rf_user_answers = {}
                    st.session_state.rf_test_started = True
                    st.session_state.rf_test_completed = False
                    st.session_state.rf_start_time = time.time()
                    st.session_state.rf_timer_duration = generator.get_timer_duration(num_questions)
                    st.session_state.rf_quiz_subject = subject
                    st.session_state.rf_quiz_student_name = student_name
                    st.rerun()
                else:
                    st.error("Failed to generate quiz questions. Please try again.")
        
        elif not student_name and st.button("🚀 Start Rapid Fire Quiz", type="primary", key="start_quiz_no_name"):
            st.warning("Please enter your name to start the quiz.")
    
    # Quiz in progress
    elif st.session_state.rf_test_started and not st.session_state.rf_test_completed:
        # Check if time is up
        elapsed_time = time.time() - st.session_state.rf_start_time
        remaining_time = st.session_state.rf_timer_duration - elapsed_time
        
        if remaining_time <= 0:
            # Time up - auto submit
            st.session_state.rf_test_completed = True
            st.rerun()
        
        # Timer display
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        
        # Create timer with color coding
        if remaining_time < 60:  # Last minute - red
            timer_color = "🔴"
        elif remaining_time < 300:  # Last 5 minutes - yellow
            timer_color = "🟡"
        else:
            timer_color = "🟢"
        
        st.markdown(f"### {timer_color} Time Remaining: {minutes:02d}:{seconds:02d}")
        
        # Progress bar
        progress = st.session_state.rf_current_question / len(st.session_state.rf_questions)
        st.progress(progress)
        st.markdown(f"**Question {st.session_state.rf_current_question + 1} of {len(st.session_state.rf_questions)}**")
        
        # Current question
        current_q = st.session_state.rf_questions[st.session_state.rf_current_question]
        
        st.markdown(f"### {current_q['question']}")
        
        if current_q['type'] == 'MCQ':
            # Multiple choice
            answer = st.radio(
                "Select your answer:",
                options=[opt.split(') ', 1)[1] for opt in current_q['options']],
                key=f"rf_q_{st.session_state.rf_current_question}"
            )
            
            # Convert back to letter format
            if answer:
                for opt in current_q['options']:
                    if opt.split(') ', 1)[1] == answer:
                        selected_letter = opt.split(') ', 1)[0]
                        break
        else:
            # Short answer
            answer = st.text_input(
                "Your answer:",
                key=f"rf_q_{st.session_state.rf_current_question}"
            )
            selected_letter = answer
        
        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.rf_current_question > 0:
                if st.button("⬅️ Previous", key="rf_prev_btn"):
                    st.session_state.rf_current_question -= 1
                    st.rerun()
        
        with col2:
            if st.button("⏭️ Skip", key="rf_skip_btn"):
                if st.session_state.rf_current_question < len(st.session_state.rf_questions) - 1:
                    st.session_state.rf_current_question += 1
                    st.rerun()
        
        with col3:
            if answer:
                if st.session_state.rf_current_question < len(st.session_state.rf_questions) - 1:
                    if st.button("➡️ Next", type="primary", key="rf_next_btn"):
                        st.session_state.rf_user_answers[f'q_{st.session_state.rf_current_question}'] = selected_letter
                        st.session_state.rf_current_question += 1
                        st.rerun()
                else:
                    if st.button("✅ Submit Quiz", type="primary", key="rf_submit_btn"):
                        st.session_state.rf_user_answers[f'q_{st.session_state.rf_current_question}'] = selected_letter
                        st.session_state.rf_test_completed = True
                        st.rerun()
        
        # Auto-refresh for timer (using placeholder for smooth updates)
        if 'rf_timer_placeholder' not in st.session_state:
            st.session_state.rf_timer_placeholder = st.empty()
        
        # Update timer every second
        st.session_state.rf_timer_placeholder.empty()
        time.sleep(1)
        st.rerun()
    
    # Quiz completed - show results
    elif st.session_state.rf_test_completed:
        st.markdown("### 🎉 Quiz Completed!")
        
        from utils.rapid_fire_generator import RapidFireGenerator
        generator = RapidFireGenerator()
        
        # Calculate score
        score_data = generator.calculate_score(
            st.session_state.rf_user_answers,
            st.session_state.rf_questions
        )
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Questions", score_data['total_questions'])
        
        with col2:
            st.metric("Correct Answers", score_data['correct_answers'])
        
        with col3:
            st.metric("Percentage", f"{score_data['percentage']}%")
        
        # Grade display with color
        grade_colors = {
            'A+': '🟢', 'A': '🟢', 'B+': '🟡', 'B': '🟡', 'C': '🟠', 'F': '🔴'
        }
        
        st.markdown(f"## {grade_colors.get(score_data['grade'], '⚪')} Grade: {score_data['grade']}")
        
        # Save result
        result_data = {
            **score_data,
            'subject': st.session_state.rf_quiz_subject,
            'student_name': st.session_state.rf_quiz_student_name,
            'questions': st.session_state.rf_questions,
            'user_answers': st.session_state.rf_user_answers
        }
        
        filepath = generator.save_rapid_fire_result(
            st.session_state.rf_quiz_student_name,
            st.session_state.rf_quiz_subject,
            result_data
        )
        
        if filepath:
            st.success("📊 Results saved to your report history!")
        
        # Reset button
        if st.button("🔄 Take Another Quiz", key="rf_reset_btn"):
            # Reset all session state
            for key in list(st.session_state.keys()):
                if key.startswith('rf_'):
                    del st.session_state[key]
            st.rerun()

def show_results():
    st.subheader("📋 View Results")
    
    # Regular question paper results
    st.markdown("### 📄 Question Paper Results")
    st.info("📊 **Evaluation Results**\n"
           "Your answer sheet evaluations will appear here once processing is complete.")
    
    # Rapid Fire results
    st.markdown("### ⚡ Rapid Fire Quiz History")
    
    # Check for rapid fire results
    rf_reports_dir = "data/reports/rapid_fire"
    if os.path.exists(rf_reports_dir):
        rf_files = [f for f in os.listdir(rf_reports_dir) if f.endswith('.json')]
        
        if rf_files:
            # Sort by timestamp (newest first)
            rf_files.sort(reverse=True)
            
            for rf_file in rf_files[:10]:  # Show last 10 results
                try:
                    with open(os.path.join(rf_reports_dir, rf_file), 'r') as f:
                        result = json.load(f)
                    
                    # Parse filename for display
                    parts = rf_file.replace('.json', '').split('_')
                    if len(parts) >= 4:
                        student = parts[0]
                        subject = parts[1]
                        timestamp = parts[3]
                        
                        # Format timestamp
                        try:
                            dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                            date_str = dt.strftime("%Y-%m-%d %H:%M")
                        except:
                            date_str = timestamp
                        
                        # Display result card
                        with st.expander(f"🎯 {subject} Quiz - {date_str} - Grade: {result.get('grade', 'N/A')}"):
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Questions", result.get('total_questions', 0))
                            with col2:
                                st.metric("Correct", result.get('correct_answers', 0))
                            with col3:
                                st.metric("Score", f"{result.get('percentage', 0)}%")
                            with col4:
                                st.metric("Grade", result.get('grade', 'N/A'))
                
                except Exception as e:
                    continue
        else:
            st.info("No rapid fire quiz results found. Take a quiz to see your history!")
    else:
        st.info("No rapid fire quiz results found. Take a quiz to see your history!")

if __name__ == "__main__":
    main()