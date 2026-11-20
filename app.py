
import streamlit as st
import pandas as pd

from database import (
    create_table,
    add_patient,
    get_patients,
    update_patient,
    delete_patient,
    is_test_data_imported,
    mark_test_data_imported
)

from validation import (
    validate_name,
    validate_email,
    validate_dob,
    validate_number
)

from ai_health import generate_health_remarks


st.set_page_config(
    page_title="Health Prediction App",
    page_icon="🏥",
    layout="wide"
)

create_table()

st.title("🏥 AI Health Information System")
st.write("Manage patient records and generate AI-assisted health remarks.")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Patient",
        "Import Test Data",
        "View Patients",
        "Edit Patient",
        "Delete Patient"
    ]
)


# Original employer-provided test data.
# Keep the values and dates exactly as supplied.

TEST_DATA = [
    ("Robyn Pears", "28.01.1960", "robyn@gmail.com", 232, 13.5, 180),
    ("John Hunter", "10.12.1990", "hunter@gmail", 94, 15, 200),
    ("Darryl Tim", "12.11.1993", "timd@smh.com.au", 240, 18.6, 326),
    ("Peter Larry", "31.11.2001", "Larry@hotmail.com", 88, 11.5, 165),
    ("Sam Kerr", "09.12.2006", "sam@news.com.au", 198, 8.9, 192),
    ("Robyn Pears", "28.01.1960", "robyn@gmail.com", 232, 13.5, 180),
    ("Madison XI", "12.09.1998", "madison@hotmail.com", 85, 7.6, 163),
    ("Kris Wu", "19.10.2030", "Kris.wu.gmail.com", 79, 16.5, 197),
    ("Tenille Singh", "30.11.1991", "Tenille@yahoo.com", 101, 15, 310),
    ("Prem Kumar", "28.04.1990", "prem@telstra.com", 155, 12.5, 265)
]


# Dashboard
if menu == "Dashboard":

    patients = get_patients()

    st.subheader("Dashboard")

    col1, col2 = st.columns(2)

    col1.metric("Total Patient Records", len(patients))
    col2.metric(
        "Employer Test Data Imported",
        "Yes" if is_test_data_imported() else "No"
    )

    st.info(
        "This application stores patient information and generates "
        "AI-assisted health explanations. It is not a diagnostic system."
    )


# Add Patient
elif menu == "Add Patient":

    st.subheader("Add New Patient")

    with st.form("add_patient_form"):

        name = st.text_input("Full Name")
        dob = st.text_input("Date of Birth (DD/MM/YYYY)")
        email = st.text_input("Email")
        glucose = st.text_input("Glucose")
        haemoglobin = st.text_input("Haemoglobin")
        cholesterol = st.text_input("Cholesterol")

        submitted = st.form_submit_button("Save Patient")

    if submitted:

        errors = []

        if not validate_name(name):
            errors.append("Full name is required.")

        if not validate_email(email):
            errors.append("Enter a valid email address.")

        valid_dob, dob_message = validate_dob(dob)

        if not valid_dob:
            errors.append(dob_message)

        numbers = {}

        for field, value in [
            ("Glucose", glucose),
            ("Haemoglobin", haemoglobin),
            ("Cholesterol", cholesterol)
        ]:
            valid, result = validate_number(value, field)

            if not valid:
                errors.append(result)
            else:
                numbers[field] = result

        if errors:
            for error in errors:
                st.error(error)

        else:
            with st.spinner("Generating AI health remarks..."):

                remarks = generate_health_remarks(
                    numbers["Glucose"],
                    numbers["Haemoglobin"],
                    numbers["Cholesterol"]
                )

            add_patient(
                name.strip(),
                dob.strip(),
                email.strip(),
                numbers["Glucose"],
                numbers["Haemoglobin"],
                numbers["Cholesterol"],
                remarks
            )

            st.success("Patient saved successfully!")
            st.write("AI-generated remarks:")
            st.write(remarks)


