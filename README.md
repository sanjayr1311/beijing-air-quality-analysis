# Beijing Air Quality: From Data to Application Development

CMP7005 – Programming for Data Analysis (PRAC1)
EDA, PM2.5 prediction model, and an interactive Tkinter dashboard built on
hourly Beijing air quality data (2013–2017) from four monitoring stations:
Dongsi, Guanyuan (urban) and Huairou, Shunyi (suburban).

## Repository Structure

- `data/` — raw station CSVs, merged dataset, and cleaned dataset
- `notes/` — Jupyter notebook covering data merging, EDA, and model building
- `app/` — Tkinter dashboard application, trained model (`best_pm25_model.pkl`)
  and scaler (`scaler.pkl`)

## How to Run

pip install pandas scikit-learn joblib
python app/<main>.py


## Summary

- Data cleaned and merged into a single 140,256-row dataset
- EDA covers univariate, bivariate, multivariate, station-wise, temporal
  and AQI-category analysis
- Random Forest Regressor selected as final model (R² = 0.938)
- Dashboard provides dataset, summary, and live PM2.5 prediction views
