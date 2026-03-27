# Tier 4: Interactive Exploration - Implementation Plan

**Created:** 2026-03-27
**Status:** Planning
**Goal:** Enable natural language queries that generate custom guides on-demand

---

## Vision

**Current (Tier 3):** Generate static guides for common workflows
**Tier 4:** Answer specific "how do I..." questions with custom, on-demand guides

**Example Interaction:**
```
User: "How do I add pagination to my Django REST Framework API?"
Doxen: [Generates custom GUIDE-pagination.md on-the-fly]
       [Includes: pagination classes, URL parameters, response format]
       [Cites: Tier 2 APIs, source code examples, related guides]
```

---

## Tier 3 vs Tier 4

| Aspect | Tier 3 (Static) | Tier 4 (Interactive) |
|--------|-----------------|----------------------|
| **Guides** | Pre-defined topics | Custom, on-demand |
| **Questions** | "Getting Started", "Authentication" | "How do I add pagination?" |
| **Generation** | Batch, upfront | Single, just-in-time |
| **Caching** | All guides saved | Common questions cached |
| **Scope** | Broad workflows | Specific solutions |
| **Use Case** | Documentation site | Developer assistant |

---

## Architecture

### Mode C: Interactive Query → Custom Guide

```
User Question: "How do I add pagination to DRF?"
        ↓
1. Query Analysis (LLM)
   - Extract intent: "pagination"
   - Identify components: serializers, views, settings
   - Determine scope: API pagination patterns
        ↓
2. Context Loading (Smart)
   - Load relevant Tier 2: REFERENCE-VIEWS.md, REFERENCE-SERIALIZERS.md
   - Load source files: rest_framework/pagination.py
   - Skip irrelevant components (authentication, permissions)
        ↓
3. Guide Synthesis (LLM)
   - Generate custom guide for specific question
   - Include quick answer, detailed workflow, examples
   - Cite relevant APIs and source code
        ↓
4. Output
   - Return markdown guide
   - Optionally save to GUIDE-pagination.md for caching
        ↓
5. Follow-up (Optional)
   - User: "What about cursor pagination?"
   - System: Refines guide or generates addendum
```

### Key Differences from Tier 3

**Tier 3 (Batch):**
- Load ALL Tier 2 docs for topic
- Load ALL relevant source files
- Generate comprehensive guide

**Tier 4 (Interactive):**
- **Smart context loading:** Only load relevant Tier 2/source
- **Focused synthesis:** Answer specific question, not full topic
- **Conversational:** Support follow-up questions

---

## Components

### 1. Query Analyzer

**Purpose:** Parse user question to determine what to load

**Input:**
```
"How do I add pagination to my Django REST Framework API?"
```

**Output:**
```json
{
  "intent": "pagination",
  "framework": "django-rest-framework",
  "components": ["views", "serializers", "settings"],
  "scope": "api_pagination",
  "difficulty": "intermediate",
  "keywords": ["PageNumberPagination", "LimitOffsetPagination", "page_size"]
}
```

**Implementation:**
```python
class QueryAnalyzer:
    def analyze(self, question: str, project: str) -> Dict[str, Any]:
        # Use LLM to parse question
        prompt = f"""
        Analyze this developer question for {project}:
        "{question}"

        Extract:
        - Intent: What is the user trying to do?
        - Components: Which components are relevant?
        - Keywords: Key terms to search for
        - Difficulty: beginner/intermediate/advanced

        Return JSON.
        """
        return llm.analyze(prompt)
```

### 2. Context Loader (Smart)

**Purpose:** Load only relevant Tier 2 + source based on query analysis

**Input:**
```json
{
  "components": ["views", "serializers"],
  "keywords": ["PageNumberPagination", "LimitOffsetPagination"]
}
```

**Output:**
- Tier 2 excerpts (not full docs)
- Source code snippets (targeted, not full files)
- Related guides (if cached)

**Implementation:**
```python
class SmartContextLoader:
    def load(self, query_analysis: Dict, project_root: Path) -> Dict[str, str]:
        # Load Tier 2 docs
        tier2_context = self._load_tier2_excerpts(
            components=query_analysis["components"],
            keywords=query_analysis["keywords"]
        )

        # Load source snippets
        source_context = self._load_source_snippets(
            keywords=query_analysis["keywords"],
            components=query_analysis["components"]
        )

        return {
            "tier2_context": tier2_context,
            "source_context": source_context,
        }
```

### 3. Interactive Guide Generator

**Purpose:** Generate focused guide for specific question

