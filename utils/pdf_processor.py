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
    
    def _extract_contents_page(self, doc):
        """Extract chapter information from Contents page (pages 1-14)"""
        contents_chapters = []
        contents_patterns = [
            r'Chapter\s+(\d+)\s+(.+?)\s+(\d+)$',      # Chapter  X Title PageNum
            r'Chapter\s+(\d+)[\s\.:]*(.+?)\s+(\d+)',  # Chapter X Title PageNum
        ]
        
        try:
            # Check pages 1-14 for Contents page
            for page_num in range(min(14, len(doc))):
                page = doc[page_num]
                try:
                    page_text = page.get_text()
                except:
                    try:
                        page_text = page.get_text("text")
                    except:
                        continue
                        
                # Look for "Contents" or "Table of Contents" 
                if any(word in page_text.lower() for word in ['contents', 'index']):
                    print(f"Found Contents page at page {page_num + 1}")
                    lines = page_text.split('\n')
                    
                    chapter_lines = []
                    for line in lines:
                        line = line.strip()
                        if 'Chapter' in line and len(line) > 5:
                            chapter_lines.append(line)
                    
                    # Process chapter lines
                    for line in chapter_lines:
                        # Handle multi-line chapter entries
                        if 'Chapter' in line:
                            parts = line.split()
                            if len(parts) >= 3:
                                # Find chapter number
                                chapter_num = None
                                for part in parts:
                                    if part.isdigit() and 1 <= int(part) <= 20:
                                        chapter_num = int(part)
                                        break
                                
                                # Find page number (last digit)
                                page_num = None
                                for part in reversed(parts):
                                    if part.isdigit() and int(part) > 20:  # Page numbers are > 20
                                        page_num = int(part)
                                        break
                                
                                if chapter_num and page_num:
                                    # Extract title (everything between chapter number and page number)
                                    title_parts = []
                                    start_collecting = False
                                    for part in parts:
                                        if part == str(chapter_num):
                                            start_collecting = True
                                            continue
                                        if part == str(page_num):
                                            break
                                        if start_collecting:
                                            title_parts.append(part)
                                    
                                    title = ' '.join(title_parts).strip()
                                    if title:
                                        contents_chapters.append({
                                            'number': chapter_num,
                                            'title': title,
                                            'start_page': page_num
                                        })
                                        print(f"Found Chapter {chapter_num}: {title} (Page {page_num})")
        except Exception as e:
            print(f"Error extracting contents: {str(e)}")
            
        return contents_chapters
    
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
            
            # First, extract Contents page to get chapter structure
            contents_chapters = self._extract_contents_page(doc)
            print(f"Found {len(contents_chapters)} chapters in Contents page")
            
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
            
            # Use Contents page chapters if available and more comprehensive
            if contents_chapters and len(contents_chapters) > len(chapters):
                print(f"Using Contents page chapters ({len(contents_chapters)}) instead of detected chapters ({len(chapters)})")
                final_chapters = contents_chapters
                
                # Add content to each chapter from the main text
                for chapter in final_chapters:
                    chapter_content = ""
                    # Extract content for this chapter based on page range
                    start_page_idx = max(14, chapter['start_page'] - 1)  # Start from page 15 minimum
                    
                    # Find end page (next chapter's start page - 1)
                    end_page_idx = total_pages
                    for next_chapter in contents_chapters:
                        if next_chapter['number'] > chapter['number']:
                            end_page_idx = next_chapter['start_page'] - 1
                            break
                    
                    # Extract content for this chapter
                    for page_num in range(start_page_idx, min(end_page_idx, total_pages)):
                        try:
                            page = doc[page_num]
                            try:
                                page_text = page.get_text()
                            except:
                                page_text = page.get_text("text")
                            chapter_content += page_text + "\n"
                        except:
                            continue
                    
                    chapter['content'] = chapter_content
            else:
                final_chapters = chapters
            
            doc.close()
            
            return {
                'content': full_text,
                'chapters': final_chapters,
                'metadata': {
                    'total_pages': total_pages,
                    'content_start_page': start_page,
                    'document_type': 'text',
                    'extracted_with_ocr': False,
                    'contents_chapters_found': len(contents_chapters)
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