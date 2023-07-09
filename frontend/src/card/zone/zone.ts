import {
    LitElement,
    html,
    PropertyValues,
} from "lit";
import {HomeAssistant} from "custom-card-helpers";
import {ZoneDto} from "./dto/zoneDto";
import {localize} from "../../localize/localize";
import {customElement, property} from "lit/decorators.js";
import {remainingTime} from "../../utils/convert/convert";
import {style} from "../../style";
import {CSSResultGroup} from "lit/development";

@customElement('heatger-zone')
export class HeatgerZone extends LitElement {
    @property() public hass!: HomeAssistant;
    @property() public zones: ZoneDto[] = [];
    private blinkBtnEverySeconds: boolean = true;

    constructor() {
        super();
    }

    setZones(zones: ZoneDto[]) {
        this.zones = zones;
    }

    protected updated(_changedProperties: PropertyValues) {
        this.blinkBtnEverySeconds = !this.blinkBtnEverySeconds;
        this.blinkStateButton();
        super.updated(_changedProperties);
    }

    createTextLine = (name: string, value: string) => {
        return html`
            <p class="flex row">
                <span class="grow">${name}</span>
                <span>${value}</span>
            </p>
        `
    }

    createButtonLine = (name: string, value: string, onClick: Function, id: string) => {
        return html`
            <p class="flex row">
                <span class="grow">${name}</span>
                <mwc-button @click='${() => onClick(id)}' class="button btn_zone" id="${id}_${name}">
                    ${value}
                </mwc-button>
            </p>
        `
    }

    setDisableButtonsZone(disable: boolean) {
        const buttons: NodeListOf<HTMLButtonElement> = this.shadowRoot!.querySelectorAll('.btn_zone')
        buttons.forEach((btn) => {
            btn.disabled = disable;
            btn.blur();
        })
    }

    toggleState = (zone: string) => {
        this.setDisableButtonsZone(true)
        void this.hass.callService("mqtt", "publish", {
            topic: `homeassistant/button/${zone}_switch_state/commands`,
        });
    }

    toggleMode = (zone: string) => {
        this.setDisableButtonsZone(true)
        void this.hass.callService("mqtt", "publish", {
            topic: `homeassistant/button/${zone}_switch_mode/commands`,
        });
    }

    blinkStateButton = () => {
        if(this.zones === undefined) return;
        this.zones.forEach((zone) => {
            if(zone.isPing) {
                const button: HTMLButtonElement | null = this.shadowRoot!.querySelector(
                    `#${zone.id}_${localize('panel.prog.state', this.hass.language)}`);
                if(!button) return;
                button.disabled = this.blinkBtnEverySeconds;
            }
        })
    }

    createZone = (zone: ZoneDto) => {
        this.setDisableButtonsZone(false)
        return html`
            <div class="grow">
                <h2>${zone.name}</h2>
                    ${this.createButtonLine(localize('panel.prog.state', this.hass.language),
            localize(`state.${zone.state.toLowerCase()}`, this.hass.language), this.toggleState, zone.id)}
                    ${this.createButtonLine(localize(`card.mode`, this.hass.language),
            localize(`mode.${zone.mode.toLowerCase()}`, this.hass.language), this.toggleMode, zone.id)}
                    ${this.createTextLine(localize('card.timeout', this.hass.language), remainingTime(zone.nextChange))}
            </div>
        `;
    }

    render() {
        return html`
            <div class="flex gap">
                ${this.zones.map((zone) => this.createZone(zone))}
            </div>
        `;
    }

    static get styles(): CSSResultGroup {
        return style;
    }
}