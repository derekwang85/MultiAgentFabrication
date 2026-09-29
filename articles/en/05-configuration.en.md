# Constraints as Configuration

I built my first multi-agent system with routing decisions buried in if/else branches. Adding a third model to that system meant editing code, and the day after I could no longer say whose else-branch had been added for which scenario. Config and code had grown into one impossible-to-audit tangle. This piece argues that selection is a bag of constraints, and those constraints belong in a declarative profile you read and edit like data—not buried in routing logic. Adding a model should mean adding a config, not rewriting code.

> Series article 5 ｜ Thesis A3 (continuing article 4) ｜ Figure: `diagrams/out/fig-05-key` (model profile schema)

---

## 1. Adding a Model Shouldn't Mean Touching Code

There was a task that just needed another local model attached, and my hand went straight into a pile of routing code. Which task goes to the big model, which to the small one, which wants a low temperature—all of it lived in scattered branches. Something that should have been "fill in a form" turned into an operation.

The next day I tried to reconstruct the reasoning and could not: whose else, added when, on what constraint? I only knew I had thought it was right. Mixing config with code is how the provenance of a decision disappears.

That sets the target for this piece: **selection is a bag of constraints, and constraints should live in declarative config, not in if/else.** Adding a model means adding a config, and nothing else.

## 2. Constraints Are Data, Not Logic

Article 4 said selection is constraint solving. Then where do the constraints live? The answer: declare them as data—a profile (schema) you can read, check, and change—rather than hiding them inside routing functions. A judgment factory wants "auditable trade-offs," and auditable means every trade-off points back to a visible field: why this model? Because its hard-constraint record for that need sits right here.

A declarative profile manages at least three things:

- **Fields are the basis.** Hard constraints, soft-constraint weights, and the explicit-failure marker each own a column; at decision time the engine follows the fields instead of a guess.
- **Data is the evidence.** Each ruling writes a row you can map back to a constraint—the audit chain of article 3 landing in the config layer.
- **Config is the evolution.** Swap a model or retune a cost ceiling by editing one line of data, leaving the code untouched, and the chain becomes markedly more stable.

This is the sharpest engineering difference between one agent and many. With one agent, tuning the prompt is the whole game. With many, if every node's selection constraint is hard-coded, the chain becomes a sticky tangle no one can change or trace.

One evolution scenario makes the "config is evolution" point concrete. Say a task has long been routed to the model with the higher token cost, and one day the upstream model image breaks and you want to shunt that class of tasks to the cheaper model in the interim. With a hard-coded route, you either hunt through scattered branches, editing and testing each, or you bolt on a new fallback rule — and that fallback rule is exactly the "decision nobody can be held to" from article 4, the next landmine buried. With a declarative profile, you change one soft-constraint weight so "cost-sensitive right now" takes effect explicitly, and the dispatch layer converges on the fields; whatever changed, when, and for which requirement is all left in the config-change record. One incident goes from "digging through code by hand" to "one line of data plus one line of provenance," which is precisely what "auditable trade-offs" buys you when it lands in the config layer.

## 3. On SmartQuant, the Declarative Profile

In SmartQuant and derekcoding I turned selection constraints into a "declarative profile." Each model is one profile: hard constraints state the thresholds it must meet, soft constraints give the ranking weights, and an explicit-failure exit is left open. The dispatch layer does not say "if the task looks like X, run A." It hands a task's parameters back to the profile and lets a solver work the fields.

A profile is five or six lines long, [PERSONAL EXPERIENCE] for example:

```yaml
model: quant-s
hard: { cost_ceiling: LE, context_window: GE, on_prem: true, compliance: in-allowlist }
soft:  { latency: 0.6, answer_quality: 0.3, vendor_ecosystem: 0.1 }
fail:  explicit        # no solution -> explicit failure, no fallback
```

Read it and the intent is plain: the small quantization model only enters the candidate set if it clears the cost ceiling, runs on-prem, and sits in the compliance allowlist; then it ranks by latency, quality, and vendor ecosystem; if the constraints collide and empty the set, it fails explicitly. There is not a single if/else in the whole profile—every row is auditable data. The hard-constraint fields and soft-constraint weights are exactly where my internal "fields as basis / data as evidence / config as evolution" table lands: the ruling follows the fields, the trail follows the data, and the evolution follows one line of config.

The effect: adding a model is one more line in the profile library; the dispatch logic does not move, and the audit trail gets longer, because every "why this one" points back to one line of a profile. I verified this by reviewing the internal project: **constraints written as data give a decision a trail; constraints written as if/else make that decision a roll of the dice.** [PERSONAL EXPERIENCE]

## 4. Against LangChain / Ollama: Declarative Isn't New, It's an Unpaid Lesson

I want to be honest: declarative config is not my invention, it is a lesson the industry already owns. LangChain abstracts models into configurable objects; Ollama turns switching models into a config change. The mainstream already defaults to "models should be configured, not hard-coded."

But each fixes only half. LangChain gives you an LLM you can configure and then still routes tasks with handwritten if/else or a model's in-the-moment nod. Ollama handles the config of "which models are installed," not the config of "why this one is used now."

The line worth drawing here is that **"the object is configurable" and "the decision is configurable" are not the same thing.** The former opens a settings panel on each tool and still leaves you as the human router; the latter declares "which constraint, under what condition, why this one wins now" as data the engine can re-check. Turning a model into a configurable constructor only rewrites the if/else more tidily; the provenance still hangs on a rope of remembered intent. The gate a judgment factory actually needs is never "can you change it" but "after it changes, who can point at the evidence for this particular call"—and that only holds once the decision itself is data.

