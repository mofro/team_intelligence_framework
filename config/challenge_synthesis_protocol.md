# Challenge/Synthesis Protocol v1.1

**Spec status**: Hardened. v1.0 established the interface contract in prose; v1.1 adds normative language, an ID-tagged artifact schema, and mechanically-checkable conformance criteria so an implementation can be verified rather than eyeballed. See Changelog at the end.

Normative keywords (MUST, MUST NOT, SHOULD, MAY) are used per RFC 2119 intent: MUST/MUST NOT are hard conformance requirements; SHOULD is a strong default that can be deviated from with reason; MAY is genuinely optional.

## Purpose

This document is the **runtime-agnostic interface contract** for two-phase challenge/synthesis collaboration. It defines what each phase must receive and produce, and how to check whether a given output conforms. Any runtime that satisfies this contract is a valid implementation — Claude Code, a shell script, a Jupyter notebook, or manual two-conversation orchestration are all equivalent at the protocol layer.

The protocol exists because genuine challenge and integrated synthesis are structurally incompatible goals within a single LLM invocation. A model asked simultaneously to challenge and synthesize will coherence-drift toward synthesis. Separating them into distinct execution contexts removes the conflict.

---

## Two-Phase Architecture

```
[Original Request + Domain Context]
          │
          ▼
    ┌─────────────┐
    │  Phase 1    │  ← Challenge Phase (separate invocation)
    │  Challenge  │    Adversarial lens. No synthesis framing.
    └──────┬──────┘
           │  Challenge Artifact (ID-tagged)
           ▼
    ┌─────────────┐
    │  Phase 2    │  ← Synthesis Phase
    │  Synthesis  │    Unified voice. Traces to every RC-n.
    └─────────────┘
```

---

## Phase 1: Challenge

**Purpose**: Surface weaknesses in the premise before solutions form. The challenge phase must be adversarial without being hostile — its job is to find what's wrong, missing, or unexamined.

**Behavioral contract**:
- Phase 1 output MUST NOT contain a solution, recommendation, or implementation path
- Phase 1 output MUST NOT use helpfulness-oriented framing ("I can help with that", "great question")
- Phase 1 MUST interrogate the premise, not only implementation details
- Phase 1 MUST produce a `verdict` of exactly one of `PROCEED`, `REFRAME`, `DEFER`
- Phase 1 SHOULD identify hidden assumptions the request takes for granted
- Phase 1 SHOULD surface risks, edge cases, and second-order effects
- Phase 1 MAY produce zero `premise_flags` or zero `risks_and_edge_cases` entries only when the request genuinely has none — an empty section MUST NOT be used to skip effort

**Inputs**:
- `original_request` (required): The user's request verbatim
- `domain_context` (required): The active `challenge_focus` from the domain's `context_configuration.json`
- `active_personas` (optional): Which specialist lenses should challenge; defaults to all relevant

> **Scope note**: This input surface assumes `original_request` is self-contained. No conversation history, session state, or project context is defined as an input. See Known Open Questions — Context Scope.

**Output — Challenge Artifact Schema**:

| Field | Cardinality | Notes |
|---|---|---|
| `schema_version` | 1 | Must match the protocol version's artifact schema (currently `1.1`) |
| `verdict` | 1 | Exactly one of `PROCEED`, `REFRAME`, `DEFER` |
| `original_request` | 1 | Verbatim restatement |
| `premise_flags` (PF-n) | 0+ | MUST be non-empty unless the request has no unstated assumptions |
| `risks_and_edge_cases` (RE-n) | 0+ | MAY be empty for low-stakes requests |
| `alternative_framings` (AF-n) | 0+ | MUST be non-empty if `verdict = REFRAME` |
| `required_clarifications` (RC-n) | 0+ | MUST be non-empty if `verdict = DEFER` |

Every entry in `premise_flags`, `risks_and_edge_cases`, `alternative_framings`, and `required_clarifications` MUST carry a stable ID (`PF-1`, `RE-1`, `AF-1`, `RC-1`, ...). IDs exist so Phase 2 can be checked for traceability — see Conformance Criteria below.

**Template**:

