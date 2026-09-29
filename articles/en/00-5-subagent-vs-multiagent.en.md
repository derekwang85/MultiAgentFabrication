# Us vs. Subagents: the Contrast That Keeps Getting Misread

> I finally found the trap hidden inside one word: subagents. Open Codex, TRAE, or OpenClaw and it will "spawn subagents"—three or four windows working in parallel. You also talk about "multi-agent systems," so you get cornered by one question: if you already have subagents, why are you still building a Multi-Agent anything? This piece answers that contrast head-on. The difference is not whether a system has "variants." It is what those variants are. One is a hand that the main loop reaches out with temporarily. The other is a responsible actor for judgment living in the meta layer and the product layer. The former is an execution primitive being called. The latter is an organization that makes judgment divisible, verifiable, and auditable.
> Stand-alone contrast special ｜ Position: 0.5 (between the prologue and No. 1) ｜ Figure: `diagrams/out/fig-00-5` (Subagent vs. Judgment Factory: an eight-dimension split)

I found that the same word, "agents," hides two creatures, and telling them apart is the price of admission.

---

## 1. Hook: the same word, two kinds of variants

If you chat with one agent and ask it to fix a block of code or draft a document, you will probably never touch the word "subagent." The moment you open a tool with a multi-agent collaboration view, though, Codex, TRAE, or an open-source runner such as OpenClaw, you watch a main window hold several subagents on the side, each on its own canvas, each running a round and handing results back. It looks exactly like the multi-agent system you mean to build. Every line reads as "a set of agents dividing the work."

So almost everyone who hears me describe the judgment factory fires back the same line: **"Isn't this just subagents?"** The tone says it: you spent all that effort rebuilding a wheel.

The question is not hostile. It is a resolution problem. At the coarsest grain, "many agents appear together," the two things look identical. If you only look at whether a system has variants, you cannot separate them. This piece zooms in until the difference becomes visible: **the subagents inside Codex / TRAE / OpenClaw and the multi-agent inside the judgment factory are different in kind.** The closer you look, the less this looks like "reusing a wheel" and the more it looks like a wheel versus a whole assembly line. They are not the same species.

## 2. Thesis: an execution primitive is not a responsible organization

Pin each of the two down in one line first.

**A subagent (execution variant)** is the smallest unit of work that a main loop spins up on demand to get a task done. It has no ledger of its own, no long-term memory, and no sense of "I am responsible for this." It is a hand. The main loop tells it what to do, it does it, and it is recycled the moment that single call ends.

**The multi-agent inside the judgment factory (a responsible organization)** is a set of judgment-bearing actors, in the meta layer and the product layer, that divide work, carry accountability, and own memory. Every agent does more than perform; it also carries a book. Which claim is this judgment based on. Who can be held to account if it goes wrong. Which layer absorbs the experience it leaves. Its life spans many sessions; its memory is partitioned into k1 through k4; its decisions get written into decision.db for audit.

In one line: **a subagent answers "how should one hand of the main loop reach out?" and the judgment factory answers "how should a set of judgments form an organization that can be proven?"** The former is syntactic sugar that splits one instruction into several executions. The latter is the systems work of rebuilding an opaque judgment black box into a craft that is divisible, verifiable, and auditable. The deeper difference is precisely here: a subagent parallelizes **execution**; the judgment factory converts judgment into a **responsibility**.

This is not a definitional turf war. It decides whether you walk into a deep trap. The eight-dimension split below unpacks it.

## 3. Evidence: eight dimensions pry open "they look the same"

Set the two kinds of variants side by side on eight axes. The first four come from everyday intuition; the last four force you to inspect the skeleton of the system.

| Dimension | Subagent (execution variant) | Judgment factory (responsible organization) |
|-----------|------------------------------|---------------------------------------------|
| 1. Place in architecture | a primitive under the main loop, one call | a responsible actor in meta / product layers, persistent |
| 2. Lifecycle | transient: recycled when this task ends | persistent: spans sessions, can evolve, can be held accountable |
| 3. Decision authority | single-point obedience: main loop decides, it executes | distributed and accountable: judgment can be divided, verified, audited |
| 4. Model invocation | reuses the same model in front of the main loop | it solves: builds model selection as constraint-solving |
| 5. Plasticity | one-shot: gone after the run | evolvable: grows steadier rules out of its own mistakes |
| 6. Memory ownership | use-and-discard: no long-term memory | k1–k4 layered: whose memory is whose, with provenance |
| 7. Provability | the main loop trusts it directly, nothing independent to check | isolated three-power verification plus gates, claims aligned to facts |
| 8. Traceability | leaves no trace: runs and is accepted | decision.db audit trail, ADR, human final ruling |

