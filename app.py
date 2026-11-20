
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


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="HealthCare | Patient Management",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_table()


# --------------------------------------------------
# CUSTOM CLINICAL LIGHT THEME
# --------------------------------------------------

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #F5F8FA;
    color: #203447;
    font-family: 'Inter', sans-serif;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5EDF1;
}

section[data-testid="stSidebar"] h1 {
    color: #087F8C;
    font-size: 25px;
    font-weight: 800;
}

/* Headings */
h1, h2, h3 {
    color: #173B50 !important;
    font-weight: 700 !important;
}

/* Paragraphs */
p, label {
    color: #536979;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E2EBEF;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 3px 12px rgba(30, 70, 90, 0.04);
}

div[data-testid="stMetricLabel"] {
    color: #627887;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #087F8C;
    font-weight: 800;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #087F8C;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 0.55rem 1.2rem;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #06636E;
    color: white;
    border: none;
}

/* Input fields */
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    border-radius: 8px;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    border-radius: 8px;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border: 1px solid #E1E9ED;
    border-radius: 12px;
    overflow: hidden;
}

/* Custom cards */
.hero-card {
    background: linear-gradient(115deg, #087F8C, #13A6A2);
    color: white;
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.hero-card h2 {
    color: white !important;
    margin-bottom: 8px;
}

.hero-card p {
    color: #E7FFFF !important;
    margin-bottom: 0;
}

.info-card {
    background: white;
    border: 1px solid #E2EBEF;
    border-radius: 14px;
    padding: 20px;
    min-height: 125px;
}

.info-card h4 {
    color: #087F8C;
    margin-top: 0;
}

.info-card p {
    color: #607584;
    font-size: 14px;
}

.section-note {
    background: #EAF6F7;
    border-left: 4px solid #087F8C;
    padding: 13px 16px;
    border-radius: 6px;
    color: #315765;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    color: #8295A1;
    font-size: 12px;
    padding: 30px 0 5px 0;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def page_header(title, subtitle):
    st.title(title)
    st.caption(subtitle)
    st.markdown("---")


def get_patient_dataframe():
    records = get_patients()

    columns = [
        "Patient ID",
        "Full Name",
        "Date of Birth",
        "Email",
        "Glucose",
        "Haemoglobin",
        "Cholesterol",
        "AI Remarks"
    ]

    return pd.DataFrame(records, columns=columns)


def validate_patient_form(name, dob, email,
                          glucose, haemoglobin, cholesterol):

    errors = []
    numbers = {}

    if not validate_name(name):
        errors.append("Full name is required.")

    if not validate_email(email):
        errors.append("Please enter a valid email address.")

    valid_dob, dob_message = validate_dob(dob)

    if not valid_dob:
        errors.append(dob_message)

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

    return errors, numbers


def show_patient_table():

    df = get_patient_dataframe()

    if df.empty:
        st.info("No patient records are available.")
        return

    display_df = df.drop(columns=["AI Remarks"])

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Patient ID": st.column_config.NumberColumn(
                "ID",
                format="%d"
            ),
            "Glucose": st.column_config.NumberColumn(
                "Glucose",
                format="%.2f"
            ),
            "Haemoglobin": st.column_config.NumberColumn(
                "Haemoglobin",
                format="%.2f"
            ),
            "Cholesterol": st.column_config.NumberColumn(
                "Cholesterol",
                format="%.2f"
            )
        }
    )


