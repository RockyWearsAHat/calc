"""
AI-Powered Course Analyzer
Analyzes scraped Canvas content to:
1. Identify key topics and their weight based on assignments/exams
2. Extract formulas and concepts from course materials  
3. Generate study guides based on YOUR course emphasis
4. Create practice problems that match YOUR exam style
"""
import json
import re
import os
from pathlib import Path
from collections import Counter, defaultdict

DATA_DIR = Path(__file__).parent / "data"

# Calc II curriculum mapping (section number -> topic)
CALC2_SECTIONS = {
    # Integration techniques
    "6.1": "areas_between_curves",
    "6.2": "volumes_disks_washers",
    "6.3": "volumes_shells",
    "6.4": "work_applications",
    "6.5": "average_value",
    "6.6": "physical_applications",
    "6.7": "physical_applications",
    # Integration techniques
    "7.1": "integration_by_parts",
    "7.2": "trig_integrals",
    "7.3": "trig_substitution",
    "7.4": "partial_fractions",
    "7.5": "integration_strategy",
    "7.7": "approximate_integration",
    "7.8": "improper_integrals",
    # Further applications
    "8.1": "arc_length",
    "8.2": "surface_area",
    # Parametric and Polar
    "10.1": "parametric_equations",
    "10.2": "parametric_calculus",
    "10.3": "polar_coordinates",
    "10.4": "polar_calculus",
    "12.1": "parametric_equations",
    "12.2": "parametric_calculus",
    # Sequences and Series
    "11.1": "sequences",
    "11.2": "series_intro",
    "11.3": "integral_test",
    "11.4": "comparison_tests",
    "11.5": "alternating_series",
    "11.6": "ratio_root_tests",
    "11.7": "series_strategy",
    "11.8": "power_series",
    "11.9": "power_series_representations",
    "11.10": "taylor_maclaurin",
    "11.11": "taylor_applications",
}

TOPIC_NAMES = {
    "areas_between_curves": "Areas Between Curves",
    "volumes_disks_washers": "Volumes (Disk/Washer Method)",
    "volumes_shells": "Volumes (Shell Method)",
    "work_applications": "Work Applications",
    "average_value": "Average Value of a Function",
    "physical_applications": "Physical Applications",
    "integration_by_parts": "Integration by Parts",
    "trig_integrals": "Trigonometric Integrals",
    "trig_substitution": "Trigonometric Substitution",
    "partial_fractions": "Partial Fractions",
    "integration_strategy": "Integration Strategy",
    "approximate_integration": "Approximate Integration",
    "improper_integrals": "Improper Integrals",
    "arc_length": "Arc Length",
    "surface_area": "Surface Area of Revolution",
    "parametric_equations": "Parametric Equations",
    "parametric_calculus": "Calculus with Parametric Curves",
    "polar_coordinates": "Polar Coordinates",
    "polar_calculus": "Calculus in Polar Coordinates",
    "sequences": "Sequences",
    "series_intro": "Introduction to Series",
    "integral_test": "Integral Test",
    "comparison_tests": "Comparison Tests",
    "alternating_series": "Alternating Series Test",
    "ratio_root_tests": "Ratio and Root Tests",
    "series_strategy": "Series Convergence Strategy",
    "power_series": "Power Series",
    "power_series_representations": "Power Series Representations",
    "taylor_maclaurin": "Taylor and Maclaurin Series",
    "taylor_applications": "Applications of Taylor Polynomials",
}

# Keywords for topic detection (fallback)
TOPIC_KEYWORDS = {
    'integration_by_parts': ['by parts', 'integration by parts', 'ibp', 'tabular'],
    'trig_integrals': ['sin^', 'cos^', 'tan^', 'sec^', 'trig integral', 'trigonometric integral'],
    'trig_substitution': ['trig sub', 'trigonometric substitution', 'sqrt(a^2', 'sqrt(x^2'],
    'partial_fractions': ['partial fraction', 'decomposition'],
    'improper_integrals': ['improper', 'infinity', '∞', 'diverge', 'converge'],
    'sequences': ['sequence', 'a_n', '{a_n}', 'monotonic', 'bounded'],
    'series_intro': ['series', 'σ', 'sum', 'geometric series', 'harmonic'],
    'integral_test': ['integral test', 'p-series'],
    'comparison_tests': ['comparison test', 'limit comparison', 'direct comparison'],
    'alternating_series': ['alternating', '(-1)^n', 'alternating series test'],
    'ratio_root_tests': ['ratio test', 'root test', 'lim |a_{n+1}/a_n|'],
    'power_series': ['power series', 'radius of convergence', 'interval of convergence', 'σ c_n'],
    'taylor_maclaurin': ['taylor', 'maclaurin', 'taylor series', 'taylor polynomial'],
    'parametric_equations': ['parametric', 'x(t)', 'y(t)', 'parameter'],
    'polar_coordinates': ['polar', 'r =', 'θ', 'theta', 'cardioid', 'rose', 'limacon'],
    'volumes_disks_washers': ['disk method', 'washer method', 'volume of revolution'],
    'volumes_shells': ['shell method', 'cylindrical shell'],
    'arc_length': ['arc length', 'length of curve'],
}


