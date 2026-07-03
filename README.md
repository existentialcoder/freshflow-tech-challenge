# FreshFlow Software Engineer Challenge

## Context

FreshFlow helps grocery stores decide **how much to order** of every fresh-food item, every day. We combine demand forecasts, current inventory, and supplier order windows to produce a recommended order quantity per item.

The `data/` folder contains CSV files for two stores.

## Data

| File | Description |
|---|---|
| `items.csv` | Item catalog — name, category, prices. Shared across stores. |
| `orderable_items.csv` | Per-store, per-day: which items can be ordered and when they'll be delivered. |
| `inventory.csv` | Per-store, per-day: how many pieces are in stock. |
| `order_recommendations.csv` | Per-store, per-day: pre-computed order recommendations with a recommended quantity. |

All quantities are in **pieces**.

## Task

Build a containerized service that exposes API endpoints to:

1. **Load data** — accept the CSV files and ingest them into the service.
2. **Retrieve recommendations** — return order recommendations for a given store and day.

### Requirements

- Python, any web framework
- Containerized: must run with `docker build` + `docker run`

## Submission

Send us a link to your git repository.

---

# Solution
## How to Run

- Build and run the application using a single `docker compose` command that will run the Postgres Database as well

```shell
docker compose up -d --build
```
- Do a restart on the application on any subsequent code changes
```shell
docker compose restart app
```
- To do a clean build and start (incl. DB), run `docker compose down -v`
```shell
docker compose down -v
```
## API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/load-data` | POST | Accepts form-data and specific key-CSV file value pairs |
| `/api/v1/recommendations` | GET | Returns list of recommendations |

### `POST /api/v1/load-data`

`Accept`: `multipart/form-data`

**Request body**
| Field | Type | Description |
|---|---|---|
| `items` | file | Item catalog |
| `orderable_items` | file | Per-store, per-day orderable items |
| `inventory` | file | Per-store, per-day inventory counts |
| `order_recommendations` | file | Per-store, per-day recommendations |

### `GET /api/v1/recommendations`

`Accept`: `application/json`

**Query parameters**
| Param | Type | Required | Description |
|---|---|---|---|
| `store_id` | string | yes | Store to filter by |
| `ordering_day` | date (`YYYY-MM-DD`) | yes | Day to filter by |
| `page` | int | no (default `1`) | Page number |
| `per_page` | int | no (default `10`, max `100`) | Per page |


### Documentation
Refer the [OpenAPI Spec doc](http://localhost:8000/docs) to try out the APIs.
