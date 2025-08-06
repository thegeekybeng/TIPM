import pytest
import gradio as gr
from hf_deployment_package.app_gradio import create_app

# python


def test_create_app_returns_blocks():
    """Test that create_app returns a Gradio Blocks instance."""
    app = create_app()
    assert isinstance(app, gr.Blocks)

def test_app_contains_expected_components():
    """Test that the app contains Markdown, Textbox, and Button components."""
    app = create_app()
    # Gradio Blocks stores components in .children
    component_types = [type(child) for child in app.children]
    assert any(issubclass(t, gr.Markdown) for t in component_types)
    assert any(issubclass(t, gr.Textbox) for t in component_types)
    assert any(issubclass(t, gr.Button) for t in component_types)

def test_analyze_country_known(monkeypatch):
    """Test analyze_country logic for a known country."""
    app = create_app()
    # Find the analyze function by inspecting the click event
    analyze_fn = None
    for child in app.children:
        if isinstance(child, gr.Button):
            if child.click_events:
                analyze_fn = child.click_events[0].fn
                break
    assert analyze_fn is not None
    result = analyze_fn("Argentina")
    assert "Country: Argentina" in result
    assert "Tariff Rate:" in result
    assert "Continent:" in result

def test_analyze_country_unknown(monkeypatch):
    """Test analyze_country logic for an unknown country."""
    app = create_app()
    analyze_fn = None
    for child in app.children:
        if isinstance(child, gr.Button):
            if child.click_events:
                analyze_fn = child.click_events[0].fn
                break
    assert analyze_fn is not None
    result = analyze_fn("Atlantis")
    assert result == "Country not found in database."