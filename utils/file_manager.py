import os
import shutil
from pathlib import Path
from datetime import datetime

class FileManager:
    def __init__(self):
        self.base_data_dir = "data"
        self.allowed_extensions = {
            'pdf': ['pdf'],
            'image': ['jpg', 'jpeg', 'png', 'bmp'],
            'text': ['txt', 'docx', 'doc']
        }
    
    def create_directory_structure(self):
        """Create the required directory structure for the application"""
        directories = [
            "data/grades/grade_7/textbooks",
            "data/grades/grade_7/textbooks/metadata",
            "data/grades/grade_7/question_papers", 
            "data/grades/grade_7/sample_answers",
            "data/grades/grade_8/textbooks",
            "data/grades/grade_8/textbooks/metadata",
            "data/grades/grade_8/question_papers",
            "data/grades/grade_8/sample_answers",
            "data/grades/grade_9/textbooks",
            "data/grades/grade_9/textbooks/metadata",
            "data/grades/grade_9/question_papers",
            "data/grades/grade_9/sample_answers",
            "data/question_papers",
            "data/evaluated_sheets",
            "data/temp"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def validate_file_type(self, filename, file_category):
        """
        Validate if file type is allowed for the given category
        
        Args:
            filename (str): Name of the file
            file_category (str): Category of file (pdf, image, text)
            
        Returns:
            bool: True if file type is allowed
        """
        file_extension = filename.lower().split('.')[-1]
        allowed_extensions = self.allowed_extensions.get(file_category, [])
        return file_extension in allowed_extensions
    
    def save_uploaded_file(self, uploaded_file, destination_path):
        """
        Save an uploaded file to the specified destination
        
        Args:
            uploaded_file: Streamlit uploaded file object
            destination_path (str): Path where file should be saved
            
        Returns:
            str: Path to saved file or None if failed
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Save the file
            with open(destination_path, "wb") as f:
                f.write(uploaded_file.read())
            
            return destination_path
            
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return None
    
    def get_files_in_directory(self, directory_path, file_extensions=None):
        """
        Get list of files in a directory with optional extension filtering
        
        Args:
            directory_path (str): Path to directory
            file_extensions (list): List of allowed extensions
            
        Returns:
            list: List of file paths
        """
        try:
            if not os.path.exists(directory_path):
                return []
            
            files = []
            for filename in os.listdir(directory_path):
                filepath = os.path.join(directory_path, filename)
                
                if os.path.isfile(filepath):
                    if file_extensions:
                        file_ext = filename.lower().split('.')[-1]
                        if file_ext in file_extensions:
                            files.append(filepath)
                    else:
                        files.append(filepath)
            
            return sorted(files)
            
        except Exception as e:
            print(f"Error getting files from directory: {str(e)}")
            return []
    
    def delete_file(self, file_path):
        """Delete a file safely"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
            
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
            return False
    
    def get_file_info(self, file_path):
        """Get information about a file"""
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            
            return {
                'name': os.path.basename(file_path),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'extension': file_path.lower().split('.')[-1]
            }
            
        except Exception as e:
            print(f"Error getting file info: {str(e)}")
            return None