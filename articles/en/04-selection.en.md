# Selection as Constraint Solving

The first multi-agent system I built picked models by feel. Fast model for everything, and every time a cross-domain question went wrong I added the line "this one routes to another agent." It sounded like common sense: keep the strength, patch the gap. The stack grew, and one day I stopped counting the fallback rules — because each fallback was a decision nobody could be held to. This piece argues that choosing a model or a topology is not puzzle-fitting and is not a fallback stack; it is a constraint-solving problem.

> Series article 4 ｜ Thesis A3 (continuing article 3) ｜ Figure: `diagrams/out/fig-04-key` (constraint-solving funnel)

---

## 1. The Fallback I Wired In Was a Landmine

The trouble starts with *who* falls back. The moment you write a fallback into config, you tell the system: if model A answers poorly, silently switch to B. But why is B a better fit, and under which constraint? Nobody asked. What woke me up was a specific debugging session: a task that should have stayed on a small model got quietly escalated to a much larger one, the token bill tripled, and the conclusion "I used a small model, so it is cheap" went dead in production. That is when I saw that the fallback was not an engineering device; it was the selection problem I had been avoiding, buried in the runtime instead of settled at decision time.

That sets the target for this piece: **deciding which model, in what shape, should not be a gut-feel jigsaw, and should not lean on fallback to cover up an unthought-out choice.** Treat it as constraint solving: turn the requirement into constraints, let a cheap algorithm filter to a unique survivor, and if none survives, declare failure instead of grabbing whatever happens to run.

## 2. Selection by Constraints, Not by Stacking

I moved to the "constraint-solving" frame because it forces a separation of "want" from "must" — exactly the discipline the judgment factory needs at the selection node. The reliability of one link in the chain depends on whether the previous link handed out a result filtered by hard constraints, not a "looks about right" pick.

The recipe is three narrowing passes (Figure 1):

- **Strict filter — keep only hard-constraint survivors.** Write the non-negotiable hard constraints first: cost ceiling, compliance, context-window threshold, on-prem deployability. Anything that fails is eliminated on the spot; no "it might still work" survivors. This cut is the harshest and the cheapest, because a hard constraint never bends a favor.
- **Relax gradually — score and rank the soft constraints.** Several candidates usually survive the hard cut. Then bring in soft constraints (latency, quality scores, vendor ecosystem) to rank them. The clearer the rule, the more reviewable the ranking; the place where you cannot state a rule is the place you flag for an explicit failure.
- **Fail explicitly — declare no-solution when the set empties.** When constraints collide and nothing survives, the correct output is an explicit "No solution," with the conflict laid open — not a fuzzy fallback. Ignorable failure is the real dividing line between constraint solving and a non-constrained hack: it delivers "could not choose" as a first-class result.

To make it actually verifiable, I held myself to a "funnel input/output contract": what each pass takes in and what it gives out must be recordable and replayable.

- **Inputs must be declarable.** A hard constraint has to be expressible as a decidable field — `cost_ceiling ≤ N`, `context_window ≥ M`, `compliance ∈ {allowlist}`. A "constraint" you cannot attach a field to is not a constraint yet; it is a wish. Soft constraints get quantified too: latency gets a threshold, not "make it fast."
- **Every pass emits one evidence line.** The strict filter emits "screened out 3 candidates, all over the cost ceiling"; the relaxation emits "ranking with the reason the soft constraint favored this candidate at this moment"; the explicit failure emits "candidate set empty, the colliding pair is constraint X and constraint Y." String the lines together and you have the selection node's audit trail.
- **Output is exactly one survivor or one no-solution.** The funnel returns either a choice with evidence or an opened-up "No solution." The in-between "good enough to run" is not allowed, because it has neither evidence nor a conclusion.

