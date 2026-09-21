# SortWise AI Prototype (Demo)

This repository now contains a minimal prototype for **SortWise AI**, an AI-powered waste-segregation decision-support demo.

## What this demo does

- Accepts a waste-item text description
- Classifies likely waste type/material
- Applies confidence handling
- Looks up a local rule profile (`default` or `campus`)
- Returns one disposal recommendation with caveats

## Run

```bash
python3 /home/runner/work/check/check/sortwise_demo.py "empty glass bottle"
python3 /home/runner/work/check/check/sortwise_demo.py "used battery" --locale campus
```

## Notes

- This is a prototype and keyword-based mock classifier.
- Hazardous or low-confidence cases are escalated to official local guidance.
- Local authority rules are always the final source of truth.