class CourseAnalyzer:
    def __init__(self):
        self.course_data = None
        self.analysis = {
            'topics_by_weight': {},
            'key_concepts': [],
            'exam_topics': [],
            'formulas_mentioned': [],
            'study_priorities': [],
            'practice_focus': [],
            'warnings': []
        }
    
    def load_course_data(self):
        """Load all scraped course data"""
        course_files = list(DATA_DIR.glob("course_*.json"))
        if not course_files:
            return None
        
        latest = max(course_files, key=lambda f: f.stat().st_mtime)
        with open(latest) as f:
            self.course_data = json.load(f)
        return self.course_data
    
    def extract_section_from_title(self, title):
        """Extract section number from assignment title like '11.3 HW - Taylor Series'"""
        match = re.search(r'(\d+\.\d+)', title)
        if match:
            return match.group(1)
        return None
    
    def analyze_topic_distribution(self):
        """Analyze which topics are most emphasized in the course"""
        topic_mentions = Counter()
        topic_assignments = defaultdict(list)
        
        if not self.course_data:
            return {}
        
        # Analyze assignments - extract section numbers
        for assignment in self.course_data.get('assignments', []):
            title = assignment.get('title', '')
            description = assignment.get('description_text', '').lower()
            
            # Try to extract section number
            section = self.extract_section_from_title(title)
            if section and section in CALC2_SECTIONS:
                topic = CALC2_SECTIONS[section]
                topic_mentions[topic] += 3  # Weight actual assignments heavily
                topic_assignments[topic].append(title)
            
            # Also check keywords in description
            full_text = f"{title} {description}".lower()
            for topic, keywords in TOPIC_KEYWORDS.items():
                for keyword in keywords:
                    if keyword.lower() in full_text:
                        topic_mentions[topic] += 1
                        if title not in topic_assignments[topic]:
                            topic_assignments[topic].append(title)
                        break
        
        # Calculate weights
        total = sum(topic_mentions.values()) or 1
        self.analysis['topics_by_weight'] = {
            topic: {
                'name': TOPIC_NAMES.get(topic, topic.replace('_', ' ').title()),
                'mentions': count,
                'weight': round(count / total * 100, 1),
                'assignments': topic_assignments.get(topic, [])
            }
            for topic, count in topic_mentions.most_common()
        }
        
        return self.analysis['topics_by_weight']
    
    def identify_current_topics(self):
        """Identify what's currently being studied based on recent assignments"""
        current = []
        
        if not self.course_data:
            return []
        
        # Look at assignments - assume recent ones are current
        assignments = self.course_data.get('assignments', [])[-10:]  # Last 10
        
        for assignment in assignments:
            title = assignment.get('title', '')
            section = self.extract_section_from_title(title)
            if section and section in CALC2_SECTIONS:
                topic = CALC2_SECTIONS[section]
                if topic not in current:
                    current.append(topic)
        
        return current
    
    def generate_study_priorities(self):
        """Generate prioritized study list"""
        priorities = []
        
        weights = self.analysis.get('topics_by_weight', {})
        current_topics = self.identify_current_topics()
        
        # Final exam critical topics (always high priority)
        final_critical = [
            'taylor_maclaurin', 'power_series', 'series_strategy',
            'integration_by_parts', 'partial_fractions', 'improper_integrals',
            'parametric_calculus', 'polar_calculus'
        ]
        
        # Build priority list
        all_topics = set(weights.keys()) | set(current_topics) | set(final_critical)
        
        for topic in all_topics:
            data = weights.get(topic, {'mentions': 0, 'weight': 0, 'assignments': []})
            base_score = data.get('weight', 0)
            
            # Boost current topics
            if topic in current_topics:
                base_score += 30
                priority = 'CURRENT'
            elif topic in final_critical:
                base_score += 20
                priority = 'HIGH'
            elif base_score > 10:
                priority = 'HIGH'
            elif base_score > 5:
                priority = 'MEDIUM'
            else:
                priority = 'REVIEW'
            
            priorities.append({
                'topic': topic,
                'name': TOPIC_NAMES.get(topic, topic.replace('_', ' ').title()),
                'priority': priority,
                'score': round(base_score, 1),
                'reason': self._get_priority_reason(topic, current_topics, final_critical, data),
                'assignments': data.get('assignments', [])
            })
        
        # Sort by priority then score
        priority_order = {'CURRENT': 0, 'HIGH': 1, 'MEDIUM': 2, 'REVIEW': 3}
        priorities.sort(key=lambda x: (priority_order.get(x['priority'], 4), -x['score']))
        
        self.analysis['study_priorities'] = priorities
        self.analysis['warnings'] = [p for p in priorities if p['priority'] in ['CURRENT', 'HIGH']]
        
        return priorities
    
    def _get_priority_reason(self, topic, current, critical, data):
        if topic in current:
            return "Currently studying - upcoming homework/exam"
        if topic in critical:
            return "Critical for final exam"
        if data.get('mentions', 0) > 0:
            return f"Mentioned in {data['mentions']} assignments"
        return "Standard Calc II topic - review as needed"
    
    def generate_study_guide(self):
        """Generate a comprehensive study guide"""
        self.analyze_topic_distribution()
        self.generate_study_priorities()
        
        current_topics = self.identify_current_topics()
        
        study_guide = {
            'generated_at': self.course_data.get('scraped_at') if self.course_data else None,
            'course_id': self.course_data.get('course_id') if self.course_data else None,
            'summary': {
                'total_assignments': len(self.course_data.get('assignments', [])) if self.course_data else 0,
                'total_modules': len(self.course_data.get('modules', [])) if self.course_data else 0,
                'current_focus': [TOPIC_NAMES.get(t, t) for t in current_topics]
            },
            'priorities': self.analysis['study_priorities'],
            'warnings': self.analysis['warnings'],
            'topic_breakdown': self.analysis['topics_by_weight'],
            'recommendations': self._generate_recommendations(current_topics)
        }
        
        # Save study guide
        output_file = DATA_DIR / "study_guide.json"
        with open(output_file, 'w') as f:
            json.dump(study_guide, f, indent=2)
        
        return study_guide
    
    def _generate_recommendations(self, current_topics):
        """Generate specific study recommendations"""
        recs = []
        
        # Current focus
        if current_topics:
            topic_names = [TOPIC_NAMES.get(t, t) for t in current_topics[:3]]
            recs.append({
                'type': 'CURRENT',
                'message': f"Current focus: {', '.join(topic_names)}. Master these before moving on.",
                'topics': current_topics[:3]
            })
        
        # Final exam prep
        recs.append({
            'type': 'FINAL',
            'message': "For the final: Series convergence tests are HEAVILY tested. Know all tests and when to use each.",
            'topics': ['series_strategy', 'ratio_root_tests', 'comparison_tests']
        })
        
        recs.append({
            'type': 'FINAL',
            'message': "Taylor series: Know common series (e^x, sin x, cos x, 1/(1-x)) and how to derive new ones.",
            'topics': ['taylor_maclaurin', 'power_series']
        })
        
        recs.append({
            'type': 'TECHNIQUE',
            'message': "Integration techniques: Practice recognizing WHICH technique to use. This is often harder than the technique itself.",
            'topics': ['integration_by_parts', 'trig_substitution', 'partial_fractions']
        })
        
        return recs


