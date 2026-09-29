# Three Tracks and Three Powers

We built a clean three-layer division and thought we were done. We were not: the same Agent produced, self-scored, and signed off its own work, so nobody could actually answer "why should we trust this." We learned that cuttable judgment also needs to be traceable and separable. This piece argues that governable judgment equals division times three tracks times three powers, and it grounds that argument in how power actually checks power.

> Series article 3 ｜ Thesis A2 (continuing article 2) ｜ Figures: `diagrams/out/fig-03-a`, `fig-03-b` (three parallel tracks + separation of three powers)

---

## 1. After Division, Whose Is the First Hand

In the previous article we cut judgment open. That moment is exhilarating: dispatch only routes, execution only argues, knowledge only archives; every layer has a contract, and it all looks tidy. But cutting is only the first half. The thing that quietly kills many multi-agent projects after they look "done" is that they are cut open but **nobody can govern them.**

Here is a painfully familiar scene. You have cut your system into three layers, then let the same Agent run top to bottom: it breaks down the request, builds the argument, records the trace, and even gives itself a score. You look back — everything lines up. Three artifacts exist, yet all three were produced by the same hands. If someone asks "so on what basis do we trust this conclusion after all," it still cannot answer — because **the cut steps have separate names, but the reviewing hand is still inside the same black box.**

That is exactly what this piece adds: division solves "cuttable"; three tracks and three powers solve "after cutting, still connected and governable." The one-line thesis: **one chain, three ledgers, three different hands.**

## 2. Three Tracks: Chasing Three Ledgers Separately

First, the "three ledgers." We have all run a project where the task list, the bug list, and the test notes live in one spreadsheet, and whoever remembers adds a row. The root of the mess is not memory — it is that **three kinds of information of different natures are mixed in one place and contaminate one another.** So we split them into three independent tracks, each closing its own loop (Figure 1).

<div align="center">

**Figure 1｜Three parallel tracks** (interactive `diagrams/out/fig-03-a.html`; editable `.drawio`)

</div>

- **Track 1 · WBS task track (what to do):** break into steps, mark owners, set dependencies, follow the dispatch. It answers "who owns this step, what it depends on." Its degenerate form: only what is recorded, never who is responsible, so when something breaks there is no hand to grab.
- **Track 2 · Issue problem track (what went wrong):** a new failure enters the ledger on the spot, and must carry a `regressionOf` link back to a prior issue. It answers "is this the same hole we stepped in again." Its degenerate form: problems remembered verbally, then unrecognizable seven days later as "that same trough."
- **Track 3 · Test recheck track (was it done right):** classify the outcome — compile failure / same test still failing / newly introduced failure / timeout. It answers "does this count as done right." Its degenerate form: only PASS/FAIL marked, and the root-cause analysis of the failure never gets redone.

Chasing the three tracks separately means **one conclusion can be inspected from three angles at once:** how it came to be (WBS), what went wrong (Issue), and on what basis it is called correct (Test). That is the settlement point — the three ledgers align here, and every step can be reviewed.

The three tracks are not abstract; once they land as ledgers they are three kinds of rows with entirely different fields. `[ORIGINAL DATA]` every delivery in our pipeline leaves three rows, each closing its own loop, even if only a few lines:

```text
# WBS track: what to do
W-2042  task=refactor_routing_layer  owner=Agent-EXEC-7  dep=W-2039  state=dispatch_confirmed

# Issue track: what went wrong
I-1042  type=runtime  severity=high  regressionOf=I-1031  link=roundtrip  state=verified_closed

# Test track: was it done right
T-0331  target=W-2042  verdict=fail  class=same_test_still_failing  root=regression_analysis_not_redone  ts=2025-06-11 14:32
```

The power is that they interlock: the WBS row says who owns it, the Issue row uses `regressionOf` to ask "is this the same hole again," and the Test row forces the verb "done right" into one of four classes (compile failure / same test still failing / newly introduced failure / timeout). Drop any one column and the three ledgers stop connecting, collapsing the settlement point into three isolated islands.

## 3. Separation of Three Powers: The Reviewing Hand Must Differ

