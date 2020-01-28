#encoding=utf-8
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MODEPASSALL = 1
MODEMATCHONCE = 2

class DefaultRulesEngine(object):
    def __init__(self, mode=MODEPASSALL):
        """
        :param mode: "pass_all", "match_once"
        """
        self.mode=mode

    def fire(self, rules, facts):
        matched_times = 0
        for rule in rules.rules_list:
            logger.debug("rule {name} triggered".format(
                name=rule.name
            ))
            condition_result = rule.condition(**facts.facts_dict)
            logger.debug("rule {name} condition test result: {result}".format(
                name=rule.name,
                result=bool(condition_result)
            ))
            if condition_result:
                matched_times += 1
                if self.mode == MODEMATCHONCE and matched_times >= 2:
                    break
                for action in rule.get_actions():
                    action(**facts.facts_dict)


class Facts(object):
    def __init__(self):
        self.facts_dict = dict()

    def put(self, key, value):
        self.facts_dict[key] = value


class Rule(object):

    def __init__(self):
        self.name = "rule"
        self.description = "description"
        self.priority = sys.maxint - 1
        self._actions = list()

    def condition(self, **kwargs):
        return False

    def action(self, **kwargs):
        return True

    def add_action(self, action):
        assert callable(action)
        if not hasattr(self, "_action"):
            self._actions = list()
        else:
            self._actions.append(action)

    def get_actions(self):
        if not hasattr(self, "_action"):
            res = list()
        else:
            res = self._actions
        for method in dir(self):
            if callable(getattr(self, method)) and method.startswith("action_"):
                res.append(getattr(self, method))
        return res


class Rules(object):
    def __init__(self):
        self.rules_list = list()

    def register(self, rule):
        assert isinstance(rule, Rule)
        self.rules_list.append(rule)
        self.rules_list.sort(key=lambda x: x.priority)