def analyze_course():
    """Main function to run analysis"""
    analyzer = CourseAnalyzer()
    
    if not analyzer.load_course_data():
        print("❌ No course data found. Run the scraper first:")
        print("   python scraper.py")
        return None
    
    print("🧠 Analyzing your course content...")
    guide = analyzer.generate_study_guide()
    
    print("\n" + "="*60)
    print("📊 STUDY GUIDE GENERATED")
    print("="*60)
    
    print(f"\n📚 Course Summary:")
    print(f"   - {guide['summary']['total_assignments']} assignments analyzed")
    if guide['summary']['current_focus']:
        print(f"   - Current focus: {', '.join(guide['summary']['current_focus'])}")
    
    print(f"\n🎯 STUDY PRIORITIES:")
    for p in guide['priorities'][:8]:
        emoji = "🔴" if p['priority'] == 'CURRENT' else "🟠" if p['priority'] == 'HIGH' else "🟡" if p['priority'] == 'MEDIUM' else "🟢"
        print(f"   {emoji} {p['name']}: {p['priority']} (score: {p['score']})")
    
    print(f"\n💡 RECOMMENDATIONS:")
    for rec in guide['recommendations']:
        print(f"   → {rec['message']}")
    
    print(f"\n✅ Full study guide saved to: backend/data/study_guide.json")
    
    return guide


if __name__ == "__main__":
    analyze_course()
