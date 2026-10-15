# Plant Care

Smart watering reminder for Home Assistant based on real soil moisture.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Features

- 💧 Monitors soil moisture via any `sensor` in Home Assistant
- 🔔 Creates a `binary_sensor` that turns `on` when the soil is too dry
- 🎛️ Configurable moisture threshold per plant
- 🪴 Multiple plants — add as many as you want
- 🌍 Localized (English & Russian)
- ⚡ No cloud, no API keys — works entirely locally

## Installation

### HACS (recommended)

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click the three dots in the top-right corner → **Custom repositories**
4. Add `https://github.com/slava87VS/plant_care` as category **Integration**
5. Search for **Plant Care** and install it
6. **Restart Home Assistant**

### Manual

1. Download the `custom_components/plant_care` folder from this repository
2. Copy it into your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Plant Care**
3. Fill in:
   - **Plant name** — e.g. "Monstera"
   - **Soil moisture sensor** — any `sensor` that returns a percentage
   - **Moisture threshold (%)** — the sensor value below which the plant needs water

After setup, you get:

| Entity | Description |
|--------|-------------|
| `binary_sensor.<plant>_needs_water` | `on` = needs water, `off` = OK |

## Automation example

```yaml
automation:
  - alias: "Notify when Monstera needs water"
    trigger:
      - platform: state
        entity_id: binary_sensor.plant_monstera_needs_water
        to: "on"
    action:
      - service: notify.mobile_app_my_phone
        data:
          title: "🌱 Plant needs water"
          message: "Monstera is thirsty!"
```

## License

MIT