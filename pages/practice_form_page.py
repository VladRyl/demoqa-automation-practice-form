from pathlib import Path
from enum import Enum

from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage
from pages.enums import Gender, Hobby, ValidationState


class PracticeFormPage(BasePage):
    def __init__(self, page: Page, config):
        super().__init__(page)
        self.config = config
        self._main_header = page.locator(".container.playgound-body h1")
        self._student_registration_form = page.locator(".container.playgound-body h5")
        self._input_first_name = page.locator("#firstName")
        self._input_last_name = page.locator("#lastName")
        self._input_user_email = page.locator("#userEmail")
        self._gender_wrapper = page.locator("#genterWrapper")
        self._mobile_number = page.locator("#userNumber")
        self._date = page.locator("#dateOfBirthInput")
        self._subjects = page.locator("#subjectsInput")
        self._hobbies_wrapper = page.locator("#hobbiesWrapper")
        self._upload_picture_input = page.locator("#uploadPicture")
        self._current_address = page.locator("#currentAddress")
        self._state_select = page.locator("#state")
        self._city_select = page.locator("#city")
        self._submit = page.locator("#submit")
        self._modal_content = page.locator(".modal-content")
        self._modal_title = self._modal_content.locator("#example-modal-sizes-title-lg")
        self._modal_table = self._modal_content.locator("table")
        self._close_modal_btn = self._modal_content.locator("#closeLargeModal")

    def open(self):
        self.open_url(self.config.PRACTICE_FORM_URL)
        expect(self._main_header).to_be_visible()

    def verify_page_loaded(self):
        expect(self._main_header).to_have_text("Practice Form")

    def verify_student_registration_form_visible(self):
        expect(self._student_registration_form).to_be_visible()
        expect(self._student_registration_form).to_have_text(
            "Student Registration Form"
        )

    def fill_first_name(self, first_name: str):
        self._input_first_name.fill(first_name)

    def fill_last_name(self, last_name: str):
        self._input_last_name.fill(last_name)

    def fill_email(self, email: str):
        self._input_user_email.fill(email)

    def select_gender(self, gender: Gender):
        gender_label = self._gender_wrapper.get_by_text(gender.value, exact=True)
        gender_label.click()

    def fill_mobile_number(self, mobile_number: str):
        self._mobile_number.fill(mobile_number)

    def fill_date_of_birth(self, date_of_birth: str):
        self._date.click()
        self._date.fill(date_of_birth)
        self._date.press("Enter")

    def fill_date_via_picker(self, day: str, month: str, year: str):
        self._date.click()
        self.page.locator(".react-datepicker__month-select").select_option(label=month)
        self.page.locator(".react-datepicker__year-select").select_option(value=year)
        day_code = f"{int(day):03d}"
        day_locator = self.page.locator(
            f".react-datepicker__day--{day_code}:not(.react-datepicker__day--outside-month)"
        )
        day_locator.click()

    def fill_subjects(self, subjects: list[str]):
        first_option = self.page.locator(".subjects-auto-complete__option").first
        for subject in subjects:
            self._subjects.fill(subject)
            try:
                first_option.wait_for(state="visible", timeout=2000)
                first_option.click()
            except Exception:
                self._subjects.press("Escape")

    def remove_subject(self, subject: str):
        badge_remove_btn = self.page.locator(
            f".subjects-auto-complete__multi-value:has-text('{subject}') .subjects-auto-complete__multi-value__remove"
        )
        badge_remove_btn.click()

    def verify_selected_subjects(self, expected_subjects: list[str]):
        actual_badges = self.page.locator(
            ".subjects-auto-complete__multi-value__label"
        ).all_text_contents()
        assert actual_badges == expected_subjects

    def verify_no_subjects_selected(self):
        expect(self.page.locator(".subjects-auto-complete__multi-value")).to_have_count(
            0
        )

    def select_hobbies(self, hobbies: list[Hobby]):
        for hobby in hobbies:
            hobby_label = self._hobbies_wrapper.get_by_text(hobby.value, exact=True)
            hobby_label.click()

    def verify_hobbies_checked(self, hobbies: list[Hobby | str]):
        all_hobbies = [Hobby.SPORTS, Hobby.READING, Hobby.MUSIC]
        expected_values = [h.value if isinstance(h, Enum) else h for h in hobbies]

        for hobby in all_hobbies:
            checkbox = self._hobbies_wrapper.locator(
                f"input[type='checkbox'][value='{self._get_hobby_value(hobby.value)}']"
            )
            if hobby.value in expected_values:
                expect(checkbox).to_be_checked()
            else:
                expect(checkbox).not_to_be_checked()

    def _get_hobby_value(self, hobby_name: str) -> str:
        mapping = {"Sports": "1", "Reading": "2", "Music": "3"}
        return mapping.get(hobby_name, hobby_name)

    def upload_picture(self, file_path: str | Path):
        self._upload_picture_input.set_input_files(file_path)

    def fill_current_address(self, current_address: str):
        self._current_address.fill(current_address)

    def select_state(self, state_name: str):
        self._state_select.click()
        option = self.page.get_by_text(state_name, exact=True)
        option.click()

    def select_city(self, city_name: str):
        self.verify_city_is_enabled()
        self._city_select.click()
        option = self.page.get_by_text(city_name, exact=True)
        option.click()

    def verify_city_is_disabled(self):
        expect(self._city_select.locator("input")).to_be_disabled()

    def verify_city_is_enabled(self):
        expect(self._city_select.locator("input")).to_be_enabled()

    def get_selected_city_text(self) -> str:
        text = self._city_select.locator("[class*='singleValue']").text_content()
        return text or ""

    def verify_city_is_reset(self):
        selected_text = self.get_selected_city_text()
        assert selected_text in ["", "Select City"]

    def submit(self):
        self._submit.click()

    def verify_modal_visible(self):
        expect(self._modal_content).to_be_visible()
        expect(self._modal_title).to_have_text("Thanks for submitting the form")

    def get_modal_value_by_label(self, label: str) -> str:
        row_value = self._modal_table.locator(
            f"tr:has(td:nth-child(1):has-text('{label}')) td:nth-child(2)"
        )
        row_value.wait_for(state="visible")
        text = row_value.text_content()
        return text.strip() if text else ""

    def close_modal(self):
        self._close_modal_btn.click()
        expect(self._modal_content).not_to_be_visible()

    def verify_field_color(
        self,
        locators: Locator | list[Locator],
        state: ValidationState = ValidationState.INVALID,
    ):
        if isinstance(locators, Locator):
            locators = [locators]

        for locator in locators:
            check_labels = locator.locator(".form-check-label")
            if check_labels.count() > 0:
                expect(check_labels.first).to_have_css("color", state.value)
            else:
                expect(locator).to_have_css("border-color", state.value)

    def verify_gender_is_checked(self, gender: Gender | str):
        val = gender.value if isinstance(gender, Enum) else gender
        radio_input = self._gender_wrapper.locator(f"input[value='{val}']")
        expect(radio_input).to_be_checked()

    def verify_gender_is_not_checked(self, gender: Gender | str):
        val = gender.value if isinstance(gender, Enum) else gender
        radio_input = self._gender_wrapper.locator(f"input[value='{val}']")
        expect(radio_input).not_to_be_checked()

    def verify_only_one_gender_checked(self, selected_gender: Gender | str):
        all_genders = [g for g in Gender]
        selected_enum = (
            selected_gender
            if isinstance(selected_gender, Gender)
            else Gender(selected_gender)
        )

        for gender in all_genders:
            if gender == selected_enum:
                self.verify_gender_is_checked(gender)
            else:
                self.verify_gender_is_not_checked(gender)
