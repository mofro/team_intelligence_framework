---
title: Configuration Reference - Team Intelligence Framework
type: technical_reference
created: 2025-12-11
updated: 2025-12-11
---

# Configuration Reference: Team Intelligence Framework

Complete technical reference for all configuration schemas, structures, and patterns used by the Team Intelligence Framework.

---

## Quick Start: Finding What You Need

**Looking for guidance on how to use something?**
- Teams → See **TEAM_DEFINITION_GUIDE.md**
- Personas → See **PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md**
- Overall architecture → See **ARCHITECTURAL_DECISIONS.md**

**Looking for the schema/structure?**
- Keep reading this document ↓

**Want to understand the principles?**
- Universal framework principles → See files in `/config/*.md`
- Collaboration & interaction → See `/config/persona_collaboration_framework_v1.md` and `/config/persona_interaction_architecture_v1.md`

---

## Overview: Two-Layer Architecture

The framework operates on two configuration layers (see **ARCHITECTURAL_DECISIONS.md Decision 1 & 2**):

**Layer 1: Universal Framework Rules** (Documented in `/config/*.md`)
- How any persona activates (Phases 1-5)
- How collaboration works (primary voice, optimistic skepticism, unified response)
- How context loads and binds to personas
- How personas communicate (@addressing system, fallback hierarchy)
- How performance is measured

**Layer 2: Context Configuration** (JSON in `/personas/[domain]/`)
- What references exist in this domain
- What behavioral protocols apply here (context-specific interpretation of universal rules)
- What activation triggers apply
- What personas are available
- What teams exist

This document defines **JSON schemas** for Layer 2 and references to Layer 1 documentation.

---

## Layer 1: Universal Framework Rules (Reference)

These rules are documented in Markdown files in `/config/`. This section summarizes what they define.

**Read these files for detailed guidance:**
- `persona_activation_framework.md` — How personas activate and transition between states
- `persona_collaboration_framework_v1.md` — How personas work together (primary voice, skepticism, unified response)
- `persona_interaction_architecture_v1.md` — Addressing system, schema portability, fallback hierarchy
- `measurement_framework.md` — Performance metrics and visibility

**Quick reference on what Universal Rules define:**

### Persona Activation Framework

Defines how any persona in any context moves through these states:
- **Available Pool**: All discoverable personas for this context
- **Active Roster**: Currently engaged personas (usually 2-5)
- **Suggested**: Recommended by the framework based on keywords
- **Dormant**: Available but not suggested or active

Three activation paths:
1. **Always-on**: Defined in `context_configuration.json` (implicit activation)
2. **Explicit**: User requests specific persona
3. **Smart trigger**: System detects keywords and suggests

Five activation phases:
1. Context detection & reference library loading
2. Persona activation
3. Reference context binding
4. Persona-to-persona communication
5. Session-end checkout

### Persona Collaboration Framework

Defines how multiple personas work together in a single response:
- **Primary voice system**: One persona leads, others weave in seamlessly
- **Optimistic skepticism**: Challenge assumptions before solving
- **Unified response**: No individual chiming, integrated team voice
- **Response tagging**: Subtle markers showing expertise shifts

### Persona Interaction Architecture

Defines addressing and schema portability:
- **@persona_name** addressing (GitHub-style)
- **Name resolution**: Custom name → persona name → display name
- **Collaboration tagging**: When multiple personas contribute to one response
- **Extended persona schema**: Backward compatible, includes collaboration fields

---

## Layer 2: Context Configuration (JSON Schemas)

### 2.1: context_configuration.json

Each domain has a `context_configuration.json` that applies universal rules in domain-specific ways.

**Location**: `/personas/[domain]/context_configuration.json`

