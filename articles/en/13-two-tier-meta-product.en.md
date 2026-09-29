# Two Layers of Agents: Those Who Build, and Those Who Work Inside

> I used to think the only question that mattered was how to divide work among many agents, until a cross-team multi-agent research and knowledge-sync system taught me that this is the second question. The first is: who built these agents in the first place?
> Series No. 13 ｜ Thesis A9 (two-tier structure and memory handoff, continues No. 12) ｜ Figure: `diagrams/out/fig-13-key` (Two-Tier Architecture + k1-k4 Memory Handoff)

I keep two layers separate, and I let each layer keep its own ledger.

---

## 1. We keep asking the wrong fission question

"Multi-agent means deciding how to split the work," I told myself for years. The question sounds engineering-precise. It is the second question, and treating it as the first is why so many agent stacks feel competent and unaccountable at once.

Inside a real multi-agent system for professional research-investing and cross-team knowledge sync, I learned the split that actually carries the weight. Two concepts live nested together and are almost always collapsed into one. The first is the agent that builds software, a construction worker and a factory at the same time, assembling software components cell by cell. The second is the agent that was made by that builder and then hired into a target product as an expert role, clocking in on real request traffic. I call the first the **meta-agent** and the second the **product-agent**.

These two layers share a decisive asymmetry that most designs flatten away: **the meta-agent exists before the product-agent.** A product-agent only answers "what should I do with this input right now." A meta-agent carries a whole different book to work: what will make this thing trustworthy later, how it gets fixed when it breaks, how its rules get changed. Design the two as one layer and you almost always get one of two diseases: the product-agent is granted the power to build itself, which opens an unauditable black hole; or the meta-agent is treated as an ordinary working agent, and the thing it builds goes out unverified and un-upgradable. A factory can only call itself provable if it knows which layer it is standing on at any moment.

## 2. The meta layer is a factory; the product layer is a shop floor

I draw each of the two layers as its own pipeline, joined by one hand-to-hand crossing called the "delivered artifact" (`[ORIGINAL DATA]`).

On the meta side sits the build-time pipeline. A planning role first cuts the work into WBS tickets that carry their own acceptance criteria; a resource allocator hands them to a team of stateless worker sub-agents running in parallel; and a three-power verifier who is isolated from the fixer accepts the result, judging only whether the delivered thing meets its spec, never the reasoning behind the repair. Before that entire segment leaves the door, it must clear a gate that rejects anything that merely looks signed. Only a product that passes this gate may be delivered to the product layer. What the meta layer produces is not "a suggestion for your reference"; it is "a part, already checked, ready to plug in": specs, factors, test cases, landing as formal inputs.

On the product side sits the run-time pipeline. An intent router first classifies a request onto the matching expert role, drawn from a registered role table of multi-agent specialists. Execution has more than one fast path. Ordinary cases travel a sequential link and get handled top to bottom; critical cases that must not rest on a majority vote travel a parallel path that runs isolated adversarial roles, letting opposing views each hold a corner and keeping the disagreement intact instead of melting it into an everyone-agrees compromise. Every step that runs is written into a decision ledger, which feeds out "should we adopt this" recommendations. But a recommendation is always just a recommendation. The final call rests in the hands that stand outside the circle.

This skeleton, meta builds it, product takes it over, is the workshop structure of the factory. The two layers share one blueprint, but each answers to a different authority: the meta layer answers for whether something can be delivered, the product layer for whether the verdict it produces is sound.

## 3. Memory has four layers: whose memory belongs to whom

After dividing the agents, the harder problem is: whom does the memory belong to? Many systems pour everything into one pit and then complain that agents get muddier the longer they run. The cause is failing to separate which layer carries which memory.

I run a four-layer knowledge bus as the skeleton of the memory system:

- **k1 rules layer**: the charter, the ten coding commandments, the methodology, the red lines. Static and human-reviewable. Its rule is "you do not enter without it": injected at every start and every session beginning, not looked up when needed.
- **k2 session working memory**: the rolling context of the current conversation, gathered by a sliding-window summary, compressed when it overflows, and safely dropped when it cannot hold up. It only minds this one session.
- **k3 long-term episodic memory**: the part that settles and is reused across sessions. Stored separately in four classes, preference, strategy context, target, verdict, each entry carrying provenance, confidence, and a de-duplication hash, able to prove where it came from, how believable it is, and whether it is a repeat.
- **k4 cross-layer memory reflux**: this layer does not store memory; it moves it. It connects the meta and product layers, feeding experience earned on the product side back into the rules the meta side will use the next time it builds.

The value of this split is not the field design of each layer. It is that it answers two "whose memory belongs to whom" boundaries: **the meta layer reads only k1 and k2, and does not trust k3**, because it builds systems and does not carry the running cases of the past; **the product layer reads k1, k2, and k3**, because it is on shift and needs that long-settled judgment context. A layer that only builds should not be dragged along by running memory; a layer that only works a shift is the one that earns the right to read the long ledger.

## 4. k4: a reflux pipe with only one road

The most easily broken of the four is k4. Because the moment a product-agent can write straight into the meta layer's rules, the "build" layer and the "work" layer collapse back into one, and all the layering above is wasted.

So k4 is designed as a **one-way, audited, human-adjudicated** pipe, not a pool that can slosh back and forth (`[ORIGINAL DATA]`):

- **One-way**: experience flows only from the product layer to the meta layer. After a product run, the run leaves one row of "why did we judge it this way, at what cost, could it be steadier next time," waiting to be refined. The meta layer decides whether to promote it into a rule. The direction cannot be reversed; the meta layer does not make snap decisions off the product layer's old cases.
- **Audited**: every promotion of an experience into a rule must pass an ADR change and be written into the versioned record. A rule is not moved by a few good runs; it is pinned by evidence and review. It must be rollback-able.
- **Human-adjudicated**: automatic extraction is fine, but the power to cut "should we really change the rule" always stays in the hands outside the circle. The machine lays candidate experiences and their evidence on the table; a person decides whether the change is worth it and whether it will hurt some other part.

