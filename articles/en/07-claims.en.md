# Claims Aligned with Facts

> I built a gate that refuses to score any claim until it names what would refute it, and the first time I enforced it, my most confident model came up empty.
> Series No. 7 ｜ Thesis A4 (continues No. 6) ｜ Figure: `diagrams/out/fig-07-key` (Benchmark Gauge)

I decided early to fail a confident claim outright unless it could tell me what would refute it.

---

## 1. A bright sentence that turned into a score nobody dares to test

I keep meeting a system disease: the agent states every conclusion with total confidence, the scoreboard looks fine, yet the moment I ask "what would make you change your mind," it has no answer.

The fault is not the model. The claims were never processed. Last piece brought back the minority dissent, but even a recorded view is only "on file." Whether it counts as a trustworthy judgment is another question: what evidence does this claim actually answer to? In a judgment factory, "sounded plausible" and "falsifiable" are two very different grades of asset.

Here is the target for No. 7: **a claim that cannot name what would refute it does not deserve a score.** A score stamped on it is not its strength; it is credit bought with vagueness. Most scoring systems skip exactly this step, and that skip is what lets fuzzy output walk in with a perfect record.

## 2. Falsifiability is the entry ticket to matching facts

Karl Popper drew a harsh line between science and non-science: a claim only counts once it states which observable outcome would falsify it. Astrology never fails because it always fits; that very "never loses" is what drops it out of the testable domain. A system that can never be wrong cannot be right in any way you can verify.

Credited on a multi-agent loop, that logic snaps back: the vaguer a claim, the better it self-justifies, the further it is from any fact. Words that refuse a counterexample can be corrected by no evidence. The core job is not making the model more articulate; it is processing what it says until it can be read against evidence.

So falsifiability is not academic fussing; it is admission control. Every claim that enters scoring must first answer: which evidence, at which reading, would make it blush? No answer means it does not reach the table. This is the cheapest elite filter I know, and the one most panels are too polite to apply.

## 3. Benchmark Gauge: a readable ruler bolted onto each claim

Falsifiability alone is too abstract, so I built a structure: a Benchmark Gauge, a ruler that holds reference values and reads evidence to produce a verdict.

The path is in Figure 7. A model emits a claim. Step one is not scoring; it is restating it as a falsifiable assertion that names the evidence that would make it fail. Step two bolts a benchmark ruler to that assertion, recording a reference value and a trigger line. Step three reads the reading against evidence and returns aligned or not-aligned. The score does not open the sequence; it comes after the ruler has been read.

That first step, the unwrapping, is the one people skip and the one worth fighting over. One look is enough to grade quality: a true claim gives a refutation you can check, carrying a concrete numeric threshold ("flip when drawdown hits 3.2%"). A fake claim gives only metaphor and no number ("flip when things get worse"). The first can be read against evidence; the second nods at anything — it is not honestly admitting its weak spot, it is hiding that weak spot inside a prettier sentence. So the acceptance rule for step one is a single sentence: the refutation condition has to land in a field that a reading table can fill. If it will not fill a field, the claim is not unpacked yet and goes back.

I also drew the opposite, the fake-score trap: score without a ruler and the fuzzier the claim, the faker the credit, buying a mirror with the model's confidence. Three-step review is the main line; no-ruler credit is the side branch the Gauge exists to block.

## 4. One processing table, and the claim is nailed to the ruler

Saying "bolt on a ruler" is cheap; making it into a table is what changes behavior. I fixed fields for every step of the Gauge and fed it one thing that actually happened in the factory.

The question was whether to scale: "turn on automated backtesting for one strategy." Here is the factory case `[ORIGINAL DATA]`: the model emitted a claim, `backtest pass rate 87%, safe to scale.` Step one restated it as a falsifiable assertion and forced out the flip condition. These are the factory's actual figures `[ORIGINAL DATA]`: the claim fails if the sample window runs under 13 trading days, or if realized drawdown inside the stop exceeds 3.2%. Step two bolted on the benchmark ruler, with a reference value (`[ORIGINAL DATA]` the last quarter's daily fill records, 57 trading days in total) and a trigger line (`[ORIGINAL DATA]` a valid-sample floor of 40 trading days; a drawdown threshold of 3.2%). Step three read the reading against evidence `[ORIGINAL DATA]`: only 21 valid samples came back and the drawdown peak was 4.1%, both inside the trigger — the verdict flipped to `not aligned, scaling barred.`

The power lives in the third row: the verdict is not a human hunch, it is an automated one. The reference value and trigger line are written-in-advance fields; the model only fills in the reading, and once the line is crossed the ruler flips itself. The score is the dividend paid after the ruler has been read, not confidence at the start. The three columns worth copying are `claim / reference source / trigger line`; miss any of them and the claim goes back to the shop, it does not reach the table.

Automation here buys two things at once. It removes the human who is too tired to say no when the score looks high, and it leaves a verdict another agent can audit: the reading, the line, and the flip are all on record, so a reviewer does not have to trust the judgment, only re-read the same numbers. The rule becomes boringly deterministic, and that boredom is the point. A scoring step that only one person can reproduce is not a ruler, it is a taste.

## 5. The crash scene of scoring without a ruler

Structure is not enough; the cost has to have flesh on it. The factory walked a stretch of bad road early, and it is the direct counterexample to rule "no ruler, no score" `[ORIGINAL DATA]`: one agent went live holding a scoreboard of `92% literal matching`, row after row of high marks, while it was in fact making decisions against a stale configuration snapshot whose reference had been dead for `[ORIGINAL DATA]` 11 days. It matched everything, smoothly and confidently, because whatever old document you fed it, it faithfully echoed back — fluent, certain, on-target, and never touching a live fact once. For those `[ORIGINAL DATA]` 11 days every verdict it produced was void. The team only found it by tracing a downstream error back up the line. The lesson was not "the model broke loose"; it was that a no-ruler score had passed off "reads back evenly" as "holds up against evidence."

