# Team Intelligence Framework - TODO & Status

**Last updated**: 2025-12-12  
**Status**: All 35 personas refactored to v1.2; framework architecture stabilized; {PROJECT_ROOT} pattern implemented

---

## COMPLETED (This Session)

### Architecture & Structure
- ✅ Expertise domain deference model implemented across all 5 domains
- ✅ Layered context_configuration structure (domain-level + project-level)
  - Gaming: domain + hero_heaven project
  - Writing: domain + screenplays project
- ✅ AI Development domain created (llm_prompt_specialist)
- ✅ Teams restructured (cross-domain in root `/teams/`, domain-specific in `/personas/{domain}/teams/`)
- ✅ EXPERTISE_DOMAINS.md comprehensive documentation (5 domains + project_lead special reference)
- ✅ {PROJECT_ROOT} variable pattern implemented for external project references (hero_heaven example)

### Personas Refactored (35 total)
- ✅ Financial: 6 personas (investment_advisor, tax_strategist, healthcare_expert, social_security_specialist, insurance_analyst, estate_planner)
- ✅ Development: 9 personas (experienced_developer, react_specialist, flutter_architect, security_specialist, cloud_architect, blits_developer, lightning_developer, ux_ui_strategist, ux_designer)
- ✅ Gaming: 3 personas (ttrpg_game_architect, lore_keeper, mythweaver)
- ✅ Writing: 4 personas (screenwriter, dialog_coach, science_advisor, director_of_photography)
- ✅ AI Development: 1 persona (llm_prompt_specialist)

### Teams
- ✅ 4 domain-specific teams (retirement_planning, react_fullstack, flutter_mobile_development, hero_heaven_worldbuilding)
- ✅ 1 cross-domain team (intelligence_framework_team in `/personas/ai_development/teams/`)

---

## PENDING

### High Priority

#### 0. Documentation: {PROJECT_ROOT} Variable Pattern (NEW - 2025-12-12)
- **What this is**: Implementation of external project reference pattern using `{PROJECT_ROOT}` variable in context_configuration.json
- **Status**: Pattern implemented in hero_heaven; needs documentation update
- **Affected files to update**:
  - **CONFIG_REFERENCE.md**: Add project-level context_configuration.json example showing {PROJECT_ROOT} pattern and how it resolves
  - **ARCHITECTURAL_DECISIONS.md**: Document {PROJECT_ROOT} as implementation detail under Decision 1 (Two-Layer Configuration Structure)
  - **PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md**: Add section "Creating Project-Level Contexts with External References" explaining:
    - When to use {PROJECT_ROOT} (external projects)
    - How to set project_root field
    - How framework resolves {PROJECT_ROOT} variables
    - Examples from hero_heaven
- **Additional validation**:
  - Check `/personas/writing/screenplays/context_configuration_screenplays.json` — determine if screenplays project is external and needs same {PROJECT_ROOT} pattern
  - If yes, update it to match hero_heaven pattern for consistency
- **Why**: Makes external project reference pattern explicit and reusable; enables other projects to follow same architecture
- **Depends on**: None
- **Effort**: 2-3 hours

#### 1. Documentation: Team Structure & Architecture
- **File**: PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md
- **Work**: Add section documenting:
  - Cross-domain teams in root `/teams/`
  - Domain-specific teams in `/personas/{domain}/teams/`
  - Layered context_configuration pattern
  - When to create a team vs relying on expertise_domain deference
- **Depends on**: None (can start anytime)
- **Effort**: 1-2 hours

#### 2. Documentation: Framework States & Controls
- **File**: New section in USER_GUIDE.md or CONFIG_REFERENCE.md
- **Work**: Document framework control patterns mentioned in initial brief:
  - "personas on" / "personas off"
  - "use this team as the set of personas"
  - How to activate specific personas or teams
- **Depends on**: Requires clarification on desired implementation
- **Effort**: 2-3 hours (design + doc)

#### 3. Cleanup: Remove Outdated Files
- **Files to delete**:
  - `.devnotes/REFACTORING_PLAN.md` (outdated; replaced by this TODO file)
  - `.devnotes/REFACTORING_REFERENCE.md` (will be superseded by HOW_TO_CREATE_A_PERSONA.md)
- **Effort**: 15 min

### Medium Priority

#### 4. Validation: Spot-Check Personas
- **Work**: Sample 5-6 personas across domains to verify:
  - Expertise domain deference consistency
  - Reference context & guide fields present
  - No orphaned fields or outdated patterns
  - Team references valid
- **Depends on**: None
- **Effort**: 1-2 hours

#### 5. Documentation: PROJECT_CONTEXT_CONFIGURATION.md
- **Work**: Document the project-level context config pattern:
  - Why project configs exist (overrides/extends domain configs)
  - How to create a new project config
  - Examples from hero_heaven and screenplays projects
  - Merge semantics (domain loads first, project extends)
  - How {PROJECT_ROOT} enables external projects
