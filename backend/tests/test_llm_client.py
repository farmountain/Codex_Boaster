import backend.llm_client as llm
import httpx


def test_call_ollama(monkeypatch):
    called = {}

    def fake_post(url, json=None, timeout=None, headers=None):
        called['url'] = url
        called['json'] = json
        called['headers'] = headers
        class R:
            def raise_for_status(self):
                pass
            def json(self):
                return {'response': 'ok'}
        return R()

    monkeypatch.setenv('OLLAMA_URL', 'http://ollama')
    monkeypatch.setenv('OLLAMA_MODEL', 'tiny')
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    monkeypatch.setattr(httpx, 'post', fake_post)

    out = llm.call_ollama_or_openai('ping')
    assert out == 'ok'
    assert called['url'] == 'http://ollama/api/generate'
    assert called['json'] == {'model': 'tiny', 'prompt': 'ping'}


def test_call_openai(monkeypatch):
    called = {}

    def fake_post(url, json=None, timeout=None, headers=None):
        called['url'] = url
        called['json'] = json
        called['headers'] = headers
        class R:
            def raise_for_status(self):
                pass
            def json(self):
                return {'choices': [{'message': {'content': 'hi'}}]}
        return R()

    monkeypatch.delenv('OLLAMA_URL', raising=False)
    monkeypatch.setenv('OPENAI_API_KEY', 'k')
    monkeypatch.setenv('OPENAI_MODEL', 'gpt-x')
    monkeypatch.setattr(httpx, 'post', fake_post)

    out = llm.call_ollama_or_openai('hello')
    assert out == 'hi'
    assert called['url'] == 'https://api.openai.com/v1/chat/completions'
    assert called['headers']['Authorization'] == 'Bearer k'
    assert called['json']['model'] == 'gpt-x'


def test_call_fallback(monkeypatch):
    monkeypatch.delenv('OLLAMA_URL', raising=False)
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)

    out = llm.call_ollama_or_openai('whatever')
    assert out.startswith('# generated code')
