# Snakemake-Workflow fr den Multi-Agenten-Prozess

MANUSCRIPT = "/workspace/manuscript"
OUTDIR = "/workspace/.agent"
PLANNER = "/workspace/planner_output.yaml"
TARGETS = "/workspace/prompts/chapter_word_targets.json"


rule all:
    input:
        OUTDIR + "/chunks.json",
        OUTDIR + "/plan.json",
        OUTDIR + "/verify.json",
        OUTDIR + "/audit.json",
        OUTDIR + "/edits.json",


rule chunks:
    output:
        OUTDIR + "/chunks.json"
    shell:
        f"python3 -m agents.cli chunk --input-dir {MANUSCRIPT} --output-dir {OUTDIR} --level 2"


rule plan:
    output:
        OUTDIR + "/plan.json"
    input:
        PLANNER
    shell:
        f"python3 -m agents.cli plan --planner-yaml {PLANNER} --output {OUTDIR}/plan.json"


rule verify:
    output:
        OUTDIR + "/verify.json"
    input:
        chunks = OUTDIR + "/chunks.json"
    shell:
        f"python3 -m agents.cli verify --manuscript-dir {MANUSCRIPT} --targets {TARGETS} --output {OUTDIR}/verify.json"


rule audit:
    output:
        OUTDIR + "/audit.json"
    input:
        chunks = OUTDIR + "/chunks.json"
    shell:
        f"python3 -m agents.cli audit --chunks {OUTDIR}/chunks.json --output {OUTDIR}/audit.json"


rule execute:
    output:
        OUTDIR + "/edits.json"
    input:
        chunks = OUTDIR + "/chunks.json",
        audit = OUTDIR + "/audit.json"
    shell:
        f"python3 -m agents.cli execute --chunks {OUTDIR}/chunks.json --audit {OUTDIR}/audit.json --log-dir {OUTDIR}/logs --output {OUTDIR}/edits.json"