```
CHALLENGE ARTIFACT
==================
schema_version: 1.1
verdict: PROCEED | REFRAME | DEFER

original_request: [verbatim]

premise_flags:
- [PF-1] [assumption being taken for granted]
- [PF-2] [hidden constraint the request doesn't acknowledge]

risks_and_edge_cases:
- [RE-1] [what breaks at scale / under edge conditions]
- [RE-2] [second-order effect not considered]

alternative_framings:
- [AF-1] [restatement that changes the solution space]
- [AF-2] [different problem the request might actually be solving]

required_clarifications:
- [RC-1] [question that must be answered for good synthesis]
- [RC-2] [decision that hasn't been made but needs to be]
```

The artifact format is intentionally human-readable prose, not JSON — structure and ID traceability matter; verbosity does not. A good challenge artifact is concise and pointed.

---

## Phase 2: Synthesis

**Purpose**: Produce a unified, integrated response that has genuinely absorbed the challenge artifact. The synthesis phase speaks with the authority of the full team and the humility of having been challenged.

**Behavioral contract**:
- Synthesis output MUST, for every `RC-n` in the challenge artifact, either resolve it explicitly or state an explicit deferral with reason — silent omission is a conformance violation
- Synthesis output MUST acknowledge every `AF-n` that changed the synthesis direction
- If `verdict = REFRAME`, synthesis MUST lead with the reframing before proposing solutions
- If `verdict = DEFER`, synthesis MUST state what's missing and what would unlock synthesis, and MUST NOT proceed to a full solution
- Synthesis SHOULD apply the primary voice system: one voice leads, others woven in seamlessly

**Inputs**:
- `original_request` (required): The user's request verbatim
- `challenge_artifact` (required): Full ID-tagged output of Phase 1
- `domain_context` (required): Full domain `context_configuration.json`

> **Scope note**: Same limitation as Phase 1 — no conversation history or session state is defined as an input. See Known Open Questions — Context Scope.

**Output**: Unified synthesis response per the active collaboration framework (`persona_collaboration_framework_v2.md`)

---

## Conforming Runtimes

All of the following satisfy the protocol. None are required infrastructure.

| Runtime | How to run Phase 1 | How to run Phase 2 |
|---|---|---|
| **Manual two-conversation** | New chat with `challenge_phase_prompt.md` as system prompt | New chat (or same) with challenge artifact pasted as context |
| **Shell script + any LLM CLI** | `llm -s "$(cat challenge_phase_prompt.md)" "$request"` | `llm -s "$(cat synthesis_prompt.md)" "$request + $artifact"` |
| **`llm` CLI (Simon Willison)** | Same as above; swap backend with `-m model_name` | Same |
| **Claude Code** (reference impl) | `/challenge [request]` — see `.claude/commands/challenge.md` | `/synthesize [request]` — see `.claude/commands/synthesize.md` |
| **Jupyter notebook** | Cell 1: challenge API call | Cell 2: synthesis API call with Cell 1 output |
| **Python script** | `anthropic.messages.create(system=challenge_prompt, ...)` | `anthropic.messages.create(system=synthesis_prompt, messages=[..., artifact])` |

The shell script pattern is the most portable and philosophically explicit: it treats the protocol as UNIX composition.

---

## Domain Challenge Focus

Each domain's `context_configuration.json` contains a `challenge_focus` field that scopes the adversarial lens. The challenge phase uses this as the primary interrogation axis.

| Domain | `challenge_focus` |
|---|---|
| development | `architecture_goals_and_software_correctness` |
| financial | `long_term_financial_outcomes_and_competing_priorities` |
| gaming | `narrative_goals_and_player_experience` |
| writing | `story_goals_and_narrative_consistency` |
| ai_development | `platform_capabilities_and_implementation_constraints` |

---

## What This Protocol Does Not Define

- **Persona identity**: Governed by individual persona schemas
- **Team composition**: Governed by team definition files
- **Synthesis voice patterns**: Governed by `persona_collaboration_framework_v2.md`
- **Domain-specific expertise routing**: Governed by `context_configuration.json`

This protocol defines only the seam between challenge and synthesis. Everything else is downstream.

