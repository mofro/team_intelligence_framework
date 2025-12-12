---
title: Team Definition Guide - Team Intelligence Framework
type: guidance
created: 2025-12-11
updated: 2025-12-11
---

# Team Definition Guide: Team Intelligence Framework

Comprehensive guide for composing, defining, and organizing teams of personas within the Team Intelligence Framework.

---

## Overview: What is a Team?

A **team** is a curated collection of personas working together toward a shared goal. Teams are more than just "a list of personas"—they define:
- **Who works together** (team membership)
- **How they work together** (collaboration patterns)
- **Who leads** (default primary)
- **Why they work together** (use cases)

Teams make explicit what would otherwise be implicit. They answer: "When should these specific personas activate together?"

---

## When to Create a Team

### ✅ Create a Team When:

1. **Multiple personas consistently work together** on a specific problem type
   - Example: Retirement planning requires Investment Advisor + Tax Strategist + Healthcare Expert
   - Pattern: These three always collaborate; they're rarely activated alone

2. **You have explicit collaboration patterns** defined between personas
   - Example: React Specialist + Developer Coding Persona work on component architecture; Security Specialist reviews authentication
   - Each pair has a known working dynamic (see: react_fullstack_team.json)

3. **Activation is context-driven** — certain keywords or scenarios always trigger the same personas
   - Example: "Early retirement" always needs Investment Advisor + Tax Strategist + Healthcare Expert + Social Security Specialist
   - Grouping them reduces decision burden (see: retirement_planning_team.json)

4. **The group has a distinct purpose** separate from individual personas
   - Example: "Retirement Planning Team" is the *collaborative act of comprehensive financial strategy*, not just six individuals
   - OR: "React Fullstack Team" is the *collaborative act of end-to-end application development*, not just six individuals

5. **Users will want to activate the whole group** as a unit
   - Example: User says "I need the retirement planning team on this" instead of listing six personas
   - More natural than: "@investment_advisor @tax_strategist @healthcare_expert..."

### ❌ Don't Create a Team When:

1. **Personas rarely activate together** (just different expertise areas)
   - Counter-example: Development context has security_specialist, but most work doesn't need security review
   - Don't make a "general development team"—let the framework suggest specialist activation

2. **The pairing is ad-hoc or situational** (collaboration is case-by-case)
   - Counter-example: "Sometimes UI designer + developer work together"
   - That's not a team; that's natural collaboration within a context

3. **You just want to name a group** without specific collaboration patterns
   - Don't create "all financial experts team"—use available_personas in context_configuration.json instead

4. **There's a clear hierarchy** and the "team" is really just a subordinate reporting structure
   - Teams are peer collaborations; if one persona is always in charge and others just support, use context configuration instead

---

## Team Composition Principles

### Principle 1: Intentional Membership

Every member should have a **clear role** in the team's purpose. No passengers.

✅ **Good**: Retirement Planning Team = Investment Advisor (strategy) + Tax Strategist (optimization) + Healthcare Expert (cost planning)
- Each role is distinct and necessary

❌ **Bad**: Retirement Planning Team = Investment Advisor + Tax Strategist + Healthcare Expert + UI Designer + Random Persona
- UI Designer and Random Persona don't belong; they dilute the team's purpose

### Principle 2: Balanced Expertise

Teams work best when members have **complementary expertise** without strict hierarchy.

✅ **Good**: React Specialist + Developer Coding Persona + UI Designer + Security Specialist
- Four different domains; each brings distinct value

❌ **Bad**: Senior Developer + Junior Developer + Another Junior Developer
- Implies hierarchy, not collaboration; use role-based context instead

### Principle 3: Explicit Collaboration Patterns

Define **how** members work together, not just **that** they do.

✅ **Good**:
```
Collaboration patterns:
- Investment Advisor + Tax Strategist: Withdrawal sequencing
- Healthcare Expert + Social Security Specialist: Medicare timing coordination
```

❌ **Bad**:
```
Members: [investment_advisor, tax_strategist, healthcare_expert]
(No explanation of how they interact)
```

### Principle 4: Manageable Size

Teams should be **2-5 members** (usually 3-4).

✅ **Good**: 3-person team can collaborate efficiently
❌ **Bad**: 8-person team becomes unwieldy; probably should be two smaller teams

---

## Team Structure & JSON Schema

Teams are defined in JSON (see CONFIG_REFERENCE.md for full schema). Key fields:

