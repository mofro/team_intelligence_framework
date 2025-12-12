---
title: Team Intelligence Framework - Architectural Decisions
type: architectural_planning
created: 2025-12-11
updated: 2025-12-11
---

# Architectural Decisions: Team Intelligence Framework

This document records significant architectural decisions, the context and reasoning behind them, and their consequences for the framework.

---

## Decision 1: Two-Layer Configuration Structure

**Status**: Decided (2025-12-11)  
**Affects**: Persona activation, context management, reference loading, documentation structure

### Problem

The Persona Framework operates in multiple contexts (development, game design, financial planning, writing, etc.). Each context has:

1. **Universal rules** — How any persona activates, how context is loaded, how personas collaborate (same everywhere)
2. **Context-specific rules** — What references exist here, what behavioral protocols apply, what triggers activation (different per context)

**The trap**: Without clear separation, these rules get duplicated across contexts, creating maintenance nightmares:
- Update a universal rule? Have to update it in 5 places.
- Add a new context? Have to know all the universal rules AND all the context patterns.
- Single source of truth breaks down quickly.

### Decision

Establish a **two-layer configuration model**:

**Layer 1: Universal Framework Rules** (Single source, never changes)
- Documented in `/config/` Markdown files
- Examples: persona_activation_framework.md, persona_collaboration_framework_v1.md, persona_interaction_architecture_v1.md

**Layer 2: Context Configuration** (Domain-specific, lives with each context)
- `personas/[domain]/context_configuration.json` — Reference libraries, behavioral protocols, activation triggers, available personas for THIS context

### Rationale

1. **Eliminates duplication** — Universal rules documented once, context rules documented once
2. **Clear separation of concerns** — Framework logic stays framework; project logic stays in context
3. **Scalable** — New contexts don't require understanding universal rules; they just create a context_configuration.json
4. **Single source of truth** — Each thing lives exactly where it makes sense
5. **Maintainable** — Update universal rules in one place; update context rules in one place

### Consequences

#### Positive
✅ Clear, maintainable architecture  
✅ Easy to add new contexts (template + context_configuration.json)  
✅ Universal rules can evolve without touching every context  
✅ Context-specific protocols can be sophisticated without bloating universal framework  
✅ New team members understand structure quickly

#### Negative/Trade-offs
⚠️ Requires new config files (initial setup work)  
⚠️ Documentation must explain both layers (more docs, but clearer)  
⚠️ Some decisions require understanding both layers (not trivial)

### Related Decisions

- Decision 2: JSON vs. Markdown file types (see below)
- [Future] Persona Schema Versioning Strategy
- [Future] Context Override Rules (when user rules conflict with framework rules)

---

## Decision 2: JSON vs. Markdown File Types

**Status**: Decided (2025-12-11)  
**Affects**: Configuration file organization, documentation structure, LLM interpretation consistency

### Problem

The framework supports two types of files: JSON (data structures) and Markdown (guidance). This creates a tension:
- **JSON**: Machine-readable, unambiguous, validates against schema, but less pleasant for humans to read/edit
- **Markdown**: Human-friendly, flexible, easy to explain context, but introduces interpretive drift for LLMs

**The question**: Which file type for which purpose? How do we maximize consistency without sacrificing usability?

### Decision

Separate by layer:

**JSON (Data Layer)** — Things that affect persona/team behavior
- `personas/[domain]/[persona_name].json` — Persona definitions
- `personas/[domain]/context_configuration.json` — Context behavior and activation rules
- `personas/[domain]/teams/[team_name].json` — Team compositions and dynamics
- `/teams/[framework_teams].json` — Framework-level teams

These are data structures that LLMs parse, personas reference, and contexts load. They must be unambiguous.