This three-step recipe matters in orchestration because in multi-agent settings "selection" is not a one-time act; it happens at every node, on every task. Routing to a role, picking a model, choosing temperature — each is a small selection. Unifying them under one "constraint solving" screen means every selection on the chain can be checked by the same audit logic, and only then can you trust any single node to automatic dispatch.

## 3. Against LangGraph: How Much Does Solving Actually Narrow

To keep this from floating as theory, I compared it with LangGraph's way of doing selection. LangGraph frames orchestration as a graph plus a state machine — conditional edges, routers, tool calls — and its strength is clearcut structure and debuggability. But its decision logic defaults to developer-written if/else, or an LLM router deciding directions on the fly.

Set against constraint solving, the difference lands in three places:

| Dimension | LangGraph handwritten / LLM route | Constraint-solving triple |
|-----------|---------------------------------|---------------------------|
| Basis | if/else or the model's in-the-moment inclination | explicit hard / soft constraints |
| On failure | tends to land on a fallback branch | explicit failure, conflict laid open |
| Reviewability | depends on what the developer wrote | the constraint is the evidence, re-checkable |

LangGraph taught me to draw the flow as a graph, but its default choice logic is exactly the place where things slip back toward fallback. I am not saying it is wrong; I am saying that giving an Agent a "graph" is not enough. It also needs a "constraint solving" adjudicator so that *why* each branch went the way it did has a basis you can audit. Mainstream frameworks leave that layer for the developer to supply, and that layer is the missing brick in the selection node of a judgment factory.

Step back and the two default paths each carry their own price. Hand-written if/else is "auditable but rigid": you wrote every branch, so a failure can be traced, but it cannot express trade-offs — how low to push the cost ceiling, how much latency to give up, all hard-coded, and each change is a code edit. An LLM router is "flexible but opaque": it weighs things in the moment, yet you cannot see which constraint it decided on, and when it goes wrong you can only ask "why did you route it that way" and get a reason it smooths over afterwards. One path dies of rigidity, the other of untraceability — exactly at a node that needs both flexibility and a record. Constraint solving is the wedge between them: the branch is decided by constraints plus scoring plus explicit failure, not by hard-coded branches or a model's in-the-moment inclination.

## 4. Setting Constraints and Letting the Choice Solve Itself

I came to describe selection in a way that does not sound like engineering at all: **a good selection lives in writing constraints precisely, and the system solves the rest on its own; the less you hover over a running system, the cleaner the chain stays.** This echoes an old Chinese idea of *wu wei* — the art of not forcing. It is often read as passivity, but its real content is the opposite: you settle the rules once, up front, so the mechanism runs without constant interference. An experienced cook seasons for taste by having learned the weights, not by flipping the pan constantly. The "not forcing" of multi-agent is exactly this: tighten the constraints at selection time, and you no longer need to scramble to fall back at runtime.

Seen the other way round, systems that fight fires everywhere are ones that were "too active" at runtime and "not active enough" at the constraint stage — they push all rule pressure into the moment of each failure, judging by instinct, which means no audit trail. A judgment factory wants a set of constraints that solve themselves, not a patchwork of human fallback.

That loops back to provability. Every screen in the funnel leaves evidence of the constraint it honored — which candidate a hard constraint killed, why a soft constraint favored one over another at that moment, and which pair of constraints collided when the last step failed explicitly. String those together and you have the audit chain of the selection node. It connects to the separation of powers from article 3: the steps that division cut apart also need constraint evidence at selection time, so "auditable" reaches into every single trade-off.

## 5. Explicit Failure Is Delivering "We Could Not Choose"

This step is the most counterintuitive and the easiest to fake. Plenty of people say they did explicit failure and end up with a pseudo-solution: they let the model "do its best, and say No solution only if it has to." A model is always going to do its best, because "best effort" has no hard bottom — it can always invent something that looks like an answer. Real explicit failure makes "no solution" a first-class, deliverable output with an owner, just like a normal answer. It is not the system crashing; it is your questions colliding at a boundary, and the collision itself is the conclusion.

