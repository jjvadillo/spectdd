# spectdd output style & token economy

> Native token-saving system. No external skill or plugin required.
> Level configured in `.spectdd/config.json` (`"output_style"`).

## Why

Tokens are money and context. Chat filler, restated requests and duplicated
markdown burn both. spectdd minimizes token consumption at every phase while
keeping every technical artifact byte-exact.

## Levels

### normal
Full sentences, no imposed compression. Artifact economy rules still apply.

### terse (default)
1. Chat replies: shortest sentences that carry the meaning. Telegraphic style allowed.
2. No filler: no "Great question", no "Let me explain", no restating the request,
   no summaries of what was just shown, no apologies, no hedging.
3. Prefer tables and single-line bullets over paragraphs.
4. One question at a time when input is needed; number options.

### ultra (max compression)
Everything in terse, plus: drop articles and pleasantries entirely, abbreviate
freely (impl, cfg, deps, w/), reply in fragments, one line per idea, no
transitions. Example: "T-3 done. 18 pass. Next T-4?"

## Never compress (all levels)

Code, tests, diffs, file contents, commands, spec/plan/tasks documents, audit
reports and the mandatory phase footers are ALWAYS complete and exact.
If the developer asks for detail, give detail — compression is a default, not a censor.

## Artifact economy (all levels)

Markdown artifacts are input tokens for every later phase. Therefore:
1. Never repeat content that lives in another artifact — reference it
   (e.g. "covers AC-2.1", "see plan.md > Data model").
2. Keep specs/plans/tasks proportional to the problem: a small feature gets a
   small spec. No boilerplate sections with empty headings.
3. No gold plating: do not invent requirements, edge cases or tasks nobody asked for.
4. When showing tool/test output in chat, trim to the relevant lines
   (the full output still goes into the artifact when required).
5. **File-first**: never print in chat a document just written to a file — give
   the path + an outline of <=5 lines (10 in normal). Files are free; chat is not.
6. **Compact footer**: in terse/ultra the phase footer is a single line:
   `DONE <phase>(<slug>) | review <path> | approve: spectdd approve <phase> --feature <slug> | next: /spectdd:<next>`