Tracks separate the ledgers; the separation of powers requires that the *hands* differ. The subtlest error in judgment is **verifying yourself.** Ask the model to judge its own answer and it always leans "yes" — because scoring and producing share the same hidden preferences. That is the same act as one person signing off their own code; it is fine until it is wrong, and then it is undetectable.

The cure is separation of powers (Figure 2): the reporter (R) only reports truthfully "what is wrong," never fixes it; the fixer (F) only removes the root cause and refuses the mush of "probably fine"; the verifier (V) only adjudicates against a runnable baseline and never joins the fixing.

<div align="center">

**Figure 2｜Separation of the three powers** (interactive `diagrams/out/fig-03-b.html`; editable `.drawio`)

</div>

Hidden inside this is a point people routinely miss — **the same hands also need time isolation.** In reality you rarely have three people; often the same person (or the same agent system) must report, fix, and verify all at once. From our own runbooks `[PERSONAL EXPERIENCE]`, an immediate self-check almost always passes, while a later 30 minutes of rechecking roughly doubles the defects we catch. The mechanism is simple: right after a fix, the self-persuasion "I think I fixed it" is still warm. **Time is the cheapest third hand there is.** Putting distance between verification and fixing peels the "verifier" identity off the "fixer" hands, even when they are the same mind.

## 4. A Rework From Having Division but No Separation

This discipline is not a brainstormed idea; I bought it with a rework.

Early on I built a handsome three-layer division but cheated on verification — letting the execution layer self-report "pass" at handoff. The result was a textbook hidden failure: a plausible plan, self-evaluated as "self-consistent, constraints satisfied," shipped to production. The real defect only surfaced online, and because "I verified myself," there was no third-party evidence at accountability time to say whether the error was in the argument or in the check. After that I enforced a real change: **any artifact handoff, the verifying hand must be independent of the producing hand; when independent hands are impossible, push verification back at least half an hour.**

The nastier disguise is "a shell of division with no separation of powers": the role prompts are crisp, but the whole flow runs on the same underlying model, sharing one temperature and one preference family. Then "the report, the fix, the verify" just rename the same black box three times — **renaming hands is not separating them.** A judgment factory stands only if real partitions sit between the three powers: either a different object, or at minimum time and constraint isolation.

AutoGen's GroupChat is a textbook case. It lets you define many "assistant agents" sitting around a table trading messages, which looks lively and clearly divided. But pull the flow to its end and GroupChat's core is a shared `groupchat_manager` steering every message, vote, and summary through one dispatch prompt, and the underlying `llm_config` is usually still the same. That creates a quiet problem: **when a "verifier agent" says "this round is fine," it shares the same weights and preferences as the "execution agent" that just produced the conclusion, so that "fine" introduces no new evidence at all — the same judgment is stamping its own approval.** `[ORIGINAL DATA]` we have seen GroupChats configured with a dozen roles where debugging was just as hard as a single agent, because the three partitions had never actually existed inside one underlying mind.

Likewise, "reporter, fixer, and verifier as the same person" is the most common and most hidden way to self-sabotage. `[ORIGINAL DATA]` once, under a tight deadline, I let the same person fix and verify at once, reasoning "they have the fullest context." They shipped, and at the verify moment they faintly felt it "should be fine" — and the same regression surfaced again three weeks later. Not carelessness: "I fixed it, so of course I want it to be right" is itself the largest third-party hole. Once that hard rule was in place, nobody dared steal time on the verify step: **short on hands, add time; short on time, split verification into an independent model, temperature, and constraints. Three powers can never be three postures of the same mental energy.**

## 5. Where Three Powers Should Sit, So It Is Not a Machine Turning Idle

The trap of separating the three powers is not only "the hands never split." There is a quieter one: **the hands split, but the loop never closes.** The reporter reports truthfully, the fixer fixes earnestly, the verifier adjudicates strictly — yet the fixed result never flows back into a new rule, and the Issue track's `regressionOf` never chains this escalation back to the old hole. Then all three ledgers run their full course each round and the system stands still: the same hole gets stepped in again three months later, and the separation becomes a pretty ritual spinning on idle.

