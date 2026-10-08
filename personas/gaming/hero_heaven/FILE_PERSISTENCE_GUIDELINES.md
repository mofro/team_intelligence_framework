---
title: File Persistence Guidelines
project: TTRPG_Tarim_Shaiel
type: operational_reference
purpose: Quick decision framework for filesystem vs. context-only artifacts
created: 2025-12-02
updated: "{{date}}"
---

# File Persistence Guidelines

## Write to Filesystem IF
- It's a source-of-truth document (world mechanics, setting details, character archetypes)
- It needs to be referenced across multiple conversations
- Lore Keeper needs to track or update it
- It's a session artifact or decision log
- It's something that should be version-controlled or shared

## Keep in Context Only IF
- It's ephemeral brainstorming or exploration
- It's only relevant to this conversation
- It's a working draft that might be discarded
- It's a temporary recap or reference

## Examples
✅ Filesystem:
- world/mechanics.md (source of truth for game mechanics)
- characters/archetypes.md (character templates and patterns)
- narrative/session_notes.md (what happened in a session)
- DECISION_LOG.md (why we chose X over Y)
- world/factions.md (faction details and relationships)

❌ Context Only:
- "What if we made magic work like X?" (brainstorm, might be rejected)
- Quick recap of last few messages (temporary reference)
- "Here's how I understood your request..." (restatement in conversation)
- Rejected world ideas (unless archiving them to filesystem)

## Lore Keeper Rule
If the Lore Keeper needs to reference it, track it, or consolidate it → filesystem.

---

## Metadata Conventions

All persistent files should include frontmatter with standardized metadata fields.

### Required Fields
```yaml
---
title: [Document title]
project: TTRPG_Tarim_Shaiel
type: [content type - see below]
---
```

### Content Types
- `world_building` - Setting content (locations, cultures, history)
- `narrative` - Story content (sessions, plot, events)
- `mechanics` - Game systems (rules, charms, progression)
- `character` - Character frameworks and archetypes
- `reference` - External reference materials
- `template` - Reusable content templates
- `operational` - Project infrastructure and workflows

### Visibility & Status
```yaml
visibility: public | gm_secrets
status: draft | review | canon | deprecated
```

**Visibility:**
- `public` - Player-facing content (or will be shared with players)
- `gm_secrets` - GM-only content (plot secrets, future reveals, mechanical balance notes)

**Status:**
- `draft` - Work in progress, not finalized
- `review` - Complete but needs review/approval
- `canon` - Finalized, official campaign content
- `deprecated` - Superseded or no longer used

### Optional Fields
Use these when relevant:
```yaml
session_type: awakening | convergence | adventure
archetype: warrior | seeker | breaker | all
location_type: city | landmark | region | dungeon
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
tags: []
```

### Full Template
See [[metadata_template|Metadata Template]] for a complete example.

### Folder + Metadata Approach
Tarim-Shaiel uses **both** folder organization **and** metadata:
- **Folders** organize content physically (`/narrative/gm_secrets/`, `/world/locations/`)
- **Metadata** enables searching, filtering, and cross-referencing
- This dual approach provides both structure and flexibility
