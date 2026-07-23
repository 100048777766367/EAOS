"""Unit test suite for EAOS execution engine subsystems."""

from engine.compiler.policy_code_compiler import PolicyCodeCompiler
from engine.executor.task_executor import AsyncTaskExecutor, ExecutionTaskDTO
from engine.generator.code_generator import CodeGeneratorEngine, GenerationSpecDTO
from engine.indexer.knowledge_indexer import KnowledgeIndexerEngine
from engine.parser.specification_parser import SpecificationParserEngine
from engine.scheduler.cybernetic_scheduler import CyberneticLoopScheduler
from engine.validator.rule_validator import RuleValidatorEngine
from engine.workflow.state_machine import FSMWorkflowEngine


def test_policy_compiler_engine() -> None:
    compiler = PolicyCodeCompiler()
    res = compiler.compile_policy_spec("P01", [{"expression": "amount > 0"}])
    assert res.policy_id == "P01"
    assert "def validate_payload" in res.executable_code


def test_async_task_executor() -> None:
    executor = AsyncTaskExecutor()
    task = ExecutionTaskDTO(task_id="T01", command="run", payload={})
    res = executor.execute_task(task)
    assert res.success is True
    assert res.execution_time_ms >= 0.0


def test_code_generator_engine() -> None:
    generator = CodeGeneratorEngine()
    spec = GenerationSpecDTO(target_module="finance", specification="Invoice Spec")
    artifact = generator.generate_module(spec)
    assert artifact.artifact_id.startswith("gen_")
    assert "Auto-generated" in artifact.content


def test_knowledge_indexer_engine() -> None:
    indexer = KnowledgeIndexerEngine()
    report = indexer.index_document("DOC-1", "Constitution", ["core"])
    assert report.total_indexed == 1


def test_specification_parser_engine() -> None:
    parser = SpecificationParserEngine()
    parsed = parser.parse_raw_dict({"id": "spec.inv", "name": "Invoice", "rules": [{"id": "R1"}]})
    assert parsed.spec_id == "spec.inv"
    assert len(parsed.rules) == 1


def test_cybernetic_scheduler_engine() -> None:
    scheduler = CyberneticLoopScheduler()
    report = scheduler.register_loop_job("FAST", "uv run task lint")
    assert report.active_jobs == 1


def test_rule_validator_engine() -> None:
    validator = RuleValidatorEngine()
    report = validator.validate_payload("S1", [{"id": "R1"}], {"val": 10})
    assert report.overall_passed is True


def test_fsm_workflow_engine() -> None:
    fsm = FSMWorkflowEngine()
    state = fsm.transition_state("INST-1", "DRAFT", "rescue_stuck")
    assert state.stuck_rescued is True
    assert state.current_state == "RESCUED"