# Import Employer Test Data
elif menu == "Import Test Data":

    st.subheader("Employer Assessment: Test Data Import")

    st.write(
        "This feature validates all 10 original records, "
        "saves valid records, and reports invalid records."
    )

    if is_test_data_imported():

        st.warning(
            "The employer test data has already been imported. "
            "It cannot be imported again using this button."
        )

    else:

        st.warning(
            "The import will save valid records to the database. "
            "Both Robyn Pears records will be retained."
        )

        if st.button("Validate and Import All 10 Records"):

            results = []
            valid_count = 0
            rejected_count = 0

            progress = st.progress(0)

            for index, record in enumerate(TEST_DATA):

                name, dob, email, glucose, haemoglobin, cholesterol = record

                errors = []

                if not validate_name(name):
                    errors.append("Full name is required.")

                if not validate_email(email):
                    errors.append("Invalid email address.")

                valid_dob, dob_message = validate_dob(dob)

                if not valid_dob:
                    errors.append(dob_message)

                number_values = {}

                for field, value in [
                    ("Glucose", glucose),
                    ("Haemoglobin", haemoglobin),
                    ("Cholesterol", cholesterol)
                ]:

                    valid, result = validate_number(value, field)

                    if not valid:
                        errors.append(result)
                    else:
                        number_values[field] = result

                if errors:

                    rejected_count += 1

                    results.append({
                        "Record": index + 1,
                        "Patient": name,
                        "Status": "Rejected",
                        "Reason": "; ".join(errors)
                    })

                else:

                    with st.spinner(
                        f"Processing record {index + 1}: {name}"
                    ):

                        remarks = generate_health_remarks(
                            number_values["Glucose"],
                            number_values["Haemoglobin"],
                            number_values["Cholesterol"]
                        )

                    add_patient(
                        name,
                        dob,
                        email,
                        number_values["Glucose"],
                        number_values["Haemoglobin"],
                        number_values["Cholesterol"],
                        remarks
                    )

                    valid_count += 1

                    results.append({
                        "Record": index + 1,
                        "Patient": name,
                        "Status": "Saved",
                        "Reason": "All validations passed."
                    })

                progress.progress((index + 1) / len(TEST_DATA))

            mark_test_data_imported()

            st.session_state["import_results"] = results
            st.session_state["valid_count"] = valid_count
            st.session_state["rejected_count"] = rejected_count

            st.success("Test data processing completed!")


    if "import_results" in st.session_state:

        st.subheader("Validation Report")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Records", 10)
        col2.metric("Valid Records", st.session_state["valid_count"])
        col3.metric("Rejected Records", st.session_state["rejected_count"])

        st.dataframe(
            pd.DataFrame(st.session_state["import_results"]),
            use_container_width=True
        )


# View Patients
elif menu == "View Patients":

    st.subheader("All Patient Records")

    patients = get_patients()

    if patients:

        columns = [
            "ID",
            "Full Name",
            "DOB",
            "Email",
            "Glucose",
            "Haemoglobin",
            "Cholesterol",
            "AI Remarks"
        ]

        df = pd.DataFrame(patients, columns=columns)

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Patient Records as CSV",
            data=csv,
            file_name="patient_records.csv",
            mime="text/csv"
        )

    else:
        st.info("No patient records found.")


# Edit Patient
elif menu == "Edit Patient":

    st.subheader("Edit Patient Details")

    patients = get_patients()

    if patients:

        patient_options = {
            f"{patient[0]} - {patient[1]} ({patient[3]})": patient
            for patient in patients
        }

        selected = st.selectbox(
            "Select Patient",
            list(patient_options.keys())
        )

        patient = patient_options[selected]

        with st.form("edit_patient_form"):

            name = st.text_input("Full Name", value=patient[1])
            dob = st.text_input("Date of Birth", value=patient[2])
            email = st.text_input("Email", value=patient[3])
            glucose = st.text_input("Glucose", value=str(patient[4]))
            haemoglobin = st.text_input("Haemoglobin", value=str(patient[5]))
            cholesterol = st.text_input("Cholesterol", value=str(patient[6]))

            submitted = st.form_submit_button("Update Patient")

        if submitted:

            errors = []

            if not validate_name(name):
                errors.append("Full name is required.")

            if not validate_email(email):
                errors.append("Enter a valid email address.")

            valid_dob, dob_message = validate_dob(dob)

            if not valid_dob:
                errors.append(dob_message)

            numbers = {}

            for field, value in [
                ("Glucose", glucose),
                ("Haemoglobin", haemoglobin),
                ("Cholesterol", cholesterol)
            ]:

                valid, result = validate_number(value, field)

                if not valid:
                    errors.append(result)
                else:
                    numbers[field] = result

            if errors:

                for error in errors:
                    st.error(error)

            else:

                remarks = patient[7]

                if (
                    numbers["Glucose"] != patient[4]
                    or numbers["Haemoglobin"] != patient[5]
                    or numbers["Cholesterol"] != patient[6]
                ):

                    with st.spinner("Updating AI health remarks..."):

                        remarks = generate_health_remarks(
                            numbers["Glucose"],
                            numbers["Haemoglobin"],
                            numbers["Cholesterol"]
                        )

                update_patient(
                    patient[0],
                    name.strip(),
                    dob.strip(),
                    email.strip(),
                    numbers["Glucose"],
                    numbers["Haemoglobin"],
                    numbers["Cholesterol"],
                    remarks
                )

                st.success("Patient updated successfully!")
                st.rerun()

    else:
        st.info("No patients available to edit.")


# Delete Patient
elif menu == "Delete Patient":

    st.subheader("Delete Patient Record")

    patients = get_patients()

    if patients:

        patient_options = {
            f"{patient[0]} - {patient[1]} ({patient[3]})": patient[0]
            for patient in patients
        }

        selected = st.selectbox(
            "Select Patient to Delete",
            list(patient_options.keys())
        )

        if st.button("Delete Selected Patient"):

            delete_patient(patient_options[selected])

            st.success("Patient deleted successfully!")
            st.rerun()

    else:
        st.info("No patient records available to delete.")
