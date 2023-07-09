import {CSSResultGroup, html, LitElement} from "lit";
import {HomeAssistant, Panel} from "custom-card-helpers";
import {customElement, property} from 'lit/decorators.js';
import {LoginQuery} from "../api/login/query/login_query";
import {isAxiosError} from "axios";
import {localize} from "../../localize/localize";
import {style} from "../../style";

@customElement('heatger-login-card')
export class HeatgerLoginCard extends LitElement {
    @property() public hass!: HomeAssistant;
    @property() public panel!: Panel;
    @property({ type: Boolean, reflect: true }) public narrow!: boolean;
    @property() public reload!: () => void;
    @property() public message: string = '';

    handleConnect(ev: Event) {
        ev.preventDefault()
        const username = this.shadowRoot?.querySelector<HTMLInputElement>('#username')
        const password = this.shadowRoot?.querySelector<HTMLInputElement>('#password')
        if(username && password) {
            LoginQuery(this.hass, {username: username.value, password: password.value}).then(() => {
                this.reload();
            }).catch((e) => {
                if(isAxiosError(e) && e.response) {
                    this.message = e.response.data;
                    this.requestUpdate()
                } else {
                    this.message = localize('panel.login.unknownError', this.hass.language);
                }
            })
        }
    }

    render() {
        return html`
            <ha-card header="Connexion">
                <div class="card-content">
                    <div class="content">
                        <form>
                            <div class="flexRow">
                                <label for="username">${localize('panel.login.username', this.hass.language)}</label>
                                <input type="text" name="username" id="username">
                            </div>
                            <div class="flexRow">
                                <label for="password">${localize('panel.login.password', this.hass.language)}</label>
                                <input type="password" name="password" id="password">
                            </div>
                            <mwc-button @click='${this.handleConnect}' class="button" id="connect">
                                ${localize('panel.login.connect', this.hass.language)}
                            </mwc-button>
                            <p>${this.message}</p>
                        </form>
                    </div>
                </div>
            </ha-card>
        `;
    }

    static get styles(): CSSResultGroup {
        return style;
    }
}