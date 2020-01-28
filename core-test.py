import logging
from core import Rule, Rules, DefaultRulesEngine, Facts, MODEPASSALL

logger = logging.getLogger(__name__)


class TestRule(Rule):

    def __init__(self):
        self.name = "test rule"
        self.priority = 1

    def condition(self, **kwargs):
        if 'a' in kwargs and kwargs['a'] > self.priority:
            return True

    def action_a(self, **kwargs):
        logger.info("<%s> action executed, facts: %s", self.name, kwargs)


class TestRule2(TestRule):

    def __init__(self):
        self.name = "test rule 2"
        self.priority = 2


class TestRule3(TestRule):

    def __init__(self):
        self.name = "test rule 3"
        self.priority = 3


if __name__ == '__main__':
    rules = Rules()
    rules.register(TestRule())
    rules.register(TestRule3())
    rules.register(TestRule2())

    facts = Facts()
    facts.put("a", 3)
    engine = DefaultRulesEngine(mode=MODEPASSALL)
    engine.fire(rules, facts)
