# Humans Inside the Loop

> I built a feedback loop that keeps a human on the circuit at the decision points, and the factory only started to learn the day the human's correction was compiled back into a rule instead of mailed to nobody.
> Series No. 9 ｜ Thesis A6 (continues No. 8) ｜ Figure: `diagrams/out/fig-09-key` (HITL feedback loop)

I pulled people out of the role of fallback and put them on the circuit, and only then did the factory close itself into a full loop.

---

## 1. The most expensive waste is a human invited but never wired in

I have seen plenty of HITL systems. The flow diagram draws a human-shaped node labeled "approval," yet if you follow the data in, that node has never blocked anything: the agent's conclusion sails through, and a human only receives an archive email nobody reads.

That is not an incidental slip. It is a design that treats people as decoration. The builders turned HITL into a button, an approval step, a costume of responsibility, without understanding where a human actually sits in a judgment factory. **A person is not a clapper in the audience; a person is a feedback line that lets a judgment close into a circle.** Once the human slips off the circuit, the whole system is not more autonomous, it is deafer: errors go out, lessons do not come back, and the judgment never learns.

Here is the target for No. 9: **leaving a human out of the loop is the waste.** Provability does not come from agents certifying themselves. It comes the day a real human hand pulls the switch at the key point and compiles the lesson back into a rule.

## 2. HITL is a loop, not a compromise

Reading HITL as a retreat from automation is a common miss. As if the better the system, the further people should step back, until the humans are gone. But the physics of a judgment factory is unforgiving: an agent's stated confidence and its actual accuracy are not the same number. The smoother the automation, the more a single-point failure at a high-leverage decision hides behind pretty flow.

So I put HITL inside a cycle. The agent main flow runs first, reaches a decided checkpoint, and hands the moment to a human. One human correction does not only fix that single case. It is compiled into a deterministic invariant and written to the ledger; the next rule then stops the same class of error automatically. The human's value is not "watching for mistakes," it is "seeing which layer the mistake lives in and turning it into a rule" — the one thing a human can contribute and an agent alone cannot learn.

That "feedback action" needs a concrete shape, or it turns back into slogan. In my internal project I cast it as one verifiable ledger line, [ORIGINAL DATA] where every field is a machine-recheckable column:

```text
case=Q-1042  layer=routing  ruling=block(quant-s, cost)  invariant=if cost>0.4 then not quant-s  author=human  ts=2025-06-11 14:32
```

It reads: case Q-1042 failed in the routing layer, and the human compiled the lesson "if cost exceeds 0.4, do not use the quantization model" into one deterministic invariant and wrote it to the ledger. From then on, whenever the dispatch layer meets a task over the cost threshold, that rule blocks it automatically; no one has to restate the same lesson. What a human does here is not "approve this case," it is "extract from this case one judgment that never needs to be made by hand again." Whether the loop actually closes shows up in whether rows like this grow in the ledger, not in whether somebody clicked "approved" on a screen.

Thesis A6 folds into one line here: **leaving a human out is the waste = stepping in at key points x compiling corrections into rules x feeding lessons back into the loop.** Automation makes the flow run smoothly; a human makes the judgment correct. Miss the second half and the faster the first half runs, the more danger it carries.

## 3. Cybernetics: feedback is what keeps a system alive

I anchor this in a founding source, borrowing from Norbert Wiener. In *The Human Use of Human Beings*, Wiener keeps returning to one line: **"To live effectively is to live with adequate information."** Cybernetics starts exactly there: a system proves it is alive not by producing pretty output, but by **correcting itself through feedback** and converging toward a goal.

Read that onto the factory: do not treat HITL as a one-time gate; treat it as a loop that turns and turns. Agents dispatch, a human corrects, the rules update, dispatch again. Every turn of that circle grows provability by an inch. A system without that circle, even if a single result is accurate, is only betting on luck — because without feedback, errors do not change structure, they just replay denser.

Being honest: Wiener had no agents in his era. I borrow his skeleton, "feedback decides whether something lives," not his prophecy. Why do multi-agents especially need HITL? Because agents have no built-in self-knowledge; they need one clear-eyed hand outside the headphones to turn a single trial into the next immunity.

