# Calculus Mastery — Audit Verification Checklist

**Generated from**: Full codebase audit, visual analysis of every page, README comparison, and professional design research.

---

## 🔴 Critical Issues (Must Fix)

### 1. Missing My Course Page
- **Status**: ❌ NOT IMPLEMENTED
- **README claim**: "My Course" page with Canvas LMS integration and personal course tracking
- **Reality**: No `/course` route in `App.jsx`, no `Course.jsx` component exists
- **Fix**: Create `src/pages/Course.jsx` + `Course.module.css`, add `/course` route to `App.jsx`, implement course tracking UI
- **Verify**: Navigate to `/course` → page loads with course data

### 2. No AI Fallback
- **Status**: ❌ NOT IMPLEMENTED
- **README claim**: "Falls back to built-in knowledge base" if Copilot CLI unavailable
- **Reality**: `smart_ai_tutor.py` hard-fails with subprocess error if CLI not found
- **Fix**: Add try/except around CLI calls, implement fallback to pre-built responses or graceful error message
- **Verify**: Stop Copilot CLI → ask AI a question → get a useful response instead of an error

### 3. Dead Backend Files
- **Status**: ⚠️ Technical debt
- **Files**: `ai_tutor.py`, `copilot_ai_tutor.py`, `copilot_tutor.py`, `canvas_scraper.py`, `deep_teaching.py`, `deep_lessons.py`, `comprehensive_lessons.py`, `teaching_engine.py`
- **Reality**: None are imported by `server.py` — all dead code
- **Fix**: Archive to `backend/deprecated/` or delete with git history preserved
- **Verify**: `grep -r "import.*<filename>" backend/server.py` returns nothing for each

---

## ⚠️ Visual Polish Issues

### 4. Boilerplate Card Descriptions
- **Status**: ❌ BROKEN
- **Location**: Dashboard topic cards
- **Problem**: Every card shows "AI lesson, guided examples, and practice linked to this section."
- **Fix**: Generate unique descriptions per topic from curriculum data, or write manual descriptions
- **Verify**: Dashboard → read every card → all descriptions are unique and topic-specific

### 5. Empty Formula Grid Cells
- **Status**: ❌ BROKEN
- **Location**: Formulas page, every section
- **Problem**: 2-column grid with odd item counts leaves blank cells
- **Fix**: Use `grid-auto-flow: dense` or make last item `grid-column: 1 / -1` to span, or add content
- **Verify**: Formulas page → no visible empty gray placeholder cells

### 6. Orphaned Blue Dot (Practice)
- **Status**: ❌ COSMETIC BUG
- **Location**: Practice page, Session Engine card
- **Problem**: Stray blue dot element with no apparent purpose
- **Fix**: Remove the element or assign it a clear purpose (e.g., status indicator)
- **Verify**: Practice page → no floating dots without labels

### 7. Redundant Ask Tutor FAB
- **Status**: ⚠️ DESIGN CONFLICT
- **Location**: Practice page
- **Problem**: "Ask Tutor" floating button duplicates "Ask the Tutor" mode card
- **Fix**: Hide FAB on Practice page (it has its own tutor mode), or remove the mode card if FAB suffices
- **Verify**: Practice page → only ONE way to access the tutor

### 8. Asterisk Multiplication
- **Status**: ❌ COSMETIC BUG
- **Location**: Learn page worked examples
- **Problem**: `*` displayed instead of proper `·` or `×` for multiplication
- **Fix**: Replace `*` with `\cdot` or `\times` in LaTeX output, or fix `latex.js` preprocessing
- **Verify**: Learn page → no `*` characters adjacent to numbers in rendered content

### 9. Near-Invisible Progress Bar
- **Status**: ❌ BROKEN
- **Location**: Practice page, 4% progress bar
- **Problem**: Progress bar fill is too narrow to see at low percentages
- **Fix**: Set `min-width: 8px` on progress fill element
- **Verify**: Start practice at 1% mastery → progress bar is still visibly rendered

### 10. Settings Page Empty
- **Status**: ❌ MISSING FEATURES
- **Location**: Settings page
- **Problem**: Lists keyboard shortcuts but has no configurable settings
- **Fix**: Add real settings: theme selection, AI preferences, data export, Canvas sync configuration
- **Verify**: Settings page → at least 3 configurable settings that persist

---

## ✅ Working Features (Verified)

| Feature | Status | Notes |
|---------|--------|-------|
| Dashboard page loads | ✅ | Hero, topic cards, quick access visible |
| Learn page loads | ✅ | Sidebar + lesson content |
| Practice page loads | ✅ | Mode selector, problem generation |
| Formulas page loads | ✅ | Category sections with KaTeX |
| Settings page loads | ✅ | Keyboard shortcuts displayed |
| Dark theme | ✅ | Comprehensive token system |
| Light theme | ✅ | Functional but less polished |
| Theme toggle | ✅ | Persists across reloads |
| KaTeX rendering | ✅ | Formulas render in all contexts |
| 48 API endpoints | ✅ | All frontend calls have matching backends |
| Adaptive practice API | ✅ | Difficulty adjusts per endpoint |
| Global chat component | ✅ | Available on configured pages |
| Header navigation | ✅ | Glass capsule design, responsive |

---

## 📋 README Feature Matrix

| README Feature | Implemented | Page | Notes |
|----------------|-------------|------|-------|
| AI-powered tutoring | ✅ Partial | /practice, /learn | Works when Copilot CLI is available |
| Structured learning path | ✅ | /learn | Topic sidebar with ordered sections |
| Adaptive practice | ✅ | /practice | Multiple modes, difficulty scaling |
| Formula reference | ✅ Partial | /formulas | Has empty grid cells |
| Personal course tracking | ❌ | /course (missing) | Page doesn't exist |
| Canvas LMS integration | ❌ Partial | — | Backend ready, no frontend UI |
| Dark/light mode | ✅ | All | Toggle in header |
| Keyboard shortcuts | ✅ Partial | /settings | Listed but not all functional |
| Copilot CLI fallback | ❌ | — | Hard-fails without CLI |
| Progress analytics | ✅ Partial | /dashboard | Shows metrics but some are placeholder |

---

## 🎯 Verification Script

To test the full stack end-to-end:

```bash
# 1. Backend health check
curl -s http://localhost:8000/ | head -5

# 2. Curriculum topics load
curl -s http://localhost:8000/api/curriculum/topics | python3 -m json.tool | head -20

# 3. Formula data loads
curl -s http://localhost:8000/api/formulas/categories | python3 -m json.tool | head -20

# 4. Practice problem generation
curl -s -X POST http://localhost:8000/api/practice/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "limits", "difficulty": 3}' | python3 -m json.tool

# 5. AI tutor (if Copilot CLI available)
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is a derivative?"}' | python3 -m json.tool

# 6. Frontend serves
curl -s -o /dev/null -w "%{http_code}" http://localhost:2000/

# 7. All routes accessible (no 404)
for route in "/" "/learn" "/practice" "/formulas" "/settings"; do
  echo "$route: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:2000$route)"
done
```

---

## Priority Order for Fixes

1. **P0** — My Course page (missing feature), AI fallback (broken claim)
2. **P1** — Boilerplate descriptions, empty grid cells, asterisk multiplication
3. **P2** — Orphaned blue dot, redundant FAB, invisible progress bar, settings content
4. **P3** — Dead backend files cleanup, typography consistency pass, animation refinement