**Markdown (Guidance Layer)** — Documentation and principles
- `/config/*.md` — Universal framework principles (persona_activation_framework.md, persona_collaboration_framework_v1.md, etc.)
- `README.md` — Framework overview
- `ARCHITECTURAL_DECISIONS.md` — Why decisions were made
- `CONFIG_REFERENCE.md` — Schema reference guide (what data structures exist and why)
- `REFACTORING_REFERENCE.md` — Maps framework principles to persona schema refactoring decisions
- `REFACTORING_PLAN.md` — Full execution plan for persona refactoring with time estimates
- `PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md` — How to set up new contexts
- `USER_GUIDE.md` — How to use personas and teams
- `TEAM_DEFINITION_GUIDE.md` — How to compose teams, conventions, patterns

Markdown is for humans to understand principles and for LLMs to learn how the framework *should* work.

### Rationale

1. **LLM Consistency**: JSON prevents interpretive drift for behavior-critical structures. Markdown is fine for guidance where flexibility is an asset.
2. **Human Usability**: Markdown is vastly more readable and editable than JSON for documentation. Reserve JSON for data structures.
3. **Validation**: JSON schemas can be validated programmatically. Markdown conventions must be enforced through clear guidance.
4. **Existing Pattern**: Framework already uses ~35+ JSON files for personas/teams and Markdown for documentation in `/config/`. This formalizes that pattern.
5. **Separation of Concerns**: Data layer ↔ guidance layer. Different purposes, different tools.

### Consequences

#### Positive
✅ LJSONom behavior is precise and unambiguous (JSON data layer)  
✅ Human documentation is readable and maintainable (Markdown guidance layer)  
✅ Clear distinction: if it affects behavior, it's JSON; if it's guidance, it's Markdown  
✅ Aligns with existing framework patterns  
✅ Can validate data structures; guide documentation interpretation  

#### Negative/Trade-offs
⚠️ Requires clear conventions in Markdown to prevent interpretive drift  
⚠️ Documentation must explicitly explain relationships between JSON structures and Markdown principles  
⚠️ More files (but fewer than if everything were JSON)  
⚠️ LLMs need clear guidance on which file types to reference for which purposes

### Next Steps

1. ✅ Create TEAM_DEFINITION_GUIDE.md (Markdown guidance for team composition)
2. ✅ Update CONFIG_REFERENCE.md to clarify it's a reference guide, not creation instructions
3. ✅ Create REFACTORING_REFERENCE.md (maps `/config/` frameworks to persona schema fields)
4. ✅ Create REFACTORING_PLAN.md (execution plan for refactoring all 20 personas)
5. 🔨 Review `/config/*.md` files for cross-references to Decision 1 and Decision 2
6. 🔨 Update PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md with conventions for reading/using both layers

### Related Decisions

- Decision 1: Two-Layer Configuration Structure (this decision implements that split)
- [Future] Schema Validation Strategy (how to validate JSON against schema)
- [Future] Markdown Convention Enforcement (how to guide LLM interpretation)

---

## Implementation Status: Phase 1, 2, & 3

### Phase 1: Configuration Foundation & Theory ✅ COMPLETE (2025-12-11)

**Deliverables:**
- ✅ ARCHITECTURAL_DECISIONS.md created with Decision 1 & 2 documented
- ✅ CONFIG_REFERENCE.md created with complete schema specifications
- ✅ Decision 2 (JSON vs. Markdown) documented, aligning with existing patterns
- ✅ Two-layer architecture fully specified

### Phase 2: Refactor Personas & Teams Together 🔨 IN PROGRESS (Started 2025-12-11)

**Completed (2025-12-11):**
- ✅ context_configuration.json created for all 4 domains (JSON data layer)
- ✅ Created teams/ subdirectories for all 4 domains
- ✅ Moved and updated team definitions with `context` field
- ✅ All context configs reference correct personas and teams
- ✅ Confirmed Decision 2: JSON for behavior-critical configs ✅
- ✅ lore_keeper_persona_schema.json refactored as template (Decision 2 pattern)
- ✅ REFACTORING_REFERENCE.md created (maps `/config/` framework principles → persona schema fields)
- ✅ REFACTORING_PLAN.md created (full plan for 20 personas with time estimates, batching strategy, progress tracking)
- ✅ Established explicit mapping: 3 `/config/` framework files → refactoring decision checklist per persona