---

## Known Open Questions

Unlike "What This Protocol Does Not Define" above — things intentionally delegated elsewhere — these are gaps this protocol has not yet resolved anywhere. Marked here so they're visible rather than silently discovered by whoever hits them first.

### Context Scope (unresolved)

The input surface for both phases (`original_request`, `domain_context`, `active_personas`, `challenge_artifact`) assumes the request is self-contained — fully meaningful without any prior conversation, session, or project history. This isn't incidental: every isolation mechanism this protocol relies on (a fresh subagent context, a genuinely separate conversation) achieves contamination-immunity specifically *by* withholding that history. Isolation and context-starvation are the same lever, not two separate properties.

This is a real scope boundary on the protocol as currently specified, not a minor gap:

- **Well-suited**: standalone decision points whose meaning doesn't depend on anything said earlier
- **Poorly suited as specified**: questions embedded in an ongoing working session, where the request's real meaning depends on situational context the request text alone doesn't carry (constraints already ruled out, diagnoses already made, prior decisions the new question is downstream of) — arguably the more common real-world case

**Unresolved**: whether to add an explicit `session_context` (or similar) input; what "appropriately scoped" context would mean if added — full history, a compacted/summarized subset, or something else; and how to admit any of it without reintroducing the context-contamination risk the current isolation exists to prevent. No dial position has been chosen.

**Until resolved**: treat this protocol as scoped to self-contained requests. A runtime applying it to a context-dependent question embedded in an ongoing session is operating outside what this spec has actually considered.

---

## Conformance Criteria

Each criterion has an ID, a MUST/SHOULD level, and a check procedure — something a human, an LLM-as-judge, or a script can actually run against a real transcript. A runtime is **structurally conformant** if it passes all `S-*` criteria and **behaviorally conformant** if it also passes all `B-*` criteria. Full conformance requires both.

### Structural (artifact shape)

| ID | Level | Criterion | Check procedure |
|---|---|---|---|
| S-1 | MUST | Challenge artifact contains `schema_version` and a `verdict` of exactly one valid value | Parse the artifact; verify both fields present and `verdict ∈ {PROCEED, REFRAME, DEFER}` |
| S-2 | MUST | Every `premise_flags`/`risks_and_edge_cases`/`alternative_framings`/`required_clarifications` entry carries a unique ID in its category | Scan entries; confirm ID prefix matches category and no duplicate IDs |
| S-3 | MUST | If `verdict = REFRAME`, `alternative_framings` is non-empty | Check cardinality against verdict |
| S-4 | MUST | If `verdict = DEFER`, `required_clarifications` is non-empty | Check cardinality against verdict |

### Behavioral (Phase 1)

| ID | Level | Criterion | Check procedure |
|---|---|---|---|
| B-1 | MUST | Phase 1 output contains no solution, recommendation, or implementation proposal | Read output; flag any sentence proposing a course of action rather than a question or risk |
| B-2 | MUST | Phase 1 output contains no helpfulness-oriented opener | Check first 1-2 sentences for service-oriented framing |
| B-3 | SHOULD | `premise_flags` is non-empty for any request with an implicit assumption | Judge whether the request contains an unstated assumption a domain expert would flag; if so, confirm ≥1 `PF-n` entry exists |

### Behavioral (Phase 2 — traceability)

| ID | Level | Criterion | Check procedure |
|---|---|---|---|
| B-4 | MUST | Every `RC-n` from the challenge artifact is referenced, resolved, or explicitly deferred in the synthesis output | For each `RC-n`, search synthesis text for a corresponding resolution or deferral; flag any `RC-n` with no trace |
| B-5 | MUST | Every `AF-n` that changed the synthesis direction is acknowledged | For each `AF-n`, confirm the synthesis either adopts, rejects with reason, or explicitly notes it didn't change the approach |
| B-6 | MUST | If `verdict = REFRAME`, the reframing appears before any proposed solution in the synthesis output | Check ordering of content |
| B-7 | MUST | If `verdict = DEFER`, the synthesis output states missing information and does not present a complete solution | Check for a "what's missing" statement and absence of a full solution |

