# Documentation Topic Coverage Strategy

**Created:** 2026-03-27
**Question:** How do we determine what documentation topics to generate?

---

## The Problem

**Ground Truth (django-rest-framework):**
- 7 tutorial guides (quickstart → advanced)
- 8 topic guides (CORS, nested serializers, etc.)
- Total: 15 integration guides

**We Generated:**
- 3 guides (Getting Started, Authentication, Serialization)
- Coverage: 20% (3/15)

**Question:** How do we know what else to generate to reach 100% coverage?

---

## Strategy 1: Enumerate from Ground Truth (If Available)

**When ground truth docs exist:**

### Step 1: Extract Topic Inventory

```python
def extract_ground_truth_topics(docs_dir: Path) -> List[Dict]:
    """Extract all topics from existing documentation."""

    topics = []

    # Scan tutorial guides
    for guide_file in (docs_dir / "tutorial").glob("*.md"):
        topics.append({
            "name": extract_title(guide_file),
            "type": "tutorial",
            "file": guide_file.name,
            "difficulty": "beginner" if "quickstart" in guide_file.name else "intermediate"
        })

    # Scan topic guides
    for guide_file in (docs_dir / "topics").glob("*.md"):
        topics.append({
            "name": extract_title(guide_file),
            "type": "topic",
            "file": guide_file.name,
            "difficulty": "advanced"
        })

    return topics
```

**Result for django-rest-framework:**
```json
[
  {"name": "Quickstart", "type": "tutorial", "difficulty": "beginner"},
  {"name": "Serialization", "type": "tutorial", "difficulty": "beginner"},
  {"name": "Requests and Responses", "type": "tutorial", "difficulty": "beginner"},
  {"name": "Class-based Views", "type": "tutorial", "difficulty": "intermediate"},
  {"name": "Authentication and Permissions", "type": "tutorial", "difficulty": "intermediate"},
  {"name": "Relationships and Hyperlinked APIs", "type": "tutorial", "difficulty": "intermediate"},
  {"name": "Viewsets and Routers", "type": "tutorial", "difficulty": "intermediate"},
  {"name": "AJAX, CSRF & CORS", "type": "topic", "difficulty": "advanced"},
  {"name": "Browsable API", "type": "topic", "difficulty": "advanced"},
  {"name": "Writable Nested Serializers", "type": "topic", "difficulty": "advanced"},
  ...
]
```

### Step 2: Map to Components

```python
def map_topics_to_components(topics: List[Dict], components: List[Dict]) -> Dict:
    """Map each topic to relevant Tier 2 components."""

    topic_mapping = {}

    for topic in topics:
        # Keywords extraction
        keywords = extract_keywords(topic["name"])

        # Find relevant components
        relevant_components = []
        for component in components:
            if any(kw in component["name"].lower() for kw in keywords):
                relevant_components.append(component)

        topic_mapping[topic["name"]] = {
            "tier2_refs": [f"REFERENCE-{c['name'].upper()}.md" for c in relevant_components],
            "source_files": [f["path"] for c in relevant_components for f in c.get("files", [])[:3]]
        }

    return topic_mapping
```

**Result:**
```json
{
  "Quickstart": {
    "tier2_refs": ["REFERENCE-SERIALIZERS.md", "REFERENCE-VIEWS.md"],
    "source_files": ["serializers.py", "views.py"]
  },
  "Writable Nested Serializers": {
    "tier2_refs": ["REFERENCE-SERIALIZERS.md"],
    "source_files": ["serializers.py", "fields.py"]
  }
}
```

### Step 3: Generate Missing Topics

```python
# Generate all topics from ground truth
for topic in topics:
    if not guide_exists(topic["name"]):
        guide_generator.generate(
            topic=topic["name"],
            tier2_refs=topic_mapping[topic["name"]]["tier2_refs"],
            source_files=topic_mapping[topic["name"]]["source_files"]
        )
```

**Pros:**
- ✅ Guaranteed to reach 100% coverage
- ✅ Topics proven useful (they exist in ground truth)
- ✅ Easy to measure progress (N/15 guides complete)

**Cons:**
- ❌ Requires ground truth to exist
- ❌ May duplicate content (if ground truth has redundancy)
- ❌ Doesn't work for new projects

---

## Strategy 2: Discover from Codebase (Proactive)

**When NO ground truth exists** (like most projects):