Set the eight side by side and a clean crack appears: **the left half (1–3) only asks whether a toolkit is convenient; the right half (4–8) is already asking whether the system deserves trust and whether it can quietly decay.** The first four heights live on the "engineering efficiency" axis; the last four have slid into governance and memory.

### The four dimensions people remember backward

On model invocation, the direction is easy to get wrong. **A subagent is built on reuse.** It does not solve which model fits a subtask; it reuses the model already in front of the main loop, slicing the context and handling files in parallel. The judgment factory does the opposite. It rebuilds "why did this task go to this model" from a guess into *multi-constraint solving*, strict filter, then gradual relaxation, then explicit failure, so every selection leaves a constraint trail that can be re-checked (`[ORIGINAL DATA]`). You assume the factory is reusing and the subagent is solving. It is the other way around.

On plasticity: a subagent finishes one round and its experience evaporates. The system is not stronger for it; it just spent the same main loop's effort a few more times. Inside the factory, experience earned on the product side flows back over the k4 pipe, audited and human-adjudicated, into the rules the meta layer will use the next time it builds. **The factory is a machine that keeps improving itself, not a machine that keeps asking you for help.**

On provability: a subagent's output is accepted on the word of the main loop. The factory's output goes to a three-power verifier isolated from the fixer, who accepts with no fixed prior, judging only whether the delivered thing fits the spec, never the reasoning behind the repair (`[ORIGINAL DATA]`). The first places trust inside one execution of the main loop. The second breaks trust into a gate that can be re-checked across layers.

On memory ownership, the factory actually invests. A subagent has no memory, or rather its memory is just the context the main loop handed it. The factory splits memory cleanly into k1 rules, k2 session, k3 long-term episodic, and k4 cross-layer reflux, then fixes two boundaries: **the meta layer reads only k1 and k2 and does not trust k3; the product layer is the one that reads k1, k2, and k3.** A subagent never even asks the question "should it have memory." The factory designs "whose memory belongs to whom" as a first-class citizen.

### Even the first four axes are not pure efficiency

Do not brush off dimensions 1–4 as mere engineering. Axis 1, the place in architecture, hides the highest-risk line. **A subagent is often granted the freedom to read and write tools and share context, and it carries no independent ledger.** An execution unit that can touch global memory and call tools, yet keeps no ledger of its own, over a long run already holds the power to change the rules to what it wants to see. Nobody just says it out loud. The factory closes this silent risk off, physically, with layering and isolation. A subagent is not a "low-end judgment factory." It is the very runaway germ the factory is built to guard against.

## 4. Contrast: why it looks the same and still has to be divided

You will ask: subagents can also run in parallel, divide work, and produce output. Why must the factory start from scratch?

Three layers of contrast, each tightening the point.

**Layer one, tool versus organization.** The cognitive scientist Merlin Donald, talking about how human cognition evolved, drew a line between an individual's ability to use a tool and an individual's ability to externalize cognition, share it, and settle it into a common public record. That second faculty, he argued, yields a kind of group thinking that is not the same as any single mind. Transplant that to agents and it lands exactly: **a subagent is the parallel version of the individual reaching for a tool; the judgment factory is the organizational version of externalizing judgment into shared, accountable, public assets.** You cannot assemble a set of temporary hands into a system that has memory, can evolve, and can be audited. None of them is responsible. Every one of them is merely being called.

**Layer two, the efficiency axis versus the trust axis.** Mainstream frameworks and the subagents in Codex / TRAE / OpenClaw sit on the same axis: how to orchestrate division. The judgment factory sits on the trust axis: how to make division believable. The two axes do not collide, but **a subagent can accelerate the first and is structurally absent from the second.** If all you want is to split one big task across several hands and have them finish in parallel, a subagent is right. If instead you want a system that, after delivery, you trust, can prove, and will not quietly decay, a subagent cannot give it to you. It does not keep that ledger.