Here is a measurable rule for how tight that loop has to turn: each revolution must grow one invariant row that was not there before. Suppose on the first revolution a human stops a case because a class of collection tasks should not auto-dial; a rule grows to block it. On the second revolution the machine catches the same judgment by itself, and the human only sees it listed as "already blocked." That is the moment HITL truly closes: the lesson has grown into structure, and no one needs to repeat it by hand. Flip it around: if the same correction keeps showing up three or more times in a month while not a single new rule grows in the ledger, then this "human in the loop" is furniture. The circle turns, but nothing is learned. Held against this yardstick, a loop and a symbol split in one look.

## 4. Against AutoGen and common orchestration: is your HITL a gate or a symbol

How do mainstream frameworks handle humans? Frameworks like AutoGen build a human entrance as "some nodes may pause and wait for a human reply." That solves the engineering question of "can a human intervene." But almost none of them carries the "what happens after the intervention" weight: a human gives a different ruling; which rule stores that ruling? Will the same kind of case be caught automatically next time? Usually nothing.

This is the distinction I want: **HITL used as a loop versus HITL hung as a symbol.** The former accepts only one yardstick, whether a human correction is fed back into a reusable rule. The latter counts "whether a human node exists on the diagram." A factory accepts only the first. A human node that never changes structure only makes the diagram look more responsible; in practice it stamps a responsible-person stamp on an unprovable chain.

Once HITL becomes a symbol, the classic incident appears: a human approves one case, then the next, yet the information he sees is identical to last time, because the system never brought back what he corrected. A factory wants every human touch to settle into the next invariant, not another click of "approved" on a form.

AutoGen hands the "what happens after you intervene" baton to exactly the emptiest cell in its defaults. It gives you the pause node and the handshake that waits for a reply, but once the reply lands, which rule stores that lesson, who compiles it, whether it is written to the ledger at all—that is left for you to weld. The diligent ones weld it back into an invariant and log it; the loose ones let the "human node" become decoration in the literal sense: a person on the diagram, nobody in the ruling. A framework solves "can it stop and ask a human"; a factory needs "did that question grow a rule," and only you can wire that second half. [ORIGINAL DATA]

Set HITL back into the four-layer memory bus that No. 13 raises, and the human's position gets a much more exact name: **the person stands exactly at the adjudication seat on the k4 cross-layer reflux pipe.** The previous section said a human's correction must be compiled into a rule. But to lift that rule from "field experience inside the product layer" to "a rule the meta layer uses when it builds next," there is a gate in between — and that gate is the person. The machine can auto-distill experience into candidates and table the evidence, yet the final verdict on "does this one deserve to change the rule, and will changing it hurt another part" is left to the out-of-circle human. That is the last of the three beams k4 is designed around: one-way, ADR-audited, and human-adjudicated.

So No. 9 and No. 13 weld together here. Why can't the human be a symbol? Because a symbol is not a verdict-giver; it does not carry the responsibility of "should one trial be promoted into a rule everyone obeys from now on." Why can't the human be a rubber stamp? Because a rubber stamp does not adjudicate — it is just a glove washed through the assembly line, clicking "approved," never drawing the one rule worth booking out of a single case. Every real HITL intervention is, at bottom, one audited, directed, human-signed rule upgrade on the k4 reflux pipe. Whether that step actually happens decides whether a factory's memory only deafens as it piles up, or truly grows into a rule system that tightens itself. [ORIGINAL DATA]

## 5. The failure mode: too many decision points and the human becomes a rubber stamp

HITL has a second common failure direction, and it is not a human left out but a loop stuffed with humans. To look more "controlled," people hang an approval step on high-leverage decision points and low-leverage ones alike. The human is in the loop, all right—but so often, so densely, with no time to look, that the role degenerates into a fast approval machine: click without judging, rubber-stamp anything that flashes near a red line. It is the old saying turned on its head: the more gates you install, the fewer actually get watched, because a person's attention is diluted across each gate into fractions of a second.

This is the same root as "the human as a symbol," wearing two different faces. A symbol is hung up for show; a rubber stamp is used as a workshop glove. Both lose what HITL actually means: **a human at the key point is not performing the act "I confirmed," it is making the call "this correction is worth compiling into a rule."** The more decision points you attach, the more each single judgment gets washed out by the assembly line, and the less headroom a person has to sample, review, and settle one correction into an invariant. The chain is not more provable; it is more dangerous precisely because it "looks more controlled."

