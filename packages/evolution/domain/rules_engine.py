from abc import ABC, abstractmethod

from pydantic import BaseModel

from packages.evolution.domain.models import EvolutionObject


class RuleResult(BaseModel):
    """Káº¿t quáº£ kiá»ƒm thá»­ cá»§a má»™t luáº­t cá»¥ thá»ƒ."""

    rule_name: str
    passed: bool
    message: str


class Rule(ABC):
    """Lá»›p trá»«u tÆ°á»£ng cho má»i quy táº¯c kiáº¿n trÃºc cáº¥p cao."""

    @abstractmethod
    def evaluate(self, obj: EvolutionObject) -> RuleResult: ...


class VersionHeaderRule(Rule):
    """Quy táº¯c báº¯t buá»™c má»i cáº¥u hÃ¬nh tiáº¿n hÃ³a pháº£i cÃ³ sá»‘ phiÃªn báº£n."""

    def evaluate(self, obj: EvolutionObject) -> RuleResult:
        version = obj.payload.get("__version")
        if version is None:
            return RuleResult(
                rule_name="VersionHeaderRule",
                passed=False,
                message="KhÃ³a '__version' bá»‹ thiáº¿u trong payload cáº¥u hÃ¬nh.",
            )
        return RuleResult(
            rule_name="VersionHeaderRule",
            passed=True,
            message=f"KhÃ³a '__version' há»£p chuáº©n, giÃ¡ trá»‹: {version}.",
        )


class CriticalityEnvironmentRule(Rule):
    """MÃ´i trÆ°á»ng production báº¯t buá»™c Ä‘á»™ nghiÃªm trá»ng pháº£i lÃ  high."""

    def evaluate(self, obj: EvolutionObject) -> RuleResult:
        env = obj.metadata.environment
        crit = obj.metadata.criticality
        if env == "production" and crit != "high":
            return RuleResult(
                rule_name="CriticalityEnvironmentRule",
                passed=False,
                message="MÃ´i trÆ°á»ng production yÃªu cáº§u criticality='high'.",
            )
        return RuleResult(
            rule_name="CriticalityEnvironmentRule",
            passed=True,
            message="Má»©c Ä‘á»™ nghiÃªm trá»ng phÃ¹ há»£p vá»›i mÃ´i trÆ°á»ng sáº£n xuáº¥t.",
        )


class PolicyEngine:
    """Äá»™ng cÆ¡ gom cÃ¡c luáº­t (Rules) thÃ nh cÃ¡c ChÃ­nh sÃ¡ch lá»›n (Policies)."""

    def __init__(self, name: str, rules: list[Rule]) -> None:
        self.name = name
        self.rules = rules

    def evaluate_policy(self, obj: EvolutionObject) -> tuple[bool, list[RuleResult]]:
        passed = True
        results = []
        for rule in self.rules:
            res = rule.evaluate(obj)
            results.append(res)
            if not res.passed:
                passed = False
        return passed, results


class FitnessEngine:
    """Äá»™ng cÆ¡ phÃ¢n tÃ­ch Ä‘iá»ƒm thá»ƒ lá»±c kiáº¿n trÃºc tá»« cÃ¡c báº±ng chá»©ng (Evidence)."""

    @staticmethod
    def calculate_fitness(obj: EvolutionObject) -> float:
        if not obj.evidences:
            return 0.0
        passed_evidences = [ev for ev in obj.evidences if ev.passed]
        return len(passed_evidences) / len(obj.evidences)
