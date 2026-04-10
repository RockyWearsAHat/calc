"""
Comprehensive Course Scraper - Follows ALL links to get actual content
- Canvas → MyLab (Pearson) homework problems
- Canvas → Gradescope exam content
- Parallel scraping for speed
- Waits for dynamic content properly
"""
import asyncio
import json
import re
import os
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, urljoin
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup
import hashlib

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CANVAS_URL = "https://utah.instructure.com"
SCRAPER_PROFILE = os.path.expanduser("~/.canvas-scraper-profile")

# External platforms to follow
EXTERNAL_PLATFORMS = {
    'pearson': ['pearson.com', 'mylab', 'mathxl', 'mylabmastering'],
    'gradescope': ['gradescope.com'],
    'cengage': ['cengage.com', 'webassign.net'],
    'mcgrawhill': ['mcgraw-hill.com', 'connect.mheducation.com'],
    'wiley': ['wileyplus.com']
}


class ComprehensiveScraper:
    def __init__(self):
        self.playwright = None
        self.context = None
        self.pages = {}  # Pool of pages for parallel scraping
        self.scraped_urls = set()
        self.all_content = {
            'course_info': {},
            'assignments': [],
            'problems': [],
            'readings': [],
            'exams': [],
            'external_content': {},
            'scraped_at': None
        }
        
    async def start(self):
        """Launch browser with persistent profile"""
        self.playwright = await async_playwright().start()
        os.makedirs(SCRAPER_PROFILE, exist_ok=True)
        
        print("🚀 Launching browser...")
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=SCRAPER_PROFILE,
            channel="chrome",
            headless=False,
            viewport={'width': 1400, 'height': 900},
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        
        # Create main page
        self.main_page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        
    async def login_and_verify(self):
        """Ensure user is logged in to Canvas"""
        await self.main_page.goto(CANVAS_URL, wait_until='networkidle')
        
        current_url = self.main_page.url
        if 'login' in current_url or 'cas' in current_url or 'sso' in current_url:
            print("\n" + "="*60)
            print("🔐 LOG IN TO CANVAS")
            print("="*60)
            print("Complete Duo authentication in the browser window.")
            print("Press ENTER when you reach the Canvas Dashboard...")
            print("="*60)
            input()
            await asyncio.sleep(2)
            await self.main_page.wait_for_load_state('networkidle')
        
        print("✅ Logged into Canvas!")
        return True
    
    async def get_page(self):
        """Get a page from pool or create new one"""
        page = await self.context.new_page()
        return page
    
    async def release_page(self, page):
        """Release page back or close it"""
        try:
            await page.close()
        except:
            pass
    
    async def find_courses(self):
        """Find all courses"""
        await self.main_page.goto(f"{CANVAS_URL}/courses", wait_until='networkidle')
        await asyncio.sleep(1)
        
        content = await self.main_page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        courses = []
        seen = set()
        
        for link in soup.select('a[href*="/courses/"]'):
            href = link.get('href', '')
            match = re.search(r'/courses/(\d+)', href)
            if match:
                cid = match.group(1)
                if cid not in seen:
                    seen.add(cid)
                    name = link.get_text(strip=True)
                    if name and len(name) > 3:
                        courses.append({'id': cid, 'name': name, 'url': f"{CANVAS_URL}/courses/{cid}"})
        
        return courses
    
    async def scrape_course_comprehensive(self, course_id: str, course_name: str):
        """Comprehensively scrape a course - follows ALL links"""
        print(f"\n{'='*60}")
        print(f"📚 COMPREHENSIVE SCRAPE: {course_name}")
        print(f"{'='*60}")
        
        self.all_content['course_info'] = {
            'id': course_id,
            'name': course_name,
            'url': f"{CANVAS_URL}/courses/{course_id}"
        }
        self.all_content['scraped_at'] = datetime.utcnow().isoformat()
        
        # Phase 1: Get all Canvas content and collect external links
        print("\n📋 Phase 1: Scanning Canvas...")
        external_links = await self.scan_canvas(course_id)
        
        # Phase 2: Scrape all external platforms in parallel
        if external_links:
            print(f"\n🔗 Phase 2: Following {len(external_links)} external links...")
            await self.scrape_external_parallel(external_links)
        
        # Phase 3: Save everything
        print("\n💾 Phase 3: Saving all content...")
        await self.save_all_content(course_id)
        
        return self.all_content
    
    async def scan_canvas(self, course_id: str):
        """Scan all Canvas pages and collect external links"""
        external_links = []
        
        # Scrape assignments page
        print("  → Assignments...")
        assignments, links = await self.scrape_assignments_list(course_id)
        self.all_content['assignments'] = assignments
        external_links.extend(links)
        
        # Scrape modules 
        print("  → Modules...")
        module_links = await self.scrape_modules(course_id)
        external_links.extend(module_links)
        
        # Scrape syllabus
        print("  → Syllabus...")
        syllabus_links = await self.scrape_syllabus(course_id)
        external_links.extend(syllabus_links)
        
        # Deduplicate links
        seen = set()
        unique_links = []
        for link in external_links:
            url = link.get('url', '')
            if url and url not in seen:
                seen.add(url)
                unique_links.append(link)
        
        print(f"  ✓ Found {len(self.all_content['assignments'])} assignments")
        print(f"  ✓ Found {len(unique_links)} external links to follow")
        
        return unique_links
    
    async def scrape_assignments_list(self, course_id: str):
        """Scrape assignments and collect their external links"""
        assignments = []
        external_links = []
        
        await self.main_page.goto(f"{CANVAS_URL}/courses/{course_id}/assignments", wait_until='networkidle')
        await asyncio.sleep(2)
        
        content = await self.main_page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all assignment links
        assignment_links = []
        for link in soup.select('a[href*="/assignments/"]'):
            href = link.get('href', '')
            match = re.search(r'/assignments/(\d+)', href)
            if match:
                aid = match.group(1)
                if aid not in [a.get('id') for a in assignment_links]:
                    assignment_links.append({
                        'id': aid,
                        'url': f"{CANVAS_URL}/courses/{course_id}/assignments/{aid}"
                    })
        
        print(f"    Found {len(assignment_links)} assignments to scrape...")
        
        # Scrape each assignment in parallel batches
        batch_size = 5
        for i in range(0, len(assignment_links), batch_size):
            batch = assignment_links[i:i+batch_size]
            tasks = [self.scrape_single_assignment(course_id, a['id']) for a in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, dict):
                    assignments.append(result)
                    if result.get('external_links'):
                        external_links.extend(result['external_links'])
                    print(f"      ✓ {result.get('title', 'Unknown')[:50]}")
        
        return assignments, external_links
    
    async def scrape_single_assignment(self, course_id: str, assignment_id: str):
        """Scrape a single assignment and extract external links"""
        page = await self.get_page()
        try:
            url = f"{CANVAS_URL}/courses/{course_id}/assignments/{assignment_id}"
            await page.goto(url, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(1)
            
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Get title
            title = None
            for selector in ['h1.title', 'h1', '.assignment-title', '#assignment_show h1']:
                el = soup.select_one(selector)
                if el and el.get_text(strip=True):
                    title = el.get_text(strip=True)
                    break
            title = title or f"Assignment {assignment_id}"
            
            # Get description
            desc_el = soup.select_one('.description, .user_content, .assignment-description')
            description = desc_el.get_text(separator='\n', strip=True) if desc_el else ""
            description_html = str(desc_el) if desc_el else ""
            
            # Get due date
            due_el = soup.select_one('.date_text, .due_date_display, .assignment-date-due')
            due_date = due_el.get_text(strip=True) if due_el else None
            
            # Get points
            points_el = soup.select_one('.points_possible, .possible')
            points = points_el.get_text(strip=True) if points_el else None
            
            # Find ALL external links
            external_links = []
            for link in soup.select('a[href]'):
                href = link.get('href', '')
                if self.is_external_platform(href):
                    external_links.append({
                        'url': href,
                        'text': link.get_text(strip=True),
                        'source': 'assignment',
                        'assignment_id': assignment_id,
                        'assignment_title': title
                    })
            
            # Also check for iframes (embedded content)
            for iframe in soup.select('iframe[src]'):
                src = iframe.get('src', '')
                if self.is_external_platform(src):
                    external_links.append({
                        'url': src,
                        'text': 'Embedded content',
                        'source': 'assignment_iframe',
                        'assignment_id': assignment_id,
                        'assignment_title': title
                    })
            
            # Look for LTI launch buttons
            for btn in soup.select('a[class*="external_tool"], a[class*="lti"], button[data-url]'):
                href = btn.get('href') or btn.get('data-url', '')
                if href:
                    external_links.append({
                        'url': href,
                        'text': btn.get_text(strip=True) or 'External Tool',
                        'source': 'lti_tool',
                        'assignment_id': assignment_id,
                        'assignment_title': title
                    })
            
            return {
                'id': assignment_id,
                'title': title,
                'description': description,
                'description_html': description_html,
                'due_date': due_date,
                'points': points,
                'url': url,
                'external_links': external_links
            }
            
        except Exception as e:
            return {'id': assignment_id, 'error': str(e)}
        finally:
            await self.release_page(page)
    
    async def scrape_modules(self, course_id: str):
        """Scrape modules and collect external links"""
        external_links = []
        
        await self.main_page.goto(f"{CANVAS_URL}/courses/{course_id}/modules", wait_until='networkidle')
        await asyncio.sleep(2)
        
        # Expand all modules
        try:
            expand_buttons = await self.main_page.query_selector_all('.expand_module_link, .ig-header-collapse')
            for btn in expand_buttons[:20]:  # Limit to avoid infinite loops
                try:
                    await btn.click()
                    await asyncio.sleep(0.3)
                except:
                    pass
        except:
            pass
        
        await asyncio.sleep(1)
        content = await self.main_page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all links in modules
        for link in soup.select('.context_module a[href], .ig-row a[href]'):
            href = link.get('href', '')
            if self.is_external_platform(href):
                external_links.append({
                    'url': href,
                    'text': link.get_text(strip=True),
                    'source': 'module'
                })
        
        return external_links
    
    async def scrape_syllabus(self, course_id: str):
        """Scrape syllabus and collect external links"""
        external_links = []
        
        await self.main_page.goto(f"{CANVAS_URL}/courses/{course_id}/assignments/syllabus", wait_until='networkidle')
        await asyncio.sleep(1)
        
        content = await self.main_page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        syllabus_div = soup.select_one('#course_syllabus, .syllabus_content, .user_content')
        if syllabus_div:
            self.all_content['syllabus'] = {
                'html': str(syllabus_div),
                'text': syllabus_div.get_text(separator='\n', strip=True)
            }
            
            for link in syllabus_div.select('a[href]'):
                href = link.get('href', '')
                if self.is_external_platform(href):
                    external_links.append({
                        'url': href,
                        'text': link.get_text(strip=True),
                        'source': 'syllabus'
                    })
        
        return external_links
    
    def is_external_platform(self, url: str) -> bool:
        """Check if URL is an external learning platform"""
        if not url:
            return False
        url_lower = url.lower()
        for platform, patterns in EXTERNAL_PLATFORMS.items():
            for pattern in patterns:
                if pattern in url_lower:
                    return True
        return False
    
    def identify_platform(self, url: str) -> str:
        """Identify which platform a URL belongs to"""
        url_lower = url.lower()
        for platform, patterns in EXTERNAL_PLATFORMS.items():
            for pattern in patterns:
                if pattern in url_lower:
                    return platform
        return 'unknown'
    
    async def scrape_external_parallel(self, links: list):
        """Scrape all external links in parallel"""
        # Group by platform
        by_platform = {}
        for link in links:
            platform = self.identify_platform(link['url'])
            if platform not in by_platform:
                by_platform[platform] = []
            by_platform[platform].append(link)
        
        for platform, platform_links in by_platform.items():
            print(f"\n  📦 {platform.upper()}: {len(platform_links)} links")
            
            if platform == 'pearson':
                await self.scrape_pearson_mylab(platform_links)
            elif platform == 'gradescope':
                await self.scrape_gradescope(platform_links)
            else:
                await self.scrape_generic_external(platform, platform_links)
    
    async def scrape_pearson_mylab(self, links: list):
        """Scrape MyLab/Pearson content - actual homework problems"""
        print("    🔑 Navigating to MyLab...")
        
        # First, try to access MyLab through Canvas LTI launch
        for link in links[:1]:  # Just need one to establish session
            try:
                page = await self.get_page()
                await page.goto(link['url'], wait_until='networkidle', timeout=60000)
                await asyncio.sleep(3)
                
                # Check if we need to authorize
                current_url = page.url
                print(f"    Current URL: {current_url[:80]}...")
                
                # Wait for MyLab to load
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)
                
                # Now scrape what we can see
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Look for assignment list
                assignments_found = await self.extract_mylab_content(page, soup, link)
                
                await self.release_page(page)
                
                if assignments_found:
                    print(f"    ✓ Extracted content from MyLab")
                    break
                    
            except PlaywrightTimeout:
                print(f"    ⏱ Timeout loading MyLab link")
            except Exception as e:
                print(f"    ⚠ Error: {str(e)[:50]}")
        
        # Try remaining links in parallel
        batch_size = 3
        for i in range(1, len(links), batch_size):
            batch = links[i:i+batch_size]
            tasks = [self.scrape_mylab_single(link) for link in batch]
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def extract_mylab_content(self, page, soup, link_info):
        """Extract actual problems from MyLab page"""
        problems = []
        
        # MyLab has different layouts - try multiple selectors
        problem_selectors = [
            '.question-container',
            '.problem-container', 
            '.exercise',
            '[class*="question"]',
            '[class*="problem"]',
            '.assignment-question',
            '.homework-item'
        ]
        
        for selector in problem_selectors:
            elements = soup.select(selector)
            if elements:
                for el in elements:
                    problem_text = el.get_text(separator='\n', strip=True)
                    if problem_text and len(problem_text) > 20:
                        # Look for math content
                        math_elements = el.select('math, .MathJax, [class*="math"]')
                        math_content = [m.get_text(strip=True) for m in math_elements]
                        
                        problems.append({
                            'text': problem_text,
                            'math': math_content,
                            'html': str(el),
                            'source': link_info.get('assignment_title', 'MyLab'),
                            'platform': 'pearson'
                        })
        
        # Also try to get the assignment overview
        overview_selectors = ['.assignment-info', '.overview', '.instructions', '.assignment-header']
        for selector in overview_selectors:
            el = soup.select_one(selector)
            if el:
                self.all_content.setdefault('readings', []).append({
                    'title': link_info.get('assignment_title', 'MyLab Content'),
                    'content': el.get_text(separator='\n', strip=True),
                    'source': 'mylab'
                })
        
        if problems:
            self.all_content['problems'].extend(problems)
            return True
        
        # If no specific problems found, save the whole page content
        body = soup.select_one('body')
        if body:
            text = body.get_text(separator='\n', strip=True)
            if len(text) > 100:
                self.all_content.setdefault('external_content', {})['pearson'] = {
                    'assignment': link_info.get('assignment_title'),
                    'raw_content': text[:50000],  # Limit size
                    'url': link_info['url']
                }
                return True
        
        return False
    
    async def scrape_mylab_single(self, link):
        """Scrape a single MyLab link"""
        page = await self.get_page()
        try:
            await page.goto(link['url'], wait_until='networkidle', timeout=45000)
            await asyncio.sleep(2)
            
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            await self.extract_mylab_content(page, soup, link)
            print(f"      ✓ {link.get('text', link['url'])[:40]}")
            
        except Exception as e:
            pass  # Silent fail for parallel scrapes
        finally:
            await self.release_page(page)
    
    async def scrape_gradescope(self, links: list):
        """Scrape Gradescope for exam content"""
        print("    📝 Checking Gradescope...")
        
        for link in links:
            try:
                page = await self.get_page()
                await page.goto(link['url'], wait_until='networkidle', timeout=45000)
                await asyncio.sleep(2)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Look for assignment/exam info
                title_el = soup.select_one('h1, .assignment-title, .title')
                title = title_el.get_text(strip=True) if title_el else link.get('text', 'Gradescope Content')
                
                # Look for questions/problems
                questions = soup.select('.question, .problem, [class*="question"]')
                
                exam_data = {
                    'title': title,
                    'url': link['url'],
                    'questions': []
                }
                
                for q in questions:
                    q_text = q.get_text(separator='\n', strip=True)
                    if q_text:
                        exam_data['questions'].append({
                            'text': q_text,
                            'html': str(q)
                        })
                
                if exam_data['questions'] or title:
                    self.all_content['exams'].append(exam_data)
                    print(f"      ✓ {title[:40]}")
                
                await self.release_page(page)
                
            except Exception as e:
                print(f"      ⚠ Could not access Gradescope link")
    
    async def scrape_generic_external(self, platform: str, links: list):
        """Generic scraper for other platforms"""
        for link in links[:5]:  # Limit per platform
            try:
                page = await self.get_page()
                await page.goto(link['url'], wait_until='networkidle', timeout=30000)
                await asyncio.sleep(1)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                body = soup.select_one('body')
                if body:
                    text = body.get_text(separator='\n', strip=True)
                    if len(text) > 100:
                        self.all_content.setdefault('external_content', {})[platform] = {
                            'content': text[:30000],
                            'url': link['url']
                        }
                        print(f"      ✓ Extracted content from {platform}")
                
                await self.release_page(page)
                break  # Just need one successful scrape per platform
                
            except:
                pass
    
    async def save_all_content(self, course_id: str):
        """Save all scraped content to files"""
        # Main comprehensive file
        output_file = DATA_DIR / f"comprehensive_{course_id}.json"
        with open(output_file, 'w') as f:
            json.dump(self.all_content, f, indent=2)
        print(f"  ✓ Saved to {output_file}")
        
        # Also save problems separately for easy access
        if self.all_content['problems']:
            problems_file = DATA_DIR / f"problems_{course_id}.json"
            with open(problems_file, 'w') as f:
                json.dump(self.all_content['problems'], f, indent=2)
            print(f"  ✓ Saved {len(self.all_content['problems'])} problems to {problems_file}")
        
        # Summary stats
        print(f"\n📊 SCRAPE SUMMARY:")
        print(f"  - Assignments: {len(self.all_content['assignments'])}")
        print(f"  - Problems extracted: {len(self.all_content['problems'])}")
        print(f"  - Exams found: {len(self.all_content['exams'])}")
        print(f"  - External platforms: {list(self.all_content.get('external_content', {}).keys())}")
    
    async def close(self):
        """Clean up"""
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()


async def main():
    scraper = ComprehensiveScraper()
    
    try:
        await scraper.start()
        await scraper.login_and_verify()
        
        print("\n🔍 Finding your courses...")
        courses = await scraper.find_courses()
        
        if not courses:
            print("No courses found!")
            return
        
        print(f"\nFound {len(courses)} courses:")
        for i, course in enumerate(courses):
            print(f"  {i+1}. {course['name']}")
        
        # Find calculus course
        calc_course = None
        for course in courses:
            name = course['name'].lower()
            if 'calc' in name or '1220' in name or '1210' in name:
                calc_course = course
                break
        
        if calc_course:
            print(f"\n🎯 Found: {calc_course['name']}")
            choice = input("Scrape this course comprehensively? (y/n): ").strip().lower()
            if choice == 'y':
                await scraper.scrape_course_comprehensive(calc_course['id'], calc_course['name'])
        else:
            choice = input("\nEnter course number to scrape: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(courses):
                    c = courses[idx]
                    await scraper.scrape_course_comprehensive(c['id'], c['name'])
        
        print("\n✨ Comprehensive scrape complete!")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Scrape interrupted by user")
    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
