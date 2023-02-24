# Specter Dataset

## Company Signals Data

- Informative / Firmographic Data
    - ...

- Funding Data
    - ...

- Website / Social Media / App URLs
    - Those with 2-6 months of growth data:
        Web Visits
        Website Popularity Rank
        LinkedIn
        Twitter
        Instagram
        Total App Downloads
        iTunes Reviews
        Google Play Reviews

- Web Data
    - ...

- Team Data
    - Those with 2-6 months of growth data:
        Employees
    - ...

- Social Data
    - ...

- App Data
    - ...
    


## Ranking

**Identify companies that are showing high growth and rank them**

Growth is defined as a company's ability to increase its user base, revenue, or other metrics over time. Ideally we would have revenue data, but we don't. If a company is selling an app, we can use app downloads as a proxy for revenue. If a company is selling a service, we can use web visits as a proxy for revenue. Number of employees can also be used a proxy for revenue.

### Employees

A [2012 blog by ProtoBi](https://protobi.com/post/revenue-per-employee-and-biologic-scaling-laws) shows that the number of employees is a good proxy for revenue. The plot shows that the number of employees is correlated with revenue via a power-law.

![Revenue per Employee](docs/revenue_per_employee.png)

$ ~revenue  ~\alpha  ~employees^{0.77} $

This scaling law basically means that if the number of employees doubles, the revenue goes up by less than 2 (~1.7), i.e. not directly proportional to employee growth. 

One thing to note re. this relationship, it is derived on data for companies with between ~200-100,000 employees and as such, the relationship may not hold for companies with fewer employees.

### App Downloads

App Downloads may be a little more difficult to use as a proxy for revenue as it depends on the type of business.

### Web Visits




Potential growth indicators include increasing:
- Web Visits
- Website Popularity Rank
- Social Media Followers
- App Downloads
- Employees


