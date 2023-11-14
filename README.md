# How to Data Engineer

This repository contains code which will generate a sample real-life data engineering use case.

## Use case description

One of the most common task of a Data Engineer in a tech company is to deal with frontend data.
These kind of data usually share the following:
1. **Volume**: In a medium/big size tech company they can easily rech 100s of GB a day in volume.
2. **Velocity**: They are generated in a streaming fashion and, if freezed, splitted in a huge number of small files
3. **Variety**: Because they are collected directly from the user, they can contain multiple data quality issues that we need to be able to address

In this sample use case we will simulate a few months of front-end data (in `raw_data`) that we will need to properly treat in order to populate a `Grafana` dashboard for business insights.

The infrastructure is provided in different docker containers, and the pipeline is coded under `dags/raw_data_load.py`.

Unfortunately the current pipeline is not able to address different issues which we purposely introduced in the data.

The goal of this workshop would be to edit the pipeline (or the data) in order for the final dashoboard to be correct.

## Requirements

- [Docker](https://www.docker.com/products/docker-desktop/)

## How to run

After having installed Docker you can follow these steps:

1. Activate Docker (simply open the app downloaded above)
2. Clone this repository
3. Open a terminal on windows or mac and position youself inside this repo
4. Perform a `docker compose up airflow-init` which will initialize and download the images
5. Perform a `docker compose up` which will start the containers (note that the terminal will stay attached to the working process, so dont expect it to "terminate the command")

After these 5 steps you should be able to reach the following services from your browser:

- [pgAdmin4](http://localhost:15432/browser/) which will allow us to look into the database, simply open the link, insert the following
    ```
    email: admin@admin.com
    password: admin
    ```

    After opening the app you should see on the left a `> Servers` tab, which when open will prompt for a password
    ```
    server password: airflow
    ```

    You will find two databases, the one we are interested in is called `postgres` in which you will find a table `raw_data` under `public` schema

- [Airflow](http://localhost:8080/) which is the DAG scheduler, simply open the link, insert the following
    ```
    username: admin
    password: admin
    ```
    and you should find a DAG called `raw_data_load`

- [Grafana](http://localhost:3111/) which is the dashbording app, simply open the link, insert the following
    ```
    username: admin
    password: admin
    ```
    and you should find a dashboard called `airflow` (on the left side you can navigate to dashboards)
    **NOTE** that the dashboard will be empty at the beginning because we still need to activate the pipeline to populate it.

## What to do

Before starting the last thing that we need to do is to activate the pipeline. To do this you can just click in the toggle at the left of the **raw_data_load** pipeline in the [Airflow](http://localhost:8080/) dashboard.

Now that everything is up to speed you should be able to see from the dashboard that there are different issues with the data (reported below). 

Your goal would be to edit the file `dags/raw_data_load.py` in order to fix the issues and recompute the data.

Not that when you edit the pipeline file you don't need to stop and start the docker container as it will be updated automatically, you can just restart the pipeline by `clearing` the state of the current execution. This can be achieved directly from the airflow dashboard.


## Issues to solve (from easier to harder)

1. Easy - Wrong value for device type `@#$%$^#!^$!#`
2. Easy - Multiple simiar values which should be merged (`iphone` and `Iphone`)
3. Mid - Missing dates for november
4. Mid - Missing dates for few days in october
5. Hard - If re-run, the pipeline simply append data making that not-idempotent