import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Healthcare Data Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🏥 Healthcare Data Analytics Dashboard")
st.write(
    "Interactive analysis of healthcare patient records, "
    "billing, medical conditions, admissions, insurance and test results."
)

st.markdown("---")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("healthcare_dataset.csv")

    # Convert date columns
    df["Date of Admission"] = pd.to_datetime(
        df["Date of Admission"],
        dayfirst=True,
        errors="coerce"
    )

    df["Discharge Date"] = pd.to_datetime(
        df["Discharge Date"],
        dayfirst=True,
        errors="coerce"
    )

    # Remove duplicate records
    df.drop_duplicates(inplace=True)

    return df


df = load_data()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.header("🔎 Filters")

# Gender filter
gender_options = ["All"] + sorted(
    df["Gender"].dropna().unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    "Select Gender",
    gender_options
)

# Medical condition filter
condition_options = ["All"] + sorted(
    df["Medical Condition"].dropna().unique().tolist()
)

selected_condition = st.sidebar.selectbox(
    "Medical Condition",
    condition_options
)

# Admission type filter
admission_options = ["All"] + sorted(
    df["Admission Type"].dropna().unique().tolist()
)

selected_admission = st.sidebar.selectbox(
    "Admission Type",
    admission_options
)

# Insurance provider filter
insurance_options = ["All"] + sorted(
    df["Insurance Provider"].dropna().unique().tolist()
)

selected_insurance = st.sidebar.selectbox(
    "Insurance Provider",
    insurance_options
)

# Test result filter
test_options = ["All"] + sorted(
    df["Test Results"].dropna().unique().tolist()
)

selected_test = st.sidebar.selectbox(
    "Test Results",
    test_options
)

# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df.copy()

if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"] == selected_gender
    ]

if selected_condition != "All":
    filtered_df = filtered_df[
        filtered_df["Medical Condition"] == selected_condition
    ]

if selected_admission != "All":
    filtered_df = filtered_df[
        filtered_df["Admission Type"] == selected_admission
    ]

if selected_insurance != "All":
    filtered_df = filtered_df[
        filtered_df["Insurance Provider"] == selected_insurance
    ]

if selected_test != "All":
    filtered_df = filtered_df[
        filtered_df["Test Results"] == selected_test
    ]

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_patients = filtered_df["Name"].count()
total_doctors = filtered_df["Doctor"].nunique()
total_hospitals = filtered_df["Hospital"].nunique()
total_insurance = filtered_df["Insurance Provider"].nunique()

col1.metric(
    "Total Patients",
    f"{total_patients:,}"
)

col2.metric(
    "Total Doctors",
    f"{total_doctors:,}"
)

col3.metric(
    "Total Hospitals",
    f"{total_hospitals:,}"
)

col4.metric(
    "Insurance Providers",
    f"{total_insurance:,}"
)

col5, col6, col7, col8 = st.columns(4)

total_billing = filtered_df["Billing Amount"].sum()
average_age = filtered_df["Age"].mean()
average_billing = filtered_df["Billing Amount"].mean()
maximum_billing = filtered_df["Billing Amount"].max()

col5.metric(
    "Total Billing",
    f"${total_billing:,.2f}"
)

col6.metric(
    "Average Age",
    f"{average_age:.1f}"
)

col7.metric(
    "Average Billing",
    f"${average_billing:,.2f}"
)

col8.metric(
    "Maximum Billing",
    f"${maximum_billing:,.2f}"
)

st.markdown("---")

# ---------------------------------------------------------
# DATASET INFORMATION
# ---------------------------------------------------------

st.subheader("📋 Dataset Information")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.write("### Dataset Shape")
    st.write(
        f"Rows: **{filtered_df.shape[0]:,}**"
    )
    st.write(
        f"Columns: **{filtered_df.shape[1]}**"
    )

with info_col2:
    st.write("### Missing Values")
    missing_values = filtered_df.isnull().sum()
    missing_values = missing_values[
        missing_values > 0
    ]

    if len(missing_values) == 0:
        st.success("No missing values found.")
    else:
        st.dataframe(
            missing_values,
            use_container_width=True
        )

# ---------------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------------

st.subheader("👀 Patient Data Preview")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)

# ---------------------------------------------------------
# EDA SECTION
# ---------------------------------------------------------

st.markdown("---")
st.header("📈 Exploratory Data Analysis")

# ---------------------------------------------------------
# GENDER DISTRIBUTION
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Gender Distribution")

    gender_counts = filtered_df["Gender"].value_counts()

    fig, ax = plt.subplots()

    gender_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Gender")
    ax.set_ylabel("Patients")
    ax.set_title("Gender Distribution")

    plt.xticks(rotation=0)

    st.pyplot(fig)

