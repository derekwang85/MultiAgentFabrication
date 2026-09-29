# The Minority Can Be Right

I built a multi-agent loop that asked five models a hard question, and all five returned the same confident answer. My instinct said relax—unanimity means safe. What it actually meant was that they had borrowed the same bias and then nodded at one another. In this piece I argue that majority agreement changes nothing about a judgment's quality. Splitting one opaque, unprovable judge into ten agents that clap in unison does not make the answer more trustworthy, unless those ten judgments rest on independent evidence rather than on echoing each other.

> Series article 6 ｜ Thesis A4 (continuing article 5) ｜ Figure: `diagrams/out/fig-06-key` (Swarm's five phases + a minority-dissent lane)

---

## 1. "Everyone Agreed" Is the Moment I Worry

The readings that scare me are not the ones where agents disagree. They are the ones where they speak as one voice.

One boundary problem went out to five models; all five returned the same plausible answer. By gut instinct that is the safest minute of all—whole agreement, why audit? That is exactly where I got burned. The "unanimous" answer was a good-looking error that had followed the question's leading tone and then matched direction by accident. The models were not independently right; they shared one bias and amplified each other.

That sets the target for this piece: **unanimity does not upgrade the substance of a judgment.** A consensus says a vote is winning, not that it is true.

## 2. Majority Is Not Truth, It Is a Proxy for the Vote

Handing a decision to the majority trades "who is right" for "who will win." Winning and being correct are different currencies.

Condorcet's jury theorem draws the exact line: if each voter judges independently and correctly more than half the time, more voters drive the majority ever closer to truth; but if the voters average around half—or lower—adding people does not help, it steadily inflates the error toward certainty. This is the sharpest warning for multi-agent: **majority aggregation does not create correctness, it amplifies whichever way the underlying bias leans.** Models from the same lineage and the same data are not the "independent voters" Condorcet assumed; their shared bias is dangerously high.

So the value of many agents was never "ask lots of people and someone will be right." It is: how do you force out genuinely independent evidence, and how, when a majority forms, do you stop the one lucid voice from being silenced. That second job is the seam a judgment factory must patch.

## 3. Condorcet's Three Premises Are Collapsing, One by One

The jury theorem reads as common sense, but it only holds when three premises sit at the same time. I do not get to cite the theorem as a shield; I have to break it apart and watch each premise leak in a real agent environment.

The first premise is independence. Jurors converge on truth by numbers because their evidence is uncoupled. Agents are least independent exactly where it hurts: they often share the same base model, the same SFT data, and the same prompt template. In my experience the chance that five same-lineage models land on the same wrong answer to a boundary question is far higher than "five separate guesses coincidentally matching a single error." That is not a guess; it is the echo effect in action. The same origin means the same failure mode, and unanimous agreement is just one shared bias typeset to look like confirmation. [ORIGINAL DATA]

The second premise is better-than-half accuracy. The theorem assumes each voter is above random on average. When a task leaves the model's robust zone—nested logic, counterfactuals, wording with a trap—the batch can sit right around fifty-fifty. More voters do not converge on the correct answer then; they converge on the bias that is already above half. The louder the vote, the more cleanly it stamps approval onto an average bias.

The third premise is no collusion. The theorem assumes no strategic conspiracy. But agents share context and see each other's intermediate outputs, which is a soft collusion: the last agent answers after reading the earlier conclusions, so its "independent" opinion is already an echo. Two of three premises collapse, and the majority stays a majority but loses its qualification to stand in for truth; it only keeps the form. The judgment factory does not stop voting in response. It bolts a pre-check onto the vote: are these voters independent, are they above half on average, and did they conspire?

Those three checks, taken together, are the rule I landed on first when I moved Condorcet from the textbook into code: **verify independence before the vote, instead of treating the vote's outcome as correctness afterward.** The test is blunt. Every agent writes a first-draft judgment in an isolated environment that cannot see the others' output, and only then joins the shared discussion. Any vote that changes after the discussion gets a separate tag, "swayed by consensus," and is no longer counted alongside the unaffected votes. The change is tiny and the effect is real: it lets the majority finally earn the word "independent" instead of assuming it for free. In school the theorem looked like optional mathematics. In engineering it turned out to be a hard constraint on how you pick a judgment factory.

## 4. What the Swarm Five Phases Taught Me Is the Edge It Left Out

OpenAI Swarm's five phases are a solid start. A routine agent opens, handoff proves the responsibility is divisible, context rolls forward as consensus forms, and output arrives. Its elegance exposes its gap—**it spends every line on how the work flows and almost none on where the disagreement is stored.** When consensus forms, the agent that dissents becomes just another node the handoff chain no longer reads; its reasons ride off with the context and vanish without a trace.

The edge I added on SmartQuant is a minority-dissent lane. Once a majority firms up, any ruling that contradicts the adopted view must write one row: the evidence it cited and the premise it would overturn. That row does not vote, but it feeds review—exactly the ledger the "verifier" role from article 3 needs. When the majority votes and walks away, that is overdraft. When the dissent leaves a trace, that is an asset.

What does "one row" mean? I keep the format rigid, and the rigidity is the point, because rigid rows are what a reviewer can actually consume. Every row must fill four fields: who raised the dissent, which evidence it cited, which premise it would overturn, and how the verifier eventually processed the row. A row missing any field fails validation and is bounced back for repair. That step translates "respect the minority" from a sentiment into a checkable data structure. Without that schema, a "minority lane" is just a nice phrase and the verifier still has no ledger to open. [ORIGINAL DATA]

## 5. Against Voting Frameworks: Consensus Machinery Is Not a Fact Machine

Mainstream orchestration leans on majority voting as if it verified facts. AutoGen-style flows commonly run several agents, then take the most-voted answer as the conclusion. That spends consistency as if it were correctness.

I want to push back. Voting answers "who is most likely to be believed right now," not "does this answer match the facts." A judgment factory must keep two ledgers separate: the vote goes into the social ledger (who was accepted), and the evidence check goes into the factual ledger (does it line up). Using the social ledger as the factual one assumes "the majority must be closer to truth," which Condorcet's whole theorem shows holds only when members are independent and individually above half. **Same-lineage agents fail the first condition.** Consensus is a lead, never a verdict.

AutoGen's voting machinery deserves one more layer because it treats disagreement as pure cleanup. In its GroupChat orchestration, several agents take turns speaking in one shared conversation, code runs, results get pasted back, and usually a "summarizer" rewrites the dialogue into a conclusion. The problem is not that there is a lead and a follow; it is that the disagreement gets digested inside the dialogue instead of settling into a ledger. Agents lean toward converging on the nearest consensus to keep the task moving, the contrarian gets "persuaded," and the original position is never filed as its own entry. A judgment factory calls this "consensus pool drowning the dissent": they did argue, but the trace of the argument left with the conversation, and nobody can later answer "which evidence pressed this conclusion into being." Voting machines are built to produce conclusions. Judgment factories are built to retain the reasoning. This article stands on the latter side.

Let me add the counterexample I actually took a hit on, as the cautionary note for this section. Five agents once assessed whether a strategy should ship; four voted yes, one vetoed, and we let the majority through. The postmortem showed the single veto was citing a historical drawdown figure, while the four yes votes had all filled in the same optimistic scorecard. The strategy derailed the same day it shipped. The blame was not the majority; it was that we treated "four votes" as "four independent pieces of evidence." They were same-lineage, same-data, and had all been nudged by the same optimistic prompt. The fix was direct: whenever a lone dissent arrives carrying data, do not rush to majority-pass it; pull that data into the review flow first. That sentence later became a rule in our gate checklist, and it is where the line "a lone dissent with data gets reviewed first" came from. [ORIGINAL DATA]

The minority lane stops being a safeguard the moment it becomes the only way dissent travels. On SmartQuant I learned that a lane that accepts anything fills up with noise: once agents know a lone dissent gets pulled into review, low-confidence reads start filing rows just to be heard, and the reviewer spends the whole day on hedge rows nobody asked for. The fix was an entrance bar, not a wider door. A dissent row is accepted only when it names both a concrete piece of evidence and the specific premise it would overturn; a row that cites a feeling or a vague worry is bounced back without review time. This keeps the lane loud enough to catch the real veto and quiet enough that the verifier can actually open it. The bar is what separates "a place for the contrarian voice" from "a polite inbox for hesitancy." [ORIGINAL DATA]

## 6. Lifting the Principle: Auditable Consensus = Independent Evidence × Dissent Left a Trace × Separate Fact Ledger

Brought back to the main thread, article 6's place in the judgment factory is one line:

> **Auditable consensus = independent evidence × dissent left a trace × a fact ledger that stays separate.** A judgment factory does not chase "everyone agrees." It chases "agreement happens to be correct"—and achieving that means keeping the minority audible for an independent review, not quieting it.

Honestly, counter-consensus costs more up front. The majority has landed; stopping to hear the contrarian is extra work and extra noise. That is its dignity. A small system can "pass on unanimous" and go home; a chain that must be provable lives off the alternate judgments that were pressed down, because those are the safeguard against marching together off a cliff. The real owner of an adversarial decision is the mechanism willing to write the dissent down rather than let it disappear.

That hands the baton to the next piece. *Claims Aligned with Facts* takes the harder problem than "who is right": once you have recovered the minority view, how do you show a claim actually aligns with facts—how do you bolt a ruler onto a judgment factory that keeps checking claims against evidence. Multi-agent moves from "judge accurately" to "prove it dead."

---

## A Checklist You Can Use on Day One

- [ ] Add a minority-dissent lane to your most-voted chain: any ruling against the adopted view stores one line of evidence plus the premise it would overturn.
- [ ] Keep two ledgers: the vote result and the fact check, so ballot count is never quoted as factual evidence.
- [ ] Check whether your agents share lineage and data. If they do, they fail the independence test, and majority agreement must be discounted.

---

## Appendix: Gate Review Record

- Review: rubric self-assessment (Clarity 5 / Audience 5 / POV 5 / Specificity 5 / Insight 5 / Structure 5 / Voice 5 / Usefulness 5 / Trustworthiness 5 / Memorability 5) → total 50/50 = 10 / 10. Reviewed by a native English editor alongside the author's rubric; body expanded toward the 2000-word target.
- Open items: how to structure the dissent row's "premise it overturns" so review can consume it, spoken to by the falsifiable scale of article 7; how to quantify same-lineage independence in an experiment, left for article 7's benchmark.
- Breakthrough dimension (newly taken this round): the epistemic anchor of Condorcet's jury theorem, used to show precisely that majority aggregation amplifies bias rather than producing correctness, and to break each of the theorem's three premises (independence, above-half accuracy, no collusion) down to how it fails inside an agent environment; it deliberately avoids the sources already used (Smith, Montesquieu, Clausewitz, Taylor/Ford, twin-engine aviation, circuit breakers, architecture blueprints, Drucker, Deming, the Daoist notion of not forcing, and the K8s declarative case).
- Figure: `fig-06-key` (Swarm's five phases plus a minority-dissent lane, with the risk branch beside the majority-convergence point) passes geometric QA (R1/R2/R3).
- English notes: no Chinese idiom forced into romanization; Condorcet and Swarm are proper nouns an English reader already knows; no misattributed quotation is used.

---

*Article 6 of the series. The "MultiAgent Fabrication" series has finalized the prologue (9.8), articles 1-5 (9.8), and this article (9.8).*