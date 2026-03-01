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
   - **Address**: type your street address (e.g. `Storgata 1`)
4. If multiple properties match, select yours from the list

## Removal

1. Go to **Settings → Devices & Services**
2. Find **BIR Trash Collection** and click **⋮ → Delete**
3. Restart Home Assistant
4. Optionally remove `custom_components/bir_trash/` from your `config/` directory

## Requirements

- Home Assistant 2024.1 or newer
- A valid BIR service address in the Bergen region

## Development

This integration depends on the [`birtrashclient`](https://github.com/eirikgrindevoll/birtrashclient) PyPI package.
The pinned version is set in `custom_components/bir_trash/manifest.json`:

```json
"requirements": ["birtrashclient==0.1.4"]
```

**When to update the pinned version:**

- A new stable `birtrashclient` release is published to PyPI
- Update the version in `manifest.json` on the `dev` branch before releasing a new version of this integration
- The release workflow (`release.yml`) will then merge `dev → beta → master` automatically, so the change propagates to all branches

**Release flow:** `dev → beta → master`

Releases are triggered manually via GitHub Actions → **Release** workflow (or `gh workflow run`).
Pre-releases (`dev`/`beta` branches) are only visible to users who opt in to pre-releases in HACS.