**Different from Tier 3:**
- Shorter, more focused output
- Direct answer to question upfront
- Less comprehensive, more specific

**Template: interactive-guide.md.j2**
```markdown
# {{ question }}

**Quick Answer:** {{ quick_answer }}

## Solution

{{ step_by_step_solution }}

## Code Example

```{{ language }}
{{ working_code_example }}
```

## Explanation

{{ detailed_explanation }}

## Related Topics

- {{ related_topic_1 }}
- {{ related_topic_2 }}

## See Also

- [{{ related_guide }}]({{ guide_path }})
- [{{ api_reference }}]({{ api_path }})
```

### 4. Conversation Manager (Optional)

**Purpose:** Handle follow-up questions in context

**Example:**
```
User: "How do I add pagination?"
Doxen: [Generates pagination guide]

User: "What about cursor pagination specifically?"
Doxen: [Refines guide to focus on cursor pagination]
      [Keeps context from previous question]
```

**Implementation:**
```python
class ConversationManager:
    def __init__(self):
        self.history = []

    def ask(self, question: str) -> str:
        # Add to history
        self.history.append({"role": "user", "content": question})

        # Generate answer with context
        answer = self._generate_with_history(question)

        # Add to history
        self.history.append({"role": "assistant", "content": answer})

        return answer
```

---

## Implementation Phases

### Phase 1: Basic Interactive (Day 1)
- [ ] Create `QueryAnalyzer` (LLM-based intent extraction)
- [ ] Create `SmartContextLoader` (keyword-based filtering)
- [ ] Create `InteractiveGuideGenerator` (focused synthesis)
- [ ] Test: Single question → custom guide

**Goal:** Answer "How do I [X]?" questions

### Phase 2: Caching (Day 1-2)
- [ ] Cache common questions → static guides
- [ ] Index: question → guide_path mapping
- [ ] Fallback: Cache miss → generate on-demand

**Goal:** Fast responses for common questions

### Phase 3: Conversational (Day 2-3)
- [ ] Add `ConversationManager`
- [ ] Support follow-up questions
- [ ] Maintain context across turns

**Goal:** Multi-turn conversations

### Phase 4: Search Enhancement (Day 3+)
- [ ] Vector search for relevant Tier 2/source
- [ ] Semantic search instead of keyword matching
- [ ] RAG-style retrieval

**Goal:** Better context loading

---

## Use Cases

### Use Case 1: Specific How-To

**Input:**
```
"How do I add custom headers to my Django REST Framework responses?"
```

**Output:**
```markdown
# Adding Custom Headers to DRF Responses

**Quick Answer:** Override `finalize_response()` in your view or use middleware.

## Solution

### Option 1: View-Level Headers

Add headers in your view's response:

\`\`\`python
from rest_framework.views import APIView
from rest_framework.response import Response

class MyAPIView(APIView):
    def get(self, request):
        response = Response({"data": "value"})
        response['X-Custom-Header'] = 'custom-value'
        return response
\`\`\`

### Option 2: Override finalize_response()

...
```

### Use Case 2: Debugging Help

**Input:**
```
"Why am I getting 'Authentication credentials were not provided' in DRF?"
```

**Output:**
```markdown
# Troubleshooting: Authentication Credentials Error

**Quick Answer:** Your view requires authentication but the request doesn't include credentials.

## Common Causes

1. Missing authentication classes
2. Incorrect token format
3. Token not in request headers

## Solutions

...
```

### Use Case 3: Feature Comparison

**Input:**
```
"What's the difference between ModelSerializer and Serializer in DRF?"
```

**Output:**
```markdown
# ModelSerializer vs Serializer

**Quick Answer:** ModelSerializer auto-generates fields from a model, Serializer requires manual field definition.

## Comparison

| Feature | Serializer | ModelSerializer |
|---------|-----------|-----------------|
| Fields | Manual | Auto-generated |
| Validation | Manual | Model-based |
| Create/Update | Manual | Built-in |

...
```

---

## Cost Analysis

### Tier 3 (Batch Static)
- Generate 3 guides: $0.20
- Generate once, serve forever

### Tier 4 (Interactive)
- Per query: $0.05-0.15 (smaller context, focused output)
- Caching reduces repeated costs

**Strategy:**
- Cache common questions as static guides
- Generate on-demand for unique questions
- Trade-off: Cost vs. specificity

---

## User Interface Options

### Option A: CLI

```bash
doxen ask "How do I add pagination to DRF?"
```

### Option B: Web Interface

