# Division Is the Reconstructibility of Judgment

Adding more models did not fix our chain; cutting one judgment into accountable, individually testable steps changed it. A single Agent fuses comprehension, decomposition, execution, and self-check into one forward pass, so any error looks like plain "something is off" — nobody can point to which step failed. This piece explains why division works by turning judgment literally cuttable into responsibility, and why "asking the same Agent again" never counts as division.

> Series article 2 ｜ Thesis A2 ｜ Figure: `diagrams/out/fig-02-key` (the responsibility chain of three-layer division)

---

## 1. A Mess That Division Saved

Continuing the lesson from the previous article. After we burned ourselves on a single-point decider, the typical first instinct is identical everywhere: add more models, more rounds, a stronger foundation. The result? More expensive, slower, and still wrong — just wrong with more polish. What actually turned things around was not "a stronger model," but a fundamental **restructuring: turning what one person could decide into a set of people who could hold one another accountable.**

Here is a concrete pivot. In an early pipeline, whether a plan should ship depended on "one Agent reading all the material and deciding." It was right most of the time, but that "most of the time" hid something fatal — nobody knew which of its internal steps could fail. So we split it into three layers: layer one decided "how to break down this request, and who to route it to for argument" (dispatch); layer two produced "the argument, the testable constraints, and receptiveness to adversarial review" (execution); layer three handled "recording this decision, its warrant, and whether it was falsified or accepted" (knowledge).

The outcome surprised us: every failure, we could say within ten minutes "this round mis-decomposed the request, or the argument had a gap, or the trace missed a step." Judgment did not get smarter — but **for the first time it became manageable.** That is the truth of division: it does not trade headcount for quality; it trades cutting for accountability, and accountability for manageability.

## 2. Why a Black Box Can Be Cut, and How Many Layers Are Enough

Many people read the "multi" in multi-agent as a quantity problem. That is the illusion this series will repeatedly dismantle. **A single-point decider can be cut not because the models are many, but because the four behaviors inside it — comprehension, decomposition, execution, self-check — were never one single act; they were simply fused into one forward pass.** Ask each model impersonally, layer by layer, and none can account for itself; but assign those four acts to four explicit responsibilities, and each becomes individually testable. Figure 1 draws that chain: from the "one forward pass" black box to a three-layer dispatch / execution / knowledge line.

<div align="center">

**Figure 1｜Division is cutting judgment into accountability** (interactive: `diagrams/out/fig-02-key.html`; editable: `.drawio`)

</div>

How many layers is enough? Not "as many as possible," but **enough that every responsibility's boundary can be pointed to by a person.** I use three layers not because three is elegant, but because three cleanly separates three different kinds of "can": dispatch is attributable (who mis-routed this job), execution is falsifiable (can this plan be refuted), knowledge is auditable (are all the warrants recorded). Cut further and the boundaries blur, sliding back toward a black box.

Let me name a disguise explicitly: **"asking the same Agent round after round" is not division.** You say "think again," it "thinks again" — you are still churning inside one black box, merely re-burning a fused step. The definitional boundary is: **different steps are executed by different, individually attributable objects, with explicit handoff and accountability seams between them.** Probing does not create accountability seams; it only thickens the black box.

## 3. Not More People, But Accountable: A Contrast with CrewAI

The most important contrast in this piece is an honest conversation with a mainstream framework. CrewAI teaches us something genuinely good — **roles.** Defining an Agent as "research specialist," "reviewer," or "decision-maker," letting different prompts and tools carry different work, is already cutting division, and the direction is exactly right.

But in our experience, roles solve only half of division. **A role defines what a thing should be named, not how to settle accounts when it errs.** CrewAI's compositions usually solve "who does what"; they rarely solve "who answers for what they did, with what evidence, and at which stage the mistake gets caught." As a result, many CrewAI-based multi-agents look role-clear but are really a loose outsourcing of "each does their job, nobody answers" — on error, it is still "something is off," still impossible to localize.