```json
{
  "metadata": {
    "name": "Human-readable name",
    "description": "What this team is for",
    "context": "Which domain (gaming, financial, development, writing)",
    "created_date": "YYYY-MM-DD"
  },

  "team": {
    "team_name": "snake_case_identifier",
    "members": ["persona1", "persona2", "persona3"],
    "default_primary": "persona_name (who leads by default)"
  },

  "team_dynamics": {
    "primary_workflow": "How they work together in plain English",
    "collaboration_patterns": [
      {
        "members": ["persona1", "persona2"],
        "focus": "What this pair focuses on"
      }
    ],
    "decision_hierarchy": ["who decides what"]
  },

  "activation": {
    "auto_suggest_contexts": ["retirement planning", "estate planning"],
    "auto_suggest_keywords": ["retire", "withdrawal", "medicare"]
  },

  "use_cases": ["specific scenario 1", "specific scenario 2"]
}
```

---

## Real Team Examples

### Example 1: Retirement Planning Team (Financial)

**Location**: `/personas/financial/teams/retirement_planning_team.json`

**Purpose**: Comprehensive retirement timeline, tax efficiency, healthcare coordination

**Team Members** (6):
- Investment Advisor (strategy lead)
- Tax Strategist (optimization)
- Healthcare Expert (cost planning)
- Social Security Specialist (claiming strategy)
- Insurance Analyst (gap coverage)
- Estate Planner (asset protection)

**Why This Works**:
- Clear domain divisions (investment, tax, health, social security, insurance, estate)
- Explicit collaboration patterns (advisor coordinates with specialists)
- Activates together for retirement-specific questions
- Decision hierarchy: Investment Advisor leads, specialists provide input

**Collaboration Flow**:
```
User: "Can I retire at 55?"
→ Investment Advisor assesses portfolio + years needed
→ Tax Strategist evaluates withdrawal sequencing
→ Healthcare Expert estimates costs pre-Medicare
→ Social Security Specialist models benefit timing
→ Insurance Analyst identifies gaps
→ Estate Planner reviews asset structure
→ Investment Advisor synthesizes into yes/no with confidence level
```

**Activation Keywords**: "retire", "retirement", "401k", "roth", "medicare", "early retirement"

---

### Example 2: React Fullstack Team (Development)

**Location**: `/personas/development/teams/react_fullstack_team.json`

**Purpose**: End-to-end React application development from design through deployment

**Team Members** (6):
- React Specialist (component architecture lead)
- Developer Coding Persona (general architecture)
- 10-Foot UI Designer (visual design)
- Design Expert (design systems)
- OTT UX Persona (user experience)
- Security Specialist (authentication, data safety)

**Why This Works**:
- Covers the full stack: components, architecture, design, UX, security
- React Specialist leads (primary) because React is the constraint
- Collaborates on component design (React Specialist + UI Designer)
- Security reviews (Security Specialist + Developer Coding Persona)
- Natural pairing of design expertise (10-Foot Designer + Design Expert + UX Persona)

**Collaboration Flow**:
```
User: "Design a new dashboard component"
→ React Specialist proposes component architecture
→ 10-Foot UI Designer focuses on big-picture usability
→ Design Expert ensures consistency with design system
→ OTT UX Persona checks interaction flow
→ Security Specialist reviews data access patterns
→ React Specialist synthesizes into implementation plan
```

**Activation Keywords**: "react", "component", "dashboard", "fullstack", "web development", "ui design"

---

### Example 3: Hero Heaven Worldbuilding Team (Gaming - Planned)

**Location**: `/personas/gaming/teams/hero_heaven_worldbuilding_team.json` (Not yet created; represents future team pattern)

**Purpose**: Collaborative world-building, mythology integration, system evaluation (when needed for Hero Heaven)

**Potential Team Members** (3):
- Lore Keeper (world documentation & consistency)
- Mythweaver (narrative resonance & theming)
- Theo TTRPG (system evaluation & mechanics, if/when needed)

**Why This Pattern Works**:
- Each has distinct expertise (docs, myth, mechanics)
- Would have explicit collaboration patterns
- Would activate together for "big picture" worldbuilding decisions
- Default primary (Lore Keeper) makes sense as the coordinator

**Note**: This team hasn't been formalized because (per the "Don't Create a Team When" section) the personas rarely activate together as a unit in current practice. Mythweaver and Lore Keeper collaborate case-by-case, and Theo TTRPG is activated explicitly when system evaluation is needed. If a use case emerges where all three consistently activate together, this team can be formalized.

---

## Common Collaboration Patterns

### Pattern 1: Hub & Spoke

