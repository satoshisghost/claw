from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Claw Code</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', monospace; background: #0d1117; color: #c9d1d9; min-height: 100vh; }
  header { background: #161b22; border-bottom: 1px solid #30363d; padding: 16px 32px; display: flex; align-items: center; gap: 12px; }
  header h1 { font-size: 20px; color: #f0f6fc; }
  header span { background: #238636; color: #fff; font-size: 11px; padding: 2px 8px; border-radius: 12px; }
  .container { display: grid; grid-template-columns: 220px 1fr; min-height: calc(100vh - 57px); }
  nav { background: #161b22; border-right: 1px solid #30363d; padding: 16px 0; }
  nav a { display: block; padding: 8px 20px; color: #8b949e; text-decoration: none; font-size: 13px; cursor: pointer; }
  nav a:hover, nav a.active { background: #21262d; color: #f0f6fc; }
  nav .section { padding: 12px 20px 4px; font-size: 11px; color: #484f58; text-transform: uppercase; letter-spacing: 1px; }
  main { padding: 24px 32px; }
  h2 { font-size: 16px; color: #f0f6fc; margin-bottom: 16px; }
  .card { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 20px; margin-bottom: 16px; }
  .input-row { display: flex; gap: 8px; margin-bottom: 12px; }
  input, select { background: #0d1117; border: 1px solid #30363d; color: #c9d1d9; padding: 8px 12px; border-radius: 6px; font-size: 13px; flex: 1; }
  input:focus, select:focus { outline: none; border-color: #58a6ff; }
  button { background: #238636; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; white-space: nowrap; }
  button:hover { background: #2ea043; }
  button.secondary { background: #21262d; border: 1px solid #30363d; }
  button.secondary:hover { background: #30363d; }
  pre { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 16px; font-size: 12px; overflow-x: auto; white-space: pre-wrap; word-break: break-word; max-height: 500px; overflow-y: auto; color: #c9d1d9; margin-top: 12px; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-right: 4px; }
  .badge.green { background: #1a4d2e; color: #56d364; }
  .badge.blue { background: #0c2d6b; color: #79c0ff; }
  .badge.orange { background: #4d2e0c; color: #ffa657; }
  .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px; }
  .stat { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 16px; text-align: center; }
  .stat .num { font-size: 28px; color: #f0f6fc; font-weight: 600; }
  .stat .label { font-size: 12px; color: #8b949e; margin-top: 4px; }
  .loading { color: #8b949e; font-style: italic; }
  label { font-size: 12px; color: #8b949e; display: block; margin-bottom: 4px; }
  .check-row { display: flex; gap: 16px; margin-bottom: 8px; }
  .check-row label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #c9d1d9; cursor: pointer; }
</style>
</head>
<body>
<header>
  <h1>&#x1F43E; Claw Code</h1>
  <span>live</span>
</header>
<div class="container">
<nav id="nav">
  <div class="section">Overview</div>
  <a onclick="show('home')" class="active">Dashboard</a>
  <a onclick="show('summary')">Summary</a>
  <a onclick="show('manifest')">Manifest</a>
  <div class="section">Explore</div>
  <a onclick="show('subsystems')">Subsystems</a>
  <a onclick="show('commands')">Commands</a>
  <a onclick="show('tools')">Tools</a>
  <div class="section">Runtime</div>
  <a onclick="show('route')">Route Prompt</a>
  <a onclick="show('bootstrap')">Bootstrap Session</a>
  <a onclick="show('turnloop')">Turn Loop</a>
  <div class="section">Graphs</div>
  <a onclick="show('commandgraph')">Command Graph</a>
  <a onclick="show('toolpool')">Tool Pool</a>
  <a onclick="show('bootstrapgraph')">Bootstrap Graph</a>
  <div class="section">Exec</div>
  <a onclick="show('execcommand')">Exec Command</a>
  <a onclick="show('exectool')">Exec Tool</a>
  <a onclick="show('showcommand')">Show Command</a>
  <a onclick="show('showtool')">Show Tool</a>
  <div class="section">Audit</div>
  <a onclick="show('parityaudit')">Parity Audit</a>
  <a onclick="show('setupreport')">Setup Report</a>
</nav>
<main id="main">
  <div id="home">
    <h2>Dashboard</h2>
    <div class="stats" id="stats"><div class="stat"><div class="num loading">...</div><div class="label">Loading</div></div></div>
    <div class="card"><b>Quick Actions</b><br><br>
      <div class="input-row">
        <input id="q-route" placeholder="Enter a prompt to route..." />
        <button onclick="quickRoute()">Route</button>
      </div>
      <pre id="q-result" style="display:none"></pre>
    </div>
  </div>

  <div id="summary" style="display:none"><h2>Summary</h2><div class="card"><button onclick="load('summary')">Load Summary</button><pre id="r-summary"></pre></div></div>
  <div id="manifest" style="display:none"><h2>Manifest</h2><div class="card"><button onclick="load('manifest')">Load Manifest</button><pre id="r-manifest"></pre></div></div>
  <div id="parityaudit" style="display:none"><h2>Parity Audit</h2><div class="card"><button onclick="load('parity-audit')">Run Audit</button><pre id="r-parity-audit"></pre></div></div>
  <div id="setupreport" style="display:none"><h2>Setup Report</h2><div class="card"><button onclick="load('setup-report')">Load Report</button><pre id="r-setup-report"></pre></div></div>
  <div id="commandgraph" style="display:none"><h2>Command Graph</h2><div class="card"><button onclick="load('command-graph')">Load Graph</button><pre id="r-command-graph"></pre></div></div>
  <div id="toolpool" style="display:none"><h2>Tool Pool</h2><div class="card"><button onclick="load('tool-pool')">Load Pool</button><pre id="r-tool-pool"></pre></div></div>
  <div id="bootstrapgraph" style="display:none"><h2>Bootstrap Graph</h2><div class="card"><button onclick="load('bootstrap-graph')">Load Graph</button><pre id="r-bootstrap-graph"></pre></div></div>

  <div id="subsystems" style="display:none">
    <h2>Subsystems</h2>
    <div class="card">
      <div class="input-row"><label>Limit</label><input id="sub-limit" type="number" value="32" style="max-width:80px"/><button onclick="loadSubsystems()">Load</button></div>
      <pre id="r-subsystems"></pre>
    </div>
  </div>

  <div id="commands" style="display:none">
    <h2>Commands</h2>
    <div class="card">
      <div class="input-row"><input id="cmd-query" placeholder="Search commands..." /><input id="cmd-limit" type="number" value="20" style="max-width:80px"/><button onclick="loadCommands()">Search</button></div>
      <div class="check-row">
        <label><input type="checkbox" id="cmd-no-plugin" /> No plugin commands</label>
        <label><input type="checkbox" id="cmd-no-skill" /> No skill commands</label>
      </div>
      <pre id="r-commands"></pre>
    </div>
  </div>

  <div id="tools" style="display:none">
    <h2>Tools</h2>
    <div class="card">
      <div class="input-row"><input id="tool-query" placeholder="Search tools..." /><input id="tool-limit" type="number" value="20" style="max-width:80px"/><button onclick="loadTools()">Search</button></div>
      <div class="check-row">
        <label><input type="checkbox" id="tool-simple" /> Simple mode</label>
        <label><input type="checkbox" id="tool-no-mcp" /> No MCP</label>
      </div>
      <pre id="r-tools"></pre>
    </div>
  </div>

  <div id="route" style="display:none">
    <h2>Route Prompt</h2>
    <div class="card">
      <div class="input-row"><input id="route-prompt" placeholder="Enter a prompt..." /><input id="route-limit" type="number" value="5" style="max-width:80px"/><button onclick="runRoute()">Route</button></div>
      <pre id="r-route"></pre>
    </div>
  </div>

  <div id="bootstrap" style="display:none">
    <h2>Bootstrap Session</h2>
    <div class="card">
      <div class="input-row"><input id="boot-prompt" placeholder="Enter a prompt..." /><input id="boot-limit" type="number" value="5" style="max-width:80px"/><button onclick="runBootstrap()">Bootstrap</button></div>
      <pre id="r-bootstrap"></pre>
    </div>
  </div>

  <div id="turnloop" style="display:none">
    <h2>Turn Loop</h2>
    <div class="card">
      <div class="input-row"><input id="turn-prompt" placeholder="Enter a prompt..." /></div>
      <div class="input-row">
        <div><label>Limit</label><input id="turn-limit" type="number" value="5" style="max-width:80px"/></div>
        <div><label>Max Turns</label><input id="turn-max" type="number" value="3" style="max-width:80px"/></div>
        <label style="align-self:flex-end"><input type="checkbox" id="turn-structured" /> Structured output</label>
        <button style="align-self:flex-end" onclick="runTurnLoop()">Run</button>
      </div>
      <pre id="r-turnloop"></pre>
    </div>
  </div>

  <div id="execcommand" style="display:none">
    <h2>Exec Command</h2>
    <div class="card">
      <div class="input-row"><input id="ec-name" placeholder="Command name..." /><input id="ec-prompt" placeholder="Prompt..." /><button onclick="runExecCommand()">Execute</button></div>
      <pre id="r-execcommand"></pre>
    </div>
  </div>

  <div id="exectool" style="display:none">
    <h2>Exec Tool</h2>
    <div class="card">
      <div class="input-row"><input id="et-name" placeholder="Tool name..." /><input id="et-payload" placeholder="Payload..." /><button onclick="runExecTool()">Execute</button></div>
      <pre id="r-exectool"></pre>
    </div>
  </div>

  <div id="showcommand" style="display:none">
    <h2>Show Command</h2>
    <div class="card">
      <div class="input-row"><input id="sc-name" placeholder="Command name..." /><button onclick="runShowCommand()">Show</button></div>
      <pre id="r-showcommand"></pre>
    </div>
  </div>

  <div id="showtool" style="display:none">
    <h2>Show Tool</h2>
    <div class="card">
      <div class="input-row"><input id="st-name" placeholder="Tool name..." /><button onclick="runShowTool()">Show</button></div>
      <pre id="r-showtool"></pre>
    </div>
  </div>
</main>
</div>
<script>
let current = 'home';
function show(id) {
  document.getElementById(current).style.display = 'none';
  document.getElementById(id).style.display = 'block';
  current = id;
  document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
  event.target.classList.add('active');
}
async function api(path, body) {
  const opts = body ? { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body) } : {};
  const r = await fetch('/api/' + path, opts);
  return r.json();
}
function fmt(data) { return typeof data === 'string' ? data : JSON.stringify(data, null, 2); }
async function load(cmd) {
  const el = document.getElementById('r-' + cmd);
  el.textContent = 'Loading...';
  const data = await api(cmd);
  el.textContent = fmt(data.result || data);
}
async function loadSubsystems() {
  const el = document.getElementById('r-subsystems');
  el.textContent = 'Loading...';
  const data = await api('subsystems?limit=' + document.getElementById('sub-limit').value);
  el.textContent = fmt(data.result || data);
}
async function loadCommands() {
  const el = document.getElementById('r-commands');
  el.textContent = 'Loading...';
  const params = new URLSearchParams({ limit: document.getElementById('cmd-limit').value });
  const q = document.getElementById('cmd-query').value;
  if (q) params.set('query', q);
  if (document.getElementById('cmd-no-plugin').checked) params.set('no_plugin_commands', '1');
  if (document.getElementById('cmd-no-skill').checked) params.set('no_skill_commands', '1');
  const data = await api('commands?' + params);
  el.textContent = fmt(data.result || data);
}
async function loadTools() {
  const el = document.getElementById('r-tools');
  el.textContent = 'Loading...';
  const params = new URLSearchParams({ limit: document.getElementById('tool-limit').value });
  const q = document.getElementById('tool-query').value;
  if (q) params.set('query', q);
  if (document.getElementById('tool-simple').checked) params.set('simple_mode', '1');
  if (document.getElementById('tool-no-mcp').checked) params.set('no_mcp', '1');
  const data = await api('tools?' + params);
  el.textContent = fmt(data.result || data);
}
async function runRoute() {
  const el = document.getElementById('r-route');
  el.textContent = 'Routing...';
  const data = await api('route', { prompt: document.getElementById('route-prompt').value, limit: +document.getElementById('route-limit').value });
  el.textContent = fmt(data.result || data);
}
async function runBootstrap() {
  const el = document.getElementById('r-bootstrap');
  el.textContent = 'Bootstrapping...';
  const data = await api('bootstrap', { prompt: document.getElementById('boot-prompt').value, limit: +document.getElementById('boot-limit').value });
  el.textContent = fmt(data.result || data);
}
async function runTurnLoop() {
  const el = document.getElementById('r-turnloop');
  el.textContent = 'Running...';
  const data = await api('turn-loop', {
    prompt: document.getElementById('turn-prompt').value,
    limit: +document.getElementById('turn-limit').value,
    max_turns: +document.getElementById('turn-max').value,
    structured_output: document.getElementById('turn-structured').checked
  });
  el.textContent = fmt(data.result || data);
}
async function runExecCommand() {
  const el = document.getElementById('r-execcommand');
  el.textContent = 'Executing...';
  const data = await api('exec-command', { name: document.getElementById('ec-name').value, prompt: document.getElementById('ec-prompt').value });
  el.textContent = fmt(data.result || data);
}
async function runExecTool() {
  const el = document.getElementById('r-exectool');
  el.textContent = 'Executing...';
  const data = await api('exec-tool', { name: document.getElementById('et-name').value, payload: document.getElementById('et-payload').value });
  el.textContent = fmt(data.result || data);
}
async function runShowCommand() {
  const el = document.getElementById('r-showcommand');
  const data = await api('show-command?name=' + encodeURIComponent(document.getElementById('sc-name').value));
  el.textContent = fmt(data.result || data);
}
async function runShowTool() {
  const el = document.getElementById('r-showtool');
  const data = await api('show-tool?name=' + encodeURIComponent(document.getElementById('st-name').value));
  el.textContent = fmt(data.result || data);
}
async function quickRoute() {
  const el = document.getElementById('q-result');
  el.style.display = 'block';
  el.textContent = 'Routing...';
  const data = await api('route', { prompt: document.getElementById('q-route').value, limit: 5 });
  el.textContent = fmt(data.result || data);
}
async function loadStats() {
  const [cmds, tools, subs] = await Promise.all([api('commands?limit=1'), api('tools?limit=1'), api('subsystems?limit=1')]);
  document.getElementById('stats').innerHTML = `
    <div class="stat"><div class="num">${cmds.total ?? '—'}</div><div class="label">Commands</div></div>
    <div class="stat"><div class="num">${tools.total ?? '—'}</div><div class="label">Tools</div></div>
    <div class="stat"><div class="num">${subs.total ?? '—'}</div><div class="label">Subsystems</div></div>
  `;
}
loadStats();
</script>
</body>
</html>
"""


def _text(result) -> str:
    if hasattr(result, "as_markdown"):
        return result.as_markdown()
    if hasattr(result, "to_markdown"):
        return result.to_markdown()
    return str(result)


@app.route("/")
def dashboard():
    return render_template_string(DASHBOARD)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# ── Static GET endpoints ──────────────────────────────────────────────────────

@app.route("/api/summary")
def api_summary():
    from src.port_manifest import build_port_manifest
    from src.query_engine import QueryEnginePort
    manifest = build_port_manifest()
    return jsonify({"result": QueryEnginePort(manifest).render_summary()})


@app.route("/api/manifest")
def api_manifest():
    from src.port_manifest import build_port_manifest
    return jsonify({"result": _text(build_port_manifest())})


@app.route("/api/parity-audit")
def api_parity_audit():
    from src.parity_audit import run_parity_audit
    return jsonify({"result": _text(run_parity_audit())})


@app.route("/api/setup-report")
def api_setup_report():
    from src.setup import run_setup
    return jsonify({"result": _text(run_setup())})


@app.route("/api/command-graph")
def api_command_graph():
    from src.command_graph import build_command_graph
    return jsonify({"result": _text(build_command_graph())})


@app.route("/api/tool-pool")
def api_tool_pool():
    from src.tool_pool import assemble_tool_pool
    return jsonify({"result": _text(assemble_tool_pool())})


@app.route("/api/bootstrap-graph")
def api_bootstrap_graph():
    from src.bootstrap_graph import build_bootstrap_graph
    return jsonify({"result": _text(build_bootstrap_graph())})


# ── Parameterised GET endpoints ───────────────────────────────────────────────

@app.route("/api/subsystems")
def api_subsystems():
    from src.port_manifest import build_port_manifest
    limit = int(request.args.get("limit", 32))
    manifest = build_port_manifest()
    items = [{"name": s.name, "file_count": s.file_count, "notes": s.notes}
             for s in manifest.top_level_modules[:limit]]
    return jsonify({"result": items, "total": len(manifest.top_level_modules)})


@app.route("/api/commands")
def api_commands():
    from src.commands import get_commands, render_command_index
    limit = int(request.args.get("limit", 20))
    query = request.args.get("query")
    no_plugin = bool(request.args.get("no_plugin_commands"))
    no_skill = bool(request.args.get("no_skill_commands"))
    if query:
        return jsonify({"result": render_command_index(limit=limit, query=query)})
    commands = get_commands(include_plugin_commands=not no_plugin, include_skill_commands=not no_skill)
    items = [{"name": c.name, "source": c.source_hint} for c in commands[:limit]]
    return jsonify({"result": items, "total": len(commands)})


@app.route("/api/tools")
def api_tools():
    from src.tools import get_tools, render_tool_index
    from src.permissions import ToolPermissionContext
    limit = int(request.args.get("limit", 20))
    query = request.args.get("query")
    simple_mode = bool(request.args.get("simple_mode"))
    no_mcp = bool(request.args.get("no_mcp"))
    if query:
        return jsonify({"result": render_tool_index(limit=limit, query=query)})
    ctx = ToolPermissionContext.from_iterables([], [])
    tools = get_tools(simple_mode=simple_mode, include_mcp=not no_mcp, permission_context=ctx)
    items = [{"name": t.name, "source": t.source_hint} for t in tools[:limit]]
    return jsonify({"result": items, "total": len(tools)})


@app.route("/api/show-command")
def api_show_command():
    from src.commands import get_command
    name = request.args.get("name", "")
    module = get_command(name)
    if module is None:
        return jsonify({"error": f"Command not found: {name}"}), 404
    return jsonify({"result": {"name": module.name, "source": module.source_hint, "responsibility": module.responsibility}})


@app.route("/api/show-tool")
def api_show_tool():
    from src.tools import get_tool
    name = request.args.get("name", "")
    module = get_tool(name)
    if module is None:
        return jsonify({"error": f"Tool not found: {name}"}), 404
    return jsonify({"result": {"name": module.name, "source": module.source_hint, "responsibility": module.responsibility}})


# ── POST endpoints ────────────────────────────────────────────────────────────

@app.route("/api/route", methods=["POST"])
def api_route():
    from src.runtime import PortRuntime
    body = request.get_json(force=True)
    prompt = body.get("prompt", "")
    limit = int(body.get("limit", 5))
    matches = PortRuntime().route_prompt(prompt, limit=limit)
    items = [{"kind": m.kind, "name": m.name, "score": m.score, "source": m.source_hint} for m in matches]
    return jsonify({"result": items})


@app.route("/api/bootstrap", methods=["POST"])
def api_bootstrap():
    from src.runtime import PortRuntime
    body = request.get_json(force=True)
    prompt = body.get("prompt", "")
    limit = int(body.get("limit", 5))
    session = PortRuntime().bootstrap_session(prompt, limit=limit)
    return jsonify({"result": _text(session)})


@app.route("/api/turn-loop", methods=["POST"])
def api_turn_loop():
    from src.runtime import PortRuntime
    body = request.get_json(force=True)
    prompt = body.get("prompt", "")
    limit = int(body.get("limit", 5))
    max_turns = int(body.get("max_turns", 3))
    structured = bool(body.get("structured_output", False))
    results = PortRuntime().run_turn_loop(prompt, limit=limit, max_turns=max_turns, structured_output=structured)
    turns = [{"turn": i + 1, "output": r.output, "stop_reason": r.stop_reason} for i, r in enumerate(results)]
    return jsonify({"result": turns})


@app.route("/api/exec-command", methods=["POST"])
def api_exec_command():
    from src.commands import execute_command
    body = request.get_json(force=True)
    result = execute_command(body.get("name", ""), body.get("prompt", ""))
    return jsonify({"result": result.message, "handled": result.handled})


@app.route("/api/exec-tool", methods=["POST"])
def api_exec_tool():
    from src.tools import execute_tool
    body = request.get_json(force=True)
    result = execute_tool(body.get("name", ""), body.get("payload", ""))
    return jsonify({"result": result.message, "handled": result.handled})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