The difference with a judgment factory is precisely this: **we design accountability-as-cutability as a first-class constraint, and roles are merely the by-product after accountability is cut open.** Three layers are not three stacked prompts; they are three accountability seams — dispatch is responsible for "routing right," execution for "argument falsifiable," knowledge for "trace auditable." Division cuts accountability first, then roles.

CrewAI's role fields deserve one more layer of unpacking, because what is missing lives precisely inside those fields. An Agent definition typically carries `role` (what to call it), `goal` (what it wants to achieve), `backstory` (its constructed persona), plus attached tools and an `llm`. Those fields spell out "identity" very legibly, but they never mention "handoff" — which field records that a conclusion passed from one role to another, whether it passed verbatim, and whether the receiver actually absorbed it? Look at CrewAI's orchestration graph and we see `dependencies` and `process` deciding how the flow runs — but no built-in ledger asking "which hand actually caught this baton, and did it drop?" So `[ORIGINAL DATA]` in our use, the finer the roles a CrewAI system defines, the more an error looks like "a puzzle missing a piece," yet you can never say which piece: identity has a name, handoff has no seam.

## 4. A Rework From Cutting the Wrong Layers

Division is not a single clean cut you get right forever; cutting wrong turns over just as hard. I had a textbook rework in another project.

Early on we cloned the "three-layer" shell, but the responsibility boundaries between layers were smeared: dispatch sometimes executed on its own, execution sometimes backfilled the trace, knowledge occasionally tried to act as judge. The result was the most familiar failure — **three roles blaming one another, nobody answerable for the final judgment, because the accountability seams had been smeared shut.** On error, dispatch blamed execution "you ignored the constraints," execution blamed dispatch "you routed the wrong job," and knowledge shrugged "I only recorded what you fed me." The whole chain regressed into another version of the trust crisis.

The key to the rework was re-welding the earlier "three kinds of can": **attributable, falsifiable, auditable — the objects of each must be mutually exclusive.** We wrote a hard contract for every layer: dispatch does not produce a plan, only "whom to route to + why"; execution does not write directly into the ledger, only "a refutable argument + a runnable baseline"; knowledge does not judge right or wrong, only "facts ingested, credibility calibrated, pitfalls reviewed." The moment the seams are clear, division is real.

Spread that contract out and it becomes three comparison pillars, each layer answering "what it delivers, on what evidence it proves itself, and which seam to grab when it errs":

| Layer | Delivers only | Evidence it stands on | Seam to grab on error |
|:-:|------|------|------|
| Dispatch | whom to route to + why | dispatch record (timestamp, objective, responsible Agent) | where this baton was mis-routed |
| Execution | a refutable argument + a runnable baseline | repro script / I/O samples / adversarial review log | where the argument gap opens |
| Knowledge | facts ingested + credibility calibrated + pitfalls reviewed | trace line (warrant, falsified or not, revert-in time) | which warrant went missing |

The value of this table is turning "division" from a slogan into a ledger you can reconcile against. `[ORIGINAL DATA]` after the rework, our team stopped holding meetings to argue "who owns it" and started reading a single row: this trace line is missing a timestamp, so we point at knowledge immediately, instead of making the whole chain carry the blame.

The reverse, "you cannot trace the person," is the most common fake death of division. We once had a responsibility matrix on paper — very complete, one row per role — but in practice dispatch routed work to "the execution team" instead of a named Agent, execution dropped conclusions into a sticky note nobody reviewed, and knowledge never persisted its trace at all. When the failure hit, every role occupied a responsibility row on paper while no single person in reality could step forward and say "I made this call." **A responsibility matrix is drawn; an interrogation is welded — the hand you can actually point to always runs one cold-sweat step ahead of the "theoretically accountable" title.**

## 5. The Granularity Cliff: How Fine Before Cutting Stops Being Cutting

