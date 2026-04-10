"""
Canvas Scraper - Uses your existing Chrome profile so you're already logged in.
"""
import asyncio
import json
import re
import os
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CANVAS_URL = "https://utah.instructure.com"

# Chrome profile path on macOS
CHROME_USER_DATA = os.path.expanduser("~/Library/Application Support/Google/Chrome")

class CanvasScraper:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        
    async def start_browser(self):
        """Launch browser with separate profile (avoids conflict with running Chrome)"""
        self.playwright = await async_playwright().start()
        
        # Use a SEPARATE profile directory for scraping to avoid Chrome lock conflicts
        scraper_profile = os.path.expanduser("~/.canvas-scraper-profile")
        os.makedirs(scraper_profile, exist_ok=True)
        
        print("🌐 Launching browser (separate profile - you'll need to log in once)...")
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=scraper_profile,
            channel="chrome",  # Use installed Chrome
            headless=False,
            viewport={'width': 1280, 'height': 900},
            args=['--disable-blink-features=AutomationControlled']
        )
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        
    async def check_login(self):
        """Check if we're logged into Canvas, prompt login if needed"""
        await self.page.goto(CANVAS_URL)
        await self.page.wait_for_load_state("networkidle")
        
        # Check if we're on dashboard or login page
        current_url = self.page.url
        if "login" in current_url or "cas" in current_url or "sso" in current_url:
            print("\n" + "="*50)
            print("🔐 Please log in to Canvas in the browser window")
            print("="*50)
            print("Press ENTER here once you're on the Dashboard...")
            input()
            await asyncio.sleep(2)
        else:
            print("✅ Already logged into Canvas!")
        
    async def get_courses(self):
        """Get list of courses from dashboard"""
        await self.page.goto(f"{CANVAS_URL}/courses")
        await self.page.wait_for_load_state("networkidle")
        
        content = await self.page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        courses = []
        # Find course cards/links
        course_links = soup.select('a[href*="/courses/"]')
        seen_ids = set()
        
        for link in course_links:
            href = link.get('href', '')
            match = re.search(r'/courses/(\d+)', href)
            if match:
                course_id = match.group(1)
                if course_id not in seen_ids:
                    seen_ids.add(course_id)
                    name = link.get_text(strip=True)
                    if name and len(name) > 2:
                        courses.append({
                            'id': course_id,
                            'name': name,
                            'url': f"{CANVAS_URL}/courses/{course_id}"
                        })
        
        return courses
    
    async def find_calculus_course(self, courses):
        """Find the calculus course"""
        for course in courses:
            name = course['name'].lower()
            if 'calc' in name or 'math 1' in name or 'math 2' in name:
                return course
        return None
    
    async def scrape_course(self, course_id):
        """Scrape all content from a course"""
        print(f"\n📚 Scraping course {course_id}...")
        
        data = {
            'course_id': course_id,
            'scraped_at': datetime.utcnow().isoformat(),
            'syllabus': None,
            'assignments': [],
            'modules': [],
            'announcements': [],
            'pages': [],
            'files': []
        }
        
        # Scrape syllabus
        print("  → Syllabus...")
        data['syllabus'] = await self.scrape_syllabus(course_id)
        
        # Scrape assignments
        print("  → Assignments...")
        data['assignments'] = await self.scrape_assignments(course_id)
        
        # Scrape modules
        print("  → Modules...")
        data['modules'] = await self.scrape_modules(course_id)
        
        # Scrape announcements
        print("  → Announcements...")
        data['announcements'] = await self.scrape_announcements(course_id)
        
        # Save to file
        output_file = DATA_DIR / f"course_{course_id}.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ Saved to {output_file}")
        return data
    
    async def scrape_syllabus(self, course_id):
        """Scrape course syllabus"""
        try:
            await self.page.goto(f"{CANVAS_URL}/courses/{course_id}/assignments/syllabus")
            await self.page.wait_for_load_state("networkidle")
            
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            syllabus_div = soup.select_one('#course_syllabus, .syllabus_content, .user_content')
            if syllabus_div:
                return {
                    'html': str(syllabus_div),
                    'text': syllabus_div.get_text(separator='\n', strip=True)
                }
        except Exception as e:
            print(f"    Warning: Could not scrape syllabus: {e}")
        return None
    
    async def scrape_assignments(self, course_id):
        """Scrape all assignments"""
        assignments = []
        try:
            await self.page.goto(f"{CANVAS_URL}/courses/{course_id}/assignments")
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(1)  # Let JS render
            
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find assignment links
            assignment_items = soup.select('.assignment, .ig-row, a[href*="/assignments/"]')
            seen_ids = set()
            
            for item in assignment_items:
                link = item if item.name == 'a' else item.select_one('a[href*="/assignments/"]')
                if link:
                    href = link.get('href', '')
                    match = re.search(r'/assignments/(\d+)', href)
                    if match and match.group(1) not in seen_ids:
                        assignment_id = match.group(1)
                        seen_ids.add(assignment_id)
                        
                        # Get assignment details
                        detail = await self.scrape_assignment_detail(course_id, assignment_id)
                        if detail:
                            assignments.append(detail)
                            
        except Exception as e:
            print(f"    Warning: Could not scrape assignments list: {e}")
        
        return assignments
    
    async def scrape_assignment_detail(self, course_id, assignment_id):
        """Scrape individual assignment details"""
        try:
            await self.page.goto(f"{CANVAS_URL}/courses/{course_id}/assignments/{assignment_id}")
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(0.5)  # Let page fully render
            
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Try multiple selectors for the title - Canvas uses different ones
            title = None
            title_selectors = [
                'h1.title',
                '.assignment-title h1',
                'h1[class*="title"]',
                '.ig-header-title',
                'h2.title',
                '#assignment_show h1',
                'h1'  # Last resort
            ]
            for selector in title_selectors:
                title_el = soup.select_one(selector)
                if title_el:
                    text = title_el.get_text(strip=True)
                    if text and len(text) > 2 and 'Assignment' not in text[:15]:
                        title = text
                        break
            
            if not title:
                title = f"Assignment {assignment_id}"
            
            desc_el = soup.select_one('.description, .user_content, #assignment_show .description, .assignment-description')
            description_html = str(desc_el) if desc_el else ""
            description_text = desc_el.get_text(separator='\n', strip=True) if desc_el else ""
            
            # Try to find due date
            due_el = soup.select_one('.date_text, .assignment_dates, .due_date_display, .assignment-date-due')
            due_date = due_el.get_text(strip=True) if due_el else None
            
            # Try to find points
            points_el = soup.select_one('.points_possible, .possible, .points')
            points = points_el.get_text(strip=True) if points_el else None
            
            # Print progress with actual title
            print(f"      📄 {title[:50]}...")
            
            return {
                'id': assignment_id,
                'title': title,
                'description_html': description_html,
                'description_text': description_text,
                'due_date': due_date,
                'points': points,
                'url': f"{CANVAS_URL}/courses/{course_id}/assignments/{assignment_id}"
            }
        except Exception as e:
            print(f"    Warning: Could not scrape assignment {assignment_id}: {e}")
            return None
    
    async def scrape_modules(self, course_id):
        """Scrape course modules"""
        modules = []
        try:
            await self.page.goto(f"{CANVAS_URL}/courses/{course_id}/modules")
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)  # Modules page needs time to load
            
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            module_divs = soup.select('.context_module, .ig-header')
            
            for mod_div in module_divs:
                header = mod_div.select_one('.ig-header-title, .name, .module_name')
                if header:
                    module_name = header.get_text(strip=True)
                    
                    items = []
                    item_els = mod_div.select('.ig-row, .context_module_item')
                    for item_el in item_els:
                        item_link = item_el.select_one('a')
                        if item_link:
                            items.append({
                                'title': item_link.get_text(strip=True),
                                'url': item_link.get('href', '')
                            })
                    
                    modules.append({
                        'name': module_name,
                        'items': items
                    })
                    
        except Exception as e:
            print(f"    Warning: Could not scrape modules: {e}")
        
        return modules
    
    async def scrape_announcements(self, course_id):
        """Scrape course announcements"""
        announcements = []
        try:
            await self.page.goto(f"{CANVAS_URL}/courses/{course_id}/announcements")
            await self.page.wait_for_load_state("networkidle")
            
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            announcement_items = soup.select('.discussion-topic, .ig-row')
            
            for item in announcement_items[:10]:  # Last 10 announcements
                link = item.select_one('a')
                if link:
                    announcements.append({
                        'title': link.get_text(strip=True),
                        'url': link.get('href', '')
                    })
                    
        except Exception as e:
            print(f"    Warning: Could not scrape announcements: {e}")
        
        return announcements
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


async def main():
    scraper = CanvasScraper()
    
    try:
        print("🚀 Launching Chrome with your profile...")
        await scraper.start_browser()
        await scraper.check_login()
        
        print("\n🔍 Finding your courses...")
        courses = await scraper.get_courses()
        
        if not courses:
            print("No courses found. Make sure you're fully logged in.")
            return
        
        print(f"\nFound {len(courses)} courses:")
        for i, course in enumerate(courses):
            print(f"  {i+1}. {course['name']}")
        
        # Try to find calculus automatically
        calc_course = await scraper.find_calculus_course(courses)
        
        if calc_course:
            print(f"\n🎯 Found calculus course: {calc_course['name']}")
            choice = input("Scrape this course? (y/n): ").strip().lower()
            if choice == 'y':
                await scraper.scrape_course(calc_course['id'])
        else:
            print("\nCouldn't auto-detect calculus course.")
            choice = input("Enter course number to scrape (or 'all'): ").strip()
            
            if choice == 'all':
                for course in courses:
                    await scraper.scrape_course(course['id'])
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(courses):
                    await scraper.scrape_course(courses[idx]['id'])
                    
        print("\n✨ Done! Your course data is saved in backend/data/")
        
    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
