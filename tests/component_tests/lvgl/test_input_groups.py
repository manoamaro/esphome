"""Regression tests for shared encoder/keypad groups and group switching."""

from pathlib import Path

import pytest

from esphome.__main__ import generate_cpp_contents
from esphome.config import read_config
from esphome.core import CORE


@pytest.fixture
def main_cpp() -> str:
    CORE.config_path = Path(__file__).parent / "config" / "input_groups_test.yaml"
    CORE.config = read_config({})
    assert CORE.config is not None
    generate_cpp_contents(CORE.config)
    return CORE.cpp_main_section


def test_inputs_reuse_declared_groups(main_cpp: str) -> None:
    assert main_cpp.count("shared_group = lv_group_create();") == 1
    assert main_cpp.count("other_group = lv_group_create();") == 1
    for listener in ("test_encoder", "test_keypad"):
        assert f"lv_indev_set_group({listener}->get_drv(), shared_group);" in main_cpp
    assert "lv_indev_set_group(default_keypad->get_drv(), lv_group_t_id);" in main_cpp


def test_both_inputs_can_switch_groups(main_cpp: str) -> None:
    for listener in ("test_encoder", "test_keypad"):
        assert f"lv_indev_set_group({listener}->get_drv(), other_group);" in main_cpp
    assert main_cpp.count("lv_group_focus_obj(first_button);") == 2