**What it defines**:
- Reference libraries this context uses
- How universal behaviors apply here (contextual interpretation)
- Activation triggers (keywords that suggest personas)
- Always-on personas (implicit activation)
- Available personas (what's in this domain)
- Available teams (pre-configured groups)
- Default primary persona (who leads by default)
- Collaboration patterns (how personas typically work together)

**Schema**:

```json
{
  "schema_version": "1.0",
  "context_name": "[domain_name]",
  "description": "[What this context is for]",
  "created_date": "YYYY-MM-DD",

  "reference_libraries": [
    "[Path to guidance docs for this domain]",
    "[Path to decision logs, project docs]",
    "[Path to world/project documentation]"
  ],

  "context_behavioral_protocols": {
    "[universal_principle]": "[How it applies here]",
    "[domain_specific_rule]": "[Custom behavior]"
  },

  "activation_triggers": {
    "persona_name": {
      "keywords": ["keyword1", "keyword2"],
      "auto_suggest": true,
      "engagement_guide_section": "[Reference to PERSONA_ENGAGEMENT_GUIDE.md]"
    }
  },

  "always_on_personas": ["persona_name"],

  "available_personas": [
    "persona_name_1",
    "persona_name_2",
    "persona_name_3"
  ],

  "available_teams": [
    "team_name_1",
    "team_name_2"
  ],

  "default_primary_persona": "persona_name",

  "collaboration_patterns": {
    "persona1": {
      "persona2": "How these collaborate",
      "trigger": "What triggers this collaboration"
    }
  }
}
```

**Example** (Hero Heaven Gaming):

```json
{
  "schema_version": "1.0",
  "context_name": "gaming",
  "description": "TTRPG game-writing - Hero Heaven primary project",
  "created_date": "2025-12-11",

  "reference_libraries": [
    "PERSONA_ENGAGEMENT_GUIDE.md",
    "ARCHITECTURAL_DECISIONS.md",
    "world/",
    "narrative/"
  ],

  "context_behavioral_protocols": {
    "primary_voice_system": "Collaborative world-building",
    "optimistic_skepticism": "Challenge narrative choices against world mechanics",
    "fourth_wall_awareness": "All personas speak as architects, not inhabitants"
  },

  "activation_triggers": {
    "mythweaver": {
      "keywords": ["myth", "cosmology", "divine", "transcendence"],
      "auto_suggest": true,
      "engagement_guide_section": "Mythweaver"
    }
  },

  "always_on_personas": ["lore_keeper"],

  "available_personas": [
    "lore_keeper",
    "mythweaver",
    "ttrpg_game_architect"
  ],

  "available_teams": ["hero_heaven_worldbuilding_team"],

  "default_primary_persona": "lore_keeper",

  "collaboration_patterns": {
    "lore_keeper": {
      "mythweaver": "Myth proposal → world consistency check"
    }
  }
}
```

---

### 2.2: Persona Schema (JSON)

Individual personas are defined in JSON. They reference the context they belong to.

**Location**: `/personas/[domain]/[persona_name].json` or `/personas/[domain]/[project]/[persona_name].json`

**Key fields**:
- `metadata`: Name, description, author, version, creation date
- `persona`: Role, expertise, approach, specializations
- `collaboration`: What they collaborate on, who they defer to
- `behavioral_rules`: How they act in conversations
- `reference_context`: Which domain/context they belong to
- `reference_guide`: Link to PERSONA_ENGAGEMENT_GUIDE.md section explaining how they operate

**Important**: No embedded `knowledge_base` arrays. References are external (via `reference_guide` and `reference_context`).

---

### 2.3: Team Schema (JSON)

Teams are pre-defined collections of personas working together. See **TEAM_DEFINITION_GUIDE.md** for comprehensive guidance on team composition.

**Location**: `/personas/[domain]/teams/[team_name].json`

**What it defines**:
- Team membership (3-5 personas from same domain)
- Default primary (who leads)
- Collaboration patterns (how members work together)
- Decision hierarchy (who decides what)
- Activation triggers (keywords that suggest this team)
- Use cases (scenarios where this team activates)

**Schema**:

```json
{
  "schema_version": "1.0",
  "metadata": {
    "name": "[Team Name]",
    "description": "[What this team does]",
    "context": "[domain_name]",
    "created_date": "YYYY-MM-DD"
  },

  "team": {
    "team_name": "[snake_case_name]",
    "display_name": "[Human Readable Name]",
    "members": ["persona1", "persona2", "persona3"],
    "default_primary": "persona1"
  },

  "activation": {
    "auto_suggest_contexts": ["context_keyword1", "context_keyword2"],
    "auto_suggest_keywords": ["keyword1", "keyword2"],
    "discovery_priority": "high|medium|low"
  },

  "team_dynamics": {
    "primary_workflow": "[How they collaborate]",
    "collaboration_patterns": [
      {
        "members": ["persona1", "persona2"],
        "focus": "[What they focus on together]"
      }
    ],
    "decision_hierarchy": [
      "persona1: [What they decide]",
      "persona2: [What they decide]"
    ]
  },

  "use_cases": [
    "[Scenario 1]",
    "[Scenario 2]"
  ]
}
```

**Example** (Retirement Planning Team):

```json
{
  "schema_version": "1.0",
  "metadata": {
    "name": "Retirement Planning Team",
    "context": "financial",
    "created_date": "2025-12-11"
  },

  "team": {
    "team_name": "retirement_planning_team",
    "display_name": "Retirement Planning Team",
    "members": [
      "investment_advisor",
      "tax_strategist",
      "healthcare_expert",
      "social_security_specialist",
      "insurance_analyst",
      "estate_planner"
    ],
    "default_primary": "investment_advisor"
  },

  "activation": {
    "auto_suggest_contexts": [
      "retirement planning",
      "early retirement",
      "withdrawal strategy"
    ],
    "auto_suggest_keywords": [
      "retire",
      "401k",
      "roth",
      "medicare"
    ],
    "discovery_priority": "high"
  },

  "team_dynamics": {
    "primary_workflow": "Investment Advisor orchestrates strategy with specialist input",
    "collaboration_patterns": [
      {
        "members": ["investment_advisor", "tax_strategist"],
        "focus": "Tax-efficient withdrawal sequencing"
      },
      {
        "members": ["healthcare_expert", "social_security_specialist"],
        "focus": "Timing coordination for benefits"
      }
    ],
    "decision_hierarchy": [
      "investment_advisor: overall strategy and timeline",
      "tax_strategist: tax optimization",
      "healthcare_expert: cost estimation",
      "social_security_specialist: benefit timing",
      "insurance_analyst: coverage gaps",
      "estate_planner: asset protection"
    ]
  },

  "use_cases": [
    "Retirement timeline analysis",
    "Early retirement bridge planning",
    "Tax-efficient withdrawal strategy",
    "Medicare gap coverage planning"
  ]
}
```

---

## Complete File Structure Reference

```
team_intelligence_framework/
├── README.md
├── ARCHITECTURAL_DECISIONS.md (Decision 1: two-layer config, Decision 2: JSON vs. Markdown)
├── CONFIG_REFERENCE.md (this file—JSON schemas)
├── TEAM_DEFINITION_GUIDE.md (Markdown—how to compose teams)
├── PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md (Markdown—how to set up contexts)
├── USER_GUIDE.md (Markdown—how to use personas/teams)
│
├── config/ (Markdown—Universal Framework Rules)
│   ├── persona_activation_framework.md
│   ├── persona_collaboration_framework_v1.md
│   ├── persona_interaction_architecture_v1.md
│   └── measurement_framework.md
│
├── personas/ (JSON Configs + Persona/Team Schemas)
│   ├── gaming/
│   │   ├── context_configuration.json ✅
│   │   ├── hero_heaven/
│   │   │   ├── lore_keeper_persona_schema.json
│   │   │   ├── mythweaver_persona_schema.json
│   │   │   └── teams/
│   │   │       └── hero_heaven_worldbuilding_team.json ✅
│   │   └── ttrpg_game_architect_persona_schema.json
│   │
│   ├── development/
│   │   ├── context_configuration.json ✅
│   │   ├── [9 persona schemas]
│   │   └── teams/
│   │       └── react_fullstack_team.json ✅
│   │
│   ├── financial/
│   │   ├── context_configuration.json ✅
│   │   ├── [6 persona schemas]
│   │   └── teams/
│   │       └── retirement_planning_team.json ✅
│   │
│   ├── writing/
│   │   ├── context_configuration.json ✅
│   │   ├── screenplays/
│   │   │   └── [4 persona schemas]
│   │   └── teams/
│   │
│   └── llm_prompt_specialist_persona_schema.json
│
└── teams/
    └── intelligence_framework_team.json
```

---

## Cross-Reference Guide

**Need guidance on...**

| Topic | See... |
|-------|--------|
| Why this architecture exists | ARCHITECTURAL_DECISIONS.md |
| How to compose a team | TEAM_DEFINITION_GUIDE.md |
| How personas activate | /config/persona_activation_framework.md |
| How personas collaborate | /config/persona_collaboration_framework_v1.md |
| How to set up a new context | PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md |
| How to use personas/teams | USER_GUIDE.md |
| Persona schema details | CONFIG_REFERENCE.md Section 2.2 |
| Team schema details | CONFIG_REFERENCE.md Section 2.3 (also TEAM_DEFINITION_GUIDE.md) |
| Context configuration details | CONFIG_REFERENCE.md Section 2.1 |

---

## Implementation Notes

- **Universal rules are stable** — they define how the framework works everywhere (in `/config/*.md`)
- **Context configs are flexible** — each domain defines how to apply universal rules in their context (JSON in `/personas/[domain]/`)
- **Teams are composable** — pre-defined teams or custom rosters, both follow the same schema
- **Personas are portable** — schemas work across contexts; reference_context field anchors them to a domain

---

## Next Steps

For implementation guidance, see:
- **Phase 2**: Refactor persona schemas (remove embedded knowledge_base, add reference_guide)
- **Phase 3**: Update documentation (README.md, PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md, USER_GUIDE.md)
