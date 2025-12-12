# Persona Interaction Architecture v1.0

## Addressing System

### Primary Addressing Format

- **GitHub-style**: `@persona_name` or `@custom_name`
- **Examples**: `@blits_developer`, `@security_specialist`, `@johnny_blits` (if custom name set)

### Name Resolution Hierarchy

1. **Custom name** (if set in persona schema): `@johnny_blits`
2. **Persona name** (snake_case default): `@blits_developer`
3. **Display name** (fallback): `@Blits Developer`

### Naming Conventions

- **Persona names**: `snake_case` for role-like references (`blits_developer`, `security_specialist`)
- **Custom names**: User-defined, any format (`johnny_blits`, `SecurityGuy`, `lightning-expert`)
- **Display names**: Human-readable (`Blits Developer`, `Security Specialist`)

## Schema Architecture

### Portability Decision: **Extended Schema**

**Rationale**: More portable and backward-compatible. Existing personas work unchanged, collaboration features are additive.

### Extended Persona Schema Format

```json
{
  "schema_version": "1.2",
  "metadata": {
    "name": "persona_name_here",
    "description": "Role description",
    "author": "creator",
    "version": "1.0",
    "created_date": "2025-01-18"
  },
  "persona": {
    "persona_name": "snake_case_identifier",
    "display_name": "Human Readable Name", 
    "custom_name": null,
    "role": "specific role description",
    "expertise": ["domain1", "domain2", "domain3"],
    "approach": "methodology description"
  },
  "collaboration": {
    "expertise_scope": ["primary", "secondary", "tertiary"],
    "defers_to": ["other_persona_names"],
    "collaborates_well_with": ["complementary_personas"],
    "approach_style": "consultative|directive|supportive",
    "conflict_style": "defer|argue|compromise"
  },
  "behavioral_rules": [
    "persona-specific behavior patterns"
  ]
}
```

## Fallback Hierarchy

### Question Routing Priority

1. **Direct addressing**: `@specific_persona` → routes to that persona
2. **Natural expertise fit**: Analyze question content → route to best match
3. **Developer Coding Persona**: General development guidance
4. **Project settings**: Ultimate fallback for non-development questions

### Collaboration Fallback

1. **Multi-persona collaboration**: When expertise overlaps or question spans domains
2. **Single persona with consultation**: Lead persona mentions team input
3. **Developer Coding Persona coordination**: General persona orchestrates when needed
4. **Project settings**: When all personas are outside scope

## Address Resolution Examples

### Schema Definition

```json
{
  "persona_name": "blits_developer",
  "display_name": "Blits Developer",
  "custom_name": "johnny_blits"
}
```

### Valid Address Formats

- `@johnny_blits` (custom name - preferred)
- `@blits_developer` (persona name - standard)
- `@Blits Developer` (display name - fallback)

### Auto-routing Examples

- **"Is this component pattern optimal?"** → `@blits_developer`
- **"Would this authentication flow be secure?"** → `@security_specialist`
- **"How should we structure this UI component?"** → `@lightning_developer`
- **"What's the best architecture approach here?"** → `@developer_coding_persona`
- **"What's the weather like?"** → Project settings (no relevant persona)

## Implementation Notes

### Schema Compatibility

- **Backward compatible**: Existing personas without collaboration fields work unchanged
- **Graceful degradation**: Missing collaboration fields default to solo operation
- **Additive enhancement**: New fields extend functionality without breaking existing behavior

### Custom Name Management

- **User flexibility**: Users can set memorable nicknames (`@johnny_blits` instead of `@blits_developer`)
- **Conflict resolution**: Custom names take precedence over persona names
- **Discovery**: System suggests available personas if addressing fails

### Collaboration Integration

- **Seamless teamwork**: Personas reference each other naturally using `@persona_name` format
- **Memory consistency**: Collaboration history uses consistent persona references
- **Cross-referencing**: Personas can defer or collaborate using the same addressing system

## Testing Protocol

### Phase 1: Basic Addressing

1. Create personas with all three name types (persona_name, display_name, custom_name)
2. Test direct addressing with each format
3. Verify fallback hierarchy works correctly
4. Confirm non-existent personas gracefully degrade

### Phase 2: Auto-routing

1. Test questions that clearly map to single personas
2. Test questions that should trigger collaboration
3. Test questions outside all persona expertise
4. Verify developer coding persona → project settings fallback

### Phase 3: Collaboration Integration

1. Test personas referencing each other using @names
2. Test collaboration memory using consistent addressing
3. Test custom name persistence across conversations
4. Test conflict resolution when multiple addressing options exist

## Architecture Benefits

### For Users

- **Natural interaction**: GitHub-style addressing feels familiar
- **Flexibility**: Custom names allow personalization
- **Discoverability**: Multiple ways to reference same expertise
- **Graceful failure**: System handles addressing errors elegantly

### For Implementation

- **Backward compatibility**: Existing schemas work unchanged
- **Extensibility**: New collaboration features are additive
- **Portability**: Personas work across different projects
- **Maintainability**: Clear separation between persona definition and collaboration behavior

### For Collaboration

- **Consistent referencing**: All personas use same addressing system
- **Memory efficiency**: Single addressing standard for collaboration history
- **Cross-persona communication**: Easy referencing between team members
- **Hierarchical fallback**: Clear escalation path when expertise is insufficient

---

**Ready for persona creation!** This architecture provides:

- ✅ Natural `@github_style` addressing
- ✅ Custom name flexibility with fallbacks
- ✅ Backward-compatible schema extension
- ✅ Clear hierarchical routing: direct → expertise → developer coding persona → project
- ✅ Seamless collaboration integration

Next step: Create the personas using this extended schema format.