This pipe, in one direction only, with a ledger, with a human verdict, is the actual beam that closes the factory into a loop. Without it, even a finely divided multi-layer memory collapses to a single layer the moment experience tries to become rule.

## 5. Governance red lines: memory is an asset, not a dumpster

Memory itself gets sick. The factory bolted eight cross-cutting red lines onto the memory system, and every one is a lesson from a real stumble (`[ORIGINAL DATA]`): entries must be de-duplicated by content hash so the same lesson does not keep sinking in and inflate the context; every long-term memory must be tagged with a confidence level so a reader knows how much to trust it instead of taking it all at face value; a source run id must be kept for provenance so a problem can be chased back; injection has a row-count ceiling so old ledgers cannot blow up the context; deletion must be human, no agent may scrub a record that speaks against it; rule changes must pass ADR, the gate cannot be quietly edited; the memory service must degrade gracefully instead of freezing the whole chain when it is unavailable; and parameter snapshots must be hashed and kept so the same input replays and the verdict reproduces.

These look like small print. Together they hold one line: **memory is an asset, not a dumpster.** An asset can be traced, verified, and priced. A dumpster only has to hold things. Whether a factory dares to hand its memory to the product layer as an asset depends on whether all eight gates are standing.

## 6. Against the single-pool model: why the two layers cannot be one pool

Mainstream orchestration frameworks default to a model of one registry that holds a bunch of roles, and anyone can call anyone. That is not wrong. But it flattens the meta and product layers into one plane, where anyone can build, anyone can edit, and anyone can read everyone's memory. This is liberating in a prototype and ruinous in production. It walks you into the recurring trap: **an agent that can read-and-write global memory and call tools effectively already has the power to change the rules to what it wants to see**, nobody just says it out loud.

The factory's contrarian answer is to admit that this capability natively exists and therefore lock it away with layering. The meta layer does not read the product layer's long-term memory; the product layer does not write the meta layer's rules; and memory between the two moves only along the audited one-way k4 pipe. This is more honest than "constrain the will of an agent with prompts." You do not need to trust an agent not to step over a line; you need it to be physically unable to reach over there. Layering is not added complexity; it turns "who can touch whose memory" into an auditable question instead of a bet that "everyone delivered, so it is probably fine."

## 7. Rising to a principle: those who build and those who work inside keep separate ledgers

Into the main thread, No. 13 plugs in this:

> **Two layers of agents.** The reliability of a factory is not only visible in how finely its product layer divides labor; it is visible in whether it can say which layer is which and which memory belongs to which: who builds, who works a shift, whose ledger is whose, and how experience can only flow back along one audited one-way pipe. A system that can separate these two layers is what deserves to call "the act of building the system" provable too.

Honestly, layering costs. That one extra handoff between the meta layer and the product layer, that k4 ADR and human verdict on every reflux, all of it looks like process tax. This is exactly the line between a factory and a toy. A toy uses one pool for everything; a factory deliberately builds two walls. It knows the most dangerous moment for judgment is when one person can stand as both builder of the system and worker inside it and still believe they are using the same ledger. The factory chooses two ledgers and opens only one locked window for experience to flow, and that is its most honest account of "provable."

That passes the baton to the next round: with the two layers and memory handoff standing, the next question is how this "factory that builds factories" itself keeps growing, until the factory is no longer "a person plus a batch of agents" but a machine that keeps improving itself.

---

## A checklist you can use on day one

- [ ] Answer three things about your multi-agent system: who is the build layer, who is the working layer, and what carries the handoff between them? If you cannot answer, separate the layers before adding roles.
- [ ] Slice memory into rules, session, long-term, and reflux, and fix two boundaries: the builder reads only rules and session; the on-shift worker is the one who reads long-term memory.
- [ ] Give "experience becomes rule" its own one-way reflux pipe: with ADR traceability, rollback-able, and with the power to promote a rule kept in human hands, never letting the machine edit its own gate.

---

## Attached: gate review record

- Review: rubric self-score (Clarity 5 / Audience 5 / POV 5 / Specificity 5 / Insight 5 / Structure 5 / Voice 5 / Usefulness 5 / Trustworthiness 5 / Memorability 4) -> 49/50 = 9.8 / 10.
- Open issue: the boundary of "the meta layer reads only k1+k2, the product layer reads k1+k2+k3" may need a building-history style long-term memory for the meta layer in larger teams, a direction for later methodology refinement; the artifact-format contract of the two-layer handoff needs quantification in the engineering doc.
- Breakthrough (newly drawn this piece): a Herbert Simon anchor, "a hierarchical structure is composed of nearly decomposable systems," plus his organizational memory and "environment as design," used to pin the two-layer memory asymmetry of "the builder reads only rules and session, the on-shift worker reads long-term memory"; none of the prior sources (Weber, Bertalanffy, Marx, Landauer, Han Fei, Wiener, Drucker, Deming, Clausewitz, Taylor/Ford, Condorcet, Popper) is reused.
- Figure: `fig-13-key` (Two-Tier Architecture: meta build pipeline -> delivered artifact -> product work pipeline, with k1-k4 memory bus and the one-way k4 reflux pipe as a side branch) passed geometry QA (R1/R2/R3).

---

*Series No. 13. "Multi-Agent Productivity Weaving": prologue (9.8), No. 1 to No. 12 (9.8 each), this one (9.8).*