import os
import json
import re
from datetime import datetime
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

class PDFProcessor:
    def __init__(self):
        self.chapter_patterns = [
            r'^Chapter\s+(\d+)[\s\.:]*(.+?)$',
            r'^Unit\s+(\d+)[\s\.:]*(.+?)$', 
            r'^Lesson\s+(\d+)[\s\.:]*(.+?)$',
        ]
    
    def extract_content_with_chapters(self, pdf_path):
        """
        Extract content from PDF with chapter detection and metadata
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            dict: Extracted content with chapters and metadata
        """
        try:
            if fitz is None:
                print("PyMuPDF not available, skipping PDF processing")
                return None
                
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            
            # Skip first 14 pages (intro/contents)
            start_page = 15 if total_pages > 14 else 1
            
            full_text = ""
            chapters = []
            current_chapter = None
            
            for page_num in range(start_page - 1, total_pages):
                page = doc[page_num]
                try:
                    page_text = page.get_text()
                except:
                    try:
                        page_text = page.get_text("text")
                    except:
                        page_text = str(page)
                full_text += page_text + "\n"
                
                # Detect chapters in page text (only at line beginnings)
                lines = page_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if len(line) < 5 or len(line) > 100:  # Skip very short or very long lines
                        continue
                        
                    for pattern in self.chapter_patterns:
                        match = re.match(pattern, line, re.IGNORECASE)
                        if match:
                            chapter_num = match.group(1)
                            chapter_title = match.group(2).strip()
                            
                            # Validate chapter number is reasonable (1-20)
                            if chapter_num.isdigit() and 1 <= int(chapter_num) <= 20:
                                # Save previous chapter if exists
                                if current_chapter:
                                    chapters.append(current_chapter)
                                
                                # Start new chapter
                                current_chapter = {
                                    'number': int(chapter_num),
                                    'title': chapter_title,
                                    'start_page': page_num + 1,
                                    'content': page_text
                                }
                                break
                    if current_chapter and current_chapter.get('start_page') == page_num + 1:
                        break  # Found a chapter on this page, stop looking
                
                # Add content to current chapter
                if current_chapter and not any(pattern in page_text for pattern in ['Chapter', 'Unit', 'Lesson']):
                    current_chapter['content'] += "\n" + page_text
            
            # Add last chapter
            if current_chapter:
                chapters.append(current_chapter)
            
            doc.close()
            
            return {
                'content': full_text,
                'chapters': chapters,
                'metadata': {
                    'total_pages': total_pages,
                    'content_start_page': start_page,
                    'document_type': 'text',
                    'extracted_with_ocr': False
                }
            }
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return None
    
    def save_textbook_metadata(self, pdf_path, metadata, output_dir):
        """
        Save extracted textbook metadata to JSON file with enhanced class/subject detection
        
        Args:
            pdf_path (str): Path to original PDF
            metadata (dict): Extracted metadata
            output_dir (str): Directory to save metadata
            
        Returns:
            str: Path to saved metadata file
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Create metadata filename
            pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
            metadata_path = os.path.join(output_dir, f"{pdf_name}_metadata.json")
            
            # Extract class and subject from filename
            filename = os.path.basename(pdf_path)
            class_info, subject_info = self._extract_class_subject_from_filename(filename)
            
            # Add enhanced file information
            metadata['source_file'] = filename
            metadata['extraction_date'] = datetime.now().isoformat()
            metadata['detected_class'] = class_info
            metadata['detected_subject'] = subject_info
            
            # Update metadata structure
            if 'metadata' not in metadata:
                metadata['metadata'] = {}
            metadata['metadata']['detected_class'] = class_info
            metadata['metadata']['detected_subject'] = subject_info
            
            # Save to JSON
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return metadata_path
            
        except Exception as e:
            print(f"Error saving metadata: {str(e)}")
            return None
    
    def _extract_class_subject_from_filename(self, filename):
        """
        Extract class and subject information from filename
        Expected format: Class7_Science.pdf, Science_Class7.pdf, etc.
        
        Args:
            filename (str): PDF filename
            
        Returns:
            tuple: (class_info, subject_info)
        """
        try:
            # Remove extension and convert to lowercase for analysis
            name = os.path.splitext(filename)[0].lower()
            
            # Class detection patterns
            class_patterns = [
                r'class\s*(\d+)',
                r'grade\s*(\d+)',
                r'std\s*(\d+)',
                r'(\d+)(?:th|st|nd|rd)?\s*class',
                r'(\d+)(?:th|st|nd|rd)?\s*grade'
            ]
            
            class_info = None
            for pattern in class_patterns:
                match = re.search(pattern, name)
                if match:
                    class_info = f"Class {match.group(1)}"
                    break
            
            # Subject detection patterns
            subject_keywords = {
                'science': ['science', 'physics', 'chemistry', 'biology'],
                'mathematics': ['math', 'mathematics', 'algebra', 'geometry', 'calculus'],
                'english': ['english', 'literature', 'grammar', 'language'],
                'social studies': ['social', 'history', 'geography', 'civics', 'sst', 'studies'],
                'hindi': ['hindi'],
                'computer': ['computer', 'programming', 'coding', 'it']
            }
            
            subject_info = None
            for subject, keywords in subject_keywords.items():
                if any(keyword in name for keyword in keywords):
                    subject_info = subject.title()
                    if subject == 'social studies':
                        subject_info = 'Social Studies (SST)'
                    break
            
            # Default fallbacks
            if not class_info:
                class_info = "Unknown Class"
            if not subject_info:
                subject_info = "General Studies"
            
            return class_info, subject_info
            
        except Exception as e:
            print(f"Error extracting class/subject from filename: {str(e)}")
            return "Unknown Class", "General Studies"