# Specter Analysis

## Running the App

Run `src/app.py` and navigate to http://127.0.0.1:8050/ in your browser.

## Deploying & Updating the App - Heroku
**NO LONGER USED**

~~Install dashtools with `pip install dash-tools` and run `dashtools heroku --deploy` to deploy your app and `dashtools heroku --update` to update your app.~~

## Deploying & Updating the App - AWS App Runner

_Heroku deployment had issues, due to being a new account, I could not updgrade to premium tiers and therefore suffered with performance issues._

To deploy on AWS App Runner, first need to push a docker image to ECR. This can be done by running `./build_deploy_image_m1.sh` (for M1 silicon Macs only).

In AWS App Runner, create a new service, and select the ECR image. The service will be created and deployed. Configure to automatically update new versions of the image. As such, to update the app, simply push a new version of the image to ECR by updating `src/version.env` and running `./build_deploy_image_m1.sh` again.

**NOTE:** You may need to run `chmod +x build_deploy_image_m1.sh` to make the script executable.

## Exploration

See `notebooks` for exploratory analysis.

## TODO

### Ranking app
- [x] make a simple dash app
- [x] [deploy](https://dash.plotly.com/deployment)
- [x] add password protection
- [x] analyze potential growth metrics
- [x] preprocess data and generate metrics
- [x] add visualizations for growth metrics
- [x] create interactive components to dig through data

### Industry classification
- [ ] investigate industry classification task
- [ ] develop methods to create a 'health & finance' industry classification
  - [ ] consider keyword list with lexical search
  - [ ] consider fine-tuned sentence transformer (contrastive learning) - [few-shot](https://github.com/huggingface/setfit) with human-in-the-loop