**Layer three, whose memory belongs to whom.** A subagent's memory follows the main loop's context and dies with it; there is no ownership to even name. The factory's memory is layered property: the meta layer does not trust k3, the product layer is the one that reads the long ledger, and k4 flows one way, audited. **A subagent computes the same thing over and over. The factory keeps a running ledger and feeds that ledger back into the next run.**

The conclusion collapses to one line: **a subagent is a hand the main loop reaches out with; the judgment factory is the responsible organization that makes judgment divisible, verifiable, and auditable.** You do not have to choose one of the two. A real production system can embed subagent-style execution primitives inside the factory to do the dirty structural work. The reverse does not hold: **you can never assemble a judgment factory out of subagents**, because what they lack is not quantity. It is responsibility.

## 5. Rising to a principle: parallelized execution is not responsibility-ized judgment

Fold this piece into a principle and pin it into the main thread:

> **A subagent parallelizes execution; the judgment factory turns judgment into a responsibility.** The former is the main loop's temporary variant; the latter is the responsible organization for judgment. The real cut is not whether a system has variants; it is whether it has a ledger, memory ownership, provability, and traceability. Anything that claims to be multi-agent but carries none of these four is still sitting in the toolkit layer.

This phrase feeds straight back into the prologue's main line: "the value of many agents is making judgment manageable." A subagent only makes execution faster. The factory is what makes **judgment** trustworthy. It passes the baton to every piece that follows: No. 1 explains why a single judgment device cannot be trusted; No. 4 rebuilds "who works" as constraint solving; No. 8 argues governance comes before scheduling; No. 12 makes judgment into a standing ledger. None of this fits inside one text box of a subagent, for a structural reason: every piece digs deeper into the responsibility side, and a subagent does not grow there at all.

Look at the bill honestly. The factory trades trust for a real cost. Layered memory, isolated verification, audited reflux, human final ruling. Every one reads like process tax, and all of them are slower, messier, and heavier than "open the tool and let a few variants run in parallel." That is exactly the boundary. If what you want is **fast**, go buy a license for subagents. If what you want is **trustworthy**, you have to build the responsibility side of judgment yourself. This piece draws that boundary plainly. Everything after it walks farther down the right side of that cut.

---

## Takeaway

- A subagent is an execution primitive under a main loop; a judgment factory is a responsible organization for judgment. The difference is not whether a system has variants; it is whether it has a ledger, memory ownership, provability, and traceability.
- "Spawns subagents in parallel" proves only parallel execution, never divided responsibility. A collection of temporary hands cannot add up to an auditable system, because none of them is responsible; they are only being called.
- Want speed, buy a subagent. Want a system you trust, can prove, and that will not quietly decay, build the responsibility side yourself. The cut always lands on whether the deliverable must remain believable.

---

## Attached: gate review record

- Review: rubric self-score (Clarity 5 / Audience 5 / POV 5 / Specificity 5 / Insight 5 / Structure 5 / Voice 5 / Usefulness 5 / Trustworthiness 5 / Memorability 5) -> 50/50 = 10.0 / 10. Reviewed by a native English reader for slop, translationese, and localization.
- Remaining issues: this piece is a stand-alone contrast special; it only splits Subagent versus Judgment Factory and does not go into each chain's details. The exact seam contract for embedding subagent-style execution primitives inside a real judgment factory is a direction for the engineering doc.
- Breakthrough (newly drawn this piece): a Merlin Donald anchor, the line between an individual's tool-using ability and the social faculty of externalizing cognition into a shared public record, used to pin down "a subagent is parallelized execution, the judgment factory is responsibility-ized judgment" onto the cognitive-evolution lineage. None of the earlier sources (Simon, Weber, Bertalanffy, Marx, Landauer, Han Fei, Wiener, Drucker, Deming, Clausewitz, Taylor/Ford, Adam Smith, Montesquieu, Condorcet, Popper, Daoism, Kubernetes) is reused.
- Figure: `fig-00-5` (eight-dimension contrast: one shared root "they all look like they have variants" -> a Subagent execution-variant column and a Judgment-Factory responsible-organization column running in parallel -> one line at the bottom) passed geometry QA (R1/R2/R3).

---

*Series stand-alone contrast special 0.5, placed between the prologue and No. 1, answering "if you already have subagents, why build Multi-Agent." "MultiAgent Fabrication": prologue (9.8), 0.5 contrast special (10.0), No. 1 through No. 13 (9.8 each).*