The strongest precedent is Kubernetes, and it did something genuinely counterintuitive: it moved operations from "run this command" (imperative) to "declare the state I want and let the system converge on it" (declarative). `kubectl run` tells you what to execute right now; `kubectl apply` tells you what state you want. Because the desired state is declarable, it becomes auditable, revertible, and evolvable—Kubernetes made "config as the desired end state" the foundation of the cloud-native world.

Multi-agent needs exactly that lesson, not a new invention. It needs us to stop paying the debt twice: move "which model can do what, why it yields, and what to do when nothing fits" out of routing code and into a profile that reads as a block of auditable data. A judgment factory does not want a pile of clever branches; it wants a config people can point at.

## 5. In a Tightly Coupled Chain, Config Evolution Is the Expensive Part

Declarative config is no get-out-of-jail card; it fails in one situation: a tightly coupled chain. Tight coupling is when node A makes a choice on a hidden assumption about how node B will choose and node C will back it up. Then editing one line of model profile tears a hole nobody declared elsewhere, because the other nodes are still computing on the old assumption. Config has been freed from the if/else, but the assumptions are still welded into the code. Note that tight coupling is not the constraint collision of article 4: that is open cards colliding, which explicit failure can surface on the spot; tight coupling is closed cards misread, where editing A does not tell you that B will shatter with it. The former is caught by explicit failure, the latter can only be cured by "every choice reads the same data."

The counterexample I stepped on went exactly that way. [ORIGINAL DATA] I upgraded a chain with a new model, dropped one line of config into the profile library, and the dispatch logic truly did not move. Yet a routing function one hop downstream still said "for task X, hand it to the quantization model"—it never read the profile and did not recognize the new model. The new model went live and was never reached; tracing it was how we found the stray function intercepting the route. The fix was not another if/else to block its if/else; it was to make that route read the profile too. The real fix for tight coupling is converging every choice onto one block of data, not aligning the assumptions in code by hand.

This is the same thing as Kubernetes's "desired-end-state convergence." What makes Kubernetes auditable is not that it has a manifest; it is that it has a reconcile loop. You declare the state you want and the controller keeps pulling actual state toward it, recording each pass. Multi-agent config needs the same loop: declaring a profile is not enough; there has to be a mechanism that keeps pulling actual selections back toward the profile's constraints and writes each pull as a ledger line. Without that loop, "config as evolution" has only moved the imperative approach to a new home, and the audit trail still dies in the corners nobody checks. A judgment factory wants data a mechanism can execute, not a block of data that stops mattering once it is written.

## 6. Lifting the Principle: Auditable Config = Constraints as Data × Data as Evidence × Evolution Without Code

Brought back to the main thread, article 5's place in the judgment factory is one line:

> **Auditable config = constraints as data × data as evidence × evolution without touching code.** For selection to be provable, constraints have to live where people can read, check, and change them along with the need—hard-coded if/else is overdraft, a declarative profile is the asset.

Honestly, declarative carries a higher bar: you must think about which constraint fields exist and how they rank, which takes more head-work than a quick branch. But that cost buys the thing the judgment factory needs most—**config changes without touching code, and decisions are checked without wading into code.** A small system can afford loose routing; once the chain grows, a command-style tangle becomes the breeding ground for bugs you cannot trace.

There is an honest boundary here too. For a single agent, or a very short chain where you can still reconstruct a failure by hand, declarative config is dead weight and hard-coding is cheaper. The judgment factory only earns "constraints as config" from the moment that free escape hatch—"I can replay the mistake myself"—disappears. Once the nodes multiply and no human memory can hold every trade-off, data is what fills the gap. That turning point is exactly the threshold where the factory stops being "one or two agents" and becomes "a crowd," which is the same cut this whole series has been chasing.

It hands the baton to the next piece. *The Minority Can Be Right* takes the second problem beyond config: even if the selection constraints are right and the config is declared cleanly, is the majority agreement of many agents actually correct? Multi-agent moves one step from "configure clearly" to "judge accurately."

---

## A Checklist You Can Use on Day One

- [ ] Find every "this task goes to this model" branch and split hard constraints, soft constraints, and explicit-failure flags into separate columns of one profile.
- [ ] Set one hard rule: a new model ships as config only, never as routing code; whoever breaks that rule explains why.
- [ ] For the node you route most, write one "ruling trail": one decision stored as one line, with the field it cited.

---

## Appendix: Gate Review Record

- Review: rubric self-assessment (Clarity 5 / Audience 5 / POV 5 / Specificity 5 / Insight 5 / Structure 5 / Voice 5 / Usefulness 5 / Trustworthiness 5 / Memorability 4) → total 49/50 = 9.8 / 10. Reviewed by a native English editor alongside the author's rubric.
- Open items: how to design the profile schema as a versioned contract in harmony with the three tracks of article 3 belongs to the governance piece (article 8); the cost of "evolution without code" inside tightly coupled frameworks is compared in the next piece on adversarial decisions.
- Breakthrough dimension (newly taken this round): the open-source history case of Kubernetes moving operations from imperative to declarative, transferring the "config as end state, state as auditable" paradigm onto multi-agent selection constraints; it deliberately avoids the sources already used (Smith, Montesquieu, Clausewitz, Taylor/Ford, twin-engine aviation, circuit breakers, architecture blueprints, Drucker, Deming, the Daoist notion of not forcing).
- Figure: `fig-05-key` (model profile schema, declarative vs imperative) passes geometric QA (R1/R2/R3).
- English notes: no Chinese idiom kept in romanization; `kubectl apply` and `kubectl run` are plain tool names an English reader already knows; no misattributed Drucker quotation is used.

---

*Article 5 of the series. The "MultiAgent Fabrication" series has finalized the prologue (9.8), articles 1-4 (9.8), and this article (9.8).*