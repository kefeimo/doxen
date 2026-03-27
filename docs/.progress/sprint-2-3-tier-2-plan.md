# Sprint 2-3: Tier 2 Implementation Plan

**Sprint:** Weeks 3-5 (Estimated: 2-3 weeks)
**Goal:** Generate REFERENCE-{component}.md documentation
**Priority:** HIGHEST (Tier 2 = 27.0% of all docs)
**Target:** 80%+ API coverage on test projects

---

## Executive Summary

Implement component reference generation (Tier 2) building on the validated Tier 1 foundation. Test on 3 gold standard projects (mui, electron, django-rest-framework) that exemplify different component documentation patterns.

---

## Success Criteria

**Must Have:**
- [ ] Component grouping logic implemented
- [ ] REFERENCE-{component}.md generation working
- [ ] Test on 3 gold standard projects (mui, electron, django-rest-framework)
- [ ] 80%+ API coverage (classes, functions, endpoints extracted)
- [ ] Generated docs are accurate and readable

**Should Have:**
- [ ] Cross-references between components work
- [ ] Code examples included where applicable
- [ ] Configuration options extracted

**Nice to Have:**
- [ ] Executable code examples validated
- [ ] Type information preserved
- [ ] Deprecation warnings included

---

## Test Projects Analysis

### 1. MUI (Material-UI) - 320 doc files
**Pattern:** Per-component API docs

**Example structure:**
```
mui/docs/data/
├── base/
│   ├── components/
│   │   ├── button/
│   │   │   └── button.md  # Individual component API
│   │   ├── text-field/
│   │   └── ...
```

**What to extract:**
- React components (props, types, events)
- Component hierarchy
- Design patterns (controlled/uncontrolled, composition)

**Expected output:**
```
docs/
├── REFERENCE-COMPONENTS.md  (or)
├── REFERENCE-BUTTON.md
├── REFERENCE-TEXTFIELD.md
└── REFERENCE-DIALOG.md
```

---

### 2. Electron - 275 doc files
**Pattern:** `/api/` folder with module docs

**Example structure:**
```
electron/docs/api/
├── command-line.md
├── safe-storage.md
├── touch-bar-slider.md
└── ...
```

**What to extract:**
- Node.js modules (classes, methods, events)
- Main process vs renderer process APIs
- Platform-specific APIs

**Expected output:**
```
docs/
├── REFERENCE-API.md  (overview)
├── REFERENCE-COMMAND-LINE.md
├── REFERENCE-SAFE-STORAGE.md
└── REFERENCE-TOUCH-BAR.md
```

---

### 3. Django REST Framework - 70 doc files
**Pattern:** `/api-guide/` with serializers, views, etc.

**Example structure:**
```
django-rest-framework/docs/api-guide/
├── serializers.md
├── views.md
├── routers.md
└── authentication.md
```

**What to extract:**
- Python classes (serializers, views, viewsets)
- REST patterns (authentication, permissions, pagination)
- Configuration options

**Expected output:**
```
docs/
├── REFERENCE-API.md  (overview)
├── REFERENCE-SERIALIZERS.md
├── REFERENCE-VIEWS.md
└── REFERENCE-AUTHENTICATION.md
```

---

## Implementation Plan

### Phase 1: Component Grouping (Week 1)

**Goal:** Group files into logical components

**Tasks:**
1. **Enhance RepositoryAnalyzer**
   - Add `group_by_component()` method
   - Detect component boundaries (directories, modules, namespaces)
   - Handle different languages (Python packages, JS modules, etc.)

2. **Create Component Detection Logic**
   - Heuristic: Group by directory structure (e.g., `src/components/button/`)
   - Semantic: Use LLM to understand component boundaries
   - Hybrid: Combine both approaches

3. **Test on 3 projects**
   - mui: Should detect ~50+ components (Button, TextField, Dialog, etc.)
   - electron: Should detect ~20+ API modules (command-line, safe-storage, etc.)
   - django-rest-framework: Should detect ~10+ API concepts (serializers, views, etc.)