### Runtime (protocol-level)

| ID | Level | Criterion | Check procedure |
|---|---|---|---|
| R-1 | MUST | Phase 1 and Phase 2 run as genuinely separate invocations (separate system prompts / separate calls), not one invocation split by instruction | Inspect the runtime's call structure |
| R-2 | SHOULD | The full protocol can be exercised via manual two-conversation orchestration with no tooling | Attempt it by hand once per new runtime type |
| R-3 | SHOULD | Swapping the LLM backend requires changing a model identifier, not the protocol structure | Attempt a backend swap; confirm no prompt restructuring is needed |

---

## Worked Example

**Domain**: development · **challenge_focus**: `architecture_goals_and_software_correctness`
**Request**: "Should we add a caching layer in front of the API?"

### Phase 1 output

```
CHALLENGE ARTIFACT
==================
schema_version: 1.1
verdict: DEFER

original_request: Should we add a caching layer in front of the API?

premise_flags:
- [PF-1] Assumes the bottleneck is read latency, not write contention or downstream service cost
- [PF-2] Assumes cache invalidation strategy is a solved problem for this data's freshness requirements

risks_and_edge_cases:
- [RE-1] Stale reads could mask a downstream data-consistency bug rather than genuinely improving performance
- [RE-2] Cache warms cold on deploy — adds a latency spike class that doesn't exist today

alternative_framings:
- [AF-1] The actual problem may be an unindexed query, which a cache would mask rather than fix

required_clarifications:
- [RC-1] What does current latency profiling actually show — is it read-heavy and cache-shaped?
- [RC-2] What's the acceptable staleness window for this data?
```

### Phase 2 output (excerpt, showing traceability)

> Before recommending a caching layer, two things need answers [RC-1, RC-2 traced]. Profiling data would tell us whether this is genuinely a read-latency problem or something a caching layer would only mask — [AF-1] an unindexed query would produce the same symptom and caching over it hides the real fix rather than solving it. If profiling confirms read latency is the driver, staleness tolerance [RC-2] determines whether we're looking at a short-TTL cache or something more aggressive. [RE-2] worth flagging: a cache adds a cold-start latency class on deploy that doesn't exist today, so it isn't a free win even once justified.

This passes B-4 (both RC-n traced), B-5 (AF-1 acknowledged and adopted into the synthesis), and B-7 (states missing info, doesn't present a full solution — consistent with `verdict = DEFER`).

---

## Non-Conforming Examples (Anti-Patterns)

**Violates B-1/B-2** (Phase 1 solutioning):
> "Great question! I'd recommend Redis with a 5-minute TTL — here's how to set it up..."
This is a synthesis response wearing a challenge-phase hat. No premise interrogation occurred.

**Violates B-4** (silent RC omission):
> Synthesis response proceeds directly to "Yes, let's add caching" without addressing `RC-1` or `RC-2` at all. Even if the eventual recommendation is defensible, the omission is a conformance failure — the challenge phase's work was discarded rather than absorbed.

**Violates S-3** (empty alternative_framings under REFRAME verdict):
> `verdict: REFRAME` with an empty `alternative_framings` section. A REFRAME verdict without a stated reframing gives Phase 2 nothing to lead with.

---

## Changelog

**v1.1 (amended)** — Added "Known Open Questions" section and scope notes on both phases' Inputs, marking that the input surface assumes self-contained requests with no defined path for conversation/session history. Surfaced while evaluating a Workflow-based runtime, which made the isolation-vs-context tradeoff concrete. No schema or conformance-criteria change; purely additive documentation of an unresolved gap.

**v1.1** — Spec-hardening pass. Added RFC-2119 normative language, ID-tagged artifact fields (`PF-n`/`RE-n`/`AF-n`/`RC-n`), formal artifact schema table, replaced prose "Verification" section with itemized Conformance Criteria (structural/behavioral/runtime), added a worked example and anti-pattern examples. No change to the two-phase architecture or conforming runtimes list.

**v1.0** — Initial protocol: two-phase architecture, challenge artifact format (unversioned prose), conforming runtimes table, domain challenge focus table.