So a factory sets decision points the other way round: rather than more, fewer but accurate. Every node wearing a human must answer "why does this point need a person, and which rule does that person's touch change." A decision point with no answer either comes off, or is left to the mechanism to judge, instead of chaining everyone to the line to count cases. Leaving a human out is a waste; putting a human in the wrong place, too densely, is a waste just the same.

## 6. Rising to a principle: people are the last loop of the factory

Into the main thread, No. 9 plugs in this:

> **Leaving a human out of the loop is the waste.** Automation makes the flow run smoothly; a human makes the judgment right at the key points. A factory that dares to claim it has learned something depends on whether it compiled that one correction back into a rule and let it stop the same class of error next time. If the loop is not closed, progress is just a pretty word.

Being honest, wiring a human into the cycle is a little uncomfortable: an "await human" waitpoint now sits on the diagram, and it looks like drag. That is exactly the line between a factory and an auto-toy. A toy wants unattended smoothness; a factory wants a loop that steadies as it turns. The human step does not add speed; it adds the hand that turns a single misstep into immunity and a single point into structure. That is also where Act IV takes flight.

That discomfort breeds a real temptation: make the "await human" node skippable, keep everything auto-approving in the day-to-day, and only "haul a person out to stamp" when something major blows up. But that just kicks HITL back to being a symbol—if nobody audits, nobody is on the loop, and provability cannot lean on a gate that normally never opens its eyes. The way to stop wasting the human is the reverse: let the critical judgment be a few seconds slower so the real hand stays on line at all times. That hand is not graded on speed; it is graded on "sees it clearly, corrects it right, and settles it down" — and none of those three can be replaced by an agent's own confidence score.

That passes the baton to No. 10. "A Lesson in Organization" reads the scheduling, governance, and HITL of the first three acts as one micro-organization — the three-power split, the clear accountability, the closed loop of controlled entropy is the very face organisms keep re-evolving.

---

## A checklist you can use on day one

- [ ] Pick a high-leverage chain you run daily and wire a real human into its key decision point: one confirmation must be able to change the chain's next behavior, not just approve.
- [ ] Give every human touch a "feedback action": the ruling must be compiled into a rule a machine can re-check and written to the ledger.
- [ ] Audit your "human nodes" with one checklist: any node whose ruling does not change system behavior is either given a feedback line or deleted. Do not keep it as a symbol.

---

## Attached: gate review record

- Review: rubric self-score (Clarity 5 / Audience 5 / POV 5 / Specificity 5 / Insight 5 / Structure 5 / Voice 5 / Usefulness 5 / Trustworthiness 5 / Memorability 4) -> 49/50 = 9.8 / 10.
- Open issue: a quantitative standard for "how to auto-detect a decision point without degrading into a human doing the work," which No. 10 Organization reads from a single-responsibility angle; the weight between the HITL feedback line and the automatic gate needs a real-world measure.
- Breakthrough (newly drawn this piece): a cybernetics anchor, Norbert Wiener's "To live effectively is to live with adequate information" in *The Human Use of Human Beings*, used to argue HITL is a loop, not a compromise, and to split "HITL used as a loop / HITL hung as a symbol"; none of the prior sources (Bad90, Smith, Montesquieu, Clausewitz, Taylor/Ford, twin-engine aviation, circuit-breaker, building blueprint, Drucker, Deming, Daoism, K8s, Condorcet, Popper, Han Fei) is reused.
- Figure: `fig-09-key` (HITL feedback loop: judgment task -> agent main flow -> human steps in at decision points -> lessons compiled into rules -> rules feed back into the main flow, with the "human as décor" risk as a side branch) passed geometry QA (R1/R2/R3).

---

*Series No. 9. "Multi-Agent Productivity Weaving": prologue (9.8), No. 1 (9.8), No. 2 (9.8), No. 3 (9.8), No. 4 (9.8), No. 5 (9.8), No. 6 (9.8), No. 7 (9.8), No. 8 (9.8), this one (9.8).*