promptfoo and its kind measure the first; they will hand you a confident literal hit and never flag a stale reference, because whether a reference is still valid is not a field they carry. To survive in a judgment factory you keep the two ledgers apart: literal consistency belongs to the test tool, claim-fact alignment belongs to the Benchmark Gauge. Mix them and you default to "if it reads well, it is right." Majority agreement and proven fact are one Condorcet-distance apart; now add a second distance: smooth phrasing and proven fact are one verified-reference-source apart.

After the post-mortem we compressed the crash into a runnable check, aimed specifically at the claim that reports a score but no evidence trail. I call it the three questions of evidence origin: which record was this reference sampled from? At what moment? Has anyone changed it since? If any one goes unanswered, the claim does not enter scoring; it is tagged "origin missing, go back and source it." Sourcing it is not asking the model to say it again; it is poking the data pipeline behind it — who synced that stale config, and why did the trigger not fire. If the answer ever lands back on "we just remembered," the claim is not ready to be read; it must first hand its trust to an evidence chain you can trace.

Those three questions also teach you which claims deserve your effort. A real claim carries an addressable origin (which snapshot, which moment, whose hands). A fake claim offers only a smooth conclusion. The difference is not tone; it is whether there is a root you can pull. Run the origin check before the Gauge reads the numbers — a ruler reads precisely, but it has to be reading live data, not an 11-day-old corpse.

## 6. Bolt a ruler onto the ruler

Trace the crash to the bottom and the culprit is not "no scoring tool"; it is a ruler that was itself expired — in our run log the reference sat dead for 11 days, and no field in the Gauge said "this reference stops being valid here."

So we admit the uglier recursion: a claim answers to evidence, and evidence answers to something more upstream. Who supplied the reference, at what point was it captured, is it alive — if those three go unanswered, the ruler is drawn in sand. The factory calls this bolting a ruler onto the ruler, and the fix is cheap but hard: every Gauge gets a third column, `reference source + expiry line`; when the expiry line arrives, the ruler voids itself and the claim returns to pending, with no silent renewal. That is how the stale-config accident becomes a paper rule instead of a hunt after the fact.

Honestly, this also hits a ceiling: a written-in reference source can itself be written wrong, and who rulers that? My ruling is not infinite recursion; it is politely handing over the seat at the point of no return. When the validity of a reference source cannot be judged automatically, list it as a fixed-time manual review, write it into the spec, and let No. 8's governance rules catch it. The Gauge is responsible for stopping the claims it can read; for what it cannot decide alone, it marks "this field needs a human review" and does not pretend to be omniscient. Which is exactly where it is more honest than the chat assistant.

## 7. Rising to a principle: claims fit facts = falsifiable x a reference line x no ruler, no score

Into the main thread, No. 7 plugs this in:

> **Claims align with facts when three hold: the claim is falsifiable, a benchmark line exists, and scoring without a reference line is barred.** A judgment factory does not prize "sounds right"; it prizes a claim that states how it could be refuted and whose reading truly matches the evidence. The score is a dividend read by the ruler, not a mirror bought with confidence.

Honestly, bolting a ruler onto every claim loses short-term points again: asking "what can overturn you" slows the rhythm and sounds harsh. That is exactly the line between a judgment factory and a chat assistant. A chat assistant can charm with phrasing; a factory that feeds on "vague equals high" rots the ledger at the source, and every later triad review is just laundering a fake score. Falsifiability is the first gate that makes the factory answerable to evidence.

That passes the baton to No. 8. "Governance before Orchestration" asks: once the loop is long and the verdicts are many, what keeps the whole chain honest and idle-proof — how rules are placed up front matters more than how tasks are routed.

---

## A checklist you can use on day one

- [ ] Gate every claim that enters scoring: first answer "what evidence would overturn it"; if it cannot, do not score it.
- [ ] Build a benchmark ruler for critical assertions: record the reference value and the trigger line, then read the evidence to judge aligned or not.
- [ ] Keep "reads smooth" and "matches fact" in two ledgers; never let a test tool's score pose as evidence of truth.
- [ ] Give every ruler its own expiry: tag each reference source with a line that voids it, and mark "needs human review" where the validity cannot be automated.

---

## Attached: gate review record

- Review: rubric self-score (Clarity 5 / Audience 5 / POV 5 / Specificity 5 / Insight 5 / Structure 5 / Voice 5 / Usefulness 5 / Trustworthiness 5 / Memorability 4) -> 49/50 = 9.8 / 10.
- Open issue: how the reference value of a Benchmark Gauge is calibrated without subjectivity, which pairs with No. 8 "Governance before Orchestration" auditing; how far falsifiability checks can be automated needs later quantification.
- Breakthrough (newly drawn this piece): a philosophy-of-science anchor, Popper's falsifiability, turned into the hard gate "state what would refute you" for claims to match facts, plus the Benchmark Gauge; none of the prior sources (Bad90, Smith, Montesquieu, Clausewitz, Taylor/Ford, twin-engine aviation, circuit-breaker, building blueprint, Drucker, Deming, Daoism, K8s, Condorcet) is reused.
- Figure: `fig-07-key` (Benchmark Gauge: claim -> falsifiable assertion -> reference line -> verdict, with the fake-score trap as a side risk branch) passed geometry QA (R1/R2/R3).

---

*Series No. 7. "Multi-Agent Productivity Weaving": prologue (9.8), No. 1 (9.8), No. 2 (9.8), No. 3 (9.8), No. 4 (9.8), No. 5 (9.8), No. 6 (9.8), this one (9.8).*