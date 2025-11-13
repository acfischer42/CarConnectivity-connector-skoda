# Skoda API Endpoints Documentation

This document provides a comprehensive list of all Skoda API endpoints currently used or referenced in the CarConnectivity Skoda connector.

## Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://identity.vwgroup.io/oidc/v1/authorize` | GET | OAuth authorization |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/authentication/exchange-authorization-code?tokenType=CONNECT` | POST | Token exchange |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/authentication/refresh-token?tokenType=CONNECT` | POST | Token refresh |

## User & Garage Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/users` | GET | User information |
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/garage` | GET | List vehicles in garage |
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/garage/vehicles/{vin}?connectivityGenerations=MOD1&connectivityGenerations=MOD2&connectivityGenerations=MOD3&connectivityGenerations=MOD4` | GET | Vehicle details |

## Vehicle Status & Information

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/vehicle-status/{vin}` | GET | Overall vehicle status |
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/vehicle-status/{vin}/driving-range` | GET | Fuel/range information |
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/connection-status/{vin}/readiness` | GET | Connection readiness |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/maps/positions?vin={vin}` | GET | Vehicle position |

## Maintenance & Health

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://mysmob.api.connect.skoda-auto.cz/api/v3/vehicle-maintenance/vehicles/{vin}/report` | GET | Maintenance information |
| ~~`https://mysmob.api.connect.skoda-auto.cz/api/v1/vehicle-health-report/warning-lights/{vin}`~~ | GET | Warning lights *(commented out/unused)* |

## Charging (Electric Vehicles)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/charging/{vin}` | GET | Charging status |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/charging/{vin}/start` | POST | Start charging |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/charging/{vin}/stop` | POST | Stop charging |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/charging/{vin}/set-charge-limit` | PUT | Set charge limit |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/charging/{vin}/set-charging-current` | PUT | Set charging current |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/charging/{vin}/set-auto-unlock-plug` | PUT | Auto unlock plug setting |

## Air Conditioning & Climate

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/air-conditioning/{vin}` | GET | AC/Climate status (includes timers, runningRequests, windowHeating) |
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/air-conditioning/{vin}/start` | POST | Start AC |
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/air-conditioning/{vin}/stop` | POST | Stop AC |
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/air-conditioning/{vin}/settings/target-temperature` | POST | Set target temperature |
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/air-conditioning/{vin}/settings/ac-at-unlock` | POST | AC on unlock setting |
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/air-conditioning/{vin}/start-window-heating` | POST | Start window heating |
| `https://mysmob.api.connect.skoda-auto.cz/api/v2/air-conditioning/{vin}/stop-window-heating` | POST | Stop window heating |

## Vehicle Access & Control

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/vehicle-access/{vin}/lock` | POST | Lock vehicle |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/vehicle-access/{vin}/unlock` | POST | Unlock vehicle |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/vehicle-access/{vin}/honk-and-flash` | POST | Honk and flash |
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/vehicle-wakeup/{vin}?applyRequestLimiter=true` | POST | Wake up vehicle |

## Vehicle Images & Renders

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://mysmob.api.connect.skoda-auto.cz/api/v1/vehicle-information/{vin}/renders` | GET | Vehicle render images |

## Summary Statistics

### By API Version
- **v1**: 13 endpoints (mainly charging, access, position, user, authentication)
- **v2**: 16 endpoints (status, garage, air conditioning, connection)
- **v3**: 1 endpoint (maintenance)

### By HTTP Method
- **GET**: 12 endpoints (status, information, authentication)
- **POST**: 17 endpoints (commands, settings, authentication)
- **PUT**: 3 endpoints (charging settings)

### Total: 30 Active Endpoints + 1 Disabled

## Base URLs
- **Primary API**: `https://mysmob.api.connect.skoda-auto.cz`
- **OAuth Authentication**: `https://identity.vwgroup.io`
- **Vehicle Renders**: `https://iprenders.blob.core.windows.net/` (URLs returned by API)

## Notes
- All vehicle-specific endpoints require VIN parameter
- Most endpoints require OAuth authentication
- One endpoint is currently disabled: `api/v1/vehicle-health-report/warning-lights/{vin}`
- The connector implements comprehensive vehicle functionality including status monitoring, remote control, charging management, climate control, access control, and maintenance information

## Data Availability

### Currently Implemented and Available in raw_api
- Vehicle details and specification
- Maintenance information (inspection and oil service intervals)
- Vehicle status (doors, windows, lights)
- Position and driving range
- Air conditioning status (including timers and running requests)
- Charging information (for electric vehicles)
- Connection status

### Air Conditioning Data Structure (Newly Discovered)
The `/api/v2/air-conditioning/{vin}` endpoint provides comprehensive climate data:
- **Basic Status**: `state`, `steeringWheelPosition`, `carCapturedTimestamp`
- **Temperature**: `outsideTemperature` with unit and timestamp
- **Window Heating**: `windowHeatingState` for front/rear/unspecified
- **Timers**: Array of climate control timers with `id`, `enabled`, `time`, `type`, `selectedDays`
- **Running Requests**: Array of active climate control requests
- **Errors**: Detailed error information (e.g., seat heating API availability)

**Note**: No separate ventilation endpoints exist - all climate functionality (AC, ventilation, heating) is unified through the air-conditioning endpoint.

### Status Renders Available but Not Fully Implemented
- Vehicle status render URLs (lightMode, oneX format)
- Detail renders for specific vehicle states

This API provides comprehensive coverage for modern connected vehicle functionality across Skoda's vehicle lineup.