# --------------------------------------------------
# EMPLOYER TEST DATA
# --------------------------------------------------

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


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 🏥 HealthCare")
    st.caption("PATIENT MANAGEMENT SYSTEM")

    st.markdown("---")

    menu = st.radio(
        "MAIN MENU",
        [
            "Dashboard",
            "Add Patient",
            "Import Test Data",
            "View Patients",
            "Edit Patient",
            "Delete Patient"
        ],
        label_visibility="visible"
    )

    st.markdown("---")

    st.markdown("### AI Assistant")

    st.markdown(
        """
        <div class="info-card">
            <h4>✦ Gemini AI</h4>
            <p>AI-assisted explanations of blood test values.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.caption("Health Information System")
    st.caption("Developed by Preeti Tavag")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if menu == "Dashboard":

    page_header(
        "Dashboard",
        "Welcome to your patient health information management system."
    )

    st.markdown(
        """
        <div class="hero-card">
            <h2>Better Patient Information Management</h2>
            <p>
                Manage patient records, validate health information,
                and generate AI-assisted health explanations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    patients = get_patients()

    total_patients = len(patients)
    imported = is_test_data_imported()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Patient Records",
        total_patients,
        help="Number of records currently stored in SQLite."
    )

    col2.metric(
        "Assessment Data",
        "Imported" if imported else "Pending"
    )

    col3.metric(
        "AI Integration",
        "Gemini API"
    )

    st.markdown("### Quick Access")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="info-card">
                <h4>＋ Add Patient</h4>
                <p>Register a new patient and generate AI remarks.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="info-card">
                <h4>▤ View Records</h4>
                <p>Review stored patient information and export CSV.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="info-card">
                <h4>✦ AI Health Remarks</h4>
                <p>Generate educational explanations using Gemini.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Recent Patient Records")

    if patients:

        recent = pd.DataFrame(
            patients[-5:],
            columns=[
                "ID", "Full Name", "DOB", "Email",
                "Glucose", "Haemoglobin", "Cholesterol", "Remarks"
            ]
        )

        st.dataframe(
            recent.drop(columns=["Remarks"]),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No patient records yet. Add a patient to get started.")


# --------------------------------------------------
# ADD PATIENT
# --------------------------------------------------

elif menu == "Add Patient":

    page_header(
        "Add New Patient",
        "Enter patient details and generate AI-assisted health remarks."
    )

    st.markdown(
        '<div class="section-note">Please enter accurate patient information. '
        'Date of birth accepts DD/MM/YYYY or DD.MM.YYYY.</div>',
        unsafe_allow_html=True
    )

    with st.form("add_patient_form"):

        st.subheader("Personal Information")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name", placeholder="Enter full name")

        with col2:
            dob = st.text_input(
                "Date of Birth",
                placeholder="DD/MM/YYYY"
            )

        email = st.text_input(
            "Email Address",
            placeholder="example@email.com"
        )

        st.markdown("---")
        st.subheader("Blood Test Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            glucose = st.text_input("Glucose", placeholder="e.g. 100")

        with col2:
            haemoglobin = st.text_input(
                "Haemoglobin",
                placeholder="e.g. 13.5"
            )

        with col3:
            cholesterol = st.text_input(
                "Cholesterol",
                placeholder="e.g. 180"
            )

        submitted = st.form_submit_button(
            "Save Patient and Generate AI Remarks",
            use_container_width=True
        )

    if submitted:

        errors, numbers = validate_patient_form(
            name, dob, email,
            glucose, haemoglobin, cholesterol
        )

        if errors:

            for error in errors:
                st.error(error)

        else:

            with st.spinner("Generating AI health explanation..."):

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

            st.success("Patient record saved successfully!")

            st.subheader("✦ AI-Generated Health Remarks")
            st.markdown(remarks)


# --------------------------------------------------
# IMPORT TEST DATA
# --------------------------------------------------

elif menu == "Import Test Data":

    page_header(
        "Assessment Data Import",
        "Validate and process the original 10 employer-provided records."
    )

    st.markdown(
        '<div class="section-note">The original test values are preserved. '
        'Valid records are saved, invalid records are rejected, and '
        'duplicate records are retained.</div>',
        unsafe_allow_html=True
    )

    if is_test_data_imported():

        st.success("The employer test data has already been imported.")

    else:

        st.info("10 original records are ready for validation.")

        if st.button(
            "Validate and Import All Records",
            use_container_width=True
        ):

            results = []
            valid_count = 0
            rejected_count = 0

            progress = st.progress(0)
            status = st.empty()

            for index, record in enumerate(TEST_DATA):

                name, dob, email, glucose, haemoglobin, cholesterol = record

                errors, numbers = validate_patient_form(
                    name,
                    dob,
                    email,
                    glucose,
                    haemoglobin,
                    cholesterol
                )

                if errors:

                    rejected_count += 1

                    results.append({
                        "Record": index + 1,
                        "Patient": name,
                        "Status": "Rejected",
                        "Reason": "; ".join(errors)
                    })

                else:

                    status.write(
                        f"Processing record {index + 1} of 10: {name}"
                    )

                    with st.spinner("Generating AI remarks..."):

                        remarks = generate_health_remarks(
                            numbers["Glucose"],
                            numbers["Haemoglobin"],
                            numbers["Cholesterol"]
                        )

                    add_patient(
                        name,
                        dob,
                        email,
                        numbers["Glucose"],
                        numbers["Haemoglobin"],
                        numbers["Cholesterol"],
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

            status.success("All 10 records have been processed.")

    if "import_results" in st.session_state:

        st.markdown("### Validation Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Records", 10)
        col2.metric(
            "Valid Records",
            st.session_state["valid_count"]
        )
        col3.metric(
            "Rejected Records",
            st.session_state["rejected_count"]
        )

        st.markdown("### Individual Validation Results")

        st.dataframe(
            pd.DataFrame(st.session_state["import_results"]),
            use_container_width=True,
            hide_index=True
        )


# --------------------------------------------------
# VIEW PATIENTS
# --------------------------------------------------

elif menu == "View Patients":

    page_header(
        "Patient Records",
        "View, review and export all stored patient information."
    )

    patients = get_patients()

    if patients:

        df = get_patient_dataframe()

        st.metric("Total Patient Records", len(df))

        st.markdown("### Patient Information")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Patient ID": st.column_config.NumberColumn(
                    "ID",
                    format="%d"
                ),
                "AI Remarks": st.column_config.TextColumn(
                    "AI Remarks",
                    width="large"
                )
            }
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Patient Records (CSV)",
            data=csv,
            file_name="patient_records.csv",
            mime="text/csv"
        )

    else:

        st.info("No patient records found. Add a patient to get started.")