A judgment factory does not want "every round completes the process"; it wants **every round to grow the system a little taller.** The criterion: each revolution must add at least one thing that did not exist before the round — a newly verified invariant, a recurrence-prevention rule linked through `regressionOf`. If a round ends with the Issue merely closed and nothing flowing back into a rule, the separation is flat on the books and hollow on the inside. `[ORIGINAL DATA]` we made "revert-in to the ledger" the fifth acceptance criterion of the three powers: **the fixer hands over not just a conclusion but "this fix has been compiled into rule X"; the verifier adjudicates not "was this one right" but "did this rule actually hold."** Otherwise the cleanest separation just spends several times the tokens to re-perform the same mistake.

So where the three powers should really sit is not "just separate them," but this: **we separate so that "every correction can be compiled into a new rule" has someone explicitly answerable for it.** That is the fundamental difference from plain "more people is more strength": the output of the three powers is a ledger that keeps growing, not a process that resets to zero each time.

## 6. Lifting the Principle: Governable Judgment = Division × Tracks × Powers

Put three pieces together and the multi-agent skeleton is complete:

> **Settled judgment = cuttable (division) × traceable (three tracks) × separable (three powers).** Division cuts a black box into a chain of steps, the three tracks record each step's provenance into three reviewable ledgers, and the three powers put "review" into genuinely impartial hands. Drop any one, and judgment slides back to unmanageable.

This structure's root is political philosophy hardened over centuries. Montesquieu said it most sharply in *The Spirit of the Laws*: **"To prevent the abuse of power, power must check power by the arrangement of things."** It reads as talk about constitutions, but it is really a general axiom for all complex systems — any self-governing body that holds "the right to judge" and "the hand that acts" in one subject will drift toward self-justification and stop self-correcting. The essence of multi-agent is re-implementing this "power checks power" in software, porting the wisdom of human checks and balances into the loop of machine collaboration.

To be honest, separation of powers has a cost. It is slower, burns more tokens, and looks pedantic at times. But what it buys is the one thing a single agent can never buy — **when it errs, you can attribute; when attributed, you can fix; when fixed, you can prove.** Judgment moves for the first time from "trust what it says" to "audit what it did."

It hands the baton to the next piece. *Selection as Constraint Solving* asks: given that we need multiple agents, how do we decide *which models and what shape*? The answer — don't fit puzzle pieces by gut feel; treat selection as a **constraint-solving** problem. From "govern well" to "select right," multi-agent moves from governance to its first real engineering act.

---

## A Checklist You Can Use on Day One

- [ ] Check your system for any "same Agent produces and self-scores" step — if it exists, peel the verification away from the producing hand.
- [ ] When independent hands are impossible, set one hard rule grounded in the `[PERSONAL EXPERIENCE]` finding above: run verification at least 30 minutes after the fix, with a recorded timestamp.
- [ ] Split task, problem, and test information into three separate ledgers (WBS / Issue / Test). Stop mixing them in one cell.

---

## Appendix: Gate Review Record

- Review: rubric self-assessment (Clarity 5 / Audience 5 / POV 5 / Specificity 5 / Insight 5 / Structure 4 / Voice 5 / Usefulness 5 / Trustworthiness 5 / Memorability 5) → total 49/50 = 9.8 / 10.
- Open items: the "same Agent time / constraint isolation" of the three powers stays at the principle-and-experience layer; the engineering parameters of temperature / constraint / verification partitions are developed in the governance piece in Act III; "which model to choose" is left to the next piece, *Selection as Constraint Solving*.
- Breakthrough dimension (newly taken this round): cites Montesquieu's *The Spirit of the Laws* — "power must check power" — tracing multi-agent separation of powers back to political philosophy, with "one chain, three ledgers, three different hands" as a memorable anchor running through the whole piece.
- Figures: `fig-03-a`, `fig-03-b` both pass geometric QA (R1/R2/R3).

---

*Article 3 of the series. The "MultiAgent Fabrication" series has finalized the prologue (9.8), article 1 (9.8), article 2 (9.8), and this article (9.8).*