### Step 1: Analyze API Surface

```python
def discover_topics_from_apis(tier2_docs: List[Path]) -> List[Dict]:
    """Discover topics by analyzing API patterns."""

    topics = []

    # Parse all Tier 2 docs
    all_apis = []
    for doc in tier2_docs:
        apis = parse_reference_doc(doc)
        all_apis.extend(apis)

    # Cluster by functionality
    clusters = cluster_by_functionality(all_apis)

    # Generate topic for each cluster
    for cluster in clusters:
        topics.append({
            "name": cluster["name"],
            "apis": cluster["apis"],
            "difficulty": infer_difficulty(cluster),
            "priority": cluster["size"]  # Larger clusters = more important
        })

    return topics
```

**Example for django-rest-framework:**
```python
# Discovered clusters:
{
  "Serialization": {
    "apis": ["Serializer", "ModelSerializer", "Field", "ValidationError"],
    "size": 45,  # 45 APIs related to serialization
    "priority": "high"
  },
  "Authentication": {
    "apis": ["BaseAuthentication", "TokenAuthentication", "SessionAuthentication"],
    "size": 12,
    "priority": "medium"
  },
  "Pagination": {
    "apis": ["PageNumberPagination", "LimitOffsetPagination", "CursorPagination"],
    "size": 8,
    "priority": "low"
  }
}
```

### Step 2: Prioritize Topics

**Prioritization Criteria:**
1. **API Coverage:** How many APIs does this topic cover?
2. **Dependency Order:** Prerequisites (auth before permissions)
3. **User Journey:** Beginner → Intermediate → Advanced
4. **Frequency:** How often is this API used? (if we have usage data)

**Priority Ranking:**
```python
priorities = sorted(topics, key=lambda t: (
    -t["size"],  # Larger clusters first
    t["difficulty"],  # Beginner before advanced
    -t["cross_component_score"]  # Topics touching multiple components
))
```

**Result:**
```
1. Quickstart (size: 15, beginner, 3 components)
2. Serialization (size: 45, beginner, 2 components)
3. Views (size: 32, intermediate, 2 components)
4. Authentication (size: 12, intermediate, 3 components)
5. Pagination (size: 8, advanced, 1 component)
...
```

### Step 3: Generate in Priority Order

```python
for topic in priorities[:10]:  # Top 10 topics
    guide_generator.generate(
        topic=topic["name"],
        tier2_refs=topic["tier2_refs"],
        source_files=topic["source_files"]
    )
```

**Pros:**
- ✅ Works without ground truth
- ✅ Data-driven priorities
- ✅ Covers actual codebase surface

**Cons:**
- ❌ May miss important but small topics
- ❌ Clustering quality depends on heuristics
- ❌ Hard to validate without ground truth

---

## Strategy 3: Query-Based Discovery (Reactive - Tier 4)

**Generate topics based on user queries:**

### Step 1: Track Common Questions

```python
# Users ask questions
questions = [
    "How do I add pagination?",
    "How do I handle file uploads?",
    "How do I implement custom authentication?",
    ...
]

# Track frequency
question_frequency = Counter(questions)
```

### Step 2: Cache as Static Guides

```python
# Generate guide for top N questions
for question, count in question_frequency.most_common(20):
    if count > 10:  # Asked more than 10 times
        topic = extract_topic(question)  # "pagination", "authentication"

        # Generate and cache as static guide
        guide_generator.generate(topic=topic)
        cache_mapping[question] = f"GUIDE-{topic}.md"
```

### Step 3: Grow Coverage Organically

**Coverage grows over time:**
- Week 1: 5 guides (most common questions)
- Month 1: 15 guides (common + edge cases)
- Year 1: 50 guides (comprehensive coverage)

**Pros:**
- ✅ User-driven priorities (actual needs)
- ✅ No upfront generation cost
- ✅ Cache optimizes for common queries

**Cons:**
- ❌ Reactive (users must ask first)
- ❌ May miss important but uncommon topics
- ❌ Takes time to reach full coverage

---

## Strategy 4: Hybrid (Recommended)

**Combine all three approaches:**

### Phase 1: Bootstrap from Ground Truth (If Available)

```python
if ground_truth_exists:
    topics = extract_ground_truth_topics(docs_dir)
    # Generate top 10 most important
    for topic in prioritize(topics)[:10]:
        generate_guide(topic)
```