**Deliverables:**
- [ ] Enhanced `RepositoryAnalyzer.group_by_component()`
- [ ] Component grouping results for 3 test projects
- [ ] Validation: Manual review of component groups (are they sensible?)

---

### Phase 2: Component Analysis (Week 2)

**Goal:** Deep-dive into each component to extract APIs

**Tasks:**
1. **Create ComponentAnalyzer Agent**
   - Input: Component file group (e.g., all files in `src/button/`)
   - Output: Structured API data (classes, functions, props, events)
   - Use AST + LLM for hybrid extraction

2. **Extract API Elements**
   - **Classes:** Name, methods, properties, inheritance
   - **Functions:** Name, parameters, return types, docstrings
   - **Components (React/Vue):** Props, events, slots
   - **Endpoints (REST APIs):** Method, path, request/response schemas

3. **Generate Structured Data**
   - JSON intermediate format for API data
   - Include source file references (file:line)
   - Preserve type information

**Deliverables:**
- [ ] `ComponentAnalyzer` agent implemented
- [ ] API extraction working for Python, JavaScript
- [ ] Structured JSON output for each component

---

### Phase 3: REFERENCE-*.md Generation (Week 2-3)

**Goal:** Generate readable REFERENCE-{component}.md files

**Tasks:**
1. **Create REFERENCE Template**
   - Consistent structure across all components
   - Sections: Overview, API Reference, Examples, Configuration, Related Components

2. **Update DocGenerator**
   - New method: `generate_reference_docs(components: Dict)`
   - Generate one REFERENCE-{component}.md per component
   - Include cross-references (links to related components)

3. **Generate for Test Projects**
   - mui: Generate REFERENCE-BUTTON.md, REFERENCE-TEXTFIELD.md, etc.
   - electron: Generate REFERENCE-COMMAND-LINE.md, etc.
   - django-rest-framework: Generate REFERENCE-SERIALIZERS.md, etc.

**Deliverables:**
- [ ] REFERENCE-*.md template defined
- [ ] DocGenerator.generate_reference_docs() implemented
- [ ] Generated docs for 3 test projects

---

### Phase 4: Validation & Refinement (Week 3)

**Goal:** Achieve 80%+ API coverage

**Tasks:**
1. **Coverage Analysis**
   - Compare generated docs vs ground truth (gold standard docs)
   - Measure: % of classes/functions/components documented
   - Target: ≥80% coverage

2. **Quality Review**
   - Manual review of 10-20 generated docs
   - Check: Accuracy, readability, completeness
   - Fix: Common issues and patterns

3. **Cross-References**
   - Ensure links between components work
   - Add "See Also" sections
   - Link to Tier 1 docs (ARCHITECTURE.md)

**Deliverables:**
- [ ] Coverage metrics for 3 test projects
- [ ] Quality assessment report
- [ ] Refined documentation generation

---

## Technical Architecture

### New Components

```
src/doxen/
├── agents/
│   ├── component_analyzer.py       # NEW: Deep-dive component analysis
│   ├── repository_analyzer.py      # ENHANCED: Add group_by_component()
│   └── doc_generator.py            # ENHANCED: Add generate_reference_docs()
├── extractors/
│   ├── component_grouper.py        # NEW: Component boundary detection
│   └── api_extractor.py            # NEW: Extract classes/functions/APIs
└── templates/
    └── reference.md.j2             # NEW: REFERENCE-*.md template
```

### Data Flow

```
Repository
    ↓
RepositoryAnalyzer.group_by_component()
    ↓ (component groups)
ComponentAnalyzer.analyze(component_files)
    ↓ (structured API data)
DocGenerator.generate_reference_docs()
    ↓
REFERENCE-{component}.md
```

---

## Example Output

### REFERENCE-BUTTON.md (for mui)

