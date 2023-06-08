import {
    LitElement,
    html,
    css,
} from "https://unpkg.com/lit-element@2.0.1/lit-element.js?module";

class HeatgerCard extends LitElement {
    static get properties() {
        return {
            hass: {},
            config: {},
        };
    }

    constructor() {
        super();
        this.timer = null
        this.timeInterval = 1000
        this.startTimer()
        this.zones
    }

    handleFrostFree(ev) {
        ev.preventDefault()
        let dateInput = this.shadowRoot.querySelector('#endDate')
        if(!dateInput) {
            dateInput = { value:'2023-01-01T00:00' }
        }
        if(dateInput.value === '') return
        this.hass.callService("mqtt", "publish", {
            topic: 'homeassistant/button/frostfree/commands',
            payload: dateInput.value

        })
    }

    toHour = (nextChange) => {
        if(nextChange === 'unknown')
            return 'Never'
        let date = new Date(new Date(nextChange).valueOf() - Date.now())
        if (date.getUTCDate() > 10) {
            date = new Date('2023-01-01T00:00:00')
        }
        if (date.getUTCDate() > 1 && date.getUTCDate() < 8) {
            this.setTimeInterval(3600000)
            return `${date.getUTCDate()-1}j ${date.getUTCHours()}h`;
        }
        if (date.getUTCHours() > 0 && date.getUTCDate() === 0) {
            this.setTimeInterval(60000)
            return `${date.getUTCHours()}h ${date.getUTCMinutes()}m`;
        }
        this.setTimeInterval(1000)
        return `${date.getUTCMinutes()}m  ${date.getUTCSeconds()}s`;
    }

    setTimeInterval(interval) {
        if(interval === this.timeInterval) return
        this.timeInterval = interval
        this.stopTimer()
        this.startTimer()
    }

    createTextLine = (name, value) => {
        return html`
            <p class="block row">
                <span class="grow">${name}</span>
                <span>${value}</span>
            </p>
        `
    }

    createButtonLine = (name, value, onClick, param) => {
        return html`
            <p class="block row">
                <span class="grow">${name}</span>
                <mwc-button @click='${() => onClick(param)}' class="button btn_zone" id="${param}_${name}">
                    ${value}
                </mwc-button>
            </p>
        `
    }

    setDisableButtonsZone(disable) {
        const buttons = this.shadowRoot.querySelectorAll('.btn_zone')
        buttons.forEach((btn) => {
            btn.disabled = disable
            btn.rippleHandlers.endFocus()
        })
    }

    toggleState = (zone) => {
        this.setDisableButtonsZone(true)
        this.hass.callService("mqtt", "publish", {
            topic: `homeassistant/button/${zone}_switch_state/commands`,
        })
    }

    toggleMode = (zone) => {
        this.setDisableButtonsZone(true)
        this.hass.callService("mqtt", "publish", {
            topic: `homeassistant/button/${zone}_switch_mode/commands`,
        })
    }

    capitalize = (word) => {
        const lower = word.toLowerCase()
        return word.charAt(0).toUpperCase() + lower.slice(1)
    }

    blinkButton = () => {
        this.zones.forEach((zone) => {
            if(zone.isPing === 'True') {
                const button = this.shadowRoot.querySelector(`#${zone.id}_State`)
                if(!button) return
                button.disabled = !button.disabled
            }
        })
    }

    createZone = (zone) => {
        this.setDisableButtonsZone(false)
        return html`
            <div class="grow">
                <h2>${zone.name}</h2>
                    ${this.createButtonLine('State', this.capitalize(zone.state), this.toggleState, zone.id)}
                    ${this.createButtonLine('Mode', this.capitalize(zone.mode), this.toggleMode, zone.id)}
                    ${this.createTextLine('Timeout', this.toHour(zone.nextChange))}
            </div>
        `;
    }

    startTimer() {
        this.timer = setInterval(() => { this.blinkButton()}, this.timeInterval)
    }

    stopTimer() {
        clearInterval(this.timer)
    }

    render() {
        const zones = []
        var i = 1
        while(this.hass.states[`sensor.zone${i}_name`] != null) {
            zones.push({
                id: `zone${i}`,
                name: this.hass.states[`sensor.zone${i}_name`].state,
                state: this.hass.states[`sensor.zone${i}_state`].state,
                mode: this.hass.states[`sensor.zone${i}_mode`].state,
                nextChange: this.hass.states[`sensor.zone${i}_next_change`].state,
                isPing: this.hass.states[`sensor.zone${i}_is_ping`].state
            })
            i++
        }

        const global = {
            temperature: this.hass.states['sensor.temperature'].state,
            consumption: this.hass.states['sensor.electric_meter'].state,
            frostfreeEndDate: this.hass.states['sensor.frostfree'].state
        }
        this.zones = zones

        if(global.frostfreeEndDate !== 'unknown') {
            console.log(global.frostfreeEndDate)
            return html`
                <ha-card header="Heatger" >
                    <div class="card-content">
                        <div>
                            <h2>Frost-free activated</h2>
                            <div class="block block-center">
                                <div class="row">
                                    <span class="center">${this.toHour(global.frostfreeEndDate)}</span>
                                </div>
                            </div>
                            <div class="block block-center">
                                <div class="row">
                                    <mwc-button @click='${this.handleFrostFree}' class="button" id="stop">
                                        Stop
                                    </mwc-button>
                                </div>
                            </div>   
                        </div>
                    </div>
                </ha-card>
            `
        }

        return html`
            <ha-card header="Heatger" >
                <div class="card-content">
                    <div class="block gap">
                        ${zones.map((zone) => this.createZone(zone))}
                    </div>
                    <div>
                        <hr>
                        <div class="grow">
                            <h2>Frost-free</h2>
                            <form>
                                <div class="grid-container">
                                    <label class="grid-item" for="endDate">End date</label>
                                    <input class="grid-item" type="datetime-local" id="endDate">
                                    <mwc-button @click='${this.handleFrostFree}' class="button grid-item">
                                        Activate
                                    </mwc-button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </ha-card>
        `;
    }

    setConfig(config) {
        this.config = config;
    }

    getCardSize() {
        return 3;
    }

    static get styles() {
        return css`
          .block {
            display: flex;
            justify-content: space-between;
          }
          .block-center {
            justify-content: center !important;
          }
          .row {
            height: 40px;
            margin: 0;
            align-items: center;
          }
          .button {
            margin-right: -0.57em;
          }
          input[type="datetime-local"] {
            height: 40px;
            background-color: var(--card-background-color);
            border: 0;
          }
          .grid-container {
            height: 40px;
            display: grid;
            grid-template-columns: auto auto auto;
            column-gap: 0.5rem;
          }
          .grid-item {
            align-self: center;
          }
          .grow {
            flex-grow: 1;
          }
          .gap {
            gap: 1rem;
          }
          h2, .center {
            text-align: center;
          }
        `;
    }
}

  customElements.define('heatger-card', HeatgerCard);