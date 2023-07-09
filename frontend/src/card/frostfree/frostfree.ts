import {
    LitElement,
    html,
    css, CSSResultGroup,
} from "lit";
import {HomeAssistant} from "custom-card-helpers";
import {localize} from "../../localize/localize";
import {customElement, property} from "lit/decorators.js";
import {remainingTime} from "../../utils/convert/convert";
import {style} from "../../style";
import {STOP_FROSTFREE_PAYLOAD} from "../../panel/consts";

@customElement('heatger-frostfree')
export class HeatgerFrostfree extends LitElement {
    @property() public hass!: HomeAssistant;
    @property() public activated!: (activated: boolean) => void;
    @property() public endDate: Date | undefined;

    handleFrostFree(ev: MouseEvent) {
        ev.preventDefault()
        const dateInput: HTMLInputElement | null = this.shadowRoot!.querySelector('#endDate')
        if(dateInput && dateInput.value === '') return
        void this.hass.callService("mqtt", "publish", {
            topic: 'homeassistant/button/frostfree/commands',
            payload: dateInput?.value ?? STOP_FROSTFREE_PAYLOAD
        });
        this.updateEndDate();
    }

    setEndDate(endDate: Date | undefined) {
        this.endDate = endDate;
        this.updateEndDate();
    }

    updateEndDate() {
        if(this.endDate === undefined) {
            this.activated(false);
        } else {
            this.activated(true);
        }
    }

    render() {
        if(this.endDate !== undefined) {
            return html`
                <div>
                    <h2>${localize("card.frostFree.title", this.hass.language)}</h2>
                    <div class="flex flex-center">
                        <div class="row">
                            <span class="center">${remainingTime(this.endDate)}</span>
                        </div>
                    </div>
                    <div class="flex flex-center">
                        <div class="row">
                            <mwc-button @click='${this.handleFrostFree}' class="button" id="stop">
                                ${localize("card.frostFree.stop", this.hass.language)}
                            </mwc-button>
                        </div>
                    </div>
                </div>
            `
        }

        return html`
            <div class="grow">
                <h2>${localize("card.frostFree.frostFree", this.hass.language)}</h2>
                <form>
                    <div class="grid-container">
                        <label class="grid-item" for="endDate">${localize("card.frostFree.endDate", this.hass.language)}</label>
                        <input class="grid-item" type="datetime-local" id="endDate">
                        <mwc-button @click='${this.handleFrostFree}' class="button grid-item">
                            ${localize("card.frostFree.activate", this.hass.language)}
                        </mwc-button>
                    </div>
                </form>
            </div>
        `;
    }

    static get styles(): CSSResultGroup {
        return css`
          ${style}
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
        `;
    }
}