with col2:

    st.subheader("Medical Condition")

    condition_counts = (
        filtered_df["Medical Condition"]
        .value_counts()
    )

    fig, ax = plt.subplots()

    condition_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Medical Condition")
    ax.set_ylabel("Patients")
    ax.set_title("Medical Condition Distribution")

    plt.xticks(rotation=45)

    st.pyplot(fig)

# ---------------------------------------------------------
# ADMISSION TYPE
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Admission Type")

    admission_counts = (
        filtered_df["Admission Type"]
        .value_counts()
    )

    fig, ax = plt.subplots()

    admission_counts.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")

    st.pyplot(fig)

with col2:

    st.subheader("Insurance Provider")

    insurance_counts = (
        filtered_df["Insurance Provider"]
        .value_counts()
    )

    fig, ax = plt.subplots()

    insurance_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Insurance Provider")
    ax.set_ylabel("Patients")
    ax.set_title("Insurance Provider Distribution")

    plt.xticks(rotation=45)

    st.pyplot(fig)

# ---------------------------------------------------------
# TEST RESULTS
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Test Results")

    test_counts = (
        filtered_df["Test Results"]
        .value_counts()
    )

    fig, ax = plt.subplots()

    test_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Test Result")
    ax.set_ylabel("Patients")
    ax.set_title("Test Results Distribution")

    plt.xticks(rotation=0)

    st.pyplot(fig)

with col2:

    st.subheader("Age Distribution")

    fig, ax = plt.subplots()

    ax.hist(
        filtered_df["Age"].dropna(),
        bins=20
    )

    ax.set_xlabel("Age")
    ax.set_ylabel("Patients")
    ax.set_title("Age Distribution")

    st.pyplot(fig)

# ---------------------------------------------------------
# BILLING DISTRIBUTION
# ---------------------------------------------------------

st.subheader("💰 Billing Amount Distribution")

fig, ax = plt.subplots()

ax.hist(
    filtered_df["Billing Amount"].dropna(),
    bins=20
)

ax.set_xlabel("Billing Amount")
ax.set_ylabel("Patients")
ax.set_title("Billing Amount Distribution")

st.pyplot(fig)

# ---------------------------------------------------------
# TOP HOSPITALS AND DOCTORS
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏥 Top 10 Hospitals")

    top_hospitals = (
        filtered_df["Hospital"]
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots()

    top_hospitals.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Hospital")
    ax.set_ylabel("Patients")
    ax.set_title("Top 10 Hospitals")

    plt.xticks(rotation=90)

    st.pyplot(fig)

with col2:

    st.subheader("👨‍⚕️ Top 10 Doctors")

    top_doctors = (
        filtered_df["Doctor"]
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots()

    top_doctors.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Doctor")
    ax.set_ylabel("Patients")
    ax.set_title("Top 10 Doctors")

    plt.xticks(rotation=90)

    st.pyplot(fig)

# ---------------------------------------------------------
# GROUP BY ANALYSIS
# ---------------------------------------------------------

st.markdown("---")
st.header("📊 Group-by Analysis")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Average Billing by Medical Condition")

    avg_billing_condition = (
        filtered_df
        .groupby("Medical Condition")["Billing Amount"]
        .mean()
        .sort_values(ascending=False)
    )

    st.dataframe(
        avg_billing_condition,
        use_container_width=True
    )

with col2:

    st.subheader("Patients by Insurance Provider")

    patients_insurance = (
        filtered_df
        .groupby("Insurance Provider")
        .size()
        .sort_values(ascending=False)
    )

    st.dataframe(
        patients_insurance,
        use_container_width=True
    )

# ---------------------------------------------------------
# BUSINESS INSIGHTS
# ---------------------------------------------------------

st.markdown("---")
st.header("💡 Business Insights")

st.write(
    f"""
    - **Total Patients:** {total_patients:,}
    - **Average Billing Amount:** ${average_billing:,.2f}
    - **Average Patient Age:** {average_age:.1f} years
    - **Total Hospitals:** {total_hospitals:,}
    - **Total Doctors:** {total_doctors:,}
    - **Total Insurance Providers:** {total_insurance:,}
    - **Total Billing Amount:** ${total_billing:,.2f}
    """
)

# ---------------------------------------------------------
# DOWNLOAD FILTERED DATA
# ---------------------------------------------------------

st.markdown("---")
st.subheader("⬇️ Download Filtered Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_healthcare_data.csv",
    mime="text/csv"
)

st.success("Dashboard loaded successfully!")