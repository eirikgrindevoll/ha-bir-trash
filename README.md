# BIR Trash Collection

Home Assistant integration for [BIR](https://bir.no) (Bergensområdets Interkommunale Renovasjonsselskap) trash pickup schedules.

Creates one sensor per waste fraction showing the next pickup date, with all upcoming dates available as an attribute.

## Sensors

| Fraction | Example sensor name |
|---|---|
| Restavfall | `sensor.bir_restavfall` |
| Matavfall | `sensor.bir_matavfall` |
| Papir | `sensor.bir_papir` |
| Glass og metallemballasje | `sensor.bir_glass_og_metallemballasje` |

Each sensor:
- **State**: next pickup date (`YYYY-MM-DD`)
- **Device class**: `date` (HA displays it as a formatted date)
- **Attribute** `upcoming_dates`: list of all pickup dates within the next 30 days

## Installation

### HACS (recommended)

1. Open HACS → Integrations → ⋮ → Custom repositories
2. Add `https://github.com/eirikgrindevoll/ha-bir-trash` as type **Integration**
3. Install **BIR Trash Collection** and restart Home Assistant

### Manual

1. Copy `custom_components/bir_trash/` into your HA `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **BIR Trash Collection**
3. Fill in the form:
   - **App ID** and **Contractor ID** are pre-filled with the BIR defaults — leave them as-is
   - **Address**: type your street address (e.g. `Vindharpevegen 46 J`)
4. If multiple properties match, select yours from the list

## Requirements

- Home Assistant 2024.1 or newer
- A valid BIR service address in the Bergen region
