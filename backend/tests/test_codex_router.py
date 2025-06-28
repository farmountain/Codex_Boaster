from backend.codex_router import route_prompt_to_agent


def test_route_plan():
    _, info = route_prompt_to_agent('plan a project')
    assert info["agent"] == 'ArchitectAgent'


def test_route_test():
    _, info = route_prompt_to_agent('generate tests')
    assert info["agent"] == 'TestSuiteAgent'


def test_route_fix():
    _, info = route_prompt_to_agent('fix this bug')
    assert info["agent"] == 'ReflexionAgent'


def test_route_fallback():
    _, info = route_prompt_to_agent('hello there')
    assert info["agent"] == 'ChatAgent'
