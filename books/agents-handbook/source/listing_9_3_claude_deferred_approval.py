"""Source-contract-checked durable-approval integration design for Listing 9.3.

Source-contract checked against claude-agent-sdk 0.2.128; application services are placeholders. Not a runtime-proven exact-resumption guarantee; requires a credentialed provider integration test.
"""
from __future__ import annotations
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, HookMatcher, ResultMessage

async def pre_tool_gate(hook_input, tool_use_id, _hook_context):
    request = canonicalise_tool_request(hook_input["tool_name"], hook_input["tool_input"])
    authority = effective_authority()
    decision = policy_service.evaluate(request, authority)
    approval = approval_store.find_fresh_approval(task_id=current_task_id(), action_hash=request.action_hash, policy_version=policy_service.version, authority_digest=authority.digest)
    audit.record_pre_tool(tool_use_id, request, decision, approval)
    if decision.effect == "deny":
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": decision.reason}}
    if decision.effect == "approval_required" and approval is None:
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "defer", "permissionDecisionReason": decision.reason, "updatedInput": request.arguments}}
    revalidate_policy_authority_and_toctou(request, approval, authority)
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow", "updatedInput": request.arguments}}

async def post_tool_evidence(hook_input, tool_use_id, _hook_context):
    evidence_store.capture(tool_use_id=tool_use_id, tool_name=hook_input["tool_name"], tool_input=hook_input["tool_input"], tool_response=hook_input["tool_response"])
    return {}

def build_options(*, resume_session_id=None):
    return ClaudeAgentOptions(tools=["ReadTicket", "InspectUI", "ProposeFinding"], hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[pre_tool_gate])], "PostToolUse": [HookMatcher(matcher=None, hooks=[post_tool_evidence])]}, permission_mode="default", setting_sources=[], resume=resume_session_id)

async def run_until_completion_or_defer(prompt, *, resume_session_id=None):
    terminal = None
    async with ClaudeSDKClient(options=build_options(resume_session_id=resume_session_id)) as client:
        await client.query(prompt)
        async for message in client.receive_response():
            event_store.append(current_task_id(), message)
            if isinstance(message, ResultMessage): terminal = message
    if terminal is None: raise RuntimeError("missing terminal ResultMessage")
    pending = terminal.deferred_tool_use
    if pending is None: return terminal
    request = canonicalise_tool_request(pending.name, pending.input)
    record = approval_store.create_request(task_id=current_task_id(), session_id=terminal.session_id, tool_use_id=pending.id, tool_name=pending.name, canonical_arguments=request.arguments, action_hash=request.action_hash, policy_version=policy_service.version, authority_digest=effective_authority().digest, expires_at=clock.now() + APPROVAL_TTL)
    durable_workflow.suspend(current_task_id(), record.id)
    return record

async def resume_approved_deferred_call(approval_request_id):
    record = approval_store.require_approved(approval_request_id)
    revalidate_record_freshness_and_authority(record)
    return await run_until_completion_or_defer("Continue the deferred operation using the recorded approval.", resume_session_id=record.session_id)