# --------------------------------------------------
# EDIT PATIENT
# --------------------------------------------------

elif menu == "Edit Patient":

    page_header(
        "Edit Patient",
        "Update existing patient information."
    )

    patients = get_patients()

    if patients:

        patient_options = {
            f"{p[0]} | {p[1]} | {p[3]}": p
            for p in patients
        }

        selected = st.selectbox(
            "Select a patient to edit",
            list(patient_options.keys())
        )

        patient = patient_options[selected]

        st.markdown("### Patient Information")

        with st.form("edit_patient_form"):

            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input(
                    "Full Name",
                    value=patient[1]
                )

                dob = st.text_input(
                    "Date of Birth",
                    value=patient[2]
                )

                email = st.text_input(
                    "Email Address",
                    value=patient[3]
                )

            with col2:
                glucose = st.text_input(
                    "Glucose",
                    value=str(patient[4])
                )

                haemoglobin = st.text_input(
                    "Haemoglobin",
                    value=str(patient[5])
                )

                cholesterol = st.text_input(
                    "Cholesterol",
                    value=str(patient[6])
                )

            submitted = st.form_submit_button(
                "Update Patient Details",
                use_container_width=True
            )

        if submitted:

            errors, numbers = validate_patient_form(
                name, dob, email,
                glucose, haemoglobin, cholesterol
            )

            if errors:

                for error in errors:
                    st.error(error)

            else:

                remarks = patient[7]

                blood_values_changed = (
                    numbers["Glucose"] != patient[4]
                    or numbers["Haemoglobin"] != patient[5]
                    or numbers["Cholesterol"] != patient[6]
                )

                if blood_values_changed:

                    with st.spinner("Regenerating AI remarks..."):

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

                st.success("Patient information updated successfully!")
                st.rerun()

    else:

        st.info("There are no patient records available to edit.")


# --------------------------------------------------
# DELETE PATIENT
# --------------------------------------------------

elif menu == "Delete Patient":

    page_header(
        "Delete Patient",
        "Remove a patient record from the database."
    )

    patients = get_patients()

    if patients:

        patient_options = {
            f"{p[0]} | {p[1]} | {p[3]}": p[0]
            for p in patients
        }

        selected = st.selectbox(
            "Select a patient to delete",
            list(patient_options.keys())
        )

        st.warning(
            "Deleting a record is permanent. Please verify the selected patient."
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this patient record."
        )

        if st.button(
            "Delete Patient Record",
            disabled=not confirm
        ):

            delete_patient(patient_options[selected])

            st.success("Patient record deleted successfully!")
            st.rerun()

    else:

        st.info("There are no patient records available to delete.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        AI Health Information System · Built with Python, Streamlit,
        SQLite and Google Gemini API<br>
        Educational information only · Not a medical diagnosis
    </div>
    """,
    unsafe_allow_html=True
)
