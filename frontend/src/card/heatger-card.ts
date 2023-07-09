import {
    LitElement,
    html,
    css,
} from "lit";
import {HomeAssistant} from "custom-card-helpers";
import {customElement, property} from "lit/decorators.js";
import "./frostfree/frostfree"
import "./zone/zone"
import {HassConfig} from "home-assistant-js-websocket/dist/types";
import {ZoneDto} from "./zone/dto/zoneDto";
import {State} from "./enum/state";
import {Mode} from "./enum/mode";
import {HeatgerZone} from "./zone/zone";
import {HeatgerFrostfree} from "./frostfree/frostfree";
import {CSSResultGroup} from "lit/development";

@customElement('heatger-card')
class HeatgerCard extends LitElement {
    @property() public hass!: HomeAssistant;
    @property() public config!: HassConfig;
    private frostFreeActivated = false;
    private AutoUpdateTimer: NodeJS.Timeout | undefined;

    constructor() {
        super();
        this.AutoUpdateTimer = setInterval(() => {
            this.updateComponents();}, 1000);
    }

    activateFrostFree(activate: boolean) {
        this.frostFreeActivated = activate;
        this.requestUpdate();
    }

    getComponents() {
        let zone = html``;
        if(!this.frostFreeActivated) {
            zone = html`
                <heatger-zone .hass="${this.hass}"></heatger-zone>
            `;
        }
        return html`
            ${zone}
            <heatger-frostfree .hass="${this.hass}" .activated="${this.activateFrostFree.bind(this)}"></heatger-frostfree>
        `;
    }

    updateComponents() {
        const zonesDatas: ZoneDto[] = [];
        let i = 1;
        while(this.hass.states[`sensor.zone${i}_name`] != null) {
            zonesDatas.push({
                id: `zone${i}`,
                name: this.hass.states[`sensor.zone${i}_name`].state,
                state: Object.values(State).find(state => state === this.hass.states[`sensor.zone${i}_state`].state) ?? State.COMFORT,
                mode: Object.values(Mode).find(mode => mode === this.hass.states[`sensor.zone${i}_mode`].state) ?? Mode.AUTO,
                nextChange: new Date(this.hass.states[`sensor.zone${i}_next_change`].state),
                isPing: this.hass.states[`sensor.zone${i}_is_ping`].state.toLowerCase() === "true"
            })
            i++
        }
        const heatgerZone = this.shadowRoot!.querySelector('heatger-zone') as HeatgerZone;
        if(heatgerZone) {
            heatgerZone.setZones(zonesDatas);
            if(!this.frostFreeActivated)
                heatgerZone.requestUpdate();
        }

        let frostFreeEndDate: Date | undefined = new Date(this.hass.states['sensor.frostfree'].state);
        if(frostFreeEndDate.toDateString() === 'Invalid Date') {
            frostFreeEndDate = undefined;
        }
        const heatgerFrostfree = this.shadowRoot!.querySelector('heatger-frostfree') as HeatgerFrostfree;
        if(!heatgerFrostfree) return;
        heatgerFrostfree.setEndDate(frostFreeEndDate);
        heatgerFrostfree.requestUpdate();
    }

    render() {
        return html`
            <ha-card header="Heatger" >
                <div class="card-content">
                    ${this.getComponents()}
                </div>
            </ha-card>
        `;
    }

    setConfig(config: HassConfig) {
        this.config = config;
    }

    getCardSize() {
        return 3;
    }

    static get styles(): CSSResultGroup {
        return css``;
    }
}