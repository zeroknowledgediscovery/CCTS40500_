
# Problem 

---


## Prediction of the eventual diagnosis of Autism Spectral Disorder (ASD) in US children 

We use  medical history of first 150 weeks for a large cohort of US children between the years 2003 and 2010. The data is an excerpt from an insurance claims database tracking over 200 million people in US over a decade. The files in the `data` folder are preprocessed to highlight different disease categories from ICD9 protocol.

### Data Description

+ Files in `data` folder:

```
Cardiovascular  Hepatic        Musculoskeletal   PNS           Urinary
Development     Immune         Negative          Positive
Digestive       Infectious     Neoplastic        Procedural
Endocrine       Integumentary  Ophthalmological  Reproductive
Hematologic     Metabolic      Otic              Respiratory

```

+ File Description:

```
FNEG26073 000000199 0 0 ... 0 1 .. 2 0 1 ..
MNEG55007 000001238 0 0 ... 0 1 .. 2 0 1 ..
FNEG55007 000001240 0 0 ... 0 1 .. 2 0 1 ..
FNEG26065 000002392 0 0 ... 0 1 .. 2 0 1 ..
MNEG26065 000002393 0 0 ... 0 1 .. 2 0 1 ..
...
FPOS13075 000762662 0 0 ..
MPOS13081 000762886 0 0 ..
FPOS13211 000762972 0 0 ..
```

**Colum 1**: 
F: Female
M: Male
POS: Children with eventual diagnosis of ASD
NEG: Children with no such diagnosis till age 12

26073,55007,... : FIPS code indicating county (first 2 digits are state, next three county in that state)

**Column 2**
Unique patient id

**Column 3 -- end**
+ 0: Healthy week
+ 1: Immunological disease (for this file, for the file "OTIC", this would mean a diagnosis of an otic disease and so on

+ 2: Some diagnoses other than immunological (again for other files such as "OTIC", this means a diagnosis other than the one that particular file targets

---

# Questions:

A. Predict POS for Males using infectious disease history
B. Predict POS for Females using infectious disease history
C. Predict POS for Males/Females using any/all combination of diseases
D. Identify the important/most predictive diseases
E. How does the prediction change if we consider only the first 100 weeks, or first 150 weeks or first 200 weeks.
F. Introduce new features (fraction of time child is sick etc.. be creative), and demonstrate improvement or lack thereof

# Target AUC: 

65%