### Phase 2: Discover from Codebase

```python
# Analyze Tier 2 APIs
discovered_topics = discover_topics_from_apis(tier2_docs)

# Fill gaps not covered by ground truth
for topic in discovered_topics:
    if not guide_exists(topic["name"]):
        generate_guide(topic)
```

### Phase 3: Expand Based on Queries (Tier 4)

```python
# As users ask questions, cache new guides
@app.route("/ask")
def ask(question):
    topic = extract_topic(question)

    if not guide_exists(topic):
        # Generate on-demand
        guide = guide_generator.generate(topic)
        cache_guide(topic, guide)

    return load_guide(topic)
```

---

## Coverage Metrics

### How to Measure "Complete" Coverage?

**Metric 1: Ground Truth Coverage** (if available)
```
Coverage = (Generated Guides / Ground Truth Guides) × 100%
Example: 3/15 = 20%
```

**Metric 2: API Coverage**
```
Coverage = (APIs Documented in Guides / Total APIs) × 100%
Example: Guides cover 120/211 APIs = 56.9%
```

**Metric 3: Topic Coverage** (semantic)
```
Topics = {Serialization, Authentication, Views, Pagination, Filtering, ...}
Coverage = (Topics with Guides / Total Topics) × 100%
Example: 5/12 topics = 41.7%
```

**Metric 4: User Query Coverage** (Tier 4)
```
Coverage = (Questions with Cached Guides / Total Unique Questions) × 100%
Example: 20/45 questions = 44.4%
```

---

## Practical Implementation

### For django-rest-framework (Ground Truth Available)

**Step 1:** Extract topics from `/tutorial/` and `/topics/`
```bash
ls experimental/projects/django-rest-framework/docs/tutorial/
ls experimental/projects/django-rest-framework/docs/topics/
```

**Step 2:** Generate configuration
```python
guides_config = [
    {"topic": "Quickstart", "source": "tutorial/quickstart.md"},
    {"topic": "Serialization", "source": "tutorial/1-serialization.md"},
    {"topic": "Class-based Views", "source": "tutorial/3-class-based-views.md"},
    {"topic": "Writable Nested Serializers", "source": "topics/writable-nested-serializers.md"},
    ...
]
```

**Step 3:** Batch generate all 15 guides
```python
for config in guides_config:
    guide_generator.generate(
        topic=config["topic"],
        tier2_refs=map_to_tier2(config["topic"]),
        source_files=map_to_source(config["topic"])
    )
```

**Result:** 15/15 guides = 100% coverage

### For discourse (No Ground Truth)

**Step 1:** Analyze Tier 2 docs
```python
tier2_docs = [
    "REFERENCE-HELPERS.md",
    "REFERENCE-MAILERS.md",
    "REFERENCE-CONTROLLERS.md"
]
```

**Step 2:** Discover topics
```python
topics = discover_topics_from_apis(tier2_docs)
# Result: ["Sending Emails", "View Helpers", "Background Jobs", ...]
```

**Step 3:** Generate by priority
```python
for topic in prioritize(topics)[:10]:
    guide_generator.generate(topic)
```

**Result:** 10 guides covering major workflows

---

## Summary: Answering Your Question

**"How do we determine documentation topic coverage?"**

**Answer:** Use a **hybrid strategy**:

1. **If ground truth exists:** Enumerate all topics → Generate all → 100% coverage
2. **If no ground truth:** Discover topics from API clustering → Prioritize → Generate top N
3. **Over time:** Use Tier 4 queries to discover missing topics → Cache → Grow organically

**Coverage Metrics:**
- Ground truth: N/M guides (e.g., 3/15 = 20%)
- API coverage: APIs in guides / Total APIs (e.g., 120/211 = 57%)
- Topic coverage: Topics with guides / Total topics (e.g., 5/12 = 42%)

**For Production:**
- Start with top 10 priority topics (80/20 rule)
- Expand based on usage analytics
- Reach 100% over time (not upfront)

---

## Next Steps

1. Implement `extract_ground_truth_topics()` for django-rest-framework
2. Implement `discover_topics_from_apis()` for projects without ground truth
3. Run Tier 3 validation to measure current coverage quality
4. Decide: Generate all 15 topics now, or prioritize top 10?

**Does this answer your question about topic coverage strategy?**