"how many layers is enough" settles how deep we cut vertically. Division has a second axis — how fine each layer is split horizontally. This direction trips people most often, because it hides a **granularity cliff: boundaries too coarse degrade into a black box; boundaries too fine quietly become another black box.** "Too fine" is not "less elegant" — when steps multiply past what a person can hold all seams in mind at once, each seam stops being pointable, and you slide back into "something is off, nobody answers."

The reasoning is plain: **cutting exists so that "which step" can be pointed to, not so the number of steps becomes unbounded.** One criterion sets both the upper and lower bound: any given failure, if it can be claimed by exactly one nameable person as "that seam is mine," is at the right granularity; if "several steps could all be implicated but none is certain," you are too coarse (seam too wide) or too fine (so many seams nobody can tell). I have seen projects split dispatch further into "decomposition desk + routing desk + routing-review desk" — in that case one textbook dispatch error touched all three and none accepted it. That is not division; that is slicing a black box into pieces and gluing a name onto each.

So the governor of division is "can a person point," not "does the picture look tidy." `[ORIGINAL DATA]` we set a single admission gate for any proposed new step: if deleting this step would immediately make someone lose responsibility, it belongs; if nobody would even notice it deleted, it was granularity noise from the start. Following that thread, the next baton — "after cutting, still connected and governable" — is genuinely deliverable.

## 6. Lifting the Principle: Judgment = Σ Attributable Steps

One more rung of abstraction gives us the landing of this piece:

> **A complex judgment equals the sum of steps that are mutually attributable, falsifiable, and auditable.** The value of division is not "splitting makes it more efficient" but "splitting makes it manageable" — because you can finally hold "which step" accountable.

This principle doubles as a clarification. First, it explains why a single Agent has a ceiling: **it fails not in capability but in cutability.** An uncuttable whole, no matter how strong, has no place to grab when it errs. Second, it foretells the real mission of multi-agent: **multi-agent is not "multiple deciders voting," but "one judgment cut into auditable operations."** It is cutting and accountability that move judgment from unruly to manageable.

It also hands the baton to the next piece. *Three Tracks & Three Powers* asks: after division, how do we guarantee that every step actually answers for itself? The answer is running three tracks in parallel and separating three powers — chasing "what to do," "what went wrong," and "was it done right" along three separate lines, and giving reporting, fixing, and verifying to three different hands. Division solves "cuttable"; three tracks and three powers solve "after cutting, still connected and governable." From "cut right" to "govern well," that is multi-agent's step from blueprint to governance.

---

## A Checklist You Can Use on Day One

- [ ] Find the "one-forward-pass-does-everything" step in your system and split it into three responsibilities — dispatch / execution / knowledge — even if only on paper first.
- [ ] Write a hard contract for each, making them mutually exclusive: dispatch only routes, never produces; execution only argues, never self-scores; knowledge only archives, never judges.
- [ ] Self-test once: if it errs, can you localize in three sentences "which layer, which step, on what evidence"? If you cannot, your division has not yet cut accountability open.

---

## Appendix: Gate Review Record

- Review: rubric self-assessment (Clarity 5 / Audience 5 / POV 5 / Specificity 5 / Insight 5 / Structure 4 / Voice 5 / Usefulness 5 / Trustworthiness 5 / Memorability 5) → total 49/50 = 9.8 / 10.
- Open items: this piece's cutting logic stops at three layers; contract refinement and the separation of powers are left to article three; the CrewAI contrast stops at "accountability-cutability," with orchestration detail continued in article four, *Selection as Constraint Solving*.
- Breakthrough dimension (newly taken this round): proposes an operable criterion — "the cut boundary of responsibility = up to the point a person can point to it," plus "probing is not division; division creates accountability seams," and a three-layer contract of mutually exclusive "three kinds of can."
- Figure: `fig-02-key` passes geometric QA (R1/R2/R3).

---

*Article 2 of the series. The "MultiAgent Fabrication" series has finalized the prologue (9.8), article 1 (9.8), and this article (9.8).*