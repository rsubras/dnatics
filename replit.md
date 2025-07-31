# PowerBI Report Narration App

## Overview

This is a web application that captures PowerBI report screenshots and generates narrative descriptions using AI models. The system consists of a React frontend that embeds PowerBI reports and a Python FastAPI backend that processes images through various AI models (Ollama, Gemini, Mistral) to provide OCR and narrative generation capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a client-server architecture with clear separation between the frontend and backend:

### Frontend Architecture
- **Framework**: React 19.0.0 with Create React App
- **UI Components**: Material-UI (@mui/material) for consistent design
- **Authentication**: Microsoft Azure MSAL for PowerBI authentication
- **PowerBI Integration**: powerbi-client-react for embedding reports
- **Screen Capture**: html2canvas and native browser screen capture API
- **Styling**: CSS with PostCSS for processing

### Backend Architecture
- **Framework**: FastAPI for REST API endpoints
- **AI Models**: Multiple model support including:
  - Ollama (llama3.2-vision) for local inference
  - Google Gemini (gemini-1.5-flash) via LangChain
  - Mistral OCR for text extraction
- **Image Processing**: PIL and base64 encoding for image handling
- **Configuration**: JSON-based model selection

## Key Components

### Frontend Components
1. **App.js**: Main application component handling MSAL authentication
2. **Layout.js**: Application layout with header and grid structure
3. **LeftContainer.js**: PowerBI report embedding and token management
4. **RightContainer.js**: Image capture and narration display
5. **msalConfig.js**: Microsoft authentication configuration

### Backend Components
1. **processimage.py**: Main FastAPI application with CORS support
2. **imageprocessing_API.py**: Ollama-specific image processing
3. **test_*.py**: Individual model testing scripts
4. **config.json**: Model selection configuration

## Data Flow

1. **Authentication Flow**:
   - User authenticates via Microsoft Azure MSAL
   - PowerBI access token acquired for report embedding
   - Token used for PowerBI report access

2. **Report Display**:
   - PowerBI report embedded in left container
   - Report rendered with hidden filters for clean display

3. **Image Processing Flow**:
   - User captures screen using browser screen capture API
   - Image converted to blob and sent to FastAPI backend
   - Backend processes image through selected AI model
   - OCR and narrative generation performed
   - Results returned to frontend for display

## External Dependencies

### Frontend Dependencies
- **@azure/msal-browser & @azure/msal-react**: Microsoft authentication
- **powerbi-client & powerbi-client-react**: PowerBI integration
- **@mui/material**: UI components
- **html2canvas**: Alternative screen capture method
- **axios**: HTTP client for API communication

### Backend Dependencies
- **FastAPI**: Web framework
- **langchain-google-genai**: Google Gemini integration
- **mistralai**: Mistral API client
- **PIL**: Image processing
- **requests**: HTTP client for Ollama communication

### AI Model Services
- **Ollama**: Local AI model server (llama3.2-vision)
- **Google Gemini**: Cloud-based vision model
- **Mistral**: OCR and text processing service

## Deployment Strategy

### Development Environment
- Frontend: React development server on localhost:3000
- Backend: FastAPI server (port not specified in current config)
- Local Ollama server: localhost:11434

### Configuration Management
- Environment variables via .env files
- JSON configuration for model selection
- Separate API keys for each service (Google, Mistral)

### Authentication Configuration
- Azure AD tenant and client ID configured
- PowerBI API scopes defined
- Redirect URI set for local development

### Build Process
- Frontend: Create React App build system
- PostCSS configuration for CSS processing
- Production builds optimized and minified

## Key Architectural Decisions

1. **Multi-Model Support**: The system supports multiple AI models (Ollama, Gemini, Mistral) to provide flexibility and redundancy in image processing capabilities.

2. **Microsoft Authentication**: Uses Azure MSAL for seamless integration with PowerBI services, ensuring secure access to enterprise reports.

3. **Screen Capture Strategy**: Implements browser-native screen capture API for high-quality screenshot capture, with html2canvas as a fallback option.

4. **FastAPI Backend**: Chosen for its automatic API documentation, async support, and easy integration with Python AI libraries.

5. **Component-Based Frontend**: React components are organized for clear separation of concerns between authentication, report display, and image processing.

6. **CORS Configuration**: Properly configured to allow frontend-backend communication during development.

The architecture prioritizes flexibility, security, and ease of development while maintaining clear separation between different functional areas of the application.

## Recent Changes (2025-07-30)

### Enhanced Question Generation System
- **Fixed Content-Based Question Generation**: Replaced generic template system with intelligent content extraction from actual textbook content
- **Improved Content Extraction**: Enhanced fact, definition, process, and example extraction from textbook sentences
- **Smarter Chapter Detection**: Fixed PDF processor to avoid false chapter detection (was detecting 261 chapters instead of actual 4-12)
- **Robust Fallback System**: Added fallback content extraction when primary extraction yields insufficient content
- **Better MCQ Options**: Generate meaningful multiple choice options based on actual textbook content instead of placeholder text

### Technical Improvements
- **Fixed PyMuPDF API**: Updated PDF text extraction to use correct `get_text("text")` method
- **Enhanced Pattern Matching**: Improved chapter detection patterns to match only at line beginnings with reasonable chapter numbers (1-20)
- **Content Validation**: Added content threshold validation with debug logging for troubleshooting
- **Sentence Processing**: Enhanced sentence classification for better educational content extraction

### User Experience Enhancements
- **Real Questions**: Questions now generated from actual textbook content about Physical Changes, Weather & Climate, Motion & Time, and Light
- **Contextual Content**: Questions include source content references for validation
- **Better Error Handling**: Improved error messages and fallback mechanisms for content processing

The system now generates meaningful educational content directly from uploaded textbook materials instead of using mock templates.

### Rapid Fire Quiz System (2025-07-30 & 2025-07-31)
- **Timed Quiz Functionality**: Added comprehensive rapid fire quiz system with automatic timer management
- **Multi-Subject Support**: Mathematics (multiplication tables, fractions, arithmetic), English (grammar, vocabulary), Science (basic concepts)
- **Flexible Question Counts**: 25 questions (5 min), 50 questions (10 min), 75 questions (15 min), 100 questions (20 min)
- **Interactive Interface**: Real-time timer with color coding, progress tracking, and question navigation
- **Automatic Grading**: Instant scoring with percentage calculation and letter grades (A+ to F)
- **Result History**: Comprehensive reporting system with saved quiz results in student dashboard
- **Auto-Submit**: Timer automatically submits quiz when time expires to ensure fair assessment

### Enhanced Rapid Fire Features (2025-07-31)
- **Progressive Timer Blinking**: Timer blinks with increasing urgency (25% → 15% → 10% → 5% → 1% remaining time)
- **Email-Based Authentication**: Replaced manual name entry with email login and automatic name extraction
- **Age-Appropriate Access Control**: Minor accounts restricted from teacher access based on email patterns
- **Performance-Based Visual Feedback**: Reward icons for high scores (90%+: trophy/stars, 70%+: medals), red gradient display for poor scores
- **Detailed Wrong Answer Review**: Shows correct answers for all incorrect responses with question-by-question breakdown
- **Subject-Wise Results Grouping**: Comprehensive performance tracking with statistics, trends, and categorized results
- **No Question Repetition**: Fixed duplicate question issue by implementing unique question pools for all subjects
- **Improved Answer Display**: Fixed null correct answer issue with proper fallback mechanisms