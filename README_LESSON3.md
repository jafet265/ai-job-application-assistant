# Lesson 3 - Better AI Resume Analysis

This version adds weighted scoring, evidence verification, requirements classification, and offline tests.

## Install in GitHub Codespaces

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py --server.address 0.0.0.0
```

Set `GEMINI_API_KEY` as a GitHub Codespaces secret. Optional `GEMINI_MODEL` selects an accessible model; default is `gemini-3.8-flash`, which should be changed if unavailable to your account.

## Notes

- Use fictional resumes for testing. API requests send resume content to the model provider.
- Matched evidence must be an exact excerpt of extracted resume text; this is a guardrail, not a complete factual verification system.
- Skills are identified by AI and may be omitted or misclassified. Review the output manually.
- The score is weighted skills coverage, not a hiring probability.
- No API requests are made by the unit tests.
