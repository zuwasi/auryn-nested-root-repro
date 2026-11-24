# Auryn repro: nested package root resolves under two dotted identities

Minimal repro for the cross-repo linkage warning:

```
cross-repo resolution MISS: 1 reference(s) matched a definition that
differs ONLY by a module prefix -- likely a package-root / project-layout
mismatch (the defining repo's dotted path has an extra leading dir, e.g.
a `src/`- or hyphen-wrapped root). These did NOT resolve and left a
dangling `resolved:false` placeholder
```

## Layout

```
plugins/com.esl.feltfixinator.backend/   # Eclipse plugin project dir (not a Python package root)
    backend/                             # Python package root: has __init__.py, put on sys.path
        __init__.py
        llm_client.py                    # class LLMClient
        violation_loader.py
        feltfixinator_bridge.py          # import llm_client  (bare import, sys.path hack)
run_bridge.py                             # from backend.feltfixinator_bridge import Bridge
```

`backend/` is a real package root (has `__init__.py` and is added to `sys.path`
by `feltfixinator_bridge.py`), but it is nested under
`plugins/com.esl.feltfixinator.backend/`. The same files therefore get two
dotted identities:

- file-path based: `plugins.com.esl.feltfixinator.backend.backend.llm_client`
- package-root based: `backend.llm_client`

Definitions are indexed under one identity while references resolve against the
other, so `import llm_client` inside `feltfixinator_bridge.py` cannot link to
the real `llm_client.py` and stays as an unresolved placeholder even though the
module is in the same repository.

## Observed result (Auryn 0.8.x, Windows)

`auryn ingest dir . --project-name nested-root-repro` reports:

```
WARNING [auryn.core.linkage] cross-repo resolution MISS: 1 reference(s)
matched a definition that differs ONLY by a module prefix ...
INFO  [auryn.core.linkage] cross-repo: 3 external reference(s) unresolved
after reconciliation (no definition in graph yet); 1 look like a layout mismatch
```

Querying the graph for unresolved nodes confirms `llm_client` and
`violation_loader` (real modules in this repo) sit unresolved, alongside the
expected stdlib externals (`sys`, `pathlib`).

## Suggested direction

A normalization pass that retries matching with the leading package prefix
stripped, or a per-repo layout hint in the config, would close these
automatically.

## Origin

Distilled from a real private repo with the same shape (an Eclipse plugin whose
Python backend is nested under `plugins/<plugin.id>/backend/`), where 83
references hit this exact mismatch.