**Remaining in Phase 2:**
- [ ] Refactor 19 remaining persona schemas using REFACTORING_REFERENCE.md as guide
  - [ ] Gaming domain: mythweaver, ttrpg_game_architect (2 personas)
  - [ ] Development domain: developer_coding_persona, react_specialist, security_specialist, 10_foot_ui_designer, design_expert, ott_ux_persona, blits_developer, lightning_developer, cloud_architect (9 personas)
  - [ ] Financial domain: investment_advisor, tax_strategist, healthcare_expert, insurance_analyst, social_security_specialist, estate_planner (6 personas)
  - [ ] Writing domain: screenwriter, dialog_coach, science_advisor, dp_persona (4 personas)
- [ ] Create PROJECT_MIGRATION_GUIDE.md with project-specific contexts extracted from personas
- [ ] Create/update PERSONA_ENGAGEMENT_GUIDE.md with per-persona operational protocols
- [ ] Verify all persona schemas aligned with Decision 2 pattern
- [ ] Spot-check 3-4 refactored personas for consistency

**Estimated effort**: ~6-7 hours concentrated work (15-20 min per persona using REFACTORING_REFERENCE.md as guide)

**Key insight**: REFACTORING_REFERENCE.md is the bridge between `/config/` framework principles and individual persona schema field decisions. All refactoring decisions flow from framework principles → reference guide.

### Phase 3: Documentation & Guidance Layer 📚 IN PROGRESS (Started 2025-12-11)

**Completed (2025-12-11):**
- ✅ Create TEAM_DEFINITION_GUIDE.md (comprehensive guidance on team composition, collaboration patterns, anti-patterns, testing)
- ✅ Update CONFIG_REFERENCE.md to be a proper technical reference with JSON-to-Markdown mapping
- ✅ Add cross-reference table in CONFIG_REFERENCE.md showing what guidance to read for what
- ✅ Update ARCHITECTURAL_DECISIONS.md with Phase 1, 2, 3 status and key insights

**Remaining in Phase 3:**
- [ ] Review `/config/*.md` files for clarity and add cross-references to Decision 1 & Decision 2
- [ ] Update PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md with file type conventions and layer guidance
- [ ] Update README.md to explain two-layer architecture with examples
- [ ] Update USER_GUIDE.md with team activation and context usage patterns
- [ ] Rename PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md to PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md (all-caps per convention)

---

## Decision Log Template (for future decisions)

For each new architectural decision, use this structure:

```
## Decision N: [Decision Title]

**Status**: Proposed/Decided/Implemented  
**Affects**: [What parts of the system]

### Problem
[What problem are we solving?]

### Decision
[What did we decide?]

### Rationale
[Why did we decide this way?]

### Consequences
#### Positive
- [benefits]

#### Negative/Trade-offs
- [downsides]

### Next Steps
[What needs to happen next?]

### Related Decisions
[Links to related decisions]
```

---

## Framework Principle → Schema Field Mapping

This summary ties Decision 1 & 2 to actual implementation. See REFACTORING_REFERENCE.md for full details.

| Framework Component | Source Document | Schema Field | Decision |
|---|---|---|---|
| Activation triggers | persona_activation_framework.md | `activation_triggers` | Persona-specific (JSON) |
| Context loading | persona_activation_framework.md | `reference_context` | Domain name (JSON) |
| Addressing system | persona_interaction_architecture_v1.md | `persona_name`, `display_name`, `custom_name` | All three required (JSON) |
| Expertise scope | persona_interaction_architecture_v1.md | `collaboration.expertise_scope` | Persona-specific (JSON) |
| Behavioral protocols | persona_collaboration_framework_v1.md | `behavioral_rules` | Persona-specific (JSON) |
| Knowledge/references | persona_interaction_architecture_v1.md | `reference_libraries` | Persona-specific, not embedded (JSON) |
| Collaboration patterns | persona_collaboration_framework_v1.md | Team definitions (not persona) | Formalized in teams, not personas (JSON) |
| Operational protocols | All `/config/` files | `reference_guide` | Points to external documentation (Markdown) |
