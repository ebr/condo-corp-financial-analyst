# condo-corp-financial-analyst skill

Skill source lives here. It may be optionally  symlinked from e.g. `~/.claude/skills/condo-corp-financial-analyst` for realtime updates during development.

## Packaging

*Soft Prerequisite*: official anthropic/skill-creator plugin needed to run evals and the automated packaging workflow.

Otherwise, only `SKILL.md` and `references/` comprise the actual body of the skill. The rest is development harness.

```bash
cd ~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator
uvx --with pyyaml python -m scripts.package_skill <path-to-this-project-dir> /tmp/
```

## Running evals

Tell Claude: *"run evals on the condo-corp-financial-analyst skill"* — the skill-creator plugin
handles spawning agents, grading, and opening the viewer. Results land in `evals/iteration-N/`.

## Development

- any implemented stories must have a corresponding eval or test suite.
