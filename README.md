# Streamlit MRI Report AI Assistant

This project is a Streamlit application designed to assist radiologists in generating AI-enhanced MRI reports. Users can upload MRI report PDFs, select between OpenAI and Anthropic for report generation, and download the generated reports with appropriate suffixes indicating the source of the report.

## Project Structure

```
streamlit-app
├── src
│   ├── app.py                # Main entry point of the Streamlit application
│   └── utils
│       ├── openai_utils.py   # Utility functions for OpenAI API interactions
│       └── anthropic_utils.py # Utility functions for Anthropic API interactions
├── requirements.txt          # Project dependencies
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd streamlit-app
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment. You can create one using `venv` or `conda`. After activating your environment, run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Execute the following command to start the Streamlit application:
   ```
   streamlit run src/app.py
   ```

## Usage Guidelines

- Upon launching the application, users will be prompted to enter their OpenAI and/or Anthropic API keys.
- Users can upload an MRI report in PDF format.
- After the report is uploaded, users can select which LLM to use for generating reports.
- The application will generate a summary, a patient-friendly report, and recommendations based on the uploaded report.
- Users can download the generated reports, which will have suffixes indicating whether they were generated by OpenAI or Anthropic (e.g., `AI_Generated_MRI_Report_OpenAI.pdf`).

## Dependencies

- Streamlit
- OpenAI
- Anthropic
- PyPDF2
- FPDF

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.