One persona leads; others provide specialized input.

**Example**: Investment Advisor (hub) with Tax, Healthcare, Social Security, Insurance, Estate (spokes)

```json
"decision_hierarchy": [
  "investment_advisor: overall strategy and coordination",
  "tax_strategist: tax optimization input",
  "healthcare_expert: cost estimation input",
  ...
]
```

**When to use**: Large teams (4+), one clear primary domain

---

### Pattern 2: Sequential Handoff

Personas work in sequence; each builds on the previous one's output.

**Example** (hypothetical): Screenwriter → Dialog Coach → Science Advisor

```json
"collaboration_patterns": [
  {
    "members": ["screenwriter", "dialog_coach"],
    "focus": "Dialogue authenticity"
  },
  {
    "members": ["science_advisor", "screenwriter"],
    "focus": "Technical accuracy in narrative"
  }
]
```

**When to use**: Teams with clear workflow (3-4 personas)

---

### Pattern 3: Peer Consultation

All members are peers; decisions are collaborative without hierarchy.

**Example**: Screenwriter + Dialog Coach + Science Advisor + DP (all support the story)

```json
"decision_hierarchy": [
  "screenwriter: story direction",
  "dialog_coach: dialogue authenticity",
  "science_advisor: technical accuracy",
  "dp_persona: visual feasibility"
]
```

**When to use**: Creative domains where expertise is complementary, not hierarchical

---

## Anti-Patterns: What to Avoid

### Anti-Pattern 1: "Everything But The Kitchen Sink"

Adding personas just because they exist.

❌ **Bad**: "React Development Team" with React Specialist + Developer + UI Designer + Security + Cloud Architect + Database Expert + DevOps Engineer
- Too many members (7+)
- Not all activate together regularly
- Muddy decision hierarchy

✅ **Better**: React Fullstack Team (React Specialist + Developer + UI Designer + Security) + separate infrastructure team for deployment/cloud concerns

---

### Anti-Pattern 2: Implicit Collaboration

Defining a team without explaining *how* they work together.

❌ **Bad**:
```json
"members": ["persona1", "persona2", "persona3"]
(No collaboration_patterns, no workflow description)
```

✅ **Better**:
```json
"primary_workflow": "Investment Advisor orchestrates strategy with specialist input",
"collaboration_patterns": [
  {"members": ["investment_advisor", "tax_strategist"], "focus": "Tax-efficient withdrawal"},
  {"members": ["healthcare_expert", "social_security_specialist"], "focus": "Medicare timing"}
]
```

---

### Anti-Pattern 3: Unclear Primary Leadership

When it's not obvious who leads, teams become indecisive.

❌ **Bad**: No `default_primary` defined, or unclear decision_hierarchy

✅ **Better**: Clear `default_primary` with explicit decision hierarchy showing who decides what

---

### Anti-Pattern 4: Mismatched Context

Defining a team with members from different domains.

❌ **Bad**: Team includes personas from gaming + financial + development
- Different behavioral protocols, reference libraries, expertise scopes
- Team would be confused about which context rules apply

✅ **Better**: All team members are from the same domain (or at least same context_configuration.json)

---

## File Organization Conventions

### Where Teams Live

Teams are organized by context:

```
/personas/[domain]/teams/
  ├── team_name_1.json
  ├── team_name_2.json
  └── team_name_3.json
```

**Current Teams**:
- `/personas/financial/teams/retirement_planning_team.json` ✅ Active
- `/personas/development/teams/react_fullstack_team.json` ✅ Active
- `/personas/gaming/teams/hero_heaven_worldbuilding_team.json` (Planned, not yet created)

### Naming Conventions

**File naming**: `[team_name]_team.json` (snake_case)
- ✅ `retirement_planning_team.json`
- ✅ `react_fullstack_team.json`
- ✅ `hero_heaven_worldbuilding_team.json`
- ❌ `RetirementPlanningTeam.json` (use snake_case)
- ❌ `retirement_team.json` (be specific, not vague)

**team_name field**: Same as file name (without .json)
- `"team_name": "retirement_planning_team"`

**display_name field**: Human-readable
- `"display_name": "Retirement Planning Team"`

---

## Creating a New Team: Step-by-Step

### 1. Define Purpose

**Question**: What specific problem do these personas solve together?

**Example**: "Comprehensive retirement planning with tax efficiency and healthcare coordination"

---

### 2. Identify Members

**Question**: Which personas should be in this team?

