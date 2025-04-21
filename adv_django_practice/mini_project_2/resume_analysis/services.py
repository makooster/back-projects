# resume_analysis/services.py
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import PyPDF2
import docx
import io
import os

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ResumeParser:
    """Service for parsing resume content"""
    
    def __init__(self, file_obj, file_type):
        self.file_obj = file_obj
        self.file_type = file_type
        self.text = None
        self.extracted_data = {
            'skills': [],
            'education': [],
            'experience': [],
            'contact_info': {}
        }
        
    def extract_text(self):
        """Extract text from PDF or DOCX file"""
        if self.file_type == 'PDF':
            return self._extract_text_from_pdf()
        elif self.file_type == 'DOCX':
            return self._extract_text_from_docx()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
    
    def _extract_text_from_pdf(self):
        """Extract text from PDF file"""
        pdf_reader = PyPDF2.PdfReader(self.file_obj)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        self.text = text
        return text
    
    def _extract_text_from_docx(self):
        """Extract text from DOCX file"""
        doc = docx.Document(self.file_obj)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        self.text = text
        return text
    
    def extract_skills(self, common_skills):
        """Extract skills from text using a predefined list"""
        if not self.text:
            self.extract_text()
            
        text_tokens = word_tokenize(self.text.lower())
        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
        
        found_skills = []
        for skill in common_skills:
            skill_pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(skill_pattern, self.text.lower()):
                found_skills.append(skill)
                
        self.extracted_data['skills'] = found_skills
        return found_skills
    
    def extract_education(self):
        """Extract education details"""
        if not self.text:
            self.extract_text()
            
        # Simple education extraction using regex
        education_patterns = [
            r'(?:(?:B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|Ph\.?D\.?|MBA|Bachelor|Master|Doctor|Doctorate).*?(?:19|20)\d{2})',
            r'(?:University|College|Institute|School).*?(?:19|20)\d{2}',
            r'(?:19|20)\d{2}.*?(?:University|College|Institute|School)'
        ]
        
        education = []
        for pattern in education_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            education.extend(matches)
            
        self.extracted_data['education'] = [edu.strip() for edu in education]
        return self.extracted_data['education']
    
    def extract_experience(self):
        """Extract work experience"""
        if not self.text:
            self.extract_text()
            
        # Simple experience extraction using regex
        experience_patterns = [
            r'(?:(?:19|20)\d{2}\s*-\s*(?:present|current|now|(?:19|20)\d{2})).*?(?:[\.\n])',
            r'(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{4}\s*-\s*(?:present|current|now|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{4})).*?(?:[\.\n])'
        ]
        
        experience = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            experience.extend(matches)
            
        self.extracted_data['experience'] = [exp.strip() for exp in experience]
        return self.extracted_data['experience']
    
    def analyze_resume(self, common_skills):
        """Extract all data from resume"""
        self.extract_text()
        self.extract_skills(common_skills)
        self.extract_education()
        self.extract_experience()
        return self.extracted_data

class ResumeAnalyzer:
    """Service for analyzing resumes and providing feedback"""
    
    def __init__(self, resume_data, job_description=None):
        self.resume_data = resume_data
        self.job_description = job_description
        self.analysis_result = {
            'overall_score': 0.0,
            'strengths': [],
            'improvements': [],
            'job_match_score': 0.0 if job_description else None
        }
        
    def analyze_resume_quality(self):
        """Analyze the quality of the resume"""
        # Basic scoring logic based on resume content
        score = 0.0
        strengths = []
        improvements = []
        
        # Check skills count
        skills_count = len(self.resume_data.get('skills', []))
        if skills_count >= 10:
            score += 30
            strengths.append("Strong technical skills section")
        elif skills_count >= 5:
            score += 20
            strengths.append("Good technical skills section")
        else:
            score += 10
            improvements.append("Add more relevant technical skills")
            
        # Check education
        if len(self.resume_data.get('education', [])) > 0:
            score += 20
            strengths.append("Education section present")
        else:
            improvements.append("Add educational background")
            
        # Check experience
        exp_count = len(self.resume_data.get('experience', []))
        if exp_count >= 3:
            score += 30
            strengths.append("Strong work experience")
        elif exp_count >= 1:
            score += 20
            strengths.append("Some work experience included")
        else:
            score += 0
            improvements.append("Add more work experience details")
            
        # Additional recommendations
        if skills_count < 10:
            improvements.append("Consider adding more in-demand tech skills")
            
        self.analysis_result['overall_score'] = min(score, 100)
        self.analysis_result['strengths'] = strengths
        self.analysis_result['improvements'] = improvements
        
        return self.analysis_result
        
    def match_with_job(self):
        """Match resume with job description if available"""
        if not self.job_description:
            return None
            
        # Simple keyword matching for job compatibility
        resume_skills = set(skill.lower() for skill in self.resume_data.get('skills', []))
        
        # Extract skills from job description (simplified)
        job_skills = set()
        for skill in resume_skills:
            if skill.lower() in self.job_description.lower():
                job_skills.add(skill)
                
        if job_skills:
            match_percentage = len(job_skills) / max(1, len(resume_skills)) * 100
            self.analysis_result['job_match_score'] = match_percentage
            
            if match_percentage >= 70:
                self.analysis_result['strengths'].append(f"Strong match ({match_percentage:.1f}%) with job requirements")
            elif match_percentage >= 50:
                self.analysis_result['strengths'].append(f"Good match ({match_percentage:.1f}%) with job requirements")
                self.analysis_result['improvements'].append("Try to acquire more skills listed in the job description")
            else:
                self.analysis_result['improvements'].append(f"Low match ({match_percentage:.1f}%) with job requirements")
                self.analysis_result['improvements'].append("Work on developing skills mentioned in the job posting")
                
        return self.analysis_result['job_match_score']
        
    def get_full_analysis(self):
        """Get complete analysis"""
        self.analyze_resume_quality()