```markdown
---
component: Button
category: Components
tier: 2
api_coverage: 95%
---

# Button Component Reference

## Overview

Material-UI Button component for user interactions.

## API Reference

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'text' \| 'contained' \| 'outlined'` | `'text'` | The variant to use |
| `color` | `'primary' \| 'secondary' \| ...` | `'primary'` | The color of the component |
| `size` | `'small' \| 'medium' \| 'large'` | `'medium'` | The size of the button |
| `disabled` | `boolean` | `false` | If true, the button is disabled |
| `onClick` | `(event: MouseEvent) => void` | - | Callback fired on click |

### Events

- `onClick`: Fired when button is clicked

### CSS Classes

- `.MuiButton-root`: Styles applied to the root element
- `.MuiButton-text`: Styles applied if `variant="text"`

## Usage Examples

```jsx
import { Button } from '@mui/material';

// Basic button
<Button>Click me</Button>

// Contained button with color
<Button variant="contained" color="primary">
  Submit
</Button>

// Outlined button with icon
<Button variant="outlined" startIcon={<SaveIcon />}>
  Save
</Button>
```

## Configuration

See [Theme customization](../ARCHITECTURE.md#theming) for global button styling.

## Related Components

- [IconButton](REFERENCE-ICONBUTTON.md) - For icon-only buttons
- [ButtonGroup](REFERENCE-BUTTONGROUP.md) - For grouped buttons
- [LoadingButton](REFERENCE-LOADINGBUTTON.md) - Button with loading state

## Source

- Source file: `src/Button/Button.tsx` ([view](https://github.com/mui/material-ui/blob/master/packages/mui-material/src/Button/Button.tsx))
- Documentation: `docs/data/base/components/button/button.md`
```

---

## Risks & Mitigation

### Risk 1: Component Boundaries Unclear
**Impact:** Medium - May group files incorrectly
**Mitigation:**
- Start with directory-based grouping (simple, predictable)
- Use LLM for semantic validation
- Manual review of first 5-10 components

### Risk 2: Language/Framework Diversity
**Impact:** High - Python, JS, Ruby have different structures
**Mitigation:**
- Implement language-specific extractors
- Test on all 3 projects (Python: DRF, JS: mui+electron)
- Focus on common patterns first (classes, functions)

### Risk 3: 80% Coverage Hard to Achieve
**Impact:** Medium - May not meet target
**Mitigation:**
- Define coverage clearly (what counts as "documented"?)
- Focus on public APIs only (skip private/internal)
- Iterate: Start with 60%, improve to 80%

---

## Timeline

**Week 1:** Component grouping + initial ComponentAnalyzer
**Week 2:** API extraction + REFERENCE-*.md generation
**Week 3:** Testing, validation, refinement

**Total:** 2-3 weeks (depending on complexity)

---

## Next Steps

### Immediate (This Session)
1. Update PROGRESS.md with Sprint 2-3 status
2. Create skeleton for ComponentAnalyzer agent
3. Enhance RepositoryAnalyzer with basic component grouping
4. Test component grouping on 1 project (start with mui or django-rest-framework)

### This Week
- Complete Phase 1 (Component Grouping)
- Start Phase 2 (ComponentAnalyzer)

### Next Week
- Complete Phase 2-3 (API extraction + doc generation)

### Week After
- Phase 4 (Validation, achieve 80% coverage)

---

## Open Questions

1. **Component naming:** REFERENCE-BUTTON.md vs REFERENCE-Components-Button.md?
   - **Decision:** Keep flat for now (REFERENCE-BUTTON.md)

2. **One file per component or grouped?**
   - **mui:** Individual files (50+ components)
   - **electron:** Individual files (20+ modules)
   - **django-rest-framework:** Individual files (10+ concepts)
   - **Decision:** Individual files for consistency

3. **Handle nested components?**
   - Example: Button > IconButton > LoadingButton
   - **Decision:** Flat structure, use "Related Components" for hierarchy

4. **What counts as 80% coverage?**
   - **Definition:** 80% of public classes + public functions documented
   - Exclude: Private methods, internal utilities, test files

---

**Status:** PLANNING COMPLETE ✅
**Ready to begin:** Phase 1 (Component Grouping)