- **Depends on**: Item #0 (understanding of {PROJECT_ROOT} pattern)
- **Effort**: 1-2 hours

#### 6. Examples: Create Project Template
- **Location**: `/personas/examples/`
- **Work**: Create a minimal project template showing:
  - Skeleton folder structure
  - Example context_configuration_{project}.json with {PROJECT_ROOT} variable
  - README with setup instructions
  - Good for future projects (e.g., new TTRPG game, new screenplay)
- **Depends on**: Item #0 (understanding of {PROJECT_ROOT} pattern)
- **Effort**: 1-2 hours

#### 7. Guide: How to Create a New Persona
- **File**: New document `HOW_TO_CREATE_A_PERSONA.md` (root or `/personas/examples/`)
- **Work**: Concise guide for creating new personas, covering:
  - Persona schema structure (metadata, persona, collaboration, behavioral_rules, reference_libraries, reference_context, reference_guide)
  - Naming conventions (persona_name snake_case, display_name readable, custom_name optional)
  - Defining expertise_scope and defers_to
  - Writing behavioral_rules (8-15 imperative statements)
  - Creating reference_libraries vs embedding knowledge
  - Registering persona in domain context_configuration.json
  - When to create a new expertise_domain vs using existing ones
  - Examples: minimal persona skeleton → full persona
- **Template reference**: Use existing personas as examples (lore_keeper, react_specialist, etc.)
- **Depends on**: None
- **Effort**: 2-3 hours
- **Note**: Can replace `.devnotes/REFACTORING_REFERENCE.md` as forward-looking guidance

### Lower Priority

#### 8. Analysis: Independent Authority Personas
- **Work**: Document the four independent authority personas
  - Dylan (software_architecture)
  - Dave (design_strategy)
  - screenwriter (story_structure_and_vision)
  - llm_prompt_specialist (llm_and_prompt_engineering)
  - What it means, when to defer to them, etc.
- **Depends on**: None
- **Effort**: 30-45 min

#### 9. Consolidation: Expertise Domain Rationalization
- **Work**: Review 22 domains across 5 areas for:
  - Overlaps or redundancies
  - Clearer naming if needed
  - Consolidation opportunities
- **Effort**: 2-3 hours (analysis only; no refactoring)
- **Note**: Not urgent; framework works fine with current domains

#### 10. Future Extensibility: Cross-Domain Patterns
- **Work**: Document patterns for:
  - Creating new domains
  - Defining new expertise domains
  - Building cross-domain teams
  - Framework growth scenarios
- **Effort**: 2-3 hours (documentation)

---

## Optional / Nice-to-Have

#### A. Journal/Transcript Organization
- **Current**: Loose transcripts in `/mnt/transcripts/`
- **Idea**: Create manifest or index linking transcripts to major work phases
- **Effort**: 1 hour

#### B. Framework Validation Script
- **Idea**: Automated check for:
  - All personas referenced in teams exist
  - All deferred-to expertise domains are documented
  - No orphaned files in domain folders
  - Schema consistency across personas
- **Effort**: 3-4 hours (Python or shell script)

#### C. Visual Architecture Diagram
- **Idea**: ASCII or Mermaid diagram showing:
  - Domain structure
  - Team compositions
  - Deference relationships
- **Effort**: 1-2 hours

---

## Decision Points Pending

### 1. Framework States & Controls (Item #2)
**Question**: How should "personas on/off" and team selection work?
- Option A: Via context_configuration.json settings?
- Option B: Via explicit API/interface?
- Option C: Documented as user responsibility (manual selection)?

**Next step**: Clarify intent, then document.

### 2. Domain Growth
**Question**: Should we add domains for:
- Data engineering?
- Product management?
- UX research?
- Other areas?

**Next step**: Assess actual needs as framework expands.

---

## Quick Reference: File Locations

| What | Where |
|------|-------|
| Persona schemas | `/personas/{domain}/` and `/personas/{domain}/{project}/` |
| Domain config | `/personas/{domain}/context_configuration.json` |
| Project config | `/personas/{domain}/{project}/context_configuration_{project}.json` |
| Domain teams | `/personas/{domain}/teams/` |
| Cross-domain teams | `/personas/ai_development/teams/` (currently only intelligence_framework_team) |
| Root teams | `/teams/` (empty except .DS_Store; reserved for future cross-domain teams) |
| Examples | `/personas/examples/` |
| Documentation | Root directory (EXPERTISE_DOMAINS.md, ARCHITECTURAL_DECISIONS.md, etc.) |

---

## Notes

- All 35 personas now use expertise_domain deference model
- {PROJECT_ROOT} pattern enables external projects as first-class members of TIF architecture
- Framework is functionally complete for current scope
- Documentation is the biggest pending item (especially {PROJECT_ROOT} pattern)
- No blocking issues; work can be prioritized flexibly
- Each pending item is independent (no chaining dependencies except as noted)
