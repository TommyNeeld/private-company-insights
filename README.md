# Specter Analysis

## Specrter App

Deployed on AWS App Runner [here](https://iw3awh3exj.eu-west-1.awsapprunner.com/)

### Running the App

Run `src/app.py` and navigate to http://127.0.0.1:8050/ in your browser.

### Deploying & Updating the App - Heroku
**NO LONGER USED**

~~Install dashtools with `pip install dash-tools` and run `dashtools heroku --deploy` to deploy your app and `dashtools heroku --update` to update your app.~~

### Deploying & Updating the App - AWS App Runner

_Heroku deployment had issues, due to being a new account, I could not updgrade to premium tiers and therefore suffered with performance issues._

To deploy on AWS App Runner, first need to push a docker image to ECR. This can be done by running `./build_deploy_image_m1.sh` (for M1 silicon Macs only).

In AWS App Runner, create a new service, and select the ECR image. The service will be created and deployed. Configure to automatically update new versions of the image. As such, to update the app, simply push a new version of the image to ECR by updating `src/version.env` and running `./build_deploy_image_m1.sh` again.

**NOTE:** You may need to run `chmod +x build_deploy_image_m1.sh` to make the script executable.

## Exploration

See `notebooks` for exploratory analysis.

**NOTE:** The folder contains it's own `requirements.txt` file.

### Ranking

**Identify companies that are showing high growth and rank them**

Growth is defined as a company's ability to increase its user base, revenue, or other metrics over time. Ideally we would have revenue data, but we don't. If a company is selling an app, we can use app downloads as a proxy for revenue. If a company is selling a service, we can use web visits as a proxy for revenue. Number of employees can also be used a proxy for revenue.

#### Employees

A [2012 blog by ProtoBi](https://protobi.com/post/revenue-per-employee-and-biologic-scaling-laws) shows that the number of employees is a good proxy for revenue. The plot shows that the number of employees is correlated with revenue via a power-law.

![Revenue per Employee](notebooks/docs/revenue_per_employee.png)

$ ~revenue  ~\alpha  ~employees^{0.77} $

This scaling law basically means that if the number of employees doubles, the revenue goes up by less than 2 (~1.7), i.e. not directly proportional to employee growth. 

One thing to note re. this relationship, it is derived on data for companies with between ~200-100,000 employees and as such, the relationship may not hold for companies with fewer employees.

#### App Downloads

App Downloads may be a little more difficult to use as a proxy for revenue as it depends on the type of business.

#### Web Visits

...


### Industry Classification

**Identify the industry of a company**

Build a taxonomy model that can populate the 'New Industry' column with 'Finance', 'Health', or 'Finance; Health', depending on the following datapoints:
- Description
- Industry
- Category Groups
- Tags

We need a taxonomy classifier with only 3 classes, although it makes sense to add a fourth class for 'Other' or 'Unclassified'.

#### Zero-shot approach

As we have limited data, we can use a zero-shot approach to classify companies into the 3 classes. We can use the [Zero-Shot approach](https://huggingface.co/spaces/joeddav/zero-shot-demo) to do this.

Pros:
- Requires no training
- Works well on common topics

Cons:
- No ability to modify
- Large model - slow to run

**Note:** can also be used to create an initial label set for later use e.g. [this](https://www.vennify.ai/generating-training-data-zero-shot/) article

#### Fine-tuning approach

[SetFit](https://github.com/huggingface/setfit) is a library that allows you to fine-tune a model on a limited set of labels. We can use this to fine-tune a model on the 3 classes.

Pros:
- Shown to be high-performing in the few-shot regime
- Requires limited training data

Cons:
- Requires human-in-the-loop to label
- Large model - slow to run 

#### Naive classifier approach

We have existing industry classifications for 'Finance' and 'Health' related categories. We can use these to train a two classifiers, one for 'Finance' and one for 'Health'. Using the probability scores from these two classifiers, we could classify a company as 'Finance; Health' if the probability scores are above a certain threshold for both classifiers i.e. Finance > 0.5 and Health > 0.5.

|        Industry                          | Count |
|------------------------------------------|-------|
| Financial Services                       | 402   |
| Hospitals and Health Care                | 86    |
| Mental Health Care                       | 34    |
| Health and Human Services                | 1     |
| Retail Health and Personal Care Products | 1     |
| Public Health                            | 1     |

This is naive in the sense that it assumes that these existing related industry classifications are the same as the new industry classifications we are creating. In reality, one could argue they are a sub-industry but it is hard to know what the definition of 'Finance', 'Health' and 'Finance; Health' are without more information and how they relate to these.

Pros:
- Quick to train
- Based on this dataset - more applicable to this task

Cons:
- Very limited training data (~100 for Health)
- Create a fixed view of the world based on related industry classifications

**NOTE**: Under the taxonomy field "Category Groups" there are 29 examples where both of the the words 'health' and 'financial' are used.

| Category                                          | Count |
|---------------------------------------------------|-------|
| Financial Services, Health Care                   | 8     |
| Administrative Services, Financial Services, H... | 4     |
| Financial Services, Health Care, Software         | 2     |
| Financial Services, Health Care, Sports           | 1     |
| Financial Services, Health Care, Lending and I... | 1     |
...

#### Combining taxonomy info

Each company has useful taxonomy categorizing information to hand, these include a company description, an 'old' industry classification, category grouping and tags.



## TODO

### Ranking app
- [x] make a simple dash app
- [x] [deploy](https://dash.plotly.com/deployment)
- [x] analyze potential growth metrics
- [x] preprocess data and generate metrics
- [x] add visualizations for growth metrics
- [x] create interactive components to dig through data
- [x] add password protection
- [ ] further exploration of the approach - see [ranking_exploration notebook](notebooks/ranking_exploration.ipynb)

### Industry classification
- [x] investigate industry classification task
- [x] come up with new industry classification approaches
- [x] implement one approach and analyze results
- [x] embed output in dash app
- [ ] fix zero-shot bug - if the batch contains only one example, the pipeline will miss it
