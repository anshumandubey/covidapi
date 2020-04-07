# COVID-19 API

It provides data of corona virus cases across the globe in JSON format.

A dashboard using this API is made in angular at https://github.com/anshumandubey/covidboard.

## Endpoints

> **[GET]** All data: https://coviddataapi.herokuapp.com/api/all

> **[GET]** All data for specfic country i.e. India: https://coviddataapi.herokuapp.com/api/all?country=india

> **[GET]** All data for specfic date i.e. 22/3/2020: https://coviddataapi.herokuapp.com/api/all?date=22-3

> **[GET]** Last day data for all countries: https://coviddataapi.herokuapp.com/api/lastday

> **[GET]** Last day data for specfic country i.e. India: https://coviddataapi.herokuapp.com/api/lastday?country=india

> **[GET]** Total cases till today: https://coviddataapi.herokuapp.com/api/total

## Response Example

```
[
  {
    "country": "india",
    "date": "2020-1-22",
    "confirmed": 0,
    "deaths": 0,
    "recovered": 0
  },
  {
    "country": "india",
    "date": "2020-1-23",
    "confirmed": 0,
    "deaths": 0,
    "recovered": 0
  },
  {
    "country": "india",
    "date": "2020-1-24",
    "confirmed": 0,
    "deaths": 0,
    "recovered": 0
  }
]
```
  