**Criteria**:
- Each persona is frequently activated for this problem type
- Personas have distinct, complementary expertise
- You can explain why each member is necessary

**Example**: Investment Advisor, Tax Strategist, Healthcare Expert, Social Security Specialist, Insurance Analyst, Estate Planner

---

### 3. Choose Default Primary

**Question**: Who leads when the team activates?

**Guidelines**:
- Usually the broadest, most general member
- Someone who synthesizes other input
- The persona users would address first

**Example**: Investment Advisor (orchestrates the whole retirement plan)

---

### 4. Map Collaboration Patterns

**Question**: How do team members work together?

**Approach**: List out each meaningful pairing

```json
"collaboration_patterns": [
  {
    "members": ["investment_advisor", "tax_strategist"],
    "focus": "Withdrawal sequencing and tax efficiency"
  },
  {
    "members": ["healthcare_expert", "social_security_specialist"],
    "focus": "Medicare timing with benefit claiming"
  }
]
```

---

### 5. Define Decision Hierarchy

**Question**: Who decides what?

**Format**: `"persona_name: domain or authority"`

```json
"decision_hierarchy": [
  "investment_advisor: overall strategy and timeline",
  "tax_strategist: tax optimization",
  "healthcare_expert: cost estimation",
  "social_security_specialist: benefit timing",
  "insurance_analyst: gap coverage",
  "estate_planner: asset structure and protection"
]
```

---

### 6. Identify Activation Triggers

**Question**: What keywords/contexts trigger this team?

**List**: Contexts and keywords that indicate the team should suggest activation

```json
"auto_suggest_contexts": [
  "retirement planning",
  "early retirement",
  "withdrawal strategy"
],
"auto_suggest_keywords": [
  "retire",
  "retirement",
  "401k",
  "roth",
  "medicare"
]
```

---

### 7. Write Use Cases

**Question**: What specific scenarios use this team?

**Format**: Concrete scenarios, not abstract

```json
"use_cases": [
  "Comprehensive retirement timeline analysis",
  "Early retirement bridge strategy (age 55-65)",
  "Roth conversion ladder planning",
  "Medicare gap coverage evaluation",
  "Social Security benefit timing optimization"
]
```

---

### 8. Write JSON

Use CONFIG_REFERENCE.md schema and follow naming conventions.

---

### 9. Register in context_configuration.json

Add the team to the domain's context configuration:

```json
"available_teams": [
  "existing_team",
  "your_new_team"
]
```

---

### 10. Validate

**Checklist**:
- [ ] All members exist as persona schemas in the same domain
- [ ] Each collaboration pattern makes sense
- [ ] Decision hierarchy covers all members
- [ ] Activation keywords are specific (not vague)
- [ ] Use cases are concrete, not abstract
- [ ] Team has a clear purpose that's distinct from just "these personas"
- [ ] File named correctly and placed in right directory

---

## Testing Your Team

Once created, validate with these scenarios:

1. **Activation Test**: Does the team activate when a user mentions the keywords?
2. **Collaboration Test**: Do the collaboration patterns match the actual workflow?
3. **Leadership Test**: Does the default_primary persona clearly lead?
4. **Redundancy Test**: Is every member necessary? Would removing anyone weaken the team?

---

## Updating Existing Teams

Teams evolve. When to update:

- **Add a member**: New expertise domain relevant to the team's purpose
- **Remove a member**: No longer participates in collaboration patterns
- **Change primary**: Better leadership for the team's current use cases
- **Update patterns**: Collaboration workflow has changed
- **Add use cases**: Team now handles new scenarios

**Always document the change and update related context_configuration.json files.**

---

## Tips for Good Team Design

1. **Start small**: 3 personas is ideal. 4-5 is manageable. 6+ needs serious justification.
2. **Test before formalizing**: Activate the personas together in a few scenarios first. Only formalize as a team if they consistently activate together.
3. **Document the why**: Collaboration patterns and decision hierarchy are more important than membership.
4. **Use keywords wisely**: Specific triggers (e.g., "retirement planning") not generic ones (e.g., "financial advice").
5. **Iterate**: Teams will change as you use them. Revisit and refine quarterly.
6. **Reference the domain**: All team members should be from the same context (gaming, financial, development, writing).

---

## Related Documentation

- **CONFIG_REFERENCE.md** — Full JSON schema for team definitions
- **ARCHITECTURAL_DECISIONS.md** — Why teams exist in this framework
- **[domain]/context_configuration.json** — How teams are registered and activated
- **USER_GUIDE.md** — How end users activate and work with teams
