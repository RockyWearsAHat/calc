"""
Canvas LMS API Client
Handles all communication with Canvas to fetch course data, assignments, modules, and files.
"""
import os
import re
import json
import asyncio
from typing import Optional
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

class CanvasClient:
    def __init__(self):
        self.api_token = os.getenv("CANVAS_API_TOKEN", "")
        self.base_url = os.getenv("CANVAS_BASE_URL", "https://utah.instructure.com")
        self.api_url = f"{self.base_url}/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def is_configured(self) -> bool:
        return bool(self.api_token and len(self.api_token) > 10)
    
    async def _get(self, endpoint: str, params: dict = None) -> dict | list:
        """Make authenticated GET request to Canvas API"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.api_url}/{endpoint}"
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    raise Exception("Invalid Canvas API token. Please check your credentials.")
                else:
                    raise Exception(f"Canvas API error: {response.status}")
    
    async def _get_all_pages(self, endpoint: str, params: dict = None) -> list:
        """Get all pages of a paginated Canvas API response"""
        all_results = []
        params = params or {}
        params['per_page'] = 100
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.api_url}/{endpoint}"
            while url:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status != 200:
                        break
                    data = await response.json()
                    if isinstance(data, list):
                        all_results.extend(data)
                    else:
                        all_results.append(data)
                    
                    # Check for next page in Link header
                    links = response.headers.get('Link', '')
                    url = None
                    for link in links.split(','):
                        if 'rel="next"' in link:
                            url = link.split(';')[0].strip('<> ')
                            params = None  # URL already contains params
                            break
        return all_results
    
    async def get_courses(self) -> list:
        """Get all courses for the authenticated user"""
        courses = await self._get_all_pages("courses", {
            "enrollment_state": "active",
            "include[]": ["term", "total_scores"]
        })
        return [c for c in courses if isinstance(c, dict) and 'name' in c]
    
    async def get_calculus_course(self) -> Optional[dict]:
        """Find the calculus course from user's enrolled courses"""
        courses = await self.get_courses()
        for course in courses:
            name = course.get('name', '').lower()
            if 'calculus' in name or 'calc' in name or 'math 1' in name or 'math 2' in name:
                return course
        return None
    
    async def get_course_modules(self, course_id: int) -> list:
        """Get all modules for a course with their items"""
        modules = await self._get_all_pages(f"courses/{course_id}/modules", {
            "include[]": ["items"]
        })
        return modules
    
    async def get_module_items(self, course_id: int, module_id: int) -> list:
        """Get all items within a module"""
        return await self._get_all_pages(f"courses/{course_id}/modules/{module_id}/items")
    
    async def get_assignments(self, course_id: int) -> list:
        """Get all assignments for a course"""
        assignments = await self._get_all_pages(f"courses/{course_id}/assignments", {
            "include[]": ["submission"],
            "order_by": "due_at"
        })
        return assignments
    
    async def get_assignment_detail(self, course_id: int, assignment_id: int) -> dict:
        """Get detailed information about a specific assignment"""
        return await self._get(f"courses/{course_id}/assignments/{assignment_id}")
    
    async def get_pages(self, course_id: int) -> list:
        """Get all pages in a course"""
        return await self._get_all_pages(f"courses/{course_id}/pages")
    
    async def get_page_content(self, course_id: int, page_url: str) -> dict:
        """Get the content of a specific page"""
        return await self._get(f"courses/{course_id}/pages/{page_url}")
    
    async def get_files(self, course_id: int) -> list:
        """Get all files in a course"""
        return await self._get_all_pages(f"courses/{course_id}/files")
    
    async def get_syllabus(self, course_id: int) -> str:
        """Get the syllabus for a course"""
        course = await self._get(f"courses/{course_id}", {"include[]": ["syllabus_body"]})
        return course.get('syllabus_body', '')
    
    async def get_announcements(self, course_id: int) -> list:
        """Get course announcements"""
        return await self._get_all_pages(f"courses/{course_id}/discussion_topics", {
            "only_announcements": "true"
        })
    
    def extract_text_from_html(self, html: str) -> str:
        """Extract plain text from HTML content"""
        if not html:
            return ""
        soup = BeautifulSoup(html, 'html.parser')
        # Remove script and style elements
        for element in soup(['script', 'style']):
            element.decompose()
        return soup.get_text(separator='\n', strip=True)
    
    def extract_math_content(self, html: str) -> list:
        """Extract math equations and formulas from content"""
        if not html:
            return []
        
        math_content = []
        
        # Look for LaTeX in various formats
        latex_patterns = [
            r'\$\$(.*?)\$\$',  # Display math
            r'\$(.*?)\$',      # Inline math
            r'\\begin\{equation\}(.*?)\\end\{equation\}',
            r'\\begin\{align\}(.*?)\\end\{align\}',
            r'\\\[(.*?)\\\]',  # LaTeX display
            r'\\\((.*?)\\\)',  # LaTeX inline
        ]
        
        for pattern in latex_patterns:
            matches = re.findall(pattern, html, re.DOTALL)
            math_content.extend(matches)
        
        return math_content

    async def sync_course_data(self, course_id: int) -> dict:
        """
        Comprehensive sync of all course data.
        Returns structured data ready for the study platform.
        """
        course = await self._get(f"courses/{course_id}")
        
        # Fetch all data concurrently
        modules_task = self.get_course_modules(course_id)
        assignments_task = self.get_assignments(course_id)
        pages_task = self.get_pages(course_id)
        syllabus_task = self.get_syllabus(course_id)
        announcements_task = self.get_announcements(course_id)
        files_task = self.get_files(course_id)
        
        modules, assignments, pages, syllabus, announcements, files = await asyncio.gather(
            modules_task, assignments_task, pages_task,
            syllabus_task, announcements_task, files_task
        )
        
        # Process assignments into topics/concepts
        topics = self._extract_topics_from_assignments(assignments)
        
        # Build comprehensive course data
        return {
            "course": {
                "id": course_id,
                "name": course.get('name', ''),
                "code": course.get('course_code', ''),
            },
            "syllabus": {
                "html": syllabus,
                "text": self.extract_text_from_html(syllabus)
            },
            "modules": modules,
            "assignments": self._process_assignments(assignments),
            "pages": pages,
            "announcements": announcements,
            "files": self._filter_relevant_files(files),
            "topics": topics,
            "synced_at": datetime.utcnow().isoformat()
        }
    
    def _process_assignments(self, assignments: list) -> list:
        """Process assignments to extract useful study information"""
        processed = []
        for a in assignments:
            processed.append({
                "id": a.get('id'),
                "name": a.get('name', ''),
                "description": self.extract_text_from_html(a.get('description', '')),
                "description_html": a.get('description', ''),
                "due_at": a.get('due_at'),
                "points_possible": a.get('points_possible'),
                "submission_types": a.get('submission_types', []),
                "html_url": a.get('html_url', ''),
                "math_content": self.extract_math_content(a.get('description', '')),
                "is_quiz": 'online_quiz' in a.get('submission_types', []),
            })
        return processed
    
    def _extract_topics_from_assignments(self, assignments: list) -> list:
        """
        Intelligently extract calculus topics from assignment names and descriptions.
        Maps to standard Calc I/II curriculum.
        """
        calculus_topics = {
            # Calc I Topics
            "limits": ["limit", "continuity", "continuous", "squeeze theorem", "epsilon-delta"],
            "derivatives": ["derivative", "differentiation", "rate of change", "tangent line", "d/dx"],
            "derivative_rules": ["product rule", "quotient rule", "chain rule", "power rule"],
            "implicit_differentiation": ["implicit", "related rates"],
            "applications_derivatives": ["optimization", "maximum", "minimum", "extrema", "critical point", "inflection"],
            "integration_basics": ["integral", "antiderivative", "indefinite integral"],
            "definite_integrals": ["definite integral", "area under", "riemann sum", "fundamental theorem"],
            "integration_techniques": ["u-substitution", "substitution", "integration by parts"],
            
            # Calc II Topics
            "advanced_integration": ["trig substitution", "partial fractions", "improper integral"],
            "applications_integration": ["volume", "arc length", "surface area", "work", "disk method", "washer", "shell method"],
            "sequences": ["sequence", "convergent sequence", "divergent sequence"],
            "series": ["series", "convergent series", "divergent series", "geometric series", "harmonic"],
            "convergence_tests": ["ratio test", "root test", "comparison test", "integral test", "alternating series"],
            "power_series": ["power series", "taylor", "maclaurin", "radius of convergence"],
            "differential_equations": ["differential equation", "separable", "first order", "initial value"],
            "parametric": ["parametric", "polar coordinates", "polar curve"],
        }
        
        found_topics = set()
        
        for assignment in assignments:
            text = f"{assignment.get('name', '')} {assignment.get('description', '')}".lower()
            for topic, keywords in calculus_topics.items():
                for keyword in keywords:
                    if keyword in text:
                        found_topics.add(topic)
                        break
        
        return list(found_topics)
    
    def _filter_relevant_files(self, files: list) -> list:
        """Filter files to only include relevant study materials"""
        relevant_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt']
        relevant = []
        for f in files:
            name = f.get('display_name', '').lower()
            if any(name.endswith(ext) for ext in relevant_extensions):
                relevant.append({
                    "id": f.get('id'),
                    "name": f.get('display_name'),
                    "url": f.get('url'),
                    "size": f.get('size'),
                    "content_type": f.get('content-type'),
                    "created_at": f.get('created_at'),
                })
        return relevant
