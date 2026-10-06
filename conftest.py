from pathlib import Path
import allure
import pytest

from config import Config
from pages.practice_form_page import PracticeFormPage

SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"


@pytest.fixture(scope="session")
def config():
    return Config()


@pytest.fixture(scope="session")
def browser_name():
    return "chromium"


@pytest.fixture
def practice_form_page(page, config):
    return PracticeFormPage(page, config)


@pytest.fixture
def create_temp_file(tmp_path):
    def _create(filename: str) -> str:
        file_path = tmp_path / filename
        file_path.write_bytes(b"\x00" * 1024)
        return str(file_path)

    return _create


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = None
        if "practice_form_page" in item.funcargs:
            page = item.funcargs["practice_form_page"].page
        elif "page" in item.funcargs:
            page = item.funcargs["page"]

        if page:
            try:
                screenshot = page.screenshot(full_page=True)

                # 1. Прикріплення до звіту Allure
                allure.attach(
                    screenshot,
                    name=f"failure_{item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )

                # 2. Збереження окремим файлом у папку screenshots/
                SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
                safe_name = "".join(
                    c if c.isalnum() or c in "._-[]" else "_" for c in item.name
                )
                (SCREENSHOTS_DIR / f"{safe_name}.png").write_bytes(screenshot)
            except Exception:
                pass
