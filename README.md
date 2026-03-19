
# Exploratory Data Analysis: Factors Influencing College Graduate Earnings

**Author:** Zilin Pan, Billy Zhang  
**Date:** March 2026  

---

## 1. Executive Summary
This project conducts an exploratory data analysis (EDA) of the U.S. Department of Education’s **College Scorecard** dataset. The primary goal is to identify which institutional factors—ranging from academic selectivity to faculty investment—most significantly impact the median earnings of graduates ten years after they first enrolled. 

By merging historical performance data (2020-21) with recent geographic metadata (2023-24), this study examines how variables like **SAT scores**, **faculty salaries**, and **institutional control** (public vs. private) correlate with financial success. The findings provide insights into the "return on investment" of higher education and highlight regional economic disparities across the United States.

Beyond simple correlations, this project incorporates multivariate regression analysis to isolate the independent effects of institutional characteristics on earnings outcomes. By controlling for multiple factors simultaneously, the analysis aims to distinguish whether the visualized relationships, such as the link between SAT scores and earnings, persist when accounting for other institutional features. This boosts the reliability of the findings and allows for a more nuanced interpretation of how different factors jointly influence graduates' earning potential.

---

## 2. Research Questions
To guide this analysis, the following research questions were examined to distinguish between correlation and more structured economic relationships:
1. **Academic Selectivity:** Does a higher average SAT score for an institution translate to higher earnings for its graduates?
2. **Resource Investment:** Is there a positive correlation between the average salary paid to faculty members and the future earnings of students?
3. **Institutional Type:** Do graduates from private non-profit institutions earn significantly more than those from public or for-profit schools?
4. **Geographic Distribution:** How do graduate earnings vary spatially across different regions of the U.S.?

---

## 3. Data Source & Features
The dataset was sourced from the [College Scorecard](https://collegescorecard.ed.gov/data/), a known and reputable source provided by the U.S. government. The College Scorecard dataset is particularly suitable for this analysis because it combines college characteristics with long-term outcomes, allowing for a direct examination of the return on education.

### Data Cleaning and Integration:
- **Merging:** Two datasets (`MERGED2020_21_PP.csv` and `MERGED2023_24_PP.csv`) were joined on the unique `UNITID` to combine student outcome data with geographical coordinates (Latitude/Longitude).
- **Filtering:** The analysis focused on institutions with valid records for median earnings (`MD_EARN_WNE_P10`).
- **Data Types:** The final dataset includes over 12 features with mixed numeric and categorical data types, covering more than 300 rows (satisfying project requirements).

### Key Features:
- `SAT_AVG`: Average SAT equivalent score of students.
- `AVGFACSAL`: Average faculty salary per month.
- `MD_EARN_WNE_P10`: Median earnings of graduates 10 years after entry (Target Variable).
- `CONTROL`: 1 (Public), 2 (Private Non-Profit), 3 (Private For-Profit).
- `LATITUDE` / `LONGITUDE`: Campus geographic location.

---

## 4. Methodology
The project follows a comprehensive data science pipeline:
1. **Data Preprocessing:** Handling missing values, converting string-based "Privacy Suppressed" data into numeric types, and removing outliers using `Pandas`.
2. **Exploratory Visualization:** Using `Seaborn` and `Matplotlib` to identify trends and distributions.
3. **Statistical Modeling:** In addition to visualization, implementing an **Ordinary Least Squares (OLS) Regression** using `statsmodels` to quantify the relationship between predictors and earnings. This is important because many characteristics are correlated with one another—for example, more selective schools often also have higher faculty salaries. Without controlling for these relationships, simple visual correlations may overstate the importance of individual variables.
4. **Geospatial Analysis:** Utilizing `hexbin` plots to visualize the density and earning levels of colleges across the United States.

---

## 5. Key Findings & Interpretation

### 5.1 The SAT - Earnings Correlation
The analysis shows a strong positive linear relationship between average SAT scores and future earnings. However, the dispersion of points around the regression line indicates that while higher SAT scores increase expected earnings, they do not fully determine outcomes.
* **Interpretation:** Higher selectivity often leads to a higher-earning peer network or reflects the "prestige" value that the labor market rewards. Employers may interpret attendance at more selective institutions as an indicator of productivity, even if the underlying skills are only partially captured by test scores.

### 5.2 Faculty Salary as a Proxy for Quality
The data indicates that institutions paying higher average faculty salaries tend to have higher graduate outcomes, though the relationship appears less steep than that of SAT scores.
* **Interpretation:** Investment in high-quality faculty may translate to better educational resources and instruction quality so better student preparation for high-paying industries. Yet, while investment in faculty contributes to better outcomes, it is likely secondary to student composition. High salary may also proxy for prestige, making it difficult to disentangle whether higher salaries directly cause improved outcomes or simply reflect already strong institutions.

### 5.3 Geographic Earnings Heatmap
Using the longitude and latitude data, the `hexbin` visualization reveals that high-earning graduates are concentrated in the Northeast and the West Coast.
* **Interpretation:** This pattern reflects the influence of local labor markets, where proximity to major economic hubs—such as New York’s financial sector and California’s technology industry—provides students with greater access to high-paying jobs, internships, and professional networks.

### 5.4 Institutional Control
Box plots and regression coefficients suggest that Private Non-Profit institutions (Control = 2) generally have a higher ceiling for graduate earnings compared to Public institutions. They also get higher average earnings. Public schools get the second highest and private for-profit get the lowest. This suggests that institutional structure plays a significant role in shaping economic outcomes.

### 5.5 Multivariate Regression Analysis
The multivariate regression results confirm that both academic selectivity and institutional investment are significant predictors of graduate earnings, even after controlling for institutional type.

### 5.6 Limitations and Causality Considerations
While the analysis identifies strong relationships between institutional characteristics and earnings, it is important to emphasize that these results do not imply causation. Other affecting factors that could have related to the dependent variable(earning) while correlating with independent variables(sat_avg) such as students’ chosen majors, prior socioeconomic background, and career preferences are not included in the model, leading to omitted variable bias. Furthermore, variables such as SAT scores and faculty salaries may act as proxies for institutional prestige rather than direct causal drivers. As a result, the findings should be conservatively interpreted as descriptive relationships rather than definitive causal effects. Nonetheless, this reserach has succeeded in discovering some of the most influencing factors of post-graduation earnings.
---

## 6. Project Reproducibility
To replicate this analysis, follow these steps:

1. **Clone this repository:**
   ```bash
   git clone <your-repository-url>
   ```

2. **Prepare the Data:**  
Ensure the `.csv` files from the College Scorecard are placed in the directory specified in the notebook or update the file paths in the `pd.read_csv()` function.

3. **Install Dependencies:**

```bash
pip install pandas numpy matplotlib seaborn statsmodels
```

4. **Run the Notebook:**  
Open `code.ipynb` and execute the cells to regenerate all figures and statistical summaries.

---

## 7. Conclusion
This study confirms that academic indicators and institutional resources are strong predictors of student financial success. While individual effort is crucial, institutional factors like academic rigor, geographic location, and faculty resources play a measurable role in determining the earning potential of graduates. The OLS model confirms that SAT scores and faculty salaries are among the most statistically significant predictors. Overall, the findings yield resulats that the return on higher education can be shaped 1) student's acumen(denoted by test score) 2) the facaulty investment of the college they study in, 3) which kind of instituion they attend, and finally 4)where the students learn.
---


