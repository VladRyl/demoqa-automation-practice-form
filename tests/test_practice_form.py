from pathlib import Path
from playwright.sync_api import expect

import pytest

from data.name_data import INVALID_NAMES, VALID_NAMES
from data.email_data import INVALID_EMAILS, VALID_EMAILS
from data.phone_data import INVALID_PHONES, VALID_PHONES
from data.file_data import VALID_FILE_NAMES, INVALID_FILE_NAMES
from data.date_data import DATE_PICKER_CASES
from data.state_city_data import STATE_CITY_MAP
from pages.enums import Gender, Hobby, ValidationState


class TestPracticeForm:
    @pytest.mark.order(1)
    @pytest.mark.dependency(name="open_form")
    def test_open_practice_form(self, practice_form_page):
        practice_form_page.open()
        practice_form_page.verify_page_loaded()

    @pytest.mark.dependency(depends=["open_form"])
    def test_all_forms_filled_correctly(self, practice_form_page):
        practice_form_page.open()
        practice_form_page.verify_student_registration_form_visible()
        practice_form_page.fill_first_name("User")
        practice_form_page.fill_last_name("Test")
        practice_form_page.fill_email("test.email@test.com")
        practice_form_page.select_gender(Gender.MALE)
        practice_form_page.fill_mobile_number("1234567890")
        practice_form_page.fill_date_of_birth("01 Jan 1990")
        practice_form_page.fill_subjects(["Maths", "Computer"])
        practice_form_page.select_hobbies([Hobby.SPORTS, Hobby.READING, Hobby.MUSIC])
        practice_form_page.upload_picture(
            Path(__file__).parent.parent / "assets" / "manul.jpg"
        )
        practice_form_page.fill_current_address("Street")
        practice_form_page.select_state("NCR")
        practice_form_page.select_city("Delhi")
        practice_form_page.submit()
        practice_form_page.verify_modal_visible()
        assert (
            practice_form_page.get_modal_value_by_label("Student Name") == "User Test"
        )
        assert (
            practice_form_page.get_modal_value_by_label("Student Email")
            == "test.email@test.com"
        )
        assert practice_form_page.get_modal_value_by_label("Gender") == "Male"
        assert practice_form_page.get_modal_value_by_label("Mobile") == "1234567890"
        assert (
            practice_form_page.get_modal_value_by_label("Date of Birth")
            == "01 January,1990"
        )
        assert (
            practice_form_page.get_modal_value_by_label("Subjects")
            == "Maths, Computer Science"
        )
        assert (
            practice_form_page.get_modal_value_by_label("Hobbies")
            == "Sports, Reading, Music"
        )
        assert practice_form_page.get_modal_value_by_label("Picture") == "manul.jpg"
        assert practice_form_page.get_modal_value_by_label("Address") == "Street"
        assert (
            practice_form_page.get_modal_value_by_label("State and City") == "NCR Delhi"
        )
        practice_form_page.close_modal()

    @pytest.mark.dependency(depends=["open_form"])
    def test_mandatory_filled_correctly(self, practice_form_page):
        practice_form_page.open()
        practice_form_page.fill_first_name("User")
        practice_form_page.fill_last_name("Test")
        practice_form_page.select_gender(Gender.FEMALE)
        practice_form_page.fill_mobile_number("1234567890")
        practice_form_page.fill_date_of_birth("01 Jan 1990")
        practice_form_page.submit()
        practice_form_page.verify_modal_visible()
        assert (
            practice_form_page.get_modal_value_by_label("Student Name") == "User Test"
        )
        assert practice_form_page.get_modal_value_by_label("Student Email") == ""
        assert practice_form_page.get_modal_value_by_label("Gender") == "Female"
        assert practice_form_page.get_modal_value_by_label("Mobile") == "1234567890"
        assert (
            practice_form_page.get_modal_value_by_label("Date of Birth")
            == "01 January,1990"
        )
        assert practice_form_page.get_modal_value_by_label("Subjects") == ""
        assert practice_form_page.get_modal_value_by_label("Hobbies") == ""
        assert practice_form_page.get_modal_value_by_label("Picture") == ""
        assert practice_form_page.get_modal_value_by_label("Address") == ""
        assert practice_form_page.get_modal_value_by_label("State and City") == ""

    @pytest.mark.dependency(depends=["open_form"])
    def test_empty_all_fields(self, practice_form_page):
        required_fields = [
            practice_form_page._input_first_name,
            practice_form_page._input_last_name,
            practice_form_page._gender_wrapper,
            practice_form_page._mobile_number,
        ]
        non_required_fields = [
            practice_form_page._input_user_email,
            practice_form_page._date,
            practice_form_page._subjects,
            practice_form_page._hobbies_wrapper,
            practice_form_page._upload_picture_input,
            practice_form_page._current_address,
            practice_form_page._state_select,
            practice_form_page._city_select,
        ]
        practice_form_page.open()
        practice_form_page.submit()
        practice_form_page.verify_field_color(required_fields, ValidationState.INVALID)
        practice_form_page.verify_field_color(
            non_required_fields, ValidationState.VALID
        )

    @pytest.mark.dependency(depends=["open_form"])
    def test_change_color(self, practice_form_page):
        required_fields = [
            practice_form_page._input_first_name,
            practice_form_page._input_last_name,
            practice_form_page._gender_wrapper,
            practice_form_page._mobile_number,
        ]
        practice_form_page.open()
        practice_form_page.submit()
        practice_form_page.verify_field_color(required_fields, ValidationState.INVALID)
        practice_form_page.fill_first_name("User")
        practice_form_page.fill_last_name("Test")
        practice_form_page.select_gender(Gender.OTHER)
        practice_form_page.fill_mobile_number("1234567890")
        practice_form_page.verify_field_color(required_fields, ValidationState.VALID)
        practice_form_page.fill_date_of_birth("01 Jan 1990")
        practice_form_page.submit()
        practice_form_page.verify_modal_visible()
        assert (
            practice_form_page.get_modal_value_by_label("Student Name") == "User Test"
        )
        assert practice_form_page.get_modal_value_by_label("Student Email") == ""
        assert practice_form_page.get_modal_value_by_label("Gender") == "Other"
        assert practice_form_page.get_modal_value_by_label("Mobile") == "1234567890"
        assert (
            practice_form_page.get_modal_value_by_label("Date of Birth")
            == "01 January,1990"
        )
        assert practice_form_page.get_modal_value_by_label("Subjects") == ""
        assert practice_form_page.get_modal_value_by_label("Hobbies") == ""
        assert practice_form_page.get_modal_value_by_label("Picture") == ""
        assert practice_form_page.get_modal_value_by_label("Address") == ""
        assert practice_form_page.get_modal_value_by_label("State and City") == ""

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("valid_name", VALID_NAMES)
    def test_valid_name_regex(self, practice_form_page, valid_name):
        practice_form_page.open()
        practice_form_page.fill_first_name(valid_name[0])
        practice_form_page.fill_last_name(valid_name[1])
        practice_form_page.submit()
        practice_form_page.verify_field_color(
            practice_form_page._input_first_name, ValidationState.VALID
        )
        practice_form_page.verify_field_color(
            practice_form_page._input_last_name, ValidationState.VALID
        )

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("invalid_name", INVALID_NAMES)
    def test_invalid_name_regex(self, practice_form_page, invalid_name):
        practice_form_page.open()
        practice_form_page.fill_first_name(invalid_name[0])
        practice_form_page.fill_last_name(invalid_name[1])
        practice_form_page.submit()
        practice_form_page.verify_field_color(
            practice_form_page._input_first_name, ValidationState.INVALID
        )
        practice_form_page.verify_field_color(
            practice_form_page._input_last_name, ValidationState.INVALID
        )

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("valid_email", VALID_EMAILS)
    def test_valid_email_regex(self, practice_form_page, valid_email):
        practice_form_page.open()
        practice_form_page.fill_email(valid_email)
        practice_form_page.submit()
        practice_form_page.verify_field_color(
            practice_form_page._input_user_email, ValidationState.VALID
        )

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("invalid_email", INVALID_EMAILS)
    def test_invalid_email_regex(self, practice_form_page, invalid_email):
        practice_form_page.open()
        practice_form_page.fill_email(invalid_email)
        practice_form_page.submit()
        practice_form_page.verify_field_color(
            practice_form_page._input_user_email, ValidationState.INVALID
        )

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("gender", [Gender.MALE, Gender.FEMALE, Gender.OTHER])
    def test_gender_switch(self, practice_form_page, gender):
        practice_form_page.open()
        practice_form_page.select_gender(gender)
        practice_form_page.verify_only_one_gender_checked(gender)

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("valid_phone", VALID_PHONES)
    def test_valid_phone_number(self, practice_form_page, valid_phone):
        practice_form_page.open()
        practice_form_page.fill_mobile_number(valid_phone)
        practice_form_page.submit()
        practice_form_page.verify_field_color(
            practice_form_page._mobile_number, ValidationState.VALID
        )

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("invalid_phone", INVALID_PHONES)
    def test_invalid_phone_number(self, practice_form_page, invalid_phone):
        practice_form_page.open()
        practice_form_page.fill_mobile_number(invalid_phone)
        practice_form_page.submit()
        practice_form_page.verify_field_color(
            practice_form_page._mobile_number, ValidationState.INVALID
        )

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("day, month, year, expected_value", DATE_PICKER_CASES)
    def test_select_dates_via_picker(
        self, practice_form_page, day, month, year, expected_value
    ):
        practice_form_page.open()
        practice_form_page.fill_date_via_picker(day, month, year)
        expect(practice_form_page._date).to_have_value(expected_value)

    @pytest.mark.dependency(depends=["open_form"])
    def test_invalid_february_31(self, practice_form_page):
        practice_form_page.open()
        with pytest.raises(Exception):
            practice_form_page.fill_date_via_picker(
                day="31", month="February", year="2024"
            )

    @pytest.mark.dependency(depends=["open_form"])
    def test_subjects_remove_badge(self, practice_form_page):
        practice_form_page.open()
        practice_form_page.fill_subjects(["Math", "Arts"])
        practice_form_page.remove_subject("Math")
        practice_form_page.verify_selected_subjects(["Arts"])
        practice_form_page.remove_subject("Arts")
        practice_form_page.verify_no_subjects_selected()

    @pytest.mark.dependency(depends=["open_form"])
    def test_incorrect_badge(self, practice_form_page):
        practice_form_page.open()
        practice_form_page.fill_subjects(["XYZ"])
        practice_form_page.verify_no_subjects_selected()

    @pytest.mark.dependency(depends=["open_form"])
    def test_unselect_hobby(self, practice_form_page):
        practice_form_page.open()
        practice_form_page.select_hobbies([Hobby.SPORTS, Hobby.READING, Hobby.MUSIC])
        practice_form_page.verify_hobbies_checked(
            [Hobby.SPORTS, Hobby.READING, Hobby.MUSIC]
        )
        practice_form_page.select_hobbies([Hobby.SPORTS, Hobby.READING, Hobby.MUSIC])
        practice_form_page.verify_hobbies_checked([])

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("filename", VALID_FILE_NAMES)
    def test_upload_valid_image_formats(
        self, practice_form_page, create_temp_file, filename
    ):
        practice_form_page.open()
        file_path = create_temp_file(filename)
        practice_form_page.upload_picture(file_path)
        expected_filename = Path(filename).name
        expect(practice_form_page._upload_picture_input).to_have_value(
            f"C:\\fakepath\\{expected_filename}"
        )

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("filename", INVALID_FILE_NAMES)
    def test_upload_invalid_file_formats(
        self, practice_form_page, create_temp_file, filename
    ):
        practice_form_page.open()
        file_path = create_temp_file(filename)
        practice_form_page.upload_picture(file_path)
        practice_form_page.fill_first_name("User")
        practice_form_page.fill_last_name("Test")
        practice_form_page.select_gender(Gender.MALE)
        practice_form_page.fill_mobile_number("1234567890")
        practice_form_page.submit()
        expect(practice_form_page._modal_content).not_to_be_visible()

    @pytest.mark.dependency(depends=["open_form"])
    def test_current_address_special_characters(self, practice_form_page):
        special_chars_address = (
            "123/4B 'Main St.' & \"Oak Ave.\"; <script>alert(1)</script> "
            "#404! ~`@$^*()_+=-[]{}\\|/? "
            "Київ-Дніпро, вул. Залізнична, 15/A \n"
            "Apartment ⚡️🏢 🔥 12345-6789"
        )
        practice_form_page.open()
        practice_form_page.fill_current_address(special_chars_address)
        expect(practice_form_page._current_address).to_have_value(special_chars_address)

    @pytest.mark.dependency(depends=["open_form"])
    def test_city_disabled_by_default(self, practice_form_page):
        practice_form_page.open()
        practice_form_page.verify_city_is_disabled()

    @pytest.mark.dependency(depends=["open_form"])
    @pytest.mark.parametrize("state, cities", STATE_CITY_MAP.items())
    def test_select_state_and_city_cascade(self, practice_form_page, state, cities):
        practice_form_page.open()
        practice_form_page.verify_city_is_disabled()
        practice_form_page.select_state(state)
        practice_form_page.verify_city_is_enabled()
        selected_city = cities[0]
        practice_form_page.select_city(selected_city)
        practice_form_page.fill_first_name("User")
        practice_form_page.fill_last_name("Test")
        practice_form_page.select_gender(Gender.MALE)
        practice_form_page.fill_mobile_number("0000000000")
        practice_form_page.submit()
        assert (
            practice_form_page.get_modal_value_by_label("State and City")
            == f"{state} {selected_city}"
        )

    @pytest.mark.dependency(depends=["open_form"])
    def test_change_state_resets_city(self, practice_form_page):
        practice_form_page.open()
        practice_form_page.select_state("NCR")
        practice_form_page.select_city("Delhi")
        practice_form_page.select_state("Rajasthan")
        practice_form_page.select_city("Jaipur")

    @pytest.mark.dependency(depends=["open_form"])
    def test_select_obly_state_cascade(self, practice_form_page):
        practice_form_page.open()
        practice_form_page.select_state("NCR")
        practice_form_page.fill_first_name("User")
        practice_form_page.fill_last_name("Test")
        practice_form_page.select_gender(Gender.MALE)
        practice_form_page.fill_mobile_number("0000000000")
        practice_form_page.submit()
        assert practice_form_page.get_modal_value_by_label("State and City") == "NCR"

    @pytest.mark.dependency(depends=["open_form"])
    def test_city_resets_on_state_change(self, practice_form_page):
        practice_form_page.open()
        practice_form_page.select_state("NCR")
        practice_form_page.select_city("Delhi")
        practice_form_page.select_state("Haryana")
        practice_form_page.verify_city_is_reset()