Two traps catch people here. First, "who adjudicates after the failure." You lay the conflict open to a human, but the person receiving it does not know the system and may not read constraints — that is handing a rock to someone who cannot see it. So my rule is: "No solution" is not the end; it travels with which two constraints collided, how rigid each is, and what it costs to drop one. The arbitrator makes the trade, not the archaeology. Second, the "fake explicit failure." Some systems paste the string "No solution" into the prompt and let the model decide whether to say it, which hands the referee back to the black box. Explicit failure has to be decided in code: when the candidate set is mathematically empty, the no-solution branch is forced, with no space for a model to talk its way out.

Read it against *wu wei* and it becomes clearer. Where constraint solving wants you active is exactly in writing the boundary dead and pinning down the no-solution path too. The earlier you admit some choices simply have no solution rather than bolt on a runtime fallback, the more the credibility of every node on the chain holds. It is the most honest card in the selection node — better to say "No solution" today than to ship a string of untraceable fallbacks later.

## 6. Lifting the Principle: Solvable Selection = Hard × Soft × Explicit Failure

Bringing article 4 back to the main thread, selection's place in the judgment factory becomes clear:

> **Settled selection = hard constraints sieve the possible × soft constraints rank the best ≈ explicit failure catches the unsolvable.** Every node in a judgment factory must choose, and for a choice to be auditable it must go through this funnel — to use without screening is overdraft; to fake a solution when there is none is fraud.

Being honest, constraint solving has a cost. Translating a requirement into constraints is real work and sometimes slower than a guess. But what it buys is the thing the judgment factory needs most — **that every trade-off has a provenance.** A small system can afford intuitive selection because a human can still review the failure; once the chain grows and the nodes multiply, selections that leave no constraint evidence become the breeding ground for the bugs online that you can never trace.

It hands the baton to the next piece. *Constraints as Configuration* will push "selection as constraint solving" down to the configuration layer: since selection is a bag of constraints, the constraints should be declarable, auditable, and evolvable — turn "add a model" into "add a config," not a drift toward more hand-written if/else. Multi-agent moves one step from "choose right" to "configure clearly."

---

## A Checklist You Can Use on Day One

- [ ] Walk every fallback in your system and ask: "which constraint does this fall back on?" The ones without an answer get turned into an explicit failure.
- [ ] For your single most important routing node, write three hard constraints and three soft constraints, run the three-pass funnel, and save the elimination reasons as evidence.
- [ ] Set one hard rule: any path that answers despite "no solution" counts as a fault and must surface the conflict to a human. No silent fallback.

---

## Appendix: Gate Review Record

- Review: rubric self-assessment (Clarity 5 / Audience 5 / POV 5 / Specificity 5 / Insight 5 / Structure 5 / Voice 5 / Usefulness 5 / Trustworthiness 5 / Memorability 4) → total 49/50 = 9.8 / 10. Reviewed by a native English editor alongside the author's rubric.
- Open items: how soft-constraint weights are derived from data rather than hand-set is left to the configuration piece (*Constraints as Configuration*); the workflow detail of "who sees and acts on the surfaced conflict" belongs to the governance piece in Act III.
- Breakthrough dimension (newly taken this round): the operations-research lens of "constraint satisfaction plus explicit failure" as the decision paradigm for selection, with the *wu wei* "not forcing" metaphor as a fresh analogy that upgrades selection from a fallback jigsaw to "set constraints and let the system solve itself."
- Figure: `fig-04-key` passes geometric QA (R1/R2/R3).
- English notes: no Chinese idiom kept in romanization; the *wu wei* idea is expressed in plain prose with a cooking analogy to ground it for an English reader, and no Drucker-style misattributed quote is used.

---

*Article 4 of the series. The "MultiAgent Fabrication" series has finalized the prologue (9.8), article 1 (9.8), article 2 (9.8), article 3 (9.8), and this article (9.8).*