```
Doxen Chat
-----------
You: How do I add pagination to DRF?

Doxen: [Generates guide]

You: What about cursor pagination?

Doxen: [Refines guide]
```

### Option C: IDE Extension

```
Right-click → "Ask Doxen"
Popup: "How do I..."
```

### Option D: API Endpoint

```bash
curl -X POST /api/ask \
  -d '{"question": "How do I add pagination?", "project": "django-rest-framework"}'
```

**Recommendation:** Start with Option A (CLI), expand to API endpoint

---

## Technical Challenges

### Challenge 1: Context Size
**Problem:** Can't load all Tier 2 + source for every query
**Solution:** Smart context loading (keyword-based filtering)

### Challenge 2: Query Understanding
**Problem:** Ambiguous questions ("How do I use views?")
**Solution:** LLM-based intent extraction, clarifying questions

### Challenge 3: Cost Management
**Problem:** Every query costs $0.05-0.15
**Solution:** Cache common questions, reuse generated guides

### Challenge 4: Answer Quality
**Problem:** Focused answers might miss important context
**Solution:** Include "See Also" links to comprehensive guides

---

## Success Metrics

### Quality Metrics
- ✅ **Relevance:** Answer matches question intent
- ✅ **Accuracy:** Code examples are correct
- ✅ **Completeness:** Sufficient detail without overwhelming
- ✅ **Actionability:** User can implement solution immediately

### Performance Metrics
- ✅ **Response time:** < 10 seconds per query
- ✅ **Cost per query:** < $0.10 on average
- ✅ **Cache hit rate:** > 50% for common questions

### User Experience Metrics
- ✅ **Satisfaction:** User got answer they needed
- ✅ **Follow-up rate:** % of queries requiring clarification
- ✅ **Adoption:** % of users using interactive vs static guides

---

## Comparison with Alternatives

### Doxen Tier 4 vs GitHub Copilot Chat

| Feature | Doxen Tier 4 | Copilot Chat |
|---------|--------------|--------------|
| **Scope** | Project-specific | General programming |
| **Context** | Tier 2 + source | Web-scraped docs |
| **Output** | Structured guides | Conversational |
| **Caching** | Yes (static guides) | No |
| **Cost** | $0.05-0.15/query | $10-20/month flat |

**Advantage:** Project-specific, cites local docs, generates reusable guides

---

## Next Steps

### Immediate (Day 1)
1. Design `QueryAnalyzer` prompt
2. Implement `SmartContextLoader`
3. Create `interactive-guide.md.j2` template
4. Test on django-rest-framework

### Short-term (Week 1)
1. Build CLI: `doxen ask "..."`
2. Implement caching for common questions
3. Test on discourse, pandas

### Medium-term (Week 2-4)
1. Add conversation support (follow-ups)
2. Build web interface
3. Add vector search for better context loading

---

## Decision Points

### Decision 1: Caching Strategy

**Option A:** Cache all generated guides
- Pro: Fast for repeated questions
- Con: Disk space grows

**Option B:** Cache only common questions (top 20%)
- Pro: Balance speed + space
- Con: Need to track popularity

**Recommendation:** Start with Option B

### Decision 2: Context Loading Strategy

**Option A:** Keyword-based filtering
- Pro: Simple, fast
- Con: May miss relevant context

**Option B:** Vector search (semantic)
- Pro: Better relevance
- Con: Requires embeddings, more complex

**Recommendation:** Start with Option A (keywords), upgrade to Option B later

### Decision 3: Output Format

**Option A:** Full markdown guide (like Tier 3)
- Pro: Reusable, detailed
- Con: Slower, more expensive

**Option B:** Shorter, focused answer
- Pro: Faster, cheaper
- Con: Less comprehensive

**Recommendation:** Option B for interactive, Option A for caching

---

## Tier 4 Roadmap

```
Phase 1: Basic Interactive
  - QueryAnalyzer
  - SmartContextLoader
  - InteractiveGuideGenerator
  - CLI: doxen ask "..."

Phase 2: Caching
  - Question → Guide index
  - Cache common questions
  - Fast retrieval

Phase 3: Conversational
  - ConversationManager
  - Follow-up questions
  - Context preservation

Phase 4: RAG Enhancement
  - Vector search
  - Semantic retrieval
  - Better context loading

Phase 5: Multi-Modal
  - Diagram generation
  - Code execution
  - Live examples
```

**Current:** Planning complete → Ready for Phase 1 implementation

---

**Document Status:** ✅ Ready for Implementation
**Next Action:** Implement Phase 1 (Basic Interactive)
**Estimated Time:** 1-2 days for Phase 1
